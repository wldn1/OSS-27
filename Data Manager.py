import pandas as pd
from collections import Counter
import datetime
import os

class NewsUtils:
    def extract_keywords(self, text, num_keywords=3):
        """
        텍스트에서 가장 많이 등장한 단어(명사 위주로 가정) 추출
        """
        if not text:
            return []
            
        # 간단하게 공백 기준으로 단어 분리 (KoNLPy 없이 구현하여 설치 오류 방지)
        words = text.split()
        # 2글자 이상인 단어만 필터링
        words = [w for w in words if len(w) >= 2]
        
        # 빈도수 계산
        counter = Counter(words)
        return counter.most_common(num_keywords)

    def save_to_csv(self, title, original, summary):
        """
        결과를 CSV 파일로 저장
        """
        date_str = datetime.datetime.now().strftime("%Y-%m-%d")
        filename = f"news_summary_{date_str}.csv"
        
        data = {
            'Date': [datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
            'Title': [title],
            'Original_Length': [len(original)],
            'Summary': [summary]
        }
        
        df = pd.DataFrame(data)
        
        # 파일이 없으면 새로 만들고, 있으면 뒤에 이어붙이기 (append)
        if not os.path.exists(filename):
            df.to_csv(filename, index=False, encoding='utf-8-sig')
        else:
            df.to_csv(filename, mode='a', header=False, index=False, encoding='utf-8-sig')
            
        return filename
