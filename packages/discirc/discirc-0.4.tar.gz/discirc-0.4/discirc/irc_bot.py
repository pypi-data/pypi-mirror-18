#! /usr/bin/env python3
# -*- coding: utf-8 -*-

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
    IRC bot
    -------

    IRC bot for DiscIRC app
"""

import bottom
import random
import discirc.signals as SIGNALNAMES

from blinker import signal
from discirc.message import Message


__author__ = 'TROUVERIE Joachim'


class IRCBot(bottom.Client):
    """IRC bot wrapper

    :param config: config for bot
    :type config: dict
    """

    COLOR_PREF = '\x03'
    CANCEL = '\u000F'
    
    def __init__(self, config):
        super(IRCBot, self).__init__(
            host=config['ircServer'],
            port=config.get('ircPort', 6667),
            ssl=config.get('ircSsl', False)
        )
        self.nick = config.get('ircNick', 'discirc')
        self.channels = config['mappingChannels']
        
        self.on('CLIENT_CONNECT', self.on_connect)
        self.on('PING', self.on_ping)
        self.on('PRIVMSG', self.on_irc_message)

        self.users = dict()

        # signals
        self.discord_signal = signal(SIGNALNAMES.DISCORD_MSG)
        self.discord_signal.connect(self.on_discord_message)
        self.discord_priv_signal = signal(SIGNALNAMES.DISCORD_PRIV_MSG)
        self.discord_priv_signal.connect(self.on_discord_priv_message)
        self.irc_signal = signal(SIGNALNAMES.IRC_MSG)
        self.irc_priv_signal = signal(SIGNALNAMES.IRC_PRIV_MSG)

    def on_connect(self):
        """On connect event"""
        self.send('NICK', nick=self.nick)
        self.send('USER', user=self.nick, realname='Discord gateway')
        for chan in self.channels.values():
            self.send('JOIN', channel=chan)

    def on_ping(self, message, **kwargs):
        """Keep alive server"""
        self.send('PONG', message=message)

    def on_irc_message(self, nick, target, message, **kwargs):
        """On IRC message event

        :param nick: Message author nick
        :param target: Message target (priv or channel)
        :param message: Message content
        """
        if nick == self.nick:
            return

        data = Message(target, nick, message)

        if target != self.nick:
            self.irc_signal.send(self, data=data)
        else:
            words = message.split(':')
            target = words.pop(0)
            content = ' '.join(words)
            data = Message(target, nick, content)
            self.irc_priv_signal.send(self, data=data)

    def on_discord_message(self, sender, **kwargs):
        """On Discord message event callback

        :param sender: Message sender
        """
        message = kwargs['data']
        chan = self.channels.get(message.channel)
        user = message.source
        content = message.content
        if chan:
            self._relay_discord_message(chan, user, content)

    def on_discord_priv_message(self, sender, **kwargs):
        """On Discord private message event callback

        :param sender: Message sender
        """
        message = kwargs['data']
        target = message.channel
        user = message.source
        content = message.content
        self._relay_discord_message(target, user, content)

    def _relay_discord_message(self, target, source, content):
        """Send discord message
        
        :param target: Message target
        :param source: Message source
        :param content: Message content
        """
        for msg in content.split('\n'):
            # set a color for this author
            if source not in self.users:
                self.users[source] = self.COLOR_PREF + str(random.randint(2, 15))
            format_msg = '<{}{}{}> {}'.format(
                self.users[source],
                source,
                self.CANCEL,
                msg
            )
            self.send('PRIVMSG', target=target, message=format_msg)

