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

awk -v col1="${1}" -v col2="${2}" \
'BEGIN {FS="\t"}
    NR == 1 {for (i=1; i<=NF; i++){
       if($i==col1){c1=i};
       if($i==col2){c2=i};}}
    NR > 1 {split($c2,tab," ");
		    for ( i in tab ) {print $c1 FS tab[i]}
		   }
END{}' "${3}"
