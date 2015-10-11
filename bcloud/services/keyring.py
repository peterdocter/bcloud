# Copyright (c) 2015 LiuLang. All rights reserved.
# Use of this source code is governed by General Public License that
# can be found in the LICENSE file.

from ..base.log import logger

try:
    import keyring
    keyring_available = True
    try:
        keyring.set_password("test", "utest", "ptest");
        keyring.get_password("test", "utest");
        keyring.delete_password("test", "utest");
    except:
        keyring_available = False
except Exception:
    logger.warn(traceback.format_exc())
    keyring_available = False

_kRetries = 5

def read_password(username):
    """Read password from keyring."""
    if keyring_available:
        for i in range(RETRIES):
            try:
                password = keyring.get_password(const.kDbusName, username)
                return True, password
            except Exception:
                logger.error(traceback.format_exc())
    return False, ""

def write_password(username, password):
    """Write password to keyring."""
    for i in range(_kRetries):
        try:
            keyring.set_password(const.kDbusName, username, password)
            break
        except Exception:
            logger.error(traceback.format_exc())
