from Corp._config import *
from Corp.controller import submit_srp, valid_lossmail


class CorpBot:
    def __init__(self, slackbot):

        @slackbot.command('srp', help='Submit for SRP from within slack. {}'.format(SRP_USAGE))
        def srp(channel, arg):
            try:
                args = arg.split(",", 2)
                url = args[1].strip().replace('<', '').replace('>', '')
                if valid_lossmail(url):
                    if len(args) == 3:
                        submit_srp(args[0], args[1], args[2])
                    else:
                        submit_srp(args[0], args[1])
                    message = "SRP submitted."
                else:
                    message = 'Invalid lossmail, please try again.'.format(SRP_USAGE)
            except (AttributeError, IndexError):  # If user doesn't enter 2 or 3 arguments (CSV's)
                    message = 'Invalid arguments. {}'.format(SRP_USAGE)

            return slackbot.post_message(channel, message)
