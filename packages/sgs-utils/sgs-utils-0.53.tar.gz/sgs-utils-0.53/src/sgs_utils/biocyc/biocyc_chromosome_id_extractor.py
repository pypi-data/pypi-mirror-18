#!/usr/bin/env python
# Copyright (c) 2015, Philippe Bordron <philippe.bordron@gmail.com>
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

# in species.dat
CHROMOSOME = "GENOME"

OUTPUT_HEADER = ["org_id", "chromosome_id_list"]

def get_chr(chr_species_map, species_file):
	species_map = load_flat_file(species_file)
	for organism in species_map:
		chr_list = []
		s = species_map[organism]
		if CHROMOSOME in s:
			chr_list = s[CHROMOSOME]
		else:
			sys.stderr.write("Warning: no chromosome in %s\n" % (organism))
		chr_species_map[organism] = chr_list


def main (argv, prog = os.path.basename(sys.argv[0])):
	import argparse
	import textwrap
	parser = argparse.ArgumentParser(
		formatter_class=argparse.RawDescriptionHelpFormatter,
		description=textwrap.dedent('''\
		Print in tabular format the chromosome list of an organism from its biocyc/metacyc flat files

		exemple:
		%(prog)s species.dat > chromosome_list.txt
		'''), prog = prog
	)

	# Requiered arguments
	#####################
	parser.add_argument("specie_files", nargs= "+", help="Biocyc flat species.dat file that contains the listing of chromosome id of the genome associated to an organism")

	# Optional arguments
	####################
	parser.add_argument("-o", "--output", default=None, help="set an output file")
	parser.add_argument("-s", "--simple_output", default=False,  action='store_true', help="Just display the list itself")

	args = parser.parse_args(argv)

	stream_out = sys.stdout
	if args.output:
		stream_out = open(args.output, 'w')

	if not args.simple_output:
		stream_out.write("%s\n" % ("\t".join(OUTPUT_HEADER)))
	# mapping chr to each chromosome
	chr_species_map = {}
	for species_file in args.specie_files:
		get_chr(chr_species_map, species_file) # fill the chr_species_map
	for organism, chr_list in chr_species_map.items():
		if args.simple_output:
			stream_out.write("%s\n" % (" ".join(chr_list)))
		else:
			stream_out.write("%s\t%s\n" % (organism, " ".join(chr_list)))
	if args.output:
		stream_out.close()


if __name__ == '__main__':
	main(sys.argv[1:])
