# from google.oauth2.service_account import Credentials
from dataclasses import dataclass
from itertools import zip_longest
from re import I
import gspread
from gspread import Client
from gspread.models import Spreadsheet, Worksheet, Cell
from gspread.utils import rowcol_to_a1
from typing import NewType

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
TITLE = '잔디정원사-smart'
USER_NAME_COL = 3
MEMBER_INFO_width = 6

_CustomRange_dict = {
    'Member30': 'Members30_with_Kicks',
    'Member40': 'Members40_with_Kicks',
    'Member50': 'Members50_with_Kicks',
    'Member_gone': 'Members_gone_100',
    'commit': '인증목록'
}

_Sheets = {
    'Member': '맴버',
    'MemberGone': '사라진 맴버',
    'Commit': '인증 관리'
}


@dataclass(frozen=True)
class CustomRange:
    Member30: str
    Member40: str
    Member50: str
    Member_gone: str
    commit: str


@dataclass(frozen=True)
class SheetName:
    Member: str
    MemberGone: str
    Commit: str


# [30, '현탱이', 'https://github.com/bhh9860', '구닌', 'python', '']
@dataclass
class Member:
    num: int
    name: str
    gitLink: str
    job: str
    lang: str
    ect: str
    kick: int

    def __str__(self, ) -> str:
        if self.__unknown():
            return 'unknwon Member'
        template = ''
        template += f'[{self.num}]' + f'      {self.name}' + '\n'
        template += f'Git Link : {self.gitLink}\n'
        template += f'Job      : {self.job}\n'
        template += f'My Power : {self.lang}\n'
        template += f'자기소개 : {self.ect}\n'
        return template

    @property
    def simple(self, ) -> str:
        if self.__unknown():
            return 'unknwon Member'
        return f'{self.name} // {self.job} // {self.gitLink}'

    def __unknown(self, ) -> bool:
        return not (bool(self.name) or bool(self.gitLink))


MEMBER_UNKNOWN = Member(0, '', '', '', '', '', 0)


class JandiSpreadsheetManager:
    def __init__(self, gs: Client) -> None:
        self.gs = gs

        self.__customRangeName = CustomRange(**_CustomRange_dict)
        self.__sheetName = SheetName(**_Sheets)

        self.JandiSpreadSheet: Spreadsheet = gs.open("잔디정원사-smart")

        self.memberSheet: Worksheet = self.JandiSpreadSheet.worksheet(
            self.__sheetName.Member
        )

    def getMember(self, name: str, replace_empty=None) -> Member:
        result: Cell = self.memberSheet.find(name, in_column=USER_NAME_COL)

        if not result or not result.value == name:
            return MEMBER_UNKNOWN

        # y, x
        start = rowcol_to_a1(result.row, result.col - 1)
        end = rowcol_to_a1(result.row, result.col - 1 + MEMBER_INFO_width - 1)

        # expected column length
        data = [None for replace_empty in range(MEMBER_INFO_width + 1)]

        reply = self.memberSheet.get_values(
            f'{start}:{end}',
            value_render_option='UNFORMATTED_VALUE'
        )[0]

        emptyFilled = [val if val else dafault for val, dafault in zip_longest(
            reply, data, fillvalue=replace_empty)]
        return emptyFilled

    def getAllMember(self,) -> list([Member]):
        # [<Worksheet '맴버' id:1476414588>, <Worksheet '사라진 맴버' id:1907237778>, <Worksheet '인증' id:1303499944>]
        # print(f'worksheets : {self.JandiSpreadSheet.worksheets()}')

        # a = self.getWorkSheet(self.sheetName.Member).getRange(CustomRange)
        # memberSheet: Worksheet = self.JandiSpreadSheet.worksheet(
        #     self.sheetName.Member
        # )

        # returns by row, with empty cell
        rawMembers = self.memberSheet.get_values(
            self.__customRangeName.Member50,
            value_render_option='UNFORMATTED_VALUE'
        )

        return [Member(*mem) for mem in rawMembers if any(mem[1:])]

    def getWorkSheet(self, sheetName: str) -> Worksheet:
        return self.JandiSpreadSheet.open(sheetName)

    def getRange(self, sheetName: str) -> str:
        pass

    def getCellAddress(self, x: int, y: int):
        return rowcol_to_a1(y, x)


if __name__ == '__main__':
    gs = gspread.service_account(filename=KEY)

    sm = JandiSpreadsheetManager(gs=gs)

    # mem = sm.getAllMember()

    if 1:
        mem = sm.getMember('ccpo')

        print(Member(*mem))

        mem = sm.getMember('디에스')

        print(Member(*mem))
        exit()

    for x in mem:
        print(x)
        print()

    # 나중에는 이렇게 해야한다...!
    # https://docs.gspread.org/en/latest/oauth2.html
    # gs = gspread.service_account(filename=KEY)
    # val = gs.open('시트 이름').sheet1.cell(1, 1).value
    # print(val)

    # sm = JandiSpreadsheetManager(gs)
