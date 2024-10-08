#!/bin/bash
for inf in *.gjf
do
echo Running ${inf} ...
# submit all once with & /one by one without this symbol &
time g16 < ${inf} > ${inf//gjf/log} 
echo ${inf} is finished
echo
done