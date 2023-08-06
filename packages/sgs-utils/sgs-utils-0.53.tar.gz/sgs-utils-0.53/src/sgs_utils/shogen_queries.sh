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

BIN_PATH="./bin"

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
CATALYZE_FILE="$2"
BONHOMME_FILE="$3"
QUERIES_FILE="$4"

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
#QUERIES_FILE="${RESULT_DIR}/queries.${SHOGEN_EXT}"

if [ -f ${QUERIES_FILE} ]; then
    rm ${QUERIES_FILE}
fi
touch ${QUERIES_FILE}

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
      if [[ "${LINE}" =~ ^-q\ .* ]]; then
          QUERIES_COMMAND="$(echo ${LINE:3} | sed -e 's/^[[:space:]]*//')"
          #>&2 echo "${LINE}"
      fi
  fi

  if [ "${LINE}" == "QUERIES:" ]; then
      BLOCK_STATE="QUERIES"
      #>&2 echo "Enter $BLOCK_STATE block"
  fi
done < "${BONHOMME_FILE}"

#--- Generate queries ---#

if [ ! -z ${QUERIES_COMMAND+x} ]; then
    #>&2 echo "${QUERIES_COMMAND}"
    if [[ "${QUERIES_COMMAND}" == genomic[[:space:]]* ]]; then
        QUERIES_STATE=""
        QUERIES_MIN=""
        QUERIES_MAX=""
        for PARAM in ${QUERIES_COMMAND:8}; do
            #>&2 echo "${PARAM}"
            if [[ "${QUERIES_STATE}" == "QUERIES_MIN" ]]; then
                QUERIES_MIN="${PARAM}"
                QUERIES_STATE=""
            elif [[ "${QUERIES_STATE}" == "QUERIES_MAX" ]]; then
                QUERIES_MAX="${PARAM}"
                QUERIES_STATE=""
            elif [[ "${PARAM}" == "-min" ]]; then
                QUERIES_STATE="QUERIES_MIN"
            elif [[ "${PARAM}" == "-max" ]]; then
                QUERIES_STATE="QUERIES_MAX"
            else
                >&2 echo "Wrong parameter(s) for genomic query generation"
                exit 1
            fi
        done
        if [[ "${QUERIES_MIN}" =~ ^[0-9]+$ && "${QUERIES_MAX}" =~ ^[0-9]+$ ]]; then
            >&2 echo "Generate queries"
            GENE_SEQ="$(mktemp -t gene_seq.XXXXXXXX)"
            for CHR in ${CHR_LIST}; do
                eval "awk -v selected_id=\"${CHR}\" -v chr_column_id=\"chromosome_id\" -v gene_column_id=\"gene_id\" '$SELECT_CHR_AWK' ${GENOME_FILE}" > ${GENE_SEQ}
                sgs-utils.py generate queries ${GENE_SEQ} ${CATALYZE_FILE} -ming ${QUERIES_MIN} -maxg ${QUERIES_MAX} | sed "s/${TAB}/ /g" >> ${QUERIES_FILE}
            done
            rm "${GENE_SEQ}"
        else
            >&2 echo "-min/-max wait for an integer"
            exit 1
        fi
    else
        >&2 echo "Wrong query generation command"
        exit 1
    fi
fi
# We remove blank lines that make shogen crash and duplicated queries.
# The sed -i syntax is different between Mac OS X and Linux. We use then a temp file.
QUERIES_FILE_TEMP="$(mktemp -t queries.XXXXXXXX)"
sed '/^$/d' ${QUERIES_FILE} | sort -u > ${QUERIES_FILE_TEMP}
mv ${QUERIES_FILE_TEMP} ${QUERIES_FILE}
