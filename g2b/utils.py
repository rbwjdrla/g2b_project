import requests
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


def fetch_data(url, params):
    r = None
    try:
        r = requests.get(url, params=params, timeout=15)
        
        logging.info(f"🌐 URL: {url}")
        logging.info(f"📊 Status Code: {r.status_code}")
        logging.info(f"🔗 Full URL: {r.url}")
        
        if r.status_code != 200:
            logging.error(f"❌ HTTP Error {r.status_code}")
            logging.error(f"응답 내용: {r.text[:500]}")
            return None
        
        r.raise_for_status()
        data = r.json()
        
        # ✅ ResponseError 체크 추가!
        if "nkoneps.com.response.ResponseError" in data:
            error_info = data["nkoneps.com.response.ResponseError"]
            error_msg = error_info.get("header", {}).get("resultMsg", "알 수 없는 에러")
            logging.error(f"❌ API 에러: {error_msg}")
            return None
        
        return data
        
    except requests.exceptions.Timeout:
        logging.error(f"❌ 타임아웃: {url}")
        return None
    except requests.exceptions.RequestException as e:
        logging.error(f"❌ 요청 실패: {e}")
        if r is not None:
            logging.error(f"resp.text: {r.text[:500]}")
        return None
    except Exception as e:
        logging.error(f"❌ 예상치 못한 에러: {e}")
        return None