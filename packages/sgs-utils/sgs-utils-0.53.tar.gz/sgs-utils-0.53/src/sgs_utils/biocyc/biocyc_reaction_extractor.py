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

from __future__ import absolute_import

import sys
import os
try:
	from biocyc_parser import *
except ImportError:
	from sgs_utils.biocyc.biocyc_parser import *

## in reactions.dat
LEFT = "LEFT"
RIGHT = "RIGHT"
ENZYMATIC_REACTION = "ENZYMATIC-REACTION"
EC_NUMBER="EC-NUMBER"
SPONTANEOUS = "SPONTANEOUS?"
COEFFICIENT = "COEFFICIENT"
COMMON_NAME = "COMMON-NAME"

## in enzrxns.dat
REACTION = "REACTION"
ENZYME = "ENZYME"
REQUIRED_PROTEIN_COMPLEX = "REQUIRED-PROTEIN-COMPLEX"
# in both
REACTION_DIRECTION = "REACTION-DIRECTION"

## in proteins.dat
CATALYZES = "CATALYZES"
COMPONENTS = "COMPONENTS" # when protein complex
COMPONENT_OF = "COMPONENT-OF" # composing protein complex
GENE = "GENE"
UNMODIFIED_FORM = "UNMODIFIED-FORM" # initial form of the protein

def complete_map(map_, key, values):
	try:
		map_[key].update(values)
	except KeyError:
		map_[key] = set(values)
	#end

def deep_search(map_proteins, prots):
	result = set()
	file_ = list(prots)
	while file_:
		p = file_.pop(0)
		if p in map_proteins:
			result.add(p)
			for c in map_proteins[p][0]:
				if c not in file_:
					file_.append(c)
	return result

def coef_list(compound_list, coef_map):
	results = []
	for c in compound_list:
		results.append(coef_map[c])
	return results

def main (argv, prog = os.path.basename(sys.argv[0])):
	#sys.stderr.write("%s\n" % (" ".join(sys.argv)))
	import argparse
	import textwrap
	parser = argparse.ArgumentParser(
		formatter_class=argparse.RawDescriptionHelpFormatter,
		description=textwrap.dedent('''\
		Generate the reaction list from Biocyc flat files

		exemple:
		%(prog)s reactions.dat -enz enzrxns.dat proteins.dat -o reaction_list.tsv
		'''), prog = prog
	)

	# Requiered arguments
	#####################
	parser.add_argument("reaction_file", help="reaction file in Biocyc flat format")

	# Optional arguments
	####################
	parser.add_argument("-o", "--output", default=None, help="set an output file")
	parser.add_argument("-enz", "--enzymatic_reactions", nargs=2, metavar=('ENZRXNS','PROTEINS'), help="enzymatic file and protein file in Biocyc flat format")
	parser.add_argument("-rds", "--reaction_direction_strategy", choices=['consensus', 'enzyme', 'reaction'], default='consensus', help="Specify the stategy when an enzyme catalyzes a reaction in another direction than the reaction direction (default: %(default)s). The 'consensus' choice consists in keeping the less restrictive direction (i.e. reversible) when a conflit exists. The 'enzyme' choice consists in thrusting enzymes more than reactions. When a conflit exists between two enzymes, the less restrictive direction is choosen. If an enzyme does not precise the direction, then the reaction direction will be used as direction for this enzyme. The 'reaction' choice consists in only considering the reaction's direction without thrusting enzyme's direction.")
	parser.add_argument("-sc", "--stoichiometric_coef", default=False, action='store_true', help="add two columns for stochiometric coef for left and right parts") # will duplicate all the arcs


	args = parser.parse_args(argv)

	stream_out = sys.stdout
	if args.output:
		stream_out = open(args.output, 'w')

	reactions_flat_map = load_flat_file(args.reaction_file, args.stoichiometric_coef)
	enzrxns_flat_map = {}
	proteins_flat_map = {}
	if (args.enzymatic_reactions):
		enzrxns_flat_map = load_flat_file(args.enzymatic_reactions[0])
		proteins_flat_map = load_flat_file(args.enzymatic_reactions[1])

	map_reactions = {}
	map_proteins = {}
	map_enzrxns = {}
	map_reactant_coefs = {}
	map_product_coefs = {}

	if (args.enzymatic_reactions):
		sys.stderr.write("Protein part\n")
	# create map of prot_id associated with genes and part of it when a complex
	for prot_id, p_data in proteins_flat_map.items():
		cpds = []
		genes = []
		if COMPONENTS in p_data:
			cpds = p_data[COMPONENTS]
		if GENE in p_data:
			genes = p_data[GENE]
		map_proteins[prot_id] = tuple((cpds, genes))

	# create map that associate enzymatic reaction to its catalytic proteins (with formula?)
	if (args.enzymatic_reactions):
		sys.stderr.write("Enzymatic reactions part\n")
	for enzrxn_id, e_data in enzrxns_flat_map.items():
		enz = []
		req = []
		if REACTION in e_data:
			rlist = e_data[REACTION]
			#if len(rlist) > 1:
			#	sys.stderr.write("Info: %s is associated to more than one reaction id: \n\t%s\n" % (enzrxn_id, "\n\t".join(sorted(rlist))))
		#	complete_map(map_rxn_to_enz, rlist[0], [enzrxn_id])
		else:
			sys.stderr.write("Info: %s has no reaction id\n" % (enzrxn_id))
		if ENZYME in e_data:
			enz = e_data[ENZYME]
		if REQUIRED_PROTEIN_COMPLEX in e_data:
			req = e_data[ENZYME]
		direction = None
		if REACTION_DIRECTION in e_data:
			if e_data[REACTION_DIRECTION][0] in ["LEFT-TO-RIGHT", "PHYSIOL-LEFT-TO-RIGHT", "IRREVERSIBLE-LEFT-TO-RIGHT"]:
				direction = 1
			if e_data[REACTION_DIRECTION][0] in ["RIGHT-TO-LEFT", "PHYSIOL-RIGHT-TO-LEFT", "IRREVERSIBLE-RIGHT-TO-LEFT"]:
				direction = -1
			if e_data[REACTION_DIRECTION][0] == "REVERSIBLE":
				direction = 0
		map_enzrxns[enzrxn_id] = tuple((rlist, direction, enz, req))

	sys.stderr.write("Reactions part with %s strategy\n" % (args.reaction_direction_strategy))
	# associate to react_id ...
	for react_id, r_data in reactions_flat_map.items():
		left = []
		right = []
		enzrxn = []
		ec_numbers = []
		name = ''
		map_product_coefs[react_id] = {}
		map_reactant_coefs[react_id] = {}
		given_direction = 0
		corrected_direction = 0
		spontaneous = False
		if LEFT in r_data:
			left = r_data[LEFT]
		else:
			sys.stderr.write("Warning: %s has no left part.\n" % (react_id))
		if RIGHT in r_data:
			right = r_data[RIGHT]
		else:
			sys.stderr.write("Warning: %s has no right part.\n" % (react_id))
		if ENZYMATIC_REACTION in r_data:
			enzrxn = r_data[ENZYMATIC_REACTION]
		if EC_NUMBER in r_data:
			ec_numbers = r_data[EC_NUMBER]
		if COMMON_NAME in r_data:
			name = r_data[COMMON_NAME][0]
		reactants = left
		products = right
		if REACTION_DIRECTION in r_data:
			if r_data[REACTION_DIRECTION][0] in ["LEFT-TO-RIGHT", "PHYSIOL-LEFT-TO-RIGHT", "IRREVERSIBLE-LEFT-TO-RIGHT"]:
				given_direction = 1
				corrected_direction = 1
			if r_data[REACTION_DIRECTION][0] in ["RIGHT-TO-LEFT", "PHYSIOL-RIGHT-TO-LEFT", "IRREVERSIBLE-RIGHT-TO-LEFT"]:
				given_direction = -1
				corrected_direction = 1
				reactants = right
				products = left
		for c in reactants:
			coef = '1'
			if not isinstance(c, basestring): # stochiometric coef
				if COEFFICIENT in c[1]:
					coef = c[1][COEFFICIENT]
				c = c[0]
			map_reactant_coefs[react_id][c] = coef
		for c in products:
			coef = '1'
			if not isinstance(c, basestring): # stochiometric coef
				if COEFFICIENT in c[1]:
					coef = c[1][COEFFICIENT]
				c = c[0]
			map_product_coefs[react_id][c] = coef
		reactants=remove_additional_info(reactants)
		products=remove_additional_info(products)
		if SPONTANEOUS in r_data:
			spontaneous = r_data[SPONTANEOUS][0] == 'T'
		#check direction with enzrxn and get the genes
		#look orientations and reverse left and right if needed

		ec_number = []
		gene_association = set()
		current_enzymatic_direction = given_direction # reaction strategy
		if args.reaction_direction_strategy != 'reaction':
			current_enzymatic_direction = None
		for erxn in enzrxn:
			if erxn in map_enzrxns:
				renz = map_enzrxns[erxn]
				enz_dir = renz[1]
				if enz_dir == None:
					enz_dir = given_direction
					#sys.stderr.write("Info: %s do not precise the reaction %s direction (%d). The %s direction will be used (%d).\n" % (erxn, react_id, given_direction, react_id, given_direction))
				## reactions direction management here
				## keep in mind that enz_dir and way given_direction are written according to the flatfile description whereas corrected_direction depends of the left to right normalization.
				## consensus rules
				if args.reaction_direction_strategy == 'consensus':
					if enz_dir != given_direction:
						current_enzymatic_direction = 0
						if enz_dir * given_direction < 0:
							sys.stderr.write("Info: %s (%d) inverses the direction of %s (%d). The %s direction is now reversible (%d)\n" % (erxn, enz_dir, react_id, given_direction, react_id, current_enzymatic_direction))
						# we "inverse" the reactants and products for consitency if needeed
						elif given_direction == 0:
							sys.stderr.write("Info: %s (%d) specializes the direction of the reaction %s (%d). The reaction %s is keept reversible (%d)\n" % (erxn, enz_dir, react_id, given_direction, react_id,current_enzymatic_direction))
						else:
							sys.stderr.write("Info: %s (%d) reverses the direction of the reaction %s (%d). The reaction %s becomes reversible (%d).\n" % (erxn, enz_dir, react_id, given_direction, react_id,current_enzymatic_direction))
				## enzyme rules
				if args.reaction_direction_strategy == 'enzyme':
					if current_enzymatic_direction:
						if current_enzymatic_direction == 0 and enz_dir != 0:
							sys.stderr.write("Info: %s (%d) specializes the direction of %s (%d), but reaction %s will be reversible (%d)\n" % (erxn, enz_dir, react_id, given_direction, react_id, current_enzymatic_direction))
						elif enz_dir != current_enzymatic_direction:
							if enz_dir * current_enzymatic_direction < 0:
								sys.stderr.write("Info: %s (%d) inverses the direction of %s (%d). The reaction %s become reversible (%d).\n" % (erxn, enz_dir, react_id, current_enzymatic_direction, react_id, 0))
							else:
								sys.stderr.write("Info: %s (%d) reverses the current reaction %s (%d). The reaction %s become reversible (%d).\n" % (erxn, enz_dir, react_id, current_enzymatic_direction, react_id, 0))
							current_enzymatic_direction = 0
						# the current enzymatic reaction reverse a previous enzymatic reaction
						else:
							# same direction, nothing to do
							pass
					else:
						current_enzymatic_direction = enz_dir
						if enz_dir != given_direction:
							sys.stderr.write("Info: %s (%d) specializes the direction of %s (%d). The reaction %s become irreversible (%d)\n" % (erxn, enz_dir, react_id, given_direction, react_id, current_enzymatic_direction))
				prots = renz[2]
				prots = deep_search(map_proteins, prots)
				for p in prots:
					for g in map_proteins[p][1]:
						gene_association.add(g)

		if given_direction < 0 and current_enzymatic_direction >= 0:
			# permute back left and right parts because of enzyme directions
			reactants, products = products, reactants
			map_reactant_coefs[react_id], map_product_coefs[react_id] = map_product_coefs[react_id], map_reactant_coefs[react_id]

		if corrected_direction:
			corrected_direction = current_enzymatic_direction
		map_reactions[react_id] = tuple((react_id, name, sorted(reactants), sorted(products), corrected_direction == 0, gene_association, ec_numbers, spontaneous))

	# Export the reaction list file
	header = ['reaction_id', 'name', 'reactants', 'products', 'reversible', 'association', 'ec_number', 'spontaneous']
	if args.stoichiometric_coef:
		header.append('reactant_coefs')
		header.append('product_coefs')
	stream_out.write('%s\n' % ('\t'.join(header)))
	list_reactions = map_reactions.keys()
	list_reactions.sort()
	for r in list_reactions:
		#print r
		react_id, name, reactants, products, rev, gene_association, ec_number, spontaneous = map_reactions[r]
		ec_number = remove_additional_info(ec_number)
		line = [react_id,\
			name,
			 " ".join(reactants),\
			 " ".join(products),\
			 str(rev),\
			 " ".join(gene_association),\
			 " ".join(ec_number),\
			 str(spontaneous)]
		if args.stoichiometric_coef:
			line.append(" ".join(coef_list(reactants, map_reactant_coefs[react_id])))
			line.append(" ".join(coef_list(products, map_product_coefs[react_id])))
		stream_out.write('%s\n' % ("\t".join(line)))
	if args.output:
		stream_out.close()
#end

if __name__ == '__main__':
	main(sys.argv[1:])
