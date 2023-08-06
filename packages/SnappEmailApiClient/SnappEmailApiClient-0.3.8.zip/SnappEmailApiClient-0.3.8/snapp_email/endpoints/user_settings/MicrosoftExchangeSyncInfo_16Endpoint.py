"""
Auto generated code

"""

import json
from snapp_email.datacontract.classes import MicrosoftExchangeSyncInfo_16
from snapp_email.datacontract.utils import export_dict, fill


class MicrosoftExchangeSyncInfo_16Endpoint:
    def __init__(self, api_client):
        self.api_client = api_client
    
    def options(self, accept_type=None):
        """
        Retrieve options available for resource 'MicrosoftExchangeSyncInfo_16'.
        
        :param accept_type: 
        :type accept_type: str
        
        :return: 
        :rtype: MicrosoftExchangeSyncInfo_16
        """
        url_parameters = {
        }
        endpoint_parameters = {
        }
        endpoint = 'user/settings'.format(**endpoint_parameters)
        add_headers = {
            'Content-Type': 'application/vnd.4thoffice.microsoft.exchange.sync.info-5.2+json',
            'Accept': 'application/vnd.4thoffice.microsoft.exchange.sync.info-5.2+json' if accept_type is None else accept_type,
        }
        response = self.api_client.api_call('options', endpoint, url_parameters, add_headers)
        
        return fill(MicrosoftExchangeSyncInfo_16, response.json())
    
    def get(self, accept_type=None):
        """
        Get sync info resource.
        
        :param accept_type: 
        :type accept_type: str
        
        :return: 
        :rtype: MicrosoftExchangeSyncInfo_16
        """
        url_parameters = {
        }
        endpoint_parameters = {
        }
        endpoint = 'user/settings'.format(**endpoint_parameters)
        add_headers = {
            'Content-Type': 'application/vnd.4thoffice.microsoft.exchange.sync.info-5.2+json',
            'Accept': 'application/vnd.4thoffice.microsoft.exchange.sync.info-5.2+json' if accept_type is None else accept_type,
        }
        response = self.api_client.api_call('get', endpoint, url_parameters, add_headers)
        
        return fill(MicrosoftExchangeSyncInfo_16, response.json())
