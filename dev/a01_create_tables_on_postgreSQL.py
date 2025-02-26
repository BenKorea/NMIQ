import pandas as pd
import psycopg2
from a0_extracted_dicom_tag_information import tag_information, subtag_information


def convert_data_types(df_tags, df_subtags):
    # 'StudyDate'와 'PatientBirthDate' 등의 날짜 관련 필드 변환
    df_tags['StudyDate'] = pd.to_datetime(df_tags['StudyDate'], format='%Y%m%d', errors='coerce')
    df_tags['PatientBirthDate'] = pd.to_datetime(df_tags['PatientBirthDate'], format='%Y%m%d', errors='coerce')
    # 'PatientSize', 'PatientWeight' 등의 숫자 데이터 변환
    df_tags['PatientSize'] = pd.to_numeric(df_tags['PatientSize'], errors='coerce')
    df_tags['PatientWeight'] = pd.to_numeric(df_tags['PatientWeight'], errors='coerce')
    df_tags['InstanceNumber'] = pd.to_numeric(df_tags['InstanceNumber'], errors='coerce')
    df_tags['RETIRED_TotalNumberOfExposures'] = pd.to_numeric(df_tags['RETIRED_TotalNumberOfExposures'], errors='coerce')
    # 'StudyDate', 'PatientBirthDate', 'PatientSize', 'PatientWeight'를 제외한 모든 열을 문자열로 변환합니다.
    cols = df_tags.columns.drop(['StudyDate', 'PatientBirthDate', 'PatientSize', 'PatientWeight', 'InstanceNumber', 'RETIRED_TotalNumberOfExposures',])
    df_tags[cols] = df_tags[cols].astype(str)  # 나머지 열을 문자열로 변환

    # 'KVP' 등의 숫자 데이터 변환
    df_subtags['KVP'] = pd.to_numeric(df_subtags['KVP'], errors='coerce')
    df_subtags['ExposureTime'] = pd.to_numeric(df_subtags['ExposureTime'], errors='coerce')
    df_subtags['XRayTubeCurrentInuA'] = pd.to_numeric(df_subtags['XRayTubeCurrentInuA'], errors='coerce')
    df_subtags['SingleCollimationWidth'] = pd.to_numeric(df_subtags['SingleCollimationWidth'], errors='coerce')
    df_subtags['TotalCollimationWidth'] = pd.to_numeric(df_subtags['TotalCollimationWidth'], errors='coerce')
    df_subtags['SpiralPitchFactor'] = pd.to_numeric(df_subtags['SpiralPitchFactor'], errors='coerce')
    df_subtags['CTDIvol'] = pd.to_numeric(df_subtags['CTDIvol'], errors='coerce')
    # 제외한 모든 열을 문자열로 변환합니다.
    df_subtags['BodyPartExamined'] = df_subtags['BodyPartExamined'].astype(str)  # 나머지 열을 문자열로 변환
    df_subtags['AcquisitionType'] = df_subtags['AcquisitionType'].astype(str)  # 나머지 열을 문자열로 변환

    return df_tags, df_subtags