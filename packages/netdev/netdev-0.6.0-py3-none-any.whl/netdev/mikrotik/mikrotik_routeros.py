import asyncssh

from ..base import BaseDevice
from ..exceptions import DisconnectError
from ..logger import logger


class MikrotikRouterOS(BaseDevice):
    """Class for working with Mikrotik RouterOS"""

    def __init__(self, host=u'', username=u'', password=u'', secret=u'', port=22, device_type=u'', known_hosts=None,
                 local_addr=None, client_keys=None, passphrase=None, loop=None):
        """
        Invoke init with some special params (base_pattern and username)

        Mikrotik duplicate prompt in connection, so we should use pattern like
        prompt .* prompt.
        For disabling colors in CLI output we should user this username = username+c
        '+c' disables colors
        '+t' disable auto term capabilities detection
        '+80w' set terminal width to 80 rows
        """
        super(MikrotikRouterOS, self).__init__(host=host, username=username, password=password, secret=secret,
                                               port=port, device_type=device_type, known_hosts=known_hosts,
                                               local_addr=local_addr, client_keys=client_keys, passphrase=passphrase,
                                               loop=loop)

        self._base_pattern = r"\[.*?\] \>.*\[.*?\] \>"
        self._username += '+ct80w'
        self._ansi_escape_codes = True

    async def connect(self):
        """
        Async Connection method

        RouterOS using 2 functions:

        * _establish_connection() for connecting to device
        * _set_base_prompt() for finding and setting device prompt
        """
        logger.info("Host {}: Connecting to device".format(self._host))
        await self._establish_connection()
        await self._set_base_prompt()
        logger.info("Host {}: Connected to device".format(self._host))

    async def _establish_connection(self):
        """Establish SSH connection to the network device"""
        logger.info('Host {}: Establishing connection to port {}'.format(self._host, self._port))
        output = ""
        # initiate SSH connection
        try:
            self._conn = await asyncssh.connect(**self._connect_params_dict)
        except asyncssh.DisconnectError as e:
            raise DisconnectError(self._host, e.code, e.reason)

        self._stdin, self._stdout, self._stderr = await self._conn.open_session(term_type='dumb')
        logger.info("Host {}: Connection is established".format(self._host))
        # Flush unnecessary data
        output = await self._read_until_prompt()
        logger.debug("Host {}: Establish Connection Output: {}".format(self._host, output))
        return output

    async def _set_base_prompt(self):
        """
        Setting two important vars
        * base_prompt - textual prompt in CLI (usually hostname)
        * base_pattern - regexp for finding the end of command. IT's platform specific parameter

        For Mikrotik devices base_pattern is "r"\[.*?\] (\/.*?)?\>"
        """
        logger.info("Host {}: Setting base prompt".format(self._host))
        self._base_pattern = self._get_default_command('pattern')
        prompt = await self._find_prompt()
        user = ''
        # Strip off trailing terminator
        prompt = prompt[1:-3]
        if '@' in prompt:
            prompt = prompt.split('@')[1]
        self._base_prompt = prompt
        logger.debug("Host {}: Base Prompt: {}".format(self._host, self._base_prompt))
        logger.debug("Host {}: Base Pattern: {}".format(self._host, self._base_pattern))
        return self._base_prompt

    async def _find_prompt(self):
        """Finds the current network device prompt, last line only."""
        logger.info("Host {}: Finding prompt".format(self._host))
        self._stdin.write("\r")
        prompt = ''
        prompt = await self._read_until_prompt()
        prompt = prompt.strip()
        if self._ansi_escape_codes:
            prompt = self._strip_ansi_escape_codes(prompt)
        if not prompt:
            raise ValueError("Unable to find prompt: {0}".format(prompt))
        logger.debug("Host {}: Prompt: {}".format(self._host, prompt))
        return prompt

    @staticmethod
    def _normalize_cmd(command):
        """Specific trailing newline for Mikrotik"""
        command = command.rstrip("\n")
        command += '\r'
        return command

    def _get_default_command(self, command):
        """
        Returning default commands for device

        :param command: command for returning
        :return: real command for this network device
        """
        # @formatter:off
        command_mapper = {
            'pattern': r"\[.*?\] (\/.*?)?\>",
        }
        # @formatter:on
        return command_mapper[command]
