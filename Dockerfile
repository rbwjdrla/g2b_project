# Python 3.12 버전의 경량 이미지를 베이스로 사용
FROM python:3.12-slim

# 환경 변수 설정 (Python 버퍼링 방지: 디버깅 및 로깅에 필수)
ENV PYTHONUNBUFFERED=1

# 필요한 리눅스 시스템 패키지 설치
# PostgreSQL 연결을 위한 libpq-dev와 빌드 도구만 설치
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# 작업 디렉터리 설정
WORKDIR /app

# Python 의존성 설치 (pip 업그레이드 및 캐시 사용 안함)
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# 프로젝트 코드 복사 (API 코드, 크롤러 코드 등)
COPY . .

# 포트 노출 (API 서버 포트)
EXPOSE 8000

# 실행 명령어 (FastAPI 서버 구동)
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]