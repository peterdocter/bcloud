# Copyright (C) 2014-2015 LiuLang <gsushzhsosgsu@gmail.com>
# Use of this source code is governed by GPLv3 license that can be found
# in http://www.gnu.org/licenses/gpl-3.0.html

import os

kHomeDir = os.path.expanduser("~")
kLocalDir = os.path.join(kHomeDir, ".local")
kPrefix = ""
if __file__.startswith("/usr/local/"):
    kPrefix = "/usr/local/share"
elif __file__.startswith("/usr/"):
    kPrefix = "/usr/share"
elif __file__.startswith(kLocalDir):
    kPrefix = os.path.join(kLocalDir, "share")
else:
    kPrefix = os.path.join(os.path.dirname(os.path.dirname(__file__)), "share")

kAppName = "bcloud"
kAppFullName = "Bcloud"
kVersion = "3.8.1"
kDbusName = "org.liulang.bcloud"

kIconPath = os.path.join(kPrefix, kAppName, "icons")
kColorSchema = os.path.join(kPrefix, kAppName, "color-schema.json")
kCacheDir = os.path.join(kHomeDir, ".cache", kAppName)
kConfigDir = os.path.join(kHomeDir, ".config", kAppName)

