import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

try:
    # 데이터베이스 연결 설정
    conn = psycopg2.connect(
        host="localhost",
        database="postgres",
        user="postgres",
        password="postgres"  # postgreSQL 설치시 설정한 비밀번호
    )

    # 자동 커밋 설정
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

    # 커서 생성
    cur = conn.cursor()

    # NMIQ 사용자가 이미 존재하는지 확인
    cur.execute("SELECT usename FROM pg_user WHERE usename = 'nmiq';") #postgreSQL에서는 대소문자 구별이 없기 때문에 소문자로 사용자를 만들었음.
    user_exists = cur.fetchone()

    if user_exists is not None:
        print("User nmiq already exists.")
    else:
        # NMIQ 사용자 생성
        cur.execute("CREATE USER nmiq WITH PASSWORD 'password';")  # 실제 비밀번호로 변경하세요.
        print("User created successfully.")

    # NMIQ 데이터베이스가 이미 존재하는지 확인
    cur.execute("SELECT datname FROM pg_database WHERE datname = 'nmiq';")
    db_exists = cur.fetchone()

    if db_exists is not None:
        print("Database nmiq already exists.")
    else:
        # NMIQ 데이터베이스 생성
        cur.execute("CREATE DATABASE nmiq WITH OWNER nmiq;")
        print("Database created successfully.")
except psycopg2.errors.DuplicateObject as e:
    if str(e).startswith('role "nmiq" already exists'):
        print("Role NMIQ already exists.")
    else:
        print(f"Database error occurred: {e}")
finally:
    # 연결 종료
    if conn:
        cur.close()
        conn.close()