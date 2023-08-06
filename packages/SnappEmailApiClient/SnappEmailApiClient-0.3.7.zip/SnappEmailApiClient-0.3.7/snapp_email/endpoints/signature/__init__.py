from .ListOfSignaturesPage_20Endpoint import ListOfSignaturesPage_20Endpoint


class SignatureEndpoint:
    def __init__(self, api_client):
        self._api_client = api_client

    @property
    def ListOfSignaturesPage_20(self):
        """
        :return: ListOfSignaturesPage_20Endpoint
        """
        return ListOfSignaturesPage_20Endpoint(self._api_client)
        