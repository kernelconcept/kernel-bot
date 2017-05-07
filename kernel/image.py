from PIL import Image, ImageDraw, ImageFont
from urllib.request import Request, urlopen
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
    avatar = Image.open(BASE_DIR + '/pictures/treating.png').resize((944, 944))
    avatar.save(BASE_DIR + '/chocolat.png')
    base.paste(avatar, (573, 6))
    base.save(BASE_DIR + '/pictures/temp_{}.png'.format(id))
    return BASE_DIR + '/pictures/temp_{}.png'.format(id)


def generate_profile(id: str,
                     profile_name: str,
                     profile_title: str,
                     profile_desc: str,
                     avatar: str,
                     profile_thanks: int):
    base = Image.open(BASE_DIR + '/templates/base.png')
    avatar_mask = Image.open(BASE_DIR + '/templates/avatarMask.png').convert('L')
    avatar_link = generate_avatar(avatar, id)
    avatar = Image.open(avatar_link)
    disponibility = Image.open(BASE_DIR + '/templates/disponibility_y.png')
    avatar_ring = Image.open(BASE_DIR + '/templates/avatarBorder.png')
    gradation = Image.open(BASE_DIR + '/templates/gradation.png')
    description_base = Image.open(BASE_DIR + '/templates/descriptionBase.png')
    blue_corner = Image.open(BASE_DIR + '/templates/blueCorner.png')
    orange_corner = Image.open(BASE_DIR + '/templates/orangeCorner.png')
    blue_arrow = Image.open(BASE_DIR + '/templates/blueArrow.png')
    heart = Image.open(BASE_DIR + '/templates/heart.png')

    base.paste(avatar, (0, 0), mask=avatar_mask)
    base.paste(avatar_ring, (0, 0), mask=avatar_ring)
    base.paste(disponibility, (0, 0), mask=disponibility)
    base.paste(gradation, (0, 0), mask=gradation)
    base.paste(description_base, (0, 0), mask=description_base)
    base.paste(blue_corner, (0, 0), mask=blue_corner)
    base.paste(orange_corner, (0, 0), mask=orange_corner)
    base.paste(blue_arrow, (0, 0), mask=blue_arrow)
    base.paste(heart, (0, 0), mask=heart)

    draw = ImageDraw.Draw(base)
    title = ImageFont.truetype(BASE_DIR + '/templates/font.ttf', 120)
    # TODO: size 48, if less than 14 then go for
    subtitle = ImageFont.truetype(BASE_DIR + '/templates/font.ttf', 78)
    numeric = ImageFont.truetype(BASE_DIR + '/templates/font.ttf', 140)
    thanks = ImageFont.truetype(BASE_DIR + '/templates/font.ttf', 78)
    desc = ImageFont.truetype(BASE_DIR + '/templates/font.ttf', 50)
    draw.text((40, 20), '{}'.format(profile_name), font=title, fill=(0, 0, 0, 255))
    draw.text((60, 170), '{}'.format(profile_title), font=subtitle, fill=(100, 100, 100, 255))
    draw.text((35, 566), '{}'.format(profile_thanks), font=numeric, fill=(246, 78, 52, 255))
    draw.text((35, 726), 'Remerciements', font=thanks, fill=(246, 78, 52, 255))
    draw.text((130, 880), 'aaa', font=desc, fill=(255, 255, 255, 255))
    draw.text((190, 940), 'aaa', font=desc, fill=(255, 255, 255, 255))
    draw.text((250, 1000), 'aaa', font=desc, fill=(255, 255, 255, 255))
    draw.text((310, 1060), 'aaa', font=desc, fill=(255, 255, 255, 255))
    base.save(BASE_DIR + '/pictures/{}.png'.format(id))
    os.remove(avatar_link)
    return BASE_DIR + '/pictures/{}.png'.format(id)
