# 🐾 RIMBERIO - 寵物媒合推薦系統

![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=flat-square&logo=python&logoColor=ffffff)
![FastAPI](https://img.shields.io/badge/FastAPI-0.124.2-009485?style=flat-square&logo=fastapi)
![LINE Bot](https://img.shields.io/badge/LINE-Bot%20SDK-00B900?style=flat-square&logo=line)
![ChromaDB](https://img.shields.io/badge/ChromaDB-Vector%20DB-green?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)

**RIMBERIO** 是一個基於 LINE Chatbot 的智慧領養顧問，結合向量空間演算法與 ChromaDB 向量數據庫，透過「6 維適性媒合推薦模型」，為飼主精準推薦最適合的寵物，旨在降低領養後的退養率。

---

## 核心特色

| 特色 | 說明 |
|------|------|
| **推薦引擎** | 向量空間模型 (VSM) + ChromaDB 向量相似度計算，精準媒合飼主與寵物 |
| **LINE 即時互動** | 無需下載 App，透過 LINE 聊天直接進行適性評估 |
| **6 維特徵分析** | 活動力、親人程度、獨立性、空間需求、掉毛程度、吵鬧程度 |
| **多輪對話流程** | 6 道情境化問題，漸進式建構用戶偏好向量 |

---

## 6 維特徵空間設計

RIMBERIO 將「飼主-寵物 適配度」定義為 6 維向量空間，每個維度的取值範圍為 **[0.0 ~ 1.0]**：

| 維度 ID | 特徵名稱 | 描述 | 低值 (0.0) | 高值 (1.0) |
|--------|---------|------|-----------|-----------|
| **0** | Activity | 活動力 | 宅男宅女 | 運動狂人 |
| **1** | Affection | 親人程度 | 獨行俠 | 黏人精 |
| **2** | Independence | 獨立性 | 時間充裕 | 時常外出 |
| **3** | Space | 空間需求 | 小套房 | 大庭院 |
| **4** | Grooming | 掉毛程度 | 幾乎不掉毛 | 掉毛狂魔 |
| **5** | Noise | 吵鬧程度 | 安靜如鼠 | 聲震天下 |

### 寵物特性向量示例

| 寵物名稱 | Activity | Affection | Independence | Space | Grooming | Noise | 適合飼主 |
|---------|----------|-----------|---------------|-------|----------|-------|---------|
| 邊境牧羊犬 | 1.0 | 0.6 | 0.3 | 0.9 | 0.8 | 0.7 | 活潑愛運動的戶外派 |
| 英國短毛貓 | 0.2 | 0.3 | 0.9 | 0.2 | 0.5 | 0.1 | 忙碌上班族 |
| 米格魯 | 0.9 | 0.9 | 0.3 | 0.6 | 0.4 | 1.0 | 親人愛玩的年輕人 |
| 暹羅貓 | 0.6 | 1.0 | 0.1 | 0.2 | 0.3 | 0.9 | 居家陪伴的伴侶獵人 |
| 柴犬 | 0.7 | 0.4 | 0.9 | 0.5 | 1.0 | 0.6 | 獨立、有耐心的飼主 |

---

## 問卷與計分機制

### 30 道題目結構

- **總計 30 道題目**，分為 6 個維度
- **每個維度 5 道題目**，每題占 20% 的權重
- 所有答案進行 **加權平均** 計算，而非簡單覆蓋

### 計分公式

$$\text{維度分數} = \frac{\sum (答案值 \times 0.2)}{1. 0} = \frac{\sum 答案值}{5}$$

### 計分示例

假設用戶在「活動力」維度的回答：
- Q1: 0.9 (weight:  0.2) → 貢獻 0.18
- Q2: 0.5 (weight: 0.2) → 貢獻 0.10
- Q3: 0.9 (weight: 0.2) → 貢獻 0.18
- Q4: 0.7 (weight: 0.2) → 貢獻 0.14
- Q5: 0.3 (weight: 0.2) → 貢獻 0.06

**最終活動力分數 = (0.18 + 0.10 + 0.18 + 0.14 + 0.06) = 0.66**

### 優勢

- 綜合考慮多個角度
- 防止單個極端答案主導結果
- 推薦結果更精準
- 用戶向量更真實

---

## 快速開始

### 1️⃣ 前置環境要求

```bash
# 檢查 Python 版本 (需 3.8 以上，建議 3.10+)
python --version
```

### 2️⃣ 建立虛擬環境與安裝套件

```bash
# 複製本專案到本機
git clone https://github.com/mato1321/rimberio.git
cd rimberio

# 建立虛擬環境
python -m venv venv

# 啟動虛擬環境
# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate

# 安裝所有依賴
pip install -r requirements.txt
```

### 3️⃣ 設定 LINE 官方帳號 (Messaging API)

#### A.建立 LINE Developers 帳號

1.前往 [LINE Developers Console](https://developers.line.biz/zh-hant/)
2.用 LINE 帳號登入 (沒有帳號請先申請)
3.點擊「Create」建立新的 Provider (如:  Rimberio)

#### B.建立 Messaging API Channel

1.在剛建立的 Provider 下，點擊「Create a new channel」
2.選擇 **Messaging API**
3.填寫以下資訊：
   - **Channel name**:  RIMBERIO Bot
   - **Channel description**: 寵物適性媒合系統
   - **Category**: 個人使用 (Personal Use)
   - **Subcategory**: 其他
4.同意服務條款，完成建立

#### C.取得金鑰並關閉自動回覆

進入建立好的 Channel，分別前往：

**1.Basic Settings 頁面**
   - 找到「Channel Secret」
   - 點擊「Copy」複製

**2.Messaging API 頁面**
   - 找到「Channel access token」
   - 點擊「Generate」或「Regenerate」
   - 點擊「Copy」複製

**3.關閉自動回覆**
   - 在 Messaging API 頁面找到 Auto-reply Messages 區塊
   - 點擊「Edit」
   - 將「Auto-response」設為 **Disabled** (停用)
   - 將「Greeting message」也設為 **Disabled** (停用)
   - 點擊「Save」

### 4️⃣ 設定環境變數 (.env.example)

把 `.env.example` 檔名，改成`.env`並且貼入剛才複製的 Token 與 Secret：

```bash
# .env
LINE_CHANNEL_ACCESS_TOKEN=你複製的_Channel_Access_Token_長字串
LINE_CHANNEL_SECRET=你複製的_Channel_Secret_亂碼
```

### 5️⃣ 啟動本機開發伺服器

```bash
# 確保虛擬環境已啟動
python -m uvicorn main:app --reload
```

輸出應如下：
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete
```

### 6️⃣ 建立公網通道 (Ngrok)

為了讓 LINE 伺服器能夠連到你的本機電腦，需要用 Ngrok 建立安全隧道。

#### A.下載並安裝 Ngrok

1.前往 [Ngrok 官網](https://ngrok.com/download)
2.下載對應你作業系統的版本
3.解壓縮到方便的位置 (如: C:\Tools\ngrok)

#### B.啟動 Ngrok

**在新的終端機視窗中執行**：

```bash
# Windows (假設 ngrok 在 C:\Tools\ngrok)
C:\Tools\ngrok\ngrok.exe http 8000

# macOS / Linux
./ngrok http 8000
```

你會看到類似的輸出：
```
ngrok                                                             (Ctrl-C to quit)

Session Status                online
Session Expires               1 hour, 59 minutes
Version                       3.0.0
Region                        Tokyo (jp)
Forwarding                    https://xxxx-xxxx.ngrok-free.app -> http://localhost:8000
Forwarding                    http://xxxx-xxxx.ngrok-free.app -> http://localhost:8000
```

**複製 Forwarding 欄位中的 HTTPS 網址** (必須是 https 開頭)，例如：
```
https://1a2b-3c4d-5e6f.ngrok-free.app
```

### 7️⃣ 設定 LINE Webhook URL

回到 [LINE Developers Console](https://developers.line.biz/zh-hant/)，在你的 Channel 的 **Messaging API** 頁面：

1.找到「Webhook URL」欄位
2.點擊「Edit」
3.貼上 Ngrok 網址 + `/callback`，例如：
   ```
   https://1a2b-3c4d-5e6f.ngrok-free.app/callback
   ```
4.點擊「Update」
5.在下方的「Use webhook」開關，確保已**開啟**
6.找到「Verify」按鈕，點擊驗證

如果顯示 **"Success"**，代表機器人已成功連線！

---

## 使用教學

### 第一步：加入機器人好友

1.在 LINE Developers Console 的 Channel 頁面，找到 **QR Code**
2.用 LINE App 掃描 QR Code
3.點擊「加入」將機器人加為好友

### 第二步：開始測驗

在聊天視窗中輸入以下任一關鍵字：
- `開始`
- `測驗`
- `開始測驗`

機器人會回覆：
```
歡迎來到 RIMBERIO！
我們將透過 30 個問題，幫你找到適合的寵物。

準備好了嗎？讓我們開始吧！
```

### 第三步：回答問題

機器人會逐一提問，每題提供 3 個選項，點擊按鈕選擇：

```
問題 1

【Q1/30 活動力】 你每天能陪狗進行戶外活動多久？

[30分鐘以內] [30-90分鐘] [90分鐘以上]
```

### 第四步：接收推薦結果

完成 6 道題目後，機器人會立即分析並回覆：

```
RIMBERIO 推薦結果出爐！
根據你的生活型態，最適合你的夥伴是：

第 1 名：英國短毛貓
速配指數：85%
安靜沈穩的紳士，適合忙碌且住在小公寓的上班族。
--------------------

第 2 名：暹羅貓
速配指數：72%
貓界像皮糖，非常愛講話，需要你隨時的陪伴。
--------------------

第 3 名：邊境牧羊犬
速配指數：45%
智商天花板，但需要大量運動與空間，適合戶外派的老手。
--------------------

想要重新測驗嗎？請輸入「開始」。
```

---

## 技術深度解析

### 核心演算法：向量空間模型 (Vector Space Model, VSM)

RIMBERIO 的推薦引擎核心是**歐幾里得距離** (Euclidean Distance)：

$$d = \sqrt{\sum_{i=0}^{5} (user_i - pet_i)^2}$$

其中：
- `user_i` = 使用者在第 i 維的偏好值
- `pet_i` = 寵物在第 i 維的特性值
- `d` = 歐幾里得距離 (越小越相似)

**速配指數計算**：
```
match_score = max(0, (1 - distance) × 100%)
```

### ChromaDB 的優勢

相比直接計算所有距離，使用 ChromaDB 向量數據庫具有：

| 優勢 | 說明 |
|------|------|
| **高效查詢** | 利用 HNSW 索引快速定位近鄰寵物 |
| **可擴展性** | 寵物數量增加時，查詢時間仍維持對數級別 |
| **持久化存儲** | 寵物資料可持久化，重啟伺服器無需重新初始化 |
| **靈活元數據** | 支援寵物名稱、描述等文本元數據 |

### FastAPI 非同步流程

```python
# 事件驅動流程
1.LINE 使用者傳送訊息
   └─> 2.  Ngrok 轉發到 /callback 端點
       └─> 3.handler.handle() 解析簽名與事件
           └─> 4.@handler.add() 路由分發
               ├─> MessageEvent (啟動測驗)
               │   └─> send_question() 發送第一題
               └─> PostbackEvent (回答題目)
                   └─> 更新 user_sessions[user_id]['vector']
                   └─> 判斷是否還有題目
                       ├─> YES: send_question() 發送下一題
                       └─> NO:  show_recommendation() 推薦寵物
```

---

## 依賴套件簡介

```txt
核心框架層
├── fastapi==0.124.2          (Web 框架)
├── uvicorn==0.38.0           (ASGI 伺服器)
├── starlette==0.50.0         (FastAPI 基礎層)
└── httptools==0.7.1          (HTTP 解析加速)

LINE 整合層
├── line-bot-sdk==3.21.0      (LINE 官方 SDK)
├── aiohttp==3.13.2           (非同步 HTTP)
└── websockets==15.0.1        (WebSocket 支援)

向量 DB 層
├── chromadb==1.3.6           (向量資料庫)
├── onnxruntime==1.23.2       (模型推理加速)
├── numpy==2.3.5              (數值計算)
└── pandas==2.3.3             (資料處理)

環境與工具
├── python-dotenv==1.2.1      (環境變數管理)
├── pydantic==2.12.5          (資料驗證)
└── requests==2.32.5          (HTTP 客戶端)
```

**完整套件清單**：見 `requirements.txt` (共 104 個依賴)

---

## 系統架構

```
┌─────────────────────────────────────────────────────┐
│                  LINE 用戶                          │
│            (掃描 QR Code 加入機器人)                 │
└────────────────────┬────────────────────────────────┘
                     │ LINE Messaging API
                     ▼
┌─────────────────────────────────────────────────────┐
│  Ngrok (Public HTTPS Tunnel - https://xxxx.app)    │
│            (本機開發環境→公網橋梁)                   │
└────────────────────┬────────────────────────────────┘
                     │ POST /callback
                     ▼
┌─────────────────────────────────────────────────────┐
│          FastAPI Web Server (Port 8000)             │
│                  (main.py)                          │
│  ┌──────────────────────────────────────────────┐  │
│  │  • WebhookHandler 事件路由                    │  │
│  │  • MessageEvent 處理 (啟動測驗)               │  │
│  │  • PostbackEvent 處理 (回答問題)              │  │
│  │  • user_sessions 記憶體管理                  │  │
│  └──────────────────────────────────────────────┘  │
└────────────────────┬────────────────────────────────┘
                     │ 向量化查詢
                     ▼
┌─────────────────────────────────────────────────────┐
│     Data Model Layer (data_model.py)                │
│  ┌──────────────────────────────────────────────┐  │
│  │  DIMENSIONS:  [Activity, Affection, ...]      │  │
│  │  QUESTIONS:  6 道適性評估題                    │  │
│  │  PET_DB: 5 隻寵物 (向量表示)                  │  │
│  │  ChromaDB: 向量數據庫 (Euclidean Distance) │  │
│  └──────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────┘
                     │ 推薦結果
                     ▼
┌─────────────────────────────────────────────────────┐
│  推薦回覆 (Flex Message / Text Message)             │
│  • 排序前 3 名寵物候選                              │
│  • 速配指數 (0-100%)                               │
│  • 寵物特性說明                                     │
└─────────────────────────────────────────────────────┘
```

---

## 專案目錄結構

```
rimberio/
├── .env.example                  # 環境變數，需要改檔名 (LINE Token & Secret)
├── .gitignore                    # Git 忽略設定
├── main.py                       # FastAPI 主程式
│   ├── FastAPI 應用初始化
│   ├── LINE WebhookHandler 路由
│   ├── 文字訊息事件處理 (啟動測驗邏輯)
│   ├── Postback 事件處理 (問卷回答邏輯)
│   ├── send_question() - 發送題目函式
│   └── show_recommendation() - 顯示推薦結果函式
│
├── data_model.py                 # 數據模型 & 向量DB 
│   ├── DIMENSIONS[] - 6 維特徵定義
│   ├── PET_DB[] - 80+ 隻寵物資料 (帶向量表示)
│   ├── QUESTIONS[] - 30 道問卷題目 (6 維，每維 5 題)
│   ├── validate_questions_weights() - 權重驗證
│   └── ChromaDB 初始化 & get_recommendations()
│
├── requirements.txt             # 依賴套件清單 
```

---

## 聯絡方式

- **Email**: charleskao811@gmail.com
- **GitHub**: [@mato1321](https://github.com/mato1321)
- **Issues**: 如有任何問題，歡迎在 [GitHub Issues](https://github.com/mato1321/rimberio/issues) 中提出

---

## 開源授權

本專案採用 **MIT License**，你可以自由地使用、複製、修改本專案。

---

**歡迎使用 RIMBERIO，為毛孩找到最適合的家！** 

```
      ᙏ̥ (๑•́  ω •̀๑)  
     ∧_∧
    ( ´・ω・)  
   /   ⊃⊂  \
  (´・ω・`)   
```