from Corp._config import *
import requests

class CorpBot:
    def __init__(self, slackbot):

        # I'd rather use try/catches for invalid arguments, but was in a hurry when I wrote this
        @slackbot.command('srp', help='Submit for SRP from within slack. {}'.format(SRP_USAGE))
        def srp(channel, arg):
            if arg:
                args = arg.split(",", 2)
                kill_url = None
                other_comments = None
                if len(args) >= 2:
                    pilot_name = args[0]
                    if ZKILL_FORMAT in args[1]:
                        kill_url = args[1].strip().replace('<', '').replace('>', '')
                    else:
                        message = 'Invalid lossmail, please try again.'.format(SRP_USAGE)
                    if len(args) == 3:
                        other_comments = args[2].strip()
                    if pilot_name and kill_url:
                        requests.post(SRP_URL.format(name=pilot_name, killmail_url=kill_url, extra_info=other_comments))
                        message = "SRP submitted."
                else:
                    message = 'Invalid arguments. {}'.format(SRP_USAGE)
            else:
                message = 'Invalid arguments. {}'.format(SRP_USAGE)

            return slackbot.post_message(channel, message)
