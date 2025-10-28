"""
나라장터 입찰공고 크롤러
웹 스크래핑을 통해 입찰 공고 데이터를 수집하고 DB에 저장
"""

import requests
from bs4 import BeautifulSoup
import time
from datetime import datetime
from typing import List, Dict, Optional
import logging

from config import settings
from database import SessionLocal
from models import Bidding


# ===== 로깅 설정 =====
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)
# 로그 예시: 2025-01-23 10:30:45 - INFO - 크롤링 시작


class NaramarketCrawler:
    """
    나라장터 크롤러 클래스
    
    기능:
    - 입찰공고 목록 크롤링
    - 상세 정보 추출
    - DB 저장
    """
    
    def __init__(self):
        """크롤러 초기화"""
        self.base_url = "http://www.g2b.go.kr:8101/ep/tbid/tbidList.do"
        self.session = requests.Session()  # 세션 재사용 (속도 향상)
        
        # User-Agent 설정 (봇 차단 방지)
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        logger.info("✅ 나라장터 크롤러 초기화 완료")
    
    
    def get_bidding_list(self, page: int = 1) -> Optional[BeautifulSoup]:
        """
        입찰공고 목록 페이지 가져오기
        
        Args:
            page: 페이지 번호
            
        Returns:
            BeautifulSoup: 파싱된 HTML 또는 None (실패 시)
        """
        params = {
            'area': '00',              # 전체 지역
            'searchType': '1',          # 검색 유형
            'bidNm': '',                # 검색어 (없음 = 전체)
            'currentPageNo': page       # 페이지 번호
        }
        
        try:
            logger.info(f"📄 {page}페이지 요청 중...")
            
            response = self.session.get(
                self.base_url,
                params=params,
                headers=self.headers,
                timeout=10  # 10초 안에 응답 없으면 타임아웃
            )
            
            # 응답 상태 확인
            response.raise_for_status()  # 4xx, 5xx 에러 시 예외 발생
            
            # 인코딩 설정 (한글 깨짐 방지)
            response.encoding = 'utf-8'
            
            # HTML 파싱
            soup = BeautifulSoup(response.text, 'html.parser')
            
            logger.info(f"✅ {page}페이지 가져오기 성공")
            return soup
            
        except requests.exceptions.Timeout:
            logger.error(f"❌ {page}페이지 타임아웃")
            return None
            
        except requests.exceptions.RequestException as e:
            logger.error(f"❌ {page}페이지 요청 실패: {e}")
            return None
    
    
    def parse_bidding_item(self, item) -> Optional[Dict]:
        """
        입찰공고 항목 파싱 (나라장터 실제 HTML 구조 반영)
        
        Args:
            item: BeautifulSoup 태그 객체 (공고 1개 <tr> 태그)
            
        Returns:
            dict: 파싱된 데이터 또는 None
        """
        try:
            data = {}
            
            # 모든 td 태그 가져오기
            tds = item.find_all('td', class_='w2group_w2tb_td')
            
            if len(tds) < 5:
                logger.warning("⚠️ td 태그 부족 - 건너뜀")
                return None
            
            # data-title 속성으로 필드 식별
            for td in tds:
                title = td.get('data-title', '')
                text = td.text.strip()
                
                # 공고종류
                if '공고종류' in title:
                    data['contract_method'] = text
                
                # 입찰방식
                elif '입찰방식' in title:
                    data['bidding_method'] = text
                
                # 입찰방법
                elif '입찰방법' in title:
                    pass  # 필요시 추가
            
            # 공고번호 추출 (label 태그 없는 td에서)
            notice_td = None
            for td in item.find_all('td'):
                if 'data-title' not in td.attrs and td.text.strip().startswith('R'):
                    notice_td = td
                    break
            
            if notice_td:
                data['notice_number'] = notice_td.text.strip()
            else:
                logger.warning("⚠️ 공고번호 없음 - 건너뜀")
                return None
            
            # 공고명 추출 (label 태그 안에)
            title_label = item.find('label')
            if title_label:
                data['title'] = title_label.text.strip()
            else:
                logger.warning("⚠️ 공고명 없음 - 건너뜀")
                return None
            
            # 발주기관 / 수요기관 추출
            # 실제 구조에서 정확한 위치 확인 필요 (임시로 None)
            data['ordering_agency'] = None
            data['demanding_agency'] = None
            
            # 예산금액 / 추정가격 (실제 필드명 확인 필요)
            data['budget_amount'] = None
            data['estimated_price'] = None
            
            # 공고일시 / 입찰마감일시
            # 날짜 형식: "2025/10/23 (2025/10/..." 같은 패턴
            date_pattern = r'(\d{4}/\d{2}/\d{2})'
            for td in tds:
                text = td.text.strip()
                if '/' in text and len(text) > 8:
                    import re
                    match = re.search(date_pattern, text)
                    if match:
                        try:
                            date_str = match.group(1)
                            parsed_date = datetime.strptime(date_str, '%Y/%m/%d')
                            
                            # 첫 번째 날짜 = 공고일시
                            if data.get('notice_date') is None:
                                data['notice_date'] = parsed_date
                            # 두 번째 날짜 = 입찰마감일시
                            elif data.get('bid_close_date') is None:
                                data['bid_close_date'] = parsed_date
                        except ValueError:
                            pass
            
            # URL 생성 (상세 페이지 링크)
            # 실제 링크 구조 확인 필요
            data['bidding_url'] = None
            link_tag = item.find('a')
            if link_tag and link_tag.get('href'):
                href = link_tag['href']
                if href.startswith('http'):
                    data['bidding_url'] = href
                else:
                    data['bidding_url'] = f"http://www.g2b.go.kr{href}"
            
            # 필수 필드 검증
            if not data.get('notice_number') or not data.get('title'):
                logger.warning("⚠️ 필수 필드 누락 - 건너뜀")
                return None
            
            return data
            
        except Exception as e:
            logger.error(f"❌ 파싱 실패: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    
    def save_to_db(self, data: Dict) -> bool:
        """
        데이터를 DB에 저장
        
        Args:
            data: 입찰공고 데이터
            
        Returns:
            bool: 저장 성공 여부
        """
        db = SessionLocal()
        
        try:
            # 중복 확인 (같은 공고번호가 이미 있는지)
            existing = db.query(Bidding).filter(
                Bidding.notice_number == data['notice_number']
            ).first()
            
            if existing:
                logger.info(f"⏭️ 중복 공고 건너뜀: {data['notice_number']}")
                return False
            
            # 새 공고 객체 생성
            bidding = Bidding(
                notice_number=data.get('notice_number'),
                title=data.get('title'),
                ordering_agency=data.get('ordering_agency'),
                budget_amount=data.get('budget_amount'),
                notice_date=data.get('notice_date'),
                bidding_url=data.get('bidding_url')
            )
            
            # DB에 추가
            db.add(bidding)
            db.commit()
            
            logger.info(f"✅ 저장 완료: {data['notice_number']} - {data['title'][:30]}")
            return True
            
        except Exception as e:
            db.rollback()  # 에러 발생 시 롤백
            logger.error(f"❌ DB 저장 실패: {e}")
            return False
            
        finally:
            db.close()
    
    
    def crawl(self, max_pages: int = None) -> Dict[str, int]:
        """
        크롤링 실행 (메인 함수)
        
        Args:
            max_pages: 최대 크롤링 페이지 수 (None이면 설정값 사용)
            
        Returns:
            dict: 크롤링 결과 통계
        """
        if max_pages is None:
            max_pages = settings.MAX_PAGES
        
        logger.info(f"🚀 크롤링 시작 - 최대 {max_pages}페이지")
        
        stats = {
            'total_items': 0,    # 전체 항목 수
            'saved_items': 0,     # 저장 성공
            'skipped_items': 0,   # 중복으로 건너뜀
            'failed_items': 0     # 실패
        }
        
        for page in range(1, max_pages + 1):
            # 페이지 가져오기
            soup = self.get_bidding_list(page)
            
            if soup is None:
                logger.warning(f"⚠️ {page}페이지 건너뜀")
                continue
            
            # 공고 목록 찾기
            # 실제 HTML: <tr id="mf_wfm_container_..." class="w2group_up">
            items = soup.find_all('tr', class_='w2group_up')
            
            # 또는 tbody 내의 모든 tr 찾기 (id가 mf_wfm으로 시작하는 것만)
            if not items:
                tbody = soup.find('tbody')
                if tbody:
                    items = [tr for tr in tbody.find_all('tr') 
                            if tr.get('id', '').startswith('mf_wfm')]
            
            if not items:
                logger.warning(f"⚠️ {page}페이지에 공고 없음")
                break
            
            logger.info(f"📋 {page}페이지: {len(items)}개 공고 발견")
            
            # 각 공고 처리
            for item in items:
                stats['total_items'] += 1
                
                # 파싱
                data = self.parse_bidding_item(item)
                
                if data is None:
                    stats['failed_items'] += 1
                    continue
                
                # 저장
                saved = self.save_to_db(data)
                
                if saved:
                    stats['saved_items'] += 1
                else:
                    stats['skipped_items'] += 1
            
            # 서버 부담 줄이기 (요청 간 대기)
            time.sleep(settings.CRAWL_DELAY)
        
        logger.info(f"""
🎉 크롤링 완료!
📊 결과:
   - 전체: {stats['total_items']}개
   - 저장: {stats['saved_items']}개
   - 중복: {stats['skipped_items']}개
   - 실패: {stats['failed_items']}개
        """)
        
        return stats


# ===== 실행 코드 =====
if __name__ == "__main__":
    """
    이 파일을 직접 실행했을 때만 동작
    
    실행 방법:
    python crawler.py
    """
    
    # 크롤러 생성
    crawler = NaramarketCrawler()
    
    # 크롤링 실행
    results = crawler.crawl()
    
    print(f"\n✅ 크롤링 완료: {results['saved_items']}개 저장됨")


"""
💡 크롤링 동작 흐름:

1. NaramarketCrawler 객체 생성
   ↓
2. crawl() 메서드 호출
   ↓
3. 페이지 1~10 반복:
   - get_bidding_list(page) → HTML 가져오기
   - 공고 목록 찾기
   - 각 공고마다:
     * parse_bidding_item() → 데이터 추출
     * save_to_db() → DB 저장
   - time.sleep() → 대기
   ↓
4. 통계 출력
"""


"""
💡 에러 처리:

1. 타임아웃 → 해당 페이지 건너뜀
2. 파싱 실패 → 해당 공고 건너뜀
3. 중복 → 저장 안하고 건너뜀
4. DB 저장 실패 → rollback 후 건너뜀

→ 일부 실패해도 계속 진행!
"""


"""
💡 실제 사용 시 주의사항:

이 코드는 "템플릿"입니다!
나라장터의 실제 HTML 구조를 확인하고:

1. CSS 선택자 수정:
   item.find('td', class_='number')
   → 실제 클래스명으로 변경

2. 필드 추가:
   - demanding_agency (수요기관)
   - contract_method (계약방법)
   - bidding_method (입찰방법)
   등 추가

3. 날짜 형식 확인:
   '%Y-%m-%d %H:%M'
   → 실제 형식에 맞게 수정
"""
