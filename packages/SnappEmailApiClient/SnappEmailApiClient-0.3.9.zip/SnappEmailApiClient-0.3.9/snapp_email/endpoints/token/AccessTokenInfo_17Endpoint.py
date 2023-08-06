"""
Auto generated code

"""

import json
from snapp_email.datacontract.classes import AccessTokenInfo_17
from snapp_email.datacontract.utils import export_dict, fill


class AccessTokenInfo_17Endpoint:
    def __init__(self, api_client):
        self.api_client = api_client
    
    def options(self, accept_type=None):
        """
        Retrieve options available for resource 'AccessTokenInfo_17'.
        
        :param accept_type: 
        :type accept_type: str
        
        :return: 
        :rtype: AccessTokenInfo_17
        """
        url_parameters = {
        }
        endpoint_parameters = {
        }
        endpoint = 'token'.format(**endpoint_parameters)
        add_headers = {
            'Content-Type': 'application/vnd.4thoffice.access.token.info-5.3+json',
            'Accept': 'application/vnd.4thoffice.access.token.info-5.3+json' if accept_type is None else accept_type,
        }
        response = self.api_client.api_call('options', endpoint, url_parameters, add_headers)
        
        return fill(AccessTokenInfo_17, response.json())
    
    def get(self, accessToken, accept_type=None):
        """
        Get user settings resource.
        
        :param accessToken: Specify access token.
        :type accessToken: String
        
        :param accept_type: 
        :type accept_type: str
        
        :return: 
        :rtype: AccessTokenInfo_17
        """
        url_parameters = {
            'accessToken': accessToken,
        }
        endpoint_parameters = {
        }
        endpoint = 'token'.format(**endpoint_parameters)
        add_headers = {
            'Content-Type': 'application/vnd.4thoffice.access.token.info-5.3+json',
            'Accept': 'application/vnd.4thoffice.access.token.info-5.3+json' if accept_type is None else accept_type,
        }
        response = self.api_client.api_call('get', endpoint, url_parameters, add_headers)
        
        return fill(AccessTokenInfo_17, response.json())
