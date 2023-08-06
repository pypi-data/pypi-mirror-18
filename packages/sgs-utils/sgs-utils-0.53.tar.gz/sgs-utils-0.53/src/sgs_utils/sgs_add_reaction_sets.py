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

ID = "reaction_id"
RXN_NAME = "name"


# compute the set of reactions acting in the SGS
def usable_reaction(reaction_graph, map_gene_to_reaction, set_of_genes, start_reaction, end_reaction, map_uncatalyzed_reaction_links={}):
	# generate subgraph
	reaction_set = set()
	for g in set_of_genes:
		# take in account the catalytic/non catalytic information
		# ac : active catalytic
		# na : non active catalytic
		# nc : non catalytic
		if not (g.startswith("ac:") or g.startswith("na:")):
			if g.startswith("nc:"):
				g = g[3:]
			if g in map_gene_to_reaction:
				for r in map_gene_to_reaction[g]:
					reaction_set.add(r)
	#print reaction_set
	subgraph = reaction_graph.subgraph(reaction_set)
	#print subgraph.nodes()
	#print subgraph.edges()
	# compute usable states
	#print start_reaction
	# nx.predecessor return the list of nodes that have start_reaction as predecessor
	result = set(nx.predecessor(subgraph, start_reaction).keys())
	subgraph.reverse(copy=False)
	result = result & set(nx.predecessor(subgraph, end_reaction).keys())
	subgraph.reverse(copy=False)
	subgraph = subgraph.subgraph(result)
	for s,t in subgraph.edges():
		if (s,t) in map_uncatalyzed_reaction_links:
			result.update(["nc:"+ x for x in map_uncatalyzed_reaction_links[(s,t)]])
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



def translate(reaction_list, map_reaction_name):
	result = []
	for r in reaction_list:
		prefix = ""
		if r.startswith("nc:"):
			prefix = r[:3]
			r = r[3:]
		if r in map_reaction_name:
			result.append(prefix + map_reaction_name[r])
		else:
			result.append(prefix + "None")
	return result

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
		%(prog)s reaction_graph.txt catalyze.txt sgs.txt > sgs_with_reaction.txt
		'''), prog = prog
	)

	# Requiered arguments
	#####################
	parser.add_argument("reaction_graph_file", help="Reaction graph file")
	parser.add_argument("catalyze_file", help="Reaction/Gene catalytic association file (.tsv)")
	parser.add_argument("sgs_file", help="The list of SGS")

	# Optional arguments
	####################
	parser.add_argument("-o", "--output", default=None, help="set an output file")
	parser.add_argument("-a", "--uncatalyzed_link_annotation", help="Put back the uncatalyzed reactions")
	parser.add_argument("-n", "--add_reaction_name", help="Add a colunm with the common reaction name", metavar="REACTION_LIST")

	args = parser.parse_args(argv)

	stream_out = sys.stdout
	if args.output:
		stream_out = open(args.output, 'w')

	reaction_graph = load_directed_graph(args.reaction_graph_file)
	#sys.stderr.write("%s\n" % (str(reaction_graph.nodes())))
	#print reaction_graph.edges()
	map_gene_to_reaction = reverse_map_id_to_set(load_map_id_to_set(args.catalyze_file, silent_warning=True))
	#sys.stderr.write("%s\n" % (str(map_gene_to_reaction)))
	headers, sgs_list = load_csv_list(args.sgs_file)
	#print headers

	map_uncatalyzed_reaction_links={}
	if args.uncatalyzed_link_annotation:
		with open(args.uncatalyzed_link_annotation, "r") as reader:
			lines = reader.read().replace('\r\n','\n').splitlines()
			for l in lines:
				tab = l.split("\t")
				map_uncatalyzed_reaction_links[(tab[0],tab[1])] = tab[2].split(" ")
		reader.close()

	stream_out.write("%s\treaction_set" % (header_to_str(headers)))

	if args.add_reaction_name:
		map_reaction_name = {}
		stream_out.write("\treaction_name_set")
		header_reaction_list, reaction_list = load_csv_list(args.add_reaction_name)
		# fill the map to convert the reaction ids to names
		for l in reaction_list:
			if RXN_NAME in header_reaction_list:
				 map_reaction_name[l[header_reaction_list[ID]]] = l[header_reaction_list[RXN_NAME]]

	stream_out.write("\n")
	for l in sgs_list:
		gene_set = l[headers["gene_set"]].split()
		start = l[headers["start_reaction"]]
		end =  l[headers["end_reaction"]]
		#print gene_set, start, end
		reaction_set = usable_reaction(reaction_graph, map_gene_to_reaction, gene_set, start, end, map_uncatalyzed_reaction_links)
		reaction_set = list(reaction_set)
		reaction_set.sort()
		#print reaction_set
		stream_out.write("%s\t%s" % ("\t".join(l), " ".join(reaction_set)))
		if args.add_reaction_name:
			reaction_name = translate(reaction_set, map_reaction_name)
			stream_out.write("\t\"%s\"" % ("\" \"".join(reaction_name)))
		stream_out.write("\n")
	#end for
	if args.output:
		stream_out.close()


if __name__ == '__main__':
	main(sys.argv[1:])
