# Copyright (c) 2015 LiuLang. All rights reserved.
# Use of this source code is governed by General Public License that
# can be found in the LICENSE file.

from gi.repository import Gtk

from ..base.i18n import _
from .notify import notify

def copy(text):
    """Copy text to system clipboard."""
    clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
    clipboard.set_text(text, -1)
    notify(_("%s copied to clipboard") % text))
