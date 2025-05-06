#!/bin/bash
set -ex

quick_test=0

if [[ ($# -eq 1) && ($1 == '-q') ]]; then
    quick_test=1
fi

rm -f simdata.* 
make clean
make 
        
time ./program

python WormViewCSV.py -nogui # Test reloading csv 

python generate_wcon.py 
python WormView.py -f simdata.wcon -nogui # Test reloading wcon  

