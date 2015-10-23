# Copyright (c) 2015 LiuLang. All rights reserved.
# Use of this source code is governed by General Public License that
# can be found in the LICENSE file.

"""Manage user profiles."""

import json
import os

from ..base import const
from ..base import decorators
from ..base.log import logger

kConfFile = os.path.join(const.kConfigDir, "conf.json")

@decorators.single_instance
class Profiles(object):

    _profiles = []
    _default = ""

    def read(self):
        """Read profile info from disk."""
        if not os.path.exists(kConfFile):
            os.makedirs(os.path.dirname(kConfFile), exist_ok=True)
            return
        with open(kConfFile) as file_stream:
            conf = json.load(file_stream)
        self._default = conf["default"]
        self._profiles = conf["profiles"]

    def write(self):
        """Write profile info to disk."""
        if not os.path.exists(kConfFile):
            os.makedirs(os.path.dirname(kConfFile), exist_ok=True)
        conf = {
            "default": self._default,
            "profiles": self._profiles,
        }
        with open(kConfFile, "w") as file_stream:
            json.dump(conf, file_stream)

    def add(self, profile_name):
        """Add a new profile item."""
        if profile_name in self._profiles:
            logger.warn("[Profiles.add] %s already exists" % profile_name)
            return
        self._profiles.append(profile_name)
        self.write()

    def remove(self, profile_name):
        """Remove a profile item."""
        if not profile_name in self._profiles:
            logger.error("[Profiles.remove] %s does not exist" % profile_name)
            raise ValueError("%s does not exist" % profile_name)
        self._profiles.remove(profile_name)
        self.write()

    @property
    def default(self):
        """Get default profile item.
        
        Default profile might be empty.
        """
        return self._default

    @default.setter
    def default(self, profile_name):
        """Set default profile item."""
        if profile_name not in self._profiles:
            logger.error("[Profiles.default] %s does not exist" % profile_name)
            raise ValueError("%s does not exist" % profile_name)
        self._default = profile_name

    @property
    def profiles(self):
        """Get profile list.

        Profile list might be empty.
        """
        return self._profiles
