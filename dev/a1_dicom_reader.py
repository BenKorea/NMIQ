import os
import pydicom

def read_dicom_files(directory):
    dicom_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".dcm"):
                filepath = os.path.join(root, file)
                ds = pydicom.dcmread(filepath, stop_before_pixels=True)
                character_set = ds.get('SpecificCharacterSet', 'ISO_IR 192')  # UTF-8 as default

                original_study_description = ds.get('StudyDescription', 'N/A')
                original_patient_name = ds.get('PatientName', 'N/A')

                #print(f"File: {file} - Specific Character Set: {character_set}")

                if 'StudyDescription' in ds:
                    study_description = decode_based_on_character_set(ds.StudyDescription, character_set)
                    ds.StudyDescription = study_description
                    #print(f"Original Study Description: {original_study_description} -> Decoded: {study_description}")

                if 'PatientName' in ds:
                    patient_name = decode_based_on_character_set(ds.PatientName, character_set)
                    ds.PatientName = patient_name
                    #print(f"Original Patient Name: {original_patient_name} -> Decoded: {patient_name}")

                dicom_files.append(ds)
    return dicom_files

def decode_based_on_character_set(value, character_set):
    if character_set == 'ISO_IR 100':
        return value.encode('iso-8859-1').decode('latin1')
    elif character_set == 'ISO_IR 192':
        return value  # UTF-8 encoded, no need to transform
    elif character_set == 'ISO_IR 149':
        return value.encode('iso-8859-1').decode('euc-kr')
    return value  # Default or unknown character set, return as is

# 실행할 디렉토리 경로 설정
directory = r"C:\NMDose\data"

# 지정된 디렉토리에서 DICOM 파일들을 읽어옵니다.
dicom_files = read_dicom_files(directory)

# 읽어온 DICOM 파일의 개수를 출력합니다.
print(f"dicom 파일 개수: {len(dicom_files)}")
