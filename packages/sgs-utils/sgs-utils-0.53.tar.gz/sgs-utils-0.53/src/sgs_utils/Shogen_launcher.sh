#! /bin/sh

# Copyright (c) 2013-2015, Philippe Bordron <philippe.bordron@gmail.com>
#
# This file is part of SHOGEN.
#
# SHOGEN is free software: you can redistribute it and/or modify
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
# along with SHOGEN.  If not, see <http://www.gnu.org/licenses/>


#-------------------------------------------#
#              Usefull stuff                #
#-------------------------------------------#

TAB_EXT="tsv"
SHOGEN_EXT="txt"

# trick to have a tabulation char that works everywhere
TAB=$(echo a | tr a '\t')

#-------------------------------------------#
#                 Awk scripts               #
#         - TO PUT IN EXTERNAL FILES -      #
#-------------------------------------------#

# TODO: TO PUT IN EXTERNAL FILES

GET_COL_AWK='BEGIN{FS="\t"; col=-1}
        NR == 1 {
                for (i=1; i<=NF; i++)
                {
                        if ($i==column_id){col=i};
                }
        }
        NR > 1 && col > 0 {print $col}
END{}'

SELECT_CHR_AWK='BEGIN{FS="\t"; d=-1}
        NR == 1 {
                for (i=1; i<=NF; i++)
                {
                        if ($i==chr_column_id){chr=i};
                        if ($i==gene_column_id){g=i};
                }
        }
        NR > 1 && $chr==selected_id {print $g}
END{}'


#-------------------------------------------#
#                Parameters                 #
#-------------------------------------------#

# TODO: add some controls when getting the parameters
GENOME_FILE="$1"
REACTION_GRAPH_FILE="$2"
CATALYZE_FILE="$3"
BONHOMME_FILE="$4"
QUERIES_FILE="$5"
RESULT_DIR="$6"

#---               Get the list of chromosomes id               ---#
#--- Mandatory to generate the list of queries in Bonhomme part ---#

#CHR_LIST="$(tail +2 ${GENOME_FILE} | cut -f1,1 | sort -u)"
CHR_LIST=$(eval "awk -v column_id='chromosome_id' '$GET_COL_AWK' ${GENOME_FILE}" | sort -u)
#echo "${CHR_LIST}"


#-------------------------------------------#
#              "Bonhomme part"              #
#-------------------------------------------#
#>&2 echo "Get the Bonhomme's choices"

#--- Get the Bonhomme's choices ---#

#DENSITY_LIMIT="0.6"
#FILTER_LENGTH="25"
#K="200"
#DENSITY_LIMIT="0.6"

# Bonhomme's part

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

  if [ "${BLOCK_STATE}" == "QUERIES" ]; then
      echo "$LINE" >> "${QUERIES_FILE}"
  elif [ "${BLOCK_STATE}" == "OPTIONS" ]; then
      if [[ "${LINE}" =~ ^-l\ .* ]]; then
          SGS_MAX_LENGTH="$(echo ${LINE:3} | sed -e 's/^[[:space:]]*//')"
          #>&2 echo "${SGS_MAX_LENGTH}"
      elif [[ "${LINE}" =~ ^-k\ .* ]]; then
          K="$(echo ${LINE:3} | sed -e 's/^[[:space:]]*//')"
          #>&2 echo "${K}"
      # elif [[ "${LINE}" =~ ^-q\ .* ]]; then
      #     QUERIES_COMMAND="$(echo ${LINE:3} | sed -e 's/^[[:space:]]*//')"
      #     #>&2 echo "${LINE}"
      # # elif [[ "${LINE}" =~ ^-d\ .* ]]; then
      # #     DENSITY_LIMIT="$(echo ${LINE:3} | sed -e 's/^[[:space:]]*//')"
      # #     #>&2 echo "${LINE}"
     fi
  fi

  # if [ "${LINE}" == "QUERIES:" ]; then
  #     BLOCK_STATE="QUERIES"
  #     #>&2 echo "Enter $BLOCK_STATE block"
  # fi
done < "${BONHOMME_FILE}"

# check that each mandatory parameter is OK

if [ -z ${SGS_MAX_LENGTH+x} ]; then
    >&2 echo "Exit: the SGS max length parameter (-l) is not set corrrectly"
    exit 1
elif [[ ! "${SGS_MAX_LENGTH}" =~ ^[0-9]+$ ]]; then
    >&2 echo "Exit: the SGS max length (-l) must be a positive integer"
    exit 1
fi

if [ -z ${K+x} ]; then
    >&2 echo "Exit: the number of ranked solution parameter (-k) is not set corrrectly"
    exit 1
elif [[ ! "${K}" =~ ^[0-9]+$ ]]; then
    >&2 echo "Exit: the number of ranked solution parameter (-k) must be a positive integer"
    exit 1
fi

# if [ -z ${DENSITY_LIMIT+x} ]; then
#     >&2 echo "Exit: the genomic density treshold parameter (-d) is not set corrrectly"
#     exit 1
# elif [[ ! "${DENSITY_LIMIT}" =~ ^[0-9]+([.][0-9]+)?$ ]]; then
#     >&2 echo "Exit: the genomic density treshold parameter (-d) must be a float in [0,1]"
#     exit 1
# fi

# #--- Generate queries ---#
#
# if [ ! -z ${QUERIES_COMMAND+x} ]; then
#     #>&2 echo "${QUERIES_COMMAND}"
#     if [[ "${QUERIES_COMMAND}" == genomic[[:space:]]* ]]; then
#         QUERIES_STATE=""
#         QUERIES_MIN=""
#         QUERIES_MAX=""
#         for PARAM in ${QUERIES_COMMAND:8}; do
#             #>&2 echo "${PARAM}"
#             if [[ "${QUERIES_STATE}" == "QUERIES_MIN" ]]; then
#                 QUERIES_MIN="${PARAM}"
#                 QUERIES_STATE=""
#             elif [[ "${QUERIES_STATE}" == "QUERIES_MAX" ]]; then
#                 QUERIES_MAX="${PARAM}"
#                 QUERIES_STATE=""
#             elif [[ "${PARAM}" == "-min" ]]; then
#                 QUERIES_STATE="QUERIES_MIN"
#             elif [[ "${PARAM}" == "-max" ]]; then
#                 QUERIES_STATE="QUERIES_MAX"
#             else
#                 >&2 echo "Wrong parameter(s) for genomic query generation"
#                 exit 1
#             fi
#         done
#         if [[ "${QUERIES_MIN}" =~ ^[0-9]+$ && "${QUERIES_MAX}" =~ ^[0-9]+$ ]]; then
#             >&2 echo "Generate queries"
#             GENE_SEQ="$(mktemp -t gene_seq.XXXXXXXX)"
#             for CHR in ${CHR_LIST}; do
#                 eval "awk -v selected_id=\"${CHR}\" -v chr_column_id=\"chromosome_id\" -v gene_column_id=\"gene_id\" '$SELECT_CHR_AWK' ${GENOME_FILE}" > ${GENE_SEQ}
#                 shogen_queries.py ${GENE_SEQ} ${CATALYZE_FILE} -ming ${QUERIES_MIN} -maxg ${QUERIES_MAX} | sed "s/${TAB}/ /g" >> ${QUERIES_FILE}
#             done
#             rm "${GENE_SEQ}"
#         else
#             >&2 echo "-min/-max wait for an integer"
#             exit 1
#         fi
#     else
#         >&2 echo "Wrong query generation command"
#         exit 1
#     fi
# fi
# # We remove blank lines that make shogen crash and duplicated queries.
# # The sed -i syntax is different between Mac OS X and Linux. We use then a temp file.
# QUERIES_FILE_TEMP="$(mktemp -t queries.XXXXXXXX)"
# sed '/^$/d' ${QUERIES_FILE} | sort -u > ${QUERIES_FILE_TEMP}
# mv ${QUERIES_FILE_TEMP} ${QUERIES_FILE}

#-------------------------------------------#
#             "SGS Computation"             #
#-------------------------------------------#
>&2 echo "SGS Computation"

# List of all the SGS (temp file).
#SGS_LIST="$(mktemp -t SGS_list.XXXXXXXX)"
SGS_LIST="SGS_list.${SHOGEN_EXT}"
SGS_HEAD=""

#--- Working on each CHROMOSOME ---#
for CHR in ${CHR_LIST}; do
        >&2 echo "Working on ${CHR}"
        SGS_LIST_TEMP="$(mktemp -t SGS_tmp.XXXXXXXX)"

        # Generate the gene sequence for each chromosome"
        GENE_SEQ="$(dirname ${GENOME_FILE})/${CHR}_gene_seq.${SHOGEN_EXT}"
        eval "awk -v selected_id=\"${CHR}\" -v chr_column_id=\"chromosome_id\" -v gene_column_id=\"gene_id\" '$SELECT_CHR_AWK' ${GENOME_FILE}" > ${GENE_SEQ}

        # Compute the SGS
        shogen.py ${GENE_SEQ} ${REACTION_GRAPH_FILE} ${CATALYZE_FILE} ${QUERIES_FILE} -k ${K} -l ${SGS_MAX_LENGTH} | shogen2tab.py -q ${GENE_SEQ} > ${SGS_LIST_TEMP}
        SGS_HEAD="$(head -1 ${SGS_LIST_TEMP})"
        awk -v id="${CHR}" 'NR > 1 {print id "\t" $0}' "${SGS_LIST_TEMP}" >> "${SGS_LIST}"
        rm "${SGS_LIST_TEMP}"
done

# Add the header
SGS_LIST_TEMP=$(mktemp -t SGS_tmp.XXXXXXXX)
mv ${SGS_LIST} ${SGS_LIST_TEMP}
echo "chromosome_id${TAB}${SGS_HEAD}" #> ${SGS_LIST}
cat ${SGS_LIST_TEMP} #>> ${SGS_LIST}
#rm ${SGS_LIST_TEMP}

# Add reactions associated to each SGS
#OUTPUT="$(mktemp -t SGS_list_react.XXXXXXXX)"
#sgs_add_reaction_sets.py ${REACTION_GRAPH_FILE} ${CATALYZE_FILE} ${SGS_LIST}
#rm ${SGS_LIST}
#mv ${OUTPUT} ${SGS_LIST}
