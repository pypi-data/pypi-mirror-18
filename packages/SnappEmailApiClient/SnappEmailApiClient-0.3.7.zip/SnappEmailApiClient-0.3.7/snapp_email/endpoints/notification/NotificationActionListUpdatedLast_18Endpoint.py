"""
Auto generated code

"""

import json
from snapp_email.datacontract.classes import NotificationActionListUpdatedLast_18
from snapp_email.datacontract.utils import export_dict, fill


class NotificationActionListUpdatedLast_18Endpoint:
    def __init__(self, api_client):
        self.api_client = api_client
    
    def options(self, accept_type=None):
        """
        Retrieve options available for resource 'NotificationActionListUpdatedLast_18'.
        
        :param accept_type: 
        :type accept_type: str
        
        :return: 
        :rtype: NotificationActionListUpdatedLast_18
        """
        url_parameters = {
        }
        endpoint_parameters = {
        }
        endpoint = 'notification'.format(**endpoint_parameters)
        add_headers = {
            'Content-Type': 'application/vnd.4thoffice.notification.action.list.updated.last-v5.8+json',
            'Accept': 'application/vnd.4thoffice.notification.action.list.updated.last-v5.8+json' if accept_type is None else accept_type,
        }
        response = self.api_client.api_call('options', endpoint, url_parameters, add_headers)
        
        return fill(NotificationActionListUpdatedLast_18, response.json())
    
    def get(self, accept_type=None):
        """
        Get last notification about updated action list.
        
        :param accept_type: 
        :type accept_type: str
        
        :return: 
        :rtype: NotificationActionListUpdatedLast_18
        """
        url_parameters = {
        }
        endpoint_parameters = {
        }
        endpoint = 'notification'.format(**endpoint_parameters)
        add_headers = {
            'Content-Type': 'application/vnd.4thoffice.notification.action.list.updated.last-v5.8+json',
            'Accept': 'application/vnd.4thoffice.notification.action.list.updated.last-v5.8+json' if accept_type is None else accept_type,
        }
        response = self.api_client.api_call('get', endpoint, url_parameters, add_headers)
        
        return fill(NotificationActionListUpdatedLast_18, response.json())
