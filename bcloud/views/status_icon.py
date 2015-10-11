# Copyright (c) 2015 LiuLang. All rights reserved.
# Use of this source code is governed by General Public License that
# can be found in the LICENSE file.

from gi.repository import Gtk
try:
    # Ubuntu Unity uses appindicator instead of status icon
    from gi.repository import AppIndicator3 as AppIndicator
except Exception:
    pass

from ..base import const
from ..base.i18n import _
from ..controllers.signal_manager import SignalManager

class BaseStatusIcon():

    def _build_menu(self):
        menu = Gtk.Menu()
        show_item = Gtk.MenuItem.new_with_label(_("Show App"))
        show_item.connect("activate",
                lambda obj: SignalManager().emit("show-main-window"))
        menu.append(show_item)

        sep_item = Gtk.SeparatorMenuItem()
        menu.append(sep_item)

        stop_download_item = Gtk.MenuItem.new_with_label(
                _("Stop Download Tasks"))
        stop_download_item.connect("activate",
                lambda obj: SignalManager().emit("stop-download-stasks"))
        menu.append(stop_download_item)

        stop_upload_item = Gtk.MenuItem.new_with_label(
                _("Stop Upload Tasks"))
        stop_upload_item.connect("activate",
                lambda obj: SignalManager().emit("stop-upload-tasks"))
        menu.append(stop_upload_item)

        sep_item = Gtk.SeparatorMenuItem()
        menu.append(sep_item)

        quit_item = Gtk.MenuItem.new_with_label(_("Quit"))
        quit_item.connect("activate",
                          lambda obj: SignalManager().emit("app-quit"))
        menu.append(quit_item)

        self.menu = menu

if "AppIndicator" in globals():
    class StatusIcon(AppIndicator.Indicator, BaseStatusIcon):
        def __init__(self):
            AppIndicator.Indicator.__init__(self)
            self.props.id = const.kAppName
            self.props.icon_name = const.kAppName

            self._build_menu()
            self.set_menu(self.menu)
            self.menu.show_all()
            self.set_category(AppIndicator.IndicatorCategory.APPLICATION_STATUS)

else:
    class StatusIcon(Gtk.StatusIcon, BaseStatusIcon):

        def __init__(self):
            Gtk.StatusIcon.__init__(self)
            self.set_from_icon_name(const.kAppName)

            self._build_menu()
            self.menu.show_all()
            self.set_status(AppIndicator.IndicatorStatus.ACTIVE)

        def do_activate(self):
            SignalManager().emit("toggle-main-window")

        def do_popup_menu(self, event_button, event_time):
            self.menu.popup(None, None,
                    lambda obj: Gtk.StatusIcon.position_menu(self.menu, self),
                    None, event_button, event_time)
