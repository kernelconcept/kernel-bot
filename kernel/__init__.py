import discord
import re


def enrich_channel_name(server: discord.Server, channel_name: str) -> discord.Channel:
    for channel in server:
        if channel.name == channel_name:
            return channel


def enrich_user_id(server: discord.Server, user_id: str) -> discord.Member:
    if user_id.startswith('<'):
        user = re.sub('[<>@!]', '', user_id)
    for member in server.members:
        check = user or user_id
        if member.id == check:
            return member
