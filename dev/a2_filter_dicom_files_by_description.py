from dev.a1_dicom_reader import dicom_files
# from a1_dicom_reader import dicom_files 

def filter_dicom_files_by_description(dicom_files):
    """DICOM 파일들을 SeriesDescription에 따라 'Dose Report'와 'Patient Protocol'로 필터링합니다."""
    dose_report_files = []
    patient_protocol_files = []

    for file in dicom_files:
        if hasattr(file, 'SeriesDescription'):
            if file.SeriesDescription == "Dose Report":
                dose_report_files.append(file)
            elif file.SeriesDescription == "Patient Protocol":
                patient_protocol_files.append(file)

    return dose_report_files, patient_protocol_files


# 'Dose Report'와 'Patient Protocol'에 해당하는 파일 필터링
dose_report_files, patient_protocol_files = filter_dicom_files_by_description(dicom_files)

# 결과 확인
print(f"Dose Report 파일 개수: {len(dose_report_files)}")
print(f"Patient Protocol 파일 개수: {len(patient_protocol_files)}")
