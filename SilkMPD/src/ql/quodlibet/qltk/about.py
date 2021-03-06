# -*- coding: utf-8 -*-
# Copyright 2004-2005 Joe Wreschnig, Michael Urman, Iñigo Serna
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation

import gtk
import mutagen
import pkg_resources

from quodlibet import const
from quodlibet import formats
from quodlibet.util import fver

class AboutDialog(gtk.AboutDialog):
    def __init__(self, parent, player, name):
        super(AboutDialog, self).__init__()
        self.set_transient_for(parent)
        self.set_program_name(name)
        self.set_version(const.VERSION)
        self.set_authors(const.AUTHORS)
        self.set_artists(const.ARTISTS)
        fmts = ", ".join(formats.modules)
        text = []
        #text.append(_("Supported formats: %s") % fmts)
        if player:
            text.append(_("Audio device: %s") % player.name)
        text.append("MPD: %s / python-mpd: %s" %(
            "test0", pkg_resources.get_distribution("python-mpd2").version))
        #text.append("Mutagen: %s" % fver(mutagen.version))
        text.append("GTK+: %s / PyGTK: %s" %(
            fver(gtk.gtk_version), fver(gtk.pygtk_version)))
        if player:
            text.append(player.version_info)
        self.set_comments("\n".join(text))
        # Translators: Replace this with your name/email to have it appear
        # in the "About" dialog.
        self.set_translator_credits(_('translator-credits'))
        self.set_website("http://code.google.com/p/quodlibet")
        self.set_copyright(
            "Copyright © 2004-2012 Joe Wreschnig, Michael Urman, & others\n"
            "MPD Edits Copyright © 2013 Chris Jacques\n"
            "<quod-libet-development@googlegroups.com>")
        self.child.show_all()

class AboutQuodLibet(AboutDialog):
    def __init__(self, parent, player):
        super(AboutQuodLibet, self).__init__(parent, player, "Quod Libet")

class AboutExFalso(AboutDialog):
    def __init__(self, parent, player=None):
        super(AboutExFalso, self).__init__(parent, player, "Ex Falso")
