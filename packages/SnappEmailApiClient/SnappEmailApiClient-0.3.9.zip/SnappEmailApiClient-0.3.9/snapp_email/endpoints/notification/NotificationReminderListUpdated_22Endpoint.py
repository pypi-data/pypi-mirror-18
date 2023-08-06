"""
Auto generated code

"""

import json
from snapp_email.datacontract.classes import NotificationReminderListUpdated_22
from snapp_email.datacontract.utils import export_dict, fill


class NotificationReminderListUpdated_22Endpoint:
    def __init__(self, api_client):
        self.api_client = api_client
    
    def options(self, accept_type=None):
        """
        Retrieve options available for resource 'NotificationReminderListUpdated_22'.
        
        :param accept_type: 
        :type accept_type: str
        
        :return: 
        :rtype: NotificationReminderListUpdated_22
        """
        url_parameters = {
        }
        endpoint_parameters = {
        }
        endpoint = 'notification'.format(**endpoint_parameters)
        add_headers = {
            'Content-Type': 'application/vnd.4thoffice.notification.reminder.list.updated-v5.18+json',
            'Accept': 'application/vnd.4thoffice.notification.reminder.list.updated-v5.18+json' if accept_type is None else accept_type,
        }
        response = self.api_client.api_call('options', endpoint, url_parameters, add_headers)
        
        return fill(NotificationReminderListUpdated_22, response.json())
    
    def create(self, obj, accept_type=None):
        """
        Crete notification.
        
        :param obj: Object to be persisted
        :type obj: NotificationReminderListUpdated_22
        
        :param accept_type: 
        :type accept_type: str
        
        :return: 
        :rtype: NotificationReminderListUpdated_22
        """
        url_parameters = {
        }
        endpoint_parameters = {
        }
        endpoint = 'notification'.format(**endpoint_parameters)
        add_headers = {
            'Content-Type': 'application/vnd.4thoffice.notification.reminder.list.updated-v5.18+json',
            'Accept': 'application/vnd.4thoffice.notification.reminder.list.updated-v5.18+json' if accept_type is None else accept_type,
        }
        data = export_dict(obj)
        response = self.api_client.api_call('post', endpoint, url_parameters, add_headers, data=json.dumps(data))
        
        return fill(NotificationReminderListUpdated_22, response.json())
