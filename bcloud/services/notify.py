# Copyright (c) 2015 LiuLang. All rights reserved.
# Use of this source code is governed by General Public License that
# can be found in the LICENSE file.

from gi.repository import Notify

from ..base import const

# Global notitification object.
_notification_obj = None

def init(notify_enabled):
    """Init notify when a new user session is started."""
    if not notify_enabled:
        _notification_obj = None
        return
    success = Notify.init(const.kAppName)
    if not success:
        return
    global _notification_obj
    _notification_obj = Notify.Notification.new(const.kAppFullName, "",
                                                const.kAppName)

def notify(text):
    """Popup a notification on desktop."""
    if _notitifcation_obj:
        _notification_obj.update(const.kAppFullName, text, const.kAppName)
        self.notify.show()
