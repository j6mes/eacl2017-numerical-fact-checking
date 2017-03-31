#!/bin/bash
#$ -l mem=18G -l rmem=18G
#$ -o /dev/null
#$ -e /dev/null

module load apps/python/anaconda3-2.5.0
module load apps/java/1.8u71

cd ..

source activate factchecking

#./gradlew writeClasspath
export CLASSPATH=`cat build/classpath.txt`

PYTHONPATH=./src python ./src/run/ds_generate_positive_features_for_query.py emnlp $SGE_TASK_ID

source deactivate
