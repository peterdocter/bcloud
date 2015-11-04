# Copyright (C) 2014-2015 LiuLang <gsushzhsosgsu@gmail.com>
# Use of this source code is governed by GPLv3 license that can be found
# in http://www.gnu.org/licenses/gpl-3.0.html

"""
This module contains some useful functions to handle string encoding/decoding,
just like escape(), encodeURLComponent()... in javascript.
"""

import json
from urllib import parse

def url_split_param(text):
    return text.replace("&", "\n&")

def url_param_plus(text):
    url = parse.urlparse(text)
    output = []
    if len(url.scheme) > 0:
        output.append(url.scheme)
        output.append("://")
    output.append(url.netloc)
    output.append(url.path)
    if len(url.query) > 0:
        output.append("?")
        output.append(url.query.replace(" ", "+"))
    return "".join(output)

def escape(text):
    return parse.quote(text)

def unescape(text):
    return parse.unquote(text)

def encode_uri(text):
    return parse.quote(text, safe="~@#$&()*!+=:;,.?/'")

def decode_uri(text):
    return parse.unquote(text)

def encode_uri_component(text):
    return parse.quote(text, safe="~()*!.'")

def decode_uri_component(text):
    return parse.unquote(text)

def json_beautify(text):
    try:
        return json.dumps(json.loads(text), indent=4)
    except ValueError:
        return ""
