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
import os
import shlex
import irc.client
from typing import List
# noinspection PyPep8Naming
from xdcc_dl.logging.LoggingTypes import LoggingTypes as LOG
from xdcc_dl.xdcc.layers.xdcc.MessageSender import MessageSender
from io import open


class AlreadyDownloaded(Exception):
    u"""
    Gets thrown if a file already exists with size >= download size
    """
    pass


# noinspection PyUnusedLocal
class XDCCInitiator(MessageSender):
    u"""
    Initiates the XDCC Connection.
    Layer 4 of the XDCC Bot
    """

    def on_ctcp(self, connection, event):
        u"""
        Client-to-Client Connection which initiates the XDCC handshake

        :param connection: the IRC Connection
        :param event:      the IRC Event
        :return:           None
        """
        super(XDCCInitiator, self).on_ctcp(connection, event)

        if event.arguments[0] != u"DCC":
            return

        payload = shlex.split(event.arguments[1])

        if payload[0] == u"SEND":
            self.dcc_send_handler(payload, connection)
        elif payload[0] == u"ACCEPT":
            self.dcc_accept_handler(payload, connection)

    def dcc_send_handler(self, ctcp_arguments, connection):
        u"""
        Handles incoming CTCP DCC SENDs. Initiates a download or RESUME request.

        :param ctcp_arguments: The CTCP Arguments
        :param connection:     The connection to use for DCC connections
        :return:               None
        """
        self.logger.log(u"Handling DCC SEND Handshake", LOG.DCC_SEND_HANDSHAKE)

        filename = ctcp_arguments[1]
        self.peer_address = irc.client.ip_numstr_to_quad(ctcp_arguments[2])
        self.peer_port = int(ctcp_arguments[3])
        self.filesize = int(ctcp_arguments[4])

        self.progress.set_single_progress_total(int(self.filesize))
        self.current_pack.set_filename(filename)

        if os.path.exists(self.current_pack.get_filepath()) and not self.dcc_resume_requested:

            position = os.path.getsize(self.current_pack.get_filepath())

            if position >= self.filesize:

                self.logger.log(u"File already completely downloaded.", LOG.DOWNLOAD_WAS_DONE)
                raise AlreadyDownloaded()

            else:

                self.logger.log(u"Requesting DCC RESUME", LOG.DCC_RESUME_REQUEST)
                self.progress.set_single_progress(position)

                self.dcc_resume_requested = True  # Let bot know that resume was attempted
                resume_parameter = u"\"" + filename + u"\" " + unicode(self.peer_port) + u" " + unicode(position)

                # -> on_ctcp -> dcc_accept_handler (Or dcc_send_handler if resume fails)
                connection.ctcp(u"DCC RESUME", self.current_pack.get_bot(), resume_parameter)

        else:

            if self.dcc_resume_requested:
                self.logger.log(u"DCC Resume Failed. Starting from scratch.", LOG.DCC_RESUME_FAILED)
                os.remove(self.current_pack.get_filepath())
                self.progress.set_single_progress(0)

            self.logger.log(u"Starting Download of " + filename, LOG.DOWNLOAD_START)

            self.file = open(self.current_pack.get_filepath(), u"wb")
            self.dcc_connection = self.dcc_connect(self.peer_address, self.peer_port, u"raw")  # -> on_dccmsg
            self.download_started = True

    def dcc_accept_handler(self, ctcp_arguments, connection):
        u"""
        Handles DCC ACCEPT messages. Resumes a download.

        :param ctcp_arguments: The CTCP arguments
        :param connection:     The connection to use for DCC connections
        :return:               None
        """
        self.logger.log(u"DCC RESUME request successful", LOG.DCC_RESUME_SUCCESS)
        self.logger.log(u"Resuming Download of " + self.current_pack.get_filepath(), LOG.DOWNLOAD_RESUME)

        self.file = open(self.current_pack.get_filepath(), u"ab")
        self.dcc_connection = self.dcc_connect(self.peer_address, self.peer_port, u"raw")  # -> on_dccmsg
        self.download_started = True
