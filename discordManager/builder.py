from handler.command_parser import template


def startBuilder() -> dict:
    template_ = dict(template)

    template_['channel'] = ''
    template_['author'] = ''
    template_['msg'] = []
    return template_


# {
#     ...
#     'msg': [
#         discord.message.Message
#     ]
# }
