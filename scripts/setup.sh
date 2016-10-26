#!/bin/bash

cd ..

mkdir logs

wget http://nlp.stanford.edu/software/sempre/wikitable/WikiTableQuestions-1.0.2.zip
unzip WikiTableQuestions-1.0.2.zip

module load apps/python/anaconda3-2.5.0
conda create -n factchecking python=3.5 numpy scikit-learn


