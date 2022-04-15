#!/usr/bin/python3                                                                                    


import os
import unittest
import json
import sys
import requests

from os.path import join, dirname
from dotenv import load_dotenv
from flashurlapi import app

dotenv_path = join(dirname(__file__), 'test.env')
load_dotenv(dotenv_path)
API_SERVER = os.getenv("API_SERVER", "").strip("")
API_PORT = os.getenv("API_PORT", "").strip("")
RECORDS_FILE = os.getenv("RECORDS", "").strip("")


class FlashUrlApiTest(unittest.TestCase):

    def setUp(self):
        self.payload = json.dumps({"url": "http://xyz.xyz/qwerty321"})
        self.base_url = 'http://'+str(API_SERVER)+':'+str(API_PORT)
        self.headers = {
                "accept": "application/json",
                "Content-Type": "application/json"
                }

    def tearDown(self):
        pass

    def test_response_code(self):
        '''
        Check response code
        '''
        resp = requests.post(self.base_url+'/api/v1/flash_shorten', headers=self.headers, data=self.payload)
        self.assertEqual(200, resp.status_code)

    def test_status_code(self):
        '''
        Check status_code
        '''
        resp = requests.post(self.base_url+'/api/v1/flash_shorten', headers=self.headers, data=self.payload)
        data = resp.json()
        self.assertEqual("1000", data['status_code'])

    def test_url_generation(self):
        '''
        Check short URL for same long URL
        '''
        resp = requests.post(self.base_url+'/api/v1/flash_shorten', headers=self.headers, data=self.payload)
        data1 = resp.json()
        resp = requests.post(self.base_url+'/api/v1/flash_shorten', headers=self.headers, data=self.payload)
        data2 = resp.json()
        self.assertEqual(data1, data2)


if __name__ == "__main__":
    unittest.main()
