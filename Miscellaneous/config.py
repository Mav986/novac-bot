# USAGE STRINGS
XKCD_USAGE = 'Usage: *!xkcd* _OR_ *!xkcd #*'
NICE_USAGE = 'Usage: *really?*'
EIGHTBALL_USAGE = 'Usage: *!8ball [question]?*'
STATUS_USAGE = 'Usage: !status or !status sisi'
WH_USAGE = 'Usage: *!wh X###* eg. !wh H296'

# MISC
EIGHTBALL_VALID_QUESTION = [
    'It is certain.',
    'It is decidedly so.',
    'Without a doubt.',
    'Yes, definitely.',
    'You may rely on it.',
    'Reply hazy, try again.',
    'Ask again later.',
    'Cannot predict now.',
    'Concentrate and ask again.',
    'Don\'t count on it.',
    'My reply is no.',
    'My sources say no.',
    'Outlook not so good.',
    'Very doubtful.'
]

EIGHTBALL_INVALID_QUESTION = [
    'Was that supposed to be a question?',
    'No you.',
    'I\'ve met toasters who could speak english better than that.',
    'Cmon, you can do better than that.',
    'I\'m an 8ball, not a translator.'
]


DOOSTER_PHRASES = [
    'Nice',
    'Get lit',
    ':350:',
    'What happened?',
    'P gud p gud',
    'Tama. Tama tama tama. Tama?',
    'Sorry for feed',
    'Mhm'
]


K162ERROR = "_Have you become trapped?_ :ghost:"


WORMHOLE_ATTR = "*{wormhole_id}* leads to _{leads_to}_\n" \
                "*Size*: {jump_mass}\n" \
                "*Total Mass*: {total_mass} kg\n" \
                "*Lifetime*: {lifetime}h"


JUMP_MASS_CATEGORIES = {
    5000000: "Small",
    20000000: "Medium",
    300000000: "Large",
    1000000000: "Freighter",
    1350000000: "Very Large",
    1800000000: "Very Large"
}
