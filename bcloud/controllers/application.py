# Copyright (c) 2015 LiuLang. All rights reserved.
# Use of this source code is governed by General Public License that
# can be found in the LICENSE file.

"""Defines Application class."""

import signal

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gio
from gi.repository import GLib
from gi.repository import Gtk

from ..base import const
from ..base.i18n import _
from ..views.about_dialog import AboutDialog
from ..views.main_window import MainWindow
from ..views.preferences_dialog import PreferencesDialog
from .signal_manager import SignalManager
from ..services.settings import Settings

class Application(Gtk.Application):
    """Application handles most import aspects of ui interactions."""

    def __init__(self):
        super().__init__()
        self.set_application_id(const.kDbusName)

    def do_startup(self):
        """Override do_startup()."""
        GLib.set_application_name(const.kAppName)
        Gtk.Application.do_startup(self)
        self.main_window = MainWindow(self)

        app_menu = Gio.Menu.new()
        app_menu.append(_("Preferences"), "app.preferences")
        app_menu.append(_("Sign out"), "app.signout")
        app_menu.append(_("About"), "app.about")
        app_menu.append(_("Quit"), "app.quit")
        self.set_app_menu(app_menu)

        preferences_action = Gio.SimpleAction.new("preferences", None)
        preferences_action.connect("activate",
                                   self.on_preferences_action_activated)
        self.add_action(preferences_action)
        signout_action = Gio.SimpleAction.new("signout", None)
        signout_action.connect("activate", self.on_signout_action_activated)
        self.add_action(signout_action)
        about_action = Gio.SimpleAction.new("about", None)
        about_action.connect("activate", self.on_about_action_activated)
        self.add_action(about_action)
        quit_action = Gio.SimpleAction.new("quit", None)
        self.add_action(quit_action)

        signal_manager = SignalManager.instance()
        quit_action.connect("activate",
                            lambda *args: signal_manager.emit("app-quit"))
        signal_manager.connect("app-quit", lambda *args: self.quit())

    def do_activate(self):
        """Override do_activate()."""
        self.main_window.show_all()
        #self.show_signin_dialog(True)

        # Handles unix signals.
        GLib.unix_signal_add(GLib.PRIORITY_HIGH, signal.SIGHUP, self.quit, None)
        GLib.unix_signal_add(GLib.PRIORITY_HIGH, signal.SIGINT, self.quit, None)
        GLib.unix_signal_add(GLib.PRIORITY_HIGH, signal.SIGTERM, self.quit,
                             None)

    def do_shutdown(self):
        """Override do_shutdown()."""
        Gtk.Application.do_shutdown(self)
        print("application do_shutdown()")

    def on_preferences_action_activated(self, action, params):
        """Show preferencies dialog."""
        dialog = PreferencesDialog(self.main_window)
        dialog.run()
        dialog.destroy()

    def on_signout_action_activated(self, action, params):
        """Show sign in dialolg without auto sign in."""
        pass

    def on_about_action_activated(self, action, params):
        """Show about dialog."""
        dialog = AboutDialog(self.main_window)
        dialog.run()
        dialog.destroy()

    def show_signin_dialog(self, auto_signin):
        Settings.instance().reset()
        dialog = SigninDialog(self.main_window, auto_signin)
        dialog.run()
        dialog.destroy()

        if Settings.instance().signed_in:
            self.main_window.init_notebook()
