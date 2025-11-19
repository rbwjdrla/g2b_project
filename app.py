"""
FastAPI 웹 서버
공공데이터포털(G2B) API 기반 입찰공고 데이터 제공 + APScheduler 자동수집 포함
"""

from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta
import logging

from config import settings
from database import get_db, init_db
from models import Bidding
from g2b.main_crawler import run_all

# APScheduler
from apscheduler.schedulers.background import BackgroundScheduler

# ==================== 로깅 설정 ====================
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# ==================== FastAPI 앱 생성 ====================
app = FastAPI(
    title="G2B 입찰정보 API 서버",
    description="공공데이터포털 API를 통해 수집한 입찰공고/발주/계약/낙찰 데이터를 제공합니다.",
    version="2.0.0",
)

# ==================== CORS 설정 ====================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 개발 단계에서는 모든 도메인 허용
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==================== Pydantic 스키마 ====================
from pydantic import BaseModel


class BiddingResponse(BaseModel):
    id: int
    notice_number: str
    title: str
    ordering_agency: Optional[str] = None
    demanding_agency: Optional[str] = None
    contract_method: Optional[str] = None
    bidding_method: Optional[str] = None
    budget_amount: Optional[int] = None
    estimated_price: Optional[int] = None
    notice_date: Optional[datetime] = None
    bid_close_date: Optional[datetime] = None
    description: Optional[str] = None
    bidding_url: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True  # ORM → Pydantic 변환


# ==================== DB 초기화 이벤트 ====================
@app.on_event("startup")
def startup_event():
    logger.info("🚀 서버 시작 중…")
    init_db()
    logger.info("✅ 데이터베이스 초기화 완료")


# ==================== APScheduler 설정 ====================
scheduler = BackgroundScheduler()


def scheduled_job():
    """
    매일 새벽 3시 자동으로 데이터 수집
    """
    logger.info("⏳ 자동 스케줄러 실행: 어제~오늘 데이터 수집 시작")

    try:
        end_date = datetime.now()
        start_date = end_date - timedelta(days=1)
        start_day = start_date.strftime("%Y%m%d")
        end_day = end_date.strftime("%Y%m%d")

        run_all(settings.SERVICE_KEY, start_day, end_day)
        logger.info("✅ 자동 데이터 수집 완료")

    except Exception as e:
        logger.error(f"❌ 스케줄러 오류: {e}")


@app.on_event("startup")
def start_scheduler():
    """
    서버가 켜질 때 스케줄러도 함께 켠다
    """
    scheduler.add_job(scheduled_job, "cron", hour=3, minute=0)
    scheduler.start()
    logger.info("🔔 APScheduler 활성화 완료 (매일 03:00 자동 실행)")


# ==================== 루트 엔드포인트 ====================
@app.get("/")
def root():
    return {
        "message": "G2B 입찰공고 API 서버 작동 중",
        "version": "2.0.0",
        "docs": "/docs",
    }


# ==================== API: 입찰공고 목록 ====================
@app.get("/api/biddings", response_model=List[BiddingResponse])
def get_biddings(
    skip: int = Query(0, ge=0, description="건너뛸 개수"),
    limit: int = Query(100, ge=1, le=1000, description="가져올 개수"),
    search: Optional[str] = Query(None, description="공고명 검색어"),
    db: Session = Depends(get_db),
):
    logger.info(f"📋 입찰공고 목록 조회 (skip={skip}, limit={limit}, search={search})")

    query = db.query(Bidding)
    if search:
        query = query.filter(Bidding.title.contains(search))

    query = query.order_by(Bidding.created_at.desc())
    results = query.offset(skip).limit(limit).all()

    logger.info(f"✅ {len(results)}개 조회 완료")
    return results


# ==================== API: 단일 공고 조회 ====================
@app.get("/api/biddings/{bidding_id}", response_model=BiddingResponse)
def get_bidding(bidding_id: int, db: Session = Depends(get_db)):
    bidding = db.query(Bidding).filter(Bidding.id == bidding_id).first()
    if not bidding:
        raise HTTPException(status_code=404, detail="공고를 찾을 수 없습니다.")
    return bidding


# ==================== API: 통계 조회 ====================
@app.get("/api/stats")
def get_stats(db: Session = Depends(get_db)):
    from sqlalchemy import func

    logger.info("📊 통계 조회 요청")

    total_count = db.query(Bidding).count()
    week_ago = datetime.now() - timedelta(days=7)
    recent_count = db.query(Bidding).filter(Bidding.created_at >= week_ago).count()

    avg_budget = (
        db.query(func.avg(Bidding.budget_amount))
        .filter(Bidding.budget_amount.isnot(None))
        .scalar()
    )

    return {
        "total_biddings": total_count,
        "recent_biddings": recent_count,
        "average_budget": int(avg_budget) if avg_budget else 0,
    }


# ==================== API: 기관별 공고 수 ====================
@app.get("/api/agencies")
def get_agencies(limit: int = Query(10, ge=1, le=100), db: Session = Depends(get_db)):
    from sqlalchemy import func

    agencies = (
        db.query(Bidding.ordering_agency, func.count(Bidding.id).label("count"))
        .filter(Bidding.ordering_agency.isnot(None))
        .group_by(Bidding.ordering_agency)
        .order_by(func.count(Bidding.id).desc())
        .limit(limit)
        .all()
    )

    return [{"agency": agency, "count": count} for agency, count in agencies]


# ==================== API: 데이터 수동 수집 ====================
@app.post("/api/crawl")
async def trigger_g2b_update(days: int = 3):
    logger.info(f"🤖 {days}일간 G2B 데이터 수집 요청")

    try:
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        start_day = start_date.strftime("%Y%m%d")
        end_day = end_date.strftime("%Y%m%d")

        run_all(settings.SERVICE_KEY, start_day, end_day)

        return {"status": "success", "message": f"{days}일간 데이터 수집 완료"}

    except Exception as e:
        logger.error(f"❌ 데이터 수집 실패: {e}")
        raise HTTPException(status_code=500, detail=f"API 수집 실패: {str(e)}")


# ==================== 헬스체크 ====================
@app.get("/health")
def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}


# ==================== 로컬 실행 ====================
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=True,
    )
