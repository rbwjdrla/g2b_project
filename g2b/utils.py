import requests
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


def fetch_data(url, params):
    r = None  # ✅ 먼저 정의!
    
    try:
        r = requests.get(url, params=params, timeout=15)
        
        # 응답 내용 먼저 확인
        logging.info(f"🌐 URL: {url}")
        logging.info(f"📊 Status Code: {r.status_code}")
        logging.info(f"🔗 Full URL: {r.url}")
        
        # 에러 응답도 JSON으로 파싱 시도
        if r.status_code != 200:
            logging.error(f"❌ HTTP Error {r.status_code}")
            logging.error(f"응답 내용: {r.text[:500]}")  # 처음 500자만
            
            # JSON 응답이면 파싱해서 에러 메시지 확인
            try:
                error_data = r.json()
                logging.error(f"JSON 응답: {error_data}")
                
                # 조달청 API는 에러도 JSON으로 반환할 수 있음
                if "response" in error_data and "header" in error_data["response"]:
                    header = error_data["response"]["header"]
                    logging.error(f"resultCode: {header.get('resultCode')}")
                    logging.error(f"resultMsg: {header.get('resultMsg')}")
            except:
                pass
        
        r.raise_for_status()
        return r.json()
        
    except requests.exceptions.RequestException as e:
        logging.error(f"❌ API 요청 실패: {url} ({e})")
        
        # ✅ r이 None이 아닐 때만 text 접근
        if r is not None:
            logging.error(f"resp.text: {r.text[:500]}")
        
        return None
        
    except Exception as e:
        logging.error(f"❌ 예상치 못한 에러: {e}")
        return None