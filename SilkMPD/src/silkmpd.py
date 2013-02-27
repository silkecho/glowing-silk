# silkmpd: A basic Python MPD client using the python-mpd library
# Copyright (C) 2013 Chris Jacques <chrisjacques.aus@gmail.com>
#
# Some elements borrowed from mpDris2 by Jean-Philippe Braun & Mantas Mikulėnas.
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

params = {
    'progname': sys.argv[0],
    # Connection
    'host': 'localhost',
    'port': 6600,
    'password': None,
    # Library
    'music_dir': '',
    # Bling
    'mmkeys': True,
    'notify': True,
}

def usage(params):
    print("""\
Usage: %(progname)s [OPTION]... [MPD_HOST] [MPD_PORT]

Note: Environment variables MPD_HOST and MPD_PORT can be used instead of above
      arguments.

     -p, --path=PATH Sets the library path of MPD to PATH
     -d, --debug Run in debug mode

Default: MPD_HOST: %(host)s, MPD_PORT: %(port)s

Report bugs to https://github.com/silkecho/glowing-silk/issues""" % params)

if __name__ == '__main__':
    #params = {}
    #params['host'] = 'localhost'
    #params['port'] = '6600'
    #params['password'] = 'gnuweed'
    usage(params)