# Copyright (c) 2015 LiuLang. All rights reserved.
# Use of this source code is governed by General Public License that
# can be found in the LICENSE file.

from gi.repository import Gdk
from gi.repository import Gtk

from ..base import const
from ..base.i18n import _
from ..controllers.signal_manager import signal_manager
from ..services.settings import settings
from .category_page import *
from .home_page import HomePage
from . import util
from .util import TargetInfo, TargetType

kDropTargets = (
    (TargetType.kUriList, Gtk.TargetFlags.OTHER_APP, TargetInfo.kUriList),
)
kDropTargetList = [Gtk.TargetEntry.new(*t) for t in kDropTargets]

kIconCol, kNameCol, kTooltipCol, kColorCol = 0, 1, 2, 3
kDarkColor  = Gdk.RGBA(0.9, 0.9, 0.9, 1)
kLightColor = Gdk.RGBA(0.1, 0.1, 0.1, 1)

class MainWindow(Gtk.ApplicationWindow):

    def __init__(self, app):
        Gtk.Window.__init__(self, application=app)

        self._init_ui()
        self._init_connect()

    def _init_ui(self):
        self.set_default_size(settings.window_width, settings.window_height)
        self.set_default_icon_name(const.kAppName)
        self.props.window_position = Gtk.WindowPosition.CENTER
        self.props.hide_titlebar_when_maximized = True

        self.default_color = kDarkColor

        paned = Gtk.Paned()
        self.add(paned)
        left_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        left_box.get_style_context().add_class(Gtk.STYLE_CLASS_SIDEBAR)
        paned.add1(left_box)
        paned.child_set_property(left_box, 'shrink', False)
        paned.child_set_property(left_box, 'resize', False)

        nav_window = Gtk.ScrolledWindow()
        nav_window.props.hscrollbar_policy = Gtk.PolicyType.NEVER
        left_box.pack_start(nav_window, True, True, 0)

        # icon_name, disname, tooltip, color
        self.nav_liststore = Gtk.ListStore(str, str, str, Gdk.RGBA)
        self.nav_treeview = Gtk.TreeView(model=self.nav_liststore)
        self.nav_treeview.get_style_context().add_class(Gtk.STYLE_CLASS_SIDEBAR)
        self.nav_treeview.props.headers_visible = False
        self.nav_treeview.set_tooltip_column(kTooltipCol)
        icon_cell = Gtk.CellRendererPixbuf()
        icon_cell.props.xalign = 1
        icon_col = Gtk.TreeViewColumn("Icon", icon_cell, icon_name=kIconCol)
        icon_col.props.fixed_width = 40
        self.nav_treeview.append_column(icon_col)
        name_cell = Gtk.CellRendererText()
        name_col = Gtk.TreeViewColumn("Places", name_cell, text=kNameCol,
                                      foreground_rgba=kColorCol)
        self.nav_treeview.append_column(name_col)
        nav_window.add(self.nav_treeview)

        self.progressbar = Gtk.ProgressBar()
        left_box.pack_end(self.progressbar, False, False, 0)

        self.capacity_label = Gtk.Label(_('Unknown'))
        left_box.pack_end(self.capacity_label, False, False, 0)

        self.img_avatar = Gtk.Image()
        self.img_avatar.props.halign = Gtk.Align.CENTER
        left_box.pack_end(self.img_avatar, False, False, 5)

        self.notebook = Gtk.Notebook()
        self.notebook.props.show_tabs = False
        paned.add2(self.notebook)

        self.init_notebook()

        # Support drop files.
        self.drag_dest_set(Gtk.DestDefaults.ALL, kDropTargetList,
                           Gdk.DragAction.COPY)

        # Add accelerator
        self.accel_group = Gtk.AccelGroup()
        self.add_accel_group(self.accel_group)
        key, mod = Gtk.accelerator_parse("F5")
        self.add_accelerator("activate-default", self.accel_group, key, mod,
                             Gtk.AccelFlags.VISIBLE)

    def _init_connect(self):
        nav_selection = self.nav_treeview.get_selection()
        nav_selection.connect("changed", self.on_nav_selection_changed)
        self.notebook.connect('switch-page', self.on_notebook_switched)

        signal_manager.connect("reload-current-page", self.reload_current_page)
        signal_manager.connect("show-main-window", lambda obj: self.present())
        signal_manager.connect("toggle-main-window-visibility",
                                lambda obj: self.toggle_visibility())

    def init_notebook(self):
        def append_page(page):
            self.notebook.append_page(page, Gtk.Label.new(page.disname))
            self.nav_liststore.append([page.icon_name, page.disname,
                                       page.tooltip, self.default_color])

        self.nav_liststore.clear()
        children = self.notebook.get_children()
        for child in children:
            self.notebook.remove(child)
        self.home_page = HomePage(self)
        append_page(self.home_page)
        self.picture_page = PicturePage(self)
        append_page(self.picture_page)
        self.doc_page = DocPage(self)
        append_page(self.doc_page)
        self.video_page = VideoPage(self)
        append_page(self.video_page)
        self.bt_page = BTPage(self)
        append_page(self.bt_page)
        self.music_page = MusicPage(self)
        append_page(self.music_page)
        self.other_page = OtherPage(self)
        append_page(self.other_page)
#        self.trash_page = TrashPage(self)
#        append_page(self.trash_page)
#        self.share_page = SharePage(self)
#        append_page(self.share_page)
#        self.cloud_page = CloudPage(self)
#        append_page(self.cloud_page)
#        self.download_page = DownloadPage(self)
#        append_page(self.download_page)
#        self.upload_page = UploadPage(self)
#        append_page(self.upload_page)
#
        self.notebook.show_all()

    def do_activate_default(self):
        self.reload_current_page()

    def toggle_visibility(self):
        if self.props.visible:
            self.hide()
        else:
            self.present()

    def do_check_resize(self):
        settings.window_width, settings.window_height = self.get_size()
        return Gtk.Window.do_check_resize(self)

    def do_delete_event(self, event):
        if settings.use_status_icon:
            self.hide()
        else:
            signal_manager.emit("app-quit")
#
    def do_drag_data_received(self, drag_context, x, y, data, info, time):
        """Drag a file/folder to main window, opens a file chooser dialog."""
        if not settings.signed_in:
            return

        if info == TargetInfo.kUriList:
            uris = data.get_uris()
            source_paths = util.uris_to_paths(uris)
            if source_paths:
                signal_manager.emit("upload-files", source_paths, "/")

    def on_nav_selection_changed(self, nav_selection):
        model, tree_iter = nav_selection.get_selected()
        if not tree_iter:
            return
        path = model.get_path(tree_iter)
        index = path.get_indices()[0]
        self.switch_page_by_index(index)

    def on_notebook_switched(self, notebook, page, index):
        page.check_first()
        page.on_page_show()

    def reload_current_page(self, *args):
        """Reload current page.

        Note: All pages shall implement reload() method.
        """
        index = self.notebook.get_current_page()
        self.notebook.get_nth_page(index).reload()

    def switch_page_by_index(self, index):
        self.notebook.set_current_page(index)

    def switch_page(self, page):
        for index, p in enumerate(self.notebook):
            if p == page:
                self.nav_selection.select_iter(self.nav_liststore[index].iter)
                break

    def set_dark_theme(self, prefer_dark_theme):
        settings = Gtk.Settings.get_default()
        settings.props.gtk_application_prefer_dark_theme = prefer_dark_theme 
        if prefer_dark_theme:
            self.default_color = kDarkColor
        else:
            self.default_color = kLightColor
        if settings.signed_in:
            for row in self.nav_liststore:
                row[kColorCol] = self.default_color
