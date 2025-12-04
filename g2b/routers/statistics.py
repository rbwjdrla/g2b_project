from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, cast, Date
from database import get_db
from models import Bidding, Award, OrderPlan
import logging

router = APIRouter(prefix="/api", tags=["통계"])
logger = logging.getLogger(__name__)

@router.get("/statistics/summary")
def get_statistics_summary(db: Session = Depends(get_db)):
    """전체 통계 요약"""
    logger.info("📊 통계 요약 조회")
    
    # 입찰공고
    total_biddings = db.query(Bidding).count()
    
    # 유형별 입찰공고
    bidding_by_type = db.query(
        Bidding.notice_type,
        func.count(Bidding.id).label('count')
    ).filter(
        Bidding.notice_type.isnot(None)
    ).group_by(
        Bidding.notice_type
    ).all()
    
    # 낙찰정보
    total_awards = db.query(Award).count()
    
    # 발주계획
    total_order_plans = db.query(OrderPlan).count()
    
    # 총 예산
    total_budget = db.query(func.sum(Bidding.budget_amount)).scalar() or 0
    
    # 총 낙찰액
    total_award_amount = db.query(func.sum(Award.award_amount)).scalar() or 0
    
    return {
        "total_biddings": total_biddings,
        "total_awards": total_awards,
        "total_order_plans": total_order_plans,
        "total_budget": int(total_budget),
        "total_award_amount": int(total_award_amount),
        "bidding_by_type": [
            {"type": t, "count": c} for t, c in bidding_by_type
        ]
    }

@router.get("/statistics/daily")
def get_daily_statistics(
    days: int = Query(30, ge=1, le=90, description="조회 일수"),
    db: Session = Depends(get_db)
):
    """일별 통계"""
    logger.info(f"📊 일별 통계 조회 ({days}일)")
    
    daily_stats = db.query(
        cast(Bidding.notice_date, Date).label('date'),
        func.count(Bidding.id).label('count')
    ).filter(
        Bidding.notice_date.isnot(None)
    ).group_by(
        cast(Bidding.notice_date, Date)
    ).order_by(
        cast(Bidding.notice_date, Date).desc()
    ).limit(days).all()
    
    return [
        {"date": str(date), "count": count} 
        for date, count in reversed(daily_stats)
    ]

@router.get("/statistics/top-agencies")
def get_top_agencies(
    limit: int = Query(10, ge=1, le=50, description="조회 개수"),
    db: Session = Depends(get_db)
):
    """발주기관 TOP"""
    logger.info(f"📊 발주기관 TOP {limit} 조회")
    
    top_agencies = db.query(
        Bidding.ordering_agency,
        func.count(Bidding.id).label('count'),
        func.sum(Bidding.budget_amount).label('total_budget')
    ).filter(
        Bidding.ordering_agency.isnot(None)
    ).group_by(
        Bidding.ordering_agency
    ).order_by(
        func.count(Bidding.id).desc()
    ).limit(limit).all()
    
    return [
        {
            "agency": agency,
            "count": count,
            "total_budget": int(total_budget or 0)
        }
        for agency, count, total_budget in top_agencies
    ]

@router.get("/statistics/by-type")
def get_statistics_by_type(db: Session = Depends(get_db)):
    """유형별 통계"""
    logger.info("📊 유형별 통계 조회")
    
    stats = db.query(
        Bidding.notice_type,
        func.count(Bidding.id).label('count'),
        func.sum(Bidding.budget_amount).label('total_budget'),
        func.avg(Bidding.budget_amount).label('avg_budget')
    ).filter(
        Bidding.notice_type.isnot(None)
    ).group_by(
        Bidding.notice_type
    ).all()
    
    return [
        {
            "type": notice_type,
            "count": count,
            "total_budget": int(total_budget or 0),
            "avg_budget": int(avg_budget or 0)
        }
        for notice_type, count, total_budget, avg_budget in stats
    ]
