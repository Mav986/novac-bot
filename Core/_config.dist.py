# Discord Config
# Bot token, generated via discord developer portal:
BOT_TOKEN = 'BOT-TOKEN-HERE'
# Delay between reads in seconds
BOT_READ_DELAY = 1

# ESI Config
ESI_BASE_URL = 'https://esi.evetech.net'
ESI_DATASOURCE = 'tranquility'
ESI_SWAGGER_JSON = '{}/_latest/swagger.json?datasource={}'.format(ESI_BASE_URL, ESI_DATASOURCE)
ESI_USER_AGENT = 'USER-AGENT-HERE'
