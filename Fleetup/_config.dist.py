# Fleetup API Keys
###################
# App Key, generated at http://fleet-up.com/Api/MyApps
# Minimum required permissions are Fittings Read and Doctrines Read
FU_APP_KEY = "fleetup app key"
# API Code, generated at http://fleet-up.com/Api/MyKeys
FU_API_CODE = "fleetup api key"
# User id, shown in api code listing
FU_USER_ID = "fleetup user id"
# Group id, from group view url or via API from /MyGroupMemberships
FU_GROUP_ID = "fleetup group id"
FU_BASE_URL = "http://api.fleet-up.com/Api.svc"
FU_APP_URI = "{}/{}/{}/{}".format(FU_BASE_URL, FU_APP_KEY, FU_USER_ID, FU_API_CODE)