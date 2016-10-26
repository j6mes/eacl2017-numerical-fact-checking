#!/bin/bash

for i in `seq 0 3`; do
    for j in `seq 0 3`; do
        BOW=$i NG=$j qsub -cwd -V eval_table_rank.sh
    done
done
