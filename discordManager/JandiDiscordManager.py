import discord
import asyncio
if __name__ != '__main__':
    from discordManager.handler.messageHandler import MessageHandler
if __name__ == '__main__':
    from handler.messageHandler import MessageHandler

# User : Discord global user
# Member(Guild Member) : user in specific channel (user with server bound information .i.e roles, nickname, ect)

# Channel : 사용자가 UI를 통해 봤을 때 채팅 채널(방)
# Guild : API 관점으로 봤을 때 Channel(사람 관점) == Guild


class JandiDiscordManager(discord.Client):

    def __init__(self,) -> None:
        super().__init__()
        self.handle = MessageHandler()

    # discord 서버에 접속 했을 때
    async def on_connect(self, ):
        print("I'm Connected!")

    # 디스코드 auth 성공하고 토큰도 확인 받고 났을 때
    # 항상 한번만 호출 되는 것이 아니며, resume 성공/실패 해도 호출 될 수 있다!
    async def on_ready(self, ):
        print("I'm ready!")

    # discord 연결에 실패하거나, 연결을 종료할 때
    async def on_disconnect(self, ):
        print("on disconnect!")

    # https://discordpy.readthedocs.io/en/latest/api.html#discord.on_error
    async def on_error(self, event, *args, **kwargs):
        pass

    async def on_message(self, msg):
        # print(f'msg.author : {msg.author}')  # op...#2123 __str__
        # print(f'msg.author.nick : {msg.author.nick}')   # ccppoo
        # print(f'msg.author.name : {msg.author.name}')   # op....

        if msg.author == self.user:
            return

        if msg.author.nick == r'ccppoo' and msg.content == 'exit':
            await msg.channel.send(f'good bye')
            await self.logout()
            return

        if msg.content.startswith('!'):
            # action : 'make', 'remove', 'get', 'update'
            # reply : ./handler/command_parser.py :: template
            action, reply = self.handle.command(msg)

            msgToSend = ''
            async with msg.channel.typing():
                # await [google spread sheet work ... ]
                await asyncio.sleep(1.0)
            await msg.channel.send(f'{action} : {reply}')

            return

        else:
            action, reply = self.handle.message(msg)

        # await msg.channel.send('Pong')

    async def gspread_action(self, ):
        pass

    async def on_typing(self, channel, user, when):
        pass

    # 메세지 삭제할 때
    async def on_message_delete(self, msg):
        pass

    async def on_message_edit(self, before, after):
        pass

    async def on_member_join(self, member):
        pass

    async def on_member_remove(self, member):
        pass

    async def on_member_update(self, before, after):
        pass

    # guild ~= channle 길드를 생성하거나 길드에 참여할 경우 발동
    async def on_guild_join(self, guild):
        pass

    # 채널에서 나가거나, 쫓겨나거나, 등
    async def on_guild_remove(self, guild):
        pass

    # 이름, timeout, 등 변경사항 있는 경우
    async def on_guild_update(self, before, after):
        pass

    # async def on_guild_role_create(self, role)
    # async def on_guild_role_delete(self, role)
    # async def on_guild_role_update(self, before, after)

    # async def on_group_join(self, channel, user)
    # async def on_group_remove(self, channel, user)


if __name__ == '__main__':
    import json
    fp = open('./secret.json', mode='r')
    secret = json.load(fp)
    JandiDiscordManager().run(secret['bot_token'])
