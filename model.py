rom transformers import PreTrainedTokenizerFast, BartForConditionalGeneration
import torch

class NewsSummarizer:
    def __init__(self):
        # Hugging Face에서 한국어 요약에 특화된 모델 로드 (KoBART)
        # 처음 실행 시 모델을 다운로드하느라 시간이 좀 걸릴 수 있음
        self.model_name = "gogamza/kobart-summarization"
        print("모델을 로딩 중입니다...")
        self.tokenizer = PreTrainedTokenizerFast.from_pretrained(self.model_name)
        self.model = BartForConditionalGeneration.from_pretrained(self.model_name)
        
    def summarize(self, text):
        """
        긴 텍스트를 받아서 3줄 요약을 반환
        """
        try:
            # 입력 텍스트를 토큰으로 변환 (Tensor)
            input_ids = self.tokenizer.encode(text, return_tensors="pt")
            
            # 모델이 요약문 생성 (Beam Search 방식 사용)
            # max_length: 요약문 최대 길이, min_length: 최소 길이
            summary_text_ids = self.model.generate(
                input_ids=input_ids,
                bos_token_id=self.model.config.bos_token_id,
                eos_token_id=self.model.config.eos_token_id,
                length_penalty=2.0,
                max_length=128,
                min_length=32,
                num_beams=4,
            )
            
            # 숫자로 된 결과를 다시 글자로 변환 (Decoding)
            summary = self.tokenizer.decode(summary_text_ids[0], skip_special_tokens=True)
            return summary
            
        except Exception as e:
            return f"요약 실패: {str(e)}"