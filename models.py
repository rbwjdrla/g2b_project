"""
데이터베이스 테이블 모델 정의
나라장터 입찰공고 데이터를 저장할 테이블 구조
"""

from sqlalchemy import Column, Integer, String, BigInteger, DateTime, Text
from sqlalchemy.sql import func
from database import Base  # 2단계에서 만든 Base 사용!


class Bidding(Base):
    """
    입찰공고 테이블
    
    나라장터에서 크롤링한 입찰 공고 정보를 저장합니다.
    """
    
    # ===== 테이블 이름 =====
    __tablename__ = "biddings"
    # → CREATE TABLE biddings (...)
    
    
    # ===== 기본 정보 =====
    id = Column(
        Integer,           # 데이터 타입: 정수
        primary_key=True,  # 기본키 (Primary Key) - 각 행을 구분하는 고유 번호
        index=True,        # 인덱스 생성 (검색 속도 향상)
        comment="고유 ID (자동 증가)"
    )
    # → id INTEGER PRIMARY KEY
    
    
    # ===== 공고 정보 =====
    notice_number = Column(
        String(50),        # 최대 50자 문자열
        unique=True,       # 중복 불가 (같은 공고번호는 한 번만 저장)
        nullable=False,    # NULL 불가 (반드시 값 있어야 함)
        index=True,        # 검색 자주 하므로 인덱스
        comment="공고번호"
    )
    # → notice_number VARCHAR(50) UNIQUE NOT NULL
    
    title = Column(
        String(500),       # 공고명은 길 수 있으므로 500자
        nullable=False,
        comment="공고명"
    )
    
    
    # ===== 발주/수요 기관 =====
    ordering_agency = Column(
        String(200),
        nullable=True,     # NULL 허용 (없을 수도 있음)
        comment="발주기관"
    )
    
    demanding_agency = Column(
        String(200),
        nullable=True,
        comment="수요기관"
    )
    
    
    # ===== 입찰 방식 =====
    contract_method = Column(
        String(100),
        nullable=True,
        comment="계약방법 (예: 일반경쟁입찰)"
    )
    
    bidding_method = Column(
        String(100),
        nullable=True,
        comment="입찰방법 (예: 전자입찰)"
    )
    
    
    # ===== 금액 정보 =====
    budget_amount = Column(
        BigInteger,        # 큰 숫자 (최대 약 9경)
        nullable=True,
        comment="예산금액 (원 단위)"
    )
    # BigInteger를 쓰는 이유: Integer는 약 21억까지만 저장 가능
    # 입찰 금액은 수십억~조 단위도 가능
    
    estimated_price = Column(
        BigInteger,
        nullable=True,
        comment="추정가격 (원 단위)"
    )
    
    
    # ===== 일시 정보 =====
    notice_date = Column(
        DateTime,          # 날짜+시간
        nullable=True,
        comment="공고일시"
    )
    
    bid_close_date = Column(
        DateTime,
        nullable=True,
        comment="입찰마감일시"
    )
    
    
    # ===== 상세 정보 =====
    description = Column(
        Text,              # 긴 텍스트 (제한 없음)
        nullable=True,
        comment="공고 상세 내용"
    )
    
    bidding_url = Column(
        String(500),
        nullable=True,
        comment="나라장터 상세 페이지 URL"
    )
    
    
    # ===== 메타 정보 (시스템이 자동 기록) =====
    created_at = Column(
        DateTime,
        default=func.now(),           # 생성 시 현재 시간 자동 입력
        nullable=False,
        comment="데이터 생성 시간"
    )
    # func.now() = SQL의 NOW() 함수 (현재 시간)
    
    updated_at = Column(
        DateTime,
        default=func.now(),           # 생성 시 현재 시간
        onupdate=func.now(),          # 수정 시 현재 시간으로 자동 업데이트
        nullable=False,
        comment="데이터 수정 시간"
    )
    
    
    def __repr__(self):
        """
        객체를 문자열로 표현 (디버깅용)
        
        예: print(bidding) 했을 때 보기 좋게 출력
        """
        return f"<Bidding(id={self.id}, notice_number={self.notice_number}, title={self.title[:20]}...)>"


