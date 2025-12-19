import os
import sys
import tempfile
from dotenv import load_dotenv
from fastapi import FastAPI, Request, HTTPException
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
    PostbackEvent, TemplateSendMessage, ButtonsTemplate, PostbackAction,
    ImageSendMessage
)
import data_model
import generate_radar_chart

load_dotenv()

# 在啟動時驗證問卷配置
data_model.validate_questions_weights()

app = FastAPI()

# 配置環境變數（添加預設值，避免缺失 .env 時崩潰）
channel_secret = os.getenv('LINE_CHANNEL_SECRET', 'test_secret_key_12345')
channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', 'test_access_token_67890')
cloudinary_cloud_name = os.getenv('CLOUDINARY_CLOUD_NAME')
cloudinary_api_key = os.getenv('CLOUDINARY_API_KEY')
cloudinary_api_secret = os.getenv('CLOUDINARY_API_SECRET')

# 設定 Cloudinary
if cloudinary_cloud_name and cloudinary_api_key and cloudinary_api_secret:
    generate_radar_chart.set_cloudinary_credentials(
        cloudinary_cloud_name,
        cloudinary_api_key,
        cloudinary_api_secret
    )
    print("Cloudinary 認證已設定")
else:
    print("⚠️ Cloudinary 認證未設定，圖表無法上傳")

# 初始化 LINE Bot
line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)
user_sessions = {}  # 存放使用者測驗進度與向量

# ============================================
# 輔助函數
# ============================================

def calculate_weighted_average(user_session):
    """
    計算每個維度的加權平均值
    
    : param user_session: 用戶的 session 數據
    :return: 6 維的最終向量 [0.0-1.0]
    """
    final_vector = []
    
    for dim_index in range(6):
        answers = user_session.get('dimension_answers', {}).get(dim_index, [])
        weights = user_session.get('dimension_weights', {}).get(dim_index, [])
        
        # 安全檢查
        if not answers or not weights: 
            # 如果沒有答案，使用中位值 0.5
            final_vector.append(0.5)
        elif len(answers) != len(weights):
            # 答案數和權重數不匹配（不應該發生）
            print(f"警告：維度 {dim_index} 答案數({len(answers)})和權重數({len(weights)})不匹配")
            final_vector.append(0.5)
        else:
            # 計算加權平均
            weighted_sum = sum(a * w for a, w in zip(answers, weights))
            total_weight = sum(weights)
            
            # 驗證權重總和應為 1.0
            if abs(total_weight - 1.0) > 0.01:  # 允許浮點誤差
                print(f"警告：維度 {dim_index} 的權重總和為 {total_weight}，不等於 1.0")
            
            dimension_value = weighted_sum / total_weight if total_weight > 0 else 0.5
            
            # 確保值在 [0.0, 1.0] 範圍內
            dimension_value = max(0.0, min(1.0, dimension_value))
            final_vector.append(dimension_value)
    
    return final_vector


def send_question(user_id, question_index):
    """發送問題給用戶"""
    if question_index >= len(data_model.QUESTIONS):
        return
    
    q_data = data_model.QUESTIONS[question_index]
    actions = []

    for option in q_data['options']: 
        data_str = f"index={question_index}&value={option['value']}"
        actions.append(
            PostbackAction(
                label=option['label'],
                display_text=option['text'],
                data=data_str
            )
        )

    template_message = TemplateSendMessage(
        alt_text=q_data['text'],
        template=ButtonsTemplate(
            title=f"問題 {question_index + 1}/30",
            text=q_data['text'],
            actions=actions
        )
    )
    
    line_bot_api.push_message(user_id, template_message)


def show_recommendation(user_id, user_vector):
    """顯示推薦結果"""
    recommendations = data_model.get_recommendations(user_vector, n_results=3)
    reply_text = "🎉 推薦結果出爐\n"
    reply_text += "根據你的生活型態，最適合你的夥伴是：\n\n"
    
    for i, pet in enumerate(recommendations):
        match_score = int((1 - pet['score']) * 100)
        match_score = max(0, match_score)
        reply_text += f"第 {i+1} 名：{pet['name']}\n"
        reply_text += f"速配指數：{match_score}%\n"
        reply_text += f"{pet['desc']}\n\n"
    
    reply_text += "想要重新測驗請輸入「開始」。"
    line_bot_api.push_message(user_id, TextSendMessage(text=reply_text))
    
    # 生成雷達圖表
    pet_vectors_dict = {}
    for pet in recommendations[: 3]:  
        for p in data_model.PET_DB:
            if p['name'] == pet['name']:
                pet_vectors_dict[pet['name']] = p['vector']
                break
    
    try:
        # 生成圖表並上傳到 Cloudinary
        cloud_url = generate_radar_chart.generate_radar_chart(user_vector, pet_vectors_dict)
        
        if cloud_url:
            print(f"✅ 圖表已上傳到 Cloudinary:  {cloud_url}")
            
            # 推送圖表給使用者
            line_bot_api.push_message(
                user_id,
                ImageSendMessage(
                    original_content_url=cloud_url,
                    preview_image_url=cloud_url
                )
            )
        else:
            print("❌ 圖表上傳失敗")
            line_bot_api.push_message(
                user_id,
                TextSendMessage(text="圖表生成失敗，但推薦結果已顯示。")
            )
            
    except Exception as e:  
        print(f"❌ 圖表生成或上傳失敗: {e}")
        line_bot_api.push_message(
            user_id,
            TextSendMessage(text="圖表生成失敗，但推薦結果已顯示。")
        )

# ============================================
# FastAPI 路由
# ============================================

@app.get("/")
def read_root():
    """健康檢查端點"""
    return {"status": "RIMBERIO Bot is running! "}


@app.post("/callback")
async def callback(request:  Request):
    """LINE Webhook 回調端點"""
    signature = request.headers.get('X-Line-Signature', '')
    body = await request.body()
    body_decoded = body.decode('utf-8')

    try:
        handler.handle(body_decoded, signature)
    except InvalidSignatureError as e:
        print(f"❌ 簽名驗證失敗: {e}")
        raise HTTPException(status_code=400, detail="Invalid signature")
    except Exception as e:
        print(f"❌ 回調處理錯誤:  {e}")
        raise HTTPException(status_code=500, detail=str(e))

    return "OK"

# ============================================
# LINE Bot 事件處理器
# ============================================

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    """處理用戶傳送的文字訊息"""
    msg = event.message.text. strip()
    user_id = event.source.user_id
    
    if msg == "開始" or msg == "測驗" or msg == "開始測驗":  
        # 初始化使用者狀態
        user_sessions[user_id] = {
            'step': 0,
            'vector': [0.0] * 6,
            'dimension_answers': {i: [] for i in range(6)},
            'dimension_weights': {i: [] for i in range(6)}
        }
        
        print(f"✅ 使用者 {user_id} 開始測驗")
        
        reply = "歡迎來到 RIMBERIO！🐾\n我們將透過 30 個問題，幫你找到靈魂伴侶。\n準備好了嗎？"
        line_bot_api. reply_message(event.reply_token, TextSendMessage(text=reply))
        
        # 發送第一題
        send_question(user_id, 0)
    else:
        reply = "輸入「開始」可以進行寵物配對測驗 🐶🐱"
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply))


@handler.add(PostbackEvent)
def handle_postback(event):
    """處理用戶點擊按鈕後的事件"""
    user_id = event.source.user_id
    data = event.postback.data
    
    try:
        params = dict(item.split('=') for item in data.split('&'))
        q_index = int(params['index'])
        val = float(params['value'])
    except (ValueError, KeyError) as e:
        print(f"❌ 解析 Postback 數據失敗: {e}")
        return

    # 檢查使用者是否存在 session 中
    if user_id not in user_sessions:  
        print(f"⚠️ 使用者 {user_id} session 不存在，請求重新開始")
        line_bot_api.reply_message(
            event.reply_token, 
            TextSendMessage(text="連線逾時，請輸入「開始」重新測驗。")
        )
        return

    # 累加答案和權重（不再直接覆蓋）
    dim_index = data_model.QUESTIONS[q_index]['dimension_index']
    weight = data_model.QUESTIONS[q_index]. get('weight', 0.2)
    
    user_sessions[user_id]['dimension_answers'][dim_index].append(val)
    user_sessions[user_id]['dimension_weights'][dim_index].append(weight)
    
    print(f"✅ 使用者 {user_id} 回答第 {q_index + 1} 題，維度 {dim_index}，值 {val}")
    
    # 進入下一題
    next_step = q_index + 1
    user_sessions[user_id]['step'] = next_step
    
    if next_step < len(data_model.QUESTIONS):
        send_question(user_id, next_step)
    else:
        # 題目問完了，計算最終向量並顯示結果
        print(f"✅ 使用者 {user_id} 已完成所有 30 道題目，開始計算結果...")
        
        final_vector = calculate_weighted_average(user_sessions[user_id])
        user_sessions[user_id]['vector'] = final_vector
        
        print(f"📊 使用者 {user_id} 的最終向量:  {final_vector}")
        
        show_recommendation(user_id, final_vector)