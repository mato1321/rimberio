# data_model.py
import chromadb

# --- 1. 核心維度定義 ---
# 這些是我們定案的 6 個特徵，順序必須固定
DIMENSIONS = [
    "Activity",      # 0: 活動力 (時間/體力)
    "Affection",     # 1: 親人程度 (情感需求)
    "Independence",  # 2: 獨立性 (工作時長)
    "Space",         # 3: 空間需求 (居住環境)
    "Grooming",      # 4: 掉毛程度 (清潔/過敏)
    "Noise"          # 5: 吵鬧程度 (居住隔音)
]

# --- 2. 寵物模擬資料庫 (知識庫) ---
# 向量順序對應上面的 DIMENSIONS
# 數值：0.0 (低/無) ~ 1.0 (高/強)
PET_DB = [
    {
        "id": "dog_border_collie",
        "name": "邊境牧羊犬",
        # 高活動, 普通親人, 低獨立, 高空間, 高掉毛, 愛叫
        "vector": [1.0, 0.6, 0.3, 0.9, 0.8, 0.7],
        "desc": "智商天花板，但需要大量運動與空間，適合戶外派的老手。"
    },
    {
        "id": "cat_british_shorthair",
        "name": "英國短毛貓",
        # 低活動, 低親人, 高獨立, 低空間, 中掉毛, 安靜
        "vector": [0.2, 0.3, 0.9, 0.2, 0.5, 0.1],
        "desc": "安靜沈穩的紳士，適合忙碌且住在小公寓的上班族。"
    },
    {
        "id": "dog_beagle",
        "name": "米格魯",
        # 高活動,以此類推...
        "vector": [0.9, 0.9, 0.3, 0.6, 0.4, 1.0],
        "desc": "非常親人活潑，但嗅覺敏銳且嗓門很大，需要包容力。"
    },
    {
        "id": "cat_siamese",
        "name": "暹羅貓",
        # 中活動, 極親人, 低獨立, 低空間, 低掉毛, 愛叫
        "vector": [0.6, 1.0, 0.1, 0.2, 0.3, 0.9],
        "desc": "貓界像皮糖，非常愛講話，需要你隨時的陪伴。"
    },
    {
        "id": "dog_shiba",
        "name": "柴犬",
        # 中高活動, 低親人, 高獨立, 中空間, 極高掉毛, 警戒叫
        "vector": [0.7, 0.4, 0.9, 0.5, 1.0, 0.6],
        "desc": "個性獨立像貓的狗，很有主見，換毛季需要勤梳毛。"
    }
]

# --- 3. 問卷題目設計 ---
# 每一題對應一個維度 (dimension_index)
QUESTIONS = [
    {
        "id": "q1",
        "text": "【Q1/6 活動力】\n週末到了，你理想的行程是？",
        "dimension_index": 0, # 對應 Activity
        "options": [
            {"label": "登山/跑步/探險", "value": 0.9, "text": "我喜歡戶外運動"},
            {"label": "公園散步/逛街", "value": 0.5, "text": "輕鬆散步就好"},
            {"label": "在家追劇/睡覺", "value": 0.1, "text": "我想在家休息"}
        ]
    },
    {
        "id": "q2",
        "text": "【Q2/6 親人程度】\n當你在家放鬆時，你希望寵物？",
        "dimension_index": 1, # 對應 Affection
        "options": [
            {"label": "黏在身上/討摸", "value": 0.9, "text": "要超級黏人"},
            {"label": "待同房偶爾互動", "value": 0.5, "text": "偶爾互動就好"},
            {"label": "各做各的/不打擾", "value": 0.2, "text": "保持距離美感"}
        ]
    },
    {
        "id": "q3",
        "text": "【Q3/6 獨立性】\n你平日外出工作的時間平均多久？",
        "dimension_index": 2, # 對應 Independence
        "options": [
            {"label": "超過 10 小時", "value": 0.9, "text": "我很忙碌"},
            {"label": "約 8 小時", "value": 0.5, "text": "朝九晚五"},
            {"label": "在家工作/時間多", "value": 0.1, "text": "時間很自由"}
        ]
    },
    {
        "id": "q4",
        "text": "【Q4/6 空間需求】\n你目前的居住環境大致是？",
        "dimension_index": 3, # 對應 Space
        "options": [
            {"label": "透天/有大庭院", "value": 0.9, "text": "空間很大"},
            {"label": "一般公寓(3房)", "value": 0.5, "text": "一般家庭式"},
            {"label": "小套房/雅房", "value": 0.1, "text": "都會小空間"}
        ]
    },
    {
        "id": "q5",
        "text": "【Q5/6 掉毛接受度】\n對於家裡出現寵物毛髮？",
        "dimension_index": 4, # 對應 Grooming
        "options": [
            {"label": "完全不行/過敏", "value": 0.1, "text": "我會過敏"},
            {"label": "勤勞打掃就好", "value": 0.5, "text": "可以接受一點"},
            {"label": "毛是家飾一部分", "value": 0.9, "text": "完全沒差"}
        ]
    },
    {
        "id": "q6",
        "text": "【Q6/6 吵鬧程度】\n關於寵物的叫聲，你的狀況是？",
        "dimension_index": 5, # 對應 Noise
        "options": [
            {"label": "隔音差/怕吵", "value": 0.1, "text": "必須安靜"},
            {"label": "住宅區/偶爾叫", "value": 0.5, "text": "普通住宅區"},
            {"label": "住鄉下/獨棟", "value": 0.9, "text": "叫聲沒關係"}
        ]
    }
]

# --- 4. ChromaDB 初始化與查詢功能 ---

# 初始化 ChromaDB Client (使用全域變數以避免重複讀取)
client = chromadb.Client()
collection_name = "rimberio_pets_v1"

# 嘗試取得 collection，如果不存在就建立並寫入資料
try:
    # 檢查是否已存在 (簡單透過 get 測試)
    collection = client.get_collection(collection_name)
except:
    # 不存在則建立
    collection = client.create_collection(collection_name)
    # 寫入預設資料
    ids = [p['id'] for p in PET_DB]
    embeddings = [p['vector'] for p in PET_DB]
    metadatas = [{"name": p['name'], "desc": p['description']} for p in PET_DB]
    
    collection.add(ids=ids, embeddings=embeddings, metadatas=metadatas)
    print("✅ ChromaDB 資料庫初始化完成，資料已寫入。")

def get_recommendations(user_vector, n_results=3):
    """
    輸入使用者的 6 維向量，回傳最推薦的寵物列表
    """
    results = collection.query(
        query_embeddings=[user_vector],
        n_results=n_results
    )
    
    # 整理回傳格式
    recommendations = []
    for i in range(len(results['ids'][0])):
        recommendations.append({
            "name": results['metadatas'][0][i]['name'],
            "desc": results['metadatas'][0][i]['desc'],
            "score": results['distances'][0][i] # 距離越小越好
        })
    return recommendations