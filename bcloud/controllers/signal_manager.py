# Copyright (c) 2015 LiuLang. All rights reserved.
# Use of this source code is governed by General Public License that
# can be found in the LICENSE file.

from gi.repository import GObject

from ..base import decorators

@decorators.single_instance
class SignalManager(GObject.GObject):

    __gsignals__ = {
        "started": (GObject.SIGNAL_RUN_LAST, GObject.TYPE_NONE, []),

        "show-main-window": (GObject.SIGNAL_RUN_LAST, GObject.TYPE_NONE, []),
        "toggle-main-window-visibility":
            (GObject.SIGNAL_RUN_LAST, GObject.TYPE_NONE, []),
        "reload-current-page": (GObject.SIGNAL_RUN_LAST, GObject.TYPE_NONE, []),

        # Terminates process.
        "app-quit": (GObject.SIGNAL_RUN_LAST, GObject.TYPE_NONE, []),

        "start-download-tasks":
            (GObject.SIGNAL_RUN_LAST, GObject.TYPE_NONE, []),
        "stop-download-tasks": (GObject.SIGNAL_RUN_LAST, GObject.TYPE_NONE, []),

        "start-upload-tasks": (GObject.SIGNAL_RUN_LAST, GObject.TYPE_NONE, []),
        "stop-upload-tasks": (GObject.SIGNAL_RUN_LAST, GObject.TYPE_NONE, []),
        "upload-files":
            (GObject.SIGNAL_RUN_LAST, GObject.TYPE_NONE,
                [GObject.TYPE_PYOBJECT, str]),
    }
