#!/bin/bash
#$ -l mem=3G -l rmem=3G
#$ -pe openmp 1

module load apps/python/anaconda3-2.5.0
cd ..

source activate factchecking

python data_reader.py $EXPT | tee logs/$EXPT.log

source deactivate