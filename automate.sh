#! /usr/bin/env bash

trap "exit" INT

for i in `find ./ -name "*.sol"`;
do
        echo '++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++'
        echo 'Now testing - '$i
        # echo '++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++' >> ./test_results.log
        # echo 'Now testing - '$i >> ./test_results.log
        echo '++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++'

        /usr/bin/time -v oyente -s $i > /oyente/mythril-results/oyente/results/$(basename $(pwd))/$(basename $i).json 2>&1


        echo '++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++'
done