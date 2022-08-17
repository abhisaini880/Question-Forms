from gspread.exceptions import WorksheetNotFound
from flask import current_app as app

from apis.response.model import Model as ResponseModel


class GoogleSheet:
    def __init__(self, app_data):
        self.app_data = app_data.get("app_data")
        self.form_id = app_data.get("form_id")
        self.response_id = app_data.get("response_id")
        self.spread_sheet_id = self.app_data.get("spread_sheet_id")
        self.worksheet_title = self.app_data.get("worksheet_title")

    def get_response_data(self):
        self.record = {}
        response_data = ResponseModel.get_response(
            response_id=self.response_id
        )
        if not response_data:
            return self.record
        print(response_data)
        for answer in response_data.get("answers", []):
            self.record[answer.get("question_title")] = answer.get("answer")

        return self.record

    def create_entry_in_sheet(self):

        if not self.record:
            return

        sheet = app.config["gsheet_client"].open_by_key(self.spread_sheet_id)

        try:
            worksheet = sheet.worksheet(self.worksheet_title)
        except WorksheetNotFound:
            worksheet = sheet.add_worksheet(
                title=self.worksheet_title, rows=0, cols=0
            )

        # use below code if want to create the sheet by yourself and share the access to client
        #
        # sheet = client.create('Spread_sheet_name')
        # sheet.share('<user-email>', perm_type='user', role='writer')

        col_list = worksheet.row_values(1)

        if not col_list:
            # NO records are present
            cols = list(self.record.keys())
            worksheet.insert_row(cols)

        # Insert the latest entry on top
        # exsiting entries will move one row below
        worksheet.insert_row(list(self.record.values()), index=2)

        # If you want to move the latest entry to bottom
        # use below code
        #
        # all_records = worksheet.get_all_records()
        # next_index = len(all_records) + 2
        # worksheet.insert_row(list(data.values()), index=next_index)
        # worksheet.insert_cols
