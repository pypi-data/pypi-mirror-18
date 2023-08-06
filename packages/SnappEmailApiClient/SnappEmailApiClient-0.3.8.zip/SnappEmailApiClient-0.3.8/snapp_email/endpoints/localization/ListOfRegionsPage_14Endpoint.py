"""
Auto generated code

"""

import json
from snapp_email.datacontract.classes import ListOfRegionsPage_14
from snapp_email.datacontract.utils import export_dict, fill


class ListOfRegionsPage_14Endpoint:
    def __init__(self, api_client):
        self.api_client = api_client
    
    def options(self, accept_type=None):
        """
        Retrieve options available for resource 'ListOfRegionsPage_14'.
        
        :param accept_type: 
        :type accept_type: str
        
        :return: 
        :rtype: ListOfRegionsPage_14
        """
        url_parameters = {
        }
        endpoint_parameters = {
        }
        endpoint = 'localization'.format(**endpoint_parameters)
        add_headers = {
            'Content-Type': 'application/vnd.4thoffice.localization.region.list-4.0+json',
            'Accept': 'application/vnd.4thoffice.localization.region.list-4.0+json' if accept_type is None else accept_type,
        }
        response = self.api_client.api_call('options', endpoint, url_parameters, add_headers)
        
        return fill(ListOfRegionsPage_14, response.json())
    
    def get(self, size, offset, searchQuery=None, accept_type=None):
        """
        Get region list
        
        :param size: Specify size of requested page.
        :type size: Int32
        
        :param offset: Specify offset of requested page.
        :type offset: Int32
        
        :param searchQuery: Specify search query.
        :type searchQuery: String
        
        :param accept_type: 
        :type accept_type: str
        
        :return: 
        :rtype: ListOfRegionsPage_14
        """
        url_parameters = {
            'size': size,
            'offset': offset,
            'searchQuery': searchQuery,
        }
        endpoint_parameters = {
        }
        endpoint = 'localization'.format(**endpoint_parameters)
        add_headers = {
            'Content-Type': 'application/vnd.4thoffice.localization.region.list-4.0+json',
            'Accept': 'application/vnd.4thoffice.localization.region.list-4.0+json' if accept_type is None else accept_type,
        }
        response = self.api_client.api_call('get', endpoint, url_parameters, add_headers)
        
        return fill(ListOfRegionsPage_14, response.json())
