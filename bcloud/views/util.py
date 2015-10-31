# Copyright (C) 2014-2015 LiuLang <gsushzhsosgsu@gmail.com>
# Use of this source code is governed by GPLv3 license that can be found
# in http://www.gnu.org/licenses/gpl-3.0.html

import json
import os
import subprocess
import threading
import time
import traceback

import dbus
from gi.repository import GdkPixbuf
from gi.repository import Gtk
from gi.repository import GLib

# Check Gtk version <= 3.6
kGtkLe36 = (Gtk.MAJOR_VERSION == 3) and (Gtk.MINOR_VERSION <= 6)
kGtkGe312 = (Gtk.MAJOR_VERSION == 3) and (Gtk.MINOR_VERSION >= 12)

# TODO:
kColorSchemaPath = ""
kAvatarUpdateInterval = 604800  # 用户头像更新频率, 默认是7天

class TargetInfo:
    """拖放类型编号"""

    kUriList = 0
    kPlainText = 1
    kRawData = 2
    kTextJson = 3

class TargetType:
    """拖放类型"""

    kUriList = "text/uri-list"
    kPlainText = "text/plain"
    kRawData = "application/octet-stream"
    kTextJson = "application/json"

class ViewMode:
    kIconView = 0
    kListView = 1

def async_call(func, *args, callback=None):
    """Call `func` in background thread, and then call `callback` in Gtk main thread.

    If error occurs in `func`, error will keep the traceback and passed to
    `callback` as second parameter. Always check `error` is not None.
    """
    def do_call():
        result = None
        error = None

        try:
            result = func(*args)
        except Exception:
            error = traceback.format_exc()
            logger.error(error)
        if callback:
            GLib.idle_add(callback, result, error)

    # TODO(liulang): using thread pool.
    thread = threading.Thread(target=do_call)
    thread.daemon = True
    thread.start()

def xdg_open(uri):
    """使用桌面环境中默认的程序打开指定的URI
    
    当然, 除了URI格式之外, 也可以是路径名, 文件名, 比如:
    xdg_open("/etc/issue")
    推荐使用Gio.app_info_xx() 来启动一般程序, 而用xdg_open() 来打开目录.
    """
    # TODO(liulang): call g_app_info
    try:
        subprocess.call(["xdg-open", uri, ])
    except FileNotFoundError:
        logger.error(traceback.format_exc())

def update_liststore_image(liststore, tree_iters, col, pcs_files, dir_name,
                           icon_size=96):
    """下载文件缩略图, 并将它显示到liststore里.
    
    pcs_files - 里面包含了几个必要的字段.
    dir_name  - 缓存目录, 下载到的图片会保存这个目录里.
    size      - 指定图片的缩放大小, 默认是96px.
    """
    def update_image(filepath, tree_iter):
        try:
            pix = GdkPixbuf.Pixbuf.new_from_file_at_size(filepath, icon_size,
                                                         icon_size)
            tree_path = liststore.get_path(tree_iter)
            if tree_path is None:
                return
            liststore[tree_path][col] = pix
        except GLib.GError:
            logger.error(traceback.format_exc())

    def dump_image(url, filepath):
        req = net.urlopen(url)
        if not req or not req.data:
            logger.warn("update_liststore_image(), failed to request %s" % url)
            return False
        with open(filepath, "wb") as fh:
            fh.write(req.data)
        return True

    for tree_iter, pcs_file in zip(tree_iters, pcs_files):
        if "thumbs" not in pcs_file:
            continue
        if "url1" in pcs_file["thumbs"]:
            key = "url1"
        elif "url2" in pcs_file["thumbs"]:
            key = "url2"
        elif "url3" in pcs_file["thumbs"]:
            key = "url3"
        else:
            continue
        fs_id = pcs_file["fs_id"]
        url = pcs_file["thumbs"][key]
        filepath = os.path.join(dir_name, "{0}.jpg".format(fs_id))
        if os.path.exists(filepath) and os.path.getsize(filepath):
            GLib.idle_add(update_image, filepath, tree_iter)
        elif not url or len(url) < 10:
            logger.warn("update_liststore_image(), failed to get url")
        else:
            status = dump_image(url, filepath)
            if status:
                GLib.idle_add(update_image, filepath, tree_iter)

def update_share_image(liststore, tree_iters, col, large_col, pcs_files,
                       dir_name, icon_size, large_icon_size):
    """下载文件缩略图, 并将它显示到liststore里.

    需要同时更新两列里的图片, 用不同的缩放尺寸.
    pcs_files - 里面包含了几个必要的字段.
    dir_name  - 缓存目录, 下载到的图片会保存这个目录里.
    """
    def update_image(filepath, tree_iter):
        try:
            tree_path = liststore.get_path(tree_iter)
            if tree_path is None:
                return
            pix = GdkPixbuf.Pixbuf.new_from_file(filepath)
            width = pix.get_width()
            height = pix.get_height()
            small_pix = pix.scale_simple(icon_size,
                                         height * icon_size // width,
                                         GdkPixbuf.InterpType.NEAREST)
            liststore[tree_path][col] = small_pix
            liststore[tree_path][large_col] = pix 
        except GLib.GError:
            logger.error(traceback.format_exc())

    def dump_image(url, filepath):
        req = net.urlopen(url)
        if not req or not req.data:
            logger.warn("update_share_image:, failed to request %s" % url)
            return False
        with open(filepath, "wb") as fh:
            fh.write(req.data)
        return True

    for tree_iter, pcs_file in zip(tree_iters, pcs_files):
        if "thumbs" not in pcs_file:
            continue
        elif "url2" in pcs_file["thumbs"]:
            key = "url2"
        elif "url1" in pcs_file["thumbs"]:
            key = "url1"
        elif "url3" in pcs_file["thumbs"]:
            key = "url3"
        else:
            continue
        fs_id = pcs_file["fs_id"]
        url = pcs_file["thumbs"][key]
        filepath = os.path.join(dir_name, "share-{0}.jpg".format(fs_id))
        if os.path.exists(filepath) and os.path.getsize(filepath):
            GLib.idle_add(update_image, filepath, tree_iter)
        elif not url or len(url) < 10:
            logger.warn("update_share_image: failed to get url %s" % url)
        else:
            status = dump_image(url, filepath)
            if status:
                GLib.idle_add(update_image, filepath, tree_iter)

def update_avatar(cookie, tokens, dir_name):
    """获取用户头像信息"""
    uk = pcs.get_user_uk(cookie, tokens)
    if not uk:
        return None
    user_info = pcs.get_user_info(tokens, uk)
    if not user_info:
        return None
    img_path = os.path.join(dir_name, "avatar.jpg")
    if (os.path.exists(img_path) and
            time.time() - os.stat(img_path).st_mtime <= kAvatarUpdateInterval):
        return (uk, user_info["uname"], img_path)
    img_url = user_info["avatar_url"]
    if not img_url:
        return None
    req = net.urlopen(img_url)
    if not req or not req.data:
        logger.warn("gutil.update_avatar(), failed to request %s" % url)
        return None
    with open(img_path, "wb") as fh:
        fh.write(req.data)
    return (uk, user_info["uname"], img_path)

def ellipse_text(text, length=10):
    if len(text) < length:
        return text
    else:
        return text[:8] + ".."

def reach_scrolled_bottom(adj):
    """Check ScrolledWindow reached bottom or not. """
    return (adj.get_upper() - adj.get_page_size() - adj.get_value()) < 80

def tree_model_natsort(model, row1, row2, user_data=None):
    """Sort tree view column with nature-sorting."""
    sort_column, sort_type = model.get_sort_column_id()
    value1 = model.get_value(row1, sort_column)
    value2 = model.get_value(row2, sort_column)
    sort_list1 = util.natsort(value1)
    sort_list2 = util.natsort(value2)
    status = sort_list1 < sort_list2
    if sort_list1 < sort_list2:
        return -1
    else:
        return 1

def escape_tooltip(tooltip):
    """Escape special characters in tooltip text"""
    return GLib.markup_escape_text(tooltip)

def text_buffer_get_all_text(buf):
    """Get all text in a GtkTextBuffer"""
    return buf.get_text(buf.get_start_iter(), buf.get_end_iter(), False)

def load_color_schema():
    if not os.path.exists(kColorSchemaPath):
        return []
    with open(_kColorSchemaPath) as fh:
        color_list = json.load(fh)

    schema = []
    for color in color_list:
        rgba = Gdk.RGBA()
        rgba.red = int(color[:2], base=16) / 255
        rgba.green = int(color[2:4], base=16) / 255
        rgba.blue = int(color[4:6], base=16) / 255
        rgba.alpha = int(color[6:], base=16) / 255
        schema.append(rgba)
    return schema

def uri_to_path(uri):
    if not uri or len(uri) < 7:
        return ""
    return urllib.parse.unquote(uri[7:])

def uris_to_paths(uris):
    """Convert uri to file path."""
    source_paths = []
    for uri in uris:
        source_path = uri_to_path(uri)
        if source_path:
            source_paths.append(source_path)
    return source_paths
