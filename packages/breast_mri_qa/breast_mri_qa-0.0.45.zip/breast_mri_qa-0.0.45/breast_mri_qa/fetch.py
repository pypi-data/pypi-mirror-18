import numpy as np
import requests
import email
import dicom
import io
import sys


class Fetcher:

    def __init__(self, host, port, user, passwd):
        self.host = host
        self.port = port
        self.user = user
        self.passwd = passwd
        self.accept = {'Accept': 'application/json'}
        self.query = {}

    def get_studies_json(self, patient_name):
        self.query = {'PatientName': patient_name}
        url = 'http://%s:%d/dicom-web/studies/' % (self.host, self.port)
        http_response = requests.get(url, auth=(self.user, self.passwd), headers=self.accept, params=self.query)
        matches = http_response.json()
        return matches

    def get_studies(self, patient_id):
        self.query = {'PatientID': patient_id}
        url = 'http://%s:%d/dicom-web/studies/' % (self.host, self.port)
        http_response = requests.get(url, auth=(self.user, self.passwd), headers=self.accept, params=self.query)
        matches = http_response.json()
        studyuids = [match['0020000D']['Value'][0] for match in matches]
        return studyuids

    def get_series(self, studyuid):
        url = 'http://%s:%d/dicom-web/studies/%s/series/' % (self.host, self.port, studyuid)
        http_response = requests.get(url, auth=(self.user, self.passwd), headers=self.accept, params=self.query)
        matches = http_response.json()
        seriesuids = [match['0020000E']['Value'][0] for match in matches]
        return seriesuids

    def get_valid_image_instance(self, studyuid, seriesuid):
        url = 'http://%s:%d/dicom-web/studies/%s/series/%s' % (self.host, self.port, studyuid, seriesuid)
        http_response = requests.get(url, auth=(self.user, self.passwd))
        # Construct valid mime by prepending content type
        if (sys.version_info[0] == 2):
            hdr = ('Content-Type: ' + http_response.headers['Content-Type']).encode()
            msg =  email.message_from_string(hdr + b'\r\n' + http_response.content)
        else:
            hdr = ('Content-Type: ' + http_response.headers['Content-Type'])
            msg =  email.message_from_bytes(hdr + '\r\n' + http_response.content)
        dcmobjs = []
        for part in msg.walk():
            dcmdata = part.get_payload(decode=True)
            if dcmdata is not None:
                if (sys.version_info[0] == 2):
                    dcmobjs.append(dicom.read_file(io.BytesIO(dcmdata)))
                else:
                    dcmobjs.append(dicom.read_file(io.StringIO(dcmdata).encode('UTF-8')))
        ret_dcm_obj = dcmobjs[0]
        ret_dicom_dict = {}
        try:
            ret_dcm_obj[0x0008, 0x0008]  # Only images have image type header tag
            ret_dicom_dict['SeriesInstanceUID'] = ret_dcm_obj[0x0020, 0x000E].value
            ret_dicom_dict['SeriesDescription'] = ret_dcm_obj[0x0008, 0x103E].value
            ret_dicom_dict['StudyDescription'] = ret_dcm_obj[0x0008, 0x1030].value
            ret_dicom_dict['StudyInstanceUID'] = ret_dcm_obj[0x0020, 0x000D].value
            ret_dicom_dict['StudyDate'] = ret_dcm_obj[0x0008, 0x0020].value
            ret_dicom_dict['StationName'] = ret_dcm_obj[0x0008, 0x1010].value
            ret_dicom_dict['PatientName'] = ret_dcm_obj[0x0010, 0x0010].value
            ret_dicom_dict['PatientID'] = ret_dcm_obj[0x0010, 0x0020].value
            ret_dicom_dict['MagneticFieldStrength'] = ret_dcm_obj[0x0018, 0x0087].value
            ret_dicom_dict['PixelArray'] = ret_dcm_obj.pixel_array
        except Exception as ex:
            pass
        if ret_dicom_dict is None:
            return None
        else:
            return ret_dicom_dict
