# Copyright (c) 2015 LiuLang. All rights reserved.
# Use of this source code is governed by General Public License that
# can be found in the LICENSE file.

def single_instance(cls):
    """Make this class singleton."""
    cls._instance = None

    def get_instance():
        if not cls._instance:
            cls._instance = cls()
        return cls._instance
    cls.get_instance = get_instance
    return cls
