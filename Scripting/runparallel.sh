#!/bin/bash

rung16() {
    echo "Running ${1} ..."
    local COUNT=${2}
    let COUNT+=1
    echo $COUNT > count.tmp
    # submit all once with & /one by one without this symbol &
    time g16 < ${1} > ${1//gjf/log} &
    wait
    COUNT=$(cat count.tmp)
    let COUNT-=1
    echo $COUNT > count.tmp
    echo "${1} is finished"
}

# write how many process you want to submit
MAXNUM=4
COUNT=0
echo $COUNT > count.tmp
for inf in *.gjf
do  
    COUNT=$(cat count.tmp)
    if [ $COUNT -lt $MAXNUM ] 
    then
        rung16 $inf $COUNT &
        sleep 2
    else
        while [ $COUNT -ge $MAXNUM ]
        do
            sleep 60
            COUNT=$(cat count.tmp)
        done
        rung16 $inf $COUNT &
    fi   
done