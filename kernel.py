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
    bot = KernelBot(api_token=token, redis=db)
    while True:  # TODO: Méthode paysanne pour relancer le bot on failure.
        if not bot.is_logged_in:
            bot.run()
