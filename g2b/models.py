"""
데이터베이스 테이블 모델 정의
나라장터 입찰공고 / 발주계획 / 계약 / 낙찰 정보를 저장할 테이블 구조
"""

from sqlalchemy import Column, Integer, String, DateTime, Text, BigInteger, Date, Float, UniqueConstraint
from sqlalchemy.sql import func
from database import Base


# ============================================================
# 1️⃣ 입찰공고 테이블
# ============================================================
class Bidding(Base):
    __tablename__ = "biddings"

    id = Column(Integer, primary_key=True, index=True)

    notice_number = Column(String(50), unique=True, nullable=False, index=True, comment="공고번호")
    notice_type = Column(String(50), nullable=True, comment="공고구분 (용역, 물품, 공사 등)") # 추가1
    title = Column(String(500), nullable=False, comment="공고명")

    ordering_agency = Column(String(200), nullable=True, comment="발주기관")
    demanding_agency = Column(String(200), nullable=True, comment="수요기관")

    contract_method = Column(String(100), nullable=True, comment="계약방법")
    bidding_method = Column(String(100), nullable=True, comment="입찰방법")

    budget_amount = Column(BigInteger, nullable=True, comment="예산금액(원)")
    estimated_price = Column(BigInteger, nullable=True, comment="추정가격(원)")

    notice_date = Column(DateTime, nullable=True, comment="공고일시")
    bid_close_date = Column(DateTime, nullable=True, comment="입찰마감일시")

    order_instt_cd = Column(String(50), nullable=True, comment="발주기관코드") # 추가 2
    order_instt_nm = Column(String(200), nullable=True, comment="발주기관명") # 추가 3

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


# ============================================================
# 3️⃣ 계약정보 테이블
# ============================================================
class Contract(Base):
    __tablename__ = "contracts"

    id = Column(Integer, primary_key=True, index=True)
    
    # 기본 정보
    unty_cntrct_no = Column(String(50), nullable=False, index=True, comment="통합계약번호")
    bsns_div_nm = Column(String(50), nullable=True, comment="사업구분명")
    dcsn_cntrct_no = Column(String(50), nullable=True, comment="결정계약번호")
    cntrct_ref_no = Column(String(50), nullable=True, comment="계약참조번호")
    contract_type = Column(String(20), nullable=True, comment="계약구분(물품/용역/공사)")
    
    # 계약 상세
    cntrct_nm = Column(String(500), nullable=True, comment="계약명")
    cmmn_cntrct_yn = Column(String(1), nullable=True, comment="공동계약여부")
    lngtrm_ctnu_div_nm = Column(String(50), nullable=True, comment="장기계속구분명")
    cntrct_cncls_date = Column(Date, nullable=True, comment="계약체결일자")
    cntrct_prd = Column(String(100), nullable=True, comment="계약기간")
    base_law_nm = Column(String(200), nullable=True, comment="근거법령명")
    
    # 금액 정보
    tot_cntrct_amt = Column(BigInteger, nullable=True, comment="총계약금액")
    thtm_cntrct_amt = Column(BigInteger, nullable=True, comment="당해계약금액")
    grntymny_rate = Column(String(20), nullable=True, comment="보증금률")
    pay_div_nm = Column(String(50), nullable=True, comment="지급구분명")
    
    # 참조 정보
    req_no = Column(String(50), nullable=True, comment="요청번호")
    ntce_no = Column(String(50), nullable=True, comment="공고번호")
    
    # 계약기관 정보
    cntrct_instt_cd = Column(String(50), nullable=True, comment="계약기관코드")
    cntrct_instt_nm = Column(String(200), nullable=True, comment="계약기관명")
    cntrct_instt_jrsdctn_div_nm = Column(String(100), nullable=True, comment="계약기관관할구분명")
    cntrct_instt_chrg_dept_nm = Column(String(200), nullable=True, comment="계약기관담당부서명")
    cntrct_instt_ofcl_nm = Column(String(100), nullable=True, comment="계약기관담당자명")
    cntrct_instt_ofcl_tel_no = Column(String(50), nullable=True, comment="계약기관담당자전화번호")
    cntrct_instt_ofcl_fax_no = Column(String(50), nullable=True, comment="계약기관담당자팩스번호")
    
    # 리스트 정보 (JSON 문자열로 저장)
    dminstt_list = Column(Text, nullable=True, comment="수요기관리스트")
    corp_list = Column(Text, nullable=True, comment="업체리스트")
    
    # URL
    cntrct_info_url = Column(String(500), nullable=True, comment="계약정보URL")
    cntrct_dtl_info_url = Column(Text, nullable=True, comment="계약상세정보URL")
    
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)
    
    # 복합 유니크 제약
    __table_args__ = (
        UniqueConstraint('unty_cntrct_no', 'contract_type', name='uix_contract_unty'),
    )

    def __repr__(self):
        return f"<Contract(id={self.id}, unty_cntrct_no={self.unty_cntrct_no}, cntrct_nm={self.cntrct_nm})>"
# ============================================================
# 4️⃣ 낙찰정보 테이블
# ============================================================
class Award(Base):
    __tablename__ = "awards"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # 기본 정보
    bid_ntce_no = Column(String(50), nullable=False, index=True)  # 입찰공고번호
    bid_ntce_ord = Column(String(10))                             # 입찰공고차수
    bid_clsfc_no = Column(String(10))                             # 입찰분류번호
    rbid_no = Column(String(10))                                  # 재입찰번호
    notice_type = Column(String(20))                              # 물품/공사/용역
    
    # 공고 정보
    bid_ntce_nm = Column(String(500))                             # 입찰공고명
    openg_dt = Column(DateTime)                                   # 개찰일시
    
    # 낙찰 정보
    prtcpt_cnum = Column(Integer)                                 # 참가업체수
    openg_corp_info = Column(Text)                                # 원본 개찰업체정보
    progrs_div_cd_nm = Column(String(50))                         # 진행상태
    
    # 파싱된 낙찰 정보
    award_company_name = Column(String(200))                      # 낙찰업체명
    award_business_no = Column(String(50))                        # 사업자번호
    award_ceo_name = Column(String(100))                          # 대표자명
    award_amount = Column(BigInteger)                             # 낙찰금액
    award_rate = Column(Float)                                    # 낙찰률
    
    # 기관 정보
    ntce_instt_cd = Column(String(50))                            # 공고기관코드
    ntce_instt_nm = Column(String(200))                           # 공고기관명
    dminstt_cd = Column(String(50))                               # 수요기관코드
    dminstt_nm = Column(String(200))                              # 수요기관명
    
    # 메타 정보
    inpt_dt = Column(DateTime)                                    # 입력일시
    rsrvtn_prce_file_existnce_yn = Column(String(1))             # 예정가격파일존재여부
    openg_rslt_ntc_cntnts = Column(Text)                         # 개찰결과공고내용
    
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # 복합 유니크 제약
    __table_args__ = (
        UniqueConstraint('bid_ntce_no', 'bid_ntce_ord', 'notice_type', name='uix_award_notice'),
    )