#!/bin/bash
#$ -l mem=3G -l rmem=3G
#$ -pe openmp 1

module load apps/python/anaconda3-2.5.0
cd ..

source activate factchecking

python data_reader.py $BOW $NG | tee logs/$BOW.$NG.log

source deactivate