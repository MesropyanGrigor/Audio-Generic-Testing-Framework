import pytest
import os

#sys.path.append("../../settings.py")

from Krisp.settings import files
import Krisp.utils as tt


#@pytest.fixture
#def testdata():
#    return [(f, 30, 45) for f in files]
testdata = [(f, 30, 45) for f in files]

#testdata = []
#
#@pytest.fixture(scope="module")
#def init_data():
#    print("Initalizing data")
#    global testdata
#    testdata = [(f, 30, 45) for f in files]
#    return testdata

@pytest.mark.parametrize("file", files)
def test_not_file_size_is_zero(file):
    assert os.path.getsize(file) > 0

@pytest.mark.parametrize("file", files)
def test_file_ends_with_wav(file):
    assert file.split('.')[-1] == 'wav'

@pytest.mark.parametrize("file,frame,threshold", testdata)
def test_compare_energy_value_with_threshold(file, frame, threshold):
    wav_obj = tt.ProcessAudio(file, frame)
    wav_obj.read()
    assert wav_obj.compute_short_term_energy() > threshold, "Error: Lower than expected"

@pytest.mark.parametrize("file", files)
def test_is_wav_file(file):
    wav_obj = tt.ProcessAudio(file)
    wav_obj.read()
    assert wav_obj.is_wav == True


# check is the file wave format or not