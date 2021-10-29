from json.decoder import JSONDecodeError
import os.path
import json

_memberFormat = {
    "member": [
        {
            "name": None,
            'git': None,
        }
    ]
}

_member_keys = [
    'name', 'git'
]


def getMembers() -> list:

    # return Members from JSON
    return __loadJSON().get('member')


def addMember(name: str, git: str):

    # Save Member at members.json

    data = __loadJSON()
    data['member'].append({
        'name': name,
        'git': git
    })

    return __dumpJSON(data)


def removeMember(name: str):
    idx = None
    for i, mem in enumerate(__loadJSON()['member']):
        if mem['name'] == name:
            idx = i
            break
    if idx:
        json_ = __loadJSON()
        json_['member'].pop(idx)
        __dumpJSON(json_)


def __loadJSON() -> dict:
    with open('members.json', mode='r') as fp:
        return json.load(fp)


def __dumpJSON(json_: dict):
    with open('members.json', mode='w') as fp:
        json.dump(json_, fp, indent=4, sort_keys=True)


def __makeFormat() -> dict:
    return _memberFormat


def __check_valid(info_: dict) -> bool:
    if not info_['member']:
        return False

    return all([x in _member_keys for x in info_.get('member')[0].keys()])


def __makeJSON_members():
    with open('members.json', mode='w') as fp:
        json.dump(_memberFormat, fp, indent=4, sort_keys=True)


def setupJSON_members():
    if not os.path.exists('./members.json'):
        __makeJSON_members()

    flag = False

    with open('members.json', mode='r') as fp:
        try:
            data = json.load(fp)
        except JSONDecodeError:
            # if empty or non json format
            __makeJSON_members()
            return []
        except Exception as e:
            print(f'Exception : {e}')
            exit(-1)
        # not valid format
        if not __check_valid(data):
            flag = True

    if flag:
        __makeJSON_members()


if __name__ == '__main__':
    setupJSON_members()
    print('add mem')
    addMember('ccpop', 'github.com')

    for mem in getMembers():
        print(mem)

    print('remove mem')
    removeMember('ccpop')

    for mem in getMembers():
        print(mem)
