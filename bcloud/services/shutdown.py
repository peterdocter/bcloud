# Copyright (C) 2014-2015 LiuLang <gsushzhsosgsu@gmail.com>
# Use of this source code is governed by GPLv3 license that can be found
# in http://www.gnu.org/licenses/gpl-3.0.html

import os

import dbus

kSessionBus, kSystemBus = 0, 1

class Shutdown(object):
    """Shutdown the system after the current snapshot has finished.

    This should work for KDE, Gnome, Unity, Cinnamon, XFCE, Mate and E17.

    Note: this class is copied from `backintime` project.
    """

    dbus_shutdown = {
        # Put unity dbus interface ahead of gnome
        "unity": {
            "bus": kSessionBus,
            "service": "com.canonical.Unity",
            "objectPath": "/com/canonical/Unity/Session",
            "method": "Shutdown",
            "interface": "com.canonical.Unity.Session",
            "arguments": (),
        },
        "gnome": {
            "bus": kSessionBus,
            "service": "org.gnome.SessionManager",
            "objectPath": "/org/gnome/SessionManager",
            "method": "Shutdown",
            #methods    Shutdown
            #           Reboot
            #           Logout
            "interface": "org.gnome.SessionManager",
            "arguments": (),
            #arg (only with Logout)
            #           0 normal
            #           1 no confirm
            #           2 force
        },
        "kde": {
            "bus": kSessionBus,
            "service": "org.kde.ksmserver",
            "objectPath": "/KSMServer",
            "method": "logout",
            "interface": "org.kde.KSMServerInterface",
            "arguments": (-1, 2, -1),
                #1st arg   -1 confirm
                #           0 no confirm
                #2nd arg   -1 full dialog with default logout
                #           0 logout
                #           1 restart
                #           2 shutdown
                #3rd arg   -1 wait 30sec
                #           2 immediately
         },
         "xfce": {
             "bus": kSessionBus,
             "service": "org.xfce.SessionManager",
             "objectPath": "/org/xfce/SessionManager",
             "method": "Shutdown",
             #methods    Shutdown
             #           Restart
             #           Suspend (no args)
             #           Hibernate (no args)
             #           Logout (two args)
             "interface":  "org.xfce.Session.Manager",
             "arguments":  (True, ),
             #arg        True    allow saving
             #           False   don"t allow saving
             #1nd arg (only with Logout)
             #           True    show dialog
             #           False   don"t show dialog
             #2nd arg (only with Logout)
             #           True    allow saving
             #           False   don"t allow saving
        },
        "mate": {
            "bus": kSessionBus,
            "service": "org.mate.SessionManager",
            "objectPath": "/org/mate/SessionManager",
            "method": "Shutdown",
            #methods Shutdown
            #        Logout
            "interface": "org.mate.SessionManager",
            "arguments": ()
            #arg (only with Logout)
            #           0 normal
            #           1 no confirm
            #           2 force
        },
        "e17": {
            "bus": kSessionBus,
            "service": "org.enlightenment.Remote.service",
            "objectPath": "/org/enlightenment/Remote/RemoteObject",
            "method": "Halt",
            #methods    Halt -> Shutdown
            #           Reboot
            #           Logout
            #           Suspend
            #           Hibernate
            "interface": "org.enlightenment.Remote.Core",
            "arguments": (),
        },
        "z_freed": {
            "bus": kSystemBus,
            "service": "org.freedesktop.ConsoleKit",
            "objectPath": "/org/freedesktop/ConsoleKit/Manager",
            "method": "Stop",
            "interface": "org.freedesktop.ConsoleKit.Manager",
            "arguments": (),
        },
    }

    _instance = None

    def __init__(self):
        if self._instance:
            raise TypeError("Call Shutdown.instance instead.")

        self._proxy, self._args = self._prepair()

        # Indicate if a valid dbus service is available to shutdown system.
        self.can_shutdown = (self._proxy is not None)

    def _prepair(self):
        """Try to connect to the given dbus services. If successful it will
        return a callable dbus proxy and those arguments.
        """
        try:
            sessionbus = dbus.SessionBus()
            systembus  = dbus.SystemBus()
        except:
            return (None, None)
        for dbus_props in self.dbus_shutdown.values():
            try:
                if dbus_props["bus"] == kSessionBus:
                    bus = sessionbus
                else:
                    bus = systembus
                interface = bus.get_object(dbus_props["service"],
                                           dbus_props["objectPath"])
                proxy = interface.get_dbus_method(dbus_props["method"],
                                                  dbus_props["interface"])
                return (proxy, dbus_props["arguments"])
            except dbus.exceptions.DBusException:
                continue
        return (None, None)

    def shutdown(self):
        """Call the dbus proxy to start the shutdown."""
        if self._proxy:
            os.sync()
            self._proxy(*self._args)
