#  msg 시작이 '!'인 상황

# --event || -e
# --user || -u
# --count || -c
# --commit || -C
# --date || -d
# --duration || -D
# --value || -v


_OPTIONS = {
    '-u': 'user',
    '-e': 'event',
    '-d': 'date',
    '-D': 'duration',
    '-c': 'count',
    '-C': 'commit'
}

# 일단 딕셔너리로...

template = {
    'entry': None,
    'event': None,
    'user': None,
    'date': None,
    'duration': None,
    'count': None,
    'commit': None,
    'value': None
}

# defaultValue if just flag))
# --date || -d = Today, today
# --commit || -c = true, True


class CommandParser:
    def __init__(self, msg: str) -> None:
        self.origin = [x for x in msg.strip().split() if x]
        self.flag = []
        self.parsed = dict(template)
        self.parse()

    def parse(self, ):

        self.parsed['entry'] = self.origin[0].replace('!', '')

        def tune(option: str):
            if(option in _OPTIONS.keys()):
                return _OPTIONS.get(option)
            else:
                return option.replace('--', '')

        for frag in self.origin[1:]:
            a, b = None, None
            # --commit, --date : default = True, today
            if(len(frag.split('=')) != 2):
                if (tune(frag) == 'date'):
                    a, b = 'date', 'today'
                    continue
                if(tune(frag) == 'commit'):
                    a, b = 'commit', True
            else:
                a, b = tune(frag.split('=')[0]), frag.split('=')[1]
            self.parsed[a] = b.replace('_', ' ') if type(b) == str else b


if __name__ == '__main__':
    cmd_user = [
        '!make --user=ccppoo',
        '!make -u=ccppoo',
        '!make --user=ccppoo --commit --date=today',

        '!remove --user=ccppoo',
        '!remove -u=ccppoo --commit --date=today',

        '!get --user=ccppoo',
        '!get -u=ccppoo --commit --date=today',
        '!get -u=ccppoo --commit --date=2021-09-10 --duration=10',

        '!update --user=ccppoo --commit --date=today --value=true'
    ]

    cmd_event = [
        '!make --event=겨울기념_강퇴_이벤트 --date=2021-10-31 --duration=12 --commit=3'
    ]

    for cmd in cmd_user:
        # print("-" * 10)
        parsed = CommandParser(cmd)
        # print(parsed.origin) # print(parsed.parsed)
        assert len(parsed.parsed.keys()) == len(template.keys())
    else:
        print()
        print(f'cmd_user : test ok')
        print()

    for cmd in cmd_event:
        # print("-" * 10)
        parsed = CommandParser(cmd)
        print(parsed.origin)
        print(parsed.parsed)
        assert len(parsed.parsed.keys()) == len(template.keys())
    else:
        print()
        print(f'cmd_event : test ok')
        print()
