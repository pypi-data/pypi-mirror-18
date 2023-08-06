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

import sys
import os
import csv

def str_to_bool(s):
    if s.lower() == 'true':
        return True
    elif s.lower() == 'false':
        return False
    else:
        raise ValueError # evil ValueError that doesn't tell you what the wrong value

def load_list_file(infile):
	with open(infile, "r") as reader:
		result = reader.read().replace('\r\n','\n').splitlines()
	reader.close()
	return result
#end def


def apply_mapping(gene_list, mapping): #from sgs_to_csv
	if mapping == {}:
		return gene_list
	result = []
	for g in gene_list:
		if g in mapping:
			result.append(mapping[g])
		else:
			sys.stderr.write("%s has no mapped value\n" % (g))
			result.append(g)
	return result
#end def


def generate_map_gene_to_position(genes_seq):
	result = {}
	i = 0
	for g in genes_seq:
		result[g] = i
		i = i + 1
	return result
#end def


def header_to_str(header_map, sep="\t"):
	tab=list()
	tmp={}
	for key, value in header_map.items():
		tmp[value]=key
	order = tmp.keys()
	order.sort()
	for key in order:
		tab.append(tmp[key])
	return sep.join(tab)


def load_tab_file(file_name): #from sgs_pathway_selection & sgs_pathway_links
	headers = {}
	lines = []
	with open(file_name, "r") as in_file:
		rows = in_file.read().replace('\r\n','\n').replace('"',"").splitlines()
		i = 0
		for e in rows[0].split("\t"):
			headers[e]=i
			i = i + 1
		for l in rows[1:]:
			if not l.startwith("#"):
				lines.append(l.split("\t"))
	in_file.close()
	return headers, lines


def load_csv_list(csv_file): # from sgs_add_reaction_set, sgs_pathways_selection & sgs_pathways_links
	lines = []
	headers = {}
	with open(csv_file, 'rb') as in_csv:
		node_reader = csv.reader(in_csv, delimiter='\t', quotechar='#')
		i=0
		for elem in node_reader.next():
			headers[elem] = i
			i = i + 1
		for row in node_reader:
			lines.append(row)
	#end
	in_csv.close()
	return (headers,lines)
#end def


def load_map_id_to_set(file_map, keep_empty=False, sep=None, silent_warning=False): #from generate_query &&
	result = {}
	with open(file_map, "r") as in_map:
		lines = in_map.read().replace('\r\n','\n').splitlines()
		for row in lines:
			l = row.split(sep)
			#print l
			if not row.startswith("#") and (keep_empty or ((not keep_empty) and len(l) > 1)):
				if not l[0] in result:
					result[l[0]] = set()
				elif not silent_warning:
					sys.stderr.write("Warning: %s has multiple lines. Value sets will be fused\n" % (l[0]))
				value = result[l[0]]
				for v in l[1:]:
					value.add(v)
	in_map.close()
	return result

def reverse_map_id_to_set(mapping): # from generate query
	result = {}
	for key, values in mapping.items():
		for v in values:
			if v not in result:
				result[v] = set()
			result[v].add(key)
	return result

def load_map_id_to_list(file_map, keep_empty=False, sep=None, silent_warning=False): #from sgs_to_csv
	result = {}
	with open(file_map, "r") as in_map:
		lines = in_map.read().replace('\r\n','\n').splitlines()
		for row in lines:
			l = row.split(sep)
			if not row.startswith("#") and (keep_empty or ((not keep_empty) and len(l) > 1)):
				if not l[0] in result:
					result[l[0]] = list()
				elif not silent_warning:
					sys.stderr.write("Warning: %s has multiple lines. Value list will be concatenated\n" % (l[0]))
				value = result[l[0]]
				for v in l[1:]:
					value.append(v)
	in_map.close()
	return result
