"""
Auto generated code

"""

import json
from snapp_email.datacontract.classes import MenuItem_21
from snapp_email.datacontract.utils import export_dict, fill


class MenuItem_21Endpoint:
    def __init__(self, api_client):
        self.api_client = api_client
    
    def options(self, accept_type=None):
        """
        Retrieve options available for resource 'MenuItem_20'.
        
        :param accept_type: 
        :type accept_type: str
        
        :return: 
        :rtype: MenuItem_21
        """
        url_parameters = {
        }
        endpoint_parameters = {
        }
        endpoint = 'navigation'.format(**endpoint_parameters)
        add_headers = {
            'Content-Type': 'application/vnd.4thoffice.menu.item-v5.17+json',
            'Accept': 'application/vnd.4thoffice.menu.item-v5.17+json' if accept_type is None else accept_type,
        }
        response = self.api_client.api_call('options', endpoint, url_parameters, add_headers)
        
        return fill(MenuItem_21, response.json())
    
    def get(self, streamId, badgeUnreadVersion=None, accept_type=None):
        """
        Get menu item.
        
        :param streamId: 
        :type streamId: 
        
        :param badgeUnreadVersion: Version string that defines which logic to use for setting of unread badge count value on menu items and unread separator on feed. Available values are: 'V18', 'V19'.
        :type badgeUnreadVersion: Int32
        
        :param accept_type: 
        :type accept_type: str
        
        :return: 
        :rtype: MenuItem_21
        """
        url_parameters = {
            'badgeUnreadVersion': badgeUnreadVersion,
        }
        endpoint_parameters = {
            'streamId': streamId,
        }
        endpoint = 'navigation/{streamId}'.format(**endpoint_parameters)
        add_headers = {
            'Content-Type': 'application/vnd.4thoffice.menu.item-v5.17+json',
            'Accept': 'application/vnd.4thoffice.menu.item-v5.17+json' if accept_type is None else accept_type,
        }
        response = self.api_client.api_call('get', endpoint, url_parameters, add_headers)
        
        return fill(MenuItem_21, response.json())
