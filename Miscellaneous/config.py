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

WORMHOLE_ATTR_REGEN = "*{wormhole_id}* leads to _{leads_to}_\n" \
                      "*Size*: {jump_mass}\n" \
                      "*Total Mass*: {total_mass} kg\n" \
                      "*Regen*: {regenMass} kg per cycle\n" \
                      "*Lifetime*: {lifetime}h"


JUMP_MASS_CATEGORIES = {
    5000000: "Small",
    20000000: "Medium",
    300000000: "Large",
    1000000000: "Freighter",
    1350000000: "Very Large",
    1480000000: "Very Large",
    1800000000: "Very Large"
}

DESTINATION_CATEGORIES = {
    1: "Class 1 W-Space",
    2: "Class 2 W-Space",
    3: "Class 3 W-Space",
    4: "Class 4 W-Space",
    5: "Class 5 W-Space",
    6: "Class 6 W-Space",
    7: "Highsec",
    8: "Lowsec",
    9: "Nullsec",
    12: "Thera",
    13: "Class 13 W-Space",
    14: "the Sentinel Drifter Wormhole",
    15: "the Barbican Drifter Wormhole",
    16: "the Vidette Drifter Wormhole",
    17: "the Conflux Drifter Wormhole",
    18: "the Redoubt Drifter Wormhole"
}
