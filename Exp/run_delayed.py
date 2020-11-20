import time
import os
import sys

os.remove('nohup.out')
n_submit = int(float(sys.argv[1]))
hours = float(sys.argv[2])
time.sleep(60 * hours)

os.system('python run.py ' + str(n_submit))
