# Copyright (c) 2015 LiuLang. All rights reserved.
# Use of this source code is governed by General Public License that
# can be found in the LICENSE file.

import gettext
import os

from . import const

__all__ = ("_", )

kLocaleDir = os.path.join(const.kPrefix, "locale")

gettext.bindtextdomain(const.kAppName, kLocaleDir)
gettext.textdomain(const.kAppName)
_ = gettext.gettext
