"""
Auto generated code

"""

import json
from snapp_email.datacontract.classes import ReminderQuestion_20
from snapp_email.datacontract.utils import export_dict, fill


class ReminderQuestion_20Endpoint:
    def __init__(self, api_client):
        self.api_client = api_client
    
    def options(self, accept_type=None):
        """
        Retrieve options available for resource 'ReminderQuestion_20'.
        
        :param accept_type: 
        :type accept_type: str
        
        :return: 
        :rtype: ReminderQuestion_20
        """
        url_parameters = {
        }
        endpoint_parameters = {
        }
        endpoint = 'reminder'.format(**endpoint_parameters)
        add_headers = {
            'Content-Type': 'application/vnd.4thoffice.reminder.question-v5.15+json',
            'Accept': 'application/vnd.4thoffice.reminder.question-v5.15+json' if accept_type is None else accept_type,
        }
        response = self.api_client.api_call('options', endpoint, url_parameters, add_headers)
        
        return fill(ReminderQuestion_20, response.json())
    
    def get(self, reminderId, accept_type=None):
        """
        Get reminder
        
        :param reminderId: 
        :type reminderId: 
        
        :param accept_type: 
        :type accept_type: str
        
        :return: 
        :rtype: ReminderQuestion_20
        """
        url_parameters = {
        }
        endpoint_parameters = {
            'reminderId': reminderId,
        }
        endpoint = 'reminder/{reminderId}'.format(**endpoint_parameters)
        add_headers = {
            'Content-Type': 'application/vnd.4thoffice.reminder.question-v5.15+json',
            'Accept': 'application/vnd.4thoffice.reminder.question-v5.15+json' if accept_type is None else accept_type,
        }
        response = self.api_client.api_call('get', endpoint, url_parameters, add_headers)
        
        return fill(ReminderQuestion_20, response.json())
    
    def create(self, obj, accept_type=None):
        """
        Create reminder
        
        :param obj: Object to be persisted
        :type obj: ReminderQuestion_20
        
        :param accept_type: 
        :type accept_type: str
        
        :return: 
        :rtype: ReminderQuestion_20
        """
        url_parameters = {
        }
        endpoint_parameters = {
        }
        endpoint = 'reminder'.format(**endpoint_parameters)
        add_headers = {
            'Content-Type': 'application/vnd.4thoffice.reminder.question-v5.15+json',
            'Accept': 'application/vnd.4thoffice.reminder.question-v5.15+json' if accept_type is None else accept_type,
        }
        data = export_dict(obj)
        response = self.api_client.api_call('post', endpoint, url_parameters, add_headers, data=json.dumps(data))
        
        return fill(ReminderQuestion_20, response.json())
    
    def delete(self, reminderId, accept_type=None):
        """
        Delete reminder
        
        :param reminderId: 
        :type reminderId: 
        
        :param accept_type: 
        :type accept_type: str
        
        :return: 
        :rtype: ReminderQuestion_20
        """
        url_parameters = {
        }
        endpoint_parameters = {
            'reminderId': reminderId,
        }
        endpoint = 'reminder/{reminderId}'.format(**endpoint_parameters)
        add_headers = {
            'Content-Type': 'application/vnd.4thoffice.reminder.question-v5.15+json',
            'Accept': 'application/vnd.4thoffice.reminder.question-v5.15+json' if accept_type is None else accept_type,
        }
        response = self.api_client.api_call('delete', endpoint, url_parameters, add_headers)
        
        return fill(ReminderQuestion_20, response.json())
