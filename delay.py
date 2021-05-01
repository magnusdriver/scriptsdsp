#!/usr/bin/python3

import numpy as np
import sys
from scipy.io.wavfile import read, write

# Función que realiza el efecto de retardo.
def delay(signal ,frameShift):
	newSignal = np.zeros_like(signal)
	delayBuffer = np.zeros(frameShift)
	bufferFull = 0 # Variable que controla el estado del buffer.
	frameCounter = 0 # Variable índice de las muestras de la señal.
	for i in signal:
		if bufferFull == 0:
			# Se lee la señal y se añade a la nueva señal y al buffer hasta que este se llena.
			newSignal[frameCounter] = i
			delayBuffer[frameCounter] = newSignal[frameCounter]
		elif bufferFull == 1:
			if frameCounter <= signal.shape[0]:
				# Con el buffer lleno se sigue leyendo la señal y a esta se empieza a sumar lo que tenemos en el buffer.
				# En el buffer se va eliminando la primera muestra y se añade la actual al final de este.
				newSignal[frameCounter] = i + (2/3)*delayBuffer[0]
				delayBuffer = np.delete(delayBuffer, [0])
				delayBuffer = np.append(delayBuffer, [newSignal[frameCounter]])
			else:
				while delayBuffer.shape[0] > 1:
					# Cuando termina la señal de entrada, se añade a la señal final lo que había en el buffer y termina la función.
					newSignal = np.append(newSignal, (2/3)*delayBuffer[0])
					delayBuffer = np.delete(delayBuffer, [0])
		frameCounter += 1
		if frameCounter == frameShift:
			bufferFull = 1

	return newSignal

samplerate, audio = read(sys.argv[1]) # El fichero .wav que se lee se toma del primer argumento.
try:
	nchannel = audio.shape[1]
except:
	nchannel = 1

if nchannel == 2:
    print('Ficheros estereo aun no están soportados')
    sys.exit(0)

delaytime = int(sys.argv[2]) # El tiempo de delay en ms se toma del segundo argumento.
fs = (delaytime/1000) * samplerate # cálculo del número de muestradas desplazadas según el tiempo y la frecuencia de muestreo.
finalAudio = delay(audio, int(fs))
write("salida.wav", samplerate, finalAudio) # El audio resultante se guarda en el archivo salida.wav
