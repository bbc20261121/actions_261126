import os
import time
from playwright.sync_api import sync_playwright

def wake_up_streamlit():
    url = os.environ.get("APP_URL")
    if not url:
        raise ValueError("APP_URL 환경 변수가 설정되지 않았습니다.")

    with sync_playwright() as p:
        # 백그라운드에서 크롬 브라우저 실행
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        print(f"접속 시도: {url}")
        page.goto(url, wait_until="networkidle")
        
        # 앱이 절전(Sleep) 상태일 경우 깨우기 버튼 확인 및 클릭
        try:
            wake_button = page.get_by_role("button", name="Yes, get this app back up!")
            if wake_button.is_visible(timeout=5000):
                print("절전 모드 감지됨. 앱 깨우기 버튼 클릭 중...")
                wake_button.click()
                # 앱이 다시 부팅될 때까지 충분히 대기
                time.sleep(20)
                print("앱 깨우기 완료!")
            else:
                print("앱이 이미 정상 실행 중입니다.")
        except Exception as e:
            print("절전 버튼이 없거나 이미 활성 상태입니다.")
            
        # Streamlit 내부 요소가 렌더링될 시간을 확보
        time.sleep(10)
        browser.close()
        print("작업 종료")

if __name__ == "__main__":
    wake_up_streamlit()
