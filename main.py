from discordManager import JandiDiscordManager
import json


def main():

    # since gspread is not async
    # spreadsheetManager and JandiDiscordManager should be run each thread

    return


if __name__ == "__main__":

    fp = open('./secret.json', mode='r')
    secret = json.load(fp)

    print(secret['bot_token'])

    # dm = JandiDiscordManager()
    # dm.run(secret['bot_token'])
