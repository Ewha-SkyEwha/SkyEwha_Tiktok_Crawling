from playwright.sync_api import sync_playwright
import re
import time
from TikTok_Crawler import save_cookies
import requests

COOKIES_FILE = "tiktok_cookies.json"
HASHTAG_URL = "https://ads.tiktok.com/business/creativecenter/inspiration/popular/hashtag/pc/en"

# 로컬
# API_URL = "http://localhost:8000/api/v1/hashtag/hashtags/"

# 서버
# API_URL = "https://skyewha-trendie.kr/api/v1/hashtag/hashtags/"

def scrape_travel_hashtags_fixed():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        ctx = browser.new_context(storage_state=COOKIES_FILE)
        page = ctx.new_page()
        #page.goto(HASHTAG_URL, wait_until="networkidle")
        page.goto(HASHTAG_URL, wait_until="domcontentloaded", timeout=60000)
        time.sleep(1)

        #1. Industry 드롭다운 찾기
        btn = page.query_selector("button:has-text('Industry')") \
            or page.query_selector("span:has-text('Industry')")
        if btn:
            btn.click()
            time.sleep(2)

        # 2. 'Travel' 탭/필터 클릭
        print("➡️ 'Travel' 탭 클릭 시도...")

        # ✅ 정확한 data-testid를 사용하여 'Travel' 탭 선택
        travel_tab_selector = '[data-testid="cc_single_select_undefined_item_16"]'
        travel_tab = page.locator(travel_tab_selector)

        try:
            # 요소가 표시될 때까지 충분히 대기합니다.
            travel_tab.wait_for(state="visible", timeout=10000)

            # 클릭합니다. 이 요소는 필터이므로 페이지 이동(URL 변경)이 없어야 합니다.
            travel_tab.click()

            # 탭 전환 후 데이터 로딩을 위해 충분히 대기합니다.
            time.sleep(4)
            print("✅ 'Travel' 탭 클릭 성공. 데이터 로딩 대기 중...")

        except Exception as e:
            # 예외가 발생하면 실패를 보고하고 종료합니다.
            print(f"❌ 'Travel' 탭 클릭 실패 또는 요소를 찾지 못함: {e}")
            browser.close()
            return []

        # 3. 스크롤 내리며 크롤링
        for _ in range(20):
            page.mouse.wheel(0, 2150)
            time.sleep(1)
        time.sleep(1)

        # ✅ 스크린샷 저장
        page.screenshot(path="debug_tiktok_page.png", full_page=True)
        print("📸 페이지 스크린샷 저장됨: debug_tiktok_page.png")

        lines = [l.strip() for l in page.inner_text("body").splitlines() if l.strip()]
        browser.close()

    results = []
    i = 0
    found_first = False
    while i < len(lines) - 4:
        if not found_first:
            if (
                re.match(r"^\d+$", lines[i])
                and lines[i + 1].startswith("#")
                and lines[i + 2] == "Travel"
                and re.match(r"^[0-9,.]+[KMB]?$", lines[i + 3])
                and lines[i + 4] == "Posts"
            ):
                results.append((lines[i + 1], lines[i + 3]))
                found_first = True

                i += 5

                while i < len(lines) and (
                    lines[i] in [
                        "See analytics",
                        "Access detail page for more insights of the trend",
                        "Got it"
                    ]
                ):
                    i += 1
                continue
            else:
                i += 1
                continue

        if (
                re.match(r"^\d+$", lines[i])
                and lines[i + 1].startswith("#")
                and lines[i + 2] == "Travel"
                and re.match(r"^[0-9,.]+[KMB]?$", lines[i + 3])
                and lines[i + 4] == "Posts"
        ):
            results.append((lines[i + 1], lines[i + 3]))
            i += 5
        else:
            i += 1

    return results

# Trendie api를 통해 Trendie 서비스로 해시태그 전송
def send_hashtags_to_api(hashtags):
    for tag, post_count in hashtags:
        try:
            week_posts= int(
                post_count
                    .replace(",","")
                    .replace("K","000")
                    .replace("M", "000000")
                    .replace("B", "000000000")
            )
        except ValueError:
            print(f"❌ 숫자 변환 실패: {post_count}")
            continue

        data = {
            "hashtag": tag.lstrip("#"),
            "week_posts": week_posts
        }

        try:
            response= requests.post(API_URL, json=data)
            response.raise_for_status()
            print(f"✅ {data['hashtag']} 전송 성공")
        except requests.RequestException as e:
            print(f"❌ {data['hashtag']} 전송 실패: {e}")

if __name__ == "__main__":
    import os
    if not os.path.exists(COOKIES_FILE):
        save_cookies.save_tiktok_cookies()
    results = scrape_travel_hashtags_fixed()
    print(f"🔎 크롤링된 해시태그 개수: {len(results)}개")

    send_hashtags_to_api(results)  # API 전송 호출