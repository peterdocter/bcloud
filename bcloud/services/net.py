# Copyright (C) 2014-2015 LiuLang <gsushzhsosgsu@gmail.com>
# Use of this source code is governed by GPLv3 license that can be found
# in http://www.gnu.org/licenses/gpl-3.0.html

import gzip
import http
import http.client
import mimetypes
import os
import traceback
import urllib.parse
import urllib.request
import zlib

from ..base import const
from ..base.log import logger

kRetries = 3
kTimeout = 50

kPassportBase = "https://passport.baidu.com/"
kPassportUrl = kPassportBase + "v2/api/"
kPassportLogin = kPassportBase + "v2/api/?login"
kReferer = kPassportBase + "v2/?login"
kUserAgent = "Mozilla/5.0 (X11; Linux x86_64; rv:31.0) Gecko/20100101 Firefox/31.0 Iceweasel/31.2.0"
kPanUrl = "http://pan.baidu.com/"
kPanApiUrl = kPanUrl + "api/"
kPanReferer = "http://pan.baidu.com/disk/home"
kShareReferer = kPanUrl + "share/manage"

# 一般的服务器名
kPcsUrl = "http://pcs.baidu.com/rest/2.0/pcs/"
# 上传的服务器名
kPcsUrlC = "http://c.pcs.baidu.com/rest/2.0/pcs/"
kPcsUrlsC = "https://c.pcs.baidu.com/rest/2.0/pcs/"
# 下载的服务器名
kPcsUrlD = "http://d.pcs.baidu.com/rest/2.0/pcs/"

## HTTP 请求时的一些常量
kContentForm = "application/x-www-form-urlencoded"
kContentFormUtf8 = kContentForm + "; charset=UTF-8"
kAcceptHtml = "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
kAcceptJson = "application/json, text/javascript, */*; q=0.8"

_kDefaultHeaders = {
    "User-agent": kUserAgent,
    "Referer": kPanReferer,
    #"x-requested-with": "XMLHttpRequest",
    "Accept": kAcceptJson,
    "Accept-language": "zh-cn, zh;q=0.5",
    "Accept-encoding": "gzip, deflate",
    "Pragma": "no-cache",
    "Cache-control": "no-cache",
}

def urloption(url, headers={}, retries=kRetries):
    """发送OPTION 请求"""
    headers_merged = _kDefaultHeaders.copy()
    for key in headers.keys():
        headers_merged[key] = headers[key]
    schema = urllib.parse.urlparse(url)
    for i in range(retries):
        try:
            conn = http.client.HTTPConnection(schema.netloc)
            conn.request("OPTIONS", url, headers=headers_merged)
            resp = conn.getresponse()
            return resp
        except Exception:
            logger.error(traceback.format_exc())
    return None


class ForbiddenHandler(urllib.request.HTTPErrorProcessor):

    def http_error_403(self, req, fp, code, msg, headers):
        return fp

    http_error_400 = http_error_403
    http_error_500 = http_error_403


def urlopen_simple(url, retries=kRetries, timeout=kTimeout):
    for i in range(retries):
        try:
            return urllib.request.urlopen(url, timeout=timeout)
        except Exception:
            logger.error(traceback.format_exc())
    return None

def urlopen(url, headers={}, data=None, retries=kRetries, timeout=kTimeout):
    """打开一个http连接, 并返回Request.

    headers 是一个dict. 默认提供了一些项目, 比如User-Agent, Referer等, 就
    不需要重复加入了.

    这个函数只能用于http请求, 不可以用于下载大文件.
    如果服务器支持gzip压缩的话, 就会使用gzip对数据进行压缩, 然后在本地自动
    解压.
    req.data 里面放着的是最终的http数据内容, 通常都是UTF-8编码的文本.
    """
    headers_merged = _kDefaultHeaders.copy()
    for key in headers.keys():
        headers_merged[key] = headers[key]
    opener = urllib.request.build_opener(ForbiddenHandler)
    opener.addheaders = [(k, v) for k,v in headers_merged.items()]

    for i in range(retries):
        try:
            req = opener.open(url, data=data, timeout=timeout)
            encoding = req.headers.get("Content-encoding")
            req.data = req.read()
            if encoding == "gzip":
                req.data = gzip.decompress(req.data)
            elif encoding == "deflate":
                req.data = zlib.decompress(req.data, -zlib.MAX_WBITS)
            return req
        except Exception:
            logger.error(traceback.format_exc())
    return None

def urlopen_without_redirect(url, headers={}, data=None, retries=kRetries):
    """请求一个URL, 并返回一个Response对象. 不处理重定向.

    使用这个函数可以返回URL重定向(Error 301/302)后的地址, 也可以重到URL中请
    求的文件的大小, 或者Header中的其它认证信息.
    """
    headers_merged = _kDefaultHeaders.copy()
    for key in headers.keys():
        headers_merged[key] = headers[key]

    parse_result = urllib.parse.urlparse(url)
    for i in range(retries):
        try:
            conn = http.client.HTTPConnection(parse_result.netloc)
            if data:
                conn.request("POST", url, body=data, headers=headers_merged)
            else:
                conn.request("GET", url, body=data, headers=headers_merged)
            return conn.getresponse()
        except Exception:
            logger.error(traceback.format_exc())
    return None

def post_multipart(url, headers, fields, files, retries=kRetries):
    content_type, body = encode_multipart_formdata(fields, files)
    schema = urllib.parse.urlparse(url)

    headers_merged = _kDefaultHeaders.copy()
    for key in headers.keys():
        headers_merged[key] = headers[key]
    headers_merged["Content-Type"] = content_type
    headers_merged["Content-length"] = str(len(body))

    for i in range(retries):
        try:
            h = http.client.HTTPConnection(schema.netloc)
            h.request("POST", url, body=body, headers=headers_merged)
            req = h.getresponse()
            encoding = req.getheader("Content-encoding")
            req.data = req.read()
            if encoding == "gzip":
                req.data = gzip.decompress(req.data)
            elif encoding == "deflate":
                req.data = zlib.decompress(req.data, -zlib.MAX_WBITS)
            return req
        except Exception:
            logger.error(traceback.format_exc())
    return None

def encode_multipart_formdata(fields, files):
    kBoundary = b"----------ThIs_Is_tHe_bouNdaRY_$"
    kPrefBoundary = b"--" + kBoundary
    kSuffixBoundary = kPrefBoundary + b"--"
    kCsrf = b"\r\n"
    kBlank = b""
    l = []
    for (key, value) in fields:
        l.append(kSBoundary)
        l.append(('Content-Disposition: form-data; name="%s"' % key).encode())
        l.append(kBlank)
        l.append(value.encode())
    for (key, filename, content) in files:
        l.append(kSuffixBoundary)
        l.append(('Content-Disposition: form-data; name="%s"; filename="%s"' %
                 (key, filename)).encode())
        l.append(kBlank)
        l.append(content)
    l.append(kSuffixBoundary)
    l.append(kBlank)
    body = kCsrf.join(l)
    content_type = "multipart/form-data; boundary=%s" % kBoundary.decode()
    return content_type, body

def get_content_type(filename):
    return mimetypes.guess_type(filename)[0] or "application/octet-stream"
