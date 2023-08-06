"""
Auto generated code

"""

import json
from snapp_email.datacontract.classes import UserSettingsLocationTracking_20
from snapp_email.datacontract.utils import export_dict, fill


class UserSettingsLocationTracking_20Endpoint:
    def __init__(self, api_client):
        self.api_client = api_client
    
    def options(self, accept_type=None):
        """
        Retrieve options available for resource 'UserSettingsLocationTracking_20'.
        
        :param accept_type: 
        :type accept_type: str
        
        :return: 
        :rtype: UserSettingsLocationTracking_20
        """
        url_parameters = {
        }
        endpoint_parameters = {
        }
        endpoint = 'user/settings'.format(**endpoint_parameters)
        add_headers = {
            'Content-Type': 'application/vnd.4thoffice.user.settings.location.tracking-5.15+json',
            'Accept': 'application/vnd.4thoffice.user.settings.location.tracking-5.15+json' if accept_type is None else accept_type,
        }
        response = self.api_client.api_call('options', endpoint, url_parameters, add_headers)
        
        return fill(UserSettingsLocationTracking_20, response.json())
    
    def get(self, accept_type=None):
        """
        Get user settings resource.
        
        :param accept_type: 
        :type accept_type: str
        
        :return: 
        :rtype: UserSettingsLocationTracking_20
        """
        url_parameters = {
        }
        endpoint_parameters = {
        }
        endpoint = 'user/settings'.format(**endpoint_parameters)
        add_headers = {
            'Content-Type': 'application/vnd.4thoffice.user.settings.location.tracking-5.15+json',
            'Accept': 'application/vnd.4thoffice.user.settings.location.tracking-5.15+json' if accept_type is None else accept_type,
        }
        response = self.api_client.api_call('get', endpoint, url_parameters, add_headers)
        
        return fill(UserSettingsLocationTracking_20, response.json())
