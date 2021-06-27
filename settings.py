import sys
import os 
import glob


sys.path.append(os.getcwd())
directories = ['data', 'voices']
threshold = 1000

#for directory in directories:
files = glob.glob(os.path.join(directories[0], '*'))
#print(files)