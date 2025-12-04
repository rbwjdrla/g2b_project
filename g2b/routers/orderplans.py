from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
from database import get_db
from models import OrderPlan  # 모델명은 유지
from schemas import OrderPlanResponse, OrderPlanListResponse
import logging

router = APIRouter(prefix="/api", tags=["발주계획"])
logger = logging.getLogger(__name__)

@router.get("/orderplans", response_model=OrderPlanListResponse)  # URL 변경
def get_orderplans(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    search: Optional[str] = Query(None),
    db: Session = Depends(get_db),
):
    """발주계획 목록 조회"""
    logger.info(f"📋 발주계획 목록 조회 (skip={skip}, limit={limit})")
    
    query = db.query(OrderPlan)
    
    if search:
        query = query.filter(OrderPlan.business_name.contains(search))
    
    query = query.order_by(OrderPlan.announce_date.desc())
    
    total = query.count()
    items = query.offset(skip).limit(limit).all()
    
    return {
        "total": total,
        "items": items,
        "skip": skip,
        "limit": limit
    }

@router.get("/orderplans/{plan_id}", response_model=OrderPlanResponse)  # URL 변경
def get_orderplan(plan_id: int, db: Session = Depends(get_db)):
    """발주계획 상세 조회"""
    logger.info(f"📋 발주계획 상세 조회 (id={plan_id})")
    
    plan = db.query(OrderPlan).filter(OrderPlan.id == plan_id).first()
    if not plan:
        raise HTTPException(status_code=404, detail="발주계획을 찾을 수 없습니다.")
    return plan