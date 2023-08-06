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
	#print("local import")
	from utils import *
except ImportError:
	try:
		#print("local relative import")
		from .utils import *
	except ValueError:
		#print("global import")
		from sgs_utils.utils import *

def format(block_str, map_gene_to_position, mapping, length_limit, block_mode):
	# return the block under a csv like collection of line such as :
	# start_reaction end_reaction start_segment end_segment length gene_list
	# if the block is not well formated, an empty line is returned
	# each block begin with "[0-9]+ best gene units catalyzing pathway from reaction \S+ to \S+" and ends with an empty line
	block = block_str.split("\n")
	result = ""
	length = 0
	length_previous = 0
	gene_set = set()
	m = re.match("^[0-9]+ best gene units catalyzing pathway from reaction (\S+) to (\S+)", block[0])
	if (m != None):
		r_start = m.group(1)
		r_end = m.group(2)
		for i in xrange(1,len(block)):
			if length <= length_limit:
				# two cases, the current length or the gene list
				m = re.match("length: ([0-9]+)", block[i])
				if (m != None):
					length_previous = length
					length = int(m.group(1))
					if (block_mode=="rank") and (length_previous != length) and (gene_set != set()):
						sg, density = genomic_density(gene_set, map_gene_to_position)
						sg_start, sg_end = sg
						gene_set = apply_mapping(gene_set, mapping)
						result = result + ("%s\n" % ("\t".join([r_start, r_end, str(sg_start), str(sg_end), str(length), str(density), " ".join(gene_set)])))
						gene_set.clear()
				else:
					m = re.match("[0-9]+: *(.+)  $", block[i])
					if (m != None):
						gene_list = re.split(" +", m.group(1))
						#sys.stderr.write("%s\n" % (str(gene_list)))
						if (block_mode=="segment"):
							sg, density = genomic_density(gene_list, map_gene_to_position)
							sg_start, sg_end = sg
							gene_list = apply_mapping(gene_list, mapping)
							gene_list.sort()
							result += "%s\n" % ("\t".join([r_start, r_end, str(sg_start), str(sg_end), str(length), str(density), " ".join(gene_list)]))
						else:
							for g in gene_list:
								gene_set.add(g)
	#end if
	if gene_set != set():
		sg, density = genomic_density(gene_set, map_gene_to_position)
		sg_start, sg_end = sg
		gene_set = apply_mapping(gene_set, mapping)
		result = result + ("%s\n" % ("\t".join([r_start, r_end, str(sg_start), str(sg_end), str(length), str(density), " ".join(gene_set)])))
	return result
#end def

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
		Print in tabular format the SGS obtained by shogen

		exemple:
		%(prog)s gene_seq.txt < sgs.txt > sgs.tsv
		'''), prog = prog
	)

	# Requiered arguments
	#####################
	parser.add_argument("gene_seq", help="Gene sequence file to compute additonal information")

	# Optional arguments
	####################
	parser.add_argument("-o", "--output", default=None, help="set an output file")
	#parser.add_argument("-b", "--block_mode", choices=['full', 'rank', 'segment'] , default="segment", help="Depreciated: How to group SGS together")
	parser.add_argument("-l", "--length_limit", type=int, default=sys.maxint, help="Filter the length of SGS according to a limit")
	parser.add_argument("-t", "--translate", default=None, help="Translate SGS gene id with the given dictionnary", metavar="DICTIONNARY")
	parser.add_argument("-q", "--quiet", action='store_true', default=False, help="quiet mode")

	args = parser.parse_args(argv)
	#block_mode = args.block_mode
	block_mode = 'segment'


	stream_out = sys.stdout
	if args.output:
		stream_out = open(args.output, 'w')

	if not args.quiet:
		sys.stderr.write("%s mode with a limit of %d\n" % (block_mode, args.length_limit))
	mapping = {}
	if args.translate:
		mapping = load_map_id_to_list(args.translate, sep='\t')
	genome = load_gene_sequence(args.gene_seq)
	map_gene_to_position = generate_map_gene_to_position(genome)

	# load results on et standard entry
	lines = sys.stdin.readlines()

	# parse blocks of results
	# each block begin with "[0-9]+ best gene units catalyzing pathway from reaction \S+ to \S+" and ends with an empty line
	stream_out.write("%s\n" % ("\t".join(["start_reaction","end_reaction", "start_position","end_position","length","density","gene_set"])))
	block = ""
	for l in lines:
		#print l
		if l == "\n":
			#print block
			stream_out.write(format(block, map_gene_to_position, mapping, args.length_limit, block_mode)) # print the block in csv like format
			block = ""
		else:
			block += l
	#end
	if block != "": # take in the account the EOF
		stream_out.write(format(block, map_gene_to_position, mapping, args.length_limit, block_mode)) # print the block in csv like format
	#print len(lines)
	#end
	if args.output:
		stream_out.close()


if __name__ == '__main__':
	main(sys.argv[1:])
