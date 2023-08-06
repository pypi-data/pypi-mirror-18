"""
Obtain dicom objects from an Orthanc server.
"""
import io
import sys
import email
import json

import numpy as np
import requests
import dicom

from .organise import Instance


class Fetcher:
    """
    Object-oriented approach to querying the Orthanc server.

    Parameter values specify the details required to connect to and
    authenticate with the Orthanc server.

    Parameters
    ----------
    host : String
        The v4 IP address of the Orthanc DICOM server.
        (e.g. `'192.168.0.3'`)
    port : int
        The port number that the Orthanc HTTP server is configured to
        run on. (e.g. `80`)
    user : String
        The username required to access the Orthanc server.
        (e.g. `'orthanc'`)
    passwd : String
        The password required to access the Orthanc server.
        (e.g. `'orthanc'`)

    Attributes
    ----------
    host : String
        The v4 IP address of the Orthanc DICOM server. (e.g. `'192.168.0.3'`)
    port : int
        The port number that the Orthanc HTTP server is configured to run on.
        (e.g. `80`)
    user : String
        The username required to access the Orthanc server. (e.g. `'orthanc'`)
    passwd : String
        The password required to access the Orthanc server. (e.g. `'orthanc'`)
    accept : dictionary
        MIME type used in the HTTP request header, default value is
        `{'Accept': 'application/json'}`
    """

    def __init__(self, host, port, user, passwd):
        self.host = host
        self.port = port
        self.user = user
        self.passwd = passwd
        self.accept = {'Accept': 'application/json'}

    def get_studies_json(self, patient_name):
        """
        Obtain a JSON object describing the studies on the server associated
        with a patient name matching that supplied in `patient_name`.

        Parameters
        ----------
        patient_name : String
            A string used to match against patient names of the studies on the
            Orthanc server. No need to include wildcards.

        Returns
        -------
        matches : JSON object
            A JSON object containing a list of matched studies with information
            such as date of study, name of patient etc...
        """
        patient_search_term = '*{}*'.format(patient_name)
        query = {'PatientName': patient_search_term}
        url = 'http://{0}:{1}/dicom-web/studies/'.format(self.host, self.port)
        http_response = requests.get(
            url,
            auth=(self.user, self.passwd),
            headers=self.accept,
            params=query
        )
        matches = http_response.json()
        return matches

    def get_n_most_recent_study_details(self, patient_name, n_most_recent):
        """
        Get the N most recent studies matching patient name criteria.

        This function extends get_studies_json by allowing an additional
        parameter specifying how many studies to return. Studies are returned in
        descending order (most recent first).

        Parameters
        ----------
        patient_name : String
            A string used to match against patient names of the studies on the
            Orthanc server. No need to include wildcards.
        n_most_recent : int
            The number of studies to return.

        Returns
        -------
        n_most_recent_studies : JSON object
            A JSON object containing a list of matched studies with information
            such as date of study, name of patient etc... The number of JSON
            objects in the list will be less than or equal to the parameter
            `n_most_recent`.
        """
        json_studies = self.get_studies_json(patient_name=patient_name)
        studies = []
        for study in json_studies:
            c = {}
            c['StudyDate'] = study['00080020']['Value'][0]
            c['StudyUID'] = study['0020000D']['Value'][0]
            c['PatientName'] = study['00100010']['Value'][0]
            seriesuids_for_station_name = self.get_series(c['StudyUID'])
            for uid in seriesuids_for_station_name:
                instance = self.get_valid_image_instance(c['StudyUID'], uid)
                if instance:
                    c['StationName'] = instance.station_name
                    break
            studies.append(c)
        studies = sorted(studies, key=lambda k: k['StudyDate'])
        n_most_recent_studies = studies[:n_most_recent]
        return n_most_recent_studies

    def get_series(self, studyuid):
        """
        Get all series UIDs associated with a certain Study.

        Parameters
        ----------
        studyuid : String
            Study Instance UID as specified in the DICOM header by (0020,000D).

        Returns
        -------
        seriesuids : list of Strings
            A list of Series Instance UIDs as specified in the DICOM header
            by tag (0020,000E).

        """
        url = 'http://{}:{}/dicom-web/studies/{}/series/'.format(
            self.host,
            self.port,
            studyuid
        )
        http_response = requests.get(
            url,
            auth=(self.user, self.passwd),
            headers=self.accept
        )
        matches = http_response.json()
        seriesuids = [match['0020000E']['Value'][0] for match in matches]
        return seriesuids

    def get_valid_image_instance(self, studyuid, seriesuid):
        """
        Check whether a series contains a valid image instance and return it if so.

        Parameters
        ----------
        studyuid : String
            Study Instance UID as specified in the DICOM header by (0020,000D).
        seriesuid : String
            Series Instance UIDs as specified in the DICOM header by (0020,000E).

        Returns
        -------
        dicom_instance_info : Instance
            An object of type Instance.

        See Also
        --------
        Instance
        """
        url = 'http://{}:{}/dicom-web/studies/{}/series/{}'.format(
            self.host,
            self.port,
            studyuid,
            seriesuid
        )
        http_response = requests.get(
            url,
            auth=(self.user, self.passwd)
        )
        # Construct valid mime by prepending content type
        if (sys.version_info[0] == 2):
            hdr = ('Content-Type: ' + http_response.headers['Content-Type'])
            msg = email.message_from_string(hdr + b'\r\n' + http_response.content)
        else:
            hdr = ('Content-Type: ' + http_response.headers['Content-Type']).encode('UTF-8')
            msg = email.message_from_bytes(hdr + b'\r\n' + http_response.content)
        dcmobjs = []
        for part in msg.walk():
            dcmdata = part.get_payload(decode=True)
            if dcmdata is not None:
                if (sys.version_info[0] == 2):
                    dcmobjs.append(dicom.read_file(io.BytesIO(dcmdata)))
                else:
                    dcmobjs.append(dicom.read_file(io.BytesIO(dcmdata)))
        # For Phillips scanners the dicom object is in the first element of the list
        dcm_obj = dcmobjs[0]
        # Create an instance object which will hold dicom instance pixel array and various headers
        instance = None
        try:
            dcm_obj[0x0008, 0x0008]  # Only images have image type header tag
            instance = Instance(
                series_instance_uid=str(dcm_obj[0x0020, 0x000E].value),
                series_description=dcm_obj[0x0008, 0x103E].value,
                study_description=dcm_obj[0x0008, 0x1030].value,
                study_instance_uid=str(dcm_obj[0x0020, 0x000D].value),
                study_date=dcm_obj[0x0008, 0x0020].value,
                station_name=dcm_obj[0x0008, 0x1010].value,
                patient_name=str(dcm_obj[0x0010, 0x0010].value),
                patient_id=dcm_obj[0x0010, 0x0020].value,
                magnetic_field_strength=str(dcm_obj[0x0018, 0x0087].value),
                pixel_array=dcm_obj.pixel_array
            )
        # If exception then the dicom object is not an image so do nothing
        except Exception as ex:
            pass

        # Don't return the empty instance
        if instance is None:
            pass
        else:
            if instance:
                return instance
