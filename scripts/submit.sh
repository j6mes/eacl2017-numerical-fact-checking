#!/bin/bash


EXPT=0 qsub -cwd -V eval_table_rank.sh
EXPT=1 qsub -cwd -V eval_table_rank.sh
EXPT=2 qsub -cwd -V eval_table_rank.sh
