#!/bin/bash

PROGRAM='synthetic-downsampler/create_data.py'
AUTHENTIC_ROOT='~/datasets/piunet_probav/probav_data/'
SYNTHETIC_ROOT='~/datasets/probav-synthetic/'

# baseline
python $PROGRAM $AUTHENTIC_ROOT "${SYNTHETIC_ROOT}probav_data1" 100 0.5 30
# A
python $PROGRAM $AUTHENTIC_ROOT "${SYNTHETIC_ROOT}probav_data_A" 50 0.5 30
# B
python $PROGRAM $AUTHENTIC_ROOT "${SYNTHETIC_ROOT}probav_data_B" 100 0.25 30
# C
python $PROGRAM $AUTHENTIC_ROOT "${SYNTHETIC_ROOT}probav_data_C" 100 0.5 15
