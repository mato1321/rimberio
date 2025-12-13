import matplotlib.pyplot as plt
import matplotlib
import numpy as np
from io import BytesIO
import base64

# 設定中文字體
matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'DejaVu Sans']
matplotlib.rcParams['axes.unicode_minus'] = False

# 六維度名稱（中文）- 與圖片一致
DIMENSION_LABELS_CN = ['活動力', '親人程度', '獨立性', '空間需求', '掉毛程度', '吵鬧程度']

def generate_radar_chart(user_vector, pet_vectors_dict, output_path=None):
    """
    生成雷達圖表 (只有雷達圖，不要長條圖)
    
    Args:
        user_vector: 使用者的向量 [0.8, 0.6, 0.4, ...]
        pet_vectors_dict: 寵物及其向量的字典
                        {'英國短毛貓': [0.2, 0.3, 0.9, ...],
                        '暹羅貓': [0.6, 1.0, 0.1, ...]}
        output_path: 輸出檔案路徑
    
    Returns:
        檔案路徑或 Base64 編碼的圖像
    """
    
    # 設定角度
    angles = np.linspace(0, 2 * np.pi, len(DIMENSION_LABELS_CN), endpoint=False).tolist()
    angles += angles[:1]  # 閉合圖形
    
    # 建立圖表 (與你的圖片尺寸相近)
    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(projection='polar'))
    fig.patch.set_facecolor('white')
    
    # 繪製使用者向量 (紅色，主要顏色)
    user_vector_plot = user_vector + user_vector[:1]
    ax.plot(angles, user_vector_plot, 'o-', linewidth=2.5, label='你的偏好', 
            color='#FF6B6B', markersize=6)
    ax.fill(angles, user_vector_plot, alpha=0.3, color='#FF6B6B')
    
    # 定義寵物顏色 (灰色背景網格)
    colors = ['#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8', '#F7DC6F']
    
    # 繪製寵物向量
    for idx, (pet_name, pet_vector) in enumerate(pet_vectors_dict.items()):
        pet_vector_plot = pet_vector + pet_vector[:1]
        color = colors[idx % len(colors)]
        ax.plot(angles, pet_vector_plot, 'o-', linewidth=1.5, label=pet_name, 
                color=color, markersize=4, alpha=0.7)
        ax.fill(angles, pet_vector_plot, alpha=0.1, color=color)
    
    # 設定標籤 (中文標籤)
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(DIMENSION_LABELS_CN, size=10, weight='bold')
    
    # 設定徑向網格
    ax.set_ylim(0, 1.0)
    ax.set_yticks([0.2, 0.4, 0.6, 0.8])
    ax.set_yticklabels(['20', '40', '60', '80'], size=8, color='gray')
    ax.set_rlabel_position(0)
    ax.grid(True, linestyle='-', alpha=0.3, color='gray', linewidth=0.5)
    
    # 設定圖例
    ax.legend(loc='upper right', bbox_to_anchor=(1.2, 1.1), fontsize=9, framealpha=0.9)
    
    # 標題
    plt.title('🐾 六維與情指數', size=13, weight='bold', pad=15)
    
    plt.tight_layout()
    
    # 返回或儲存
    if output_path:
        plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
        plt.close()
        return output_path
    else: 
        # 轉換為 Base64
        buffer = BytesIO()
        plt.savefig(buffer, format='png', dpi=150, bbox_inches='tight', facecolor='white')
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.read()).decode()
        plt.close()
        return image_base64


def generate_user_only_radar(user_vector, output_path=None):
    """
    只生成使用者的雷達圖 (不要長條圖)
    """
    angles = np.linspace(0, 2 * np.pi, len(DIMENSION_LABELS_CN), endpoint=False).tolist()
    angles += angles[:1]
    
    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(projection='polar'))
    fig.patch.set_facecolor('white')
    
    # 使用者向量 (紅色)
    user_vector_plot = user_vector + user_vector[:1]
    ax.plot(angles, user_vector_plot, 'o-', linewidth=2.5, color='#FF6B6B', markersize=6)
    ax.fill(angles, user_vector_plot, alpha=0.3, color='#FF6B6B')
    
    # 設定標籤
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(DIMENSION_LABELS_CN, size=10, weight='bold')
    
    ax.set_ylim(0, 1.0)
    ax.set_yticks([0.2, 0.4, 0.6, 0.8])
    ax.set_yticklabels(['20', '40', '60', '80'], size=8, color='gray')
    ax.set_rlabel_position(0)
    ax.grid(True, linestyle='-', alpha=0.3, color='gray', linewidth=0.5)
    
    plt.title('📊 你的六維偏好指數', size=13, weight='bold', pad=15)
    
    plt.tight_layout()
    
    if output_path:
        plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
        plt.close()
        return output_path
    else:
        buffer = BytesIO()
        plt.savefig(buffer, format='png', dpi=150, bbox_inches='tight', facecolor='white')
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.read()).decode()
        plt.close()
        return image_base64


def generate_pet_comparison_radar(user_vector, pet_name, pet_vector, output_path=None):
    """
    生成使用者和單一寵物的對比雷達圖 (只有雷達圖)
    """
    angles = np.linspace(0, 2 * np.pi, len(DIMENSION_LABELS_CN), endpoint=False).tolist()
    angles += angles[:1]
    
    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(projection='polar'))
    fig.patch.set_facecolor('white')
    
    # 使用者向量 (紅色)
    user_vector_plot = user_vector + user_vector[:1]
    ax.plot(angles, user_vector_plot, 'o-', linewidth=2.5, label='你的偏好', 
            color='#FF6B6B', markersize=6)
    ax.fill(angles, user_vector_plot, alpha=0.3, color='#FF6B6B')
    
    # 寵物向量 (藍綠色)
    pet_vector_plot = pet_vector + pet_vector[:1]
    ax.plot(angles, pet_vector_plot, 'o-', linewidth=2.5, label=pet_name, 
            color='#4ECDC4', markersize=6)
    ax.fill(angles, pet_vector_plot, alpha=0.2, color='#4ECDC4')
    
    # 設定標籤
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(DIMENSION_LABELS_CN, size=10, weight='bold')
    
    ax.set_ylim(0, 1.0)
    ax.set_yticks([0.2, 0.4, 0.6, 0.8])
    ax.set_yticklabels(['20', '40', '60', '80'], size=8, color='gray')
    ax.set_rlabel_position(0)
    ax.grid(True, linestyle='-', alpha=0.3, color='gray', linewidth=0.5)
    
    ax.legend(loc='upper right', bbox_to_anchor=(1.2, 1.1), fontsize=9, framealpha=0.9)
    
    plt.title(f'🐾 與 {pet_name} 的相性', size=13, weight='bold', pad=15)
    
    plt.tight_layout()
    
    if output_path: 
        plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
        plt.close()
        return output_path
    else:
        buffer = BytesIO()
        plt.savefig(buffer, format='png', dpi=150, bbox_inches='tight', facecolor='white')
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.read()).decode()
        plt.close()
        return image_base64


# 使用範例
if __name__ == "__main__":
    # 測試資料
    user_vector = [0.9, 0.3, 0.5, 0.2, 0.1, 0.6]
    
    pet_vectors = {
        '英國短毛貓':  [0.2, 0.3, 0.9, 0.2, 0.5, 0.1],
        '暹羅貓':  [0.6, 1.0, 0.1, 0.2, 0.3, 0.9],
        '邊境牧羊犬': [1.0, 0.6, 0.3, 0.9, 0.8, 0.7]
    }
    
    # 生成完整對比圖
    generate_radar_chart(user_vector, pet_vectors, 'radar_full.png')
    print("✅ 完整對比圖已生成:  radar_full.png")
    
    # 生成單一使用者圖
    generate_user_only_radar(user_vector, 'radar_user.png')
    print("✅ 使用者圖已生成: radar_user.png")
    
    # 生成單一寵物對比
    generate_pet_comparison_radar(user_vector, '英國短毛貓', 
                                    pet_vectors['英國短毛貓'], 'radar_pet.png')
    print("✅ 寵物對比圖已生成: radar_pet.png")