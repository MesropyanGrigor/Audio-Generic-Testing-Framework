import os
import wave
import scipy.signal as sps
import shlex
import subprocess
import soundfile
import shutil
import numpy as np
import matplotlib.pyplot as plt

class ProcessAudio:
    """ 
    A ProcessAudio class parse or process an uncompressed wav format files

    For reading audio files used soundfile module as it is working better,
    It can parse 64RF format audio file, which for example others could not
    (wave, scipy.io.wavefile).

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
    >>> audio.compute_energy()
    >>> audio.get_sample_rate())
    >>> audio.resampling(100000)
    """

    executable = os.path.abspath(os.path.join('.', 'ffmpeg', 'bin', 'ffmpeg.exe'))

    def __init__(self, path, tmp='tmp_1'):
        self.file = path
        if not os.path.isfile(self.executable):
            raise OSError(f"Error: {executable} is not found!")
        self.data = np.array([]) # empty array
        self._is_wav_format = False
        self.rate = -1
        self.stream = None 
        self.frame = None 
        self.frames = None
        self.length = None
        self.frame_size_in_ms = 0.01
        self.nptype = None
        self.out_file = 'm_' + os.path.basename(self.file)
        self.tmp = os.path.abspath(tmp)
        if os.path.exists(self.tmp):
            shutil.rmtree(self.tmp, ignore_errors=True)
        os.mkdir(self.tmp)

    @staticmethod
    def chunks(data, size):
        """
        Yields chunks of size from a given data list.
        """
        for ind in range(0, len(data), size):
            yield data[ind:ind+size]

    def compute_energy(self):
        energy = []
        for chunk in self.chunks(self.data.tolist(), 
                                int(self.rate * self.frame_size_in_ms)):
            energy.append(self.energy(chunk))
        return sum(energy)

    def set_length(self):
        """Setting length attribute"""
        if self.data is not None:
            self.length = self.data.shape[0]//self.rate
            print(f"length = {self.length}s")

    def is_wav(self):
        return self._is_wav_format

    def read(self):
        """
        Reading audio file, parsing it into numpy array
        
        There are wav files in 64RF format which currently can handle 
        'soundfile' module.
        """
        if not os.path.isfile(self.file):
            raise FileNotFoundError(f"Error: Audio file is not found: {self.file}")
        try:
           self.stream = soundfile.SoundFile(self.file)
           self.stream._prepare_read(0, None, -1)
           # if self.stream.getsampwidth() == 1:
           #     self.nptype = np.uint8
           # elif self.stream.getsampwidth() == 2:
           #     self.nptype = np.uint16
           self.data = self.stream.read()
           self.rate = self.stream.samplerate
           self._is_wav_format = True
           self.set_length()
        except ValueError as value_error:
            print(f"Error: Can not read {self.file}"
                  "(It is not uncompressed wav format)")

    #def resample(self, rate):
    #    """
    #    Resampling inputed wav file by given sample rate

    #    parameters
    #    ----------
    #        rate : int
    #            sample rate
    #    """
    #    self.out_stream = wave.open(self.out_file, 'w')
    #    self.out_stream.setframerate(rate)
    #    self.out_stream.setnchannels(self.stream.channels)
    #    self.out_stream.setsampwidth (self.stream.getsampwidth())
    #    self.out_stream.setnframes(1)
    #    audio = self.stream.readframes(self.stream.getnframes())
    #    nroutsamples = round(len(audio) * rate/self.get_sample_rate())
    #    print("Nr output samples: %d" %  nroutsamples)
    #    #audio_out = sps.resample(np.fromstring(audio, self.nptype), nroutsamples)
    #    audio_formatter = np.fromstring(audio, np.uint16)
    #    audio_out = sps.resample(audio_formatter, len(audio_formatter))
    #    audio_out = audio_out.astype(np.uint16)
    #    self.out_stream.writeframes(audio_out.copy(order='C'))
    #    self.out_stream.close()


    def resampling(self, rate):
        """
        Resampling inputed wav file by given sample rate
        
        Using scipy.signal.resaple function

        parameters
        ----------
            rate : int
                sample rate
        """
        n_of_samples = round(len(self.data) * rate/self.rate)
        new_data = sps.resample(self.data, n_of_samples)
        out_file = os.path.join(self.tmp, self.out_file)
        with soundfile.SoundFile(out_file, 'w', rate, 1, 'PCM_24') as file_:
            file_.write(new_data)
        if os.path.isfile(self.out_file):
            self.file = out_file
            print(f"Created {os.path.abspath(out_file)} file")

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
        plt.plot(time, self.data, label="Left channel")
        #plt.plot(time, self.data[:, 1], label="Right channel")
        plt.legend()
        plt.xlabel("Time [s]")
        plt.ylabel("Amplitude")
        plt.show()

    def get_sample_rate(self):
        return self.stream.samplerate

    def get_nframes(self):
        return self.stream.frames

    def run_cmd(self, command):
        print(f"Running command: {command}")
        popen = subprocess.Popen(command,
            stdout = -1, stderr=-1, stdin=-1, shell=True, encoding='utf-8',
            #cwd=self.tmp
            )
        out, err = popen.communicate()
        return out, err, popen.returncode

    def rw_by_ffmprg(self, out_file):
        """Read and write wav file via ffmpeg tool"""
        out_file = os.path.join(self.tmp, out_file)
        print(f"{self.executable} -i {self.file} -o {out_file}")
        if os.path.isfile(out_file):
            os.remove(out_file)
        cmd = f"{self.executable} -i {os.path.abspath(self.file)} -f wav {out_file}"
        out, err, returncode = self.run_cmd(cmd)
        #with open(f'{os.path.basename(self.file)}_ffmpeg', 'w') as f:
        #    f.write(out)
        #    f.write(err)
        if returncode == 0 and os.path.isfile(out_file):
            print(f"Regenerated {out_file_to_in} by ffmpeg")
            self.file = out_file

    def resampling_by_ffmperg(self, rate, file_=sys.stdout):
        """Changing sample rate by ffmpeg tool"""
        out_file  = f'resapled_{os.path.basename(self.file)}_{rate}.wav'
        out_file = os.path.join(self.tmp, out_file)
        if os.path.isfile(out_file):
            os.remove(out_file)
        cmd = f"{self.executable} -i {self.file} -ar {rate} {out_file}"
        out, err, returncode = self.run_cmd(cmd)
        if returncode == 0:
            self.file = out_file
            print(f"Created {os.path.abspath(out_file)}")
        else:
            print(out, err, file=file_)
