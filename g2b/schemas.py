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
    # ML 분석 필드
    ai_category: Optional[str] = None
    ai_tags: Optional[str] = None
    competition_level: Optional[str] = None
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
    order_plan_unty_no: str
    biz_nm: Optional[str] = None
    order_instt_nm: Optional[str] = None
    dept_nm: Optional[str] = None
    ofcl_nm: Optional[str] = None
    tel_no: Optional[str] = None
    prcrmnt_methd: Optional[str] = None
    cntrct_mthd_nm: Optional[str] = None
    sum_order_amt: Optional[int] = None
    sum_order_dol_amt: Optional[str] = None
    qty_cntnts: Optional[str] = None
    unit: Optional[str] = None
    prdct_clsfc_no: Optional[str] = None
    dtil_prdct_clsfc_no: Optional[str] = None
    prdct_clsfc_no_nm: Optional[str] = None
    dtil_prdct_clsfc_no_nm: Optional[str] = None
    usg_cntnts: Optional[str] = None
    spec_cntnts: Optional[str] = None
    rmrk_cntnts: Optional[str] = None
    order_year: Optional[str] = None
    order_mnth: Optional[str] = None
    ntice_dt: Optional[datetime] = None
    chg_dt: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
        
class OrderPlanListResponse(BaseModel):
    total: int
    items: list[OrderPlanResponse]
    skip: int
    limit: int