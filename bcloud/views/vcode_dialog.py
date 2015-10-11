# Copyright (C) 2014-2015 LiuLang <gsushzhsosgsu@gmail.com>
# Use of this source code is governed by GPLv3 license that can be found
# in http://www.gnu.org/licenses/gpl-3.0.html

import os

from gi.repository import Gtk

from ..base.i18n import _
from ..base.log import logger
from ..services import net
from ..services.settings import Settings
from . import util

class VCodeDialog(Gtk.Dialog):

    def __init__(self, parent, info):
        super().__init__(_("Verification.."), parent,
                         Gtk.DialogFlags.MODAL,
                         (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                          Gtk.STOCK_OK, Gtk.ResponseType.OK))

        self.set_default_response(Gtk.ResponseType.OK)
        self.set_default_size(320, 200)
        self.set_border_width(10)

        box = self.get_content_area()
        box.set_spacing(10)

        #util.async_call(net.urlopen, info["img"],
        #                 {"Cookie": app.cookie.header_output()},
        #                 callback=self.update_img)
        self.img = Gtk.Image()
        box.pack_start(self.img, False, False, 0)

        self.entry = Gtk.Entry()
        self.entry.connect("activate",
                lambda *args: self.response(Gtk.ResponseType.OK))
        box.pack_start(self.entry, False, False, 0)

        box.show_all()

    def get_vcode(self):
        return self.entry.get_text()

    def update_img(self, request, error=None):
        #TODO(liulang): simplifies parameter list.
        if error or not request:
            # TODO: add a refresh button
            logger.error("[vcode_dialog.update_img] %s, %s" % (request, error))
            return
        vcode_path = os.path.join(util.get_tmp_path(Profile().username),
                                  "bcloud-download-vcode.jpg")
        with open(vcode_path, "wb") as fh:
            fh.write(request.data)
        self.img.set_from_file(vcode_path)
