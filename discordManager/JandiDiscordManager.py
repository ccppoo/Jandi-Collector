import discord
import asyncio
import json
from builder import *
from discord.member import Member
from discord.guild import Guild
from discord.message import Message
# from discord.channel import ChannelType, TextChannel
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
        intents = discord.Intents.all()

        super().__init__(intents=intents)
        self.handle = MessageHandler()
        self.buildMemo = {}

    # discord 서버에 접속 했을 때
    async def on_connect(self, ):
        print("I'm Connected!")

    # 디스코드 auth 성공하고 토큰도 확인 받고 났을 때
    # 항상 한번만 호출 되는 것이 아니며, resume 성공/실패 해도 호출 될 수 있다!

    async def on_ready(self, ):
        print("I'm ready!")

        # from formats import getGuild, updateGuildInfo, makeFormat
        # import os.path

        # if not os.path.exists('./guilds.json'):
        #     with open('./guilds.json', mode='w') as fp:
        #         json.dump(makeFormat(), fp, indent=4, sort_keys=True)

        # guild_data = None

        # with open('./guilds.json', mode='r+') as fp:
        #     guild_data = json.load(fp)

        # A chunked guild means that member_count is equal to the number of members
        # stored in the internal members cache.

        # for guild in self.guilds:
        #     updateGuildInfo(guild_data, id=guild.id, name=guild.name)
        #     for mem in guild.members:
        #         pass
        # print("for loop end :: self.guilds")

    # discord 연결에 실패하거나, 연결을 종료할 때

    async def on_disconnect(self, ):
        print("on disconnect!")

    # https://discordpy.readthedocs.io/en/latest/api.html#discord.on_error
    async def on_error(self, event, *args, **kwargs):
        pass

    async def build_command(self, msg: Message):
        # !build command already exists or not finished
        # remove all messages generated from last !build command
        if self.buildMemo[str(msg.author)]:
            for msgObj in self.buildMemo[str(msg.author)]['msg']:
                await msgObj.delete()
        else:
            self.buildMemo[str(msg.author)] = startBuilder()

        self.buildMemo[str(msg.author)]['channel'] = msg.channel
        self.buildMemo[str(msg.author)]['author'] = msg.author
        self.buildMemo[str(msg.author)]['msg'] = msg
        self.on_message()

    async def on_message(self, msg: Message):
        # print(f'msg.author : {msg.author}')  # op...#2123 __str__
        # print(f'msg.author.nick : {msg.author.nick}')   # ccppoo
        # print(f'msg.author.name : {msg.author.name}')   # op....

        if msg.author == self.user:
            return

        # await msg.delete()

        if msg.author.nick == r'ccppoo' and msg.content == 'exit':
            await msg.channel.send(f'good bye')
            await self.logout()
            return

        if not msg.content.startwith('!'):
            action, reply = self.handle.message(msg)

        # if command !build is detected, ignore all following options
        if msg.content.startwith('!build'):
            print("!build commmand")
            reply = self.build_command(msg)
            msg.channel.send(reply)
            # 1. make, get, update, remove -select one

            # 2. event, user

            # 3. none, commit
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

        # await msg.channel.send('Pong')

    async def gspread_action(self, ) -> str:
        pass

    async def check_guild_channel(self, ):
        self.get_guild
        pass

    async def on_typing(self, channel, user, when):
        pass

    # 메세지 삭제할 때
    async def on_message_delete(self, msg: Message):
        pass

    async def on_message_edit(self, before, after):
        pass

    async def on_member_join(self, member: Member):
        # member.guild.channels
        pass

    async def on_member_remove(self, member: Member):
        pass

    async def on_member_update(self, before, after):
        pass

    # guild ~= channle 길드를 생성하거나 길드에 참여할 경우 발동
    async def on_guild_join(self, guild: Guild):
        print("on_guild_join")
        JandiChannel = await guild.create_text_channel('잔디관리사', position=1)

    # 채널에서 나가거나, 쫓겨나거나, 등

    async def on_guild_remove(self, guild: Guild):
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

    try:
        JandiDiscordManager().run(secret['bot_token'])
    except RuntimeError as e:
        pass
        # print(e)
