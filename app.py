"""
FastAPI 웹 서버
크롤링한 입찰공고 데이터를 REST API로 제공
"""

from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
import logging

from config import settings
from database import get_db, init_db
from models import Bidding


# ===== 로깅 설정 =====
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


# ===== FastAPI 앱 생성 =====
app = FastAPI(
    title="나라장터 입찰공고 API",
    description="공공 입찰공고 데이터 조회 API",
    version="1.0.0",
)


# ===== CORS 설정 =====
# 프론트엔드에서 API 호출 가능하게
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 모든 도메인 허용 (실무에서는 특정 도메인만)
    allow_credentials=True,
    allow_methods=["*"],  # 모든 HTTP 메서드 허용
    allow_headers=["*"],  # 모든 헤더 허용
)

"""
💡 CORS란?

브라우저 보안 정책:
- http://localhost:3000 (React)
- http://43.201.32.63 (API)
→ 다른 도메인 = 차단!

CORS 설정 = "이 API는 다른 도메인에서 호출 가능해요"
"""


# ===== Pydantic 스키마 =====
# API 응답 형식 정의
from pydantic import BaseModel


class BiddingResponse(BaseModel):
    """입찰공고 응답 스키마"""

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
        from_attributes = True  # ORM 모델 → Pydantic 변환 허용


"""
💡 Pydantic 스키마 역할:

1. 응답 형식 정의
   → API 문서 자동 생성
   
2. 데이터 검증
   → 타입 자동 체크
   
3. JSON 변환
   → ORM 객체 → JSON
"""


# ===== API 엔드포인트 =====


@app.on_event("startup")
async def startup_event():
    """
    서버 시작 시 실행
    데이터베이스 테이블 초기화
    """
    logger.info("🚀 서버 시작 중...")
    init_db()  # 테이블 생성 (없으면)
    logger.info("✅ 서버 시작 완료!")


@app.get("/")
def root():
    """
    루트 경로 - API 상태 확인

    Returns:
        dict: 상태 메시지
    """
    return {
        "message": "나라장터 입찰공고 API",
        "status": "running",
        "docs": "/docs",  # API 문서 경로
    }


"""
💡 사용 예시:
브라우저에서 http://43.201.32.63/ 접속
→ {"message": "나라장터 입찰공고 API", ...}
"""


@app.get("/api/biddings", response_model=List[BiddingResponse])
def get_biddings(
    skip: int = Query(0, ge=0, description="건너뛸 개수 (페이지네이션)"),
    limit: int = Query(100, ge=1, le=1000, description="가져올 개수 (최대 1000)"),
    search: Optional[str] = Query(None, description="검색어 (공고명)"),
    db: Session = Depends(get_db),
):
    """
    입찰공고 목록 조회

    Args:
        skip: 건너뛸 개수 (페이지네이션)
        limit: 가져올 개수
        search: 검색어 (공고명에서 검색)
        db: 데이터베이스 세션

    Returns:
        List[BiddingResponse]: 입찰공고 목록
    """
    logger.info(
        f"📋 입찰공고 목록 조회 요청 (skip={skip}, limit={limit}, search={search})"
    )

    # 기본 쿼리
    query = db.query(Bidding)

    # 검색어가 있으면 필터링
    if search:
        query = query.filter(Bidding.title.contains(search))

    # 최신순 정렬
    query = query.order_by(Bidding.created_at.desc())

    # 페이지네이션
    biddings = query.offset(skip).limit(limit).all()

    logger.info(f"✅ {len(biddings)}개 조회 완료")

    return biddings


"""
💡 사용 예시:

1. 전체 목록 (최신 100개)
   GET /api/biddings

2. 페이지네이션
   GET /api/biddings?skip=0&limit=20    (1페이지)
   GET /api/biddings?skip=20&limit=20   (2페이지)

3. 검색
   GET /api/biddings?search=컴퓨터

4. 검색 + 페이지네이션
   GET /api/biddings?search=책상&skip=0&limit=10
"""


@app.get("/api/biddings/{bidding_id}", response_model=BiddingResponse)
def get_bidding(bidding_id: int, db: Session = Depends(get_db)):
    """
    입찰공고 상세 조회

    Args:
        bidding_id: 공고 ID
        db: 데이터베이스 세션

    Returns:
        BiddingResponse: 입찰공고 상세 정보
    """
    logger.info(f"🔍 입찰공고 상세 조회 요청 (id={bidding_id})")

    bidding = db.query(Bidding).filter(Bidding.id == bidding_id).first()

    if not bidding:
        logger.warning(f"⚠️ 공고 없음 (id={bidding_id})")
        raise HTTPException(status_code=404, detail="공고를 찾을 수 없습니다")

    logger.info(f"✅ 조회 완료: {bidding.title}")

    return bidding


"""
💡 사용 예시:
GET /api/biddings/123
→ id가 123인 공고의 상세 정보
"""


@app.get("/api/stats")
def get_stats(db: Session = Depends(get_db)):
    """
    통계 정보 조회

    Args:
        db: 데이터베이스 세션

    Returns:
        dict: 통계 정보
    """
    logger.info("📊 통계 조회 요청")

    # 전체 공고 수
    total_count = db.query(Bidding).count()

    # 최근 7일 공고 수
    from datetime import timedelta

    week_ago = datetime.now() - timedelta(days=7)
    recent_count = db.query(Bidding).filter(Bidding.created_at >= week_ago).count()

    # 평균 예산금액 (NULL 제외)
    from sqlalchemy import func

    avg_budget = (
        db.query(func.avg(Bidding.budget_amount))
        .filter(Bidding.budget_amount.isnot(None))
        .scalar()
    )

    stats = {
        "total_biddings": total_count,
        "recent_biddings": recent_count,
        "average_budget": int(avg_budget) if avg_budget else 0,
    }

    logger.info(f"✅ 통계 조회 완료: {stats}")

    return stats


"""
💡 사용 예시:
GET /api/stats
→ {
    "total_biddings": 1500,
    "recent_biddings": 120,
    "average_budget": 50000000
  }
"""


@app.get("/api/agencies")
def get_agencies(
    limit: int = Query(10, ge=1, le=100, description="가져올 기관 수"),
    db: Session = Depends(get_db),
):
    """
    발주기관 목록 조회 (공고 수 많은 순)

    Args:
        limit: 가져올 기관 수
        db: 데이터베이스 세션

    Returns:
        list: 발주기관 목록과 공고 수
    """
    logger.info(f"🏢 발주기관 목록 조회 (limit={limit})")

    from sqlalchemy import func

    agencies = (
        db.query(Bidding.ordering_agency, func.count(Bidding.id).label("count"))
        .filter(Bidding.ordering_agency.isnot(None))
        .group_by(Bidding.ordering_agency)
        .order_by(func.count(Bidding.id).desc())
        .limit(limit)
        .all()
    )

    result = [{"agency": agency, "count": count} for agency, count in agencies]

    logger.info(f"✅ {len(result)}개 기관 조회 완료")

    return result


"""
💡 사용 예시:
GET /api/agencies?limit=10
→ [
    {"agency": "교육부", "count": 150},
    {"agency": "국방부", "count": 120},
    ...
  ]
"""


@app.post("/api/crawl")
async def trigger_crawl():
    """
    크롤링 수동 실행 (관리자용)

    Returns:
        dict: 크롤링 결과
    """
    logger.info("🤖 수동 크롤링 요청")

    try:
        from crawler import NaramarketCrawler

        crawler = NaramarketCrawler()
        stats = crawler.crawl(max_pages=5)  # 5페이지만 크롤링

        logger.info(f"✅ 크롤링 완료: {stats}")

        return {"status": "success", "message": "크롤링 완료", "stats": stats}

    except Exception as e:
        logger.error(f"❌ 크롤링 실패: {e}")
        raise HTTPException(status_code=500, detail=f"크롤링 실패: {str(e)}")


"""
💡 사용 예시:
POST /api/crawl
→ 크롤러 실행
→ {"status": "success", "stats": {...}}
"""


# ===== 헬스체크 =====
@app.get("/health")
def health_check():
    """
    서버 상태 확인 (헬스체크)

    Returns:
        dict: 상태 정보
    """
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}


"""
💡 Docker/Kubernetes 헬스체크용
컨테이너가 정상 동작하는지 확인
"""


# ===== 서버 실행 =====
if __name__ == "__main__":
    """
    개발 환경에서 직접 실행

    실행 방법:
    python app.py
    """
    import uvicorn

    uvicorn.run(
        "app:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=True,  # 코드 수정 시 자동 재시작 (개발용)
    )


"""
💡 전체 API 목록:

1. GET  /                     - API 상태
2. GET  /api/biddings         - 입찰공고 목록
3. GET  /api/biddings/{id}    - 입찰공고 상세
4. GET  /api/stats            - 통계 정보
5. GET  /api/agencies         - 발주기관 목록
6. POST /api/crawl            - 크롤링 실행
7. GET  /health               - 헬스체크

API 문서 (자동 생성):
- Swagger UI: http://43.201.32.63/docs
- ReDoc:      http://43.201.32.63/redoc
"""


"""
💡 사용 시나리오:

1. 프론트엔드 개발자:
   - /api/biddings 호출
   - JSON 받아서 React로 화면 표시

2. 데이터 분석가:
   - /api/stats 호출
   - 통계 데이터 분석

3. 시스템 관리자:
   - /api/crawl 호출
   - 수동으로 데이터 수집

4. 모니터링:
   - /health 호출
   - 서버 상태 확인
"""
