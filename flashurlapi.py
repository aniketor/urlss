#!/usr/bin/env python3

import os
import sys
import argparse
import logging
import csv
from flask import Flask
from flask_restx import Api
from flockcontext import FlockOpen
from waitress import serve
#from dotenv import load_dotenv

from src.constants import Constants
from src.shorten_service_api import api as ss_api_ns

PROG = Constants.PROG_NAME
EXIT_CODE = 0

# Initialize logging
logger = logging.getLogger(PROG)
f = logging.Formatter('$name $message', style='$')
h = logging.StreamHandler(sys.stdout)
h.setFormatter(f)
logger.addHandler(h)


app = Flask(PROG)

class FlashUrlConfigs:


    def __init__(self):
        # Set the default values
        self.flashurl_api_port = "9009"
        self.records = "records.csv"
        self.thread_count = 3


    def load_env(self):
        # Read environment variables
        port = os.getenv("API_SERVICE_PORT", "").strip()
        if port:
            self.flashurl_api_port = port

        records = os.getenv("RECORDS_FILE", "").strip()
        if records:
            self.records = records


class FlashUrlAPI:
    '''
    Main class for Flash URL API
    '''


    def __init__(self):
        self.api = Api(version='1.0', title='Flash URL API',
                       description='APIs for Flash URL shortening service.')
        self.api.add_namespace(ss_api_ns)


    def start(self, port_, tc_):
        logger.info('Starting {} -----------------'.format(PROG))
        app.config['ERROR_INCLUDE_MESSAGE'] = False
        app.config['RESTPLUS_MASK_SWAGGER'] = False
        app.logger.handlers.clear()
        self.api.init_app(app)
        serve(app, host='0.0.0.0', port=int(port_), threads=tc_)


    def stop(self):
        logger.info('End {} -----------------'.format(PROG))



if __name__ == '__main__':

    # Define sanity check methods
    def count_type(value):
        count = int(value)
        if count < 0:
            raise argparse.ArgumentTypeError("invalid count:" + count)
        return count

    def port_type(value):
        port = int(value)
        if port <= 0:
            raise argparse.ArgumentTypeError("invalid port:" + str(value))
        return port

    flashurl_api = None
    try:
        # Load configuration values
        config = FlashUrlConfigs()
        config.load_env()

        # Setup commandline parameters
        ap = argparse.ArgumentParser(description=PROG + ' parameters:',
                                     formatter_class=argparse.RawTextHelpFormatter)
        ap.add_argument("--port", metavar="PORT", type=port_type,
                        dest="flashurl_api_port", default=config.flashurl_api_port,
                        help=PROG + " port (default: %(default)s)")
        ap.add_argument("--records", metavar="FILE", #type=lambda x: is_valid_file(ap, x),
                        dest="filename", default="records.csv",
                        help="file to store records (default: %(default)s)")
        ap.add_argument("--thread-count", metavar="THREAD_COUNT", type=count_type,
                        dest="thread_count", default=config.thread_count,
                        help="number of threads to handle api request (default: %(default)s)")
        ap.add_argument("--debug", action="store_true",
                        dest="debug", default=False,
                        help="enable debug logs")


        args = ap.parse_args()


        # Override the environment variables by the arguments
        config.flashurl_api_port = args.flashurl_api_port
        config.thread_count = args.thread_count
        config.records = args.filename

        with open(config.records, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['long_url', 'short_url'])

        if args.debug:
            logger.setLevel(logging.DEBUG)
        else:
            logger.setLevel(logging.INFO)

        flashurl_api = FlashUrlAPI()
        # Acquire lock
        with FlockOpen("/tmp/" + PROG, "w"):
            flashurl_api.start(args.flashurl_api_port, config.thread_count)

    except Exception as e:
        logger.exception(e)
        EXIT_CODE = 1
    finally:
        if flashurl_api is not None:
            flashurl_api.stop()
        sys.exit(EXIT_CODE)

# End.
