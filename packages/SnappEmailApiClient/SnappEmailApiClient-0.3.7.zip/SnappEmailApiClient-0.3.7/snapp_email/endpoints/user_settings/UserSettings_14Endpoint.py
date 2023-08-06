"""
Auto generated code

"""

import json
from snapp_email.datacontract.classes import UserSettings_14
from snapp_email.datacontract.utils import export_dict, fill


class UserSettings_14Endpoint:
    def __init__(self, api_client):
        self.api_client = api_client
    
    def options(self, accept_type=None):
        """
        Retrieve options available for resource 'UserSettings_14'.
        
        :param accept_type: 
        :type accept_type: str
        
        :return: 
        :rtype: UserSettings_14
        """
        url_parameters = {
        }
        endpoint_parameters = {
        }
        endpoint = 'user/settings'.format(**endpoint_parameters)
        add_headers = {
            'Content-Type': 'application/vnd.4thoffice.user.settings-4.0+json',
            'Accept': 'application/vnd.4thoffice.user.settings-4.0+json' if accept_type is None else accept_type,
        }
        response = self.api_client.api_call('options', endpoint, url_parameters, add_headers)
        
        return fill(UserSettings_14, response.json())
    
    def get(self, accept_type=None):
        """
        Get user settings resource.
        
        :param accept_type: 
        :type accept_type: str
        
        :return: 
        :rtype: UserSettings_14
        """
        url_parameters = {
        }
        endpoint_parameters = {
        }
        endpoint = 'user/settings'.format(**endpoint_parameters)
        add_headers = {
            'Content-Type': 'application/vnd.4thoffice.user.settings-4.0+json',
            'Accept': 'application/vnd.4thoffice.user.settings-4.0+json' if accept_type is None else accept_type,
        }
        response = self.api_client.api_call('get', endpoint, url_parameters, add_headers)
        
        return fill(UserSettings_14, response.json())
    
    def update(self, obj, accept_type=None):
        """
        Update user settings resource.
        
        :param obj: Object to be persisted
        :type obj: UserSettings_14
        
        :param accept_type: 
        :type accept_type: str
        
        :return: 
        :rtype: UserSettings_14
        """
        url_parameters = {
        }
        endpoint_parameters = {
        }
        endpoint = 'user/settings'.format(**endpoint_parameters)
        add_headers = {
            'Content-Type': 'application/vnd.4thoffice.user.settings-4.0+json',
            'Accept': 'application/vnd.4thoffice.user.settings-4.0+json' if accept_type is None else accept_type,
        }
        data = export_dict(obj)
        response = self.api_client.api_call('put', endpoint, url_parameters, add_headers, data=json.dumps(data))
        
        return fill(UserSettings_14, response.json())
