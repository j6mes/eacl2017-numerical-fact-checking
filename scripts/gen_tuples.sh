#!/bin/bash
#$ -l mem=20G -l rmem=20G
#$ -pe openmp 1

module load apps/python/anaconda3-2.5.0
module load apps/java/1.8u71

cd ..

source activate factchecking

python data_reader.py $BOW $NG | tee logs/$BOW.$NG.log

source deactivate