# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

#
# This file contains renderers from the supported input formats.
# As of [[2020-01-09]]:
# - markdown
# - orgmode

import re
from . import config
from . import regexes
from . import util 
from marko import Markdown, inline
from orgpython import to_html
from html import escape
from urllib.parse import quote


# Markdown
class WikilinkElement(inline.InlineElement):
    pattern = regexes.WIKILINK.pattern
    parse_children = True

    def __init__(self, match):
        self.target = match.group(1)

class WikilinkRendererMixin(object):

    # This name is magic; it must match render_<class_name_in_snake_case>.
    def render_wikilink_element(self, element):
        # return '<span class="wikilink-marker">[[</span><a href="{}">{}</a><span class="wikilink-marker">]]</span>'.format(
        return '<span class="wikilink-marker">[[</span><a href="{}" class="wikilink">{}</a><span class="wikilink-marker">]]</span>'.format(
            # util.canonical_wikilink(self.escape_url(element.target)), self.render_children(element)
            quote(util.canonical_wikilink(element.target)), self.render_children(element)
        )
# Modified the default behavior of HTMLRenderer to prevent XSS
class ModifiedHTMLRendererMixin(object):

    def render_html_block(self, element):
        return escape(element.children)

    def render_link(self, element):
        template = '<a href="{}"{}>{}</a>'
        title = (
            ' title="{}"'.format(self.escape_html(element.title))
            if element.title
            else ""
        )
        url = self.escape_url(element.dest)
        body = self.render_children(element)

        # https://raw.githubusercontent.com/cujanovic/Markdown-XSS-Payloads/master/Markdown-XSS-Payloads.txt
        blocked_schemas = ['data', 'javascript', 'vbscript']
        for schema in blocked_schemas:
            if url.lower().startswith(schema):
                return url

        return template.format(url, title, body)

class Extras():
    elements = [WikilinkElement]
    renderer_mixins = [WikilinkRendererMixin, ModifiedHTMLRendererMixin]
        

markdown = Markdown(extensions=[Extras])


# Org-mode -- simple but, well, bad for now.
orgmode = to_html


# Embeds.
# The *application* of this pattern could perhaps be here instead of in... hmm, db.py? Yeah, that doesn't make sense.
# TODO: [[refactor]].

# Twitter embeds.
# def add_twitter_embeds(content, subnode):
#     TWITTER_REGEX='(https://twitter.com/\w+/status/[0-9]+)'
#     TWITTER_EMBED='<blockquote class="twitter-tweet" data-dnt="true" data-theme="dark"><a href="\\1"></blockquote><script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>'
#     return re.sub(TWITTER_REGEX, TWITTER_EMBED, content)

# def add_twitter_pull(content, subnode):
#     TWITTER_REGEX='(https://twitter.com/\w+/status/[0-9]+)'
#     TWITTER_EMBED='\\1 <button class="pull-tweet" value="\\1">pull</button>'
#     return re.sub(TWITTER_REGEX, TWITTER_EMBED, content)

# def add_mastodon_pull(content, subnode):
#     MASTODON_REGEX='(https://[a-zA-Z-.]+/web/statuses/[0-9]+)'
#     MASTODON_REGEX_ALT='(https://[a-zA-Z-.]+/@\w+/[0-9]+)'
#     MASTODON_EMBED='\\1 <button class="pull-mastodon-status" value="\\1">pull</button>'
#     ret = re.sub(MASTODON_REGEX, MASTODON_EMBED, content)
#     ret = re.sub(MASTODON_REGEX_ALT, MASTODON_EMBED, ret)
#     return ret

# def add_url_pull(content, subnode):
#     # hacky but, hey, it seems to work often enough and covers wikipedia + wikidata.
#     # https://stackoverflow.com/questions/3809401/what-is-a-good-regular-expression-to-match-a-url
#     # -> https://regexr.com/3e6m0
#     # 'http(s)?:\/\/.)?(www\.)?[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*'

#     # URL_REGEX='(\[\[go\]\]) (.+:\/\/.+)'
#     # @(https?|ftp)://(-\.)?([^\s/?\.#-]+\.?)+(/[^\s]*)?$@iS
#     # URL_REGEX='(https?:\/\/([^s/?\<>]+wiki.+)'
#     # URL_REGEX="^[a-z0-9!#$%&'-*+\/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+\/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?"
#     # URL_REGEX='http(s)?:\/\/.)?(www\.)?[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*'
#     URL_REGEX='(https?:\/\/\S+wiki\S+)'
#     URL_EMBED='\\1 <button class="pull-url" value="\\1">pull</button>'

#     ret = re.sub(URL_REGEX, URL_EMBED, content)
#     return ret

# def add_go_button(content, subnode):
#     URL_REGEX='(\[\[go\]\]) (.+:\/\/.+)'
#     URL_EMBED='<button class="go-url" value="\\2">go</button> \\2'
#     ret = re.sub(URL_REGEX, URL_EMBED, content)
#     return ret

# Trim front matter until we do something useful with it.
def trim_front_matter(content, subnode):
    FRONT_MATTER_REGEX = '---(\n.*)*---'
    return re.sub(FRONT_MATTER_REGEX, '', content, flags=re.MULTILINE)

#def content_to_obsidian_embeds(content):
#    match = regexes.WIKILINKS.findall(content)
#    if match:
#        # Work around broken forward links due to org mode convention I didn't think of.
#        # TODO: make link parsing format-aware.
#        return [util.canonical_wikilink(m) for m in match if '][' not in m]
#    else:
#        return []

# Obsidian pasted images / attachments.
# def add_obsidian_embeds(content, subnode):
#     OBSIDIAN_REGEX = re.compile('!' + regexes.WIKILINK.pattern)
#     OBSIDIAN_EMBED=f'<a href="/raw/garden/{subnode.user}/\\1"><img class="image-embed" src="/raw/garden/{subnode.user}/\\1"></img><p class="obsidian-embed"></a>⥅ [[\\1]]</p>'
#     return re.sub(OBSIDIAN_REGEX, OBSIDIAN_EMBED, content)

def preprocess(content, subnode=''):
    filters = [trim_front_matter]
    for f in filters:
        content = f(content, subnode)
    return content

def postprocess(content, subnode=''):
    # filters = [add_twitter_embeds]
    filters = []
    for f in filters:
        content = f(content, subnode)
    return content

