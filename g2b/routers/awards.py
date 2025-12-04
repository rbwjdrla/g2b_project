from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Optional
from database import get_db
from models import Award
from schemas import AwardResponse, AwardListResponse
import logging

router = APIRouter(prefix="/api", tags=["낙찰정보"])
logger = logging.getLogger(__name__)

@router.get("/awards", response_model=AwardListResponse)
def get_awards(
    skip: int = Query(0, ge=0, description="건너뛸 개수"),
    limit: int = Query(20, ge=1, le=100, description="가져올 개수"),
    notice_type: Optional[str] = Query(None, description="공고 유형"),
    search: Optional[str] = Query(None, description="업체명 검색"),
    db: Session = Depends(get_db),
):
    """낙찰정보 목록 조회"""
    logger.info(f"🏆 낙찰정보 목록 조회 (skip={skip}, limit={limit})")
    
    query = db.query(Award)
    
    # 유형 필터
    if notice_type:
        query = query.filter(Award.notice_type == notice_type)
    
    # 검색
    if search:
        query = query.filter(Award.award_company_name.contains(search))
    
    # 최신순
    query = query.order_by(Award.opening_date.desc())
    
    total = query.count()
    items = query.offset(skip).limit(limit).all()
    
    return {
        "total": total,
        "items": items,
        "skip": skip,
        "limit": limit
    }

@router.get("/awards/{award_id}", response_model=AwardResponse)
def get_award(award_id: int, db: Session = Depends(get_db)):
    """낙찰정보 상세 조회"""
    logger.info(f"🏆 낙찰정보 상세 조회 (id={award_id})")
    
    award = db.query(Award).filter(Award.id == award_id).first()
    if not award:
        raise HTTPException(status_code=404, detail="낙찰정보를 찾을 수 없습니다.")
    return award

@router.get("/awards/statistics/top-companies")
def get_top_companies(
    limit: int = Query(10, ge=1, le=50, description="조회 개수"),
    db: Session = Depends(get_db)
):
    """낙찰 업체 TOP"""
    logger.info(f"🏆 낙찰 업체 TOP {limit} 조회")
    
    top_companies = db.query(
        Award.award_company_name,
        func.count(Award.id).label('count'),
        func.sum(Award.award_amount).label('total_amount'),
        func.avg(Award.award_rate).label('avg_rate')
    ).filter(
        Award.award_company_name.isnot(None)
    ).group_by(
        Award.award_company_name
    ).order_by(
        func.count(Award.id).desc()
    ).limit(limit).all()
    
    return [
        {
            "company": company,
            "count": count,
            "total_amount": int(total_amount or 0),
            "avg_rate": round(float(avg_rate or 0), 2)
        }
        for company, count, total_amount, avg_rate in top_companies
    ]
