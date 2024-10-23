#!/bin/bash
# Author: Leo 

# Current version: 1.0
# Update log 
# 2024-10-23 Version: 1.0: The first version released by Leo
# launch multiple g16 jobs at the same time

###### Begin User INPUT ####################

# write how many tasks you want to submit at the same time
MAXNUM=4

####### End User INPUT #####################

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