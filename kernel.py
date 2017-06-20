from os import path

from kernel.db import load
from kernel.bot import KernelBot


def prompt_token():
    token = open('.token', 'w')
    token.write(
            input('You may paste your bot user token now : '))
    token.close()

if __name__ == '__main__':
    if not path.isfile('.token'):
        prompt_token()
    token = open('.token', 'r').read()
    db = load()
    bot = KernelBot(db, api_token=token)
    bot.run()
