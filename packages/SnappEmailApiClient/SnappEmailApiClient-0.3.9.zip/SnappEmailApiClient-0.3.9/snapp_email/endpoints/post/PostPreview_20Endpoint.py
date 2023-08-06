"""
Auto generated code

"""

import json
from snapp_email.datacontract.classes import PostPreview_20
from snapp_email.datacontract.utils import export_dict, fill


class PostPreview_20Endpoint:
    def __init__(self, api_client):
        self.api_client = api_client
    
    def options(self, accept_type=None):
        """
        Retrieve options available for resource 'Post_20'.
        
        :param accept_type: 
        :type accept_type: str
        
        :return: 
        :rtype: PostPreview_20
        """
        url_parameters = {
        }
        endpoint_parameters = {
        }
        endpoint = 'post'.format(**endpoint_parameters)
        add_headers = {
            'Content-Type': 'application/vnd.4thoffice.post.preview-5.15+json',
            'Accept': 'application/vnd.4thoffice.post.preview-5.15+json' if accept_type is None else accept_type,
        }
        response = self.api_client.api_call('options', endpoint, url_parameters, add_headers)
        
        return fill(PostPreview_20, response.json())
    
    def get(self, postId, accept_type=None):
        """
        Retrieve post resource.
        
        :param postId: 
        :type postId: 
        
        :param accept_type: 
        :type accept_type: str
        
        :return: 
        :rtype: PostPreview_20
        """
        url_parameters = {
        }
        endpoint_parameters = {
            'postId': postId,
        }
        endpoint = 'post/{postId}'.format(**endpoint_parameters)
        add_headers = {
            'Content-Type': 'application/vnd.4thoffice.post.preview-5.15+json',
            'Accept': 'application/vnd.4thoffice.post.preview-5.15+json' if accept_type is None else accept_type,
        }
        response = self.api_client.api_call('get', endpoint, url_parameters, add_headers)
        
        return fill(PostPreview_20, response.json())
