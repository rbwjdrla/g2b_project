"""
환경 설정 관리
.env 파일에서 환경변수를 로드하고 애플리케이션 설정을 관리합니다.
"""

from pydantic_settings import BaseSettings
from typing import Optional, Literal
from pydantic import Field


class Settings(BaseSettings):
    """
    애플리케이션 설정 클래스
    
    .env 파일에서 자동으로 값을 읽어옵니다.
    예: .env에 DB_HOST=localhost 라고 쓰면
        settings.DB_HOST 로 접근 가능
    """
    
    # ===== 데이터베이스 설정 =====
    DB_HOST: str          # RDS 엔드포인트 주소
    DB_PORT: int = 5432   # PostgreSQL 기본 포트
    DB_USER: str          # DB 사용자명
    DB_PASSWORD: str      # DB 비밀번호
    DB_NAME: str          # 데이터베이스 이름
    
    db_sslmode: Literal["disable","allow","prefer","require","verify-ca","verify-full"] = Field( "require", alias="DB_SSLMODE" )
    # ===== API 서버 설정 =====
    API_PORT: int = 8000        # FastAPI 서버 포트
    API_HOST: str = "0.0.0.0"   # 모든 IP에서 접근 허용
    
    # ===== 크롤링 설정 =====
    CRAWL_DELAY: int = 10   # 요청 간 대기 시간 (초) - 서버 부담 줄이기
    MAX_PAGES: int = 10    # 최대 크롤링 페이지 수
    
    # ===== 로그 설정 =====
    LOG_LEVEL: str = "INFO"  # 로그 레벨: DEBUG, INFO, WARNING, ERROR
    
    # ===== 환경 설정 =====
    ENVIRONMENT: str = "production"  # development, production
    
    class Config:
        """Pydantic 설정"""
        env_file = ".env"              # .env 파일에서 읽기
        env_file_encoding = "utf-8"    # 한글 지원
    
    @property
    def database_url(self) -> str:
        """
        PostgreSQL 연결 URL 생성
        
        형식: postgresql://user:password@host:port/dbname
        
        Returns:
            str: 데이터베이스 연결 문자열
        """
        return (
            f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
            f"?sslmode={self.db_sslmode}"
)



# ===== 전역 설정 인스턴스 =====
# 다른 파일에서 from config import settings 로 사용
settings = Settings()


# ===== 사용 예시 =====
# from config import settings
# print(settings.DB_HOST)        # RDS 주소 출력
# print(settings.database_url)   # 전체 연결 URL 출력
