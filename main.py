import streamlit as st
from crawler import NewsCrawler
from text_cleaner import TextCleaner
from model import NewsSummarizer
from Data_Manager import NewsUtils

# 페이지 기본 설정
st.set_page_config(page_title="3줄 뉴스 요약 봇", page_icon="📰")

#초기화(객체 생성)
@st.cache_resource
def load_summarizer():
    return NewsSummarizer()

crawler = NewsCrawler()
cleaner = TextCleaner()
utils = NewsUtils()
summarizer = load_summarizer()

#화면 구성 (UI)
st.title("📰 AI 3줄 뉴스 요약 봇")
st.markdown("네이버 뉴스 URL을 입력하면 **AI가 내용을 3줄로 요약**해줍니다.")

# 사이드바: 사용법 설명
with st.sidebar:
    st.header("사용 방법")
    st.markdown("1. 네이버 뉴스에 접속한다.")
    st.markdown("2. 기사 링크(URL)를 복사한다.")
    st.markdown("3. 입력창에 붙여넣고 버튼을 누른다.")
    st.info("Team 5 Project : Open Source SW")

# URL 입력창
url = st.text_input("뉴스 기사 URL을 입력하세요:")

# 버튼 클릭 시 동작
if st.button("요약 시작 🚀"):
    if url:
        try:
            with st.spinner('1단계: 뉴스를 가져오는 중입니다... 🕷️'):
                title, raw_content = crawler.get_news(url)
            
            if not title:
                st.error(raw_content) # 에러 메시지 출력
            else:
                st.success(f"기사 수집 완료: {title}")
                
                with st.spinner('2단계: 내용을 다듬고 AI가 읽는 중입니다... 🧹'):
                    clean_content = cleaner.clean_text(raw_content)
                
                # 본문 내용 미리보기
                with st.expander("원문 기사 내용 보기"):
                    st.write(clean_content)

                if cleaner.is_valid_length(clean_content):
                    with st.spinner('3단계: AI가 열심히 요약 중입니다... 🤖'):
                        summary = summarizer.summarize(clean_content)
                    
                    #결과 출력
                    st.divider()
                    st.subheader("📝 3줄 요약 결과")
                    st.info(summary)
                    
                    #키워드 분석
                    keywords = utils.extract_keywords(clean_content)
                    st.write("🔑 **핵심 키워드:** ", ", ".join([f"#{k[0]}" for k in keywords]))
                    
                    #파일 저장
                    saved_file = utils.save_to_csv(title, clean_content, summary)
                    st.caption(f"✅ 결과가 '{saved_file}' 파일에 자동 저장되었습니다.")
                    
                else:
                    st.warning("기사 내용이 너무 짧아서 요약할 수 없습니다.")
                    
        except Exception as e:
            st.error(f"오류가 발생했습니다: {e}")
    else:
        st.warning("URL을 입력해주세요!")