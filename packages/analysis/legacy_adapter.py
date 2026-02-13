import os
from typing import List, Optional

LEGACY_PROJECT_PATH = os.path.join(os.path.dirname(__file__), "legacy_project")
RESULT_PATH = os.path.join(LEGACY_PROJECT_PATH, "result")

def get_available_images() -> List[str]:
    """获取所有可用的分析图表图片"""
    if not os.path.exists(RESULT_PATH):
        return []
    
    # 过滤出图片文件
    images = [
        f for f in os.listdir(RESULT_PATH) 
        if f.lower().endswith(('.png', '.jpg', '.jpeg', '.svg')) and not f.startswith('.')
    ]
    return sorted(images)

def get_image_path(image_name: str) -> Optional[str]:
    """获取特定图片的完整路径"""
    # 防止路径遍历攻击
    if '..' in image_name or '/' in image_name or '\\' in image_name:
        return None
        
    image_path = os.path.join(RESULT_PATH, image_name)
    if os.path.exists(image_path) and os.path.isfile(image_path):
        return image_path
    return None

def get_image_metadata(image_name: str) -> dict:
    """获取图片的元数据（如标题、描述等）"""
    # 简单的文件名到标题的映射
    title_map = {
        "clinical_trials_count_by_country.png": "各国临床试验数量分布",
        "clinical_trials_trend.png": "临床试验数量趋势",
        "clinical_trials_trend2.png": "临床试验状态趋势",
        "clinical_trials_fails.png": "失败原因分析",
        "clinical_trials_fails_cropped.png": "失败原因分析（裁剪版）",
        "clinical_trials_quanzhong.png": "权重分布分析",
        "clinical_trials_quanzhong_cropped.png": "权重分布分析（裁剪版）",
        "clinical_trials_trend_cropped.png": "趋势分析（裁剪版）",
        "clinical_trials_trend2_cropped.png": "状态趋势分析（裁剪版）",
        "clinical_trials_map_cropped.png": "全球分布地图（裁剪版）",
        "各个类别生存图.png": "不同类别的生存曲线",
    }
    
    return {
        "filename": image_name,
        "title": title_map.get(image_name, image_name),
        "url": f"/api/analysis/images/{image_name}"
    }
