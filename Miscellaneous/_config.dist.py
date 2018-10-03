# REDDIT CONFIG
ID = 'ID-HERE'
SECRET = 'SECRET-HERE'
CONTACT_INFO = 'CONTACT-INFO-HERE'
AGENT = 'NovacBot for No-Vacancies: {}'.format(CONTACT_INFO)
REDDIT_WHITELIST = ('.gifv', '.gif', 'gfycat.com', 'i.redd.it', '.jpg', '.png', 'imgur.com')
MAX_POSTS = 5
MAX_INDEX = MAX_POSTS - 1
SUBREDDIT = 'Eyebleach'

# USAGE STRINGS
XKCD_USAGE = 'Usage: *!xkcd* _OR_ *!xkcd #*'
NICE_USAGE = 'Usage: *really?*'
EIGHTBALL_USAGE = 'Usage: *!8ball [question]?*'
FLUFF_USAGE = 'Usage: *!fluff*'

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
