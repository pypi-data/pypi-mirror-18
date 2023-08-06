"""
Auto generated code

"""

import json
from snapp_email.datacontract.classes import Campaign_12
from snapp_email.datacontract.utils import export_dict, fill


class Campaign_12Endpoint:
    def __init__(self, api_client):
        self.api_client = api_client
    
    def options(self, accept_type=None):
        """
        Retrieve options available for resource 'Campaign_12'.
        
        :param accept_type: 
        :type accept_type: str
        
        :return: 
        :rtype: Campaign_12
        """
        url_parameters = {
        }
        endpoint_parameters = {
        }
        endpoint = 'user/campaign'.format(**endpoint_parameters)
        add_headers = {
            'Content-Type': 'application/vnd.marg.bcsocial.campaign-3.5+json',
            'Accept': 'application/vnd.marg.bcsocial.campaign-3.5+json' if accept_type is None else accept_type,
        }
        response = self.api_client.api_call('options', endpoint, url_parameters, add_headers)
        
        return fill(Campaign_12, response.json())
    
    def create(self, obj, accept_type=None):
        """
        Log campaign info
        
        :param obj: Object to be persisted
        :type obj: Campaign_12
        
        :param accept_type: 
        :type accept_type: str
        
        :return: 
        :rtype: Campaign_12
        """
        url_parameters = {
        }
        endpoint_parameters = {
        }
        endpoint = 'user/campaign'.format(**endpoint_parameters)
        add_headers = {
            'Content-Type': 'application/vnd.marg.bcsocial.campaign-3.5+json',
            'Accept': 'application/vnd.marg.bcsocial.campaign-3.5+json' if accept_type is None else accept_type,
        }
        data = export_dict(obj)
        response = self.api_client.api_call('post', endpoint, url_parameters, add_headers, data=json.dumps(data))
        
        return fill(Campaign_12, response.json())
