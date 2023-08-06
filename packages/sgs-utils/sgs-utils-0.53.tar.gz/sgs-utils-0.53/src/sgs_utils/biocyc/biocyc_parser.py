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
import re

LINE_COMMENT = "#"
BLOCK_SEPARATOR = "\n//\n"
UNIQUE_ID = "UNIQUE-ID"
FIELD_SEP = " - "
LINE_BREAK = "/"
ADDITIONAL_INFO = "^"
# return the contents of a flat file into an map
# map[unique_id] -> map[attributes] -> list of values
def load_flat_file(flat_file, complementary_attributes=False):
	flat_map = {}
	with open(flat_file, "r") as reader:
		blocks = reader.read().replace('\r\n','\n').split(BLOCK_SEPARATOR)
		for b in blocks:
			unique_id, attributes = parse_block(b, complementary_attributes)
			if unique_id:
				flat_map[unique_id] = attributes
			else:
				if b != "":
					sys.stderr.write("Warning, bad structured block:\n%s\n" % (b))
	return flat_map

def remove_additional_info(value_list):
	result = []
	for v in value_list:
		if isinstance(v, basestring):
			result.append(v)
		else:
			result.append(v[0])
	return result


# take the string corresponding to a block and return an id and a map such as
# id = UNIQUE_ID
# map[attributes] -> list of strings
# when complementary_attributes is set to True, Attributes that start with an ^ like ^COMPARTMENT are taken into account is the data structure. The new map is then:
# map[attributes] -> list of (strings | tuple(string, map[attributes, string]))
def parse_block(block, complementary_attributes):
	attribute_map = {}
	unique_id = ""
	last_attribute = ""
	for l in block.splitlines():
		if l and not l.startswith(LINE_COMMENT):
			if l.startswith(LINE_BREAK):
				attribute = attribute_map[last_attribute]
				attribute[-1]= attribute[-1] + "\n" + l
			elif l.startswith(ADDITIONAL_INFO):
				if complementary_attributes:
					# transform previous entry by adding complementary information
					attribute = attribute_map[last_attribute]
					av = l.lstrip(ADDITIONAL_INFO).split(FIELD_SEP)
					#av = l.split(FIELD_SEP)
					# test if map of list
					if isinstance(attribute[-1], basestring):
						attribute[-1] = (attribute[-1], {})
					attribute[-1][1][av[0]] = av[1]
			else:
				av = l.split(FIELD_SEP)
				if av[0] == UNIQUE_ID:
					unique_id = av[1]
				else:
					if len(av) > 1:
						last_attribute = av[0]
						if last_attribute in attribute_map:
							attribute_map[last_attribute].append(FIELD_SEP.join(av[1:]))
						else:
							attribute_map[last_attribute] = [FIELD_SEP.join(av[1:])]
					else:
						# file malformed with missing LINE_BREAK (e.g. pathway.dat with |CITS:[ColiSalII]|)
						attribute = attribute_map[last_attribute]
						sys.stderr.write("Warning: Malformed bloc %s for %s attribute: missing breakline\n" % (unique_id, last_attribute))
						attribute[-1]= attribute[-1] + "\n" + l
	return unique_id, attribute_map

################
# Main program #
################

def main (argv, prog = os.path.basename(sys.argv[0])):
	import argparse

	parser = argparse.ArgumentParser(prog = prog)

	# Requiered arguments
	#####################
	parser.add_argument("flatfile", help="Biocyc .dat flatfile")

	args = parser.parse_args(argv)
	for k,v in load_flat_file( args.flatfile, True).iteritems():
		print k, v


if __name__ == '__main__':
	main(sys.argv[1:])
