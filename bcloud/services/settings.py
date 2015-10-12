# Copyright (c) 2015 LiuLang. All rights reserved.
# Use of this source code is governed by General Public License that
# can be found in the LICENSE file.

"""Settings for each baidu-pan user account.

Settings shall be reset to default value when a new user session is started.

NOTE: |password| is not kept in settings, it is kept in keyring if available and
      is only used when retrieving cookie and tokens from remote server.
"""

from gi.repository import GObject

_kAuthConf = "auth.json"

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

    username = GObject.property(type=str, default="")
    remember_password = GObject.property(type=bool, default=True)
    auto_signin = GObject.property(type=bool, default=True)
    signed_in = GObject.property(type=bool, default=False)

    window_width = GObject.property(type=int, default=800)
    window_height = GObject.property(type=int, default=600)

    # Page mode
    HomePage = GObject.property(type=int, minimum=0, maximum=1, default=0)
    PicturePage = GObject.property(type=int, minimum=0, maximum=1, default=0)
    DocPage = GObject.property(type=int, minimum=0, maximum=1, default=0)
    VideoPage = GObject.property(type=int, minimum=0, maximum=1, default=0)
    BTPage = GObject.property(type=int, minimum=0, maximum=1, default=0)
    MusicPage = GObject.property(type=int, minimum=0, maximum=1, default=0)
    OtherPage = GObject.property(type=int, minimum=0, maximum=1, default=0)

    def reset(self):
        """Reset settings to default value and clear username/password."""
        for prop in self.props:
            self.set_property(prop.name, prop.default_value)

    def read(self):
        """Read settings from disk."""
        path = os.path.join(self.tmp_path(), _kAuthConf)
        if not os.path.exists(path):
            self.reset()
            return
        with open(path) as fh:
            conf = json.load(fh)
        for key in conf:
            self.set_property(key, conf[key])

    def write(self):
        """Write settings to disk."""
        print("[Settings.write]")
        path = os.path.join(self.tmp_path(), _kAuthConf)
        conf = {}
        for prop in self.props:
            conf[prop.name] = self.get_property(prop.name)
        with open(path, "w") as fh:
            json.dump(conf, fh)

    @property
    def username_hash(self):
        """Get hashed username."""
        if not self.username:
            raise ValueError("[Settings] username is empty")
        return string_hash.md5(self.username)

    @property
    def cache_path(self):
        """Get cache folder of this user.

        Cache folder is used to store file thumnails and user avator.
        """
        path = os.path.join(const.kCacheDir, self.username_hash, "cache")
        if not os.path.exists(path):
            os.makedirs(path, exist_ok=True)
        return path

    @property
    def tmp_path(self):
        """Get tmp folder of this user.

        Temp folder is used to store verification-code image and file pieces
        when uploading.
        """
        path = os.path.join(const.kCacheDir, self.username_hash, "tmp")
        if not os.path.exists(path):
            os.makedirs(path, exist_ok=True)
        return path

settings = Settings()
