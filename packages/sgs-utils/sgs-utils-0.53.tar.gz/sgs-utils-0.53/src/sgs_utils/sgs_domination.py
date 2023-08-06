#!/usr/bin/env python
# -*- coding: utf8 -*-
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

# Let be I a set of intervals of genes and A an interval of genes from I.
# Let be d(A) the density of A. The interval A is removed from I if it
# exists an interval B in I such as that set of genes of A is strictly
# include into the set of genes of B and d(A)<d(B). This process is
# applied for each interval in I.

import csv
import os
import sys
#from utils import *


def load(file):
	result = {}
	head = ""
	headers = {}

	with open(file, 'rb') as input_file:
		line_reader = csv.reader(input_file, delimiter='\t', quotechar='#')
		head = line_reader.next()  # get headers
		# TODO: Check headers

		for i in range(0, len(head)):
			headers[head[i]] = i
		# print headers

		chr = ""
		org = ""
		for row in line_reader:

			if "chr_id" in headers:
				chr = row[headers["chr_id"]]
				if "org_id" in headers:
					chr = row[headers["org_id"]]
			density = float(row[headers["density"]])

			s = (org, chr, frozenset(row[headers["gene_set"]].split(" ")))
			# a give set of genes alway has the same density
			if not (s in result):
				result[s] = (density, list())
			result[s][1].append(row)
	return headers, head, result
# end def


################
# Main program #
################


# load csv like files and create a map that associate a set of genes to a list of lines and the density of the set of genes.
# create a map on inclusion.
# create a set of reaction that are included into the set of genes by using the inclusion.
# the output will be a csv like file with:
# start_position end_position length density gene_set reaction_set

def main (argv, prog = os.path.basename(sys.argv[0])):
	#sys.stderr.write("%s\n" % (" ".join(sys.argv)))
	import argparse
	import textwrap
	parser = argparse.ArgumentParser(
		formatter_class=argparse.RawDescriptionHelpFormatter,
		description=textwrap.dedent('''\
		Generate the dominant SGS list from a SGS list

		exemple:
		%(prog)s sgs_list.tsv > dominant_sgs_list.tsv
		'''), prog = prog
	)

	# Requiered arguments
	#####################
	parser.add_argument("sgs_file", help="SGS list in .tsv file format")

	# Optional arguments
	####################
	parser.add_argument("-o", "--output", default=None, help="set an output file")

	args = parser.parse_args(argv)

	stream_out = sys.stdout
	if args.output:
		stream_out = open(args.output, 'w')

	to_remove = set()
	map_overset_of = {}
	headers, head, sgs_list = load(args.sgs_file)
	#sys.stderr.write(str(sgs_list) + "\n")
	gene_set_to_reaction_set = {}
	if "reaction_set" in headers:
		for fset, values in sgs_list.items():
			density, rows = values
			#sys.stderr.write(str(fset) + ":" + str(rows) + "\n")
			gene_set_to_reaction_set[fset] = set(rows[0][headers["reaction_set"]].split())


	for fset1, values1 in sgs_list.items():
		density1, rows1 = values1
		org1, chr1, gene_set1 = fset1
		for fset2, values2 in sgs_list.items():
			density2, rows2 = values2
			org2, chr2, gene_set2 = fset2
			# test if fset1 is include in fset2
			if org1 == org2 and chr1 == chr2 and gene_set1 < gene_set2 and density1 <= density2:
				to_remove.add(fset1)
				if not(fset2 in map_overset_of):
					map_overset_of[fset2] = set()
				map_overset_of[fset2].add(fset1)
			if "reaction_set" in headers and fset1 == fset2:  # if same set of gene, fuse reactions set
				s = gene_set_to_reaction_set[fset1] | gene_set_to_reaction_set[fset2]
				gene_set_to_reaction_set[fset1] = s
				gene_set_to_reaction_set[fset2] = s

	# end


	# printing results.
	remove_from_headers = []
	if "start_reaction" in headers:
		remove_from_headers.append(headers["start_reaction"])
	if "end_reaction" in headers:
		remove_from_headers.append(headers["end_reaction"])
	remove_from_headers.sort()
	remove_from_headers.reverse()
	# print headers

	for i in remove_from_headers:
		head.pop(i)

	stream_out.write("%s\n" % ("\t".join(head)))

	for fset, values in sgs_list.items():
		if not fset in to_remove:
			density, rows = values
			row = rows[0]
			if "reaction_set" in headers:
				row[headers["reaction_set"]] = " ".join(gene_set_to_reaction_set[fset])
			for i in remove_from_headers:
				row.pop(i)
			stream_out.write("%s\n" % ("\t".join(row)))
	# end
	if args.output:
		stream_out.close()


if __name__ == '__main__':
	main(sys.argv[1:])
