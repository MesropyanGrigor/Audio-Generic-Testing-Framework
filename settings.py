import sys
import os 
import glob


sys.path.append(os.getcwd())
TEST_DIR = "tests"
directories = [os.path.join(TEST_DIR, 'sample_data', dir_) for dir_ in ['data', 'voices']]
threshold = 1000

#for directory in directories:
files = []
for dir_ in directories:
    files.extend(glob.glob(os.path.join(directories[0], '*')))
THRESHOLD = 5000
RESAMPLE_DATA = [(file_, THRESHOLD, sign)for file_ in files for sign in ['+', '-']] 