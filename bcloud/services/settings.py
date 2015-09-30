# Copyright (c) 2015 LiuLang. All rights reserved.
# Use of this source code is governed by General Public License that
# can be found in the LICENSE file.

from gi.repository import GObject

from ..base import decorators

@decorators.single_instance
class Settings(GObject.GObject):

    use_streaming = GObject.property(type=bool, default=True)
    use_notify = GObject.property(type=bool, default=True)
    use_dark_theme = GObject.property(type=bool, default=False)
    use_status_icon = GObject.property(type=bool, default=False)
    display_avatar = GObject.property(type=bool, default=True)

    save_dir = GObject.property(type=str, default="") 
    concurrent_download = GObject.property(type=int, minimum=1, maximum=5,
                                           default=3)
    concurrent_per_task = GObject.property(type=int, minimum=1, maximum=5,
                                           default=1)
    download_retries = GObject.property(type=int, minimum=0, maximum=120,
                                        default=30)
    download_timeout = GObject.property(type=int, minimum=10, maximum=240,
                                        default=30)
    # TODO(xushaohua): Use enum.
    download_mode = GObject.property(type=int, minimum=0, maximum=2, default=1)
    download_confirm_delete = GObject.property(type=bool, default=True)

    concurrent_upload = GObject.property(type=int, minimum=1, maximum=5,
                                         default=2)
    upload_hidden = GObject.property(type=bool, default=False)
    upload_mode = GObject.property(type=int, minimum=0, maximum=2, default=1)

    auto_sync = GObject.property(type=bool, default=False)
    sync_local_dir = GObject.property(type=str, default="")
    sync_remote_dir = GObject.property(type=str, default="")
