
import scipy.io.wavfile
import os
import numpy as np
import matplotlib.pyplot as plt
import ffmpeg
import wave
import scipy.signal as sps
import dask

class ProcessAudio:
    """ 
    A ProcessAudio class to parse or process an uncompressed wav format files

    Parameters
    ==========
        path: str
            audio file path
        frame: int
            audio file frame size
    
    Examples
    ========
    >>> audio = ProcessAudio("file.wav", 2048)
    >>> audio.read()
    >>> 
    """
    audio_reader = scipy.io.wavfile

    def __init__(self, path):
        self.file = path
        self.rate = None
        self.stream = None 
        self.data = None
        self.frame = None 
        self.frames = None
        self.length = None
        self._is_wav_format = None
        self.in_rate = 44100.0
        self.nptype = None

    def length(self):
        if self.data is not None:
            self.length = self.data.shape[0]//self.rate
            print(f"length = {self.length}s")

    def is_wav(self):
        return self._is_wav_format

    def read(self):
        """
        Reading audio file, parsing it into numpy array
        """
        if not os.path.isfile(self.file):
            print(f"Error: Audio file is not found: {self.file}")
        try:
            self.stream = wave.open(self.file)
            if self.stream.getsampwidth() == 1:
                self.nptype = np.uint8
            elif self.stream.getsampwidth() == 2:
                self.nptype = np.uint16
            self.rate, self.data = self.audio_reader.read(self.file)
            self._is_wav_format = True
        except ValueError as value_error:
            print(f"Error: Can not read {self.file}"
                  "(It is not uncompressed wav format)")
            self.rate, self.data = -1, np.array([])
            self._is_wav_format = False

    def resample(self, rate):
        self.out_stream = wave.open(f"m_{os.path.basename(self.file)}", 'w')
        self.out_stream.setframerate(rate)
        self.out_stream.setnchannels(self.stream.getnchannels())
        self.out_stream.setsampwidth (self.stream.getsampwidth())
        self.out_stream.setnframes(1)
        #print("Nr output channels: %d" % self.out_stream.getnchannels())
        audio = self.stream.readframes(self.stream.getnframes())
        nroutsamples = round(len(audio) * rate/self.get_sample_rate())
        print("Nr output samples: %d" %  nroutsamples)
        #audio_out = sps.resample(np.fromstring(audio, self.nptype), nroutsamples)
        audio_formatter = np.fromstring(audio, self.nptype)
        audio_out = sps.resample(audio_formatter, len(audio_formatter))
        audio_out = audio_out.astype(self.nptype)
        self.out_stream.writeframes(audio_out.copy(order='C'))
        self.out_stream.close()

    def compute_short_term_energy(self):
        """Counting Short-term energy:
            it is defined as the sum of the squared absolute values of 
            the amplitudes, normalized by the frame length"""
        if self.data is not None:
            # array_split splits an array into multiple sub-arrays of equal or near-equal size.
            self.frames = np.array_split(self.data, self.get_nframes())
            return sum([abs(float(sum(x)))**2 for x in self.frames])/len(self.frames)
        else:
            print("Error: First of all need to call 'read' method!")

    def plot(self):
        """
        Ploting audio file in 2D dieagram
        """
        time = np.linspace(0., self.length, self.data.shape[0])
        breakpoint()
        plt.plot(time, self.data, label="Left channel")
        #plt.plot(time, self.data[:, 1], label="Right channel")
        plt.legend()
        plt.xlabel("Time [s]")
        plt.ylabel("Amplitude")
        plt.show()

    def get_sample_rate(self):
        return self.stream.getframerate()

    def get_nframes(self):
        return self.stream.getnframes()

    @staticmethod
    def change_sample_rate(in_file, out_file, rate):
        executable = os.path.join('ffmpeg', 'bin', 'ffmpeg.exe')
        if os.path.isfile(executable):
            os.system(f"{executable} -i {in_file} -ar {rate} -o {out_file}_{rate}.wav")
        else:
            print(f"Error: {executable} is not found!")


def test(file_):
    po = ProcessAudio(file_)
    po.read()
    print(po.get_nframes())
    print(po.get_sample_rate())
    po.resample(60000)
    print(po.compute_short_term_energy())
    #breakpoint()

file_ = os.path.join("./tests", "sample_data", "data", "English.wav")
test(file_)
#test("m_English.wav")

