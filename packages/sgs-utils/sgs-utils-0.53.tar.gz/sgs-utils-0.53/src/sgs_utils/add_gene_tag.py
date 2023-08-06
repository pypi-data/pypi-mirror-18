#!/usr/bin/env python
# -*- coding: utf8 -*-
# Copyright (c) 2013-2014, Philippe Bordron <philippe.bordron@gmail.com>
#
# This file is part of sgs-utils.
#
# sgs-utils is free software: you can redistribute it and/or modify
# it under the terms of the GNU LESSER GENERAL PUBLIC LICENSE as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# sgs-utils is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU LESSER GENERAL PUBLIC LICENSE for more details.
#
# You should have received a copy of the GNU LESSER GENERAL PUBLIC LICENSE
# along with sgs-utils.  If not, see <http://www.gnu.org/licenses/>

import sys
import os
import re
try:
	import utils
except ImportError:
	import sgs_utils.utils as utils


################
# Main program #
################

# load genome to have genes position
def main (argv, prog = os.path.basename(sys.argv[0])):
	import argparse
	import textwrap
	parser = argparse.ArgumentParser(
		formatter_class=argparse.RawDescriptionHelpFormatter,
		description=textwrap.dedent('''\
		Change the list of active genes in a SGS into a list of 'active','non active' and 'non catalytic' genes in the SGS with tags

		exemple:
		python %(prog)s sgs_list.tsv gene_seq.txt [-na catalyze.txt]> sgs_list_with_gene_tag.tsv
		'''), prog = prog
	)

	# Requiered arguments
	#####################
	parser.add_argument("sgs_file", help="SGS list file")
	parser.add_argument("gene_seq", help="Gene sequence file to compute additonal information")

	# Optional arguments
	####################
	parser.add_argument("-o", "--output", default=None, help="set an output file")
	parser.add_argument("-na", "--non_active", default=None, help="differenciate non-active from non-catalytic reaction list")

	args = parser.parse_args(argv)

	stream_out = sys.stdout
	if args.output:
		stream_out = open(args.output, 'w')

	genome = utils.load_gene_sequence(args.gene_seq)
	#map_gene_to_position = generate_map_gene_to_position(genome)
	sgs_header, sgs_list = utils.load_csv_list(args.sgs_file)
	map_catalytic = {}
	if args.non_active:
		map_catalytic = utils.reverse_map_id_to_set(utils.load_map_id_to_set(args.non_active, silent_warning=True))

	# add tag to genes
	stream_out.write("{}\n".format(utils.header_to_str(sgs_header)))
	for l in sgs_list:
		gene_set = l[sgs_header["gene_set"]].split()
		start = int(l[sgs_header["start_position"]])
		end =  int(l[sgs_header["end_position"]])
		new_gene_list=[]
		if start <= end:
			for i in range(start, end+1):
				g = genome[i]
				if g in gene_set:
					new_gene_list.append("ac:" + g)
				elif g in map_catalytic:
					new_gene_list.append("na:" + g)
				else:
					new_gene_list.append("nc:" + g)
		else:
			for i in range(end, len(genome)):
				g = genome[i]
				if g in gene_set:
					new_gene_list.append("ac:" + g)
				elif g in map_catalytic:
					new_gene_list.append("na:" + g)
				else:
					new_gene_list.append("nc:" + g)
			for i in range(0, start+1):
				g = genome[i]
				if g in gene_set:
					new_gene_list.append("ac:" + g)
				elif g in map_catalytic:
					new_gene_list.append("na:" + g)
				else:
					new_gene_list.append("nc:" + g)
		l[sgs_header["gene_set"]] = " ".join(new_gene_list)
		stream_out.write("{}\n".format("\t".join(l)))
	#end

	if args.output:
		stream_out.close()


if __name__ == '__main__':
	main(sys.argv[1:])
