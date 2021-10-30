# from google.oauth2.service_account import Credentials
from dataclasses import dataclass
from itertools import zip_longest
import gspread
from gspread import Client
from gspread.models import Spreadsheet, Worksheet, Cell
from gspread.utils import a1_to_rowcol, rowcol_to_a1
from typing import NewType
from datetime import datetime

##### ##### ##### ##### ##### #####
# 나중에 실제 DOC 문서를 접근 할 것을 대비해서
# 새로운 sheet에 접근할 수 있는 권한을 어떻게 등록(?) 할 수 있을지 만들기
# ex)
# 디스코드에 봇 추가하고,
# 관리자 권한을 부여받고,
# 관리할 sheet를 등록하는 절차
##### ##### ##### ##### ##### #####

# row, col str
# TODO : gspread - commit A1 static class for Type Hinting
A1 = NewType('A1', str)

KEY = './secret/jandi-manager-key.json'
TITLE = '잔디정원사-smart'
USER_NAME_COL = 3
COMMIT_DATE_ROW_START = 'H7'
MEMBER_INFO_width = 6

_CustomRange_dict = {
    'Member30': 'Members30_with_Kicks',
    'Member40': 'Members40_with_Kicks',
    'Member50': 'Members50_with_Kicks',
    'Member_gone': 'Members_gone_100',
    'commit': '인증목록',
    'commit_dates': 'Commit_date_row'
}

_Sheets = {
    'Member': '맴버',
    'MemberGone': '사라진 맴버',
    'Commit': '인증'
}


# TODO :  gspread - commit Dimension static class for not using 'ROWS', 'COLUMNS'
@dataclass(frozen=True)
class Dimension:
    row: str
    col: str


dimension = Dimension(**{
    'row': 'ROWS',
    'col': 'COLUMNS'
})


@dataclass(frozen=True)
class CustomRange:
    Member30: str
    Member40: str
    Member50: str
    Member_gone: str
    commit: str
    commit_dates: str


@dataclass(frozen=True)
class SheetName:
    Member: str
    MemberGone: str
    Commit: str


# [int, str, str(url), str, str, str]
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

# ## TODO : spearate to util function


def isToday(date_: str) -> bool:
    # get date_:str value from google sheet
    # date format from google is '%Y. %m. %d'

    dateFormat = '%Y. %m. %d'

    dateVal = datetime.strptime(date_, dateFormat).date()

    return dateVal == datetime.today().date()


# TODO : gspread - commit to util function
def a1_shift_rowcol(a1: A1, row: int = 0, col: int = 0) -> A1:
    a = a1_to_rowcol(a1)
    return rowcol_to_a1(a[0] + row, a[1] + col)


# TODO : gspread - commit to util function
# github issue : https://github.com/burnash/gspread/issues/947
def empty_filled(from_: A1, to_: A1, default=None) -> list:
    rf, cf = a1_to_rowcol(from_)
    rt, ct = a1_to_rowcol(to_)

    rows = rt - rf + 1
    cols = ct - cf + 1

    emptyFilled = [[default for _ in range(cols)] for _ in range(rows)]

    return emptyFilled


class JandiSpreadsheetManager:
    # This class interacts with discord bot API
    # Run

    def __init__(self, gs: Client) -> None:
        self.gs = gs

        self.__customRangeName = CustomRange(**_CustomRange_dict)
        self.__sheetName = SheetName(**_Sheets)

        self.JandiSpreadSheet: Spreadsheet = gs.open("잔디정원사-smart")

        self.memberSheet: Worksheet = self.JandiSpreadSheet.worksheet(
            self.__sheetName.Member
        )

        self.commitSheet: Worksheet = self.JandiSpreadSheet.worksheet(
            self.__sheetName.Commit
        )

    # check and compare member from members.json v
    def update_checkMember(self):

        pass

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

        # return by row, with empty cell
        rawMembers = self.memberSheet.get_values(
            self.__customRangeName.Member50,
            value_render_option='UNFORMATTED_VALUE'
        )

        return [Member(*mem) for mem in rawMembers if any(mem[1:])]

    def updateCommit(self, members: list([str]), commited: bool) -> bool:

        # TODO : check member name for typo

        # get today, and search for date coordinate from sheet('인증')

        dates = self.commitSheet.get(
            self.__customRangeName.commit_dates,
            value_render_option='FORMATTED_VALUE'
        )[0]

        dates = [d for d in dates if not d == '-1']

        cell_COL_shift = 0

        for i, d in enumerate(dates):
            if isToday(d):
                cell_COL_shift = i
                break
        else:
            # TODO : return error if Today date doesn't exists
            return False

        #  A1 coord to today
        a1: A1 = a1_shift_rowcol(COMMIT_DATE_ROW_START, col=cell_COL_shift)

        # we know coordinate, check user preventing duplication

        # start coord (search range)
        start = a1_shift_rowcol(a1, row=1)
        # end coord (search range)
        end = a1_shift_rowcol(a1, row=45 + 1)

        searchRange = f'{start}:{end}'

        membersCommited = self.commitSheet.get(
            searchRange,
            value_render_option='FORMATTED_VALUE',
            major_dimension=dimension.col
        )[0]

        print(membersCommited)

        toUpdate = []

        for member in members:
            if member not in membersCommited:
                toUpdate.append(member)

        # we now have number and name of member to update,
        # let's input user nickname to today's commit cells(col)

        a2 = a1_shift_rowcol(start, row=len(membersCommited))
        a3 = a1_shift_rowcol(a2, row=len(toUpdate)-1)

        targetRange = f'{a2}:{a3}'

        # when update, major dimension is always ROW
        self.commitSheet.update(
            targetRange,
            [[nick] for nick in toUpdate]
        )  # ok!

        return True

    def kickMember(self,):
        # move member from sheet('맴버') to sheet('사라진 맴버')
        # if member kicked is not latest member, shift members

        pass

    def __getWorkSheet(self, sheetName: str) -> Worksheet:
        return self.JandiSpreadSheet.open(sheetName)

    def __getRange(self, sheetName: str) -> str:
        pass

    def getCellAddress(self, x: int, y: int):
        return rowcol_to_a1(y, x)


def test():

    a = empty_filled('A1', 'D4')
    from pprint import pprint

    pprint(a, depth=4)


if __name__ == '__main__':
    if False:
        test()
        exit()

    gs = gspread.service_account(filename=KEY)

    sm = JandiSpreadsheetManager(gs=gs)

    # a = sm.memberSheet.get_values(
    #     'sample',
    #     value_render_option='UNFORMATTED_VALUE'
    # )
    a = sm.updateCommit(['sally', 'ccppoo', '현', '냠냠'], True)
    print(a)
    exit()
    a = sm.commitSheet.get(
        'H7:M7',
        value_render_option='FORMATTED_VALUE'
    )

    print(a)

    exit()

    print(Member(mem))

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
