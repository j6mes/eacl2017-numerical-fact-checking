#!/bin/bash
#$ -l mem=42G -l rmem=20G

module load apps/python/anaconda3-2.5.0
module load apps/java/1.8u71

cd ..

source activate factchecking

#./gradlew writeClasspath
export CLASSPATH=`cat build/classpath.txt`

PYTHONPATH=./src python ./src/eval.py $SGE_TASK_ID

source deactivate
