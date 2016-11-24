#!/bin/bash
#$ -l mem=10G -l rmem=10G
#$ -t 0-55
#$ -o /dev/null
#$ -e /dev/null

module load apps/python/anaconda3-2.5.0
module load apps/java/1.8u71

cd ..

source activate factchecking

#./gradlew writeClasspath
export CLASSPATH=`cat build/classpath.txt`

python src/run/ $SGE_TASK_ID

source deactivate