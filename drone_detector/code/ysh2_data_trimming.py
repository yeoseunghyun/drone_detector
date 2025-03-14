# -*- coding: utf-8 -*-
"""Data_Trimming.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1pI52knQtsy-8hhTyZ_8PNDLS4K70HFvK
"""

# Commented out IPython magic to ensure Python compatibility.
import numpy as np
import random
import librosa
import matplotlib.pyplot as plt
import csv
import pandas as pd
import os
import random
import math

# %matplotlib inline

# Trim 할 오디오가 있는 폴더와 csv 파일 경로

# Trim 한 오디오를 저장할 폴더와 csv 파일 경로

#name = ['1', 'ps1_1', 'ps1_2', 'ps2_1', 'ps2_2', 'ts_2']
#name =['test_1']
name = ['1','2' ,'ps1_1', 'ps1_2', 'ps2_1', 'ps2_2','ts_1' ,'ts_2']

SR = 44100
OVERLAP = 0 #second
DURATION = 0.4 #second


def load_audio_file(file_path):
    data = librosa.core.load(file_path, sr = SR)[0] #, sr=44100

    return data

def save_newfile(y, name, label):
    #change this path to yours
    path = Trim_dataDir

    mid = int(len(y) / 2)
    l_data = y[:mid]
    r_data =  y[mid:]
    #audio time series split iterate 하기
    output_length = SR * DURATION
    stride = OVERLAP * SR
    i = 0
    left_duration = len(y) / 2 - output_length + stride

    while(left_duration >= stride):
        data1 = l_data[int(stride * i) : int(output_length + stride * i)]
        data2 = r_data[int(stride * i) : int(output_length + stride * i)]
        data3 = np.append(data1, data2)

        librosa.output.write_wav(path + "/" + name + "_" + str(i) + ".wav", data3, SR)
        left_duration = left_duration - stride  
        i = i + 1

    # i 개 중 30%만 뽑기
    numlist = []
    for j in range(i):
        numlist.append(j)
    
    sample_ratio = math.floor(i * 0.3) #30%
    s = random.sample(numlist, sample_ratio)

    #print(numlist)
    #print(s)


    f = open(Trim_csvPath, 'a', encoding='utf-8', newline='')
    wr = csv.writer(f)

    for k in range(i): ##fold 지정하기 0, 1 총 i개 중 30퍼만 validation set으로.
        if k in s:
            fold = '1' #validation set
        else:
            fold = '0'
        
        wr.writerow([name + "_" + str(k), label, fold])

    f.close()

for path in name:

    dataDir = '/home/stealthdrone/Desktop/dataset/Drone_audio_'+path
    csvPath = '/home/stealthdrone/Desktop/csv/Drone_audio_'+path+'.csv'
    Trim_dataDir = '/home/stealthdrone/Desktop/dataset/' + str(DURATION) + 'Trimmed_audio_' + path
    Trim_csvPath = '/home/stealthdrone/Desktop/csv/' + str(DURATION) + 'Trimmed_audio_' + path + '.csv'



    #data dir iteration
    metadata = pd.read_csv(csvPath, sep=",")
    metadata = metadata.sort_values(by=['filename'])
    metadata = metadata.reset_index(drop=True)
    metadata

    fileList = np.sort(np.array([x.split(".wav") for x in os.listdir(dataDir)])[:,0])

    fileDic = dict([(fileList[x],x) for x in range(len(fileList))])

    for i in os.listdir(dataDir):
        try:
            name = i.split(".wav")[0]
            location = fileDic[name]
            #print(name)
            ##1. load
            y = load_audio_file(dataDir + "/" + i)

            sound_type = metadata.loc[location]["class"]
            save_newfile(y, name, sound_type)

        except:
            continue
