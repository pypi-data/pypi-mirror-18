"""
Auto generated code

"""

import json
from snapp_email.datacontract.classes import LogOnUserMobile_4
from snapp_email.datacontract.utils import export_dict, fill


class LogOnUserMobile_4Endpoint:
    def __init__(self, api_client):
        self.api_client = api_client
    
    def options(self, accept_type=None):
        """
        Retrieve options available for resource 'LogOnUserMobile_4'.
        
        :param accept_type: 
        :type accept_type: str
        
        :return: 
        :rtype: LogOnUserMobile_4
        """
        url_parameters = {
        }
        endpoint_parameters = {
        }
        endpoint = 'user/session/logon'.format(**endpoint_parameters)
        add_headers = {
            'Content-Type': 'application/vnd.marg.bcsocial.logon.user.mobile-v2.6+json',
            'Accept': 'application/vnd.marg.bcsocial.logon.user.mobile-v2.6+json' if accept_type is None else accept_type,
        }
        response = self.api_client.api_call('options', endpoint, url_parameters, add_headers)
        
        return fill(LogOnUserMobile_4, response.json())
    
    def create(self, obj, accept_type=None):
        """
        Perform login.
        
        :param obj: Object to be persisted
        :type obj: LogOnUserMobile_4
        
        :param accept_type: 
        :type accept_type: str
        
        :return: 
        :rtype: LogOnUserMobile_4
        """
        url_parameters = {
        }
        endpoint_parameters = {
        }
        endpoint = 'user/session/logon'.format(**endpoint_parameters)
        add_headers = {
            'Content-Type': 'application/vnd.marg.bcsocial.logon.user.mobile-v2.6+json',
            'Accept': 'application/vnd.marg.bcsocial.logon.user.mobile-v2.6+json' if accept_type is None else accept_type,
        }
        data = export_dict(obj)
        response = self.api_client.api_call('post', endpoint, url_parameters, add_headers, data=json.dumps(data))
        
        return fill(LogOnUserMobile_4, response.json())
    
    def delete(self, accept_type=None):
        """
        Perform logout.
        
        :param accept_type: 
        :type accept_type: str
        
        :return: 
        :rtype: LogOnUserMobile_4
        """
        url_parameters = {
        }
        endpoint_parameters = {
        }
        endpoint = 'user/session/logon'.format(**endpoint_parameters)
        add_headers = {
            'Content-Type': 'application/vnd.marg.bcsocial.logon.user.mobile-v2.6+json',
            'Accept': 'application/vnd.marg.bcsocial.logon.user.mobile-v2.6+json' if accept_type is None else accept_type,
        }
        response = self.api_client.api_call('delete', endpoint, url_parameters, add_headers)
        
        return fill(LogOnUserMobile_4, response.json())
