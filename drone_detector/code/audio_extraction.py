# -*- coding: utf-8 -*-
"""Audio_Extraction.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1rf8PjkYjgSwmfHZqfOPNpymYyyIczpyI

#Audio Extraction
* 녹음했던 전체 오디오 파일에서 특정 부분을 가져와 분할하고 두 녹음파일을 합쳐서 저장합니다.
"""

import librosa
import numpy as np

LEFT_AUDIO_PATH = '/home/stealthdrone/Desktop/dataset/1025/2-L.wav'
RIGHT_AUDIO_PATH = '/home/stealthdrone/Desktop/dataset/1025/2-R.wav'

SR = 44100
PATH = '/home/stealthdrone/Desktop/dataset/Drone_audio_test_1'

def min2sec(time): # 09:02:43

    minute = int(time.split(':')[0])
    second = int(time.split(':')[1])
    milisec = int(time.split(':')[2])

    return minute * 60 + second + milisec / 100

left_audio = librosa.core.load(LEFT_AUDIO_PATH, sr = SR)[0]
right_audio = librosa.core.load(RIGHT_AUDIO_PATH, sr = SR)[0]

"""
#1 -balanced
left_start = ['03:22:00','03:52:00', '04:19:00', '04:45:00',
              '05:43:00', '06:18:00', '06:50:00','07:09:00', 
              '07:54:00','08:31:00','08:58:00', '09:20:00']
left_end = ['03:25:00','03:55:00', '04:22:00','04:55:00','05:45:00', '06:20:00',
            '06:52:00','07:15:00', '07:58:00','08:35:00','09:02:00', '09:33:00']
nameList = ['1-1', '1-2', '1-3','1-h', 
            '2-1', '2-2', '2-3', '2-h',
            '3-1', '3-2', '3-3', '3-h']
time_diff = 0.4


"""
#2 -balanced
"""
left_start = ['03:53:00','04:27:00', '04:53:00','05:12:00','05:51:00', '06:20:00', '06:50:00','07:10:00', '07:45:00',              '08:18:00','08:49:00', '09:09:00']
left_end = ['03:56:00','04:30:00', '04:56:00','05:20:00','05:55:00', '06:24:00',
            '06:54:00','07:21:00', '07:48:00','08:21:00','08:52:00', '09:19:00']
time_diff = 0.1
nameList = ['(2)1-1', '(2)1-2', '(2)1-3','(2)1-h',
            '(2)2-1', '(2)2-2', '(2)2-3', '(2)2-h',
            '(2)3-1', '(2)3-2', '(2)3-3', '(2)3-h']
"""

#testset
left_start = ['09:49:00', '10:03:00', '10:19:00', '10:37:00', '11:12:00', '11:42:00', '12:38:00', '13:12:00' ]
left_end = ['9:54:00', '10:07:00', '10:31:00', '10:48:00', '11:23:00', '11:65:00', '12:50:00', '13:24:00']

time_diff = 0.1
nameList=['3to1_across_1','1to3_across_1', '3to1_across_2', '1to3_across_2',
        '3to1_diag_1', '3to1_diag_2', '1to3_diag_1', '1to3_diag_2']
        

for i in range(len(left_start)):
      duration = min2sec(left_end[i]) - min2sec(left_start[i])
      print(nameList[i], duration)

for i in range(len(left_start)):

    l_start = int(min2sec(left_start[i]) * SR)
    l_end = int(min2sec(left_end[i]) * SR)
    data1 = left_audio[l_start:l_end]

    r_start = int((min2sec(left_start[i]) + time_diff) * SR)
    r_end = int((min2sec(left_end[i]) + time_diff) * SR)
    data2 = right_audio[r_start:r_end]

    data3 = np.append(data1, data2)
    print(nameList[i], int(len(data3) / SR))
    librosa.output.write_wav(PATH + "/" + nameList[i] + ".wav", data3, SR)
