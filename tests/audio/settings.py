import os 
import glob
import shutil

TMP = 'tmp_1'
if os.path.isdir(TMP) and len(os.listdir(TMP)) != 0:
    shutil.rmtree(TMP, ignore_errors=True)
os.mkdir(TMP)

TEST_DIR = "tests"
DIRECTORIES = [os.path.join(TEST_DIR, 'sample_data', dir_) for dir_ in ['data', 'voices\\audios']]

#for directory in directories:
FILES = []
for dir_ in DIRECTORIES:
    FILES.extend(glob.glob(os.path.join(dir_, '*')))
THRESHOLD = 10
RESAMPLE_DATA = [(file_, THRESHOLD, sign) for file_ in FILES for sign in ['+', '-']] 