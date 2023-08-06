"""
Auto generated code

"""

import json
from snapp_email.datacontract.classes import File_14
from snapp_email.datacontract.utils import export_dict, fill


class File_14Endpoint:
    def __init__(self, api_client):
        self.api_client = api_client
    
    def options(self, accept_type=None):
        """
        Retrieve options available for resource 'File_14'.
        
        :param accept_type: 
        :type accept_type: str
        
        :return: 
        :rtype: File_14
        """
        url_parameters = {
        }
        endpoint_parameters = {
        }
        endpoint = 'document'.format(**endpoint_parameters)
        add_headers = {
            'Content-Type': 'application/vnd.4thoffice.file-v4.0+json',
            'Accept': 'application/vnd.4thoffice.file-v4.0+json' if accept_type is None else accept_type,
        }
        response = self.api_client.api_call('options', endpoint, url_parameters, add_headers)
        
        return fill(File_14, response.json())
    
    def get(self, documentId, accept_type=None):
        """
        Retrieve document.
        
        :param documentId: 
        :type documentId: 
        
        :param accept_type: 
        :type accept_type: str
        
        :return: 
        :rtype: File_14
        """
        url_parameters = {
        }
        endpoint_parameters = {
            'documentId': documentId,
        }
        endpoint = 'document/{documentId}'.format(**endpoint_parameters)
        add_headers = {
            'Content-Type': 'application/vnd.4thoffice.file-v4.0+json',
            'Accept': 'application/vnd.4thoffice.file-v4.0+json' if accept_type is None else accept_type,
        }
        response = self.api_client.api_call('get', endpoint, url_parameters, add_headers)
        
        return fill(File_14, response.json())
