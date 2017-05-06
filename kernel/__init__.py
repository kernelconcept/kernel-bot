import discord
import re


def enrich_channel_name(server: discord.Server, channel_name: str) -> discord.Channel:
    for channel in server.channels:
        if channel.name == channel_name:
            return channel


def enrich_user_id(server: discord.Server, user: str) -> discord.Member:
    if user.startswith('<'):
        user_id = re.sub('[<>@!]', '', user)
    else:
        user_id = user
    for member in server.members:
        check = user_id or user
        if member.id == check:
            return member
