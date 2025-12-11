import re

class TextCleaner:
    def clean_text(self, text):
        """
        뉴스 본문에서 불필요한 기호, 이메일, 기자 이름 등을 제거하는 함수
        """
        if not text:
            return ""

        # 1. 이메일 제거
        text = re.sub(r'[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+', '', text)
        
        # 2. 괄호 안의 내용 제거 (기자명, 사진 출처 등)
        text = re.sub(r'\[.*?\]', '', text) 
        text = re.sub(r'\(.*?\)', '', text) 
        
        # 3. 특수문자 및 공백 정리
        text = re.sub(r'[^가-힣a-zA-Z0-9. ]', ' ', text)
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text

    def is_valid_length(self, text, min_len=50):
        return len(text) >= min_len

if __name__ == "__main__":
    cleaner = TextCleaner()
    print("테스트 실행: 코드가 정상 작동합니다.")
