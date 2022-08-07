#!/bin/bash
for trace in traces/*.gz
do
    for pref in example_prefetchers/*.cc
    do
        echo "Processing $trace on $pref"
        mkdir -p result/$(basename $trace _trace2.dpc.gz)
        rm -rf dpc2sim-stream
        g++ -Wall -o dpc2sim-stream $pref lib/dpc2sim.a
        time (zcat $trace | ./dpc2sim-stream) > result/$(basename "$trace" _trace2.dpc.gz)/$(basename "$pref" .cc) 2>&1
        echo "Done."
    done
done