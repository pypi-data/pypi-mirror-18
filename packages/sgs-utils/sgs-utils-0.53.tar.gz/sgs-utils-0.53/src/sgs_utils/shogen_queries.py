#!/usr/bin/env python
# -*- coding: utf8 -*-
# Copyright (c) 2013-2014, Philippe Bordron <philippe.bordron@gmail.com>
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
	from utils import *
except ImportError:
	from sgs_utils.utils import *
import itertools

def update_dist(dist_map, x, y, d):
	if y<x:
		x,y = y,x
	try:
		if dist_map[(x,y)] > d:
			dist_map[(x,y)] = d
	except KeyError:
		dist_map[(x,y)] = d

def get_dist(dist_map, x, y):
	if y<x:
		x,y = y,x
	return dist_map[(x,y)]

def main (argv, prog = os.path.basename(sys.argv[0])):
	import argparse
	import textwrap
	parser = argparse.ArgumentParser(
		formatter_class=argparse.RawDescriptionHelpFormatter,
		description=textwrap.dedent('''\
		Compute and print reaction queries for shogen:

		exemple:
		%(prog)s chromosome.txt catalyze.txt.dat -maxg 10 > queries.txt
		'''), prog =  prog
	)

	# Requiered arguments
	#####################
	parser.add_argument("chr_file", help="Gene sequence of a chromosome")
	parser.add_argument("catalyze_file", help="Gene-reaction association file")

	parser.add_argument("-maxg", "--max_genomic_dist",  type=int, default=sys.maxint-1, help="Maximum distance in number of genes between two reactions")
	parser.add_argument("-ming", "--min_genomic_dist",  type=int, default=1, help="Minimum distance in number of genes between two reactions")

	## optionnal arguments
	parser.add_argument("-o", "--output",  type=argparse.FileType('w'), help="output to a file")
	parser.add_argument("-d", "--display_dist", default=False,  action='store_true', help="Display the minimal distance between to reactions in a thrid column")

	args = parser.parse_args(argv)

	if args.output:
		sys.stdout = args.output

	# chr = liste de genes
	gene_list = load_gene_sequence(args.chr_file)
	#print gene_list
	# chaque reaction associe a des genes
	map_reaction_to_genes = load_map_id_to_set(args.catalyze_file, silent_warning=True)
	# chaque gene associe a des reactions
	#map_gene_to_reactions = load_mapping(catalyze_file)
	map_gene_to_reactions = reverse_map_id_to_set(map_reaction_to_genes)
	#print map_gene_to_reactions
	# on parcourt de facon circulaire la liste avec une fenetre de gene_dist genes.
	# on prend les reactions associees
	queries={}
	dist_map={}
	for i in xrange(0,len(gene_list)):
		gs = gene_list[i]
		if gs in map_gene_to_reactions:
			rs_set = map_gene_to_reactions[gs]
			for d in xrange(max(1, args.min_genomic_dist), min(args.max_genomic_dist+1,len(gene_list))):
				j = (i + d)% len(gene_list)
				ge = gene_list[j]
				if ge in map_gene_to_reactions:
					re_set = map_gene_to_reactions[ge]
					# on ecrit les couples de reactions possibles.
					for rs in rs_set:
						for re in re_set:
							if rs != re:
								update_dist(dist_map, rs, re, d)
								if rs not in queries:
									queries[rs]=set()
								queries[rs].add(re)
								if re not in queries:
									queries[re]=set()
								queries[re].add(rs)

	for rs, rset in queries.items():
		for re in rset:
			if args.display_dist:
				sys.stdout.write('%s %s %d\n' %(re, rs, get_dist(dist_map, rs, re)))
			else:
				sys.stdout.write('%s %s\n' %(re, rs))
	if args.output:
		sys.stdout.close()


if __name__ == '__main__':
	main(sys.argv[1:])
