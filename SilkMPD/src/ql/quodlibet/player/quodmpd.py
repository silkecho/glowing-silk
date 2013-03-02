# Copyright 2013 Chris Jacques
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation

import mpd
from quodlibet import config

class Singleton(type):
    _instances = {}
    def __call__(self, cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class PollerError(Exception):
    """Fatal error in poller."""

class QuodMpd(object):
    '''This is based on the python-mpd example code.'''
    #__metaclass__ = Singleton
    def __init__(self):
        self._host = None
        self._port = None
        self._password = None
        self._client = mpd.MPDClient()
        
    def is_connected(self):
        '''Test function to see if we are connected'''
        try:
            print(self._client.stats())
            print("Is connected")
        except (mpd.MPDError, IOError):
            '''Crude, but works'''
            print("Is not connected")
            return False
        return True
        

    def connect(self):
        '''Moved from __init__ to ensure we always read the current
            configuration data'''
        self._host = config.get("connection", "hostname")
        self._port = config.get("connection", "port")
        self._password = config.get("connection", "password")
        try:
            self._client.connect(self._host, self._port)

        # Catch socket errors
        except IOError as (errno, strerror):
            raise PollerError("Could not connect to '%s': %s" %
                              (self._host, strerror))
        except mpd.MPDError as e:
            raise PollerError("Could not connect to '%s': %s" %
                              (self._host, e))

        if self._password:
            try:
                self._client.password(self._password)
            # Catch errors with the password command (e.g., wrong password)
            except mpd.CommandError as e:
                raise PollerError("Could not connect to '%s': "
                                  "password commmand failed: %s" %
                                  (self._host, e))

            # Catch all other possible errors
            except (mpd.MPDError, IOError) as e:
                raise PollerError("Could not connect to '%s': "
                                  "error with password command: %s" %
                                  (self._host, e))

    def disconnect(self):
        # Try to tell MPD we're closing the connection first
        try:
            self._client.close()
        # If that fails, don't worry, just ignore it and disconnect
        except (mpd.MPDError, IOError):
            pass

        try:
            self._client.disconnect()
        # Disconnecting failed, so use a new client object instead
        # This should never happen.  If it does, something is seriously broken,
        # and the client object shouldn't be trusted to be re-used.
        except (mpd.MPDError, IOError):
            self._client = mpd.MPDClient()

    def print_current_song(self):
        try:
            song = self._client.currentsong()

        # Couldn't get the current song, so try reconnecting and retrying
        except (mpd.MPDError, IOError):
            # No error handling required here
            # Our disconnect function catches all exceptions, and therefore
            # should never raise any.
            self.disconnect()

            try:
                self.connect()

            # Reconnecting failed
            except PollerError as e:
                raise PollerError("Reconnecting failed: %s" % e)

            try:
                song = self._client.currentsong()

            # Failed again, just give up
            except (mpd.MPDError, IOError) as e:
                raise PollerError("Couldn't retrieve current song: %s" % e)

        # Hurray!  We got the current song without any errors!
        print song
        
    def browse_audio_outputs(self):
        items = []
        #if not self.is_connected():
        #    self.connect()
        #print self._client._fetch_outputs()
        #for Kind in browsers:
        #    if Kind.in_menu:
        #        item = "Browser" + Kind.__name__
        #        items.append("<menuitem action='%s'/>" % item)
        return "\n".join(items)
        