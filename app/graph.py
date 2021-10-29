# Copyright 2021 Google LLC
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
# The [[agora]] models search as an open market of providers (who bid content for each query) and users (who are interested in media of any type which is relevant within a given [[context]], which maps to a query).

import re
import urllib
from flask import current_app, redirect, url_for
from . import db
from . import util

from json import dumps
from rdflib import Graph, Namespace, URIRef


def add_node(node: db.Node, g: Graph, only_forward=False):

    for linked_node in node.forward_links():
        if re.search('<.*>', linked_node):
            # work around links with html in them (?)
            continue
        if '|' in linked_node:
            # early support for https://anagora.org/go/agora-rfc/2
            linked_node = re.sub('|.*', '', linked_node)
        # this does away with lots of encoding problems in irregular links, but also encodes unicode characters, so some legibility is lost in the final result unless it is urldecoded.
        linked_node = urllib.parse.quote_plus(linked_node)
        n0 = node.wikilink
        n1 = linked_node
        g.add((
            URIRef(f"/{n0}"),
            URIRef(f"/links"),
            URIRef(f"/{n1}"),
        ))

    if only_forward:
        return

    for backlinking_node in node.back_links():
        n0 = backlinking_node
        n1 = node.wikilink
        g.add((
            URIRef(f"/{n0}"),
            URIRef(f"/links"),
            URIRef(f"/{n1}"),
        ))

    for pushing_node in node.pushing_nodes():
        n0 = node.wikilink
        n1 = linked_node
        g.add((
            URIRef(f"/{n0}"),
            URIRef(f"/pushes"),
            URIRef(f"/{n1}"),
        ))

    for pulling_node in node.pulling_nodes():
        n0 = pulling_node
        n1 = node.wikilink
        g.add((
            URIRef(f"/{n0}"),
            URIRef(f"/pulls"),
            URIRef(f"/{n1}"),
        ))

def parse_node(node: db.Node) -> dict:

    d = dict()
    d["nodes"] = []
    d["links"] = []
    unique_nodes = set()

    forward_links = node.forward_links()
    if forward_links:
        unique_nodes.add('forward link')
        for linked_node in forward_links:
            if re.search('<.*>', linked_node):
                # work around links with html in them (?)
                continue
            if '|' in linked_node:
                # early support for https://anagora.org/go/agora-rfc/2
                linked_node = re.sub('|.*', '', linked_node)
            n0 = node.wikilink
            n1 = linked_node
            d["links"].append({'source': n0, 'target': "forward link"})
            d["links"].append({'source': "forward link", 'target': n1})
            unique_nodes.add(n0)
            unique_nodes.add(n1)

    back_links = node.back_links()
    if back_links:
        unique_nodes.add('back link')
        for backlinking_node in back_links:
            n0 = backlinking_node
            n1 = node.wikilink
            d["links"].append({'source': n0, 'target': "back link"})
            d["links"].append({'source': "back link", 'target': n1})
            unique_nodes.add(n0)
            unique_nodes.add(n1)

    pushing_nodes = node.pushing_nodes()
    if pushing_nodes:
        unique_nodes.add('push')
        for pushing_node in pushing_nodes:
            n0 = node.wikilink
            n1 = pushing_node.wikilink
            d["links"].append({'source': n0, 'target': "push"})
            d["links"].append({'source': "push", 'target': n1})
            unique_nodes.add(n0)
            unique_nodes.add(n1)

    pulling_nodes = node.pulling_nodes()
    if pulling_nodes:
        unique_nodes.add('pull')
        for pulling_node in pulling_nodes:
            n0 = pulling_node.wikilink
            n1 = node.wikilink
            d["links"].append({'source': n0, 'target': "pull"})
            d["links"].append({'source': "pull", 'target': n1})
            unique_nodes.add(n0)
            unique_nodes.add(n1)

    for n in unique_nodes:
        if n == node.wikilink:
            d["nodes"].append({'id': n, 'name': n, 'val': 8, 'group': 1})
        elif n == 'pull':
            d["nodes"].append({'id': n, 'name': n, 'val': 4, 'group': 2})
        elif n == 'push':
            d["nodes"].append({'id': n, 'name': n, 'val': 4, 'group': 3})
        elif n == 'back link':
            d["nodes"].append({'id': n, 'name': n, 'val': 2, 'group': 2})
        elif n == 'forward link':
            d["nodes"].append({'id': n, 'name': n, 'val': 2, 'group': 3})
        else:
            d["nodes"].append({'id': n, 'name': n, 'val': 1, 'group': 6})

    return d


def json_node(node):
    # format: /force-graph

    d = parse_node(node)
    return dumps(d)


# technically doesn't belong here but... perhaps this becomes graph.py eventually.
def json_nodes(nodes):
    # format: /force-graph
    # this first redoes the RDF graph and then converts it to JSON.
    # the code duplication can be fixed with refactoring; more important is whether going through RDF makes sense at all.
    # I think because RDF does some cleanup to get to "well formed ids" there might be enough of a benefit from reusing that.

    g = Graph()
    agora = Namespace(f"/")
    g.namespace_manager.bind('agora', agora)

    print(f"jsoing agora using forward links only")
    node_count = len(nodes)
    print(f"node count: {node_count}")

    for node in nodes:
        add_node(node, g, only_forward=True)

    d = {}
    d["nodes"] = []
    d["links"] = []
    unique_nodes = set()

    for n0, _, n1 in g.triples((None, None, None)):
        # this step needed because dicts don't fit in sets in python because they're not hashable.
        unique_nodes.add(n0)
        unique_nodes.add(n1)

    for node in unique_nodes:
        d["nodes"].append({'id': node, 'name': node, 'val': 1})

    for n0, link, n1 in g.triples((None, None, None)):
        d["links"].append({'source': n0, 'target': n1})
        
    return dumps(d)

