# The public API for feedparser
# Copyright 2010-2025 Kurt McKee <contactme@kurtmckee.org>
# Copyright 2002-2008 Mark Pilgrim
# All rights reserved.
#
# This file is a part of feedparser.
#
# Redistribution and use in source and binary forms, with or without modification,
# are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice,
#   this list of conditions and the following disclaimer.
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS 'AS IS'
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

import io
import urllib.error
import urllib.parse
import xml.sax
from typing import IO

from . import http
from .encodings import MissingEncoding, convert_file_to_utf8
from .html import BaseHTMLProcessor
from .mixin import XMLParserMixin
from .parsers.json import JSONParser
from .parsers.loose import LooseXMLParser
from .parsers.strict import StrictXMLParser
from .sanitizer import replace_doctype
from .urls import make_safe_absolute_uri
from .util import FeedParserDict

# List of preferred XML parsers, by SAX driver name.  These will be tried first,
# but if they're not installed, Python will keep searching through its own list
# of pre-installed parsers until it finds one that supports everything we need.
PREFERRED_XML_PARSERS = ["drv_libxml2"]

_XML_AVAILABLE = True

SUPPORTED_VERSIONS = {
    "": "unknown",
    "rss090": "RSS 0.90",
    "rss091n": "RSS 0.91 (Netscape)",
    "rss091u": "RSS 0.91 (Userland)",
    "rss092": "RSS 0.92",
    "rss093": "RSS 0.93",
    "rss094": "RSS 0.94",
    "rss20": "RSS 2.0",
    "rss10": "RSS 1.0",
    "rss": "RSS (unknown version)",
    "atom01": "Atom 0.1",
    "atom02": "Atom 0.2",
    "atom03": "Atom 0.3",
    "atom10": "Atom 1.0",
    "atom": "Atom (unknown version)",
    "cdf": "CDF",
    "json1": "JSON feed 1",
}


def _open_resource(
    url_file_stream_or_string,
    result,
):
    """URL, filename, or string --> stream

    This function lets you define parsers that take any input source
    (URL, pathname to local or network file, or actual data as a string)
    and deal with it in a uniform manner.  Returned object is guaranteed
    to have all the basic stdio read methods (read, readline, readlines).
    Just .close() the object when you're done with it.

    :return: A seekable, readable file object.
    """
    pass


def _to_in_memory_file(data):
    pass


class LooseFeedParser(LooseXMLParser, XMLParserMixin, BaseHTMLProcessor):
    pass


class StrictFeedParser(StrictXMLParser, XMLParserMixin, xml.sax.handler.ContentHandler):
    pass


def parse(
    url_file_stream_or_string,
    response_headers: dict[str, str] | None = None,
    resolve_relative_uris: bool | None = None,
    sanitize_html: bool | None = None,
    optimistic_encoding_detection: bool | None = None,
) -> FeedParserDict:
    """Parse a feed from a URL, file, stream, or string.

    :param url_file_stream_or_string:
        File-like object, URL, file path, or string. Both byte and text strings
        are accepted. If necessary, encoding will be derived from the response
        headers or automatically detected.

        Note that strings may trigger network I/O or filesystem access
        depending on the value. Wrap an untrusted string in
        a :class:`io.StringIO` or :class:`io.BytesIO` to avoid this. Do not
        pass untrusted strings to this function.

        When a URL is not passed the feed location to use in relative URL
        resolution should be passed in the ``Content-Location`` response header
        (see ``response_headers`` below).
    :param response_headers:
        A mapping of HTTP header name to HTTP header value. Multiple values may
        be joined with a comma. If a HTTP request was made, these headers
        override any matching headers in the response. Otherwise this specifies
        the entirety of the response headers.
    :param resolve_relative_uris:
        Should feedparser attempt to resolve relative URIs absolute ones within
        HTML content?  Defaults to the value of
        :data:`feedparser.RESOLVE_RELATIVE_URIS`, which is ``True``.
    :param sanitize_html:
        Should feedparser skip HTML sanitization? Only disable this if you know
        what you are doing!  Defaults to the value of
        :data:`feedparser.SANITIZE_HTML`, which is ``True``.
    :param optimistic_encoding_detection:
        Should feedparser use only a prefix of the feed to detect encodings
        (uses less memory, but the wrong encoding may be detected in rare cases).
        Defaults to the value of
        :data:`feedparser.OPTIMISTIC_ENCODING_DETECTION`, which is ``True``.

    """
    pass


def _parse_file_inplace(
    file: IO[bytes] | IO[str],
    result: dict,
    *,
    resolve_relative_uris: bool | None = None,
    sanitize_html: bool | None = None,
    optimistic_encoding_detection: bool | None = None,
) -> None:
    # Avoid a cyclic import.
    pass
