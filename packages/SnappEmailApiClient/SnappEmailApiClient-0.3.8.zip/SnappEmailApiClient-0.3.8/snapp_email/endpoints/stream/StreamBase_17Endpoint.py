"""
Auto generated code

"""

import json
from snapp_email.datacontract.classes import StreamBase_17
from snapp_email.datacontract.utils import export_dict, fill


class StreamBase_17Endpoint:
    def __init__(self, api_client):
        self.api_client = api_client
    
    def options(self, accept_type=None):
        """
        Retrieve options available for resource 'StreamBase_17'.
        
        :param accept_type: 
        :type accept_type: str
        
        :return: 
        :rtype: StreamBase_17
        """
        url_parameters = {
        }
        endpoint_parameters = {
        }
        endpoint = 'stream'.format(**endpoint_parameters)
        add_headers = {
            'Content-Type': 'application/vnd.4thoffice.stream-5.3+json',
            'Accept': 'application/vnd.4thoffice.stream-5.3+json' if accept_type is None else accept_type,
        }
        response = self.api_client.api_call('options', endpoint, url_parameters, add_headers)
        
        return fill(StreamBase_17, response.json())
    
    def get(self, streamId, size, offset, htmlFormat=None, accept_type=None):
        """
        Get stream resource.
        
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
        
        :param accept_type: 
        :type accept_type: str
        
        :return: 
        :rtype: StreamBase_17
        """
        url_parameters = {
            'htmlFormat': htmlFormat,
            'size': size,
            'offset': offset,
        }
        endpoint_parameters = {
            'streamId': streamId,
        }
        endpoint = 'stream/{streamId}'.format(**endpoint_parameters)
        add_headers = {
            'Content-Type': 'application/vnd.4thoffice.stream-5.3+json',
            'Accept': 'application/vnd.4thoffice.stream-5.3+json' if accept_type is None else accept_type,
        }
        response = self.api_client.api_call('get', endpoint, url_parameters, add_headers)
        
        return fill(StreamBase_17, response.json())
