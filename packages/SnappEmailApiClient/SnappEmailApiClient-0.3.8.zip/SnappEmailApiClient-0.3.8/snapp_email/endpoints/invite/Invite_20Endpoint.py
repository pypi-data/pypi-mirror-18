"""
Auto generated code

"""

import json
from snapp_email.datacontract.classes import Invite_20
from snapp_email.datacontract.utils import export_dict, fill


class Invite_20Endpoint:
    def __init__(self, api_client):
        self.api_client = api_client
    
    def options(self, accept_type=None):
        """
        Retrieve options available for resource 'Invite_20'.
        
        :param accept_type: 
        :type accept_type: str
        
        :return: 
        :rtype: Invite_20
        """
        url_parameters = {
        }
        endpoint_parameters = {
        }
        endpoint = 'invite'.format(**endpoint_parameters)
        add_headers = {
            'Content-Type': 'application/vnd.4thoffice.invite-5.15+json',
            'Accept': 'application/vnd.4thoffice.invite-5.15+json' if accept_type is None else accept_type,
        }
        response = self.api_client.api_call('options', endpoint, url_parameters, add_headers)
        
        return fill(Invite_20, response.json())
    
    def get(self, accept_type=None):
        """
        Retrieve invite template resource.
        
        :param accept_type: 
        :type accept_type: str
        
        :return: 
        :rtype: Invite_20
        """
        url_parameters = {
        }
        endpoint_parameters = {
        }
        endpoint = 'invite'.format(**endpoint_parameters)
        add_headers = {
            'Content-Type': 'application/vnd.4thoffice.invite-5.15+json',
            'Accept': 'application/vnd.4thoffice.invite-5.15+json' if accept_type is None else accept_type,
        }
        response = self.api_client.api_call('get', endpoint, url_parameters, add_headers)
        
        return fill(Invite_20, response.json())
