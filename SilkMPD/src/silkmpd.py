# silkmpd: A basic Python MPD client using the python-mpd library
# Copyright (C) 2013 Chris Jacques <chrisjacques.aus@gmail.com>
#
# Some elements borrowed from mpDris2 by Jean-Philippe Braun & Mantas Mikulėnas.
# Some elements also borrowed from NCMPY by Cyker Way.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import mpd
import sys
from socket import error as SocketError
from time import sleep
from mpd import MPDClient

params = {
    'progname': sys.argv[0],
    # Connection
    'host': 'keymaker',
    'port': 6600,
    'password': None,
    # Library
    'music_dir': '',
}

class PollerError(Exception):
    '''Error in poller'''

class MPDPoller(object):
    def __init__(self, host='localhost', port='6600', password=None):
        self._host = host
        self._port = port
        self._password = password
        self._client = MPDClient()
        
    def connect(self):
        try:
            self._client.connect(self._host, self._port)
        except IOError as strerror:
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
        try:
            self._client.close()
        except (mpd.MPDError, IOError):
            pass
        
        try:
            self._client.disconnect()
        except (mpd.MPDError, IOError):
            self._client = mpd.MPDClient()
            
    def poll(self):
        try:
            song = self._client.currentsong()
        except (mpd.MPDError, IOError):
            self.disconnect()
            try:
                self.connect()
            except PollerError as e:
                raise PollerError("Reconnecting failed: %s" % e)
            
            try:
                song = self._client.currentsong()
            except (mpd.MPDError, IOError) as e:
                raise PollerError("Couldn't retrieve current song: %s" % e)
            
        print(song)

def main():
    poller = MPDPoller(params['host'])
    poller.connect()
    
    while True:
        poller.poll()
        sleep(3)
    
    sys.exit(0)

if __name__ == '__main__':
    try:
        main()
    except PollerError as e:
        print(e)
        sys.stderr.write("Fatal poller error:" % e)
    except Exception as e:
        sys.stderr.write("Unexpected exception:" % e)
    except:
        sys.exit(0)
        