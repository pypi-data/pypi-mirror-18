from .MobileDevice_4Endpoint import MobileDevice_4Endpoint


class UserDeviceEndpoint:
    def __init__(self, api_client):
        self._api_client = api_client

    @property
    def MobileDevice_4(self):
        """
        :return: MobileDevice_4Endpoint
        """
        return MobileDevice_4Endpoint(self._api_client)
        