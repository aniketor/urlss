#!/usr/bin/env python3

import logging
from flask_restx import Namespace

from src.constants import Constants


api = Namespace(Constants.API_NAMESPACE, description='Flash URL API')
logger = logging.getLogger(Constants.PROG_NAME)


# End.
