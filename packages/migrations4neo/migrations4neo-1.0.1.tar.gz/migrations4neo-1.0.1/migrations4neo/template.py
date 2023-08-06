body = '''# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import os

from py2neo import Graph

graph = Graph(os.getenv('NEO4J_REST_URL'))


# MIGRATION: {}


def up():
    graph.run(""" """)


def down():
    graph.run(""" """)
'''
