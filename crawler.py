import requests
from bs4 import BeautifulSoup

class NewsCrawler:
    def __init__(self):
        # 크롤링 시 차단 방지를 위한 User-Agent 설정
        self.headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            )
        }

    def clean_text(self, text):
        """
        뉴스 본문에서 불필요한 공백, 광고 문구 등 제거
        """
        replace_list = [
            "무단 전재 및 재배포 금지", 
            "▶", 
            "■",
            "▲",
            "ⓒ", 
            "관련 기사 더 보기"
        ]
        for r in replace_list:
            text = text.replace(r, "")

        return text.strip()

    def get_news(self, url):
        """
        URL을 받아서 (제목, 본문) 반환
        실패 시 (None, 에러메시지) 반환
        """
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')

            # ---------------------------
            # 제목 추출
            # ---------------------------
            title_selectors = [
                "#title_area",             # 네이버 뉴스 제목
                ".media_end_head_title",   # 네이버 최신 구조
                "h2",                      # 일반적인 제목 태그
                "h1"                       # 일부 사이트에서 제목
            ]

            title_tag = None
            for selector in title_selectors:
                title_tag = soup.select_one(selector)
                if title_tag:
                    break

            if not title_tag:
                return None, "제목을 찾을 수 없습니다."

            title = title_tag.get_text(strip=True)

            # ---------------------------
            # 본문 추출
            # ---------------------------
            content_selectors = [
                "#dic_area",          # 네이버 뉴스 본문
                ".go_content",        # 일부 구조
                ".article_body", 
                ".article-content",
                "article",
                "#articeBody"
            ]

            content_tag = None
            for selector in content_selectors:
                content_tag = soup.select_one(selector)
                if content_tag:
                    break

            if not content_tag:
                return None, "본문을 찾을 수 없습니다."

            content = content_tag.get_text(separator="\n", strip=True)
            content = self.clean_text(content)

            return title, content

        except requests.exceptions.Timeout:
            return None, "요청 시간이 초과되었습니다."
        except requests.exceptions.RequestException as req_err:
            return None, f"HTTP 요청 오류: {str(req_err)}"
        except Exception as e:
            return None, f"크롤링 중 알 수 없는 오류 발생: {str(e)}"


# -----------------------------------------------------------
# 테스트 코드 (해당 파일을 단독 실행하면 동작)
# -----------------------------------------------------------
if __name__ == "__main__":
    crawler = NewsCrawler()

    test_url = input("뉴스 URL을 입력하세요: ")
    title, content = crawler.get_news(test_url)

    print("\n=== [제목] ===")
    print(title)

    print("\n=== [본문] ===")
    print(content)
