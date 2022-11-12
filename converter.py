import numpy as np
import pandas as pd
from scipy.io.wavfile import write
import os
from os.path import isfile, join
from pathlib import Path

input_path = './csv'
output_path = './wav'

Path(input_path).mkdir(exist_ok=True)
Path(output_path).mkdir(exist_ok=True)

input_files_basenames = [os.path.splitext(f)[0] for f in os.listdir(input_path) if isfile(join(input_path, f)) and f.endswith('.csv')]

samplerate = 250
amplitude = np.iinfo(np.int16).max
axiis = ['x', 'y', 'z']

if len(input_files_basenames) == 0:
    print(f"No files found in {input_path} folder")
    exit(1)

for file_basename in input_files_basenames:
    csv_file_path = os.path.join(input_path, f"{file_basename}.csv")
    imu_signals = pd.read_csv(csv_file_path, header=None, sep=',', names=['timestamp', 'crap', 'x', 'y', 'z', 'more_crap', 'u', 'v', 'w'])

    for axis in axiis:
        wav_file_path = os.path.join(output_path, f"{file_basename}-{axis}.wav")
        print(f"Writing {wav_file_path}")
        imu_axis = imu_signals[axis] * amplitude
        write(wav_file_path, samplerate, imu_axis.astype(np.int16))
