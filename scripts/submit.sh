#!/bin/bash


EXPT=0 qsub -cwd -V eval_table_rank.sh
EXPT=1 qsub -cwd -V eval_table_rank.sh #bag of words intersection
EXPT=2 qsub -cwd -V eval_table_rank.sh #bag of words union
EXPT=3 qsub -cwd -V eval_table_rank.sh #both bag of words models
