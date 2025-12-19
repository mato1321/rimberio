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
data_model.validate_questions_weights()
data_model.validate_pet_types()
app = FastAPI()

# 配置環境變數
channel_secret = os.getenv('LINE_CHANNEL_SECRET', 'test_secret_key_12345')
channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', 'test_access_token_67890')
cloudinary_cloud_name = os.getenv('CLOUDINARY_CLOUD_NAME')
cloudinary_api_key = os.getenv('CLOUDINARY_API_KEY')
cloudinary_api_secret = os.getenv('CLOUDINARY_API_SECRET')
if cloudinary_cloud_name and cloudinary_api_key and cloudinary_api_secret:
    generate_radar_chart.set_cloudinary_credentials(
        cloudinary_cloud_name,
        cloudinary_api_key,
        cloudinary_api_secret
    )
    print("Cloudinary 認證已設定")
else:
    print("Cloudinary 認證未設定，圖表無法上傳")
line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)
user_sessions = {}  # 存放使用者測驗進度與向量

def calculate_weighted_average(user_session):
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


def show_recommendation(user_id, user_vector, pet_type='all'):
    # 根據寵物類型獲取推薦
    if pet_type == 'dog':
        recommendations_all = data_model.get_recommendations_with_type(user_vector, n_results=3, pet_type='dog')
        type_emoji = ""
        type_text = "犬種"
    elif pet_type == 'cat':
        recommendations_all = data_model.get_recommendations_with_type(user_vector, n_results=3, pet_type='cat')
        type_emoji = ""
        type_text = "貓種"
    else:  # all
        recommendations_all = data_model.get_recommendations(user_vector, n_results=3)
        type_emoji = ""
        type_text = "寵物"
    
    # 組建回覆消息
    reply_text = "推薦結果出爐\n"
    reply_text += f"根據你的生活型態，最適合你的{type_text}是：\n\n"
    
    # 顯示所有推薦
    for i, pet in enumerate(recommendations_all):
        match_score = int((1 - pet['score']) * 100)
        match_score = max(0, match_score)
        pet_emoji = "" if pet.get('type') == 'dog' else ""
        reply_text += f"第 {i+1} 名：{pet_emoji} {pet['name']}\n"
        reply_text += f"速配指數：{match_score}%\n"
        reply_text += f"{pet['desc']}\n\n"
    
    # 添加分類推薦（只在選擇「都可以」時顯示）
    if pet_type == 'all':
        reply_text += "━━━━━━━━━━━━━━━━━━━\n"
        reply_text += "分類推薦\n\n"
        
        dog_recommendations = data_model.get_recommendations_with_type(user_vector, n_results=1, pet_type='dog')
        cat_recommendations = data_model.get_recommendations_with_type(user_vector, n_results=1, pet_type='cat')
        
        if dog_recommendations: 
            dog = dog_recommendations[0]
            dog_score = int((1 - dog['score']) * 100)
            dog_score = max(0, dog_score)
            reply_text += f"   最佳犬種：{dog['name']}\n"
            reply_text += f"   速配指數：{dog_score}%\n"
            reply_text += f"   {dog['desc']}\n\n"
        
        if cat_recommendations:
            cat = cat_recommendations[0]
            cat_score = int((1 - cat['score']) * 100)
            cat_score = max(0, cat_score)
            reply_text += f"  最佳貓種：{cat['name']}\n"
            reply_text += f"   速配指數：{cat_score}%\n"
            reply_text += f"   {cat['desc']}\n\n"
    
    reply_text += "想要重新測驗請輸入「開始」。"
    line_bot_api.push_message(user_id, TextSendMessage(text=reply_text))
    
    # 生成雷達圖表
    pet_vectors_dict = {}
    for pet in recommendations_all[: 3]:  
        for p in data_model.PET_DB:
            if p['name'] == pet['name']:
                pet_vectors_dict[pet['name']] = p['vector']
                break
    
    try:
        # 生成圖表並上傳到 Cloudinary
        cloud_url = generate_radar_chart.generate_radar_chart(user_vector, pet_vectors_dict)
        
        if cloud_url:
            print(f"圖表已上傳到 Cloudinary:  {cloud_url}")
            
            # 推送圖表給使用者
            line_bot_api.push_message(
                user_id,
                ImageSendMessage(
                    original_content_url=cloud_url,
                    preview_image_url=cloud_url
                )
            )
        else:
            print("圖表上傳失敗")
            line_bot_api.push_message(
                user_id,
                TextSendMessage(text="圖表生成失敗，但推薦結果已顯示。")
            )
            
    except Exception as e:  
        print(f"圖表生成或上傳失敗: {e}")
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
    msg = event.message.text.strip()
    user_id = event.source.user_id
    
    if msg == "開始" or msg == "測驗" or msg == "開始測驗":  
        # 詢問寵物類型
        print(f"使用者 {user_id} 開始測驗，等待選擇寵物類型")
        
        reply = "歡迎來到 RIMBERIO！\n請選擇你想要的寵物類型："
        
        buttons_template = TemplateSendMessage(
            alt_text="選擇寵物類型",
            template=ButtonsTemplate(
                title="寵物類型選擇",
                text="你想找一個什麼樣的寵物？",
                actions=[
                    PostbackAction(
                        label="我想要狗狗",
                        display_text="我想要狗狗",
                        data="pet_type=dog"
                    ),
                    PostbackAction(
                        label="我想要貓咪",
                        display_text="我想要貓咪",
                        data="pet_type=cat"
                    ),
                    PostbackAction(
                        label="都可以",
                        display_text="都可以",
                        data="pet_type=all"
                    )
                ]
            )
        )
        
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply))
        line_bot_api.push_message(user_id, buttons_template)
        
        # 初始化寵物類型選擇狀態
        user_sessions[user_id] = {
            'step': -1,  # -1 表示等待選擇寵物類型
            'pet_type': None,
            'vector':  [0.0] * 6,
            'dimension_answers': {i: [] for i in range(6)},
            'dimension_weights': {i: [] for i in range(6)}
        }
    else:
        reply = "輸入「開始」可以進行寵物配對測驗 🐶🐱"
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply))


@handler.add(PostbackEvent)
def handle_postback(event):
    user_id = event.source.user_id
    data = event.postback.data
    
    try:
        params = dict(item.split('=') for item in data.split('&'))
    except (ValueError, KeyError) as e:
        print(f"解析 Postback 數據失敗: {e}")
        return

    # ==================== 檢查是否在選擇寵物類型 ====================
    if 'pet_type' in params:
        pet_type = params['pet_type']
        
        if user_id not in user_sessions: 
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="連線逾時，請輸入「開始」重新開始。")
            )
            return
        
        # 保存寵物類型選擇
        user_sessions[user_id]['pet_type'] = pet_type
        user_sessions[user_id]['step'] = 0
        
        print(f"使用者 {user_id} 選擇寵物類型:  {pet_type}")
        
        # 根據選擇顯示不同的歡迎訊息
        if pet_type == 'dog':
            welcome_msg = "你選擇了狗狗！\n\n我們將透過 12 個問題，幫你找到最適合的狗狗夥伴。\n準備好了嗎？"
        elif pet_type == 'cat':
            welcome_msg = "你選擇了貓咪！\n\n我們將透過 12 個問題，幫你找到最適合的貓咪夥伴。\n準備好了嗎？"
        else:  # pet_type == 'all'
            welcome_msg = "你選擇了都可以！\n\n我們將透過 12 個問題，幫你找到最適合的寵物伴侶。\n準備好了嗎？"
        
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=welcome_msg)
        )
        
        # 開始發送第一題
        send_question(user_id, 0)
        return

    # ==================== 檢查是否在回答問題 ====================
    if 'index' in params and 'value' in params:
        q_index = int(params['index'])
        val = float(params['value'])
        
        # 檢查使用者是否存在 session 中
        if user_id not in user_sessions:  
            print(f"使用者 {user_id} session 不存在，請求重新開始")
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="連線逾時，請輸入「開始」重新測驗。")
            )
            return
        
        # 累加答案和權重（不再直接覆蓋）
        dim_index = data_model.QUESTIONS[q_index]['dimension_index']
        weight = data_model.QUESTIONS[q_index].get('weight', 0.2)
        user_sessions[user_id]['dimension_answers'][dim_index].append(val)
        user_sessions[user_id]['dimension_weights'][dim_index].append(weight)
        
        print(f"使用者 {user_id} 回答第 {q_index + 1} 題，維度 {dim_index}，值 {val}")
        
        # 進入下一題
        next_step = q_index + 1
        user_sessions[user_id]['step'] = next_step
        
        if next_step < len(data_model.QUESTIONS):
            send_question(user_id, next_step)
        else:
            # 題目問完了，計算最終向量並顯示結果
            print(f"使用者 {user_id} 已完成所有 12 道題目，開始計算結果...")
            
            final_vector = calculate_weighted_average(user_sessions[user_id])
            user_sessions[user_id]['vector'] = final_vector
            
            # 獲取使用者選擇的寵物類型
            pet_type_choice = user_sessions[user_id].get('pet_type', 'all')
            
            print(f"使用者 {user_id} 的最終向量: {final_vector}")
            print(f"寵物類型選擇:  {pet_type_choice}")
            
            show_recommendation(user_id, final_vector, pet_type_choice)