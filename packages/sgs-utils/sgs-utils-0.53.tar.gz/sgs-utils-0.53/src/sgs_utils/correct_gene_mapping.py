#!/usr/bin/env python
# Copyright (c) 2016, Philippe Bordron <philippe.bordron@gmail.com>
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

def main (argv, prog = os.path.basename(sys.argv[0])):
	import argparse
	import textwrap
	parser = argparse.ArgumentParser(
		formatter_class=argparse.RawDescriptionHelpFormatter,
		description=textwrap.dedent('''\
		Translate a the association column with genes id from the genome with the helps of a translation dictonary

		exemple:
		%(prog)s reaction_list_file dict_file > corrected_reaction_list_file
		'''), prog = prog
	)

	# Requiered arguments
	#####################
	parser.add_argument("reaction_list_file", help="List of reaction (.tsv file)")
	parser.add_argument("translation_file", help="Translation dictionary")

	# Optional arguments
	####################
	parser.add_argument("-o", "--output", default=None, help="set an output file")

	filedp = parser.add_mutually_exclusive_group()
	filedp.add_argument("-r", "--replace", action='store_true', help="For each id in assocation field, replace it with by its translations")
	filedp.add_argument("-a", "--add", action='store_true', help="For each assocation id, add its translations in the assocation field (Default)")

	args = parser.parse_args(argv)

	stream_out = sys.stdout
	if args.output:
		stream_out = open(args.output, 'w')

	replace = False
	if args.replace:
		replace = True

	header, reaction_list = tabfiles.load_csv_list(args.reaction_list_file)
	dictionary = tabfiles.load_map_id_to_set(args.translation_file, silent_warning=True)
	stream_out.write("{}\n".format("\t".join([x for x,_ in sorted(header.items(), key=lambda (k, v): v)])))
	for line in reaction_list:
		asso_set = set(line[header["association"]].split(" "))
		trans_set = set()
		for asso in asso_set:
			if asso in dictionary:
				trans_set.update(dictionary[asso])
			if not replace:
				trans_set.add(asso)
		line[header["association"]] = " ".join(sorted(list(trans_set)))
		stream_out.write("{}\n".format("\t".join(line)))
	if args.output:
		stream_out.close()
#end


if __name__ == '__main__':
	main(sys.argv[1:])
