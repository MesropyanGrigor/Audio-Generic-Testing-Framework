import os 
import glob


TEST_DIR = "tests"
DIRECTORIES = [os.path.join(TEST_DIR, 'sample_data', dir_) for dir_ in ['data', 'voices\\audios']]

#for directory in directories:
FILES = []
for dir_ in DIRECTORIES:
    FILES.extend(glob.glob(os.path.join(dir_, '*')))
THRESHOLD = 0.5

THRESHOLD_1 = 1
RESAMPLE_DATA = [(file_, THRESHOLD_1, sign) for file_ in FILES for sign in ['+', '-']] 