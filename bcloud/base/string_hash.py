# Copyright (c) 2015 LiuLang. All rights reserved.
# Use of this source code is governed by General Public License that
# can be found in the LICENSE file.

"""Calculate string hashes."""

import base64
import hashlib

md5 = lambda text: hashlib.md5(text.encode()).hexdigest()

sha1 = lambda text: hashlib.sha1(text.encode()).hexdigest()

sha224 = lambda text: hashlib.sha224(text.encode()).hexdigest()

sha256 = lambda text: hashlib.sha256(text.encode()).hexdigest()

sha384 = lambda text: hashlib.sha384(text.encode()).hexdigest()

sha512 = lambda text: hashlib.sha512(text.encode()).hexdigest()

base64_encode = lambda text: base64.b64encode(text.encode()).decode()

def base64_decode(text):
    try:
        return base64.b64decode(text.encode()).decode()
    except Exception as e:
        return ""
