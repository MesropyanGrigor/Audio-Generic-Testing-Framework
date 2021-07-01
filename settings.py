import sys
import os 
import glob


sys.path.append(os.getcwd())
TEST_DIR = "tests"
DIRECTORIES = [os.path.join(TEST_DIR, 'sample_data', dir_) for dir_ in ['data', 'voices\\audios']]

#for directory in directories:
files = []
for dir_ in DIRECTORIES:
    files.extend(glob.glob(os.path.join(dir_, '*')))
THRESHOLD = 10
RESAMPLE_DATA = [(file_, THRESHOLD, sign) for file_ in files for sign in ['+', '-']] 