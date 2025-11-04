"""
데이터베이스 테이블 모델 정의
나라장터 입찰공고 및 발주계획 데이터를 저장할 테이블 구조
"""

from sqlalchemy import Column, Integer, String, BigInteger, DateTime, Text
from sqlalchemy.sql import func
from database import Base


# ============================================================
# 1️⃣ 입찰공고 테이블
# ============================================================
class Bidding(Base):
    __tablename__ = "biddings"

    id = Column(Integer, primary_key=True, index=True)

    notice_number = Column(String(50), unique=True, nullable=False, index=True, comment="공고번호")
    title = Column(String(500), nullable=False, comment="공고명")

    ordering_agency = Column(String(200), nullable=True, comment="발주기관")
    demanding_agency = Column(String(200), nullable=True, comment="수요기관")

    contract_method = Column(String(100), nullable=True, comment="계약방법")
    bidding_method = Column(String(100), nullable=True, comment="입찰방법")

    budget_amount = Column(BigInteger, nullable=True, comment="예산금액(원)")
    estimated_price = Column(BigInteger, nullable=True, comment="추정가격(원)")

    notice_date = Column(DateTime, nullable=True, comment="공고일시")
    bid_close_date = Column(DateTime, nullable=True, comment="입찰마감일시")

    description = Column(Text, nullable=True, comment="공고 상세 내용")
    bidding_url = Column(String(500), nullable=True, comment="나라장터 상세 페이지 URL")

    created_at = Column(DateTime, default=func.now(), nullable=False, comment="데이터 생성 시간")
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False, comment="데이터 수정 시간")

    def __repr__(self):
        return f"<Bidding(id={self.id}, notice_number={self.notice_number}, title={self.title[:20]}...)>"


# ============================================================
# 2️⃣ 발주계획 테이블
# ============================================================
class OrderPlan(Base):
    __tablename__ = "order_plans"

    id = Column(Integer, primary_key=True, index=True)
    order_plan_unty_no = Column(String(50), unique=True, index=True, nullable=False, comment="발주계획 통합번호")

    biz_nm = Column(String(500), nullable=True, comment="사업명")
    order_instt_nm = Column(String(200), nullable=True, comment="발주기관명")
    dept_nm = Column(String(200), nullable=True, comment="부서명")
    ofcl_nm = Column(String(100), nullable=True, comment="담당자")
    tel_no = Column(String(50), nullable=True, comment="전화번호")

    prcrmnt_methd = Column(String(100), nullable=True, comment="조달방식")
    cntrct_mthd_nm = Column(String(100), nullable=True, comment="계약방법")

    sum_order_amt = Column(BigInteger, nullable=True, comment="발주금액(원)")
    sum_order_dol_amt = Column(String(50), nullable=True, comment="발주금액(달러표기 원문)")
    qty_cntnts = Column(String(50), nullable=True, comment="수량")
    unit = Column(String(50), nullable=True, comment="단위")

    prdct_clsfc_no = Column(String(50), nullable=True, comment="품목분류번호")
    dtil_prdct_clsfc_no = Column(String(50), nullable=True, comment="세부품목번호")
    prdct_clsfc_no_nm = Column(String(200), nullable=True, comment="품목명")
    dtil_prdct_clsfc_no_nm = Column(String(200), nullable=True, comment="세부품목명")

    usg_cntnts = Column(Text, nullable=True, comment="용도")
    spec_cntnts = Column(Text, nullable=True, comment="규격 내용")
    rmrk_cntnts = Column(Text, nullable=True, comment="비고")

    order_year = Column(String(4), nullable=True, comment="발주연도")
    order_mnth = Column(String(2), nullable=True, comment="발주월")
    ntice_dt = Column(DateTime, nullable=True, comment="공고일시(변환)")
    chg_dt = Column(DateTime, nullable=True, comment="변경일시(변환)")

    created_at = Column(DateTime, default=func.now(), nullable=False, comment="데이터 생성 시간")
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False, comment="데이터 수정 시간")

    def __repr__(self):
        return f"<OrderPlan(id={self.id}, biz_nm={self.biz_nm}, order_instt_nm={self.order_instt_nm})>"
