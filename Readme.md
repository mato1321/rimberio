# 🐾 RIMBERIO - 寵物媒合推薦系統

![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=flat-square&logo=python&logoColor=ffffff)
![FastAPI](https://img.shields.io/badge/FastAPI-0.124.2-009485?style=flat-square&logo=fastapi)
![LINE Bot](https://img.shields.io/badge/LINE-Bot%20SDK-00B900?style=flat-square&logo=line)
![ChromaDB](https://img.shields.io/badge/ChromaDB-Vector%20DB-green?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)

**RIMBERIO** 是一個基於 LINE Chatbot 的智慧領養顧問，結合向量空間演算法與 ChromaDB 向量數據庫，透過「6 維適性媒合推薦模型」，為飼主精準推薦最適合的寵物，旨在降低領養後的退養率。

---
[YouTube Video](https://youtube.com/shorts/PiXQjn4DSv8?feature=share)

## 核心特色

| 特色 | 說明 |
|------|------|
| **推薦引擎** | 向量空間模型 (VSM) + ChromaDB 向量相似度計算，精準媒合飼主與寵物 |
| **LINE 即時互動** | 無需下載 App，透過 LINE 聊天直接進行適性評估 |
| **6 維特徵分析** | 活動力、親人程度、獨立性、空間需求、掉毛程度、吵鬧程度 |
| **快速評估流程** | 12 道精心設計的情境化問題，2-3 分鐘快速了解適配度 |

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

### 計分公式

$$\text{維度分數} = \frac{\sum (答案值 \times 0.5)}{1.0} = \frac{\text{答案 1} + \text{答案 2}}{2}$$

### 計分示例

假設用戶在「活動力」維度的回答：
- Q1: 0.9 (weight: 0.5) → 貢獻 0.45
- Q2: 0.5 (weight: 0.5) → 貢獻 0.25

**最終活動力分數 = (0.45 + 0.25) = 0.70**

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

把 `.env.example` 檔名，改成 `.env` 並且貼入剛才複製的 Token 與 Secret：

```bash
# .env
LINE_CHANNEL_ACCESS_TOKEN=你複製的_Channel_Access_Token_長字串
LINE_CHANNEL_SECRET=你複製的_Channel_Secret_亂碼
CLOUDINARY_CLOUD_NAME=你的_Cloudinary_帳號
CLOUDINARY_API_KEY=你的_API_Key
CLOUDINARY_API_SECRET=你的_API_Secret
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
歡迎來到 RIMBERIO！🐾
請選擇你想要的寵物類型：

[我想要狗狗] [我想要貓咪] [都可以]
```

### 第三步：選擇寵物類型

點擊按鈕選擇你偏好的寵物類型，機器人會顯示：

```
你選擇了狗狗！

我們將透過 12 個問題，幫你找到最適合的狗狗夥伴。
準備好了嗎？
```

### 第四步：回答問題

機器人會逐一提問，每題提供 3 個選項，點擊按鈕選擇：

```
問題 1/12

你每天能陪寵物進行活動多久？

[30分鐘以內] [30-90分鐘] [超過90分鐘]
```

### 第五步：接收推薦結果

完成 12 道題目後，機器人會立即分析並回覆：

```
推薦結果出爐
根據你的生活型態，最適合你的犬種是：

第 1 名：比熊犬
速配指數：92%
白色蓬鬆毛髮，性格開朗親人，需要定期修剪。

第 2 名：貴賓犬
速配指數：88%
聰慧易訓練，掉毛少，是台灣最受歡迎的犬種之一。

第 3 名：西施犬
速配指數：85%
長毛古老犬種，溫順親人，需要細心打理毛髮。

━━━━━━━━━━━━━━━━━
分類推薦

最佳犬種：比熊犬
速配指數：92%
白色蓬鬆毛髮，性格開朗親人，需要定期修剪。

想要重新測驗請輸入「開始」。
```

**同時會收到一張雷達圖表**，視覺化顯示你的偏好與推薦寵物的匹配度。

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

### FastAPI 非同步流程

```python
# 事件驅動流程
1.LINE 使用者傳送訊息
   └─> 2.Ngrok 轉發到 /callback 端點
       └─> 3.handler.handle() 解析簽名與事件
           └─> 4.@handler.add() 路由分發
               ├─> MessageEvent (啟動測驗)
               │   └─> 詢問寵物類型選擇
               │       └─> send_question() 發送第一題
               └─> PostbackEvent (回答題目 / 選擇類型)
                   ├─> 更新 user_sessions[user_id]
                   ├─> 判斷是否還有題目
                   │   ├─> YES: send_question() 發送下一題
                   │   └─> NO: 計算最終向量
                   │       └─> show_recommendation() 推薦寵物
```
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
│  │  • PostbackEvent 處理 (回答問題、選擇寵物)    │  │
│  │  • user_sessions 記憶體管理                  │  │
│  │  • calculate_weighted_average() 計分計算     │  │
│  └──────────────────────────────────────────────┘  │
└────────────────────┬────────────────────────────────┘
                     │ 向量化查詢
                     ▼
┌─────────────────────────────────────────────────────┐
│     Data Model Layer (data_model.py)                │
│  ┌──────────────────────────────────────────────┐  │
│  │  DIMENSIONS:  [Activity, Affection, ...]      │  │
│  │  QUESTIONS:  12 道精心設計的適性評估題        │  │
│  │  PET_DB:  40 隻寵物 (20 狗+20 貓, 向量表示)   │  │
│  │  ChromaDB: 向量數據庫 (Euclidean Distance) │  │
│  └──────────────────────────────────────────────┘  │
└────────────────────┬────────────────────────────────┘
                     │ 推薦結果
                     ▼
┌─────────────────────────────────────────────────────┐
│  推薦回覆 + 視覺化雷達圖表 (Cloudinary)              │
│  • 排序前 3 名寵物候選                              │
│  • 速配指數 (0-100%)                               │
│  • 寵物特性說明                                     │
│  • 六維偏好指數雷達圖                               │
└─────────────────────────────────────────────────────┘
```

---

## 專案目錄結構

```
rimberio/
├── .env.example                  # 環境變數模板 (需改檔名為 .env)
├── .gitignore                    # Git 忽略設定
├── main.py                       # FastAPI 主程式
│   ├── FastAPI 應用初始化
│   ├── LINE WebhookHandler 路由
│   ├── 文字訊息事件處理 (啟動測驗邏輯)
│   ├── Postback 事件處理 (選擇寵物類型 & 回答題目邏輯)
│   ├── calculate_weighted_average() - 計分計算
│   ├── send_question() - 發送題目函式
│   └── show_recommendation() - 顯示推薦結果函式
│
├── data_model.py                 # 數據模型 & 向量 DB
│   ├── DIMENSIONS[] - 6 維特徵定義
│   ├── PET_DB[] - 40 隻寵物資料 (帶向量表示、型態分類)
│   ├── QUESTIONS[] - 12 道問卷題目 (6 維，每維 2 題，權重各 0.5)
│   ├── validate_questions_weights() - 權重驗證
│   ├── validate_pet_types() - 寵物類型驗證
│   ├── get_recommendations() - 通用推薦函式
│   ├── get_recommendations_with_type() - 按類型推薦
│   └── ChromaDB 初始化
│
├── generate_radar_chart.py       # 雷達圖表生成與上傳
│   ├── generate_radar_chart() - 生成推薦對比圖
│   ├── generate_user_only_radar() - 單人偏好圖
│   ├── upload_to_cloudinary() - 上傳到 Cloudinary
│   └── set_cloudinary_credentials() - Cloudinary 設定
│
├── requirements.txt              # 依賴套件清單 (104 個)
├── Readme.md                     # 本檔案 (專案說明文檔)
└── .gitignore                    # Git 配置
```

---

## 數據統計

### 寵物資料庫規模

```
狗狗品種：20 隻
   - 小型犬：吉娃娃、博美、馬爾濟斯、約克夏等
   - 中型犬：柯基、比熊、貴賓、西施等
   - 大型犬：柴犬、黃金獵犬、拉布拉多、德國牧羊犬等

貓咪品種：20 隻
   - 短毛貓：英國短毛、美國短毛、虎斑、暹羅、緬甸等
   - 長毛貓：波斯、布偶、挪威森林、西伯利亞等
   - 特殊貓：蘇格蘭折耳、孟加拉、曼赤肯、斯芬克斯等

 總計：40 隻寵物
```
---

## 聯絡方式

- **Email**:  charleskao811@gmail.com
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