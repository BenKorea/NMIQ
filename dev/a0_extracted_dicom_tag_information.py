tag_information = [
    ((0x0008, 0x0008), "ImageType", "TEXT"),
    ((0x0008, 0x0020), "StudyDate", "DATE"),
    ((0x0008, 0x0030), "StudyTime", "TIME"),
    ((0x0008, 0x0060), "Modality", "TEXT"),
    ((0x0008, 0x0070), "Manufacturer", "TEXT"),
    ((0x0008, 0x0080), "InstitutionName", "TEXT"),
    ((0x0008, 0x1030), "StudyDescription", "TEXT"),
    ((0x0032, 0x1060), "RequestedProcedureDescription", "TEXT"),
    ((0x0008, 0x103E), "SeriesDescription", "TEXT"),
    ((0x0008, 0x1090), "ManufacturerModelName", "TEXT"),
    ((0x0010, 0x0010), "PatientName", "TEXT"),
    ((0x0010, 0x0020), "PatientID", "TEXT"),
    ((0x0010, 0x0030), "PatientBirthDate", "DATE"),
    ((0x0010, 0x0040), "PatientSex", "TEXT"),
    ((0x0010, 0x1010), "PatientAge", "TEXT"),  # or "TEXT" if includes non-numeric characters
    ((0x0010, 0x1020), "PatientSize", "NUMERIC"),
    ((0x0010, 0x1030), "PatientWeight", "NUMERIC"),
    ((0x0018, 0x1030), "ProtocolName", "TEXT"),
    ((0x0018, 0x5100), "PatientPosition", "TEXT"),
    ((0x0020, 0x0011), "SeriesNumber", "TEXT"),
    ((0x0020, 0x0013), "InstanceNumber", "INTEGER"),
    ((0x0040, 0x0301), "RETIRED_TotalNumberOfExposures", "INTEGER"),
    ((0x0040, 0x0310), "CommentsOnRadiationDose", "TEXT"),
    ((0x0020, 0x000E), "SeriesInstanceUID", "TEXT")
]

subtag_information = [
    ((0x0018, 0x0015), "BodyPartExamined", "TEXT"),
    ((0x0018, 0x0060), "KVP", "NUMERIC"),
    ((0x0018, 0x1150), "ExposureTime", "INTEGER"),
    ((0x0018, 0x8151), "XRayTubeCurrentInuA", "NUMERIC"),
    ((0x0018, 0x9302), "AcquisitionType", "TEXT"),
    ((0x0018, 0x9306), "SingleCollimationWidth", "NUMERIC"),
    ((0x0018, 0x9307), "TotalCollimationWidth", "NUMERIC"),
    ((0x0018, 0x9311), "SpiralPitchFactor", "NUMERIC"),
    ((0x0018, 0x9345), "CTDIvol", "NUMERIC"),
]
