import discord


def enrich_channel_name(server: discord.Server, channel_name: str) -> discord.Channel:
    for channel in server:
        if channel.name == channel_name:
            return channel


def enrich_user_id(server: discord.Server, user_id: str) -> discord.Member:
    for member in server.members:
        if member.id == user_id:
            return member
