from os.path import isfile

def prompt_token():
    token = open('.token', 'w')
    token.write(
            input('You may paste your bot user token now : '))

if __name__ == '__main__':
    if not isfile('.token'):
        prompt_token()
