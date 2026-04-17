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

import base64
import binascii
import copy
import html.entities
import re
import xml.sax.saxutils

from .html import _cp1252
from .namespaces import _base, cc, dc, georss, itunes, mediarss, psc
from .sanitizer import HTMLSanitizer, sanitize_html
from .urls import _urljoin, make_safe_absolute_uri, resolve_relative_uris
from .util import FeedParserDict

email_pattern = re.compile(
    r"(([a-zA-Z0-9_.+-]+)@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.)"
    r"|(([a-zA-Z0-9-]+\.)+))([a-zA-Z]{2,4}|[0-9]{1,3})(]?))"
    r"(\?subject=\S+)?"
)


class XMLParserMixin(
    _base.Namespace,
    cc.Namespace,
    dc.Namespace,
    georss.Namespace,
    itunes.Namespace,
    mediarss.Namespace,
    psc.Namespace,
):
    namespaces = {
        "": "",
        "http://backend.userland.com/rss": "",
        "http://blogs.law.harvard.edu/tech/rss": "",
        "http://purl.org/rss/1.0/": "",
        "http://my.netscape.com/rdf/simple/0.9/": "",
        "http://example.com/newformat#": "",
        "http://example.com/necho": "",
        "http://purl.org/echo/": "",
        "uri/of/echo/namespace#": "",
        "http://purl.org/pie/": "",
        "http://purl.org/atom/ns#": "",
        "http://www.w3.org/2005/Atom": "",
        "http://purl.org/rss/1.0/modules/rss091#": "",
        "http://webns.net/mvcb/": "admin",
        "http://purl.org/rss/1.0/modules/aggregation/": "ag",
        "http://purl.org/rss/1.0/modules/annotate/": "annotate",
        "http://media.tangent.org/rss/1.0/": "audio",
        "http://backend.userland.com/blogChannelModule": "blogChannel",
        "http://creativecommons.org/ns#license": "cc",
        "http://web.resource.org/cc/": "cc",
        "http://cyber.law.harvard.edu/rss/creativeCommonsRssModule.html": (
            "creativeCommons"
        ),
        "http://backend.userland.com/creativeCommonsRssModule": "creativeCommons",
        "http://purl.org/rss/1.0/modules/company": "co",
        "http://purl.org/rss/1.0/modules/content/": "content",
        "http://my.theinfo.org/changed/1.0/rss/": "cp",
        "http://purl.org/dc/elements/1.1/": "dc",
        "http://purl.org/dc/terms/": "dcterms",
        "http://purl.org/rss/1.0/modules/email/": "email",
        "http://purl.org/rss/1.0/modules/event/": "ev",
        "http://rssnamespace.org/feedburner/ext/1.0": "feedburner",
        "http://freshmeat.net/rss/fm/": "fm",
        "http://xmlns.com/foaf/0.1/": "foaf",
        "http://www.w3.org/2003/01/geo/wgs84_pos#": "geo",
        "http://www.georss.org/georss": "georss",
        "http://www.opengis.net/gml": "gml",
        "http://postneo.com/icbm/": "icbm",
        "http://purl.org/rss/1.0/modules/image/": "image",
        "http://www.itunes.com/DTDs/PodCast-1.0.dtd": "itunes",
        "http://example.com/DTDs/PodCast-1.0.dtd": "itunes",
        "http://purl.org/rss/1.0/modules/link/": "l",
        "http://search.yahoo.com/mrss": "media",
        # Version 1.1.2 of the Media RSS spec added the trailing slash on the namespace
        "http://search.yahoo.com/mrss/": "media",
        "http://madskills.com/public/xml/rss/module/pingback/": "pingback",
        "http://prismstandard.org/namespaces/1.2/basic/": "prism",
        "http://www.w3.org/1999/02/22-rdf-syntax-ns#": "rdf",
        "http://www.w3.org/2000/01/rdf-schema#": "rdfs",
        "http://purl.org/rss/1.0/modules/reference/": "ref",
        "http://purl.org/rss/1.0/modules/richequiv/": "reqv",
        "http://purl.org/rss/1.0/modules/search/": "search",
        "http://purl.org/rss/1.0/modules/slash/": "slash",
        "http://schemas.xmlsoap.org/soap/envelope/": "soap",
        "http://purl.org/rss/1.0/modules/servicestatus/": "ss",
        "http://hacks.benhammersley.com/rss/streaming/": "str",
        "http://purl.org/rss/1.0/modules/subscription/": "sub",
        "http://purl.org/rss/1.0/modules/syndication/": "sy",
        "http://schemas.pocketsoap.com/rss/myDescModule/": "szf",
        "http://purl.org/rss/1.0/modules/taxonomy/": "taxo",
        "http://purl.org/rss/1.0/modules/threading/": "thr",
        "http://purl.org/rss/1.0/modules/textinput/": "ti",
        "http://madskills.com/public/xml/rss/module/trackback/": "trackback",
        "http://wellformedweb.org/commentAPI/": "wfw",
        "http://purl.org/rss/1.0/modules/wiki/": "wiki",
        "http://www.w3.org/1999/xhtml": "xhtml",
        "http://www.w3.org/1999/xlink": "xlink",
        "http://www.w3.org/XML/1998/namespace": "xml",
        "http://podlove.org/simple-chapters": "psc",
    }
    _matchnamespaces: dict[str, str] = {}

    can_be_relative_uri = {
        "comments",
        "docs",
        "href",
        "icon",
        "id",
        "link",
        "logo",
        "url",
        "wfw_comment",
        "wfw_commentrss",
    }

    can_contain_relative_uris = {
        "content",
        "copyright",
        "description",
        "info",
        "rights",
        "subtitle",
        "summary",
        "tagline",
        "title",
    }

    can_contain_dangerous_markup = {
        "content",
        "copyright",
        "description",
        "info",
        "rights",
        "subtitle",
        "summary",
        "tagline",
        "title",
    }

    html_types = {
        "application/xhtml+xml",
        "text/html",
    }

    def __init__(self):
        if not self._matchnamespaces:
            for k, v in self.namespaces.items():
                self._matchnamespaces[k.lower()] = v
        self.feeddata = FeedParserDict()  # feed-level data
        self.entries = []  # list of entry-level data
        self.version = ""  # feed type/version, see SUPPORTED_VERSIONS
        self.namespaces_in_use = {}  # dictionary of namespaces defined by the feed
        self.resolve_relative_uris = False
        self.sanitize_html = False

        # the following are used internally to track state;
        # this is really out of control and should be refactored
        self.infeed = 0
        self.inentry = 0
        self.incontent = 0
        self.intextinput = 0
        self.inimage = 0
        self.inauthor = 0
        self.incontributor = 0
        self.inpublisher = 0
        self.insource = 0
        self.isentrylink = 0

        self.sourcedata = FeedParserDict()
        self.contentparams = FeedParserDict()
        self._summaryKey = None
        self.namespacemap = {}
        self.elementstack = []
        self.basestack = []
        self.langstack = []
        self.svgOK = 0
        self.title_depth = -1
        self.depth = 0
        self.hasContent = 0
        if self.lang:
            self.feeddata["language"] = self.lang.replace("_", "-")

        # A map of the following form:
        #     {
        #         object_that_value_is_set_on: {
        #             property_name: depth_of_node_property_was_extracted_from,
        #             other_property: depth_of_node_property_was_extracted_from,
        #         },
        #     }
        self.property_depth_map = {}
        super().__init__()

    def _normalize_attributes(self, kv):
        raise NotImplementedError

    def unknown_starttag(self, tag, attrs):
        # increment depth counter
        pass

    def unknown_endtag(self, tag):
        # match namespaces
        pass

    def handle_charref(self, ref):
        # Called for each character reference, e.g. for '&#160;', ref is '160'
        pass

    def handle_entityref(self, ref):
        # Called for each entity reference, e.g. for '&copy;', ref is 'copy'
        pass

    def handle_data(self, text, escape=1):
        # Called for each block of plain text, i.e. outside of any tag and
        # not containing any character or entity references
        pass

    def handle_comment(self, text):
        # Called for each comment, e.g. <!-- insert message here -->
        pass

    def handle_pi(self, text):
        # Called for each processing instruction, e.g. <?instruction>
        pass

    def handle_decl(self, text):
        pass

    def parse_declaration(self, i):
        # Override internal declaration handler to handle CDATA blocks.
        pass

    @staticmethod
    def map_content_type(content_type):
        pass

    def track_namespace(self, prefix, uri):
        pass

    def resolve_uri(self, uri):
        pass

    @staticmethod
    def decode_entities(element, data):
        pass

    @staticmethod
    def strattrs(attrs):
        pass

    def push(self, element, expecting_text):
        pass

    def pop(self, element, strip_whitespace=1):
        pass

    def push_content(self, tag, attrs_d, default_content_type, expecting_text):
        pass

    def pop_content(self, tag):
        pass

    # a number of elements in a number of RSS variants are nominally plain
    # text, but this is routinely ignored.  This is an attempt to detect
    # the most common cases.  As false positives often result in silent
    # data loss, this function errs on the conservative side.
    @staticmethod
    def looks_like_html(s):
        """
        :type s: str
        :rtype: bool
        """
        pass

    def _map_to_standard_prefix(self, name):
        pass

    def _get_attribute(self, attrs_d, name):
        pass

    def _is_base64(self, attrs_d, contentparams):
        pass

    @staticmethod
    def _enforce_href(attrs_d):
        pass

    def _save(self, key, value, overwrite=False):
        pass

    def _get_context(self):
        pass

    def _save_author(self, key, value, prefix="author"):
        pass

    def _save_contributor(self, key, value):
        pass

    def _sync_author_detail(self, key="author"):
        pass

    def _add_tag(self, term, scheme, label):
        pass

    def _start_tags(self, attrs_d):
        # This is a completely-made up element. Its semantics are determined
        # only by a single feed that precipitated bug report 392 on Google Code.
        # In short, this is junk code.
        pass

    def _end_tags(self):
        pass
