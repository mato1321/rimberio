import chromadb
DIMENSIONS = [
    "Activity",      # 0: 活動力
    "Affection",     # 1: 親人程度
    "Independence",  # 2: 獨立性
    "Space",         # 3: 空間需求
    "Grooming",      # 4: 掉毛程度
    "Noise"          # 5: 吵鬧程度
]

PET_DB = [
    # 狗狗品種
    {
        "id": "1",
        "name": "柴犬",
        "type": "dog",
        "vector": [0.5, 0.6, 0.4, 0.5, 0.4, 0.5],
        "desc": "日本國寶犬，性格獨立有主見，適合有耐心的飼主。"
    },
    {
        "id": "2",
        "name": "黃金獵犬",
        "type": "dog",
        "vector": [0.6, 0.7, 0.5, 0.6, 0.5, 0.6],
        "desc": "溫順友善，是家庭首選，很受台灣家庭歡迎。"
    },
    {
        "id": "3",
        "name": "拉布拉多",
        "type": "dog",
        "vector": [0.7, 0.8, 0.6, 0.7, 0.6, 0.7],
        "desc": "親人活潑，需要充足運動，適合愛運動的家庭。"
    },
    {
        "id": "4",
        "name": "法國鬥牛犬",
        "type": "dog",
        "vector": [0.5, 0.7, 0.5, 0.5, 0.5, 0.6],
        "desc": "體型小，適合公寓，是都市上班族的熱門選擇。"
    },
    {
        "id":  "5",
        "name":  "吉娃娃",
        "type": "dog",
        "vector": [0.3, 0.7, 0.6, 0.2, 0.4, 0.4],
        "desc": "世界最小犬種，親人黏人，適合想要伴侶犬的人。"
    },
    {
        "id":  "6",
        "name":  "博美犬",
        "type": "dog",
        "vector": [0.4, 0.8, 0.5, 0.3, 0.5, 0.5],
        "desc":  "毛茸茸可愛，性格活潑，需要定期美容。"
    },
    {
        "id": "7",
        "name": "馬爾濟斯",
        "type": "dog",
        "vector": [0.3, 0.7, 0.5, 0.2, 0.6, 0.3],
        "desc": "長毛優雅，親人溫柔，適合台灣濕熱氣候。"
    },
    {
        "id": "8",
        "name": "約克夏",
        "type": "dog",
        "vector": [0.3, 0.7, 0.5, 0.3, 0.5, 0.4],
        "desc": "小型長毛犬，活潑聰慧，是台灣常見的寵物犬。"
    },
    {
        "id": "9",
        "name": "柯基犬",
        "type": "dog",
        "vector": [0.6, 0.7, 0.4, 0.5, 0.4, 0.5],
        "desc": "短腿長身，聰慧友善，台灣飼養率高。"
    },
    {
        "id": "10",
        "name": "比熊犬",
        "type": "dog",
        "vector": [0.4, 0.8, 0.5, 0.4, 0.6, 0.6],
        "desc": "白色蓬鬆毛髮，性格開朗親人，需要定期修剪。"
    },
    {
        "id": "11",
        "name": "貴賓犬",
        "type": "dog",
        "vector": [0.4, 0.6, 0.5, 0.4, 0.3, 0.4],
        "desc": "聰慧易訓練，掉毛少，是台灣最受歡迎的犬種之一。"
    },
    {
        "id": "12",
        "name": "西施犬",
        "type": "dog",
        "vector": [0.3, 0.6, 0.4, 0.4, 0.5, 0.4],
        "desc": "長毛古老犬種，溫順親人，需要細心打理毛髮。"
    },
    {
        "id": "13",
        "name": "米克斯",
        "type": "dog",
        "vector": [0.5, 0.7, 0.6, 0.5, 0.4, 0.5],
        "desc": "混種犬，性格多樣，適應力強，值得領養。"
    },
    {
        "id": "14",
        "name": "德國牧羊犬",
        "type": "dog",
        "vector": [0.6, 0.7, 0.4, 0.6, 0.5, 0.6],
        "desc": "聰慧忠誠，需要充足空間和運動，適合經驗豐富的飼主。"
    },
    {
        "id": "15",
        "name": "英國鬥牛犬",
        "type": "dog",
        "vector": [0.4, 0.6, 0.5, 0.5, 0.4, 0.5],
        "desc": "外表威武但溫和，怕熱，台灣養護需注意空調。"
    },
    {
        "id": "16",
        "name": "喜樂蒂牧羊犬",
        "type": "dog",
        "vector": [0.5, 0.7, 0.4, 0.5, 0.5, 0.5],
        "desc": "活潑聰慧，容易訓練，是家庭犬的好選擇。"
    },
    {
        "id":  "17",
        "name":  "可卡犬",
        "type": "dog",
        "vector": [0.5, 0.8, 0.5, 0.5, 0.6, 0.6],
        "desc": "溫順友善，需要運動和愛心，是親人伴侶犬。"
    },
    {
        "id": "18",
        "name": "巴哥犬",
        "type": "dog",
        "vector": [0.3, 0.7, 0.4, 0.4, 0.3, 0.4],
        "desc": "皺紋可愛的小型犬，懶散溫和，適合台灣家庭。"
    },
    {
        "id": "19",
        "name": "臘腸犬",
        "type":  "dog",
        "vector":  [0.4, 0.6, 0.4, 0.3, 0.3, 0.4],
        "desc": "長身短腿，親人活潑，需要注意脊椎健康。"
    },
    {
        "id": "20",
        "name": "邊境牧羊犬",
        "type": "dog",
        "vector": [0.8, 0.5, 0.3, 0.7, 0.3, 0.4],
        "desc": "最聰慧的犬種，需要大量運動和心理刺激，適合有時間的飼主。"
    },
    # 貓咪品種
    {
        "id": "21",
        "name": "英國短毛貓",
        "type": "cat",
        "vector": [0.2, 0.3, 0.9, 0.2, 0.5, 0.1],
        "desc": "安靜穩重，獨立自主，適合忙碌的上班族，是台灣最受歡迎的貓。"
    },
    {
        "id": "22",
        "name": "美國短毛貓",
        "type": "cat",
        "vector": [0.4, 0.4, 0.8, 0.3, 0.4, 0.2],
        "desc": "活潑好奇，適應力強，容易照顧，台灣很多家庭飼養。"
    },
    {
        "id": "23",
        "name": "虎斑貓",
        "type": "cat",
        "vector": [0.3, 0.5, 0.7, 0.3, 0.5, 0.2],
        "desc": "紋路漂亮，性格溫和，是台灣領養最多的貓咪。"
    },
    {
        "id": "24",
        "name": "波斯貓",
        "type": "cat",
        "vector": [0.1, 0.8, 0.5, 0.3, 0.8, 0.1],
        "desc": "長毛優雅，需要細心打理毛髮，性格溫順親人。"
    },
    {
        "id": "25",
        "name": "暹羅貓",
        "type": "cat",
        "vector": [0.6, 0.9, 0.3, 0.4, 0.3, 0.6],
        "desc": "聰慧愛叫，極度黏人，喜歡和主人互動和玩耍。"
    },
    {
        "id": "26",
        "name": "緬甸貓",
        "type": "cat",
        "vector": [0.5, 0.9, 0.2, 0.4, 0.2, 0.5],
        "desc": "性格開朗親人，喜歡陪伴主人，感情豐富。"
    },
    {
        "id":  "27",
        "name":  "蘇格蘭折耳貓",
        "type": "cat",
        "vector": [0.2, 0.8, 0.7, 0.3, 0.6, 0.2],
        "desc": "折耳可愛，溫順親人，但需要注意健康問題。"
    },
    {
        "id": "28",
        "name": "布偶貓",
        "type": "cat",
        "vector": [0.3, 0.9, 0.6, 0.4, 0.4, 0.3],
        "desc": "溫柔乖巧，容易被抱起，親人黏人，是家庭貓的首選。"
    },
    {
        "id": "29",
        "name": "俄羅斯藍貓",
        "type":  "cat",
        "vector":  [0.3, 0.5, 0.8, 0.3, 0.2, 0.2],
        "desc": "性格內向但親人，安靜優雅，適合安靜家庭。"
    },
    {
        "id": "30",
        "name": "孟加拉貓",
        "type": "cat",
        "vector": [0.7, 0.6, 0.5, 0.5, 0.3, 0.4],
        "desc":  "豹紋漂亮，活潑好動，需要充足互動和玩耍。"
    },
    {
        "id": "31",
        "name": "曼赤肯貓",
        "type": "cat",
        "vector": [0.4, 0.7, 0.5, 0.3, 0.4, 0.3],
        "desc": "短腿可愛，性格開朗，是新興的台灣熱門貓種。"
    },
    {
        "id": "32",
        "name": "斯芬克斯無毛貓",
        "type": "cat",
        "vector": [0.5, 0.8, 0.6, 0.4, 0.1, 0.4],
        "desc": "無毛特別，性格親人，需要特殊照顧和保暖。"
    },
    {
        "id": "33",
        "name": "拉珀姆捲毛貓",
        "type": "cat",
        "vector": [0.5, 0.8, 0.4, 0.4, 0.5, 0.3],
        "desc": "捲毛獨特，性格愛玩，需要定期修剪毛髮。"
    },
    {
        "id":  "34",
        "name":  "新加坡貓",
        "type": "cat",
        "vector": [0.3, 0.8, 0.5, 0.2, 0.2, 0.3],
        "desc": "世界最小貓種，性格開朗，需要溫暖環境。"
    },
    {
        "id": "35",
        "name": "埃及貓",
        "type": "cat",
        "vector": [0.8, 0.6, 0.6, 0.5, 0.3, 0.4],
        "desc": "天然斑點，跑得極快，忠誠但對陌生人害羞。"
    },
    {
        "id": "36",
        "name": "日本短尾貓",
        "type": "cat",
        "vector": [0.5, 0.7, 0.5, 0.4, 0.3, 0.4],
        "desc": "短尾招財，性格活潑，適應力強，台灣常見。"
    },
    {
        "id": "37",
        "name": "德文卷毛貓",
        "type": "cat",
        "vector": [0.6, 0.8, 0.4, 0.4, 0.3, 0.4],
        "desc": "捲毛精靈，性格活潑親人，喜歡被抱和陪伴。"
    },
    {
        "id":  "38",
        "name":  "康瓦爾卷毛貓",
        "type": "cat",
        "vector": [0.6, 0.8, 0.4, 0.3, 0.2, 0.4],
        "desc": "超級捲毛，性格友善活潑，需要溫暖環境。"
    },
    {
        "id": "39",
        "name": "挪威森林貓",
        "type": "cat",
        "vector": [0.4, 0.6, 0.6, 0.6, 0.7, 0.3],
        "desc": "大型長毛貓，性格溫和獨立，需要充足空間。"
    },
    {
        "id":  "40",
        "name":  "西伯利亞貓",
        "type": "cat",
        "vector": [0.5, 0.7, 0.4, 0.6, 0.7, 0.4],
        "desc": "大型長毛貓，親人友善，適應台灣氣候。"
    }
]
# 問卷題目設計
QUESTIONS = [
    # ==================== 維度 0:  活動力 ====================
    {
        "id": "q1",
        "dimension_index": 0,
        "weight": 0.5,
        "text": "【Q1/12 活動力】\n你每天能陪寵物進行活動多久？",
        "options": [
            {
                "label": "30分鐘以內",
                "value": 0.1,
                "text": "較低程度"
            },
            {
                "label": "30-90分鐘",
                "value": 0.5,
                "text": "中等程度"
            },
            {
                "label": "超過90分鐘",
                "value": 0.9,
                "text": "較高程度"
            }
        ]
    },
    {
        "id": "q2",
        "dimension_index":  0,
        "weight":  0.5,
        "text": "【Q2/12 活動力】\n若寵物精力過剩需要每天玩耍 30 分鐘，你的意願是？",
        "options": [
            {
                "label":  "太累了",
                "value": 0.1,
                "text":  "意願低"
            },
            {
                "label": "盡力配合",
                "value": 0.5,
                "text": "意願普通"
            },
            {
                "label": "我很樂意",
                "value":  0.9,
                "text": "意願高"
            }
        ]
    },
    # ==================== 維度 1: 親人程度 ====================
    {
        "id": "q3",
        "dimension_index":  1,
        "weight":  0.5,
        "text": "【Q3/12 親人程度】\n你希望寵物多常主動與你互動？",
        "options": [
            {
                "label": "偶爾就好",
                "value": 0.1,
                "text":  "較低程度"
            },
            {
                "label": "每天幾次",
                "value": 0.5,
                "text":  "中等程度"
            },
            {
                "label": "隨時隨地",
                "value":  0.9,
                "text": "較高程度"
            }
        ]
    },
    {
        "id": "q4",
        "dimension_index": 1,
        "weight": 0.5,
        "text": "【Q4/12 親人程度】\n當你在家時，你希望寵物在哪裡？",
        "options":  [
            {
                "label": "在另一個房間",
                "value": 0.1,
                "text": "保持距離"
            },
            {
                "label": "在腳邊陪著",
                "value":  0.5,
                "text": "適度陪伴"
            },
            {
                "label": "要抱抱蹭人",
                "value": 0.9,
                "text":  "緊密接觸"
            }
        ]
    },
    # ==================== 維度 2: 獨立性 ====================
    {
        "id": "q5",
        "dimension_index":  2,
        "weight":  0.5,
        "text": "【Q5/12 獨立性】\n你每週有多少天需要讓寵物獨自在家超過 8 小時？",
        "options": [
            {
                "label": "幾乎沒有",
                "value":  0.1,
                "text": "很少獨處"
            },
            {
                "label": "2-3天",
                "value": 0.5,
                "text":  "偶爾獨處"
            },
            {
                "label": "5天以上",
                "value":  0.9,
                "text": "經常獨處"
            }
        ]
    },
    {
        "id": "q6",
        "dimension_index": 2,
        "weight": 0.5,
        "text": "【Q6/12 獨立性】\n當你出門時，你希望寵物的反應是？",
        "options": [
            {
                "label":  "焦慮不安",
                "value": 0.1,
                "text": "依賴心強"
            },
            {
                "label": "觀察一下就放鬆",
                "value":  0.5,
                "text": "適度獨立"
            },
            {
                "label": "完全不在意",
                "value": 0.9,
                "text": "非常獨立"
            }
        ]
    },
    # ==================== 維度 3: 空間需求 ====================
    {
        "id": "q7",
        "dimension_index": 3,
        "weight": 0.5,
        "text": "【Q7/12 空間需求】\n你的居住空間如何？",
        "options": [
            {
                "label": "空間狹小",
                "value":  0.1,
                "text": "小公寓"
            },
            {
                "label": "空間適中",
                "value": 0.5,
                "text": "普通住宅"
            },
            {
                "label": "空間寬敞",
                "value": 0.9,
                "text": "大房子"
            }
        ]
    },
    {
        "id": "q8",
        "dimension_index": 3,
        "weight": 0.5,
        "text": "【Q8/12 空間需求】\n你能接受家中為了寵物擺放籠子或佔據生活空間嗎？",
        "options": [
            {
                "label": "沒地方放",
                "value":  0.1,
                "text": "無法接受"
            },
            {
                "label": "喬一下可以",
                "value": 0.5,
                "text":  "勉強接受"
            },
            {
                "label": "為了寵物可以",
                "value": 0.9,
                "text": "完全接受"
            }
        ]
    },
    # ==================== 維度 4: 掉毛程度 ====================
    {
        "id": "q9",
        "dimension_index": 4,
        "weight": 0.5,
        "text": "【Q9/12 掉毛程度】\n對於家中出現寵物毛髮，你的忍受程度？",
        "options": [
            {
                "label": "完全不能接受",
                "value": 0.1,
                "text": "潔癖"
            },
            {
                "label": "有一點沒關係",
                "value": 0.5,
                "text": "普通"
            },
            {
                "label": "視為日常",
                "value": 0.9,
                "text": "無所謂"
            }
        ]
    },
    {
        "id": "q10",
        "dimension_index": 4,
        "weight": 0.5,
        "text": "【Q10/12 掉毛程度】\n你願意每個月花多少預算在寵物美容上？",
        "options": [
            {
                "label": "越少越好",
                "value": 0.1,
                "text": "低預算"
            },
            {
                "label": "適度花費",
                "value":  0.5,
                "text": "中預算"
            },
            {
                "label": "不惜成本",
                "value": 0.9,
                "text": "高預算"
            }
        ]
    },
    # ==================== 維度 5: 吵鬧程度 ====================
    {
        "id":  "q11",
        "dimension_index": 5,
        "weight": 0.5,
        "text": "【Q11/12 吵鬧程度】\n你能接受寵物發出聲音對生活造成影響嗎？",
        "options": [
            {
                "label": "完全不能",
                "value": 0.1,
                "text": "較低程度"
            },
            {
                "label": "偶爾可以",
                "value": 0.5,
                "text":  "中等程度"
            },
            {
                "label": "習慣了",
                "value": 0.9,
                "text":  "較高程度"
            }
        ]
    },
    {
        "id": "q12",
        "dimension_index":  5,
        "weight":  0.5,
        "text": "【Q12/12 吵鬧程度】\n你的居住環境隔音效果如何？",
        "options": [
            {
                "label": "隔音差/怕投訴",
                "value":  0.1,
                "text": "隔音差"
            },
            {
                "label": "普通公寓",
                "value": 0.5,
                "text": "隔音普通"
            },
            {
                "label": "獨棟/不怕吵",
                "value": 0.9,
                "text": "隔音好"
            }
        ]
    }
]
# ChromaDB 初始化與查詢功能
client = chromadb.Client()
collection_name = "rimberio_pets_v1"
try:
    collection = client.get_collection(collection_name)
except:
    collection = client.create_collection(collection_name)
    ids = [p['id'] for p in PET_DB]
    embeddings = [p['vector'] for p in PET_DB]
    metadatas = [{"name": p['name'], "desc": p['desc']} for p in PET_DB]
    collection.add(ids=ids, embeddings=embeddings, metadatas=metadatas)
    print("ChromaDB 資料庫初始化完成，資料已寫入。")

def get_recommendations(user_vector, n_results=3):
    results = collection.query(
        query_embeddings=[user_vector],
        n_results=n_results
    )
    recommendations = []
    for i in range(len(results['ids'][0])):
        recommendations.append({
            "name": results['metadatas'][0][i]['name'],
            "desc": results['metadatas'][0][i]['desc'],
            "score": results['distances'][0][i]
        })
    return recommendations


def get_recommendations_with_type(user_vector, n_results=3, pet_type=None):
    # 如果指定類型，先過濾
    if pet_type:
        filtered_pets = [p for p in PET_DB if p.get("type") == pet_type]
        # 重新創建或更新 ChromaDB collection
        temp_collection_name = f"rimberio_pets_{pet_type}"
        try:
            temp_collection = client.get_collection(temp_collection_name)
        except:
            temp_collection = client.create_collection(temp_collection_name)
            ids = [p['id'] for p in filtered_pets]
            embeddings = [p['vector'] for p in filtered_pets]
            metadatas = [{"name": p['name'], "desc": p['desc'], "type": p.get("type", "unknown")} for p in filtered_pets]
            temp_collection.add(ids=ids, embeddings=embeddings, metadatas=metadatas)
        
        results = temp_collection.query(
            query_embeddings=[user_vector],
            n_results=min(n_results, len(filtered_pets))
        )
    else:
        results = collection.query(
            query_embeddings=[user_vector],
            n_results=n_results
        )
    
    recommendations = []
    for i in range(len(results['ids'][0])):
        recommendations.append({
            "name": results['metadatas'][0][i]['name'],
            "desc": results['metadatas'][0][i]['desc'],
            "type": results['metadatas'][0][i].get('type', 'unknown'),
            "score": results['distances'][0][i]
        })
    return recommendations


def validate_questions_weights():
    """驗證所有 QUESTIONS 的權重配置"""
    dimension_weights = {i: 0.0 for i in range(6)}
    dimension_count = {i: 0 for i in range(6)}
    
    for q in QUESTIONS:
        dim = q['dimension_index']
        weight = q.get('weight', 0.0)
        dimension_weights[dim] += weight
        dimension_count[dim] += 1
    print("="*50)
    errors = []
    for dim in range(6):
        total_weight = dimension_weights[dim]
        count = dimension_count[dim]
        print(f"維度 {dim}: {count} 題，權重總和 = {total_weight:.4f}")
        if abs(total_weight - 1.0) > 0.01:
            errors.append(f"維度 {dim}:  權重總和 = {total_weight:.4f} (應為 1.0)")
    print("="*50)
    if errors:
        print("權重驗證失敗：")
        for error in errors:
            print(f"  - {error}")
        return False
    else:
        print("所有維度的權重配置正確")
        return True
    
    
def validate_pet_types():
    """驗證所有寵物都有正確的 type 字段"""
    print("="*50)
    print("寵物類型驗證")
    dog_count = 0
    cat_count = 0
    unknown_count = 0
    for pet in PET_DB:
        pet_type = pet.get('type', 'unknown')
        if pet_type == 'dog': 
            dog_count += 1
        elif pet_type == 'cat':
            cat_count += 1
        else: 
            unknown_count += 1
            print(f"{pet['name']} 的 type 為 {pet_type}")
    print(f"狗狗: {dog_count} 隻")
    print(f"貓咪: {cat_count} 隻")
    if unknown_count > 0:
        print(f"未分類:  {unknown_count} 隻")
    print("="*50 + "\n")
    return dog_count > 0 and cat_count > 0 and unknown_count == 0