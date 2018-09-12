import random
import time

from Core._config import SLACK_BOT_MAX_RETRIES, SLACK_BOT_READ_DELAY
from Core.personalities import personalities

# PREFIX = '<@{}>'.format(SLACK_BOT_ID)
PREFIX = '!'


class Slackbot:
    def __init__(self, slack_client, logger):
        self.slack_client = slack_client
        self._logger = logger
        self._commands = {}
        self._aliases = {}
        self._command_help = {}
        self._retries = 0
        self.personality = None

    def run(self):
        """
        Attempt to connect to slack and start handling commands. Read delay set in config
        """
        running = self._auto_reconnect(self.slack_client.rtm_connect())
        while running:
            try:
                self._process_events()
                time.sleep(SLACK_BOT_READ_DELAY)
            except KeyboardInterrupt:
                self._logger.info('Received Keyboard interrupt.')
                running = False
            except Exception as e:
                self._logger.exception(e)
                running = self._auto_reconnect(self.slack_client.rtm_connect())

    def command(self, command_name, **kwargs):
        """
        Command decorator. Registers chat commands and their help entires.
        :param command_name: Chat command to trigger the function
        :param kwargs: Possible optional args: `help`: String containing detailed help entry.
        :return: Function decorator to run command.
        """

        def decorator(f):
            if 'help' in kwargs:
                self._command_help[command_name] = kwargs['help']
            if 'aliases' in kwargs and (isinstance(kwargs['aliases'], tuple) or isinstance(kwargs['aliases'], list)):
                for alias in kwargs['aliases']:
                    self._aliases[alias] = command_name
            self._commands[command_name] = f
            return f

        return decorator

    def personality_message(self, command, default):
        if not self.personality:
            return default
        if not "replies" in self.personality.keys():
            return default
        if not command in self.personality["replies"].keys():
            return default
        return random.choice(self.personality["replies"][command])

    def _handle_command(self, command, channel, arg):
        """
        Executes command function if command is registered.
        :param command: Name of the command
        :param channel: Channel the command was called from
        :param arg: Any text after the command text
        :return: Return value of the command function called.
        :raises ValueError: If a message is parsed as a command, but the command is not recognized.
        """
        self.personality = random.choice(personalities)
        command_function = self._commands.get(command)
        if not command_function:
            command_function = self._commands.get(self._aliases.get(command, ''))
        if command_function:
            self._logger.info('Received command %s with arg %s in channel %s', command, arg, channel)
            return command_function(channel, arg)
        else:
            self._logger.info('Received invalid command %s', command)
            message = self.personality_message('unknown_command',
                                               'Command "{}" not recognized. `help` to show supported commands.'.format(
                                                   command))
            raise ValueError(message)

    def _parse_slack_output(self, slack_rtm_output):
        """
        Takes the output from `SlackClient.rtm_read()`. If it is prefixed as a command (e. g. @bot-name), the command
        gets split into command name and arg and a 3-tuple of command name, argument and channel is returned.
        :param slack_rtm_output: Dictionary returned by `SlackClient.rtm_read()`
        :return: 3-tuple of command, argument and channel
        """
        if slack_rtm_output and len(slack_rtm_output) > 0:
            for output in slack_rtm_output:
                if output and 'text' in output and output['text'].startswith(PREFIX):
                    text = output['text'].split(PREFIX)[1].strip()
                    tokens = text.split(' ', 1)
                    # This could be done much nicer, but it'll do for now.
                    # consider supplying a pattern via the command decorator
                    if len(tokens) == 2:
                        command, arg = tokens[0], tokens[1]
                    else:
                        command, arg = tokens[0], None
                    return command, arg, output['channel']
        return None, None, None

    def post_message(self, channel, text, as_user=True, **kwargs):
        """
        Post a message to a slack channel.
        :param channel: Channel ID of the target channel
        :param text: Raw text of the message. Required if no attachments provided
        :param as_user: Whether the authed bot identity should be used.
        :param kwargs: Additional parameters. For full list, check chat.postMessage Slack API docs [here](https://api.slack.com/methods/chat.postMessage)
        :return: Output of the slack api call.
        """
        if self.personality:
            if self.personality.get("icon_emoji"):
                return self.slack_client.api_call("chat.postMessage", channel=channel, text=text, as_user=False,
                                                  username=self.personality.get("name", "Bot"),
                                                  icon_emoji=self.personality.get("icon_emoji", ":robot_face:"))
            else:
                return self.slack_client.api_call("chat.postMessage", channel=channel, text=text, as_user=False,
                                                  username=self.personality.get("name", "Bot"),
                                                  icon_url=self.personality.get("icon_url"))

        return self.slack_client.api_call("chat.postMessage", channel=channel, text=text, as_user=as_user, **kwargs)

    def _auto_reconnect(self, running):
        """
        Validates Slack RTM connection, attempts to reconnect if connection fails.
        :param running: Boolean return of SlackClient.rtm_connect()
        :return: Boolean connection status after retrying.
        """
        while not running:
            if self._retries < SLACK_BOT_MAX_RETRIES:
                self._retries += 1
                try:
                    # Delay for increasing amounts of time after failed reconnect in case of longer outages.
                    current_delay = (self._retries + (self._retries - 1)) * 5
                    time.sleep(current_delay)
                    running = self.slack_client.rtm_connect()
                except KeyboardInterrupt:
                    self._logger.info('Received Keyboard interrupt.')
                    break
            else:
                self._logger.error("Max retries exceeded")
                break

        if running:
            self._logger.info('Connection successful after %s retries', self._retries)
            # reset retries after successful connection
            self._retries = 0

        return running

    def _process_events(self):
        """
        Parse slack output and trigger command handling if message looks like a command.
        :return: Return of command function or post message if command not recognized.
        """
        command, arg, channel = self._parse_slack_output(self.slack_client.rtm_read())

        if command and channel:
            try:
                return self._handle_command(command, channel, arg)
            except ValueError as e:
                # ValueError if message looks like a command but command isn't recognized.
                return self.post_message(channel, str(e))

    def set_typing(self, channel):
        """
        Send "typing" status message to a channel
        :param channel: Channel ID of the channel
        :return: n/a
        """
        self.slack_client.server.send_to_websocket({'id': 1, 'type': 'typing', 'channel': channel})

    def _get_user(self, user_id):
        """
        Get a user from the list of all current users
        :param user_id: integer representing the id to search for
        :return: either the user entry matching the user id, or None
        """
        for user_entry in self.slack_client.api_call('users.list')['members']:
            if user_id in user_entry['id']:
                return user_entry

        return None
