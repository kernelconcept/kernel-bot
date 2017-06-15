"""
text.py

Container for text responses.
"""

HUGS = [
    '(づ｡◕‿‿◕｡)づ',
    '(੭ु｡╹▿╹｡)੭ु⁾⁾',
    'c⌒っ╹v╹ )っ',
    '(つ ͡° ͜ʖ ͡°)つ',
    'ʕっ•ᴥ•ʔっ',
    '⊂(◉‿◉)つ',
    '⊂((・▽・))⊃',
    '(っ⇀⑃↼)っ',
    '(.づσ▿σ)づ.',
    '(づ￣ ³￣)づ',
        ]


BOT_DESC = """Le bot Discord de Kernel.
Cool, opérationnel, mais ne fait pas de câlins."""
COMMAND_NOT_FOUND = "La commande {} n'existe pas. Désolé."
COMMAND_HAS_NO_SUBCOMMANDS = "La commande {0.name} n'a pas de sous-commandes."
NEW_MEMBER = "Une nouvelle recrue a rejoint nos rangs. \n\n Bienvenue sur {0}, {1.mention} !"
MEMBER_LEAVE = "Tristement, {0.mention} a décidé de quitter nos rangs. Nous ne t'oublierons jamais."
MEMBER_BAN = "Les administrateurs ont fait retentir le marteau ! {0.name} a subi la sentence martiale et nous a quitté."


# General replies
NO_RIGHTS = "tu n'as pas le droit d'utiliser cette commande."
USER_DOESNT_EXIST = "cet utilisateur n'existe pas (ou je n'ai, du moins, pas réussi à le trouver dans ce channel)."
COMMAND_NO_ARGS_GIVEN = "tu n'as pas donné de paramètres (`!help {}` pourrait t'aider)."
COMMAND_NO_ROLES = "cette commande ne fonctionne pas pour les rôles."
COMMAND_USER_NOT_FOUND = "cette personne n\'existe pas dans ce serveur."
USELESS = "Eh attends. COMMENT ÇA INUTILE ?!"


# Commands replies

# `avatar` command
SELF_AVATAR = "voici ton avatar: {0.avatar_url}."
USER_AVATAR = "voici l'avatar de {0.mention}: {0.avatar_url}."

# `kill` command
KILL = "extinction en cours."

# `whoareyou` command
WHOAREYOU = "Je suis le très rare Kernel Bot aux quatres yeux. Je réponds à tout le monde." \
            "Je vois tout ceux qui sont ici. Je sais ce que vous faites."

# `role` command
ROLE = "{0.mention} a les rôles suivants:```\n"

# Profile related replies

# `init` command
INIT_ONE = "une personne a été ajoutée."
INIT_MULTIPLE = "j\'ai annexé {} nouvelles personnes."
INIT_NOBODY = "la base de données est déjà à jour."

# `reset` command
RESET = "ton profil a bien été remis à zéro."

# `cleanse` command
CLEANSE = "Tout le personnel de Kernel a été éradiqué dans d'horribles souffrances."

# `profile` command
PROFILE_SUCCESS = "{0.mention}, Voilà ton image de profil."
PROFILE_FAILURE = "je n'ai pas réussi à générer ton image."

# `thanks` command
THANKS_SELF = "bien l'amour propre ou ..?"
THANKS_ACTION_MSG = "tu as bien remercié {} ! (déjà remercié {} fois) ```{}```"
THANKS_ACTION = "tu as bien remercié {} ! (déjà remercié {} fois)"
THANKS = "tu as été remercié {} fois !"
THANKS_NONE = "tu n'as jamais été remercié."

# `availability` command
AVAILABILITY_CHANGE = "tu as bien changé ta disponibilité."
AVAILABILITY_TRUE = "{0.name} est défini comme disponible."
AVAILABILITY_FALSE = "{0.name} est défini comme indisponible ou n'a pas spécifié sa disponibilité."
AVAILABILITY_WRONG_ARGS = "tu dois fournir une disponibilité (oui/non) ou un/des utilisateurs."

# `nick` command
HAS_NICK = "{} a le titre de {}."
HAS_SELF_NICK = "tu dispose du titre de {}."
NO_NICK = "cet utilisateur n'a pas de titre."
NO_SELF_NICK = "tu n'as pas de titre, pauvre paysan que tu es."
UPDATED_NICK = "tu as maintenant le titre de {}."
TOO_LONG_NICK = "ton titre doit avoir maximum 24 caractères."
USAGE_NICK = "Tu dois fournir un titre entre guillemets (e.g. : `!titre edit \"Mon titre\"`)"

# `desc` command
HAS_DESC = "description de {} : ```diff\n{}\n```"
HAS_SELF_DESC = "voilà ta description : ```diff\n{}\n```"
NO_DESC = "cet utilisateur n'a pas de description."
NO_SELF_DESC = "tu n'as pas de description."
UPDATED_DESC = "voici ta nouvelle description : ```diff\n{}\n```"
TOO_LONG_DESC = "ta description ne doit pas dépasser 150 caractères."
USAGE_DESC = "tu dois fournir une description entre guillemets (e.g. : `!desc edit \"Ma description\"`)"

# `badge` command

HAS_BADGES = "{} dispose des badges suivants: \n\n{}"
NO_BADGES = "{} n\'a pas de badges."
BADGE_NOT_FOUND = "ce badge n\'existe pas (ou tu n\'as simplement pas donné un ID de badge)."
