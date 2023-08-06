"""
Auto generated code

"""

import json
from snapp_email.datacontract.classes import LocalizedResult_1
from snapp_email.datacontract.utils import export_dict, fill


class LocalizedResult_1Endpoint:
    def __init__(self, api_client):
        self.api_client = api_client
    
    def options(self, accept_type=None):
        """
        Retrieve options available for resource 'LocalizedResult_1'.
        
        :param accept_type: 
        :type accept_type: str
        
        :return: 
        :rtype: LocalizedResult_1
        """
        url_parameters = {
        }
        endpoint_parameters = {
        }
        endpoint = ''.format(**endpoint_parameters)
        add_headers = {
            'Content-Type': 'application/vnd.marg.bcsocial.result.localized-v2.6+json',
            'Accept': 'application/vnd.marg.bcsocial.result.localized-v2.6+json' if accept_type is None else accept_type,
        }
        response = self.api_client.api_call('options', endpoint, url_parameters, add_headers)
        
        return fill(LocalizedResult_1, response.json())
