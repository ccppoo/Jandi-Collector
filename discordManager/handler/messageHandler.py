# Every Function must work as pure function

import typing
from discord.message import Message

if __name__ != '__main__':
    try:
        from discordManager.handler.command_parser import CommandParser
    except:
        from handler.command_parser import CommandParser
if __name__ == '__main__':
    from command_parser import CommandParser

Action = typing.NewType('Action', str)
Options = typing.NewType('Options', dict)


# sync, but never interacts
class MessageHandler:
    def __init__(self) -> None:
        pass

    def message(self, msgObject: Message) -> tuple([Action, str]):
        # msgObject.content
        return (None, '')

    def command(self, msgObject: Message) -> tuple([Action, Options]):
        temp = CommandParser(msgObject.content)
        return (temp.parsed['entry'], temp.parsed)


if __name__ == '__main__':

    class dummy:
        def __init__(self) -> None:
            self.content = '!make --event=겨울기념_강퇴_이벤트 --date=2021-10-31 --duration=12 --commit=3'

    mh = MessageHandler()

    mh.command(dummy())

    def test():
        pass
