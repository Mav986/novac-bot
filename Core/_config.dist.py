# Slack Config
# Bot token, generated via slack custom integrations
SLACK_BOT_TOKEN = 'BOT-TOKEN-HERE'
# UserID for the bot.
SLACK_BOT_ID = 'BOT-ID-HERE'
# Maximum connection retries
SLACK_BOT_MAX_RETRIES = 5
# Delay between reads in seconds
SLACK_BOT_READ_DELAY = 1

# ESI Config
ESI_BASE_URL = 'https://esi.evetech.net'
ESI_DATASOURCE = 'tranquility'
ESI_SWAGGER_JSON = '{}/_latest/swagger.json?datasource={}'.format(ESI_BASE_URL, ESI_DATASOURCE)
ESI_USER_AGENT = 'USER-AGENT-HERE'
