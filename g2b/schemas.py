from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# ==================== 입찰공고 ====================
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
    notice_type: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class BiddingListResponse(BaseModel):
    total: int
    items: list[BiddingResponse]
    skip: int
    limit: int

# ==================== 낙찰정보 ====================
class AwardResponse(BaseModel):
    id: int
    bid_ntce_no: str
    notice_type: Optional[str] = None
    award_company_name: Optional[str] = None
    award_business_no: Optional[str] = None
    award_ceo_name: Optional[str] = None
    award_amount: Optional[int] = None
    award_rate: Optional[float] = None
    opening_date: Optional[datetime] = None
    ntce_instt_cd: Optional[str] = None
    dminstt_cd: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class AwardListResponse(BaseModel):
    total: int
    items: list[AwardResponse]
    skip: int
    limit: int

# ==================== 발주계획 ====================
class OrderPlanResponse(BaseModel):
    id: int
    announce_number: str
    demand_org_name: Optional[str] = None
    public_org_name: Optional[str] = None
    business_name: Optional[str] = None
    total_predict_price: Optional[int] = None
    announce_date: Optional[datetime] = None
    reference_date: Optional[datetime] = None
    demand_class_name: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class OrderPlanListResponse(BaseModel):
    total: int
    items: list[OrderPlanResponse]
    skip: int
    limit: int
