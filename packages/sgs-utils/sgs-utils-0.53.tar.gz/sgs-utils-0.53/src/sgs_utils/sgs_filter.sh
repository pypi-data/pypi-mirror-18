# !/bin/bash
# Copyright (c) 2013-2014, Philippe Bordron <philippe.bordron@gmail.com>
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


# Args description
# -l : min length of a SGS
# -L : max length of a SGS
# -d : min density of a SGS
# -D : dominant SGS only
# -s : sort
# -S : sort in reverse order
# -i : input

# If a parameter is used many time, only the last one will be considered

# INIT
MIN_LENGTH=
MAX_LENGTH=
DENSITY=
#DOMINANT=
INPUT=
SORT=0 # <0 : reverse order, >0 natural order, 0 no sorting

# Usefull things
TAB=$(echo a | tr a '\t')

#while getopts "l:L:d:i:DsS" opt; do
while getopts "l:d:i:DsS" opt; do
  case $opt in
    l)
      MIN_LENGTH=$OPTARG
      ;;
 #   L)
 #     MAX_LENGTH=$OPTARG
 #	  ;;
    d)
      DENSITY=$OPTARG
      ;;
    #D)
    #  DOMINANT=$(true)
    #  ;;
    s)
      SORT=-1
      ;;
    S)
	  SORT=1
	  ;;
    i)
	  INPUT=$OPTARG
	  ;;
	:)
      echo "Missing argument to option -$OPTARG" >&2
	  exit 1
	  ;;
    \?)
      echo "Invalid option: -$OPTARG" >&2
      ;;
  esac
done

if [ ! $INPUT ]; then
	echo "missing input file (-i switch)"
	exit 1
fi

CMD="cat $INPUT"


FILTER_AWK='BEGIN{FS="\t"; d=-1}
	NR == 1 {
		print $0;
		for (i=1; i<=NF; i++)
		{
			if ($i==column_id){d=i};
		}
	}
	NR > 1 && $d >= value {print $0}
END{}'

if [ $MIN_LENGTH ]; then
        #echo "SGS minimal size : $MIN_LENGTH"
		#LCMD="awk -v column_id=\"length\" -v value=$MIN_LENGTH -v mod=1 '$FILTER_AWK'"
		LCMD="awk -v column_id=\"length\" -v value=$MIN_LENGTH '$FILTER_AWK'"
		CMD="$CMD | $LCMD"

fi

if [ $MAX_LENGTH ]; then
		LCMD="awk -v column_id=\"length\" -v value=$MAX_LENGTH -v mod='-1' '$FILTER_AWK'"
		CMD="$CMD | $LCMD"
fi

if [ $DENSITY ]; then
		#LCMD="awk -v column_id=\"density\" -v value=$DENSITY -v mod=1 '$FILTER_AWK'"
		LCMD="awk -v column_id=\"density\" -v value=$DENSITY '$FILTER_AWK'"
		CMD="$CMD | $LCMD"
fi

HEAD="head -n 1 $INPUT"
if [ ${SORT} -ne 0 ]; then
  HEADER=$(head -n 1 $INPUT | tr "\t" " ")
  COUNT=0
  for H in ${HEADER}; do
    COUNT=$((COUNT+1))
    if [[ "$H" == "start_position" ]]; then
       START_COL="${COUNT}";
    fi
    if [[ "$H" == "end_position" ]]; then
       END_COL="${COUNT}";
    fi
  done
  eval $HEAD
fi

if [ ${SORT} -lt 0 ]; then
  		LCMD="awk 'NR > 1' | sort -k${START_COL}nr,${START_COL}nr -k${END_COL}n,${END_COL}n"
		CMD="$CMD | $LCMD"
elif [ ${SORT} -gt 0 ]; then
		LCMD="awk 'NR > 1' | sort -k${START_COL}n,${START_COL}n -k${END_COL}nr,${END_COL}nr"
		CMD="$CMD | $LCMD"
fi


#echo $CMD
eval $CMD
