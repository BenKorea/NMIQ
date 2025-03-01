import pandas as pd
import pydicom
import psycopg2
from sqlalchemy import create_engine
# from a2_filter_dicom_files_by_description import dose_report_files, patient_protocol_files
from dev.a2_filter_dicom_files_by_description import dose_report_files, patient_protocol_files
# from a0_extracted_dicom_tag_information import tag_information, subtag_information
from dev.a0_extracted_dicom_tag_information import tag_information, subtag_information
from dev.a01_create_tables_on_postgreSQL import convert_data_types
from dev.connect_n_save_DB import connect_to_database, save_dataframe_to_database


def extract_data(dicom_files, tag_information):
    data = []
    for dicom_data in dicom_files:
        row = {}
        for tag, desc, _ in tag_information:
            value = dicom_data.get(tag, None)
            row[desc] = value.value if value is not None else None
        data.append(row)
    return pd.DataFrame(data)


def extract_subtags_with_ctdivol_average_per_patient(dicom_files, sequence_tag, subtag_information):
    patient_series_data = {}  # 환자별 시퀀스 데이터 저장
    ctdivol_averages_per_patient = {}  # 환자별 CTDIvol 평균값 저장

    for dicom_data in dicom_files:
        series_instance_uid = dicom_data.get((0x0020, 0x000E), "Unknown SeriesInstanceUID").value

        # 환자별 CTDIvol 값 저장을 위한 리스트 초기화
        if series_instance_uid not in patient_series_data:
            patient_series_data[series_instance_uid] = []
            ctdivol_averages_per_patient[series_instance_uid] = []

        if sequence_tag in dicom_data:
            sequence_items = dicom_data[sequence_tag]
            for item_index, item in enumerate(sequence_items, start=1):
                item_subtags = {"SeriesInstanceUID": series_instance_uid, "ItemNumber": item_index}
                is_helical = False

                for subtag, desc, _ in subtag_information:
                    value = item.get(subtag, None)
                    if value is not None:
                        item_subtags[desc] = value.value
                        if desc == "AcquisitionType" and value.value == "SPIRAL":
                            is_helical = True
                        if desc == "CTDIvol" and is_helical:
                            try:
                                # 환자별 CTDIvol 값 추가
                                ctdivol_averages_per_patient[series_instance_uid].append(float(value.value))
                            except ValueError:
                                pass
                    else:
                        item_subtags[desc] = None

                patient_series_data[series_instance_uid].append(item_subtags)

    # 각 환자별 CTDIvol 평균값 계산
    for uid, ctdivol_values in ctdivol_averages_per_patient.items():
        if ctdivol_values:
            ctdivol_averages_per_patient[uid] = sum(ctdivol_values) / len(ctdivol_values)
        else:
            ctdivol_averages_per_patient[uid] = None

    return patient_series_data, ctdivol_averages_per_patient


# Extract tag and subtag information
combined_files = dose_report_files + patient_protocol_files
df_tags = extract_data(combined_files, tag_information)

sequence_tag = (0x0040, 0x030E)
patient_series_data, ctdivol_averages_per_patient = extract_subtags_with_ctdivol_average_per_patient(dose_report_files, sequence_tag, subtag_information)

# Combine all patient sequence data into a single list
all_series_list = [item for sublist in patient_series_data.values() for item in sublist]
df_subtags = pd.DataFrame(all_series_list)

# Convert data types
convert_data_types(df_tags, df_subtags)


for uid, average in ctdivol_averages_per_patient.items():
    print(f"{uid}: CTDIvol 평균값 (SPIRAL) = {average}")

# Merge ctdivol_averages_per_patient with df_tags
df_tags['CTDIvol_Average'] = df_tags['SeriesInstanceUID'].map(ctdivol_averages_per_patient)

print(df_tags['CTDIvol_Average'])
print(df_tags['CTDIvol_Average'])

#  Database connection and data saving
conn = connect_to_database()
if conn:
    save_dataframe_to_database(df_tags, conn, "Dose_Report")
    save_dataframe_to_database(df_subtags, conn, "Dose_Report_subtags")
    conn.close()
    print("Database connection closed.")
