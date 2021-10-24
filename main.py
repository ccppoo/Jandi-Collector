from discordManager import JandiDiscordManager
import json

if __name__ == "__main__":

    fp = open('./secret.json', mode='r')
    secret = json.load(fp)

    print(secret['bot_token'])

    # dm = JandiDiscordManager()
    # dm.run(secret['bot_token'])
