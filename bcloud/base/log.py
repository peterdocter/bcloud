# Copyright (C) 2014-2015 LiuLang <gsushzhsosgsu@gmail.com>
# Use of this source code is governed by GPLv3 license that can be found
# in http://www.gnu.org/licenses/gpl-3.0.html

import logging
import logging.handlers
import os
import sys
import time

from . import const

__all__ = ("logger", "redirect_stdout")

kLogInterval = 30 * 86400      # 30 days
kLogFileMaxSize = 5 * 2 ** 20  # 5Mb
kBackupCount = 5               # Number of backup files used by logging mod.
kLogLevel = logging.INFO
kFileLog = os.path.join(const.kConfigDir, "bcloud.log")
kConsoleLog = os.path.join(const.kConfigDir, "bcloud-console.log")

def _init_logger(log_file, log_level, maxBytes, backupCount):
    looger = logging.getLogger(const.kAppName)
    file_handler = logging.handlers.RotatingFileHandler(
            log_file, maxBytes=maxBytes,
            backupCount=backupCount)
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    file_handler.setFormatter(formatter)
    looger.addHandler(file_handler)
    looger.setLevel(log_level)
    return looger

# Global logging instance.
logger = _init_logger(kFileLog, kLogLevel, kLogFileMaxSize, kBackupCount)

def redirect_stdout():
    """Redirect stdout and stderr to file."""
    if (os.path.exists(kConsoleLog) and
            time.time() - os.stat(kConsoleLog).st_ctime > kLogInterval):
        os.remove(kConsoleLog)
    file_stream = open(kConsoleLog, "a")
    sys.stdout = file_stream
    sys.stderr = file_stream
