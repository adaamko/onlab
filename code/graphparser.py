#!/usr/bin/python
import pydot
import pyparsing
import json
import pygraphviz as pgv
import sys


G = pgv.AGraph(sys.argv[1])

s = open(sys.argv[2], 'r').read()
d = eval(s)


for n in G.nodes():
	if n.attr['label'] == d['arg2']:
		for e in G.edges():
			if e[0] == n:
				if e.attr['label'] == '0':
					G.add_edge(d['arg3'], e[1], label='0')

for n in G.nodes():
        if n.attr['label'] == d['arg2']:
                for e in G.edges():
                        if e[0] == n:
                                if e.attr['label'] == '2':
                                        G.add_edge(d['arg1'], e[1], label='0')

G.layout()
G.draw('file.png')
