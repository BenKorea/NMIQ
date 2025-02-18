import pytesseract
from PIL import Image
import os
import pandas as pd
from connect_n_save_DB import connect_to_database, save_dataframe_to_database

# Tesseract OCR 엔진의 실행 파일 경로 설정
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def extract_text_and_save_cropped_images(directory, crop_areas_with_labels):
    text_results = []  # 추출된 텍스트를 저장할 리스트
    cropped_image_folder = os.path.join(directory, "cropped_images")  # 크롭된 이미지를 저장할 서브 폴더 경로
    os.makedirs(cropped_image_folder, exist_ok=True)  # 크롭된 이미지 폴더가 없으면 생성

    for filename in os.listdir(directory):  # 주어진 디렉토리의 파일을 순회
        if filename.endswith(".png"):  # 파일 확장자가 .png인 경우에만 처리
            image_path = os.path.join(directory, filename)  # 이미지 파일 경로
            file_texts = {'Filename': filename}  # 파일명을 key로 하는 딕셔너리 생성
            try:
                image = Image.open(image_path)  # 이미지 파일 열기
                # 주어진 크롭 영역과 라벨에 대해 반복 처리
                for crop_area_with_label in crop_areas_with_labels:
                    crop_area = crop_area_with_label['area']  # 크롭할 영역
                    label = crop_area_with_label['label']  # 크롭 영역에 해당하는 라벨
                    cropped_image = image.crop(crop_area)  # 이미지 크롭
                    cropped_image_path = os.path.join(cropped_image_folder, f"{label}_{filename}")  # 크롭된 이미지 저장 경로
                    cropped_image.save(cropped_image_path)  # 크롭된 이미지 저장
                    text = pytesseract.image_to_string(cropped_image).replace('\n', ' ')  # OCR 실행 후 줄바꿈 문자를 공백으로 대체

                    file_texts[label] = text.strip()  # 추출된 텍스트의 앞뒤 공백 제거 후 저장
            except Exception as e:
                print(f"Error processing {filename}: {e}")
            text_results.append(file_texts)  # 파일별 추출된 텍스트 정보를 리스트에 추가

    # 추출된 텍스트 정보를 담은 리스트를 pandas 데이터프레임으로 변환
    df = pd.DataFrame(text_results)
    return df

# 나머지 코드는 이전과 동일하게 유지하면 됩니다.



directory = r"C:\NMDose\patient_protocol_images"
crop_areas_with_labels = [
    {'area': (  0, 152-3, 512, 162+3), 'label': "Total_mAs"},
    {'area': (  0, 219-3, 512, 233-1), 'label': "PatientPosition"},
    {'area': (  0, 233-3, 512, 246-1), 'label': "Topogram"},
    {'area': (  0, 246-1, 512, 260-1), 'label': "CT"},
    {'area': (  0, 260-1, 512, 268+3), 'label': "PET"},
    {'area': (  0, 268+3, 512, 268+14), 'label': "another"},
     # 추가 크롭 영역과 라벨을 여기에 정의하세요.
]

# 함수 호출 및 데이터프레임 저장
df_texts = extract_text_and_save_cropped_images(directory, crop_areas_with_labels)

# 수정된 데이터프레임 출력 예시
for index, row in df_texts.iterrows():
    print(f"Filename: {row['Filename']}")
    # 크롭된 영역과 라벨에 대해 반복
    for label in crop_areas_with_labels:
        label_text = label['label']  # 라벨 텍스트
        if label_text in row:
            # 추출된 텍스트 출력
            print(f"{label_text}: {row[label_text]}")
    print("-" * 50)  # 행 구분을 위한 구분선


#Database connection and data saving
conn = connect_to_database()
if conn:
    save_dataframe_to_database(df_texts, conn, "Patient_protocol_OCR")
    conn.close()
    print("Database connection closed.")