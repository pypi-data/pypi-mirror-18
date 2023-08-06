#!/usr/bin/env python
# Copyright (c) 2013, Philippe Bordron <philippe.bordron@gmail.com>
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

import sys
import os
try:
	from libs import tabfiles
except ImportError:
	from sgs_utils.libs import tabfiles

## important columns
ID = "reaction_id"
REACTANTS = "reactants"
PRODUCTS = "products"
#ASSOCIATION="association"
#EC_NUMBER = "ec_number"
REVERSIBLE = "reversible"

def complete_map(map_, key, values):
	try:
		map_[key].update(values)
	except KeyError:
		map_[key] = set(values)
	#end

def generate_reaction_graph(as_substract_map, as_product_map, set_removed_cpd):
	successors = {}
	for cpd, sub_reaction_set in as_substract_map.items():
		if cpd not in set_removed_cpd and cpd in as_product_map:
			prod_reaction_set = as_product_map[cpd]
			for r1 in sub_reaction_set:
				for r2 in prod_reaction_set:
					if r1 != r2:
						if r1 not in successors:
							successors[r1] = set()
						successors[r1].add(r2)
	return successors


def main (argv, prog = os.path.basename(sys.argv[0])):
	#sys.stderr.write("%s\n" % (" ".join(sys.argv)))

	import argparse
	import textwrap

	parser = argparse.ArgumentParser(
		formatter_class=argparse.RawDescriptionHelpFormatter,
		description=textwrap.dedent('''\
		Generate the reaction graph of a metabolic network from a list of reactions in .tsv file format.

		exemple:
		%(prog)s reaction_list.tsv [-c 40] > reaction_graph.txt
		'''), prog = prog
	)

	# Requiered arguments
	#####################
	parser.add_argument("reaction_list_file", help="reaction list in tabular file format (.tsv)")

	# Optional arguments
	####################
	parser.add_argument("-o", "--output", default=None, help="set an output file")
	parser.add_argument("-c", "--cutoff", type=int, default=-1, help="remove from reactions the compounds that appear in strictly more than CUTOFF reactions")
	parser.add_argument("-frev", "--force_reversible", default=False, action='store_true', help="consider all reactions as reversible") # will duplicate all the arcs
	parser.add_argument("-cofactors", "--remove_cofactors", nargs= "+", default=[], metavar='COFACTOR', help="list of cofactors that will be ignored during the graph construction")
	#parser.add_argument("-asso", "--association", choice=['ec', 'association'], help="Choose the association method")

	args = parser.parse_args(argv)
	cutoff = args.cutoff

	stream_out = sys.stdout
	if args.output:
		stream_out = open(args.output, 'w')

	compounds_count={}

	as_substract_map={} #map that associate each compound to the set of reactions where it is a substract
	as_product_map={} #map that associate each compound to the set of reactions where it is a product
	well_formed_reactions = []

	header, reaction_list = tabfiles.load_csv_list(args.reaction_list_file)
	for l in reaction_list:
		is_well_formed = True
		r = l[header[ID]]
		rev = tabfiles.str_to_bool(l[header[REVERSIBLE]])
		reactants = set(l[header[REACTANTS]].split())
		products = set(l[header[PRODUCTS]].split())
		if reactants:
			for c in reactants:
				complete_map(as_substract_map, c, [r])
		else:
			sys.stderr.write("Warning: %s has no left part. It will be not taken in account.\n" % (r))
			is_well_formed = False
		if products:
			for c in products:
				complete_map(as_product_map, c, [r])
		else:
			sys.stderr.write("Warning: %s has no right part. It will be not taken in account.\n" % (r))
			is_well_formed = False
		if is_well_formed:
			well_formed_reactions.append(r)
		if rev or args.force_reversible:
			for c in reactants:
				complete_map(as_product_map, c, [r])
			for c in products:
				complete_map(as_substract_map, c, [r])
		for c in reactants | products:
			try:
				compounds_count[c] = compounds_count[c]+1
			except KeyError:
				compounds_count[c] = 1
	map_removed_cpd = {}

	# list removed compounds
	for c in args.remove_cofactors:
		try:
			map_removed_cpd[c] = compounds_count[c]
		except:
			map_removed_cpd[c] = 0
	if cutoff > 0:
		for c, val in compounds_count.items():
			if val > cutoff:
				map_removed_cpd[c] = compounds_count[c]
				#sys.stderr.write("%s %s\n" %(val, c))
	if args.remove_cofactors:
		sys.stderr.write("Info: The following cofactors have been removed:\n\t%s\n" % ("\n\t".join(sorted(args.remove_cofactors))))

	removed_list = sorted(map_removed_cpd.items(), key=lambda removed: removed[1], reverse=True)
	if cutoff > 0:
		sys.stderr.write("Info: The following compounds have been cutted off (>%d):\n%s\n" % (cutoff, "\n".join('\t{0}\t{1}'.format(*reversed(el)) for el in removed_list)))

	# Export the reaction graph file
	reaction_graph = generate_reaction_graph(as_substract_map, as_product_map, map_removed_cpd.keys())
	number_of_vertices = len(well_formed_reactions)
	number_of_edges = 0
	for r1, succ in reaction_graph.items():
		for r2 in succ:
			stream_out.write("%s\t%s\n" % (r1, r2))
			number_of_edges += 1
	sys.stderr.write("Info: %d vertices and %d arcs\n" %(number_of_vertices, number_of_edges))
	if args.output:
		stream_out.close()
#end


if __name__ == '__main__':
	main(sys.argv[1:])
