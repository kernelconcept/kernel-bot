from discord.ext import commands
import discord

COMMAND_PREFIXES = ['!']
DESC = """Le bot Discord de Kernel.
Cool, opérationnel, mais ne fait pas de câlins."""
COMMAND_NOT_FOUND = "La commande {} n'existe pas. Désolé."
COMMAND_HAS_NO_SUBCOMMANDS = "La commande {0.name} n'a pas de sous-commandes."
NEW_MEMBER = "Welcome to {0}, {1.mention} !"

SERVER_NAME = "Anaheim Industries"


class KernelBot(commands.Bot):
    """
    Kernel bot

    This class defines the bot. It keeps settings and events
    since we're just overriding the base Discord bot events.
    """
    def __init__(self, api_token, test_channel_string: str = 'bot-test'):
        super().__init__(COMMAND_PREFIXES,
                         description=DESC,
                         pm_help=True,  # Help don't spam, Help uses private messaging !
                         command_not_found=COMMAND_NOT_FOUND,
                         command_has_no_subcommands=COMMAND_HAS_NO_SUBCOMMANDS)
        self.token = api_token
        self.server_name = SERVER_NAME
        self.test_channel_string = test_channel_string

    @property
    def server(self) -> discord.Server:
        return discord.utils.find(lambda s: s.name == self.server_name, self.servers)

    @property
    def test_channel(self) -> discord.Channel:
        for channel in self.server.channels:
            if channel.name == self.test_channel_string:
                return channel

    async def on_ready(self):
        if self.user:
            await self.send_message(self.server, "Hello world!")

    async def on_member_join(self, member):
        await self.send_message(self.server, NEW_MEMBER.format(SERVER_NAME, member))

    async def send_test(self, message):
        await self.send_message(self.test_channel, message)

    def run(self):
        super().run(self.token)
