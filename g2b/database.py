from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import settings

# 엔진 생성
engine = create_engine(
    settings.database_url,
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=10
)

# 세션 팩토리
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# 베이스 클래스
Base = declarative_base()

# 세션 제공 함수
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 초기화 함수
def init_db():
    from models import Bidding
    Base.metadata.create_all(bind=engine)
    print("✅ 데이터베이스 테이블 생성 완료")