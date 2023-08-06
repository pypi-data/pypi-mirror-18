#! /bin/sh

# Copyright (c) 2013-2015, Philippe Bordron <philippe.bordron@gmail.com>
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

#-------------------------------------------#
#              Usefull stuff                #
#-------------------------------------------#

TAB_EXT="tsv"
SHOGEN_EXT="txt"

#-------------------------------------------#
#                Parameters                 #
#-------------------------------------------#

# TODO: add some controls when getting the parameters
REACTION_LIST_FILE="$1"

#-------------------------------------------#
#              "Bonhomme part"              #
#-------------------------------------------#
#>&2 echo "Get the Bonhomme's choices"

#--- Get the Bonhomme's choices ---#

METABOLIC_CUTOFF=""
#METABOLIC_CUTOFF=$2
BONHOMME_FILE="$2"

BLOCK_STATE=""
while IFS= read -r LINE || [[ -n "$LINE" ]]; do
# the || [[ -n "$LINE" ]] is a trick to ensure to read the last line of the file
# when the file is not finishing by a newline char.
  #>&2 echo "$LINE"
  # remove comments from the current line
  HASH_POS=$(echo "$LINE"|awk '{print index($0,"#")-1}')
  if [ ${HASH_POS} -ge 0 ]; then
    LINE=$(echo ${LINE:0:${HASH_POS}} | sed -e 's/[[:space:]]*$//')
  fi

  if [ "${LINE}" == "OPTIONS:" ]; then
      BLOCK_STATE="OPTIONS"
      #>&2 echo "Enter $BLOCK_STATE block"
  fi

  if [ "${BLOCK_STATE}" == "OPTIONS" ]; then
      if [[ "${LINE}" =~ ^-c\ .* ]]; then
          METABOLIC_CUTOFF="$(echo ${LINE:3} | sed -e 's/^[[:space:]]*//')"
          #>&2 echo "${METABOLIC_CUTOFF}"
      fi
  fi

  if [ "${LINE}" == "QUERIES:" ]; then
      BLOCK_STATE="QUERIES"
      #>&2 echo "Enter $BLOCK_STATE block"
  fi
done < "${BONHOMME_FILE}"

# check that each mandatory parameter is OK

#echo " ${METABOLIC_CUTOFF}\n ${SGS_MAX_LENGTH}\n ${K}\n ${QUERIES_COMMAND}"

if [ -z "${METABOLIC_CUTOFF+x}" ]; then
    >&2 echo "Exit: the metabolic cutoff parameter (-c) is not set corrrectly"
    exit 1
elif [[ ! "${METABOLIC_CUTOFF}" =~ ^[0-9]+$ ]]; then
    >&2 echo "Exit: the metabolic cutoff parameter (-c) must be a positive integer"
    exit 1
fi

#-------------------------------------------#
#         "Generate reaction graph"         #
#-------------------------------------------#
>&2  echo "Generate reaction graph"

#reaction_graph_generator.py -c ${METABOLIC_CUTOFF} ${REACTION_LIST_FILE}
sgs-utils.py generate reaction_graph -c ${METABOLIC_CUTOFF} ${REACTION_LIST_FILE}
