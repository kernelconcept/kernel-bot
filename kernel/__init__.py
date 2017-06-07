import discord
import time
import re


def fetch_users_from_role(server: discord.Server, role):
    output = []
    for member in server.members:
        for serverrole in member.roles:
            if serverrole.id == role.id:
                output.append(member)
    return output


def has_admin(server: discord.Server, user: discord.Member, admin_role: str = 'admin') -> bool:
    for role in user.roles:
        if role == enrich_role_name(server, admin_role):
            return True
    return False


def enrich_channel_name(server: discord.Server, channel_name: str) -> discord.Channel:
    for channel in server.channels:
        if channel.name == channel_name:
            return channel


def enrich_role_id(server: discord.Server, role_id: str) -> discord.Role:
    if role_id.startswith('<'):
        role_id = re.sub('[<>@!&]', '', role_id)
    for role in server.roles:
        check = role_id
        if role.id == check:
            return role


def enrich_role_name(server: discord.Server, role_name: str) -> discord.Role:
    for role in server.roles:
        if role.name.upper() == role_name.upper():
            return role


def enrich_user_id(server: discord.Server, user: str) -> discord.Member:
    if user.startswith('<'):
        user_id = re.sub('[<>@!]', '', user)
    else:
        user_id = user
    for member in server.members:
        check = user_id or user
        if member.id == check:
            return member


def enrich_emoji(server: discord.Server, emoji_name: str) -> discord.Emoji:
    for emoji in server.emojis:
        if emoji.name == emoji_name:
            return emoji