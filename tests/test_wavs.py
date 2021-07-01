import pytest
import os
import glob

from Krisp.settings import files, RESAMPLE_DATA, THRESHOLD
import Krisp.utils as tt

ALL_FILES = files
TESTDATA = [(f, 30, 45) for f in files]

@pytest.fixture()
def threshold():
    return THRESHOLD

@pytest.mark.parametrize("file", ALL_FILES)
def test_file_size_is_not_zero(file):
    assert os.path.getsize(file) > 0, "Empty file"

@pytest.mark.parametrize("file", ALL_FILES)
def test_file_ends_with_wav(file):
    assert file.split('.')[-1] == 'wav', "Does not end 'wav extension'"

@pytest.mark.parametrize("file", ALL_FILES)
def test_is_wav_file(file):
    wav_obj = tt.ProcessAudio(file)
    wav_obj.read()
    assert wav_obj.is_wav() == True, f"{file} is not wav format"

@pytest.mark.parametrize("file", ALL_FILES)
def test_rate_is_44100(file):
    wav_obj = tt.ProcessAudio(file)
    wav_obj.read()
    assert wav_obj.rate == 44100, f"Rate is not 44100"

@pytest.mark.parametrize("file", ALL_FILES)
def test_energy_with_threshold(file, threshold):
    wav_obj = tt.ProcessAudio(file)
    wav_obj.read()
    assert wav_obj.compute_energy() > threshold, "Error: Lower than expected"

@pytest.mark.parametrize("file", ALL_FILES)
def test_is_energy_0(file):
    wav_obj = tt.ProcessAudio(file)
    wav_obj.read()
    assert wav_obj.compute_energy() > 0, "Error: Energy should not be lower than 0"

@pytest.mark.parametrize("file,threshold,sign", RESAMPLE_DATA)
def test_energy_after_up_or_down_sampling(file, threshold, sign):
    # threshold is unsued variable keeped it to use 
    # RESAMPLE_DATA
    wav_obj = tt.ProcessAudio(file)
    wav_obj.read()
    energy = wav_obj.compute_energy()
    wav_obj.resampling(eval(f"{wav_obj.rate} {sign} 10000"))
    wav_obj.read()
    energy_after_resampling = wav_obj.compute_energy()
    sub = energy - energy_after_resampling
    assert abs(sub) > 0  and abs(sub) < 100 

@pytest.mark.parametrize("file,threshold,sign", RESAMPLE_DATA)
def test_energy_after_up_or_down_sampling_by_ffmpeg(file, threshold, sign):
    wav_obj = tt.ProcessAudio(file)
    wav_obj.read()
    wav_obj.resampling_by_ffmpeg(eval(f"{wav_obj.rate} {sign} 10000"))
    wav_obj.read()
    assert wav_obj.compute_energy() > threshold, "Error: Lower than expected"


# create tests1/tests_wav2.py tests1/tests_wav1.py
# create tests2/test_wav1.py
# create help file
# represent pytest first of all 
# create html report file for tests

#def pytest_generate_tests(metafunc, all_files):
#    if "file" in metafunc.funcargnames:
#        for file in all_files:
#            metafunc.addcall(funcargs=dict(file=file))
