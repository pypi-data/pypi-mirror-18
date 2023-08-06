#!/usr/bin/env python
# -*- coding: utf8 -*-
# Copyright (c) 2013-2015, Philippe Bordron <philippe.bordron@gmail.com>
#
# This file is part of SIPPER.
#
# SIPPER is free software: you can redistribute it and/or modify
# it under the terms of the GNU LESSER GENERAL PUBLIC LICENSE as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# SIPPER is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU LESSER GENERAL PUBLIC LICENSE for more details.
#
# You should have received a copy of the GNU LESSER GENERAL PUBLIC LICENSE
# along with SIPPER.  If not, see <http://www.gnu.org/licenses/>


import sys, os
try:
	from utils import *
except ImportError:
	from sgs_utils.utils import *
import networkx as nx

# compute the set of accessible and co-accessible nodes
def usefull_nodes(graph, src, target):
	# nx.predecessor return the list of nodes that have s as predecessor
	# then the keys give the list of accessible node from s.
	result = set(nx.predecessor(graph, src).keys())
	graph.reverse(copy=False)
	result = result & set(nx.predecessor(graph, target).keys())
	graph.reverse(copy=False)
	return result

def load_directed_graph(graph_file):
	graph = nx.DiGraph()
	with open(graph_file, "r") as in_graph:
		edges = in_graph.read().replace('\r\n','\n').splitlines()
		for l in edges:
			e = l.split()
			graph.add_edge(e[0],e[1])
	in_graph.close()
	return graph

################
# Main program #
################

# load genome to have genes position
def main (argv, prog = os.path.basename(sys.argv[0])):
	#sys.stderr.write("%s\n" % (" ".join(sys.argv)))

	import argparse
	import textwrap

	parser = argparse.ArgumentParser(
		formatter_class=argparse.RawDescriptionHelpFormatter,
		description=textwrap.dedent('''\
		Generate the reaction graph of a metabolic network from a list of reactions in .tsv file format.

		exemple:
		%(prog)s reaction_graph catalyze
		'''), prog = prog
	)

	# Requiered arguments
	#####################
	parser.add_argument("reaction_graph_file", help="Reaction graph file")
	parser.add_argument("catalyze_file", help="Reaction/Gene catalytic association file (.tsv)")
	parser.add_argument("output_reaction_graph_file", help="The output reaction graph")
	parser.add_argument("uncatalyzed_edge_file", help="The list of uncatalyzed 'shortcut' edges")


	# Optional arguments
	#####################
	parser.add_argument("-k", "--keep_non_catalytic_reactions", action='store_true', default=False, help="Keep the vertices (and related edges) corresponding to non catalytic reactions")

	args = parser.parse_args(argv)


	reaction_graph = load_directed_graph(args.reaction_graph_file)
	map_reaction_to_gene = load_map_id_to_set(args.catalyze_file, silent_warning=True)

	uncatalyzed_reaction_set = set(reaction_graph.nodes()) - set(map_reaction_to_gene.keys())
	#print(uncatalyzed_reaction_set)

	uncatalyzed_subgraph = reaction_graph.subgraph(uncatalyzed_reaction_set)
	#usefull_node={}
	# We compute the set of usefull nodes for each couple of non catalysed reaction
	map_annotation_non_catalytic_edge={}

	# We compute which are the supp edge for the reaction with a non catalysed reaction as neighbor
	for cc in nx.connected_components(nx.Graph(uncatalyzed_subgraph)):
#		for s, t in itertools.permutations(cc, 2):
		for s in cc:
			catalytic_predecessor = []
			for v in reaction_graph.predecessors(s):
				if v not in uncatalyzed_reaction_set:
					catalytic_predecessor.append(v)
			for t in cc:
				# we look if there is a neighbor of s that is a possible catalytic source.
				# and a neighbor of t that is a possible catalytic target.
				catalytic_successor = []
				for v in reaction_graph.successors(t):
					if v not in uncatalyzed_reaction_set:
						catalytic_successor.append(v)
				temp = usefull_nodes(uncatalyzed_subgraph, s , t)
				#usefull_node[(s,t)] = temp
				if temp:
					for rs in catalytic_predecessor:
						for rt in catalytic_successor:
							if rs != rt and not reaction_graph.has_edge(rs,rt):
								if (rs,rt) not in map_annotation_non_catalytic_edge:
									map_annotation_non_catalytic_edge[(rs,rt)] = set()
								map_annotation_non_catalytic_edge[(rs,rt)].update(temp)

	#print(usefull_node)

	for s,t in map_annotation_non_catalytic_edge.keys():
		reaction_graph.add_edge(s,t)

	if not args.keep_non_catalytic_reactions:
		reaction_graph.remove_nodes_from(uncatalyzed_reaction_set)

	output = open(args.output_reaction_graph_file, "w")
	for s,t in reaction_graph.edges():
		output.write("%s\t%s\n" % (s,t))
	output.close()

	output = open(args.uncatalyzed_edge_file, "w")
	for s,t in map_annotation_non_catalytic_edge.keys():
		output.write("%s\t%s\t%s\n" % (s,t, " ".join(sorted(map_annotation_non_catalytic_edge[(s,t)]))))
	output.close()
	sys.stderr.write("Info: %d vertices and %d arcs; %d non-catalytic arcs\n" %(reaction_graph.number_of_nodes(), reaction_graph.number_of_edges(), len(map_annotation_non_catalytic_edge)))


if __name__ == '__main__':
	main(sys.argv[1:])
