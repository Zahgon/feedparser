# Character encoding routines
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

from __future__ import annotations

import codecs
import io
import re
import typing

try:
    try:
        import cchardet as chardet  # type: ignore[import]
    except ImportError:
        import chardet  # type: ignore[no-redef]
except ImportError:
    lazy_chardet_encoding = None
else:

    def lazy_chardet_encoding(data):
        pass


from .exceptions import (
    CharacterEncodingOverride,
    CharacterEncodingUnknown,
    FeedparserError,
    NonXMLContentType,
)

# Each marker represents some of the characters of the opening XML
# processing instruction ('<?xm') in the specified encoding.
EBCDIC_MARKER = b"\x4c\x6f\xa7\x94"
UTF16BE_MARKER = b"\x00\x3c\x00\x3f"
UTF16LE_MARKER = b"\x3c\x00\x3f\x00"
UTF32BE_MARKER = b"\x00\x00\x00\x3c"
UTF32LE_MARKER = b"\x3c\x00\x00\x00"

ZERO_BYTES = b"\x00\x00"

# Match the opening XML declaration.
# Example: <?xml version="1.0" encoding="utf-8"?>
RE_XML_DECLARATION = re.compile(r"^<\?xml[^>]*?>")

# Capture the value of the XML processing instruction's encoding attribute.
# Example: <?xml version="1.0" encoding="utf-8"?>
RE_XML_PI_ENCODING = re.compile(rb'^<\?.*encoding=[\'"](.*?)[\'"].*\?>')


def parse_content_type(line: str) -> tuple[str, str]:
    """Parse an HTTP Content-Type header.

    The return value will be a tuple of strings:
    the MIME type, and the value of the "charset" (if any).

    This is a custom replacement for Python's cgi.parse_header().
    The cgi module will be removed in Python 3.13.
    """
    pass


def convert_to_utf8(
    http_headers: dict[str, str], data: bytes, result: dict[str, typing.Any]
) -> bytes:
    """Detect and convert the character encoding to UTF-8."""
    pass


# How much to read from a binary file in order to detect encoding.
# In initial tests, 4k was enough for ~160 mostly-English feeds;
# 64k seems like a safe margin.
CONVERT_FILE_PREFIX_LEN = 2**16

# How much to read from a text file, and use as an utf-8 bytes prefix.
# Note that no encoding detection is needed in this case.
CONVERT_FILE_STR_PREFIX_LEN = 2**13

CONVERT_FILE_TEST_CHUNK_LEN = 2**16


def convert_file_to_utf8(
    http_headers, file, result, optimistic_encoding_detection=True
):
    """Like convert_to_utf8(), but for a stream.

    Unlike convert_to_utf8(), do not read the entire file in memory;
    instead, return a text stream that decodes it on the fly.
    This should consume significantly less memory,
    because it avoids (repeatedly) converting the entire file contents
    from bytes to str and back.

    To detect the encoding, only a prefix of the file contents is used.
    In rare cases, the wrong encoding may be detected for this prefix;
    use optimistic_encoding_detection=False to use the entire file contents
    (equivalent to a plain convert_to_utf8() call).

    Args:
        http_headers (dict): The response headers.
        file (IO[bytes] or IO[str]): A read()-able (binary) stream.
        result (dict): The result dictionary.
        optimistic_encoding_detection (bool):
            If true, use only a prefix of the file content to detect encoding.

    Returns:
        StreamFactory: a stream factory, with the detected encoding set, if any

    """
    pass


def convert_file_prefix_to_utf8(
    http_headers,
    file: typing.IO[bytes],
    result,
    *,
    prefix_len: int = CONVERT_FILE_PREFIX_LEN,
    read_to_ascii_len: int = 2**8,
) -> bytes:
    """Like convert_to_utf8(), but only use the prefix of a binary file.

    Set result like convert_to_utf8() would.

    Return the updated prefix, as bytes.

    """
    pass


def read_to_after_ascii_byte(file: typing.IO[bytes], max_len: int) -> bytes:
    pass


class MissingEncoding(io.UnsupportedOperation):
    pass


class StreamFactory:
    """Decode on the fly a binary stream that *may* have a known encoding.

    If the underlying stream is seekable, it is possible to call
    the get_{text,binary}_file() methods more than once.

    """

    def __init__(self, prefix: bytes, file, encoding=None):
        self.prefix = prefix
        self.file = ResetFileWrapper(file)
        self.encoding = encoding
        self.should_reset = False

    def get_text_file(self, fallback_encoding=None, errors="strict"):
        pass

    def get_binary_file(self):
        pass

    def get_file(self):
        pass

    def reset(self):
        pass


class ResetFileWrapper:
    """Given a seekable file, allow reading its content again
    (from the current position) by calling reset().

    """

    def __init__(self, file):
        self.file = file
        try:
            self.file_initial_offset = file.tell()
        except OSError:
            self.file_initial_offset = None

    def read(self, size=-1):
        pass

    def reset(self):
        # raises io.UnsupportedOperation if the underlying stream is not seekable
        pass


class PrefixFileWrapper:
    """Stitch a (possibly modified) prefix and a file into a new file object.

    >>> file = io.StringIO('abcdef')
    >>> file.read(2)
    'ab'
    >>> wrapped = PrefixFileWrapper(file.read(2).upper(), file)
    >>> wrapped.read()
    'CDef'

    """

    def __init__(self, prefix, file):
        self.prefix = prefix
        self.file = file
        self.offset = 0

    def read(self, size=-1):
        pass

    def close(self):
        # do not touch the underlying stream
        pass
