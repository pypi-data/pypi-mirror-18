
import logging
logger = logging.getLogger('agiletix')

try:
    from urllib import parse
except ImportError:
    import urlparse as parse

import json
import re
import slumber
import time

from collections import namedtuple

from .exceptions import ImproperlyConfigured
from .utils import *


DEFAULT_AGILE_RESPONSE_FORMAT = 'json'
DEFAULT_AGILE_DATE_FORMAT = '%Y-%m-%dT%H:%M:%S'

# A struct to hold Agile error codes
ERROR_CODES = {
    'MemberNotFound': 1022,
    'MemberNotValid': 1025, 
    'MemberExpired': 1023,
    'MemberRenewalRequired': 1024,
    'OnlineAccountRequired': 1026,
    'InvalidLogin': 1027, 
}

AgileErrorStruct = namedtuple('AgileErrorStruct', ' '.join(ERROR_CODES.keys()))
AgileError = AgileErrorStruct(**ERROR_CODES)

# A struct to hold API response error code and message
APIResponseErrorStruct = namedtuple('APIResponseErrorStruct', 'code message')


class APIResponse(object):
    """A class representing a respone from the API. 

    Attributes:
        data (dict): The json response
        error (tuple): A named tuple containg error code and message 
        success (bool): Returns True if the request was successful

    """

    error = None
    data = None

    def __init__(self, data, *args, **kwargs):
        # If an error occurs, 'Code' will be in the response dict
        if isinstance(data, dict) and 'Code' in data:
            self.error = APIResponseErrorStruct(code=data['Code'], message=data.get('Message'))
        else:
            self.data = data

    @property 
    def success(self):
        return (not self.error)


class BaseAgileAPI(object):
    """Base class for Agile API interfaces 

    """

    def __init__(
            self, 
            base_url,
            app_key,
            user_key,
            corp_org_id,
            response_format=None,
            service_type=None, 
        ):

        self.base_url = base_url
        self.app_key = app_key
        self.user_key = user_key
        self.corp_org_id = corp_org_id

        if not service_type:
            service_type = self.SERVICE_TYPE
            if not service_type:
                raise ImproperlyConfigured("service_type is required")
        if not response_format: 
            response_format = DEFAULT_AGILE_RESPONSE_FORMAT

        base_url = parse.urljoin(base_url, '{0}.svc/{1}'.format(service_type, response_format))
        self.api = slumber.API(base_url=base_url, format='json', append_slash=False)

    def get_base_kwargs(self):
        return {
            'appKey': self.app_key,
            'userKey': self.user_key, 
            'corpOrgID': self.corp_org_id, 
            }

    def _make_request(self, request_type, name=None, **kwargs):
        cleaned_kwargs = {}
        for key, value in kwargs.items():
            if value:
                cleaned_kwargs[to_pascal_case(key)] = value
        kwargs =  merge_two_dicts(self.get_base_kwargs(), cleaned_kwargs)
        empty_value_keys = []
        for key, value in kwargs.items():
            if not value: empty_value_keys.append(key)
        for key in empty_value_keys:
            kwargs.pop(key, None)
        response = None
        data = None

        retry_max = 5
        retry_sleep = 2
        retry = True
        
        i = 0

        while retry:
            retry = False
            try:
                data = getattr(
                    getattr(
                        self.api, 
                        name
                    )(),
                    request_type.lower()
                    )(**kwargs)
                response = APIResponse(data)
            except slumber.exceptions.HttpNotFoundError:
                logger.error("HttpNotFoundError: {0}".format(data))
            except slumber.exceptions.HttpClientError:
                logger.error("HttpClientError: {0}".format(data))
            except slumber.exceptions.HttpServerError:
                logger.error("HttpServerError: {0}".format(data))
                retry = True
            except:
                logger.error("HttpUknownError: {0}".format(data))
                retry = True

            if retry:
                i += 1
                if i < retry_max:
                    retry = True
                    time.sleep(retry_sleep)
                else:
                    retry = False

        return response


