"""
Auto generated code

"""

import json
from snapp_email.datacontract.classes import UserAvatar_17
from snapp_email.datacontract.utils import export_dict, fill


class UserAvatar_17Endpoint:
    def __init__(self, api_client):
        self.api_client = api_client
    
    def options(self, userId, accept_type=None):
        """
        Retrieve options available for resource 'UserAvatar_17'.
        
        :param userId: 
        :type userId: 
        
        :param accept_type: 
        :type accept_type: str
        
        :return: 
        :rtype: UserAvatar_17
        """
        url_parameters = {
            'userId': userId,
        }
        endpoint_parameters = {
        }
        endpoint = 'user/{userId}/avatar'.format(**endpoint_parameters)
        add_headers = {
            'Content-Type': 'application/vnd.4thoffice.user.avatar-5.3+json',
            'Accept': 'application/vnd.4thoffice.user.avatar-5.3+json' if accept_type is None else accept_type,
        }
        response = self.api_client.api_call('options', endpoint, url_parameters, add_headers)
        
        return fill(UserAvatar_17, response.json())
    
    def get(self, userId, accept_type=None):
        """
        Get user avatar.
        
        :param userId: 
        :type userId: 
        
        :param accept_type: 
        :type accept_type: str
        
        :return: 
        :rtype: UserAvatar_17
        """
        url_parameters = {
            'userId': userId,
        }
        endpoint_parameters = {
        }
        endpoint = 'user/{userId}/avatar'.format(**endpoint_parameters)
        add_headers = {
            'Content-Type': 'application/vnd.4thoffice.user.avatar-5.3+json',
            'Accept': 'application/vnd.4thoffice.user.avatar-5.3+json' if accept_type is None else accept_type,
        }
        response = self.api_client.api_call('get', endpoint, url_parameters, add_headers)
        
        return fill(UserAvatar_17, response.json())
    
    def update(self, obj, userId, accept_type=None):
        """
        Update user avatar.
        
        :param obj: Object to be persisted
        :type obj: UserAvatar_17
        
        :param userId: 
        :type userId: 
        
        :param accept_type: 
        :type accept_type: str
        
        :return: 
        :rtype: UserAvatar_17
        """
        url_parameters = {
            'userId': userId,
        }
        endpoint_parameters = {
        }
        endpoint = 'user/{userId}/avatar'.format(**endpoint_parameters)
        add_headers = {
            'Content-Type': 'application/vnd.4thoffice.user.avatar-5.3+json',
            'Accept': 'application/vnd.4thoffice.user.avatar-5.3+json' if accept_type is None else accept_type,
        }
        data = export_dict(obj)
        response = self.api_client.api_call('put', endpoint, url_parameters, add_headers, data=json.dumps(data))
        
        return fill(UserAvatar_17, response.json())
