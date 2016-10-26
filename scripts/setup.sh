#!/bin/bash

module load apps/python/anaconda3-2.5.0
cd ..

conda create -n factchecking python=3.5 numpy scikit-learn


wget http://nlp.stanford.edu/software/sempre/wikitable/WikiTableQuestions-1.0.2.zip
unzip WikiTableQuestions-1.0.2.zip
