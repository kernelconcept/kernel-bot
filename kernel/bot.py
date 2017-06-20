import discord
import warnings
from discord.ext import commands
from redis import StrictRedis
from kernel import enrich_channel_name, text
from kernel.cogs import admin, general, profile
from kernel import db



SERVER_NAME = "Kernel Concept"
GAME = "réfléchir au sens de la vie"
COMMAND_PREFIXES = ['!']
MESSAGE_DELETE_AFTER = 300.00


class KernelBot(commands.Bot):
    """
    Kernel bot

    This class defines the bot. It keeps settings and events
    since we're just overriding the base Discord bot events.
    """
    def __init__(self,
                 api_token,
                 redis: StrictRedis,
                 test_channel_name: str = 'bot',
                 welcome_channel_name: str = 'salle-commune'):
        super().__init__(COMMAND_PREFIXES,
                         description=text.BOT_DESC,
                         pm_help=True,  # Help don't spam, Help uses private messaging !
                         command_not_found=text.COMMAND_NOT_FOUND,
                         command_has_no_subcommands=text.COMMAND_HAS_NO_SUBCOMMANDS)
        self.redis = redis or db.load()
        self.token = api_token
        self.server_name = SERVER_NAME
        self.test_channel_name = test_channel_name
        self.welcome_channel_name = welcome_channel_name

    @property
    def server(self) -> discord.Server:
        return discord.utils.find(lambda s: s.name == self.server_name, self.servers)

    @property
    def test_channel(self) -> discord.Channel:
        return enrich_channel_name(self.server, self.test_channel_name)

    @property
    def welcome_channel(self) -> discord.Channel:
        return enrich_channel_name(self.server, self.welcome_channel_name)

    def run(self):
        if not self.redis:
            warnings.warn('Redis didn\'t load.')
        self.add_cog(general.ListenersCog(self))
        self.add_cog(general.CommandsCog(self))
        self.add_cog(profile.ProfileCog(self))
        super().run(self.token)
