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
    avatar_w, avatar_h = avatar.size
    base_w, base_h = base.size
    pos_x = (base_w-avatar_w)//2
    base.paste(avatar, (pos_x, 24))
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
    if len(profile_name) <= 8:
        name_font = 120
        title_v = 170
    elif len(profile_name) <= 10:
        name_font = 100
        title_v = 140
    elif len(profile_name) <= 14:
        name_font = 80
        title_v = 120
    else:
        name_font = 40
        title_v = 80
    if len(profile_title) <= 14:
        title_font = 78
    else:
        title_font = 48
    top_layer = Image.open(BASE_DIR + '/templates/topLayer.png')
    base.paste(avatar, (0, 0), mask=avatar_mask)
    base.paste(top_layer, (0, 0), mask=top_layer)
    base.paste(disponibility, (0, 0), mask=disponibility)
    draw = ImageDraw.Draw(base)
    title = ImageFont.truetype(BASE_DIR + '/templates/font.ttf', name_font)
    subtitle = ImageFont.truetype(BASE_DIR + '/templates/font.ttf', title_font)
    numeric = ImageFont.truetype(BASE_DIR + '/templates/font.ttf', 140)
    thanks = ImageFont.truetype(BASE_DIR + '/templates/font.ttf', 78)
    desc = ImageFont.truetype(BASE_DIR + '/templates/font.ttf', 50)
    draw.text((40, 20), '{}'.format(profile_name), font=title, fill=(0, 0, 0, 255))
    draw.text((60, title_v), '{}'.format(profile_title), font=subtitle, fill=(100, 100, 100, 255))
    draw.text((35, 566), '{}'.format(profile_thanks), font=numeric, fill=(246, 78, 52, 255))
    draw.text((35, 726), 'Remerciements', font=thanks, fill=(246, 78, 52, 255))
    draw.text((130, 880), 'aaa', font=desc, fill=(255, 255, 255, 255))
    draw.text((190, 940), 'aaa', font=desc, fill=(255, 255, 255, 255))
    draw.text((250, 1000), 'aaa', font=desc, fill=(255, 255, 255, 255))
    draw.text((310, 1060), 'aaa', font=desc, fill=(255, 255, 255, 255))
    base.save(BASE_DIR + '/pictures/{}.png'.format(id))
    os.remove(avatar_link)
    return BASE_DIR + '/pictures/{}.png'.format(id)
