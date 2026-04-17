# Copyright 2010-2025 Kurt McKee <contactme@kurtmckee.org>
# Copyright 2002-2008 Mark Pilgrim
# All rights reserved.
#
# This file is a part of feedparser.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
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

import re
import time

# ISO-8601 date parsing routines written by Fazal Majid.
# The ISO 8601 standard is very convoluted and irregular - a full ISO 8601
# parser is beyond the scope of feedparser and would be a worthwhile addition
# to the Python library.
# A single regular expression cannot parse ISO 8601 date formats into groups
# as the standard is highly irregular (for instance is 030104 2003-01-04 or
# 0301-04-01), so we use templates instead.
# Please note the order in templates is significant because we need a
# greedy match.
_iso8601_tmpl = [
    "YYYY-?MM-?DD",
    "YYYY-0MM?-?DD",
    "YYYY-MM",
    "YYYY-?OOO",
    "YY-?MM-?DD",
    "YY-?OOO",
    "YYYY",
    "-YY-?MM",
    "-OOO",
    "-YY",
    "--MM-?DD",
    "--MM",
    "---DD",
    "CC",
    "",
]

_iso8601_re = [
    tmpl.replace("YYYY", r"(?P<year>\d{4})")
    .replace("YY", r"(?P<year>\d\d)")
    .replace("MM", r"(?P<month>[01]\d)")
    .replace("DD", r"(?P<day>[0123]\d)")
    .replace("OOO", r"(?P<ordinal>[0123]\d\d)")
    .replace("CC", r"(?P<century>\d\d$)")
    + r"(T?(?P<hour>\d{2}):(?P<minute>\d{2})"
    + r"(:(?P<second>\d{2}))?"
    + r"(\.(?P<fracsecond>\d+))?"
    + r"(?P<tz>[+-](?P<tzhour>\d{2})(:(?P<tzmin>\d{2}))?|Z)?)?"
    for tmpl in _iso8601_tmpl
]
_iso8601_matches = [re.compile(regex).match for regex in _iso8601_re]


def _parse_date_iso8601(date_string):
    """Parse a variety of ISO-8601-compatible formats like 20040105"""
    pass
