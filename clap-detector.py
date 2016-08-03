
import pyaudio
import audioop
import sys

class ClapDetector():
    #TODO:Could I eventually use a nerual network/other magic to auto adjust the settings to good levels
    def __init__(self):
        self.quietcount = 0
        self.block_counter = 0
        self.clap_counter = 0
        self.noisycount = 0
        self.rate = 44100
        self.block_time = 0.05
        self.clap_length = 0.1/self.block_time
        self.pattern_limit = 3/self.block_time #number of blocks in 3 secs
        self.patterns = {2:'Do something', 3:'Do something else'}
        self.block = int(self.rate*self.block_time)
        self.pa = pyaudio.PyAudio()
        self.stream = self.start_stream()
        self.background_level = self.listen_to_background()



    def start_stream( self ):
        stream = self.pa.open(   format = pyaudio.paInt16,
                                 channels = 1,
                                 rate = 44100,
                                 input = True,
                                 input_device_index = None,
                                 frames_per_buffer = self.block)

        return stream

    def stop(self):
        self.stream.close()

    def listen_to_background(self):
        #try to detect how loud background is.
        print('calibrating')
        rms_values = []
        for i in range(10):
            try:
                block = self.stream.read(self.block*20) #1 second sample
                rms_values.append(audioop.rms(block, 2))
            except IOError as e:
                i -= 1
        return max(rms_values)

    def clapDetected(self):
        print('CLAP!')

    def detect_pattern(self):
        #do some action if a certain number of claps are detected in a period of time
        if self.clap_counter in self.patterns.keys():
            print(self.patterns[self.clap_counter])

    def listen(self):
        try:
            block = self.stream.read(self.block)
        except IOError as e:
            print('error')
            return
        amplitude = audioop.rms(block, 2 )
        if self.block_counter >= self.pattern_limit:
            self.detect_pattern()
            self.clap_counter = 0
            self.block_counter = 0


        if amplitude > self.background_level * 2:
            # noisy
            self.noisycount += 1
            if self.noisycount  > 3/self.block_time :
                #we've had 3 seconds of noise, maybe background is louder. Recalibrate.
                self.background_level = self.listen_to_background() #TODO:Recalibrate on separate thread.
                self.noisycount = 0
        else:
            # quiet
            self.quietcount += 1
            if 1 <= self.noisycount <= self.clap_length:
                #we just had a period of noisy blocks which match the length of a clap
                self.clap_counter += 1
                self.clapDetected()
            self.noisycount = 0
        self.block_counter += 1
