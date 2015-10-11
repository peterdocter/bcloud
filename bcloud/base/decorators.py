# Copyright (c) 2015 LiuLang. All rights reserved.
# Use of this source code is governed by General Public License that
# can be found in the LICENSE file.

def single_instance(cls):
    """Make this class singleton."""
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            # TODO(xushaohua): support multiple inheritence.
            super_cls = cls.mro()[1]
            cls._instance = super_cls.__new__(cls, *args, **kwargs)
        return cls._instance
    cls.__new__ = __new__
    return cls
