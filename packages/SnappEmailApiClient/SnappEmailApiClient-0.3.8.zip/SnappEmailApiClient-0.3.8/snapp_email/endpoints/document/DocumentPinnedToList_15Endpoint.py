"""
Auto generated code

"""

import json
from snapp_email.datacontract.classes import DocumentPinnedToList_15
from snapp_email.datacontract.utils import export_dict, fill


class DocumentPinnedToList_15Endpoint:
    def __init__(self, api_client):
        self.api_client = api_client
    
    def options(self, accept_type=None):
        """
        Retrieve options available for resource 'DocumentPinnedToList_15'.
        
        :param accept_type: 
        :type accept_type: str
        
        :return: 
        :rtype: DocumentPinnedToList_15
        """
        url_parameters = {
        }
        endpoint_parameters = {
        }
        endpoint = 'document'.format(**endpoint_parameters)
        add_headers = {
            'Content-Type': 'application/vnd.4thoffice.document.pinnedto.list-v5.0+json',
            'Accept': 'application/vnd.4thoffice.document.pinnedto.list-v5.0+json' if accept_type is None else accept_type,
        }
        response = self.api_client.api_call('options', endpoint, url_parameters, add_headers)
        
        return fill(DocumentPinnedToList_15, response.json())
    
    def get(self, documentId, accept_type=None):
        """
        Retrieve document pinned-to list.
        
        :param documentId: 
        :type documentId: 
        
        :param accept_type: 
        :type accept_type: str
        
        :return: 
        :rtype: DocumentPinnedToList_15
        """
        url_parameters = {
        }
        endpoint_parameters = {
            'documentId': documentId,
        }
        endpoint = 'document/{documentId}'.format(**endpoint_parameters)
        add_headers = {
            'Content-Type': 'application/vnd.4thoffice.document.pinnedto.list-v5.0+json',
            'Accept': 'application/vnd.4thoffice.document.pinnedto.list-v5.0+json' if accept_type is None else accept_type,
        }
        response = self.api_client.api_call('get', endpoint, url_parameters, add_headers)
        
        return fill(DocumentPinnedToList_15, response.json())
    
    def update(self, obj, documentId, accept_type=None):
        """
        Update document pinned-to list.
        
        :param obj: Object to be persisted
        :type obj: DocumentPinnedToList_15
        
        :param documentId: 
        :type documentId: 
        
        :param accept_type: 
        :type accept_type: str
        
        :return: 
        :rtype: DocumentPinnedToList_15
        """
        url_parameters = {
        }
        endpoint_parameters = {
            'documentId': documentId,
        }
        endpoint = 'document/{documentId}'.format(**endpoint_parameters)
        add_headers = {
            'Content-Type': 'application/vnd.4thoffice.document.pinnedto.list-v5.0+json',
            'Accept': 'application/vnd.4thoffice.document.pinnedto.list-v5.0+json' if accept_type is None else accept_type,
        }
        data = export_dict(obj)
        response = self.api_client.api_call('put', endpoint, url_parameters, add_headers, data=json.dumps(data))
        
        return fill(DocumentPinnedToList_15, response.json())
