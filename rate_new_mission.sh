#!/bin/bash

# pass logname as parameter
# move file to processed when done
#
# need to count argv and also have use statement
#
# check file is in cwd missions directory and
# error if not
if [ "$#" -ne 1 ]; then
    echo "Illegal number of parameters"
    echo "USAGE: " $0 "mavlogdump filename"
    exit 1
fi

# data directory in current working directory

mkdir -p data
rm -fr missions
mkdir -p missions

cp $1 missions

if [ "$?" != 0 ]; then
    echo $1 " file does not exist " 
    exit 1
fi

tlogname=`ls missions `
filename=`echo "$tlogname" | awk -F"." '{ print "missions/"$1".log" }'`
timefile=`echo "$tlogname" | awk -F"." '{ print "data/times_"$1".log" }'`
outputdir=`echo "$tlogname" | awk -F"." '{ print "data/"$1"/"}'`
outputdirname=`echo "$tlogname" | awk -F"." '{ print "$1"}'`

# files directory in current working directory

mkdir -p ${outputdir}

# check that this can execute and returns 0

python code/mavlogdump.py "missions/${tlogname}" > "${filename}"
if [ "$?" != 0 ]; then
    echo "File missions/" ${tlogname} " not in mavlogdump format" 
    exit 1
fi
#
# find unique times during mission
#

awk '{print $1, substr($2, 0, length($2))}' ${filename} |sort | uniq > "${timefile}"

i=$((0))

cat ${timefile} | while read a 
do 
    echo "grep" \'$a\' "${filename}" > data/x.sh
    chmod +x data/x.sh
    data/x.sh > y.txt

    #
    # print status as counts every 10%
    # need to be able to do a mod with i in bash
    #

    printf "date,time,mission,quality" > head.txt
    head -1 y.txt |  m=$mission q=$quality awk '{printf $1","substr($2,0,length($2))","ENVIRON["m"]","ENVIRON["q"] }' > data.txt

    cat y.txt | while read a
    do
       event_name=''
       event_name=$(echo $a | awk '{print $3}')
       
       if [ "$event_name" != "STATUSTEXT" -a "$event_name" != "BAD_DATA" -a "$event_name" != "PARAM_REQUEST_LIST" -a "$event_name" != "REQUEST_DATA_STREAM" -a "$event_name" != "PARAM_VALUE" -a "$event_name" != "TERRAIN_DATA" -a "$event_name" != "AUTOPILOT_VERSION" ]; then
                                                                             
           var_name=$(echo $a | awk -F{ '{print $2}')
           var_name=`echo "$var_name" | sed -r 's/ : /,/g' | sed -r 's/, /,/g' | sed -r 's/}//g'`

           for ((c=1;c<=`echo $var_name | awk -F, '{print NF}'`; c++))
           do
               if [ "$(($c%2))" -eq "0" ]; then
                        echo $var_name | X=$event_name awk -v c=$c -F, '{printf "," $c}'>>data.txt
                    else
                        echo $var_name | X=$event_name awk -v c=$c -F, '{printf ","ENVIRON["X"]"_"$c}'>>head.txt
               fi
           done
        fi
       #X=$var_name Y=$event_name awk 'BEGIN{print ENVIRON["X"], ENVIRON["Y"]}'
    done
    
    # only move files with data

    if [ "`cat head.txt | awk -F, '{print NF}'`" -gt "4" ]; then

        # add end of line

        sed  -i -e '$a\' head.txt
        sed  -i -e '$a\' data.txt

        # add data to file

        cat data.txt >> head.txt

        mv head.txt ${outputdir}file${i}.txt

        i=$((i + 1))
    fi
done

mv "missions/${tlogname}" "missions/${tlogname}.processed"

cd code

python read_txt_to_df.py ${outputdirname}
python agribotix_model.py ${outputdirname}
