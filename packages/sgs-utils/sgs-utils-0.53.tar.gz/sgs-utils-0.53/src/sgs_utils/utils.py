# -*- coding: utf8 -*-
# Copyright (c) 2013, Philippe Bordron <philippe.bordron@gmail.com>
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
import csv

def load_gene_sequence(genome_file):
	with open(genome_file, "r") as in_gene_seq:
		genes_seq = in_gene_seq.read().replace('\r\n','\n').splitlines()
	in_gene_seq.close()
	return genes_seq
#end def


#compute the genomic density of a set of elements (genes) on the genome.
def genomic_density(genes, map_gene_to_position):
	#print "genomic density of %s" % (genes)
	positions = list()
	for g in genes:
		positions.append(map_gene_to_position[g])
	positions.sort()
	# compute de maximum interval that contains none of the given genes
	interval = (0,0) # complementary of the maximum interval
	max_size = -2 # -2 because we won't take in account the extremities of the maximum interval
	size = -2
	for i in xrange(0, len(positions)):
		deb = positions[i]
		fin = positions[(i+1)%len(positions)]
		#print "testing interval ]%d..%d[ " % (deb,fin)
		if fin < deb:
			size = len(map_gene_to_position)-(deb - fin + 1) # size when the begin is before the end in the list of gene describing the circular genome.
		else:
			size = (fin - deb - 1) # normal case
		#print size
		if size > max_size: # keep the longest interval
			max_size = size
			interval = (fin,deb) # it is the complementary interval
	#print "the complementary induced interval of %s : ]%d..%d[ has a size of %d" % (genes, interval[0], interval[1], max_size)
	#print "the induced interval of %s : %s has a size of %d" % (genes, interval, len(genome)-max_size)

	# the complement of the maximum interval is the smaller interval that contains all the given genes
	# so it is easy to compute the density.
	if max_size < 0:
		max_size = len(map_gene_to_position)+ max_size
	return (interval, len(genes)/float(len(map_gene_to_position)-max_size))
#end def

def apply_mapping(gene_list, mapping):
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

def load_map_id_to_set(file_map, keep_empty=False, sep=None, silent_warning=False):
	result = {}
	with open(file_map, "r") as in_map:
		lines = in_map.read().replace('\r\n','\n').splitlines()
		for row in lines:
			l = row.split(sep)
			#print l
			if keep_empty or ((not keep_empty) and len(l) > 1):
				if not l[0] in result:
					result[l[0]] = set()
				elif not silent_warning:
					sys.stderr.write("Warning: %s has multiple lines. Value sets will be fused\n" % (l[0]))
				value = result[l[0]]
				for v in l[1:]:
					value.add(v)
	in_map.close()
	return result

def reverse_map_id_to_set(mapping):
	result = {}
	for key, values in mapping.items():
		for v in values:
			if v not in result:
				result[v] = set()
			result[v].add(key)
	return result

def load_map_id_to_list(file_map, keep_empty=False, sep=None, silent_warning=False):
	result = {}
	with open(file_map, "r") as in_map:
		lines = in_map.read().replace('\r\n','\n').splitlines()
		for row in lines:
			l = row.split(sep)
			if keep_empty or ((not keep_empty) and len(l) > 1):
				if not l[0] in result:
					result[l[0]] = list()
				elif not silent_warning:
					sys.stderr.write("Warning: %s has multiple lines. Value list will be concatenated\n" % (l[0]))
				value = result[l[0]]
				for v in l[1:]:
					value.append(v)
	in_map.close()
	return result


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
