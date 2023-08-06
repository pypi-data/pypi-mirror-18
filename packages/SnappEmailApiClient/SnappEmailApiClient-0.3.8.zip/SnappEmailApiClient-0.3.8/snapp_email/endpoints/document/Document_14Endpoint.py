"""
Auto generated code

"""

import json
from snapp_email.datacontract.classes import Document_14
from snapp_email.datacontract.utils import export_dict, fill


class Document_14Endpoint:
    def __init__(self, api_client):
        self.api_client = api_client
    
    def options(self, accept_type=None):
        """
        Retrieve options available for resource 'Document_14'.
        
        :param accept_type: 
        :type accept_type: str
        
        :return: 
        :rtype: Document_14
        """
        url_parameters = {
        }
        endpoint_parameters = {
        }
        endpoint = 'document'.format(**endpoint_parameters)
        add_headers = {
            'Content-Type': 'application/vnd.4thoffice.document-v4.0+json',
            'Accept': 'application/vnd.4thoffice.document-v4.0+json' if accept_type is None else accept_type,
        }
        response = self.api_client.api_call('options', endpoint, url_parameters, add_headers)
        
        return fill(Document_14, response.json())
    
    def get(self, documentId, accept_type=None):
        """
        Retrieve document.
        
        :param documentId: 
        :type documentId: 
        
        :param accept_type: 
        :type accept_type: str
        
        :return: 
        :rtype: Document_14
        """
        url_parameters = {
        }
        endpoint_parameters = {
            'documentId': documentId,
        }
        endpoint = 'document/{documentId}'.format(**endpoint_parameters)
        add_headers = {
            'Content-Type': 'application/vnd.4thoffice.document-v4.0+json',
            'Accept': 'application/vnd.4thoffice.document-v4.0+json' if accept_type is None else accept_type,
        }
        response = self.api_client.api_call('get', endpoint, url_parameters, add_headers)
        if accept_type == 'application/octet-stream':
            return response.content
        return fill(Document_14, response.json())
    
    def create(self, obj, obj_filename, accept_type=None):
        """
        Create document.
        
        :param obj: Object to be persisted
        :type obj: 
        
        :param obj_filename: Filename of object to be persisted
        :type obj_filename: str
        
        :param accept_type: 
        :type accept_type: str
        
        :return: 
        :rtype: Document_14
        """
        url_parameters = {
        }
        endpoint_parameters = {
        }
        endpoint = 'document'.format(**endpoint_parameters)
        add_headers = {
            'Content-Type': 'application/octet-stream',
            'Accept': 'application/vnd.4thoffice.document-v4.0+json' if accept_type is None else accept_type,
            'X-Upload-File-Name': obj_filename,
        }
        response = self.api_client.api_call('post', endpoint, url_parameters, add_headers, data=obj)
        
        return fill(Document_14, response.json())
    
    def update(self, obj, obj_filename, documentId, accept_type=None):
        """
        Update document.
        
        :param obj: Object to be persisted
        :type obj: 
        
        :param obj_filename: Filename of object to be persisted
        :type obj_filename: str
        
        :param documentId: 
        :type documentId: 
        
        :param accept_type: 
        :type accept_type: str
        
        :return: 
        :rtype: Document_14
        """
        url_parameters = {
        }
        endpoint_parameters = {
            'documentId': documentId,
        }
        endpoint = 'document/{documentId}'.format(**endpoint_parameters)
        add_headers = {
            'Content-Type': 'application/octet-stream',
            'Accept': 'application/vnd.4thoffice.document-v4.0+json' if accept_type is None else accept_type,
            'X-Upload-File-Name': obj_filename,
        }
        response = self.api_client.api_call('put', endpoint, url_parameters, add_headers, data=obj)
        
        return fill(Document_14, response.json())
    
    def delete(self, documentId, accept_type=None):
        """
        Delete document.
        
        :param documentId: 
        :type documentId: 
        
        :param accept_type: 
        :type accept_type: str
        
        :return: 
        :rtype: Document_14
        """
        url_parameters = {
        }
        endpoint_parameters = {
            'documentId': documentId,
        }
        endpoint = 'document/{documentId}'.format(**endpoint_parameters)
        add_headers = {
            'Content-Type': 'application/vnd.4thoffice.document-v4.0+json',
            'Accept': 'application/vnd.4thoffice.document-v4.0+json' if accept_type is None else accept_type,
        }
        response = self.api_client.api_call('delete', endpoint, url_parameters, add_headers)
        
        return fill(Document_14, response.json())
