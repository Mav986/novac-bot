# Discord Config
# Bot token, generated via discord developer portal:
TOKEN = 'BOT TOKEN HERE'
# Delay between reads in seconds
READ_DELAY = 1
# Prefix to use for bot commands
PREFIX = '!'

# ESI Config
ESI_BASE_URL = 'https://esi.evetech.net'
ESI_DATASOURCE = 'tranquility'
ESI_SWAGGER_JSON = '{}/_latest/swagger.json?datasource={}'.format(ESI_BASE_URL, ESI_DATASOURCE)
ESI_USER_AGENT = 'USER AGENT HERE'
