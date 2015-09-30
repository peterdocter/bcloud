# Copyright (c) 2015 LiuLang. All rights reserved.
# Use of this source code is governed by General Public License that
# can be found in the LICENSE file.

from gi.repository import Gtk

from ..base import const

from ..service.settings import Settings


class MainWindow(Gtk.ApplicationWindow):

    def __init__(self, app):
        Gtk.Window.__init__(self, application=app)

        self._initUI()
        #self._initCallbacks()

    def _initUI(self):
        #self.set_default_size()
        self.set_default_icon_name(const.kAppName)
        self.props.window_position = Gtk.WindowPosition.CENTER
        self.props.hide_titlebar_when_maximized = True

#    def _initCallbacks(self):
#        pass
#
#    def do_check_resize(self):
#        signal_manager.main_window_resized.emit()
#
#    def do_delete_event(self, event):
#        signal_manager.main_window_deleted.emit()
#        return True
