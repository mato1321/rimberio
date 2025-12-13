import matplotlib.pyplot as plt
import matplotlib
import numpy as np
from io import BytesIO
import base64
import cloudinary
import cloudinary.uploader
import tempfile
import os
matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'DejaVu Sans']
matplotlib.rcParams['axes.unicode_minus'] = False
DIMENSION_LABELS_CN = ['活動力', '親人程度', '獨立性', '空間需求', '掉毛程度', '吵鬧程度']

def set_cloudinary_credentials(cloud_name, api_key, api_secret):
    cloudinary.config(
        cloud_name=cloud_name,
        api_key=api_key,
        api_secret=api_secret
    )

def upload_to_cloudinary(image_path):
    try:
        result = cloudinary.uploader.upload(
            image_path,
            folder="rimberio",
            resource_type="image",
            quality="auto"
        )
        return result['secure_url']
    except Exception as e:
        print(f"Cloudinary 上傳失敗: {e}")
        return None

def generate_radar_chart(user_vector, pet_vectors_dict, output_path=None):    
    # 設定角度
    angles = np.linspace(0, 2 * np.pi, len(DIMENSION_LABELS_CN), endpoint=False).tolist()
    angles += angles[:1]
    
    # 建立圖表
    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(projection='polar'))
    fig.patch.set_facecolor('white')
    
    # 繪製使用者向量 (紅色)
    user_vector_plot = user_vector + user_vector[:1]
    ax.plot(angles, user_vector_plot, 'o-', linewidth=2.5, label='你的偏好', 
            color='#FF6B6B', markersize=6)
    ax.fill(angles, user_vector_plot, alpha=0.3, color='#FF6B6B')
    
    # 定義寵物顏色
    colors = ['#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8', '#F7DC6F']
    
    # 繪製寵物向量
    for idx, (pet_name, pet_vector) in enumerate(pet_vectors_dict.items()):
        pet_vector_plot = pet_vector + pet_vector[:1]
        color = colors[idx % len(colors)]
        ax.plot(angles, pet_vector_plot, 'o-', linewidth=1.5, label=pet_name, 
                color=color, markersize=4, alpha=0.7)
        ax.fill(angles, pet_vector_plot, alpha=0.1, color=color)
    
    # 設定標籤
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
    plt.title('六維偏好指數', size=13, weight='bold', pad=15)
    
    plt.tight_layout()
    
    # 儲存到臨時檔案
    temp_file = tempfile.NamedTemporaryFile(suffix='.png', delete=False)
    temp_path = temp_file.name
    temp_file.close()
    
    plt.savefig(temp_path, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    
    # 上傳到 Cloudinary
    cloud_url = upload_to_cloudinary(temp_path)
    
    # 刪除臨時檔案
    os.unlink(temp_path)
    
    return cloud_url


def generate_user_only_radar(user_vector, output_path=None):
    angles = np.linspace(0, 2 * np.pi, len(DIMENSION_LABELS_CN), endpoint=False).tolist()
    angles += angles[:1]
    
    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(projection='polar'))
    fig.patch.set_facecolor('white')
    
    user_vector_plot = user_vector + user_vector[:1]
    ax.plot(angles, user_vector_plot, 'o-', linewidth=2.5, color='#FF6B6B', markersize=6)
    ax.fill(angles, user_vector_plot, alpha=0.3, color='#FF6B6B')
    
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(DIMENSION_LABELS_CN, size=10, weight='bold')
    
    ax.set_ylim(0, 1.0)
    ax.set_yticks([0.2, 0.4, 0.6, 0.8])
    ax.set_yticklabels(['20', '40', '60', '80'], size=8, color='gray')
    ax.set_rlabel_position(0)
    ax.grid(True, linestyle='-', alpha=0.3, color='gray', linewidth=0.5)
    
    plt.title('你的六維偏好指數', size=13, weight='bold', pad=15)
    
    plt.tight_layout()
    
    # 儲存到臨時檔案
    temp_file = tempfile.NamedTemporaryFile(suffix='.png', delete=False)
    temp_path = temp_file.name
    temp_file.close()
    
    plt.savefig(temp_path, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    
    # 上傳到 Cloudinary
    cloud_url = upload_to_cloudinary(temp_path)
    
    # 刪除臨時檔案
    os.unlink(temp_path)
    
    return cloud_url


def generate_pet_comparison_radar(user_vector, pet_name, pet_vector, output_path=None):
    angles = np.linspace(0, 2 * np.pi, len(DIMENSION_LABELS_CN), endpoint=False).tolist()
    angles += angles[:1]
    
    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(projection='polar'))
    fig.patch.set_facecolor('white')
    
    user_vector_plot = user_vector + user_vector[:1]
    ax.plot(angles, user_vector_plot, 'o-', linewidth=2.5, label='你的偏好', 
            color='#FF6B6B', markersize=6)
    ax.fill(angles, user_vector_plot, alpha=0.3, color='#FF6B6B')
    
    pet_vector_plot = pet_vector + pet_vector[:  1]
    ax.plot(angles, pet_vector_plot, 'o-', linewidth=2.5, label=pet_name, 
            color='#4ECDC4', markersize=6)
    ax.fill(angles, pet_vector_plot, alpha=0.2, color='#4ECDC4')
    
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(DIMENSION_LABELS_CN, size=10, weight='bold')
    
    ax.set_ylim(0, 1.0)
    ax.set_yticks([0.2, 0.4, 0.6, 0.8])
    ax.set_yticklabels(['20', '40', '60', '80'], size=8, color='gray')
    ax.set_rlabel_position(0)
    ax.grid(True, linestyle='-', alpha=0.3, color='gray', linewidth=0.5)
    
    ax.legend(loc='upper right', bbox_to_anchor=(1.2, 1.1), fontsize=9, framealpha=0.9)
    
    plt.title(f'與 {pet_name} 的相性', size=13, weight='bold', pad=15)
    
    plt.tight_layout()
    
    # 儲存到臨時檔案
    temp_file = tempfile.NamedTemporaryFile(suffix='.png', delete=False)
    temp_path = temp_file.name
    temp_file.close()
    
    plt.savefig(temp_path, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    
    # 上傳到 Cloudinary
    cloud_url = upload_to_cloudinary(temp_path)
    
    # 刪除臨時檔案
    os.unlink(temp_path)
    
    return cloud_url