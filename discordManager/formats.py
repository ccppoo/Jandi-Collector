import os.path
import json

_guildFormat = {
    "guild": [
        {
            "name": None,
            'id': 0,
            "users": [
                {
                    "name": None,
                    "nick": None,
                    "id": None,
                    "roles": []
                }
            ]
        }
    ]
}

_guild_keys = [
    'name',
    'id',
]

_user_keys = [
    'guild_name', 'users',
]


def __check_valid(info_: dict) -> bool:

    if "guild" not in info_.keys():
        return False

    if not info_['guild']:
        return False

    valid1 = all([x in _guild_keys for x in info_['guild'].keys()])

    if info_.get('guild'):
        valid2 = all([x in _user_keys for x in info_.get('guild')[0].keys()])
    else:
        valid2 = True

    return valid1 and valid2


def __make_field(info_: dict) -> dict:

    if "guild" not in info_.keys():
        info_['guild'] = []

    if not info_['guild']:
        from copy import deepcopy
        field = deepcopy(_guildFormat['guild'][0])

        info_["guild"] = [
            field
        ]

    return info_


def makeFormat() -> dict:
    return _guildFormat


def getGuild(info: dict) -> dict:

    if __check_valid(info):
        pass


def updateGuildInfo(info: dict, id: int, name: str,):
    if not __check_valid(info):
        info = __make_field(info)


if __name__ == '__main__':

    print(os.path.exists('./guilds.json'))

    with open('./guilds.json', mode='w') as fp:
        json.dump(_guildFormat, fp, indent=4, sort_keys=True)

    exit()
    import pprint
    a = __make_field({})
    pprint.pprint(a)
