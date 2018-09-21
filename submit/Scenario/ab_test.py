import pathlib
import os.path
import sys
import socket

source_path = '/common/home/kalyakulina_a/Work/mlmg/source/python/Methylation'
source_name = 'infrastructure.hierarchy'

os.system('sbatch ./ab_submit.sh' + ' ' + source_path + ' ' + source_name)
