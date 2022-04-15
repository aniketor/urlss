#!/usr/bin/env python3

import logging
import flask
import time
from flask_restx import fields, Resource

from src.api_namespace import api
from src.constants import Constants
from src.request_handler import ShortSvcRequestHandler


#shorten_get_resp_model = api.model('Shorten service API Get Response', {
#    'status_code': fields.String(required=True, description='Status Code'),
#    'message': fields.String(required=True, description='Status Code'),
#    'data': fields.Raw(required=True, description='Json data')
#})

shorten_update_resp_model = api.model('Shorten Service Response (Put, Post)', {
    'status_code': fields.String(required=True, description='Status Code'),
    'message': fields.String(required=True, description='Status Message'),
    'data': fields.String(required=True, description='Short URL'),
})

shorten_post_req_model = api.model('Generate short URL', {                                                                                                                              
    'url': fields.String(required=True, description='Long URL'),
})


logger = logging.getLogger(Constants.PROG_NAME)

@api.route('/flash_shorten')
@api.header('X-Frame-Options', 'sameorigin')
@api.header('X-XSS-Protection', '1; mode=block')
@api.header('Cache-Control', 'no-cache')
class ShortenSvcAPI(Resource):
    '''Shorten service API'''


    def __init__(self, api_):
        self.api = api_
        self._handler = ShortSvcRequestHandler()


    #@api.marshal_with(shorten_get_resp_model)
    #def get(self, shorturl_):
    #    '''
    #    Get long URL
    #    '''
    #    start_time = time.time()
    #    logger.debug(self.__class__.__name__ + ".get() for long URL")
    #    req_params =  flask.request.args
    #    response = self._handler.handle_get(api.payload)
    #    logger.debug("{} > {} > Elapsed: {}".format(flask.request.method, flask.request.url, (time.time() - start_time)))
    #    return response


    @api.marshal_with(shorten_update_resp_model)
    @api.expect(shorten_post_req_model)
    def post(self):
        '''
        Generate and return shortened URL
        '''
        start_time = time.time()
        logger.debug(self.__class__.__name__ + ".post() for generate short URL")
        #self._handler._validate_payload(api.payload, logs_gen_req_model)
        response = self._handler.handle_post(api.payload)
        logger.info("{} > {} > Elapsed: {}".format(flask.request.method, flask.request.url, (time.time() - start_time)))
        return response

# End.
