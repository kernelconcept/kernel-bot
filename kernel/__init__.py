import discord
import re


def enrich_channel_name(server: discord.Server, channel_name: str) -> discord.Channel:
    for channel in server.channels:
        if channel.name == channel_name:
            return channel


def enrich_role_name(server: discord.Server, role_name: str) -> discord.Role:
    for role in server.roles:
        if role.name == role_name:
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