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
<<<<<<< HEAD
    bot = KernelBot(api_token=token)
    bot.add_cog(
        Commands(bot)
    )
    bot.add_cog(
        Profile(bot)
    )
    while True:  # TODO: Méthode paysanne pour relancer le bot on failure.
        if not bot.is_logged_in:
            bot.run()
=======
    db = load()
    bot = KernelBot(token, db)
    bot.run()
>>>>>>> e9314225b796755e5e6b58e9bcf2020874809cd2
