# Copyright (c) 2015 LiuLang. All rights reserved.
# Use of this source code is governed by General Public License that
# can be found in the LICENSE file.

#
#class State:
#    """下载状态常量"""
#    DOWNLOADING = 0
#    WAITING = 1
#    PAUSED = 2
#    FINISHED = 3
#    CANCELED = 4
#    ERROR = 5
#
#class UploadState:
#    UPLOADING = 0
#    WAITING = 1
#    PAUSED = 2
#    FINISHED = 3
#    CANCELED = 4
#    ERROR = 5
#
#class UploadMode:
#    """上传时, 如果服务器端已存在同名文件时的操作方式"""
#    IGNORE = 0
#    OVERWRITE = 1
#    NEWCOPY = 2
#
#DownloadMode = UploadMode

# TODO:
kUploadOnDup = ("", "overwrite", "newcopy")

## 视图模式
#ICON_VIEW, TREE_VIEW = 0, 1
#
#class ValidatePathState:
#    """文件路径检验结果"""
#    OK = 0
#    LENGTH_ERROR = 1
#    CHAR_ERROR2 = 2
#    CHAR_ERROR3 = 3
#
#ValidatePathStateText = (
#    "",
#    _("Max characters in filepath shall no more than 1000"),
#    _("Filepath should not contain \\ ? | \" > < : *"),
#    _("\\r \\n \\t \\0 \\x0B or SPACE should not appear in start or end of filename"),
#)
#
#
