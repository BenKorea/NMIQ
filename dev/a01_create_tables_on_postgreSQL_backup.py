import pandas as pd
import psycopg2
from dev.a0_extracted_dicom_tag_information import tag_information, subtag_information

def create_table_from_tag_info(connection, cursor, table_name, tag_info, add_series_instance_uid=False, add_item_number=False, add_ctdivol_average=False):
    # 테이블 생성 SQL 쿼리 생성
    create_table_query = f"CREATE TABLE IF NOT EXISTS {table_name} ("
    if add_series_instance_uid:
        # SeriesInstanceUID 컬럼 추가
        create_table_query += '\n    "SeriesInstanceUID" TEXT,'
    if add_item_number:
        # ItemNumber 컬럼 추가
        create_table_query += '\n    "ItemNumber" INTEGER,'
    for tag, desc, data_type in tag_info:
        # 컬럼 이름을 따옴표로 감싸 대소문자를 구분하도록 함
        create_table_query += f'\n    "{desc}" {data_type},'
    if add_ctdivol_average:
        # CTDIvol_Average 컬럼 추가
        create_table_query += '\n    "CTDIvol_Average" DOUBLE PRECISION,'

    create_table_query = create_table_query.rstrip(",")  # 마지막 쉼표 제거
    create_table_query += "\n);"

    # SQL 쿼리 실행하여 테이블 생성
    cursor.execute(create_table_query)
    connection.commit()

try:
    # 데이터베이스 연결 설정
    conn = psycopg2.connect(
        host="localhost",
        database="nmiq",
        user="nmiq",
        password="password"  # 향후 실제 비밀번호로 변경 필요
    )
    cur = conn.cursor()

    # 메인 태그 정보를 사용해 테이블 생성, CTDIvol_Average 컬럼 추가
    main_table_name = '"Dose_Report"'
    create_table_from_tag_info(conn, cur, main_table_name, tag_information, add_ctdivol_average=True)

    # 서브태그 정보를 사용해 별도의 테이블 생성, SeriesInstanceUID 및 ItemNumber 컬럼 추가
    sub_table_name = '"Dose_Report_subtags"'
    create_table_from_tag_info(conn, cur, sub_table_name, subtag_information, add_series_instance_uid=True, add_item_number=True)

    print("Tables created successfully.")
except Exception as e:
    print(f"Database error occurred: {e}")
finally:
    # 연결 종료
    if conn:
        cur.close()
        conn.close()

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