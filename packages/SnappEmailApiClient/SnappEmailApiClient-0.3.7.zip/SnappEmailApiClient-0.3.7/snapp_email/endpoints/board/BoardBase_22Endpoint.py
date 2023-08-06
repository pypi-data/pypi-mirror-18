"""
Auto generated code

"""

import json
from snapp_email.datacontract.classes import BoardBase_22
from snapp_email.datacontract.utils import export_dict, fill


class BoardBase_22Endpoint:
    def __init__(self, api_client):
        self.api_client = api_client
    
    def options(self, accept_type=None):
        """
        Retrieve options available for resource 'BoardBase_22'.
        
        :param accept_type: 
        :type accept_type: str
        
        :return: 
        :rtype: BoardBase_22
        """
        url_parameters = {
        }
        endpoint_parameters = {
        }
        endpoint = 'board'.format(**endpoint_parameters)
        add_headers = {
            'Content-Type': 'application/vnd.4thoffice.board.base-5.18+json',
            'Accept': 'application/vnd.4thoffice.board.base-5.18+json' if accept_type is None else accept_type,
        }
        response = self.api_client.api_call('options', endpoint, url_parameters, add_headers)
        
        return fill(BoardBase_22, response.json())
    
    def get(self, boardId, accept_type=None):
        """
        Retrieve board resource.
        
        :param boardId: 
        :type boardId: 
        
        :param accept_type: 
        :type accept_type: str
        
        :return: 
        :rtype: BoardBase_22
        """
        url_parameters = {
        }
        endpoint_parameters = {
            'boardId': boardId,
        }
        endpoint = 'board/{boardId}'.format(**endpoint_parameters)
        add_headers = {
            'Content-Type': 'application/vnd.4thoffice.board.base-5.18+json',
            'Accept': 'application/vnd.4thoffice.board.base-5.18+json' if accept_type is None else accept_type,
        }
        response = self.api_client.api_call('get', endpoint, url_parameters, add_headers)
        
        return fill(BoardBase_22, response.json())
