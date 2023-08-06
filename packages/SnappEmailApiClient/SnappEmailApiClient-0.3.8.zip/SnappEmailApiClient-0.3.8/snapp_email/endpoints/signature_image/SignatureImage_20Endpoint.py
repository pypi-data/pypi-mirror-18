"""
Auto generated code

"""

import json
from snapp_email.datacontract.classes import SignatureImage_20
from snapp_email.datacontract.utils import export_dict, fill


class SignatureImage_20Endpoint:
    def __init__(self, api_client):
        self.api_client = api_client
    
    def options(self, imageId, accept_type=None):
        """
        Retrieve options available for resource 'SignatureImage_20'.
        
        :param imageId: 
        :type imageId: 
        
        :param accept_type: 
        :type accept_type: str
        
        :return: 
        :rtype: SignatureImage_20
        """
        url_parameters = {
            'imageId': imageId,
        }
        endpoint_parameters = {
        }
        endpoint = 'signature/image'.format(**endpoint_parameters)
        add_headers = {
            'Content-Type': 'application/vnd.4thoffice.signature.image-5.15+json',
            'Accept': 'application/vnd.4thoffice.signature.image-5.15+json' if accept_type is None else accept_type,
        }
        response = self.api_client.api_call('options', endpoint, url_parameters, add_headers)
        
        return fill(SignatureImage_20, response.json())
    
    def get(self, imageId, accept_type=None):
        """
        Retrieve signature image
        
        :param imageId: 
        :type imageId: 
        
        :param accept_type: 
        :type accept_type: str
        
        :return: 
        :rtype: SignatureImage_20
        """
        url_parameters = {
            'imageId': imageId,
        }
        endpoint_parameters = {
        }
        endpoint = 'signature/image/{imageId}'.format(**endpoint_parameters)
        add_headers = {
            'Content-Type': 'application/vnd.4thoffice.signature.image-5.15+json',
            'Accept': 'application/vnd.4thoffice.signature.image-5.15+json' if accept_type is None else accept_type,
        }
        response = self.api_client.api_call('get', endpoint, url_parameters, add_headers)
        
        return fill(SignatureImage_20, response.json())
    
    def update(self, obj, imageId, accept_type=None):
        """
        Create signature image
        
        :param obj: Object to be persisted
        :type obj: SignatureImage_20
        
        :param imageId: 
        :type imageId: 
        
        :param accept_type: 
        :type accept_type: str
        
        :return: 
        :rtype: SignatureImage_20
        """
        url_parameters = {
            'imageId': imageId,
        }
        endpoint_parameters = {
        }
        endpoint = 'signature/image/{imageId}'.format(**endpoint_parameters)
        add_headers = {
            'Content-Type': 'application/vnd.4thoffice.signature.image-5.15+json',
            'Accept': 'application/vnd.4thoffice.signature.image-5.15+json' if accept_type is None else accept_type,
        }
        data = export_dict(obj)
        response = self.api_client.api_call('put', endpoint, url_parameters, add_headers, data=json.dumps(data))
        
        return fill(SignatureImage_20, response.json())
