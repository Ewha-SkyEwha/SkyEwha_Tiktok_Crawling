# TRENDIE
> 여행 유튜버(인플루언서)를 위한 틱톡, 유튜브의 트렌드를 분석하여 현재 여행 트렌드를 제공하고, 사용자가 업로드 할 영상을 분석하여 (맞춤형) 해시태그와 제목을 제공하는 모바일 어플리케이션

## 🔍 프로젝트 개요

**TRENDIE**는

✔ 최신 여행 트렌드를 시각화한 대시보드  
✔ 사용자 영상의 트렌드 일치도 피드백 보고서  

를 제공하는 **여행 유튜버 대상 피드백 제공 서비스**입니다.

---

## TikTok Hashtag Crawler 설명

TikTok Creative Center의 인기 해시태그 데이터를 자동으로 수집하고,
Travel 관련 해시태그를 추출하여 외부 API(Trendie 서비스)로 전송하는 크롤러입니다.

본 프로젝트는 Playwright 기반의 브라우저 자동화를 활용하여
TikTok 로그인 세션을 유지한 상태에서 데이터를 수집합니다.

## 소스코드 설명
1. save_cookies.py
   
   `save_tiktok_cookies()`
   - Playwright를 사용하여 TikTok Creative Center 페이지 접속
   - 사용자가 직접 로그인 완료 후 Enter 입력
   - 로그인 세션을 tiktok_cookies.json 파일로 저장
   - 이후 크롤링 시 로그인 과정 생략 가능
   
2. hashtag_crawler.py

   `scrape_travel_hashtags_fixed()`
    - TikTok Creative Center 해시태그 페이지 접속
    - Industry 드롭다운에서 Travel 필터 선택
    - 페이지 스크롤을 통해 해시태그 데이터 로딩
    - DOM 전체 텍스트를 파싱하여 해시태그명, 주간 게시물 수 추출
  
    `send_hashtags_to_api(hashtags)`
    - 크롤링한 해시태그 데이터를 외부 API로 POST 전송
    - 게시물 수를 정수형으로 변환 후 전송
    - API 통신 성공/실패 로그 출력

---
  ## 🛠 How to Build
  본 프로젝트는 별도의 빌드 과정이 필요하지 않습니다.
  Python 스크립트 기반으로 실행됩니다.

  ## ⚙️ How to Install
   1. Python(최소 3.8 필요) 설치
   2. `pip install -r requirements.txt`
        </br>playwright 최초 설치일 경우 아래 명령어로 브라우저 드라이버 설치:
          </br>`playwright install`
   3. 틱톡 크리에이티브 센터 로그인 쿠키 저장:
        </br>`python save_tiktok_cookies.py` 실행
       </br>자동 실행된 브라우저(틱톡 크리에이티브 센터)에 직접 로그인 후 터미널에 Enter 입력
   4. 인기 해시태그 순위 크롤링:
        </br>`python tiktok_hashtag_crawler.py` 실행

  ## 🧪 How to Test
  1. 로그인 쿠키 저장 테스트
     정상적으로 `tiktok_cookies.json` 생성 여부 확인
  2. 크롤링 테스트
     `debug_tiktok_page.png` 생성 여부 확인
  3. API 전송 테스트
     API URL을 로컬 환경 또는 Trendie 서버로 설정 후 POST 요청 성공 로그 확인

  ## 📂 주요 폴더 구조
  ```text
  .
  ├── TikTok_Crawler/
  │   └── debug_tiktok_page.png   # 크롤링 시점 페이지 스크린샷
  │   └── hashtag_crawler.py      # 해시태그 크롤링 및 API 전송 메인 로직
  │   └── requirements.txt
  │   └── tiktok_cookies.json     # 로그인 세션 쿠키 (자동 생성)
  │   └── save_cookies.py         # TikTok 로그인 후 쿠키 저장
  ├── .gitignore
  └── README.md
  ```
## 📊 Description of Sample Data
크롤링 데이터 예시
```
{
  "hashtag": "travelkorea",
  "week_posts": 125000
}
```
hashtag: 해시태그 이름

week_posts: 최근 주간 게시물 수 (정수)

## Description of Used Open Source
1. Playwright
브라우저 자동화 및 크롤링
https://playwright.dev/
Apache 2.0 License
2. Requests
외부 API 통신
https://docs.python-requests.org/
Apache 2.0 License

## Disclaimer
This project is for educational and internal use only.

Users are responsible for complying with TikTok’s Terms of Service.
