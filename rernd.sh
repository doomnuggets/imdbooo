#!/bin/bash

#
# Make sure the indexer keeps running when it either finishes or crashes.
#

while true
do
    process_alive=$(pgrep rnd.sh)
    if [ ! $process_alive ]
    then
        echo 'Restarting crawler...'
        ./rnd.sh $@
    fi
done
