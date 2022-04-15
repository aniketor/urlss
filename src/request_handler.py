#!/usr/bin/env python3

import logging
import json
import time
import os
import csv
import shutil
import pandas as pd
import src.short_url as short_url

from src.constants import Constants

logger = logging.getLogger(Constants.PROG_NAME)

RECORDS = os.getenv("RECORDS_FILE", "").strip()

class ShortSvcRequestHandler:
    '''
    Request handler to handle requests for URL shortening.
    '''

    def _check_url_in_csv(self, url_):
        df = pd.read_csv(RECORDS)
        nf = df.loc[df['long_url'] == url_]
        if not nf.empty:
            return nf['short_url'].values[0], df
        return None, df

    def _convert_url(self, url_:str) -> str:
        s_url, df = self._check_url_in_csv(url_)
        if not s_url:
            len_df = len(df)
            s_url = short_url.encode_url(len_df+1)
            with open(RECORDS, 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([url_, s_url])
        return s_url

    def _valid_url(self, url_):
        return True if url_.startswith("http://") else False

    def handle_post(self, json_data_):
        try:
            url_ = json_data_['url']
            if self._valid_url(url_):
                resp_url = self._convert_url(url_)
                status_code = "1000"
                msg = "short URL generated"
                data = f"http://127.0.0.1/{resp_url}"
            else:
                status_code = "1010"
                msg = "Check the URL"
                data = None
            return { 
                     "status_code": status_code,
                     "message": msg,
                     "data": data
                     }
        except Exception as ex:
            logger.exception("URL generation failed.")
            return { 
                     "status_code": "10100",
                     "message": f"Oops! Failed. Please try again."
                   }

# End.
