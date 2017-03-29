"""
Du Python, encore et toujours.

profile.py
"""

from discord.ext import commands
import asyncio_redis


class Badge:
    """
    Badge class
    """

class Person:
    """
    Person class
    """

class Profile:
    """
    Profile cog.
    """

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.redis = self.load() or None


async def load(self, host='127.0.0.1', port=6379):
    try:
        return await asyncio_redis.Connection.create(host=host, port=port)
    except asyncio_redis.exceptions.Error:
        pass  # TODO: Mentionner l'erreur (logging w/ Sentry)
