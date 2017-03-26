from os.path import isfile
from kernel.bot import KernelBot


def prompt_token():
    token = open('.token', 'w')
    token.write(
            input('You may paste your bot user token now : '))
    token.close()

if __name__ == '__main__':
    if not isfile('.token'):
        prompt_token()
    token = open('.token', 'r').read()
    KernelBot(api_token=token).run()