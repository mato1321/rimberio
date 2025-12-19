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
app = FastAPI()
channel_secret = os.getenv('LINE_CHANNEL_SECRET')
channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN')
cloudinary_cloud_name = os.getenv('CLOUDINARY_CLOUD_NAME')
cloudinary_api_key = os.getenv('CLOUDINARY_API_KEY')
cloudinary_api_secret = os.getenv('CLOUDINARY_API_SECRET')

if channel_secret is None or channel_access_token is None:  
    print("錯誤：找不到 .env 設定，請確認檔案是否存在。")
    sys.exit(1)

# 設定 Cloudinary
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
    """
    計算每個維度的加權平均值
    """
    final_vector = []
    for dim_index in range(6):
        answers = user_session['dimension_answers'][dim_index]
        weights = user_session['dimension_weights'][dim_index]
        
        if len(answers) == 0:
            final_vector.append(0.5)
        else:
            weighted_sum = sum(a * w for a, w in zip(answers, weights))
            total_weight = sum(weights)
            dimension_value = weighted_sum / total_weight
            # Clamp to [0.0, 1.0] range for safety (though values should already be within bounds)
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
            title=f"問題 {question_index + 1}",
            text=q_data['text'],
            actions=actions
        )
    )
    
    line_bot_api.push_message(user_id, template_message)

# 顯示推薦結果
def show_recommendation(user_id, user_vector):
    recommendations = data_model.get_recommendations(user_vector, n_results=3)
    reply_text = "推薦結果出爐\n"
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
    for pet in recommendations[:  3]:  
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

# FastAPI 路由設定
@app.get("/")
def read_root():
    return {"status": "RIMBERIO Bot is running! "}

@app.post("/callback")
async def callback(request: Request):
    signature = request.headers.get('X-Line-Signature', '')
    body = await request.body()
    body_decoded = body.decode('utf-8')

    try:
        handler.handle(body_decoded, signature)
    except InvalidSignatureError:
        raise HTTPException(status_code=400, detail="Invalid signature")

    return "OK"

# 啟動測驗
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg = event.message.text.strip()
    user_id = event.source.user_id
    
    if msg == "開始" or msg == "測驗" or msg == "開始測驗":  
        # 初始化使用者狀態
        user_sessions[user_id] = {
            'step': 0,
            'vector': [0.5] * 6,
            'dimension_answers': {i: [] for i in range(6)},
            'dimension_weights': {i: [] for i in range(6)}
        }
        
        reply = "歡迎來到 RIMBERIO！\n我們將透過 30 個問題，幫你找到靈魂伴侶。\n準備好了嗎？"
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply))
        send_question(user_id, 0)
    else:
        reply = "輸入「開始」可以進行寵物配對測驗"
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply))

# 處理使用者點擊按鈕後的事件
@handler.add(PostbackEvent)
def handle_postback(event):
    user_id = event.source.user_id
    data = event.postback.data
    params = dict(item.split('=') for item in data.split('&'))
    q_index = int(params['index'])
    val = float(params['value'])

    # 檢查使用者是否存在 session 中
    if user_id not in user_sessions:  
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="連線逾時，請輸入「開始」重新測驗。"))
        return

    # 累加答案和權重
    question = data_model.QUESTIONS[q_index]
    dim_index = question['dimension_index']
    weight = question['weight']
    
    user_sessions[user_id]['dimension_answers'][dim_index].append(val)
    user_sessions[user_id]['dimension_weights'][dim_index].append(weight)
    
    # 進入下一題
    next_step = q_index + 1
    user_sessions[user_id]['step'] = next_step
    
    if next_step < len(data_model.QUESTIONS):
        send_question(user_id, next_step)
    else:
        # 題目問完了，計算加權平均並顯示結果
        final_vector = calculate_weighted_average(user_sessions[user_id])
        user_sessions[user_id]['vector'] = final_vector
        print(f"User {user_id} vector: {final_vector}")
        show_recommendation(user_id, final_vector)