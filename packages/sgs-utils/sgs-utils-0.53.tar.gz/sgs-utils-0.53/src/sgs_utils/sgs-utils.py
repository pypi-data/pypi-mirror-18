#!/usr/bin/env python
# -*- coding: utf8 -*-
# Copyright (c) 2016, Philippe Bordron <philippe.bordron@gmail.com>
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

# sgs-utils.py is a wrapper that maps all the programs from sgs_utils to one
# program. The parameters will be passed from sgs_utils to the asked program.
#
# The syntaxe is simple:
# sgs-utils program_name parameters

import sys
import os
import importlib

# Mandatory for making the imports work with this wapper as an installable script in the PATH
# It is mandatory to have a distinct name between the wrapper script and the package name !!!
# else there will be ImportError exceptions when loading (sub-)modules when installed
PKG_NAME="sgs_utils"
DISP_HIDDEN="hidden"

# (action, what/to, from/where/type, ...): (hidden, module_name)
# Alway end with a comma else 'singleton tuple' will be considered as string
CMD_DICT = {
    ("extract", "chromosome", "biocyc", ): (True, "biocyc.biocyc_chromosome_id_extractor"),
    ("extract", "genome", "biocyc", ): (False, "biocyc.biocyc_genome_extractor"),
    ("extract", "reaction", "biocyc", ): (False, "biocyc.biocyc_reaction_extractor"),
    ("extract", "genome", "gbk", ): (False, "gbk.gbk_genome_extractor"),
    ("extract", "reaction", "sbml", ): (False, "sbml.sbml_reaction_extractor"),
    ("generate", "reaction_graph", ): (False, "reaction_graph_generator"),
    ("add", "non-catalityc-links", "reaction_graph", ): (False, "add_non_catalytic_links"),
    ("generate", "queries", ): (False, "shogen_queries"),
    ("add", "gene_name", "sgs", ): (False, "add_gene_name"),
    ("add", "gene_tag", "sgs", ): (True, "add_gene_tag"), #old version of add_gene_name
    ("add", "reaction_set", "sgs", ): (False, "sgs_add_reaction_sets"),
    ("compute", "domination", ): (False, "sgs_domination"),
    ("correct", "gene_mapping", "genbank", ): (True, "correct_gene_mapping"), #specific tools not usefull for standard case
    ("convert", "sgs", "shogen", ): (True, "shogen2tab")
}

###################
class cmdtreenode:

    def __init__(self, action = None, next = None):
        self.action = action
        if next is None:
            self.next={}
        else:
            self.next = next
        self.__repr__ = self.__str__

    def __str__(self):
        return "({} - {})".format(str(self.action), str(self.next))

######################

def cmd_tree(cmd_dict):
    # Tree of cmd with for each node the action and the next nodes
    root = cmdtreenode()
    for key, value in cmd_dict.items():
        node = root
        for elem in key:
            try:
                node = node.next[elem]
            except KeyError:
                node.next[elem] = cmdtreenode()
                node = node.next[elem]
        node.action = value
    return root

def list_cmd_rec(node, disp_hidden = False):
    result = []
    if node.action and (not(node.action[0]) or disp_hidden):
        result.append([])
    for k, n in node.next.items():
        for cmd in list_cmd_rec(n, disp_hidden):
            cmd.append(k)
            result.append(cmd)
    return result


def list_cmd(node, disp_hidden = False):
    return [" ".join(reversed(s)) for s in list_cmd_rec(node, disp_hidden)]


def load_module(name, pkg_name=PKG_NAME):
    try: # for dev purpose
        #print("try to load local module '{}'".format(name))
        return importlib.import_module(name)
    except ImportError:  # for install purpose
        #print("try to load global module '{}'".format(".".join([pkg_name, name])))
        return importlib.import_module(".".join([pkg_name, name]))


def main(argv):
    parameters = cmd_tree(CMD_DICT)

    parameter_index = 1
    sys.argv[0] = os.path.basename(sys.argv[0])
    if len(sys.argv) <= parameter_index:
        sys.stderr.write('\nMissing arguments.\n\nPossible commands are:\n{}\n'.format(
        "\n".join([sys.argv[0] + " " + x for x in list_cmd(parameters)])
        ))
        sys.stderr.write('\nMore info about each command if using the command with the -h parameter\n\n')
    else:
        father = parameters
        node = father
        while len(sys.argv) > parameter_index:
            #print(sys.argv[parameter_index])
            if sys.argv[parameter_index] in node.next: # we go down in the param tree
                father = node
                node = node.next[sys.argv[parameter_index]]
                parameter_index = parameter_index + 1
            elif node.action:  # we cannot more go down in the tree; we check if it is the right function
                prog = load_module(node.action[1])
                prog.main(sys.argv[parameter_index:], ' '.join(sys.argv[0:parameter_index]))
                break;
            else:
                if " ".join(sys.argv[1:]) == DISP_HIDDEN:
                    sys.stderr.write('\nPossible commands are (including hidden ones):\n{}\n'.format(
                    "\n".join([sys.argv[0] + " " + x for x in list_cmd(parameters, disp_hidden=True)])
                    ))
                    sys.stderr.write('\nMore info about each command if using the command with the -h parameter\n\n')
                else:
                    sys.stderr.write('\nThe parameter {} is unknown\nPossible related commands are:\n\n{}\n'.format(
                    " ".join(sys.argv[:parameter_index+1]),
                    "\n".join([' '.join(sys.argv[:parameter_index]) + " " + x for x in list_cmd(father)])
                    ))
                    sys.stderr.write('\nMore info about each command if using the command with the -h parameter\n\n')
                break;
        else:
            if node.action:  # we cannot more go down in the tree; we check if it is the right function
                prog = load_module(node.action[1])
                prog.main(sys.argv[parameter_index:], ' '.join(sys.argv[0:parameter_index]))
            else:
                sys.stderr.write('\nMissing arguments.\n\nPossible commands are:\n{}\n'.format(
                "\n".join([sys.argv[0] + " " + x for x in list_cmd(parameters)])
                ))
                sys.stderr.write('\nMore info about each command if using the command with the -h parameter\n\n')

if __name__ == '__main__':
    main(sys.argv)
