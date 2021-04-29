#!/usr/bin/python3

import matplotlib.pyplot as plt
import numpy as np
import wave
from scipy.io.wavfile import read
import sys
from scipy.fft import fft, fftfreq, ifft

print('Análisis de', str(sys.argv[1]))

audio = wave.open(sys.argv[1], 'r')
nchannel = audio.getnchannels()

if nchannel == 1:
	signal = audio.readframes(-1)
	signal = np.fromstring(signal, 'int16')
	samplerate, data = read(sys.argv[1])
elif nchannel == 2:
	print('Ficheros estereo aun no están soportados')
	sys.exit(0)
	
N = len(data)
T = 1/samplerate
time = np.arange(0, T*N, T)
nSample = np.arange(0, samplerate)

#Muestra de señal continua
plt.figure(1)
plt.title("Señal wav...")
plt.plot(time, signal)
plt.xlabel('Tiempo (s)')
plt.ylabel('Amplitud')
plt.show()

#Muestra de señal discreta
plt.stem(nSample, signal[0:samplerate], use_line_collection=True)
plt.xlabel('Muestras')
plt.ylabel('Amplitud')
plt.show()

signalf = fft(signal)
xf = fftfreq(N, T)[:N//2]
#plt.plot(signalf)
#plt.grid()
#plt.show()
plt.plot(xf, 2.0/N * np.absolute(signalf[0:N//2]))
plt.xlabel('Frecuencia (Hz)')
plt.grid()
plt.show()

sines = []

sintime = np.linspace(0, 0.05, 2 * samplerate, endpoint=False)
for z in range(6000):
	if signalf[z].real > 2e+6:
		sines.append(signalf[z].real*np.sin(2*np.pi*z*sintime))
for z in sines:
	plt.plot(sintime, z)

#plt.plot(signalf)
plt.show()

print(xf)
print(signalf)
