
import scipy.io.wavfile
import os
import numpy as np
import matplotlib.pyplot as plt
import ffmpeg
import wave
import scipy.signal as sps
import shlex

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
    >>> audio = ProcessAudio("file.wav")
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
        self.frame_size_in_ms = 0.01
        self.nptype = None
        self.out_file = 'm_' + os.path.basename(self.file)

    @staticmethod
    def chunks(l, k):
        """
        Yields chunks of size k from a given list.
        """
        for i in range(0, len(l), k):
            yield l[i:i+k]

    def compute_energy(self):
        energy = []
        for chunk in self.chunks(self.data.tolist(), 
                                int(self.in_rate * self.frame_size_in_ms)):
#            breakpoint()
            energy.append(self.energy(chunk))
        return sum(energy)

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
        """
        Resampling inputed wav file by given sample rate

        parameters
        ----------
            rate : int
                sample rate
        """
        self.out_stream = wave.open(self.out_file, 'w')
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
        print(f"Created {self.out_file} file")

    @staticmethod
    def energy(frames):
        return sum([abs(x)**2 for x in frames])/len(frames)

    def compute_short_term_energy(self):
        """Counting Short-term energy:
            it is defined as the sum of the squared absolute values of 
            the amplitudes, normalized by the frame length"""
        if self.data is not None:
            # array_split splits an array into multiple sub-arrays of equal or near-equal size.
            self.frames = np.array_split(self.data, self.get_nframes())
            #return sum([abs(float(sum(x)))**2 for x in self.frames])/len(self.frames)
            return self.energy(self.frames)
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
    def change_sample_rate_by_ffmprg(in_file, out_file, rate):
        executable = os.path.join('ffmpeg', 'bin', 'ffmpeg.exe')
        out_file_to_in = f'{out_file}_{rate}.wav'
        if os.path.isfile(executable):
            popen = subprocess.peopen(
                shlex.split(f"{executable} -i {in_file} -ar {rate} -o {out_file_to_int}"),
                stdout = -1, stderr=-1
                )
            out, err = popen.communicate()
            if popen.returncode:
                self.in_file = out_file_to_in
        else:
            print(f"Error: {executable} is not found!")


def test(file_):
    po = ProcessAudio(file_)
    po.read()
    print(po.get_nframes())
    print(po.get_sample_rate())
    po.resample(60000)
    print(po.compute_energy())
    print(po.compute_short_term_energy())
    #breakpoint()

file_ = os.path.join("./tests", "sample_data", "data", "English.wav")
test(file_)
#test("m_English.wav")

