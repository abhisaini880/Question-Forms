""" It will accept the data from consumer and call the related service """

from abc import ABC, abstractmethod
from services.google_sheet import GoogleSheet


def InterfaceFactory(app):
    """Factory Method"""
    services = {
        "gsheet": GoogleSheetApp,
    }

    return services[app]()


class ServiceInterface(ABC):
    @abstractmethod
    def process(self, app_data):
        pass


class GoogleSheetApp(ServiceInterface):
    def process(self, app_data):
        GS = GoogleSheet(app_data)
        GS.get_response_data()
        GS.create_entry_in_sheet()
