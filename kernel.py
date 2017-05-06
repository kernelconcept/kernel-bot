from os import path
from kernel.commands import Commands
from kernel.profile import Profile
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
    bot = KernelBot(api_token=token)
    bot.add_cog(
        Commands(bot)
    )
    bot.add_cog(
        Profile(bot)
    )
    bot.run()
