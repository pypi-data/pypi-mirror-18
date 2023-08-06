"""
Auto generated code

"""

import json
from snapp_email.datacontract.classes import MobileDevice_4
from snapp_email.datacontract.utils import export_dict, fill


class MobileDevice_4Endpoint:
    def __init__(self, api_client):
        self.api_client = api_client
    
    def options(self, deviceId, accept_type=None):
        """
        Retrieve options available for resource 'MobileDevice_4'.
        
        :param deviceId: 
        :type deviceId: 
        
        :param accept_type: 
        :type accept_type: str
        
        :return: 
        :rtype: MobileDevice_4
        """
        url_parameters = {
            'deviceId': deviceId,
        }
        endpoint_parameters = {
        }
        endpoint = 'user/device'.format(**endpoint_parameters)
        add_headers = {
            'Content-Type': 'application/vnd.marg.bcsocial.device.mobile-2.6+json',
            'Accept': 'application/vnd.marg.bcsocial.device.mobile-2.6+json' if accept_type is None else accept_type,
        }
        response = self.api_client.api_call('options', endpoint, url_parameters, add_headers)
        
        return fill(MobileDevice_4, response.json())
    
    def get(self, deviceId, accept_type=None):
        """
        Retrieve user device
        
        :param deviceId: 
        :type deviceId: 
        
        :param accept_type: 
        :type accept_type: str
        
        :return: 
        :rtype: MobileDevice_4
        """
        url_parameters = {
            'deviceId': deviceId,
        }
        endpoint_parameters = {
        }
        endpoint = 'user/device/{deviceId}'.format(**endpoint_parameters)
        add_headers = {
            'Content-Type': 'application/vnd.marg.bcsocial.device.mobile-2.6+json',
            'Accept': 'application/vnd.marg.bcsocial.device.mobile-2.6+json' if accept_type is None else accept_type,
        }
        response = self.api_client.api_call('get', endpoint, url_parameters, add_headers)
        
        return fill(MobileDevice_4, response.json())
    
    def create(self, obj, deviceId, removeOther=None, accept_type=None):
        """
        Register user device
        
        :param obj: Object to be persisted
        :type obj: MobileDevice_4
        
        :param deviceId: 
        :type deviceId: 
        
        :param removeOther: Boolean flag indicating registration request with force removal of already registered resources.
        :type removeOther: Boolean
        
        :param accept_type: 
        :type accept_type: str
        
        :return: 
        :rtype: MobileDevice_4
        """
        url_parameters = {
            'deviceId': deviceId,
            'removeOther': removeOther,
        }
        endpoint_parameters = {
        }
        endpoint = 'user/device'.format(**endpoint_parameters)
        add_headers = {
            'Content-Type': 'application/vnd.marg.bcsocial.device.mobile-2.6+json',
            'Accept': 'application/vnd.marg.bcsocial.device.mobile-2.6+json' if accept_type is None else accept_type,
        }
        data = export_dict(obj)
        response = self.api_client.api_call('post', endpoint, url_parameters, add_headers, data=json.dumps(data))
        
        return fill(MobileDevice_4, response.json())
    
    def update(self, obj, deviceId, accept_type=None):
        """
        Update user device
        
        :param obj: Object to be persisted
        :type obj: MobileDevice_4
        
        :param deviceId: 
        :type deviceId: 
        
        :param accept_type: 
        :type accept_type: str
        
        :return: 
        :rtype: MobileDevice_4
        """
        url_parameters = {
            'deviceId': deviceId,
        }
        endpoint_parameters = {
        }
        endpoint = 'user/device/{deviceId}'.format(**endpoint_parameters)
        add_headers = {
            'Content-Type': 'application/vnd.marg.bcsocial.device.mobile-2.6+json',
            'Accept': 'application/vnd.marg.bcsocial.device.mobile-2.6+json' if accept_type is None else accept_type,
        }
        data = export_dict(obj)
        response = self.api_client.api_call('put', endpoint, url_parameters, add_headers, data=json.dumps(data))
        
        return fill(MobileDevice_4, response.json())
    
    def delete(self, deviceId, accept_type=None):
        """
        Unregister user device
        
        :param deviceId: 
        :type deviceId: 
        
        :param accept_type: 
        :type accept_type: str
        
        :return: 
        :rtype: MobileDevice_4
        """
        url_parameters = {
            'deviceId': deviceId,
        }
        endpoint_parameters = {
        }
        endpoint = 'user/device/{deviceId}'.format(**endpoint_parameters)
        add_headers = {
            'Content-Type': 'application/vnd.marg.bcsocial.device.mobile-2.6+json',
            'Accept': 'application/vnd.marg.bcsocial.device.mobile-2.6+json' if accept_type is None else accept_type,
        }
        response = self.api_client.api_call('delete', endpoint, url_parameters, add_headers)
        
        return fill(MobileDevice_4, response.json())
