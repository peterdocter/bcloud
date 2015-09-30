# Copyright (c) 2015 LiuLang. All rights reserved.
# Use of this source code is governed by General Public License that
# can be found in the LICENSE file.

from gi.repository import GObject

from ..base import decorators

@decorators.single_instance
class SignalManager(GObject.GObject):

    __gsignals__ = {
        "started": (GObject.SIGNAL_RUN_LAST, GObject.TYPE_NONE, []),
    }
