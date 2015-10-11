# Copyright (c) 2015 LiuLang. All rights reserved.
# Use of this source code is governed by General Public License that
# can be found in the LICENSE file.

from gi.repository import GLib
from gi.repository import GObject
from gi.repository import Gtk

from ..base.i18n import _
from ..services.settings import Settings

class PreferencesDialog(Gtk.Dialog):

    def __init__(self, parent_window):
        super().__init__(_("Preferences"), parent_window,
                         Gtk.DialogFlags.MODAL,
                         (Gtk.STOCK_CLOSE, Gtk.ResponseType.OK))
        self.set_default_response(Gtk.ResponseType.OK)
        self.set_default_size(480, 360)
        self.set_border_width(10)

        self._init_ui()

    def _init_ui(self):
        settings = Settings()
        box = self.get_content_area()

        notebook = Gtk.Notebook()
        box.pack_start(notebook, True, True, 0)

        # General Tab
        general_grid = Gtk.Grid()
        general_grid.props.halign = Gtk.Align.CENTER
        general_grid.props.column_spacing = 12
        general_grid.props.row_spacing = 5
        general_grid.props.margin_top = 5
        notebook.append_page(general_grid, Gtk.Label.new(_("General")))

        stream_label = Gtk.Label.new(_("Streaming mode"))
        stream_label.props.xalign = 1
        general_grid.attach(stream_label, 0, 0, 1, 1)
        stream_switch = Gtk.Switch()
        stream_switch.props.active = settings.props.use_streaming
        stream_switch.bind_property("active", settings, "use-streaming",
                                    GObject.BindingFlags.BIDIRECTIONAL)
        stream_switch.props.halign = Gtk.Align.START
        stream_switch.set_tooltip_text(
                _("Open the compressed version of videos, useful for those whose network connection is slow."))
        general_grid.attach(stream_switch, 1, 0, 1, 1)

        notify_label = Gtk.Label.new(_("Use notification:"))
        notify_label.props.xalign = 1
        general_grid.attach(notify_label, 0, 1, 1, 1)
        notify_switch = Gtk.Switch()
        notify_switch.props.halign = Gtk.Align.START
        notify_switch.props.active = settings.props.use_notify
        notify_switch.bind_property("active", settings, "use-notify",
                                    GObject.BindingFlags.BIDIRECTIONAL)
        general_grid.attach(notify_switch, 1, 1, 1, 1)

        dark_theme_label = Gtk.Label.new(_("Use dark theme:"))
        dark_theme_label.props.xalign = 1
        general_grid.attach(dark_theme_label, 0, 2, 1, 1)
        dark_theme_switch = Gtk.Switch()
        dark_theme_switch.props.active = settings.props.use_dark_theme
        dark_theme_switch.bind_property("active", settings, "use-dark-theme",
                                        GObject.BindingFlags.BIDIRECTIONAL)
        dark_theme_switch.props.halign = Gtk.Align.START
        general_grid.attach(dark_theme_switch, 1, 2, 1, 1)

        status_label = Gtk.Label.new(_("Use Status Icon:"))
        status_label.props.xalign = 1
        general_grid.attach(status_label, 0, 3, 1, 1)
        status_switch = Gtk.Switch()
        status_switch.props.active = settings.props.use_status_icon
        status_switch.bind_property("active", settings, "use-status-icon",
                                    GObject.BindingFlags.BIDIRECTIONAL)
        status_switch.props.halign = Gtk.Align.START
        general_grid.attach(status_switch, 1, 3, 1, 1)

        avatar_label = Gtk.Label.new(_("Display Avatar:"))
        avatar_label.props.xalign = 1
        general_grid.attach(avatar_label, 0, 4, 1, 1)
        avatar_switch = Gtk.Switch()
        avatar_switch.props.active = settings.props.display_avatar
        avatar_switch.bind_property("active", settings, "display-avatar",
                                    GObject.BindingFlags.BIDIRECTIONAL)
        avatar_switch.props.halign = Gtk.Align.START
        general_grid.attach(avatar_switch, 1, 4, 1, 1)


        # download tab
        download_grid = Gtk.Grid()
        download_grid.props.halign = Gtk.Align.CENTER
        download_grid.props.column_spacing = 12
        download_grid.props.row_spacing = 5
        download_grid.props.margin_top = 5
        notebook.append_page(download_grid, Gtk.Label.new(_("Download")))

        dir_label = Gtk.Label.new(_("Save To:"))
        dir_label.props.xalign = 1
        download_grid.attach(dir_label, 0, 0, 1, 1)
        dir_button = Gtk.FileChooserButton()
        dir_button.set_action(Gtk.FileChooserAction.SELECT_FOLDER)
        dir_button.set_current_folder(settings.props.save_dir)
        dir_button.connect("file-set", self.on_save_dir_updated)
        download_grid.attach(dir_button, 1, 0, 1, 1)

        concurr_label = Gtk.Label.new(_("Concurrent downloads:"))
        concurr_label.props.xalign = 1
        download_grid.attach(concurr_label, 0, 1, 1, 1)
        concurr_spin = Gtk.SpinButton.new_with_range(
                Settings.props.concurrent_download.minimum,
                Settings.props.concurrent_download.maximum,
                1)
        concurr_spin.props.value = settings.props.concurrent_download
        concurr_spin.bind_property("value", settings, "concurrent-download",
                                   GObject.BindingFlags.BIDIRECTIONAL)
        concurr_spin.props.halign = Gtk.Align.START
        download_grid.attach(concurr_spin, 1, 1, 1, 1)

        segments_label = Gtk.Label.new(_("Per task:"))
        segments_label.props.xalign = 1
        download_grid.attach(segments_label, 0, 2, 1, 1)
        segments_spin = Gtk.SpinButton.new_with_range(
                Settings.props.concurrent_per_task.minimum,
                Settings.props.concurrent_per_task.maximum,
                1)
        segments_spin.props.value = settings.props.concurrent_per_task
        segments_spin.bind_property("value", settings, "concurrent-per-task",
                                    GObject.BindingFlags.BIDIRECTIONAL)
        segments_spin.props.halign = Gtk.Align.START
        download_grid.attach(segments_spin, 1, 2, 1, 1)
        segments_label2 = Gtk.Label.new(_("connections"))
        segments_label2.props.xalign = 0
        download_grid.attach(segments_label2, 2, 2, 1, 1)

        retries_each = Gtk.Label.new(_("Retries each:"))
        retries_each.props.xalign = 1
        download_grid.attach(retries_each, 0, 3, 1, 1)
        retries_spin = Gtk.SpinButton.new_with_range(
                Settings.props.download_retries.minimum,
                Settings.props.download_retries.maximum,
                1)
        retries_spin.props.value = settings.props.download_retries
        retries_spin.bind_property("value", settings, "download-retries",
                                   GObject.BindingFlags.BIDIRECTIONAL)
        retries_spin.props.halign = Gtk.Align.START
        retries_spin.set_tooltip_text(_("0: disable retry"))
        download_grid.attach(retries_spin, 1, 3, 1, 1)
        retries_minute_label = Gtk.Label.new(_("minutes"))
        retries_minute_label.props.xalign = 0
        download_grid.attach(retries_minute_label, 2, 3, 1, 1)

        download_timeout = Gtk.Label.new(_("Download timeout:"))
        download_timeout.props.xalign = 1
        download_grid.attach(download_timeout, 0, 4, 1, 1)
        download_timeout_spin = Gtk.SpinButton.new_with_range(
                Settings.props.download_timeout.minimum,
                Settings.props.download_timeout.maximum,
                10)
        download_timeout_spin.props.value = settings.props.download_timeout
        download_timeout_spin.bind_property("value", settings,
                "download-timeout", GObject.BindingFlags.BIDIRECTIONAL)
        download_timeout_spin.props.halign = Gtk.Align.START
        download_grid.attach(download_timeout_spin, 1, 4, 1, 1)
        download_timeout_second = Gtk.Label.new(_("seconds"))
        download_timeout_second.props.xalign = 0
        download_grid.attach(download_timeout_second, 2, 4, 1, 1)

        download_mode_label = Gtk.Label.new(_("File exists while downloading:"))
        download_mode_label.props.xalign = 1
        download_grid.attach(download_mode_label, 0, 5, 1, 1)
        download_mode_combo = Gtk.ComboBoxText()
        download_mode_combo.append_text(_("Do Nothing"))
        download_mode_combo.append_text(_("Overwrite"))
        download_mode_combo.append_text(_("Rename Automatically"))
        download_mode_combo.props.active = settings.props.download_mode
        download_mode_combo.bind_property("active", settings, "download-mode",
                                          GObject.BindingFlags.BIDIRECTIONAL)
        download_mode_combo.set_tooltip_text(
                _("What to do when downloading a file which already exists on local disk"))
        download_grid.attach(download_mode_combo, 1, 5, 2, 1)

        confirm_delete_label = Gtk.Label(
                _("Ask me when deleting unfinished tasks:"))
        download_grid.attach(confirm_delete_label, 0, 6, 1, 1)
        confirm_delete_switch = Gtk.Switch()
        confirm_delete_switch.props.active = \
                settings.props.download_confirm_delete
        confirm_delete_switch.bind_property("active", settings,
                "download-confirm-delete", GObject.BindingFlags.BIDIRECTIONAL)
        confirm_delete_switch.props.halign = Gtk.Align.START
        download_grid.attach(confirm_delete_switch, 1, 6, 1, 1)


        # upload tab
        upload_grid = Gtk.Grid()
        upload_grid.props.halign = Gtk.Align.CENTER
        upload_grid.props.column_spacing = 12
        upload_grid.props.row_spacing = 5
        upload_grid.props.margin_top = 5
        notebook.append_page(upload_grid, Gtk.Label.new(_("Upload")))

        concurr_upload_label = Gtk.Label.new(_("Concurrent uploads:"))
        concurr_upload_label.props.xalign = 1
        upload_grid.attach(concurr_upload_label, 0, 0, 1, 1)
        concurr_upload_spin = Gtk.SpinButton.new_with_range(
                Settings.props.concurrent_upload.minimum,
                Settings.props.concurrent_upload.maximum,
                1)
        concurr_upload_spin.props.halign = Gtk.Align.START
        concurr_upload_spin.props.value = settings.props.concurrent_upload
        concurr_upload_spin.bind_property("value", settings,
                "concurrent-upload", GObject.BindingFlags.BIDIRECTIONAL)
        upload_grid.attach(concurr_upload_spin, 1, 0, 1, 1)

        upload_hidden_label = Gtk.Label.new(_("Upload hidden files:"))
        upload_hidden_label.props.xalign = 1
        upload_grid.attach(upload_hidden_label, 0, 1, 1, 1)
        upload_hidden_switch = Gtk.Switch()
        upload_hidden_switch.props.halign = Gtk.Align.START
        upload_hidden_switch.set_tooltip_text(
                _("Also upload hidden files and folders"))
        upload_hidden_switch.props.active = settings.props.upload_hidden
        upload_hidden_switch.bind_property("active", settings, "upload-hidden",
                                           GObject.BindingFlags.BIDIRECTIONAL)
        upload_grid.attach(upload_hidden_switch, 1, 1, 1, 1)

        upload_mode_label = Gtk.Label.new(_("File exists while uploading:"))
        upload_mode_label.props.xalign = 1
        upload_grid.attach(upload_mode_label, 0, 2, 1, 1)
        upload_mode_combo = Gtk.ComboBoxText()
        upload_mode_combo.append_text(_("Do Nothing"))
        upload_mode_combo.append_text(_("Overwrite"))
        upload_mode_combo.append_text(_("Rename Automatically"))
        upload_mode_combo.set_tooltip_text(
                _("What to do when uploading a file which already exists on server"))
        upload_mode_combo.props.active = settings.props.upload_mode
        upload_mode_combo.bind_property("active", settings, "upload-mode",
                                        GObject.BindingFlags.BIDIRECTIONAL)
        upload_grid.attach(upload_mode_combo, 1, 2, 2, 1)

        enable_sync_label = Gtk.Label.new(_("Automatically Sync:"))
        enable_sync_label.props.xalign = 1
        upload_grid.attach(enable_sync_label, 0, 3, 1, 1)
        sync_switch = Gtk.Switch()
        sync_switch.props.active = settings.props.auto_sync
        sync_switch.bind_property("active", settings, "auto-sync",
                                  GObject.BindingFlags.BIDIRECTIONAL)
        sync_switch.props.halign = Gtk.Align.START
        upload_grid.attach(sync_switch, 1, 3, 1, 1)

        sync_local_dir_label = Gtk.Label.new(_("Sync Local Directory:"))
        sync_local_dir_label.props.xalign = 1
        sync_local_dir_label.props.sensitive = settings.props.auto_sync
        settings.bind_property("auto-sync", sync_local_dir_label, "sensitive")
        upload_grid.attach(sync_local_dir_label, 0, 4, 1, 1)
        sync_local_dir_button = Gtk.FileChooserButton()
        sync_local_dir_button.set_action(Gtk.FileChooserAction.SELECT_FOLDER)
        sync_local_dir_button.props.sensitive = settings.props.auto_sync
        settings.bind_property("auto-sync", sync_local_dir_button, "sensitive")
        sync_local_dir_button.set_current_folder(settings.props.sync_local_dir)
        sync_local_dir_button.connect("file-set",
                                      self.on_sync_local_dir_updated)
        upload_grid.attach(sync_local_dir_button, 1, 4, 1, 1)

        sync_remote_dir_label = Gtk.Label.new(_("Sync Cloud Directory:"))
        sync_remote_dir_label.props.sensitive = settings.props.auto_sync
        settings.bind_property("auto-sync", sync_remote_dir_label, "sensitive")
        sync_remote_dir_label.props.xalign = 1
        upload_grid.attach(sync_remote_dir_label, 0, 5, 1, 1)
        sync_remote_dir_button = Gtk.Button.new_with_label(
                settings.props.sync_remote_dir)
        sync_remote_dir_button.props.sensitive = settings.props.auto_sync
        settings.bind_property("auto-sync", sync_remote_dir_button, "sensitive")
        sync_remote_dir_button.connect("clicked",
                                       self.on_sync_remote_dir_button_clicked)
        upload_grid.attach(sync_remote_dir_button, 1, 5, 1, 1)

        box.show_all()

    def on_save_dir_updated(self, file_button):
        dir_name = file_button.get_filename()
        if dir_name:
            Settings().props.save_dir = dir_name

    def on_sync_local_dir_updated(self, file_button):
        dir_name = file_button.get_filename()
        if dir_name:
            Settings().props.sync_local_dir = dir_name

    def on_sync_remote_dir_button_clicked(self, button):
        folder_dialog = FolderBrowserDialog()
        response = folder_dialog.run()
        if response != Gtk.ResponseType.OK:
            folder_dialog.destroy()
            return
        dir_name = folder_dialog.get_path()
        folder_dialog.destroy()
        button.set_label(dir_name)
        Settings().props.sync_remote_dir = dir_name
