"""
Auto generated code

"""

import json
from snapp_email.datacontract.classes import BoardPersonal_21
from snapp_email.datacontract.utils import export_dict, fill


class BoardPersonal_21Endpoint:
    def __init__(self, api_client):
        self.api_client = api_client
    
    def options(self, accept_type=None):
        """
        Retrieve options available for resource 'BoardPersonal_21'.
        
        :param accept_type: 
        :type accept_type: str
        
        :return: 
        :rtype: BoardPersonal_21
        """
        url_parameters = {
        }
        endpoint_parameters = {
        }
        endpoint = 'board'.format(**endpoint_parameters)
        add_headers = {
            'Content-Type': 'application/vnd.4thoffice.board.personal-5.17+json',
            'Accept': 'application/vnd.4thoffice.board.personal-5.17+json' if accept_type is None else accept_type,
        }
        response = self.api_client.api_call('options', endpoint, url_parameters, add_headers)
        
        return fill(BoardPersonal_21, response.json())
    
    def get(self, boardId, accept_type=None):
        """
        Retrieve board resource.
        
        :param boardId: 
        :type boardId: 
        
        :param accept_type: 
        :type accept_type: str
        
        :return: 
        :rtype: BoardPersonal_21
        """
        url_parameters = {
        }
        endpoint_parameters = {
            'boardId': boardId,
        }
        endpoint = 'board/{boardId}'.format(**endpoint_parameters)
        add_headers = {
            'Content-Type': 'application/vnd.4thoffice.board.personal-5.17+json',
            'Accept': 'application/vnd.4thoffice.board.personal-5.17+json' if accept_type is None else accept_type,
        }
        response = self.api_client.api_call('get', endpoint, url_parameters, add_headers)
        
        return fill(BoardPersonal_21, response.json())
    
    def create(self, obj, accept_type=None):
        """
        Create board resource.
        
        :param obj: Object to be persisted
        :type obj: BoardPersonal_21
        
        :param accept_type: 
        :type accept_type: str
        
        :return: 
        :rtype: BoardPersonal_21
        """
        url_parameters = {
        }
        endpoint_parameters = {
        }
        endpoint = 'board'.format(**endpoint_parameters)
        add_headers = {
            'Content-Type': 'application/vnd.4thoffice.board.personal-5.17+json',
            'Accept': 'application/vnd.4thoffice.board.personal-5.17+json' if accept_type is None else accept_type,
        }
        data = export_dict(obj)
        response = self.api_client.api_call('post', endpoint, url_parameters, add_headers, data=json.dumps(data))
        
        return fill(BoardPersonal_21, response.json())
    
    def update(self, obj, boardId, accept_type=None):
        """
        Update board resource.
        
        :param obj: Object to be persisted
        :type obj: BoardPersonal_21
        
        :param boardId: 
        :type boardId: 
        
        :param accept_type: 
        :type accept_type: str
        
        :return: 
        :rtype: BoardPersonal_21
        """
        url_parameters = {
        }
        endpoint_parameters = {
            'boardId': boardId,
        }
        endpoint = 'board/{boardId}'.format(**endpoint_parameters)
        add_headers = {
            'Content-Type': 'application/vnd.4thoffice.board.personal-5.17+json',
            'Accept': 'application/vnd.4thoffice.board.personal-5.17+json' if accept_type is None else accept_type,
        }
        data = export_dict(obj)
        response = self.api_client.api_call('put', endpoint, url_parameters, add_headers, data=json.dumps(data))
        
        return fill(BoardPersonal_21, response.json())
    
    def delete(self, boardId, accept_type=None):
        """
        Delete board resource.
        
        :param boardId: 
        :type boardId: 
        
        :param accept_type: 
        :type accept_type: str
        
        :return: 
        :rtype: BoardPersonal_21
        """
        url_parameters = {
        }
        endpoint_parameters = {
            'boardId': boardId,
        }
        endpoint = 'board/{boardId}'.format(**endpoint_parameters)
        add_headers = {
            'Content-Type': 'application/vnd.4thoffice.board.personal-5.17+json',
            'Accept': 'application/vnd.4thoffice.board.personal-5.17+json' if accept_type is None else accept_type,
        }
        response = self.api_client.api_call('delete', endpoint, url_parameters, add_headers)
        
        return fill(BoardPersonal_21, response.json())
