# %%
import os
import pydicom


def read_dicom_files(directory):
    dicom_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".dcm"):
                filepath = os.path.join(root, file)
                ds = pydicom.dcmread(filepath, stop_before_pixels=True)
                dicom_files.append(ds)
    return dicom_files


# 실행할 디렉토리 경로 설정
directory = r"C:\NMDose\data"

# 지정된 디렉토리에서 DICOM 파일들을 읽어옵니다.
dicom_files = read_dicom_files(directory)

# 읽어온 DICOM 파일의 개수를 출력
print(f"dicom 파일 개수: {len(dicom_files)}")
