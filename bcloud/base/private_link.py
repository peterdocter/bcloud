# Copyright (C) 2014-2015 LiuLang <gsushzhsosgsu@gmail.com>
# Use of this source code is governed by GPLv3 license that can be found
# in http://www.gnu.org/licenses/gpl-3.0.html

"""Decode private links."""

import base64
import traceback

from .log import logger

__all__ = ("decode", )

def _decodeFlashget(link):
    try:
        l = base64.decodestring(link[11:len(link)-7].encode()).decode()
    except ValueError:
        logger.warn(traceback.format_exc())
        l = base64.decodestring(link[11:len(link)-7].encode()).decode("gbk")
    return l[10:len(l)-10]

def _decodeThunder(link):
    # AAhttp://127.0.0.1
    if link.startswith("QUFodHRwOi8vMTI3LjAuMC4"):
        return ""
    try:
        l = base64.decodestring(link[10:].encode()).decode("gbk")
    except ValueError:
        logger.warn(traceback.format_exc())
        l = base64.decodestring(link[10:].encode()).decode()
    return l[2:-2]

def _decodeQqdl(link):
    try:
        return base64.decodestring(link[7:].encode()).decode()
    except ValueError:
        logger.warn(traceback.format_exc())
        return base64.decodestring(link[7:].encode()).decode("gbk")

_router = {
    "flashge": _decodeFlashget,
    "thunder": _decodeThunder,
    "qqdl://": _decodeQqdl,
}

def decode(link):
    "Decode private link."""
    if not isinstance(link, str) or len(link) < 10:
        logger.error("[private_link.decode] unknown link: %s" % link)
        return ""
    link_prefix = link[:7].lower()
    if link_prefix in _router:
        try:
            return _router[link_prefix](link)
        except IndexError:
            logger.error(traceback.format_exc())
            return ""
    else:
        logger.warn("[private_link.decode] unknown protocol: %s" % link)
        return ""
