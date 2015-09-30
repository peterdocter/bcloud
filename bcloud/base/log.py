# Copyright (C) 2014-2015 LiuLang <gsushzhsosgsu@gmail.com>
# Use of this source code is governed by GPLv3 license that can be found
# in http://www.gnu.org/licenses/gpl-3.0.html

import logging
import logging.handlers
import os
import sys
import time

from . import const

_kLogInterval = 30 * 86400      # 30 days
_kLogFileMaxSize = 5 * 2 ** 20  # 5Mb
_kBackupCount = 5               # Number of backup files used by logging mod.
_kLogLevel = logging.INFO
_kFileLog = os.path.join(const.kConfigDir, "bcloud.log")
_kConsoleLog = os.path.join(const.kConfigDir, "bcloud-console.log")

def _initLogger(log_file, log_level, maxBytes, backupCount):
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
logger = _initLogger(_kFileLog, _kLogLevel, _kLogFileMaxSize, _kBackupCount)

def redirectStdout():
    """Redirect stdout and stderr to file."""
    if (os.path.exists(_kConsoleLog) and
            time.time() - os.stat(_kConsoleLog).st_ctime > _kLogInterval):
        os.remove(_kConsoleLog)
    fd = open(_kConsoleLog, "a")
    sys.stdout = fd
    sys.stderr = fd
