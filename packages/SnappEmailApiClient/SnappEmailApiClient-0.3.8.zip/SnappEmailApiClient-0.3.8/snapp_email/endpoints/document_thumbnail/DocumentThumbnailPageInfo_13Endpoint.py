"""
Auto generated code

"""

import json
from snapp_email.datacontract.classes import DocumentThumbnailPageInfo_13
from snapp_email.datacontract.utils import export_dict, fill


class DocumentThumbnailPageInfo_13Endpoint:
    def __init__(self, api_client):
        self.api_client = api_client
    
    def options(self, documentId, accept_type=None):
        """
        Retrieve options available for resource 'DocumentThumbnailPageInfo_13'.
        
        :param documentId: 
        :type documentId: 
        
        :param accept_type: 
        :type accept_type: str
        
        :return: 
        :rtype: DocumentThumbnailPageInfo_13
        """
        url_parameters = {
            'documentId': documentId,
        }
        endpoint_parameters = {
        }
        endpoint = 'document/{documentId}/thumbnail'.format(**endpoint_parameters)
        add_headers = {
            'Content-Type': 'application/vnd.marg.bcsocial.document.thumbnail.page.info-v3.6+json',
            'Accept': 'application/vnd.marg.bcsocial.document.thumbnail.page.info-v3.6+json' if accept_type is None else accept_type,
        }
        response = self.api_client.api_call('options', endpoint, url_parameters, add_headers)
        
        return fill(DocumentThumbnailPageInfo_13, response.json())
    
    def get(self, documentId, thumbnailSize, thumbnailPage=None, accept_type=None):
        """
        Retrieve document thumbnail page info.
        
        :param documentId: 
        :type documentId: 
        
        :param thumbnailSize: Specify thumbnail size. Available values are: 'Small', 'Medium' and 'Large'.
        :type thumbnailSize: ThumbnailSize
        
        :param thumbnailPage: Specify thumbnail page.
        :type thumbnailPage: Int32
        
        :param accept_type: 
        :type accept_type: str
        
        :return: 
        :rtype: DocumentThumbnailPageInfo_13
        """
        url_parameters = {
            'documentId': documentId,
            'thumbnailSize': thumbnailSize,
            'thumbnailPage': thumbnailPage,
        }
        endpoint_parameters = {
        }
        endpoint = 'document/{documentId}/thumbnail'.format(**endpoint_parameters)
        add_headers = {
            'Content-Type': 'application/vnd.marg.bcsocial.document.thumbnail.page.info-v3.6+json',
            'Accept': 'application/vnd.marg.bcsocial.document.thumbnail.page.info-v3.6+json' if accept_type is None else accept_type,
        }
        response = self.api_client.api_call('get', endpoint, url_parameters, add_headers)
        
        return fill(DocumentThumbnailPageInfo_13, response.json())
