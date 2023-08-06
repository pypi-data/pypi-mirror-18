"""
Auto generated code

"""

import json
from snapp_email.datacontract.classes import ApiIndex_1
from snapp_email.datacontract.utils import export_dict, fill


class ApiIndex_1Endpoint:
    def __init__(self, api_client):
        self.api_client = api_client
    
    def options(self, accept_type=None):
        """
        Retrieve options available for resource 'ApiIndex_1'.
        
        :param accept_type: 
        :type accept_type: str
        
        :return: 
        :rtype: ApiIndex_1
        """
        url_parameters = {
        }
        endpoint_parameters = {
        }
        endpoint = ''.format(**endpoint_parameters)
        add_headers = {
            'Content-Type': 'application/vnd.marg.bcsocial.api.index-v1.9+json',
            'Accept': 'application/vnd.marg.bcsocial.api.index-v1.9+json' if accept_type is None else accept_type,
        }
        response = self.api_client.api_call('options', endpoint, url_parameters, add_headers)
        
        return fill(ApiIndex_1, response.json())
    
    def get(self, accept_type=None):
        """
        Retrieve information about the api index.
        
        :param accept_type: 
        :type accept_type: str
        
        :return: 
        :rtype: ApiIndex_1
        """
        url_parameters = {
        }
        endpoint_parameters = {
        }
        endpoint = ''.format(**endpoint_parameters)
        add_headers = {
            'Content-Type': 'application/vnd.marg.bcsocial.api.index-v1.9+json',
            'Accept': 'application/vnd.marg.bcsocial.api.index-v1.9+json' if accept_type is None else accept_type,
        }
        response = self.api_client.api_call('get', endpoint, url_parameters, add_headers)
        
        return fill(ApiIndex_1, response.json())
