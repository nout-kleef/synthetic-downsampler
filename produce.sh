#!/bin/bash

SYNTHETIC_ROOT='/Users/nout/github/piunet/synthetic'

# baseline
# python synthetic-downsampler/create_data.py ~/datasets/piunet_probav/probav_data "${SYNTHETIC_ROOT}/probav_data1" 100 0.5 30
# A
python synthetic-downsampler/create_data.py ~/datasets/piunet_probav/probav_data "${SYNTHETIC_ROOT}/probav_data_A" 50 0.5 30
zip -r "${SYNTHETIC_ROOT}/probav_data_A.zip" "${SYNTHETIC_ROOT}/probav_data_A"
# B
python synthetic-downsampler/create_data.py ~/datasets/piunet_probav/probav_data "${SYNTHETIC_ROOT}/probav_data_B" 100 0.25 30
zip -r "${SYNTHETIC_ROOT}/probav_data_B.zip" "${SYNTHETIC_ROOT}/probav_data_B"
# # C
python synthetic-downsampler/create_data.py ~/datasets/piunet_probav/probav_data "${SYNTHETIC_ROOT}/probav_data_C" 100 0.5 15
zip -r "${SYNTHETIC_ROOT}/probav_data_C.zip" "${SYNTHETIC_ROOT}/probav_data_C"
