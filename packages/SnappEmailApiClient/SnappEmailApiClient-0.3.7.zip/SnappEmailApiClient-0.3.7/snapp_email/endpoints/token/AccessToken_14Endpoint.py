"""
Auto generated code

"""

import json
from snapp_email.datacontract.classes import AccessToken_14
from snapp_email.datacontract.utils import export_dict, fill


class AccessToken_14Endpoint:
    def __init__(self, api_client):
        self.api_client = api_client
    
    def options(self, accept_type=None):
        """
        Retrieve options available for resource 'AccessToken_14'.
        
        :param accept_type: 
        :type accept_type: str
        
        :return: 
        :rtype: AccessToken_14
        """
        url_parameters = {
        }
        endpoint_parameters = {
        }
        endpoint = 'token'.format(**endpoint_parameters)
        add_headers = {
            'Content-Type': 'application/vnd.4thoffice.access.token-4.0+json',
            'Accept': 'application/vnd.4thoffice.access.token-4.0+json' if accept_type is None else accept_type,
        }
        response = self.api_client.api_call('options', endpoint, url_parameters, add_headers)
        
        return fill(AccessToken_14, response.json())
    
    def create(self, obj, accessTokenScope, accept_type=None):
        """
        Refresh access token.
        
        :param obj: Object to be persisted
        :type obj: AccessToken_14
        
        :param accessTokenScope: Specify access token scope.
        :type accessTokenScope: String
        
        :param accept_type: 
        :type accept_type: str
        
        :return: 
        :rtype: AccessToken_14
        """
        url_parameters = {
            'accessTokenScope': accessTokenScope,
        }
        endpoint_parameters = {
        }
        endpoint = 'token'.format(**endpoint_parameters)
        add_headers = {
            'Content-Type': 'application/vnd.4thoffice.access.token-4.0+json',
            'Accept': 'application/vnd.4thoffice.access.token-4.0+json' if accept_type is None else accept_type,
        }
        data = export_dict(obj)
        response = self.api_client.api_call('post', endpoint, url_parameters, add_headers, data=json.dumps(data))
        
        return fill(AccessToken_14, response.json())
