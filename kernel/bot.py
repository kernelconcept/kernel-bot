from discord.ext import commands
from kernel import enrich_channel_name
from .replies import reply
import discord

COMMAND_PREFIXES = ['!']
DESC = """Le bot Discord de Kernel.
Cool, opérationnel, mais ne fait pas de câlins."""
COMMAND_NOT_FOUND = "La commande {} n'existe pas. Désolé."
COMMAND_HAS_NO_SUBCOMMANDS = "La commande {0.name} n'a pas de sous-commandes."
NEW_MEMBER = "Une nouvelle recrue a rejoint nos rangs. \n\n Bienvenue sur {0}, {1.mention} !"
MEMBER_LEAVE = "Tristement, {0.mention} a décidé de quitter nos rangs. Nous ne t'oublierons jamais."
MEMBER_BAN = "Les administrateurs ont fait retentir le marteau ! {0.name} a subi la sentence martiale et nous a quitté."

SERVER_NAME = "Kernel Concept"
GAME = "réfléchir au sens de la vie"


class KernelBot(commands.Bot):
    """
    Kernel bot

    This class defines the bot. It keeps settings and events
    since we're just overriding the base Discord bot events.
    """
    def __init__(self, api_token, test_channel_name: str = 'bot', welcome_channel_name: str = 'salle-commune'):
        super().__init__(COMMAND_PREFIXES,
                         description=DESC,
                         pm_help=True,  # Help don't spam, Help uses private messaging !
                         command_not_found=COMMAND_NOT_FOUND,
                         command_has_no_subcommands=COMMAND_HAS_NO_SUBCOMMANDS)
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

    async def on_ready(self):
        print('Online.')
        await self.change_presence(
            game=discord.Game(name=GAME))

    async def on_member_join(self, member):
        await self.send_message(self.welcome_channel, NEW_MEMBER.format(SERVER_NAME, member))

    async def on_member_remove(self, member):
        await self.send_message(self.welcome_channel, MEMBER_LEAVE.format(member))

    async def on_member_ban(self, member):
        await self.send_message(self.welcome_channel, MEMBER_BAN.format(member))

    async def send_test(self, message):
        await self.send_message(self.test_channel, message)

    def run(self):
        super().run(self.token)
