from discord.ext.commands import Bot
from asyncio import coroutine
import discord

COMMAND_PREFIXES = ['!']
DESC = """Le bot Discord de Kernel.
Cool, opérationnel, mais ne fait pas de câlins."""
COMMAND_NOT_FOUND = "La commande {} n'existe pas. Désolé."
COMMAND_HAS_NO_SUBCOMMANDS = "La commande {0.name} n'a pas de sous-commandes."
NEW_MEMBER = "Welcome to {0}, {1.mention} !"

SERVER_NAME = "Anaheim Industries"


class KernelBot(Bot):
    def __init__(self, api_token):
        super().__init__(COMMAND_PREFIXES,
                         description=DESC,
                         pm_help=True,  # Help don't spam, Help uses private messaging !
                         command_not_found=COMMAND_NOT_FOUND,
                         command_has_no_subcommands=COMMAND_HAS_NO_SUBCOMMANDS)
        self.token = api_token
        self.server_name = SERVER_NAME

    @property
    def server(self) -> discord.Server:
        return discord.utils.find(lambda s: s.name == self.server_name, self.servers)

    async def on_ready(self):
        if self.user:
            await self.send_message(self.server, "Hello world!")

    async def on_member_join(self, member):
        await self.send_message(self.server, NEW_MEMBER.format(SERVER_NAME, member))

    def run(self):
        super().run(self.token)
