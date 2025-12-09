# G2B Project – 정부 입찰 정보 수집·분석 플랫폼

**G2B Project**는 조달청(G2B) 공개 API를 활용해  
**입찰 공고·발주 계획·낙찰(계약) 정보를 자동 수집**하고, 이를 **REST API와 React 대시보드**로 제공하는 프로젝트입니다.  

데이터 수집 → 저장 → 통계/ML 분석 → 시각화까지 하나의 흐름으로 구현한 풀스택 사이드 프로젝트입니다.

---

## ✨ 주요 기능

- **입찰/발주/낙찰 정보 자동 수집**
  - 공공데이터포털 G2B Open API 연동
  - APScheduler로 **매일 새벽 자동 크롤링**
  - 필요 시 API로 수동 수집 트리거 가능

- **REST API (FastAPI 기반)**
  - 입찰공고 / 낙찰 / 발주계획 / 통계 / ML 분석용 엔드포인트 제공
  - 검색어, 공고 유형, 예산 범위, 카테고리 등 다양한 필터 지원

- **머신러닝 기반 분석**
  - 공고 제목 기반 **카테고리 분류** (건설, 용역, 물품, IT 등)
  - 예산·마감일 정보를 이용한 **자동 태그 생성**
    

- **웹 대시보드 (React)**
  - 기간/예산/유형/카테고리/검색어 필터
  - 입찰·낙찰·발주계획 탭별 리스트 & 상세 모달
  - 최근 30일 입찰 건수 추이, 유형별 분포 등 차트 시각화

---

## 🛠 기술 스택

| 영역        | 기술 |
|------------|------|
| Backend    | Python, FastAPI, SQLAlchemy, APScheduler |
| Database   | PostgreSQL |
| ML         | scikit-learn, pandas, NumPy |
| Frontend   | React, React Router, Material UI, Chart.js, dayjs |
| Infra/기타 | Docker, Uvicorn, Pydantic, .env 환경 설정 |

---

## 📁 프로젝트 구조

```bash
g2b_project/
├── g2b/                         # FastAPI Backend
│   ├── app.py                   # FastAPI 앱 엔트리 포인트
│   ├── database.py              # PostgreSQL 연결 및 세션 관리
│   ├── models.py                # SQLAlchemy ORM 모델 정의
│   ├── schemas.py               # Pydantic 스키마
│   ├── config.py                # 환경 변수 및 설정
│   ├── scheduler.py             # APScheduler 스케줄링(자동 수집/분석)
│   ├── ml_analyzer.py           # 머신러닝 분석 로직
│   ├── apis/                    # G2B Open API 연동 모듈
│   │   ├── bidding_api.py
│   │   ├── award_api.py
│   │   ├── orderplan_api.py
│   │   └── main.py              # 전체 수집 orchestration
│   ├── routers/                 # 도메인별 API 라우터
│   │   ├── biddings.py          # 입찰공고 API
│   │   ├── awards.py            # 낙찰/계약 API
│   │   ├── orderplans.py        # 발주계획 API
│   │   ├── statistics.py        # 통계 API
│   │   └── ml.py                # ML 분석 API
│   └── utils.py                 # 공통 유틸 함수
│
├── g2b_frontend/                # React Frontend
│   └── src/
│       ├── pages/               # Dashboard 페이지
│       ├── components/          # 필터/테이블/차트/모달 등 UI 컴포넌트
│       └── services/            # Backend API 호출 래퍼
│
├── requirements.txt             # Python 의존성 목록
├── Dockerfile                   # Backend 컨테이너 설정
└── README.md
