"""
Auto generated code

"""

import json
from snapp_email.datacontract.classes import DiscussionSeparatorUnread_18
from snapp_email.datacontract.utils import export_dict, fill


class DiscussionSeparatorUnread_18Endpoint:
    def __init__(self, api_client):
        self.api_client = api_client
    
    def options(self, accept_type=None):
        """
        Retrieve options available for resource 'DiscussionSeparatorUnread_18'.
        
        :param accept_type: 
        :type accept_type: str
        
        :return: 
        :rtype: DiscussionSeparatorUnread_18
        """
        url_parameters = {
        }
        endpoint_parameters = {
        }
        endpoint = 'feed'.format(**endpoint_parameters)
        add_headers = {
            'Content-Type': 'application/vnd.4thoffice.discussion.separator.unread-5.8+json',
            'Accept': 'application/vnd.4thoffice.discussion.separator.unread-5.8+json' if accept_type is None else accept_type,
        }
        response = self.api_client.api_call('options', endpoint, url_parameters, add_headers)
        
        return fill(DiscussionSeparatorUnread_18, response.json())
    
    def delete(self, feedscope, feedidentity, accept_type=None):
        """
        Clear unread separator
        
        :param feedscope: Specify feed scope.
            Available values:
            - Stream
        :type feedscope: String
        
        :param feedidentity: Specify feed id.
        :type feedidentity: String
        
        :param accept_type: 
        :type accept_type: str
        
        :return: 
        :rtype: DiscussionSeparatorUnread_18
        """
        url_parameters = {
            'feedscope': feedscope,
            'feedidentity': feedidentity,
        }
        endpoint_parameters = {
        }
        endpoint = 'feed'.format(**endpoint_parameters)
        add_headers = {
            'Content-Type': 'application/vnd.4thoffice.discussion.separator.unread-5.8+json',
            'Accept': 'application/vnd.4thoffice.discussion.separator.unread-5.8+json' if accept_type is None else accept_type,
        }
        response = self.api_client.api_call('delete', endpoint, url_parameters, add_headers)
        
        return fill(DiscussionSeparatorUnread_18, response.json())
