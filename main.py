import os
import sys
from dotenv import load_dotenv
from fastapi import FastAPI, Request, HTTPException
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
    PostbackEvent, TemplateSendMessage, ButtonsTemplate, PostbackAction,
    FlexSendMessage, BubbleContainer, ImageComponent, BoxComponent, TextComponent
)
import data_model

load_dotenv()
app = FastAPI()
channel_secret = os.getenv('LINE_CHANNEL_SECRET')
channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN')
if channel_secret is None or channel_access_token is None:
    print("錯誤：找不到 .env 設定，請確認檔案是否存在。")
    sys.exit(1)
line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)
user_sessions = {}  # 存放使用者測驗進度與向量

def send_question(user_id, question_index):
    if question_index >= len(data_model.QUESTIONS):
        return # 超出範圍
    q_data = data_model.QUESTIONS[question_index]
    actions = []

    for option in q_data['options']:
        # Postback data 格式: "index=0&value=0.9"
        data_str = f"index={question_index}&value={option['value']}"
        actions.append(
            PostbackAction(
                label=option['label'], # 按鈕上顯示的文字
                display_text=option['text'], # 點擊後使用者會說出的話
                data=data_str # 隱藏回傳給伺服器的資料
            )
        )

    # 建立按鈕樣板訊息
    template_message = TemplateSendMessage(
        alt_text=q_data['text'], # 電腦版顯示的替代文字
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
    reply_text = "推薦結果出爐！\n"
    reply_text += "根據你的生活型態，最適合你的夥伴是：\n\n"
    
    for i, pet in enumerate(recommendations):
        match_score = int((1 - pet['score']) * 100) # 距離越小越相似
        match_score = max(0, match_score)
        reply_text += f"第 {i+1} 名：{pet['name']}\n"
        reply_text += f"速配指數：{match_score}%\n"
        reply_text += f"{pet['desc']}\n"
        reply_text += "--------------------\n"
    reply_text += "\n想要重新測驗請輸入「開始」。"
    line_bot_api.push_message(user_id, TextSendMessage(text=reply_text))


# FastAPI 路由設定
@app.get("/")
def read_root():
    return {"status": "RIMBERIO Bot is running!"}

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
    
    # 簡單的啟動邏輯
    if msg == "開始" or msg == "測驗" or msg == "開始測驗":
        # 初始化使用者狀態
        user_sessions[user_id] = {
            'step': 0, 
            'vector': [0.5] * 6 
        }
        
        reply = "歡迎來到 RIMBERIO！\n我們將透過 6 個問題，幫你找到靈魂伴侶。\n"
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply))
        send_question(user_id, 0)
    else:
        reply = "輸入「開始」可以進行寵物配對測驗"
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply))

# 處理使用者點擊按鈕後的事件
@handler.add(PostbackEvent)
def handle_postback(event):
    user_id = event.source.user_id
    data = event.postback.data     # 例如: "index=0 & value=0.9"
    params = dict(item.split('=') for item in data.split('&'))
    q_index = int(params['index'])
    val = float(params['value'])

    # 檢查使用者是否存在 session 中
    if user_id not in user_sessions:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="連線逾時，請輸入「開始」重新測驗。"))
        return

    # 更新向量分數
    # 取得這一題對應哪一個維度 (例如 Q1 對應 Activity)
    dim_index = data_model.QUESTIONS[q_index]['dimension_index']
    user_sessions[user_id]['vector'][dim_index] = val
    
    # 進入下一題
    next_step = q_index + 1
    user_sessions[user_id]['step'] = next_step
    
    if next_step < len(data_model.QUESTIONS):
        send_question(user_id, next_step)
    else:
        # 題目問完了，顯示結果，並且取得最終向量
        final_vector = user_sessions[user_id]['vector']
        print(f"User {user_id} vector: {final_vector}") # 方便你在終端機除錯
        show_recommendation(user_id, final_vector)