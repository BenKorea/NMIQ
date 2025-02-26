# %%
import chardet

# DICOM에서 읽은 데이터 (바이트)
text_bytes = b"Hello \xbe\xc8\xc5\xf5"

# 인코딩 자동 감지
detected = chardet.detect(text_bytes)
encoding = detected['encoding']
print(f"Detected encoding: {encoding}")

# 감지된 인코딩으로 디코딩
decoded_text = text_bytes.decode(encoding)
print(decoded_text)  # 정상 출력

# %%
