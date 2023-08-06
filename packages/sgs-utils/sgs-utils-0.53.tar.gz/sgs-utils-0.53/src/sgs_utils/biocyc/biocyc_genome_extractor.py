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

import sys, os

try:
	from biocyc_parser import *
except ImportError:
	from sgs_utils.biocyc.biocyc_parser import *
try:
	from biocyc_chromosome_id_extractor import get_chr
except ImportError:
	from sgs_utils.biocyc.biocyc_chromosome_id_extractor import get_chr

# in genes.dat
TRANSCRIPTION_DIRECTION = "TRANSCRIPTION-DIRECTION"
LEFT = "LEFT-END-POSITION"
RIGHT = "RIGHT-END-POSITION"
COMPONENT_OF = "COMPONENT-OF"
COMMON_NAME = "COMMON-NAME"


def generate_gene_listing(genes_map, chr_list, metacyc_new, supplementary_fields):
	result = [] # list of list starting with (chr_id, start_position, end_position,...)
	for gene_id, attributes in genes_map.items():
		try:
			chr_id = attributes[COMPONENT_OF]
			if metacyc_new:
				chr_id_corr=set()
				for c in chr_id: # here to consider duplicated chr_id (CHR_ID-XX and CHR_ID-YY) in genes.dat
					chr_id_corr.add(c.rsplit("-", 1)[0])
				chr_id = chr_id_corr
			for c in chr_id:
				if c in chr_list:
					try:
						left = int(attributes[LEFT][0])
						right = int(attributes[RIGHT][0])
						direction = attributes[TRANSCRIPTION_DIRECTION]
						line = [c, gene_id, left, right, " ".join(direction)]
						for field in supplementary_fields:
							f = ""
							if field in attributes:
								f = attributes[field]
							line.append(" ".join(f))
						#print(line)
						result.append(line)
					except KeyError:
						sys.stderr.write("Warning: %s has no left or right end position registred\n" % (gene_id))
		except KeyError:
			sys.stderr.write("Warning: %s is not attached to a chromosome\n" % (gene_id))
	return result

def compare_gene_list(a, b):
	 # we compare the first, then third and finally the fourth columns
	return cmp(a[0], b[0]) or cmp(a[2], b[2]) or cmp(a[3], b[3])

# output headers
OUTPUT_HEADER = ["chromosome_id", "gene_id", "left_end_position", "right_end_position", "transcription_direction"]

def main (argv, prog = os.path.basename(sys.argv[0])):
	import argparse
	import textwrap
	parser = argparse.ArgumentParser(
		formatter_class=argparse.RawDescriptionHelpFormatter,
		description=textwrap.dedent('''\
		Print in tabular format the gene list of an organism from its biocyc/metacyc flat files

		exemple:
		%(prog)s genes.dat species.dat > genome.tsv
		'''), prog = prog
	)

	# Requiered arguments
	#####################
	parser.add_argument("genes_file", help="Biocyc flat genes.dat file")
	parser.add_argument("species_file", help="Biocyc flat species.dat file that contains the listing of chromosome id of the genome associated to an organism")

	# Optionan arguments
	####################
	parser.add_argument("-o", "--output", default=None, help="set an output file")
	parser.add_argument("-org", "--organism", nargs='+', help="Selected organism id (all if not precised)")
	parser.add_argument("-sf", "--supplementary_fields", nargs= "+", default=[], help="Add custom supplementary fields in the tabular files")
	parser.add_argument("-sc", "--selected_chromosomes", nargs= "+", default=None, help="list of selected chromosomes id (all if not precised)")

	biocyc_version = parser.add_mutually_exclusive_group()
	biocyc_version.add_argument("-new", "--metacyc_new", action='store_true', help="Manage metacyc 18.5+ flatfiles format (default)")
	biocyc_version.add_argument("-old", "--metacyc_old", action='store_false', help="Manage metacyc 18.0- flatfiles format")

	args = parser.parse_args(argv)

	chr_list =[]
	# mapping pathway to subpathway and set of reactions
	chr_species_map = {}
	get_chr(chr_species_map, args.species_file)

	v185 = True
	if not args.metacyc_old:
		v185 = False

	stream_out = sys.stdout
	if args.output:
		stream_out = open(args.output, 'w')

	if not args.organism:
		args.organism = chr_species_map.keys()
	for organism in args.organism:
		if organism in chr_species_map:
			chr_list = chr_species_map[organism]
		else:
			sys.stderr.write("Error: no specie %s in %s\n" % (organism, args.species_file))
			sys.exit()

	if args.selected_chromosomes:
		chr_list = list(set(chr_list).intersection(args.selected_chromosomes))

	genes_map = load_flat_file(args.genes_file)
	gene_list = generate_gene_listing(genes_map, chr_list, v185, args.supplementary_fields)
	gene_list.sort(compare_gene_list)

	head = OUTPUT_HEADER + args.supplementary_fields
	stream_out.write("%s\n" % ("\t".join(head)))
	for elem in gene_list:
		line = [str(i) for i in elem]
		stream_out.write("%s\n" % ("\t".join(line)))
	if args.output:
		stream_out.close()

if __name__ == '__main__':
	main(sys.argv[1:])
