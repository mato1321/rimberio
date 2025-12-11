# main.py
import os
import sys
from dotenv import load_dotenv

# 載入 .env 環境變數
load_dotenv()

from fastapi import FastAPI, Request, HTTPException
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
    PostbackEvent, TemplateSendMessage, ButtonsTemplate, PostbackAction,
    FlexSendMessage, BubbleContainer, ImageComponent, BoxComponent, TextComponent
)

# 匯入我們寫好的資料模型
import data_model

# --- 設定 ---
app = FastAPI()

# 從環境變數讀取 Token (對應 .env 檔案)
channel_secret = os.getenv('LINE_CHANNEL_SECRET')
channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN')

if channel_secret is None or channel_access_token is None:
    print("錯誤：找不到 .env 設定，請確認檔案是否存在。")
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)

# --- 🧠 記憶體 (暫存使用者狀態) ---
# 注意：這只是暫存在記憶體中，重啟伺服器會消失。
# 結構: { 'user_id': { 'step': 0, 'vector': [0.5, 0.5...] } }
user_sessions = {}

# --- 輔助函式：發送題目 ---
def send_question(user_id, question_index):
    # 取得題目資料
    if question_index >= len(data_model.QUESTIONS):
        return # 超出範圍

    q_data = data_model.QUESTIONS[question_index]
    
    # 建立選項按鈕
    actions = []
    for option in q_data['options']:
        # Postback data 格式: "index=0&value=0.9"
        # 這樣我們才知道是回答哪一題、幾分
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

# --- 輔助函式：顯示推薦結果 ---
def show_recommendation(user_id, user_vector):
    # 1. 呼叫 ChromaDB 計算相似度
    recommendations = data_model.get_recommendations(user_vector, n_results=3)
    
    # 2. 構建回覆文字 (未來可升級為 Flex Message)
    reply_text = "🎉 RIMBERIO 推薦結果出爐！\n"
    reply_text += "根據你的生活型態，最適合你的夥伴是：\n\n"
    
    for i, pet in enumerate(recommendations):
        # 分數轉換：距離越小越相似 (1 - distance)
        match_score = int((1 - pet['score']) * 100)
        # 避免分數變負數
        match_score = max(0, match_score)
        
        reply_text += f"🏆 第 {i+1} 名：{pet['name']}\n"
        reply_text += f"❤️ 速配指數：{match_score}%\n"
        reply_text += f"📝 {pet['desc']}\n"
        reply_text += "--------------------\n"
        
    reply_text += "\n想要重新測驗嗎？請輸入「開始」。"
    
    line_bot_api.push_message(user_id, TextSendMessage(text=reply_text))


# --- FastAPI 路由 ---
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

# --- LINE 事件處理邏輯 ---

# 1. 處理文字訊息 (啟動測驗)
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg = event.message.text.strip()
    user_id = event.source.user_id
    
    # 簡單的啟動邏輯
    if msg == "開始" or msg == "測驗" or msg == "開始測驗":
        # 初始化使用者狀態
        # 預設 6 個維度都是 0.5 (中庸)
        user_sessions[user_id] = {
            'step': 0, 
            'vector': [0.5] * 6 
        }
        
        reply = "🐶 歡迎來到 RIMBERIO！\n我們將透過 6 個問題，幫你找到靈魂伴侶。\n\n準備好了嗎？讓我們開始吧！"
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply))
        
        # 發送第一題
        send_question(user_id, 0)
        
    else:
        # 其他對話的回應
        reply = "你好！輸入「開始」可以進行寵物配對測驗喔！"
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply))

# 2. 處理 Postback 事件 (使用者點擊按鈕後)
@handler.add(PostbackEvent)
def handle_postback(event):
    user_id = event.source.user_id
    data = event.postback.data # 例如: "index=0&value=0.9"
    
    # 解析回傳資料
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
        # 還有題目，繼續問
        send_question(user_id, next_step)
    else:
        # 題目問完了，顯示結果
        # 取得最終向量
        final_vector = user_sessions[user_id]['vector']
        print(f"User {user_id} vector: {final_vector}") # 方便你在終端機除錯
        
        show_recommendation(user_id, final_vector)
        
        # 清除狀態 (可選)
        # del user_sessions[user_id]