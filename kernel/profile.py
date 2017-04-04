"""
Du Python, encore et toujours.

profile.py
"""

from raven import Client
from discord.ext import commands
from typing import List
import asyncio_redis

sentry = Client('https://62ffbf83e1204334ae60fd85305239f2:c8033d9c0312464f87593d93b7040a11@sentry.io/154891')

LIVE_PERSONS = []


class Project:
    """
    Project class
    """
    def __init__(self):
        pass


class Badge:
    """
    Badge class
    """
    def __init__(self):
        pass


class Person:
    """
    Person class
    """
    def __init__(self, discord_id: str, redis):
        self.discord_id = discord_id
        self.redis = redis
        self.last_recorded_name: str = None
        self.thanks_count: int = None
        self.project_status: bool = False
        self.complete_projects: int = None
        self.message_count: int = None
        self.title: str = None
        self.desc: str = None
        self.badges: List = []

        LIVE_PERSONS.append(self)


class Profile:
    """
    Profile cog.
    """

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.redis = self.load() or None

    async def load(self, host='127.0.0.1', port=6379):
        """
        Create a connection to redis.

        :param host: Redis' server IP
        :param port: Redis' server port
        :return: Redis connection object.
        """
        try:
            connection = await asyncio_redis.Connection.create(host=host, port=port)
            return connection
        except asyncio_redis.exceptions.Error:
            sentry.captureMessage('Could not initiate a connection to Redis.')

    @commands.command(pass_context=True)
    async def init(self, ctx: commands.Context):
        pass

    @commands.command(pass_context=True)
    async def reset(self, ctx: commands.Context):
        pass

    @commands.command(pass_context=True)
    async def thanks(self, ctx: commands.Context, member):
        pass

    @commands.command(pass_context=True)
    async def available(self, ctx: commands.Context, member):
        pass

    @commands.command(pass_context=True)
    async def nick(self, ctx: commands.Context, member):
        pass

    @commands.command(pass_context=True)
    async def desc(self, ctx: commands.Context, member):
        pass

    @commands.command(pass_context=True)
    async def badge(self, ctx: commands.Context, member):
        pass
