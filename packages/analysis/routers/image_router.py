from fastapi import APIRouter
from fastapi.responses import FileResponse, JSONResponse
from legacy_adapter import get_available_images, get_image_path, get_image_metadata

router = APIRouter(
    prefix="/api/analysis/images",
    tags=["images"]
)

# ==========================================
# 静态图表资源接口 (Legacy)
# ==========================================

@router.get("")
async def list_analysis_images():
    """获取所有可用的分析图表列表"""
    try:
        images = get_available_images()
        result = [get_image_metadata(img) for img in images]
        return {"code": 200, "data": result, "msg": "success"}
    except Exception as e:
        return JSONResponse(status_code=500, content={"code": 500, "msg": str(e)})

@router.get("/{image_name}")
async def get_analysis_image(image_name: str):
    """获取特定的分析图表图片文件"""
    image_path = get_image_path(image_name)
    if not image_path:
        return JSONResponse(status_code=404, content={"code": 404, "msg": "Image not found"})
    
    return FileResponse(image_path)
