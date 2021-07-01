
import scipy.io.wavfile
import os
import numpy as np
import matplotlib.pyplot as plt
import wave
import scipy.signal as sps
import shlex
import subprocess
import soundfile

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
    executable = os.path.abspath(os.path.join('.', 'ffmpeg', 'bin', 'ffmpeg.exe'))

    def __init__(self, path):
        self.data = np.array([])
        self._is_wav_format = False
        self.file = path
        self.rate = -1
        self.stream = None 
        self.frame = None 
        self.frames = None
        self.length = None
        self.frame_size_in_ms = 0.01
        self.nptype = None
        self.out_file = 'm_' + os.path.basename(self.file)
        self.tmp = 'tmp_1'

    @staticmethod
    def chunks(data, size):
        """
        Yields chunks of size k from a given list.
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
            raise OSError(f"Error: Audio file is not found: {self.file}")
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

    def resample(self, rate):
        """
        Resampling inputed wav file by given sample rate

        parameters
        ----------
            rate : int
                sample rate
        """
        #self.out_stream = wave.open(self.out_file, 'w')
        #self.out_stream.setframerate(rate)
        #self.out_stream.setnchannels(self.stream.channels)
        #self.out_stream.setsampwidth (self.stream.getsampwidth())
        #self.out_stream.setnframes(1)
        #audio = self.stream.readframes(self.stream.getnframes())
        #nroutsamples = round(len(audio) * rate/self.get_sample_rate())
        #print("Nr output samples: %d" %  nroutsamples)
        ##audio_out = sps.resample(np.fromstring(audio, self.nptype), nroutsamples)
        #audio_formatter = np.fromstring(audio, np.uint16)
        #audio_out = sps.resample(audio_formatter, len(audio_formatter))
        #audio_out = audio_out.astype(np.uint16)
        #self.out_stream.writeframes(audio_out.copy(order='C'))
        #self.out_stream.close()


    def resampling(self, rate):
        """
        Resampling inputed wav file by given sample rate

        parameters
        ----------
            rate : int
                sample rate
        """
        n_of_samples = round(len(self.data) * rate/self.rate)
        new_data = sps.resample(self.data, n_of_samples)
        out_file_to_in = f"{self.tmp}\\{self.out_file}"
        with soundfile.SoundFile(out_file_to_in, 'w', rate, 1, 'PCM_24') as file_:
            file_.write(new_data)
        print(f"Created {self.out_file} file")
        if os.path.isfile(self.out_file):
            self.file = out_file_to_in
            print(f"Created {os.path.abspath(out_file_to_in)}")

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
            #cwd='tmp_1'
            )
        out, err = popen.communicate()
        return out, err, popen.returncode

    def rw_by_ffmprg(self, out_file):
        """Read and write wav file via ffmpeg tool"""
        out_file_to_in = os.path.join(self.tmp, out_file)
        if os.path.isfile(self.executable):
            print(f"{self.executable} -i {self.file} -o {out_file_to_in}")
            if os.path.isfile(out_file_to_in):
                os.remove(out_file_to_in)
            cmd = f"{self.executable} -i {os.path.abspath(self.file)} -f wav {out_file_to_in}"
            out, err, returncode = self.run_cmd(cmd)
            with open(f'{os.path.basename(self.file)}_ffmpeg', 'w') as f:
                f.write(out)
                f.write(err)
            if returncode == 0 and os.path.isfile(out_file_to_in):
                print(f"Regenerated {out_file_to_in} by ffmpeg")
                self.in_file = out_file_to_in
        else:
            print(f"Error: {self.executable} is not found!")

    #def change_sample_rate_by_ffmprg(self, rate):
    def resampling_by_ffmperg(self, rate):
        """Changing sample rate by ffmpeg tool"""
        out_file_to_in = f'resampled_{os.path.basename(self.file)}_{rate}.wav'
        if os.path.isfile(self.executable):
            if os.path.isfile(out_file_to_in):
                os.remove(out_file_to_in)
            cmd = f"{self.executable} -i {self.file} -ar {rate} {out_file_to_in}"
            out, err, returncode = self.run_cmd(cmd)
            if returncode == 0:
                self.file = out_file_to_in
                print(f"Created {os.path.abspath(out_file_to_in)}")
            else:
                print(out, err)
        else:
            print(f"Error: {executable} is not found!")

def test(file_):
    po = ProcessAudio(file_)
    try:
        po.read()
        print(po.get_nframes())
        print(po.get_sample_rate())
        po.resample(60000)
        print(po.compute_energy())
        print(po.compute_short_term_energy())
    except BaseException as b_e:
        print(b_e)
    po.rw_by_ffmprg('new_'+os.path.basename(po.file))
    po.read()
    print(po.rate)

def test1(file_):
    po = ProcessAudio(file_)
    #po.rw_by_ffmprg('new_'+os.path.basename(po.file))
    po.read()
    print(po.get_nframes())
    print(po.get_sample_rate())
    po.resampling(60000)
    print(po.compute_energy())
    print(po.compute_short_term_energy())
    print(po.rate)
    #po.plot()

def test2(file_):
    po = ProcessAudio(file_)
    #po.rw_by_ffmprg('new_'+os.path.basename(po.file))
    po.read()
    print(po.get_nframes())
    print(po.get_sample_rate())
    po.change_sample_rate_by_ffmprg(100000)
    #po.resampling(100000)
    po.file = po.out_file
    po.read()
    print(po.get_nframes())
    print(po.get_sample_rate())
    print(po.rate)
    #po.plot()

def test3(file_):
    po = ProcessAudio(file_)
    po.read()
    print(po.compute_energy())
    po.change_sample_rate_by_ffmprg(100000)
    po.read()
    print(po.compute_energy())

file_ = os.path.join("./tests", "sample_data", "data", "English.wav")
#test3(file_)
#test("m_English.wav")
file1_ = "tests\\sample_data\\data\\nistwav_signed16bPCM_8k_mono.wav"
#test1(file1_)
file2 = "tests\\sample_data\\data\\nistwav_signed32bPCM_44.1k_mono.wav"
file3 = "tests\\sample_data\\voices\\audios\\4.wav"
#test1(file2)
#test1(file1_)


def test_up_or_down_sampling(file, sign):
    wav_obj = ProcessAudio(file)
    wav_obj.read()
    energy = wav_obj.compute_energy()
    print(energy)
    wav_obj.resampling(eval(f"{wav_obj.rate} {sign} 10000"))
    wav_obj.read()
    energy_after_resampling = wav_obj.compute_energy()
    print(energy_after_resampling)
    breakpoint()
    sub = energy - energy_after_resampling
    print(abs(sub) >= 0  and abs(sub) < 1 )


#test_up_or_down_sampling(file2, '+')