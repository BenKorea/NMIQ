from pynetdicom import AE
from pynetdicom.sop_class import PatientRootQueryRetrieveInformationModelFind

# DICOM 서버의 IP 주소, 포트 번호, AE Title 설정
pacs_server_ip = '127.0.0.1'
pacs_server_port = 5678
ae_title = 'NMDOSE'

# AE 생성 및 Query/Retrieve Presentation Contexts 요청
ae = AE()
ae.add_requested_context(PatientRootQueryRetrieveInformationModelFind)

# DICOM 서버에 연결 시도
assoc = ae.associate(pacs_server_ip, pacs_server_port, ae_title=ae_title)
if assoc.is_established:
    print("DICOM 서버에 성공적으로 연결되었습니다.")
    # 연결 종료
    assoc.release()
else:
    print("DICOM 서버에 연결할 수 없습니다. 설정을 확인하세요.")

# 연결 테스트 완료
