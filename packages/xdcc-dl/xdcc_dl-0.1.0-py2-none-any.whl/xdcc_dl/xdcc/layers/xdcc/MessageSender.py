u"""
LICENSE:
Copyright 2016 Hermann Krumrey

This file is part of xdcc_dl.

    xdcc_dl is a program that allows downloading files via hte XDCC
    protocol via file serving bots on IRC networks.

    xdcc_dl is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    xdcc_dl is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with xdcc_dl.  If not, see <http://www.gnu.org/licenses/>.
LICENSE
"""

# imports
from __future__ import absolute_import
import irc.client
from xdcc_dl.xdcc.layers.irc.BotFinder import BotFinder
# noinspection PyPep8Naming
from xdcc_dl.logging.LoggingTypes import LoggingTypes as LOG


# noinspection PyUnusedLocal
class MessageSender(BotFinder):
    u"""
    Class that handles initiating the XDCC Connection by sending the appropriate message to the bot
    Layer 3 of the XDCC Bot
    """

    def on_join(self, connection, event):
        u"""
        Method called when a channel was joined. The first channel that was joined triggers sending a message
        to the bot to initiate the XDCC handshake

        :param connection: the IRC Connection
        :param event:      the IRC Event
        :return:           None
        """
        if event.source.startswith(self.user.get_name()):
            self.logger.log(u"Joined Channel " + event.target, LOG.CHANNEL_JOIN_SUCCESS)

            if not self.channel_joined:  # Only send the XDCC message when the first channel was joined
                self.channel_joined = True  # Let other on_joins know that message was already sent

                log_message = u"Sending XDCC Request to " + self.current_pack.get_bot()
                log_message += u" for pack " + unicode(self.current_pack.get_packnumber())
                self.logger.log(log_message, LOG.MESSAGE_SEND)

                connection.privmsg(self.current_pack.get_bot(), self.current_pack.get_request_message())
                # -> on_ctcp

    def on_namreply(self, connection, event):
        u"""
        Event when a channel sends the existing users on the channel after joining

        :param connection: the IRC Connection
        :param event:      the IRC Event
        :return:           None
        """
        users = event.arguments[2].split(u" ")
        message = u"Channel Users:\n"
        for user in users:
            message += user + u";"
        self.logger.log(message, LOG.CHANNEL_USERS)

    def on_endofnames(self, connection, event):
        u"""
        Marks the End of a series of namreplys

        :param connection: the IRC Connection
        :param event:      the IRC Event
        :return:           None
        """
        self.logger.log(u"End Of joined users list", LOG.CHANNEL_USERS)

    def on_currenttopic(self, connection, event):
        u"""
        Receives the current topic of the newly joined channel

        :param connection: the IRC Connection
        :param event:      the IRC Event
        :return:           None
        """
        self.logger.log(u"Topic " + event.arguments[0] + u": " + event.arguments[1], LOG.CHANNEL_TOPIC)

    def on_topicinfo(self, connection, event):
        u"""
        Receives the current topic information of the newly joined Channel

        :param connection: the IRC Connection
        :param event:      the IRC Event
        :return:           None
        """
        self.logger.log(u"Topic Info: " + event.arguments[1], LOG.CHANNEL_TOPIC)

    def on_quit(self, connection, event):
        u"""
        Logs that a user left a channel

        :param connection: the IRC Connection
        :param event:      the IRC Event
        :return:           None
        """
        self.logger.log(event.arguments[0] + u" quit.", LOG.CHANNEL_QUIT)

    def on_part(self, connection, event):
        u"""
        Logs that a user left a channel using part

        :param connection: the IRC Connection
        :param event:      the IRC Event
        :return:           None
        """
        self.logger.log(event.source + u" left.", LOG.CHANNEL_PART)

    def on_kick(self, connection, event):
        u"""
        Logs that a user was kicked from the channel

        :param connection: the IRC Connection
        :param event:      the IRC Event
        :return:           None
        """
        self.logger.log(event.arguments[0] + u" was kicked.", LOG.CHANNEL_KICK)

    def on_mode(self, connection, event):
        u"""
        Called whenever the mode of a user changes

        :param connection: the IRC Connection
        :param event:      the IRC Event
        :return:           None
        """
        self.logger.log(event.arguments[0] + u" mode changed", LOG.CHANNEL_MODE_CHANGE)

    def on_action(self, connection, event):
        u"""
        Called whenever an action on the channel occurs

        :param connection: the IRC Connection
        :param event:      the IRC Event
        :return:           None
        """
        self.logger.log(event.arguments[0] + u" mode changed", LOG.CHANNEL_ACTION)

    def on_nick(self, connection, event):
        u"""
        Called whenever a user changes his nick

        :param connection: the IRC Connection
        :param event:      the IRC Event
        :return:           None
        """
        self.logger.log(event.source + u" nick changed", LOG.CHANNEL_NICK_CHANGED)
