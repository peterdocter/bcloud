# Copyright (c) 2015 LiuLang. All rights reserved.
# Use of this source code is governed by General Public License that
# can be found in the LICENSE file.

"""Defines SignalManager class which manages signals between widgets."""

from gi.repository import GObject

class SignalManager(GObject.GObject):
    """Manages signals between widgets."""

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

    _instance = None

    def __init__(self):
        if self._instance:
            raise ValueError("Call SignalManager.instance() instead.")
        super().__init__()

    @classmethod
    def instance(cls):
        """Returns signal instance of SignalManager."""
        if not cls._instance:
            cls._instance = cls()
        return cls._instance
