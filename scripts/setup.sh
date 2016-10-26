#!/bin/bash

module load apps/python/anaconda3-2.5.0
cd ..

conda create -n factchecking python=3.5 numpy scikit-learn
