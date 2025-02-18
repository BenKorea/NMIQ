import psycopg2

try:
    # 데이터베이스 연결 설정
    conn = psycopg2.connect(
        host="localhost",  # 호스트 주소
        database="postgres",  # 데이터베이스 이름
        user="postgres",  # 사용자 이름
        password="postgres"  # 비밀번호
    )
    cur = conn.cursor()

    # Dose_Report 테이블 삭제 쿼리
    drop_table_query = 'DROP TABLE IF EXISTS "Dose_Report";'
    drop_table_query_subtags = 'DROP TABLE IF EXISTS "Dose_Report_subtags";'    # 쿼리 실행
    drop_table_query_OCR = 'DROP TABLE IF EXISTS "Patient_protocol_OCR";'  # 쿼리 실행
    drop_table_query_OCR_total = 'DROP TABLE IF EXISTS "Patient_protocol_OCR_total";'  # 쿼리 실행
    cur.execute(drop_table_query)
    cur.execute(drop_table_query_subtags)
    cur.execute(drop_table_query_OCR)
    cur.execute(drop_table_query_OCR_total)
    conn.commit()  # 변경사항 커밋
    print("Tables have been deleted successfully.")

except psycopg2.DatabaseError as error:
    print(f"Error occurred: {error}")
finally:
    # 데이터베이스 연결 종료
    if conn is not None:
        conn.close()
