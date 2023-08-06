from .ListOfAgendaPage_22Endpoint import ListOfAgendaPage_22Endpoint
from .AgendaSummary_22Endpoint import AgendaSummary_22Endpoint
from .AppointmentListPage_20Endpoint import AppointmentListPage_20Endpoint
from .AppointmentResponse_20Endpoint import AppointmentResponse_20Endpoint


class AppointmentEndpoint:
    def __init__(self, api_client):
        self._api_client = api_client

    @property
    def ListOfAgendaPage_22(self):
        """
        :return: ListOfAgendaPage_22Endpoint
        """
        return ListOfAgendaPage_22Endpoint(self._api_client)
        
    @property
    def AgendaSummary_22(self):
        """
        :return: AgendaSummary_22Endpoint
        """
        return AgendaSummary_22Endpoint(self._api_client)
        
    @property
    def AppointmentListPage_20(self):
        """
        :return: AppointmentListPage_20Endpoint
        """
        return AppointmentListPage_20Endpoint(self._api_client)
        
    @property
    def AppointmentResponse_20(self):
        """
        :return: AppointmentResponse_20Endpoint
        """
        return AppointmentResponse_20Endpoint(self._api_client)
        