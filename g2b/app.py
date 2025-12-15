"""
FastAPI 웹 서버
G2B API 기반 입찰공고/낙찰정보/발주계획 데이터 제공
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging

from config import settings
from database import init_db
from scheduler import create_scheduler, scheduled_job

# ==================== 로깅 설정 ====================
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# ==================== 스케줄러 생성 ====================
scheduler = create_scheduler()

# ==================== 라이프사이클 ====================
@asynccontextmanager
async def lifespan(app: FastAPI):
    """앱 시작/종료 시 실행"""
    # 시작
    logger.info("🚀 FastAPI 서버 시작")
    init_db()
    logger.info("✅ 데이터베이스 초기화 완료")
    
    # 스케줄러 시작 - 1시간마다 2일치 데이터 수집
    scheduler.add_job(
        scheduled_job,
        trigger="interval",
        hours=1,
        id="scheduled_job",
        replace_existing=True
    )
    scheduler.start()
    logger.info("✅ 스케줄러 시작 (1시간마다 2일치 데이터 수집)")
    
    yield
    
    # 종료
    scheduler.shutdown()
    logger.info("🛑 스케줄러 종료")

# ==================== FastAPI 앱 ====================
app = FastAPI(
    title="G2B 입찰공고 API",
    description="나라장터 입찰공고/낙찰정보/발주계획 조회 API",
    version="2.0.0",
    lifespan=lifespan
)

# ==================== CORS ====================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==================== 라우터 연결 ====================
from routers import biddings, awards, orderplans, statistics, ml

app.include_router(biddings.router)
app.include_router(awards.router)
app.include_router(orderplans.router)
app.include_router(statistics.router)
app.include_router(ml.router)

# ==================== 기본 엔드포인트 ====================
@app.get("/")
def root():
    return {
        "message": "G2B 입찰공고 API 서버 작동 중",
        "version": "2.0.0",
        "docs": "/docs",
    }

@app.get("/health")
def health_check():
    from datetime import datetime
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    }

# ==================== 수동 수집 ====================
@app.post("/collect")
def manual_collect(days: int = 2):
    """수동 데이터 수집 트리거"""
    from apis.main import run_all

    logger.info(f"🔄 수동 데이터 수집 시작 ({days}일)")
    try:
        run_all(days=days)
        return {"status": "success", "message": f"데이터 수집 완료 ({days}일)"}
    except Exception as e:
        logger.error(f"❌ 수동 데이터 수집 실패: {e}")
        return {"status": "error", "message": str(e)}

# ==================== 로컬 실행 ====================
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=True,
    )