import numpy as np
from PIL import Image
import os
from a2_filter_dicom_files_by_description import patient_protocol_files

def save_overlay_images(dicom_objects, output_folder="C:/NMDose/patient_protocol_images"):

    i_overlay = 1
    n_bits = 8

    for j, ds in enumerate(dicom_objects):
        series_instance_uid = ds.SeriesInstanceUID
        overlay_tag = (0x6000, 0x3000)  # 오버레이 데이터 태그 고정
        if overlay_tag in ds:
            overlay_raw = ds[overlay_tag].value
            rows = ds[(0x6000, 0x0010)].value  # 오버레이의 행 수
            cols = ds[(0x6000, 0x0011)].value  # 오버레이의 열 수

            decoded_linear = np.zeros(len(overlay_raw) * n_bits)

            # 오버레이 데이터 디코딩
            for i in range(1, len(overlay_raw)):
                for k in range(0, n_bits):
                    byte_as_int = overlay_raw[i]
                    decoded_linear[i * n_bits + k] = (byte_as_int >> k) & 0b1

            # 디코딩된 데이터를 오버레이 이미지로 변환
            overlay = np.reshape(decoded_linear, [rows, cols])
            image = Image.fromarray(overlay * 255).convert('L')

            # 이미지 파일로 저장
            output_image_path = os.path.join(output_folder, f"{series_instance_uid}.png")
            image.save(output_image_path)
            print(f"Overlay image saved to {output_image_path}")


# patient_protocol_files 리스트의 DICOM 객체들에서 오버레이 이미지를 추출하고 저장
save_overlay_images(patient_protocol_files)
