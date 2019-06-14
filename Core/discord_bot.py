import random
import time

from Core._config import READ_DELAY, PREFIX
from Core.personalities import personalities


class DiscordBot:
    def __init__(self, client, logger):
        self.client = client
        self._logger = logger
        self._commands = {}
        self._aliases = {}
        self._command_help = {}
        self._retries = 0
        self.personality = None

    def run(self, token):
        """
        Attempt to connect to discord and set up initial event handlers. Read delay set in config
        """

        @self.client.event
        async def on_ready():
            self._logger.info('Connection established!')

        @self.client.event
        async def on_message(ctx):
            if not ctx.author.bot:
                try:
                    await self._process_events(ctx)
                    time.sleep(READ_DELAY)
                except KeyboardInterrupt:
                    self._logger.info('Received Keyboard interrupt.')
                except Exception as e:
                    self._logger.exception(e)

        self.client.run(token)

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

    async def _handle_command(self, command, channel, arg, user):
        """
        Executes command function if command is registered.
        :param command: Name of the command
        :param channel: Channel the command was called from
        :param arg: Any text after the command text
        :return: Return value of the command function called.
        :raises ValueError: If a message is parsed as a command, but the command is not recognized.
        """
        self.personality = random.choice(personalities)
        command = command.lower()
        command_function = self._commands.get(command)
        if not command_function:
            command_function = self._commands.get(self._aliases.get(command, ''))
        if command_function:
            self._logger.info('Received command %s with arg %s in channel %s from %s', command, arg, channel, user)
            await channel.trigger_typing()
            return await command_function(channel, arg, user)
        else:
            self._logger.info('Received invalid command %s', command)
            message = 'Command "{}" not recognized. `help` to show supported commands.'.format(command)
            raise ValueError(message)

    async def _parse_output(self, ctx):
        """
        Parses the text received from discord. If it is prefixed as a command (e. g. !command), the command
        gets split into command name and arg and a 4-tuple of command name, argument, channel, user is returned.
        :param ctx: Message disctionary received from Discord
        :return: 4-tuple of command, args, channel, and user
        """
        content = ctx.content
        if content and len(content) > 0:
            if content.strip().startswith(PREFIX):
                text = content.split(PREFIX, 1)[1].strip()
                tokens = text.split(' ', 1)
                # This could be done much nicer, but it'll do for now.
                # consider supplying a pattern via the command decorator
                if len(tokens) == 2:
                    command, arg = tokens[0], tokens[1]
                else:
                    command, arg = tokens[0], None
                return command, arg, ctx.channel, ctx.author
        return None, None, None, None

    async def post_message(self, channel, text, embed=None):
        """
        Post a message to a discord channel.
        :param channel: Channel ID of the target channel
        :param text: Raw text of the message. Required if no attachments provided
        :param embed: An Embed object
        :return: The sent message
        """
        if embed:
            return await channel.send(text, embed=embed)
        else:
            return await channel.send(text)

    async def _process_events(self, ctx):
        """
        Parse discord output and trigger command handling if message looks like a command.
        :return: Return of command function or post message if command not recognized.
        """
        command, arg, channel, user = await self._parse_output(ctx)

        if command and channel:
            try:
                return await self._handle_command(command, channel, arg, user)
            except ValueError as e:
                # ValueError if message looks like a command but command isn't recognized.
                return await self.post_message(channel, str(e))
