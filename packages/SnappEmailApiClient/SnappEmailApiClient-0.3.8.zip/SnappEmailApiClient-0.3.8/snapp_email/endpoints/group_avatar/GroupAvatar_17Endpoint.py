"""
Auto generated code

"""

import json
from snapp_email.datacontract.classes import GroupAvatar_17
from snapp_email.datacontract.utils import export_dict, fill


class GroupAvatar_17Endpoint:
    def __init__(self, api_client):
        self.api_client = api_client
    
    def options(self, groupId, accept_type=None):
        """
        Retrieve options available for resource 'GroupAvatar_17'.
        
        :param groupId: 
        :type groupId: 
        
        :param accept_type: 
        :type accept_type: str
        
        :return: 
        :rtype: GroupAvatar_17
        """
        url_parameters = {
            'groupId': groupId,
        }
        endpoint_parameters = {
        }
        endpoint = 'group/{groupId}/avatar'.format(**endpoint_parameters)
        add_headers = {
            'Content-Type': 'application/vnd.4thoffice.group.avatar-5.3+json',
            'Accept': 'application/vnd.4thoffice.group.avatar-5.3+json' if accept_type is None else accept_type,
        }
        response = self.api_client.api_call('options', endpoint, url_parameters, add_headers)
        
        return fill(GroupAvatar_17, response.json())
    
    def get(self, groupId, accept_type=None):
        """
        Get group avatar.
        
        :param groupId: 
        :type groupId: 
        
        :param accept_type: 
        :type accept_type: str
        
        :return: 
        :rtype: GroupAvatar_17
        """
        url_parameters = {
            'groupId': groupId,
        }
        endpoint_parameters = {
        }
        endpoint = 'group/{groupId}/avatar'.format(**endpoint_parameters)
        add_headers = {
            'Content-Type': 'application/vnd.4thoffice.group.avatar-5.3+json',
            'Accept': 'application/vnd.4thoffice.group.avatar-5.3+json' if accept_type is None else accept_type,
        }
        response = self.api_client.api_call('get', endpoint, url_parameters, add_headers)
        
        return fill(GroupAvatar_17, response.json())
    
    def update(self, obj, groupId, accept_type=None):
        """
        Update group avatar.
        
        :param obj: Object to be persisted
        :type obj: GroupAvatar_17
        
        :param groupId: 
        :type groupId: 
        
        :param accept_type: 
        :type accept_type: str
        
        :return: 
        :rtype: GroupAvatar_17
        """
        url_parameters = {
            'groupId': groupId,
        }
        endpoint_parameters = {
        }
        endpoint = 'group/{groupId}/avatar'.format(**endpoint_parameters)
        add_headers = {
            'Content-Type': 'application/vnd.4thoffice.group.avatar-5.3+json',
            'Accept': 'application/vnd.4thoffice.group.avatar-5.3+json' if accept_type is None else accept_type,
        }
        data = export_dict(obj)
        response = self.api_client.api_call('put', endpoint, url_parameters, add_headers, data=json.dumps(data))
        
        return fill(GroupAvatar_17, response.json())
