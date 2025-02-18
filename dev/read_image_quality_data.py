import os
import pandas as pd
import psycopg2

def read_image_quality_data(root_directory):
    # 데이터프레임을 생성할 리스트를 생성합니다.
    df_list = []
    # root_directory부터 시작하여 모든 디렉토리를 탐색합니다.
    for root, dirs, files in os.walk(root_directory):
        # 각 디렉토리에 대해서 실행합니다.
        for directory in dirs:
            # 디렉토리 이름에서 PtID와 StudyDate를 추출합니다.
            PtID, StudyDate = extract_PtID_StudyDate(directory)
            # PtID와 StudyDate가 유효한 경우에만 실행합니다.
            if PtID and StudyDate:
                # image_quality_data_path를 생성합니다.
                image_quality_data_path = os.path.join(root, directory, 'image_quality_data')
                # image_quality_data_path 내의 csv 파일들을 찾습니다.
                csv_files = find_csv_files(image_quality_data_path)
                # 각 csv 파일에 대해서 실행합니다.
                for file in csv_files:
                    # csv 파일의 경로를 생성합니다.
                    csv_path = os.path.join(image_quality_data_path, file)
                    try:
                        # csv 파일을 읽어서 데이터프레임을 생성합니다.
                        df = pd.read_csv(csv_path)
                        # Mean 컬럼의 값과 Standard deviation 항목을 나누어서 SNR이라는 컬럼을 생성합니다.
                        df['SNR'] = df['Mean'] / df['Standard deviation']
                        # 필요한 컬럼들만 선택하여 데이터프레임을 업데이트합니다.
                        df = df[['Segment', 'Volume mm3 (LM)', 'Mean', 'Standard deviation', 'SNR']]
                        # 데이터프레임을 리스트에 추가합니다.
                        df_list.append(pd.DataFrame({'PtID': PtID, 'StudyDate': StudyDate, 'SeriesDescription': file.replace('.csv', ''), 'Segment': df['Segment'], 'Volume mm3 (LM)': df['Volume mm3 (LM)'], 'Mean': df['Mean'], 'Standard deviation': df['Standard deviation'], 'SNR': df['SNR']}))
                    except Exception as e:
                        # 파일을 읽는 도중 에러가 발생한 경우 에러 메시지를 출력합니다.
                        print(f"Error reading file {csv_path}: {e}")
    # 모든 데이터프레임을 합쳐서 하나의 데이터프레임으로 만듭니다.
    result_df = pd.concat(df_list, ignore_index=True)
    # 결과 데이터프레임을 반환합니다.
    return result_df
def extract_PtID_StudyDate(directory):
    # 디렉토리 이름을 '_'로 분리합니다.
    parts = directory.split('_')
    # parts 리스트의 길이가 2이고, parts[0]가 8자리 숫자이고, parts[1]이 8자리 숫자인 경우에만 해당 값을 반환합니다.
    if len(parts) == 2 and parts[0].isdigit() and len(parts[0]) == 8 and parts[1].isdigit() and len(parts[1]) == 8:
        return parts[0], parts[1]
    # 그 외의 경우에는 None을 반환합니다.
    return None, None

def find_csv_files(image_quality_data_path):
    # csv 파일들을 저장할 리스트를 생성합니다.
    csv_files = []
    # image_quality_data_path가 존재하는 경우에만 실행합니다.
    if os.path.exists(image_quality_data_path):
        # image_quality_data_path 내의 파일들을 탐색합니다.
        for file in os.listdir(image_quality_data_path):
            # 파일이 '.csv'로 끝나고, 'schema'가 파일 이름에 포함되지 않은 경우에만 리스트에 추가합니다.
            if file.endswith('.csv') and 'schema' not in file:
                csv_files.append(file)
    # csv_files 리스트를 반환합니다.
    return csv_files


# 실행할 디렉토리 경로 설정
directory_path = r"C:\NMIQ\data"
# 데이터 읽기
image_quality_data = read_image_quality_data(directory_path)
print(image_quality_data)



from sqlalchemy import create_engine

def save_to_postgresql(dataframe):
    # SQLAlchemy를 사용하여 PostgreSQL에 연결
    engine = create_engine('postgresql://nmiq:password@localhost:5432/nmiq')

    # 데이터프레임을 PostgreSQL 테이블로 저장
    dataframe.to_sql('image_quality_data', engine, if_exists='replace', index=False)

# PostgreSQL에 데이터 저장
save_to_postgresql(image_quality_data)

# 저장된 레코드 수 출력
print(f"Successfully saved {len(image_quality_data)} records to PostgreSQL.")
