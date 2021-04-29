#!/usr/bin/python3

import numpy as np
import sys
from scipy.io.wavfile import read, write

def delay(signal ,frameShift):
	newSignal = np.zeros_like(signal)
	delayBuffer = np.zeros(frameShift)
	bufferFull = 0
	frameCounter = 0
	for i in signal:
		if bufferFull == 0:
			newSignal[frameCounter] = i
			delayBuffer[frameCounter] = newSignal[frameCounter]
		elif bufferFull == 1:
			if frameCounter <= signal.shape[0]:
				newSignal[frameCounter] = i + (1/2)*delayBuffer[0]
				delayBuffer = np.delete(delayBuffer, [0])
				np.append(delayBuffer, newSignal[frameCounter])
			else:
				while delayBuffer.shape[0] >= 1:
					np.append(newSignal, (1/2)*delayBuffer[0])
					delayBuffer = np.delete(delayBuffer, [0])

	return newSignal

samplerate, audio = read(sys.argv[1])
try:
	nchannel = audio.shape[1]
except:
	nchannel = 1

#if nchannel == 1:
#    signal = audio.readframes(-1)
#    signal = np.fromstring(signal, 'int16')
#    samplerate, data = read(sys.argv[1])
if nchannel == 2:
    print('Ficheros estereo aun no están soportados')
    sys.exit(0)

delaytime = int(sys.argv[2])
fs = (delaytime/1000) * samplerate
finalAudio = delay(audio, fs)

