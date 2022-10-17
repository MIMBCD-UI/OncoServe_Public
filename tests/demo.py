import json
import requests
import unittest
import pdb
import os, shutil
from os.path import dirname, realpath
import sys
import pathlib
import csv
sys.path.append(dirname(dirname(realpath(__file__))))
import oncoserve.aggregators.basic as aggregators

DOMAIN = "http://oncoserver:5000"

class Test_MIT_App(unittest.TestCase):

    def setUp(self):
        
        self.files = []
        Path = "dataset/"
        filelist = [f for f in os.listdir(Path) if '.dcm' in f]

        # Open all the files in the dataset
        for file in filelist:

            # Add the files to the list
            self.files.append(open(Path + file, 'rb'))

            # Fake MRN
            self.MRN = '11111111'
            
            # Fake Accession
            self.ACCESSION = '2222222'
            self.METADATA = {'mrn':self.MRN, 'accession': self.ACCESSION}

    def tearDown(self):

        # Try to close all the files
        for file in self.files:
            try:
                file.close()
            except Exception as e:
                pass

    def test_normal_request(self):
        '''
        Demo of how to use MIRAI. Note, this is applicable for all MIRAI applications.
        '''

        fileTabular = open('densenties/demo.csv', 'w')

        '''
         1. Load dicoms. Make sure to filter by view, MIRAI will not take responsibility for this.
        '''

        for file in self.files:

            '''
            2. Send request to model at /serve with dicoms in files field, and any metadata in the data field.
            Note, files should contain a list of tuples:
            [ ('dicom': bytes), '(dicom': bytes)', ('dicom': bytes) ].
            Deviating from this may result in unexpected behavior.
            '''
            r = requests.post(os.path.join(DOMAIN,"serve"), files=[('dicom', file)], data=self.METADATA)
            
            '''
            3. Results will contain prediction, status, version info, all original metadata
            '''
            rquestObject = r.__dict__
            print(rquestObject)
            print(file)
            writer = csv.writer(fileTabular)
            dataTabular = [file, rquestObject]
            writer.writerow(dataTabular)

            self.assertEqual(r.status_code, 200)
            content = json.loads(r.content)
            self.assertEqual(content['metadata']['mrn'], self.MRN)
            self.assertEqual(content['metadata']['accession'], self.ACCESSION)

            file.close()

if __name__ == '__main__':
    unittest.main()
