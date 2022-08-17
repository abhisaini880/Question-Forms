import gspread
from oauth2client.service_account import ServiceAccountCredentials


class GoogleSheet:
    def __init__(self, conn):
        self.conn = conn
        self.client = self.get_client()

    def get_client(self):
        SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

        credentials = ServiceAccountCredentials.from_json_keyfile_dict(
            self.conn, SCOPES
        )

        return gspread.authorize(credentials=credentials)
