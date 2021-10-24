# from google.oauth2.service_account import Credentials
import gspread
from gspread import Client
from gspread.models import Spreadsheet, Worksheet
from gspread.utils import rowcol_to_a1
from typing import NewType
import sys
import os

##### ##### ##### ##### ##### #####
# 나중에 실제 DOC 문서를 접근 할 것을 대비해서
# 새로운 sheet에 접근할 수 있는 권한을 어떻게 등록(?) 할 수 있을지 만들기
# ex)
# 디스코드에 봇 추가하고,
# 관리자 권한을 부여받고,
# 관리할 sheet를 등록하는 절차
##### ##### ##### ##### ##### #####

# row, col str
A1 = NewType('A1', str)

# print(rowcol_to_a1(34, 50))

toSecret = './secret/jandi-manager-key.json'

KEY = './secret/jandi-manager-key.json'

# gs = gspread.service_account(filename=KEY)

# worksheets = {
#     'test': '현재인원관리_2',
#     'current_members': '현재인원관리',
#     'commit_check': '인증관리',
#     'event': '이벤트'
# }

TITLE = 'temp'
# spreadsheet: Spreadsheet = gc.open(TITLE)

# test = spreadsheet.worksheet('현재인원관리_2')

# cell = test.cell(1, 2, value_render_option='FORMULA').value
# print(test.get('A1:B2'))
# test.get("")


class JandiSpreadsheetManager:
    def __init__(self, gs: Client) -> None:
        self.gs = gs

    def getMember(self,):
        self.gs.open('')
        spreadsheet: Spreadsheet = self.gs.open(TITLE)
        pass

    def getWorkSheet(self, sheetName: str):
        pass

    def getRange(self, sheetName: str):
        pass

    def getCell(self, x: int, y: int):
        return rowcol_to_a1(y, x)


if __name__ == '__main__':
    gs = gspread.service_account(filename=KEY)

    val = gs.open(TITLE).sheet1.cell(1, 1).value
    print(val)
    print("--------------")

    # 나중에는 이렇게 해야한다...!
    # https://docs.gspread.org/en/latest/oauth2.html
    # gs = gspread.service_account(filename=KEY)
    # val = gs.open('시트 이름').sheet1.cell(1, 1).value
    # print(val)

    # sm = JandiSpreadsheetManager(gs)
