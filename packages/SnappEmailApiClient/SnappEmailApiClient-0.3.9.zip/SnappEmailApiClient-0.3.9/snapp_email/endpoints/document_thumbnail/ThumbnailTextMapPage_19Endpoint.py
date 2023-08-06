"""
Auto generated code

"""

import json
from snapp_email.datacontract.classes import ThumbnailTextMapPage_19
from snapp_email.datacontract.utils import export_dict, fill


class ThumbnailTextMapPage_19Endpoint:
    def __init__(self, api_client):
        self.api_client = api_client
    
    def options(self, documentId, accept_type=None):
        """
        Retrieve options available for resource 'ThumbnailTextMapPage_19'.
        
        :param documentId: 
        :type documentId: 
        
        :param accept_type: 
        :type accept_type: str
        
        :return: 
        :rtype: ThumbnailTextMapPage_19
        """
        url_parameters = {
            'documentId': documentId,
        }
        endpoint_parameters = {
        }
        endpoint = 'document/{documentId}/thumbnail'.format(**endpoint_parameters)
        add_headers = {
            'Content-Type': 'application/vnd.marg.bcsocial.thumbnail.text.map.page-v5.12+json',
            'Accept': 'application/vnd.marg.bcsocial.thumbnail.text.map.page-v5.12+json' if accept_type is None else accept_type,
        }
        response = self.api_client.api_call('options', endpoint, url_parameters, add_headers)
        
        return fill(ThumbnailTextMapPage_19, response.json())
    
    def get(self, documentId, thumbnailPage, size, offset, accept_type=None):
        """
        Retrieve document thumbnail text map.
        
        :param documentId: 
        :type documentId: 
        
        :param thumbnailPage: Specify thumbnail page.
        :type thumbnailPage: Int32
        
        :param size: Specify size of requested page.
        :type size: Int32
        
        :param offset: Specify offset of requested page.
        :type offset: Int32
        
        :param accept_type: 
        :type accept_type: str
        
        :return: 
        :rtype: ThumbnailTextMapPage_19
        """
        url_parameters = {
            'documentId': documentId,
            'thumbnailPage': thumbnailPage,
            'size': size,
            'offset': offset,
        }
        endpoint_parameters = {
        }
        endpoint = 'document/{documentId}/thumbnail'.format(**endpoint_parameters)
        add_headers = {
            'Content-Type': 'application/vnd.marg.bcsocial.thumbnail.text.map.page-v5.12+json',
            'Accept': 'application/vnd.marg.bcsocial.thumbnail.text.map.page-v5.12+json' if accept_type is None else accept_type,
        }
        response = self.api_client.api_call('get', endpoint, url_parameters, add_headers)
        
        return fill(ThumbnailTextMapPage_19, response.json())
