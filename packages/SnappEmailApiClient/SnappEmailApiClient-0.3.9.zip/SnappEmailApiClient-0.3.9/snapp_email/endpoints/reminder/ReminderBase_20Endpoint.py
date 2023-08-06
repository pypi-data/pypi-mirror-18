"""
Auto generated code

"""

import json
from snapp_email.datacontract.classes import ReminderBase_20
from snapp_email.datacontract.utils import export_dict, fill


class ReminderBase_20Endpoint:
    def __init__(self, api_client):
        self.api_client = api_client
    
    def options(self, accept_type=None):
        """
        Retrieve options available for resource 'ReminderBase_20'.
        
        :param accept_type: 
        :type accept_type: str
        
        :return: 
        :rtype: ReminderBase_20
        """
        url_parameters = {
        }
        endpoint_parameters = {
        }
        endpoint = 'reminder'.format(**endpoint_parameters)
        add_headers = {
            'Content-Type': 'application/vnd.4thoffice.reminder.base-v5.15+json',
            'Accept': 'application/vnd.4thoffice.reminder.base-v5.15+json' if accept_type is None else accept_type,
        }
        response = self.api_client.api_call('options', endpoint, url_parameters, add_headers)
        
        return fill(ReminderBase_20, response.json())
    
    def get(self, reminderId, accept_type=None):
        """
        Get reminder
        
        :param reminderId: 
        :type reminderId: 
        
        :param accept_type: 
        :type accept_type: str
        
        :return: 
        :rtype: ReminderBase_20
        """
        url_parameters = {
        }
        endpoint_parameters = {
            'reminderId': reminderId,
        }
        endpoint = 'reminder/{reminderId}'.format(**endpoint_parameters)
        add_headers = {
            'Content-Type': 'application/vnd.4thoffice.reminder.base-v5.15+json',
            'Accept': 'application/vnd.4thoffice.reminder.base-v5.15+json' if accept_type is None else accept_type,
        }
        response = self.api_client.api_call('get', endpoint, url_parameters, add_headers)
        
        return fill(ReminderBase_20, response.json())
    
    def delete(self, reminderId, accept_type=None):
        """
        Delete reminder
        
        :param reminderId: 
        :type reminderId: 
        
        :param accept_type: 
        :type accept_type: str
        
        :return: 
        :rtype: ReminderBase_20
        """
        url_parameters = {
        }
        endpoint_parameters = {
            'reminderId': reminderId,
        }
        endpoint = 'reminder/{reminderId}'.format(**endpoint_parameters)
        add_headers = {
            'Content-Type': 'application/vnd.4thoffice.reminder.base-v5.15+json',
            'Accept': 'application/vnd.4thoffice.reminder.base-v5.15+json' if accept_type is None else accept_type,
        }
        response = self.api_client.api_call('delete', endpoint, url_parameters, add_headers)
        
        return fill(ReminderBase_20, response.json())
