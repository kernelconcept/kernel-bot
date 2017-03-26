from discord.ext.commands import Bot

COMMAND_PREFIXES = ['!']
DESC = """Le bot Discord de Kernel.
Cool, opérationnel, mais ne fais pas de câlins."""
COMMAND_NOT_FOUND = "La commande {} n'existe pas. Désolé."
COMMAND_HAS_NO_SUBCOMMANDS = "La commande {0.name} n'a pas de sous-commandes."


class KernelBot(Bot):
    def __init__(self, api_token):
        super().__init__(COMMAND_PREFIXES,
                         description=DESC,
                         pm_help=True,  # Help don't spam, Help uses private messaging !
                         command_not_found=COMMAND_NOT_FOUND,
                         command_has_no_subcommands=COMMAND_HAS_NO_SUBCOMMANDS)
        self.token = api_token

    def run(self):
        super().run(self.token)
