from PIL import Image, ImageDraw, ImageFont
from urllib.request import Request, urlopen
from textwrap import wrap
import os

BASE_DIR = os.path.dirname(os.path.realpath(__file__)) + '/..'

HEADERS = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
           'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
           'Accept-Encoding': 'none',
           'Accept-Language': 'en-US,en;q=0.8',
           'Connection': 'keep-alive'}


def generate_avatar(avatar_url, id):
    base = Image.open(BASE_DIR + '/templates/base.png')
    r = Request(avatar_url, headers=HEADERS)
    content = urlopen(r).read()
    with open(BASE_DIR + '/pictures/treating.png', mode='wb+') as f:
        f.write(content)
        f.close()
    avatar = Image.open(BASE_DIR + '/pictures/treating.png').resize((1148, 1148))
    base.paste(avatar, (0, 0))
    base.save(BASE_DIR + '/pictures/temp_{}.png'.format(id))
    return BASE_DIR + '/pictures/temp_{}.png'.format(id)


def generate_profile(id: str,
                     profile_name: str,
                     profile_title: str,
                     profile_desc: str,
                     profile_disp: bool,
                     avatar: str,
                     profile_thanks: int):
    base = Image.open(BASE_DIR + '/templates/baseWhite.png')
    avatar_mask = Image.open(BASE_DIR + '/templates/avatarMask.png').convert('L')
    avatar_link = generate_avatar(avatar, id)
    avatar = Image.open(avatar_link)

    if profile_disp:
        disponibility = Image.open(BASE_DIR + '/templates/disponibility_y.png')
    else:
        disponibility = Image.open(BASE_DIR + '/templates/disponibility.png')
    if profile_thanks < 10:
        thanks_x = 55
    elif profile_thanks < 100:
        thanks_x = 110
    else:
        thanks_x = 165
    top_layer = Image.open(BASE_DIR + '/templates/topLayer.png')
    base.paste(avatar, (0, 0), mask=avatar_mask)
    base.paste(disponibility, (0, 0), mask=disponibility)
    base.paste(top_layer, (0, 0), mask=top_layer)
    draw = ImageDraw.Draw(base)
    title = ImageFont.truetype(BASE_DIR + '/templates/font-bold.ttf', 80)
    caps_title = ImageFont.truetype(BASE_DIR + '/templates/font-bold.ttf', 60)
    subtitle = ImageFont.truetype(BASE_DIR + '/templates/font-italic.ttf', 60)
    thanks = ImageFont.truetype(BASE_DIR + '/templates/font.ttf', 78)
    thanks_little = ImageFont.truetype(BASE_DIR + '/templates/font.ttf', 50)
    desc = ImageFont.truetype(BASE_DIR + '/templates/font.ttf', 45)
    draw.text((1150, 110), '{}'.format(profile_name[0].upper()), font=title, fill=(255, 255, 255, 255))
    draw.text((1205, 129), '{}'.format(profile_name[1:].upper()), font=caps_title, fill=(255, 255, 255, 255))
    draw.text((1150, 200), '{}'.format(profile_title), font=subtitle, fill=(100, 100, 100, 255))
    draw.text((1080, 990), '{}'.format(profile_thanks), font=thanks, fill=(246, 78, 52, 255))
    draw.text((1090 + thanks_x, 990), 'R'.format(profile_thanks), font=thanks, fill=(246, 78, 52, 255))
    draw.text((1145 + thanks_x, 1015), 'EMERCIEMENTS'.format(profile_thanks), font=thanks_little, fill=(246, 78, 52, 255))
    description = wrap(profile_desc, width=38)
    base_y = 300
    for line in description:
        draw.text((1150, base_y), '{}'.format(line), font=desc, fill=(0, 153, 204, 255))
        base_y += 70
    base.save(BASE_DIR + '/pictures/{}.png'.format(id))
    os.remove(avatar_link)
    return BASE_DIR + '/pictures/{}.png'.format(id)
