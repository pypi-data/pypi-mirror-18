"""
Auto generated code

"""

import json
from snapp_email.datacontract.classes import StreamBase_22
from snapp_email.datacontract.utils import export_dict, fill


class StreamBase_22Endpoint:
    def __init__(self, api_client):
        self.api_client = api_client
    
    def options(self, accept_type=None):
        """
        Retrieve options available for resource 'StreamBase_22'.
        
        :param accept_type: 
        :type accept_type: str
        
        :return: 
        :rtype: StreamBase_22
        """
        url_parameters = {
        }
        endpoint_parameters = {
        }
        endpoint = 'stream'.format(**endpoint_parameters)
        add_headers = {
            'Content-Type': 'application/vnd.4thoffice.stream.base-5.18+json',
            'Accept': 'application/vnd.4thoffice.stream.base-5.18+json' if accept_type is None else accept_type,
        }
        response = self.api_client.api_call('options', endpoint, url_parameters, add_headers)
        
        return fill(StreamBase_22, response.json())
    
    def get(self, streamId, accept_type=None):
        """
        Get stream resource.
        
        :param streamId: 
        :type streamId: 
        
        :param accept_type: 
        :type accept_type: str
        
        :return: 
        :rtype: StreamBase_22
        """
        url_parameters = {
        }
        endpoint_parameters = {
            'streamId': streamId,
        }
        endpoint = 'stream/{streamId}'.format(**endpoint_parameters)
        add_headers = {
            'Content-Type': 'application/vnd.4thoffice.stream.base-5.18+json',
            'Accept': 'application/vnd.4thoffice.stream.base-5.18+json' if accept_type is None else accept_type,
        }
        response = self.api_client.api_call('get', endpoint, url_parameters, add_headers)
        
        return fill(StreamBase_22, response.json())
