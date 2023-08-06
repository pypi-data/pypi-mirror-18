"""
Auto generated code

"""

import json
from snapp_email.datacontract.classes import StreamCards_22
from snapp_email.datacontract.utils import export_dict, fill


class StreamCards_22Endpoint:
    def __init__(self, api_client):
        self.api_client = api_client
    
    def options(self, accept_type=None):
        """
        Retrieve options available for resource 'StreamCards_22'.
        
        :param accept_type: 
        :type accept_type: str
        
        :return: 
        :rtype: StreamCards_22
        """
        url_parameters = {
        }
        endpoint_parameters = {
        }
        endpoint = 'stream'.format(**endpoint_parameters)
        add_headers = {
            'Content-Type': 'application/vnd.4thoffice.stream.cards-5.18+json',
            'Accept': 'application/vnd.4thoffice.stream.cards-5.18+json' if accept_type is None else accept_type,
        }
        response = self.api_client.api_call('options', endpoint, url_parameters, add_headers)
        
        return fill(StreamCards_22, response.json())
    
    def get(self, streamId, size, offset, htmlFormat=None, unreadFirst=None, unreadOnly=None, loadUnread=None, returnForwardedCopyPosts=None, accept_type=None):
        """
        Get stream cards.
        
        :param streamId: 
        :type streamId: 
        
        :param size: Specify size of requested page.
        :type size: Int32
        
        :param offset: Specify offset of requested page.
        :type offset: Int32
        
        :param htmlFormat: Mime format for html body of post resource.
            Available values:
            - text/html-stripped
            - text/html-stripped.mobile
        :type htmlFormat: String
        
        :param unreadFirst: Load unread discussion cards first.
        :type unreadFirst: Int32
        
        :param unreadOnly: Load unread discussion cards only.
        :type unreadOnly: Int32
        
        :param loadUnread: Count of unread items that should get loaded per each card.
        :type loadUnread: Int32
        
        :param returnForwardedCopyPosts: Return copied posts on forwarded discussion card.
        :type returnForwardedCopyPosts: Boolean
        
        :param accept_type: 
        :type accept_type: str
        
        :return: 
        :rtype: StreamCards_22
        """
        url_parameters = {
            'htmlFormat': htmlFormat,
            'unreadFirst': unreadFirst,
            'unreadOnly': unreadOnly,
            'loadUnread': loadUnread,
            'returnForwardedCopyPosts': returnForwardedCopyPosts,
            'size': size,
            'offset': offset,
        }
        endpoint_parameters = {
            'streamId': streamId,
        }
        endpoint = 'stream/{streamId}'.format(**endpoint_parameters)
        add_headers = {
            'Content-Type': 'application/vnd.4thoffice.stream.cards-5.18+json',
            'Accept': 'application/vnd.4thoffice.stream.cards-5.18+json' if accept_type is None else accept_type,
        }
        response = self.api_client.api_call('get', endpoint, url_parameters, add_headers)
        
        return fill(StreamCards_22, response.json())
