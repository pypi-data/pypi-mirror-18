"""
Auto generated code

"""

import json
from snapp_email.datacontract.classes import AssistantInsight_22
from snapp_email.datacontract.utils import export_dict, fill


class AssistantInsight_22Endpoint:
    def __init__(self, api_client):
        self.api_client = api_client
    
    def options(self, accept_type=None):
        """
        Retrieve options available for resource 'AssistantInsight_22'.
        
        :param accept_type: 
        :type accept_type: str
        
        :return: 
        :rtype: AssistantInsight_22
        """
        url_parameters = {
        }
        endpoint_parameters = {
        }
        endpoint = 'post'.format(**endpoint_parameters)
        add_headers = {
            'Content-Type': 'application/vnd.4thoffice.assistant.insight-5.18+json',
            'Accept': 'application/vnd.4thoffice.assistant.insight-5.18+json' if accept_type is None else accept_type,
        }
        response = self.api_client.api_call('options', endpoint, url_parameters, add_headers)
        
        return fill(AssistantInsight_22, response.json())
    
    def update(self, obj, postId, accept_type=None):
        """
        Update invoice
        
        :param obj: Object to be persisted
        :type obj: AssistantInsight_22
        
        :param postId: 
        :type postId: 
        
        :param accept_type: 
        :type accept_type: str
        
        :return: 
        :rtype: AssistantInsight_22
        """
        url_parameters = {
        }
        endpoint_parameters = {
            'postId': postId,
        }
        endpoint = 'post/{postId}'.format(**endpoint_parameters)
        add_headers = {
            'Content-Type': 'application/vnd.4thoffice.assistant.insight-5.18+json',
            'Accept': 'application/vnd.4thoffice.assistant.insight-5.18+json' if accept_type is None else accept_type,
        }
        data = export_dict(obj)
        response = self.api_client.api_call('put', endpoint, url_parameters, add_headers, data=json.dumps(data))
        
        return fill(AssistantInsight_22, response.json())
