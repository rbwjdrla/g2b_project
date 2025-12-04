from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
from database import get_db
from models import Bidding
from schemas import BiddingResponse, BiddingListResponse
import logging

router = APIRouter(prefix="/api", tags=["입찰공고"])
logger = logging.getLogger(__name__)

@router.get("/biddings", response_model=BiddingListResponse)
def get_biddings(
    skip: int = Query(0, ge=0, description="건너뛸 개수"),
    limit: int = Query(20, ge=1, le=100, description="가져올 개수"),
    notice_type: Optional[str] = Query(None, description="공고 유형 (공사/용역/물품)"),
    search: Optional[str] = Query(None, description="공고명 검색어"),
    db: Session = Depends(get_db),
):
    """입찰공고 목록 조회"""
    logger.info(f"📋 입찰공고 목록 조회 (skip={skip}, limit={limit}, type={notice_type}, search={search})")
    
    query = db.query(Bidding)
    
    # 유형 필터
    if notice_type:
        query = query.filter(Bidding.notice_type == notice_type)
    
    # 검색
    if search:
        query = query.filter(Bidding.title.contains(search))
    
    # 최신순 정렬
    query = query.order_by(Bidding.notice_date.desc())
    
    # 전체 개수
    total = query.count()
    
    # 페이징
    items = query.offset(skip).limit(limit).all()
    
    return {
        "total": total,
        "items": items,
        "skip": skip,
        "limit": limit
    }

@router.get("/biddings/{bidding_id}", response_model=BiddingResponse)
def get_bidding(bidding_id: int, db: Session = Depends(get_db)):
    """입찰공고 상세 조회"""
    logger.info(f"📋 입찰공고 상세 조회 (id={bidding_id})")
    
    bidding = db.query(Bidding).filter(Bidding.id == bidding_id).first()
    if not bidding:
        raise HTTPException(status_code=404, detail="공고를 찾을 수 없습니다.")
    return bidding
