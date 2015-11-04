# Copyright (c) 2015 LiuLang. All rights reserved.
# Use of this source code is governed by General Public License that
# can be found in the LICENSE file.

"""Defines AboutDialog class."""

from gi.repository import Gtk

from ..base import const
from ..base.i18n import _

kHomepage = "https://github.com/LiuLang/bcloud"

# See https://github.com/LiuLang/bcloud/pulls
kAuthors = (
    "Alexzhang <alex8224@gmail.com>",
    "Aetf <horizonvei@gmail.com>",
    "CzBiX <czbix@live.com>",
    "HybridGlucose <a07051226@gmail.com>",
    "Iridium Cao <iridiumcao@gmail.com>",
    "Khalid Hsu <khalidhsu@gmail.com>",
    "latyas <latyas@gmail.com>",
    "Libertas <horizonvei@gmail.com>",
    "LiuLang <gsushzhsosgsu@gmail.com>",
    "Zhenbo Li <litimetal@gmail.com>",
    "slawdan <schludern@gmail.com>",
    "Zihao Wang <wzhdev@gmail.com>",
)
kCopyright = "Copyright (c) 2014-2015 LiuLang"
kDescription = _("Baidu Pan client for GNU/Linux desktop users.")

class AboutDialog(Gtk.AboutDialog):
    """AboutDialog displays basic information about this program."""

    def __init__(self, parent):
        super().__init__()
        self.set_modal(True)
        self.set_transient_for(parent)
        self.set_program_name(const.kAppFullName)
        self.set_logo_icon_name(const.kAppName)
        self.set_version(const.kVersion)
        self.set_comments(kDescription)
        self.set_copyright(kCopyright)
        self.set_website(kHomepage)
        self.set_license_type(Gtk.License.GPL_3_0)
        self.set_authors(kAuthors)
