
import scipy.io.wavfile
import os
import numpy as np
import matplotlib.pyplot as plt
import ffmpeg

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

    def __init__(self, path, frame=None):
        self.file = path
        self.rate = None
        self.data = None
        self.frame = frame
        self.frames = None
        self.length = None
        self._is_wav_format = None

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
            self.rate, self.data = self.audio_reader.read(self.file)
            self._is_wav_format = True
        except ValueError as value_error:
            print(f"Error: Can not read {self.file}"
                  "(It is not uncompressed wav format)")
            self.rate, self.data = -1, np.array([])
            self._is_wav_format = False

    def compute_short_term_energy(self):
        """Counting Short-term energy:
            it is defined as the sum of the squared absolute values of 
            the amplitudes, normalized by the frame length"""
        if self.data is not None:
            # array_split splits an array into multiple sub-arrays of equal or near-equal size.
            self.frames = np.array_split(self.data, self.frame)
        return sum([abs(float(sum(x)))**2 for x in self.frames])/len(self.frames)

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