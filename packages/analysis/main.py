from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os
from dotenv import load_dotenv
from routers.analysis_router import router as analysis_router
from routers.image_router import router as image_router

# 加载环境变量
load_dotenv()

app = FastAPI(
    title="Clinical Trial Analysis API",
    description="Python backend for clinical trial data mining and analysis",
    version="1.0.0"
)

# 配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 在生产环境中应该设置为具体的域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(analysis_router)
app.include_router(image_router)

@app.get("/")
async def root():
    return {"message": "Welcome to Clinical Trial Analysis Service"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
