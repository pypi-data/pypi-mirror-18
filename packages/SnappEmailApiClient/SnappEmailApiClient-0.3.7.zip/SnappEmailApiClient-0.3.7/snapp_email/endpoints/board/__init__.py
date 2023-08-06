from .BoardName_22Endpoint import BoardName_22Endpoint
from .BoardPersonal_22Endpoint import BoardPersonal_22Endpoint
from .BoardPersonal_21Endpoint import BoardPersonal_21Endpoint
from .BoardPersonal_20Endpoint import BoardPersonal_20Endpoint
from .BoardGroup_22Endpoint import BoardGroup_22Endpoint
from .BoardBase_22Endpoint import BoardBase_22Endpoint
from .BoardPersonal_15Endpoint import BoardPersonal_15Endpoint
from .BoardBase_15Endpoint import BoardBase_15Endpoint


class BoardEndpoint:
    def __init__(self, api_client):
        self._api_client = api_client

    @property
    def BoardName_22(self):
        """
        :return: BoardName_22Endpoint
        """
        return BoardName_22Endpoint(self._api_client)
        
    @property
    def BoardPersonal_22(self):
        """
        :return: BoardPersonal_22Endpoint
        """
        return BoardPersonal_22Endpoint(self._api_client)
        
    @property
    def BoardPersonal_21(self):
        """
        :return: BoardPersonal_21Endpoint
        """
        return BoardPersonal_21Endpoint(self._api_client)
        
    @property
    def BoardPersonal_20(self):
        """
        :return: BoardPersonal_20Endpoint
        """
        return BoardPersonal_20Endpoint(self._api_client)
        
    @property
    def BoardGroup_22(self):
        """
        :return: BoardGroup_22Endpoint
        """
        return BoardGroup_22Endpoint(self._api_client)
        
    @property
    def BoardBase_22(self):
        """
        :return: BoardBase_22Endpoint
        """
        return BoardBase_22Endpoint(self._api_client)
        
    @property
    def BoardPersonal_15(self):
        """
        :return: BoardPersonal_15Endpoint
        """
        return BoardPersonal_15Endpoint(self._api_client)
        
    @property
    def BoardBase_15(self):
        """
        :return: BoardBase_15Endpoint
        """
        return BoardBase_15Endpoint(self._api_client)
        