| split | condition | regime | reference mode | recordings | seeds | comparison-minutes (all seeds) | added/min | interval | removed/min | interval | detections before (unique) | kept (all seeds) | kept fraction | interval | kept in every seed | max score change |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| train | gain +6 dB | R1 |  | 145 | [1] | 65.3 | 0.199 | 95% [0.093, 0.321] | 0.184 | 95% [0.031, 0.408] | 198 | 195/198 | 0.985 | 95% [0.965, 1] | 195/198 | 5.92 |
| train | gain +6 dB | R2 | single | 22 | [1] | 11.9 | 0 | 95% [0, 0.31] | 0 | 95% [0, 0.31] | 8 | 8/8 | 1 | degenerate [1, 1] (no spread across the resampled clusters) | 8/8 | 0.146 |
| train | gain -6 dB | R1 |  | 145 | [1] | 65.3 | 0.0918 | 95% [0.03, 0.182] | 0.107 | 95% [0.031, 0.201] | 198 | 196/198 | 0.99 | 95% [0.974, 1] | 196/198 | 7.46 |
| train | gain -6 dB | R2 | single | 22 | [1] | 11.9 | 0 | 95% [0, 0.31] | 0 | 95% [0, 0.31] | 8 | 8/8 | 1 | degenerate [1, 1] (no spread across the resampled clusters) | 8/8 | 9.8 |
| train | low-pass 3.4 kHz | R1 |  | 145 | [1] | 65.3 | 1.61 | 95% [1.31, 1.95] | 0.49 | 95% [0.27, 0.737] | 198 | 192/198 | 0.97 | 95% [0.942, 0.99] | 192/198 | 7.65 |
| train | low-pass 3.4 kHz | R2 | single | 22 | [1] | 11.9 | 0 | 95% [0, 0.31] | 0.0842 | 95% [0, 0.263] | 8 | 7/8 | 0.875 | 95% [0.5, 1] | 7/8 | 9.81 |
| train | white noise 20 dB SNR | R1 |  | 145 | [1, 2, 3] | 196 | 2.39 | 95% [1.83, 3.07] | 1.01 | 95% [0.659, 1.4] | 198 | 525/594 | 0.884 | 95% [0.839, 0.922] | 171/198 | 10.2 |
| train | white noise 20 dB SNR | R2 | single | 22 | [1, 2, 3] | 35.6 | 0 | 95% [0, 0.31] | 0.589 | 95% [0.174, 1.09] | 8 | 18/24 | 0.75 | 95% [0.429, 1] | 6/8 | 9.91 |
| train | MP3 64 kbit/s | R1 |  | 145 | [1] | 65.3 | 0.0765 | 95% [0.015, 0.151] | 0.0612 | 95% [0.015, 0.126] | 198 | 195/198 | 0.985 | 95% [0.966, 1] | 195/198 | 2.11 |
| train | MP3 64 kbit/s | R2 | single | 22 | [1] | 11.9 | 0.0842 | 95% [0, 0.26] | 0 | 95% [0, 0.31] | 8 | 8/8 | 1 | degenerate [1, 1] (no spread across the resampled clusters) | 8/8 | 0.761 |
| train | dynamic-range compression | R1 |  | 145 | [1] | 65.3 | 2.94 | 95% [2.47, 3.49] | 1.32 | 95% [0.98, 1.67] | 198 | 157/198 | 0.793 | 95% [0.724, 0.851] | 157/198 | 14.2 |
| train | dynamic-range compression | R2 | single | 22 | [1] | 11.9 | 0 | 95% [0, 0.31] | 0.421 | 95% [0.082, 0.905] | 8 | 4/8 | 0.5 | 95% [0.111, 0.875] | 4/8 | 1.27 |
| train | room reverb RT60 0.4 s | R1 |  | 145 | [1, 2, 3] | 196 | 0.964 | 95% [0.711, 1.24] | 0.633 | 95% [0.39, 0.895] | 198 | 563/594 | 0.948 | 95% [0.912, 0.976] | 184/198 | 12 |
| train | room reverb RT60 0.4 s | R2 | single | 22 | [1, 2, 3] | 35.6 | 0.365 | 95% [0.056, 0.754] | 0.73 | 95% [0.253, 1.3] | 8 | 15/24 | 0.625 | 95% [0.142, 1] | 5/8 | 9.34 |
| train | phone band + mu-law (participant only) | R1 |  | 145 | [1] | 65.3 | 1.99 | 95% [1.63, 2.35] | 0.735 | 95% [0.428, 1.11] | 198 | 185/198 | 0.934 | 95% [0.898, 0.966] | 185/198 | 10.5 |
| train | phone band + mu-law (participant only) | R2 | single | 22 | [1] | 11.9 | 0.0842 | 95% [0, 0.26] | 0.253 | 95% [0, 0.569] | 8 | 6/8 | 0.75 | 95% [0.375, 1] | 6/8 | 9.86 |
| train | WORLD speaker transform | R1 |  | 145 | [1] | 65.3 | 0.52 | 95% [0.346, 0.695] | 0.428 | 95% [0.225, 0.692] | 198 | 193/198 | 0.975 | 95% [0.951, 0.995] | 193/198 | 6.11 |
| train | WORLD speaker transform | R2 | single | 22 | [1] | 11.9 | 0 | 95% [0, 0.31] | 0.337 | 95% [0.083, 0.66] | 8 | 6/8 | 0.75 | 95% [0.429, 1] | 6/8 | 0.739 |
| train | babble 10 dB SNR | R1 |  | 145 | [1, 2, 3] | 196 | 30.4 | 95% [28.2, 32.4] | 2.71 | 95% [2.21, 3.23] | 198 | 359/594 | 0.604 | 95% [0.509, 0.691] | 93/198 | 33.8 |
| train | babble 10 dB SNR | R2 | single | 22 | [1, 2, 3] | 35.6 | 0.982 | 95% [0.656, 1.47] | 1.46 | 95% [0.8, 2.19] | 8 | 1/24 | 0.0417 | 95% [0, 0.111] | 0/8 | 25.7 |
| train | babble 20 dB SNR | R1 |  | 145 | [1, 2, 3] | 196 | 13.6 | 95% [12, 15.2] | 0.969 | 95% [0.666, 1.31] | 198 | 522/594 | 0.879 | 95% [0.826, 0.919] | 156/198 | 23.5 |
| train | babble 20 dB SNR | R2 | single | 22 | [1, 2, 3] | 35.6 | 0.112 | 95% [0, 0.311] | 1.09 | 95% [0.557, 1.69] | 8 | 5/24 | 0.208 | 95% [0, 0.481] | 1/8 | 2.6 |
| val | gain +6 dB | R1 |  | 58 | [1] | 28.9 | 0.208 | per speaker: eisenhower_farewell_1961 0.346, lbush_radio_2001 0.069; range [0.069, 0.346] | 0.0347 | per speaker: eisenhower_farewell_1961 0.069, lbush_radio_2001 0; range [0, 0.069] | 73 | 73/73 | 1 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1; range [1, 1] | 73/73 | 0.835 |
| val | gain -6 dB | R1 |  | 58 | [1] | 28.9 | 0.277 | per speaker: eisenhower_farewell_1961 0.415, lbush_radio_2001 0.139; range [0.139, 0.415] | 0.104 | per speaker: eisenhower_farewell_1961 0.138, lbush_radio_2001 0.069; range [0.069, 0.138] | 73 | 73/73 | 1 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1; range [1, 1] | 73/73 | 2.86 |
| val | low-pass 3.4 kHz | R1 |  | 58 | [1] | 28.9 | 0.381 | per speaker: eisenhower_farewell_1961 0.484, lbush_radio_2001 0.278; range [0.278, 0.484] | 0.416 | per speaker: eisenhower_farewell_1961 0.623, lbush_radio_2001 0.208; range [0.208, 0.623] | 73 | 70/73 | 0.959 | per speaker: eisenhower_farewell_1961 0.973, lbush_radio_2001 0.944; range [0.944, 0.973] | 70/73 | 5.61 |
| val | white noise 20 dB SNR | R1 |  | 58 | [1, 2, 3] | 86.6 | 2.63 | per speaker: eisenhower_farewell_1961 1.96, lbush_radio_2001 3.31; range [1.96, 3.31] | 0.739 | per speaker: eisenhower_farewell_1961 0.6, lbush_radio_2001 0.879; range [0.6, 0.879] | 73 | 199/219 | 0.909 | per speaker: eisenhower_farewell_1961 0.928, lbush_radio_2001 0.889; range [0.889, 0.928] | 64/73 | 10.1 |
| val | MP3 64 kbit/s | R1 |  | 58 | [1] | 28.9 | 0.0693 | per speaker: eisenhower_farewell_1961 0.138, lbush_radio_2001 0; range [0, 0.138] | 0.0693 | per speaker: eisenhower_farewell_1961 0.138, lbush_radio_2001 0; range [0, 0.138] | 73 | 73/73 | 1 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1; range [1, 1] | 73/73 | 0.527 |
| val | dynamic-range compression | R1 |  | 58 | [1] | 28.9 | 6.48 | per speaker: eisenhower_farewell_1961 8.03, lbush_radio_2001 4.93; range [4.93, 8.03] | 1.56 | per speaker: eisenhower_farewell_1961 1.94, lbush_radio_2001 1.18; range [1.18, 1.94] | 73 | 57/73 | 0.781 | per speaker: eisenhower_farewell_1961 0.757, lbush_radio_2001 0.806; range [0.757, 0.806] | 57/73 | 18.5 |
| val | room reverb RT60 0.4 s | R1 |  | 58 | [1, 2, 3] | 86.6 | 0.889 | per speaker: eisenhower_farewell_1961 0.969, lbush_radio_2001 0.81; range [0.81, 0.969] | 0.635 | per speaker: eisenhower_farewell_1961 0.784, lbush_radio_2001 0.486; range [0.486, 0.784] | 73 | 208/219 | 0.95 | per speaker: eisenhower_farewell_1961 0.964, lbush_radio_2001 0.935; range [0.935, 0.964] | 68/73 | 14.7 |
| val | phone band + mu-law (participant only) | R1 |  | 58 | [1] | 28.9 | 1.84 | per speaker: eisenhower_farewell_1961 2.91, lbush_radio_2001 0.764; range [0.764, 2.91] | 0.624 | per speaker: eisenhower_farewell_1961 0.623, lbush_radio_2001 0.625; range [0.623, 0.625] | 73 | 65/73 | 0.89 | per speaker: eisenhower_farewell_1961 0.946, lbush_radio_2001 0.833; range [0.833, 0.946] | 65/73 | 6.17 |
| val | WORLD speaker transform | R1 |  | 58 | [1] | 28.9 | 0.936 | per speaker: eisenhower_farewell_1961 1.45, lbush_radio_2001 0.417; range [0.417, 1.45] | 0.485 | per speaker: eisenhower_farewell_1961 0.692, lbush_radio_2001 0.278; range [0.278, 0.692] | 73 | 70/73 | 0.959 | per speaker: eisenhower_farewell_1961 0.973, lbush_radio_2001 0.944; range [0.944, 0.973] | 70/73 | 14.8 |
| val | babble 10 dB SNR | R1 |  | 58 | [1, 2, 3] | 86.6 | 24.5 | per speaker: eisenhower_farewell_1961 27.2, lbush_radio_2001 21.8; range [21.8, 27.2] | 2.33 | per speaker: eisenhower_farewell_1961 2.7, lbush_radio_2001 1.97; range [1.97, 2.7] | 73 | 143/219 | 0.653 | per speaker: eisenhower_farewell_1961 0.694, lbush_radio_2001 0.611; range [0.611, 0.694] | 38/73 | 26.8 |
| val | babble 20 dB SNR | R1 |  | 58 | [1, 2, 3] | 86.6 | 8.41 | per speaker: eisenhower_farewell_1961 10.6, lbush_radio_2001 6.18; range [6.18, 10.6] | 1.18 | per speaker: eisenhower_farewell_1961 1.5, lbush_radio_2001 0.856; range [0.856, 1.5] | 73 | 194/219 | 0.886 | per speaker: eisenhower_farewell_1961 0.91, lbush_radio_2001 0.861; range [0.861, 0.91] | 61/73 | 19.7 |
| test | gain +6 dB | R1 |  | 58 | [1] | 28.8 | 0.139 | per speaker: mobama_weekly_2014 0.139, nixon_resignation_1974 0.138; range [0.138, 0.139] | 0.173 | per speaker: mobama_weekly_2014 0, nixon_resignation_1974 0.346; range [0, 0.346] | 78 | 78/78 | 1 | per speaker: mobama_weekly_2014 1, nixon_resignation_1974 1; range [1, 1] | 78/78 | 3.71 |
| test | gain -6 dB | R1 |  | 58 | [1] | 28.8 | 0.278 | per speaker: mobama_weekly_2014 0.418, nixon_resignation_1974 0.138; range [0.138, 0.418] | 0.0694 | per speaker: mobama_weekly_2014 0.07, nixon_resignation_1974 0.069; range [0.069, 0.07] | 78 | 78/78 | 1 | per speaker: mobama_weekly_2014 1, nixon_resignation_1974 1; range [1, 1] | 78/78 | 15.5 |
| test | low-pass 3.4 kHz | R1 |  | 58 | [1] | 28.8 | 1.46 | per speaker: mobama_weekly_2014 2.44, nixon_resignation_1974 0.484; range [0.484, 2.44] | 0.659 | per speaker: mobama_weekly_2014 0.836, nixon_resignation_1974 0.484; range [0.484, 0.836] | 78 | 73/78 | 0.936 | per speaker: mobama_weekly_2014 0.895, nixon_resignation_1974 0.975; range [0.895, 0.975] | 73/78 | 16.6 |
| test | white noise 20 dB SNR | R1 |  | 58 | [1, 2, 3] | 86.5 | 1.85 | per speaker: mobama_weekly_2014 1.39, nixon_resignation_1974 2.31; range [1.39, 2.31] | 0.729 | per speaker: mobama_weekly_2014 0.603, nixon_resignation_1974 0.853; range [0.603, 0.853] | 78 | 213/234 | 0.91 | per speaker: mobama_weekly_2014 0.895, nixon_resignation_1974 0.925; range [0.895, 0.925] | 71/78 | 16.6 |
| test | MP3 64 kbit/s | R1 |  | 58 | [1] | 28.8 | 0.139 | per speaker: mobama_weekly_2014 0.279, nixon_resignation_1974 0; range [0, 0.279] | 0.104 | per speaker: mobama_weekly_2014 0, nixon_resignation_1974 0.207; range [0, 0.207] | 78 | 78/78 | 1 | per speaker: mobama_weekly_2014 1, nixon_resignation_1974 1; range [1, 1] | 78/78 | 11.8 |
| test | dynamic-range compression | R1 |  | 58 | [1] | 28.8 | 2.6 | per speaker: mobama_weekly_2014 2.16, nixon_resignation_1974 3.04; range [2.16, 3.04] | 1.49 | per speaker: mobama_weekly_2014 1.46, nixon_resignation_1974 1.52; range [1.46, 1.52] | 78 | 59/78 | 0.756 | per speaker: mobama_weekly_2014 0.737, nixon_resignation_1974 0.775; range [0.737, 0.775] | 59/78 | 13.2 |
| test | room reverb RT60 0.4 s | R1 |  | 58 | [1, 2, 3] | 86.5 | 0.613 | per speaker: mobama_weekly_2014 0.743, nixon_resignation_1974 0.484; range [0.484, 0.743] | 0.44 | per speaker: mobama_weekly_2014 0.186, nixon_resignation_1974 0.691; range [0.186, 0.691] | 78 | 231/234 | 0.987 | per speaker: mobama_weekly_2014 1, nixon_resignation_1974 0.975; range [0.975, 1] | 75/78 | 14.3 |
| test | phone band + mu-law (participant only) | R1 |  | 58 | [1] | 28.8 | 5.52 | per speaker: mobama_weekly_2014 2.3, nixon_resignation_1974 8.71; range [2.3, 8.71] | 0.763 | per speaker: mobama_weekly_2014 0.557, nixon_resignation_1974 0.968; range [0.557, 0.968] | 78 | 68/78 | 0.872 | per speaker: mobama_weekly_2014 0.842, nixon_resignation_1974 0.9; range [0.842, 0.9] | 68/78 | 32.1 |
| test | WORLD speaker transform | R1 |  | 58 | [1] | 28.8 | 0.763 | per speaker: mobama_weekly_2014 0.836, nixon_resignation_1974 0.691; range [0.691, 0.836] | 0.798 | per speaker: mobama_weekly_2014 0.766, nixon_resignation_1974 0.83; range [0.766, 0.83] | 78 | 77/78 | 0.987 | per speaker: mobama_weekly_2014 0.974, nixon_resignation_1974 1; range [0.974, 1] | 77/78 | 14.9 |
| test | babble 10 dB SNR | R1 |  | 58 | [1, 2, 3] | 86.5 | 26.2 | per speaker: mobama_weekly_2014 20.4, nixon_resignation_1974 31.9; range [20.4, 31.9] | 2.66 | per speaker: mobama_weekly_2014 1.81, nixon_resignation_1974 3.5; range [1.81, 3.5] | 78 | 141/234 | 0.603 | per speaker: mobama_weekly_2014 0.693, nixon_resignation_1974 0.517; range [0.517, 0.693] | 40/78 | 28.9 |
| test | babble 20 dB SNR | R1 |  | 58 | [1, 2, 3] | 86.5 | 13.2 | per speaker: mobama_weekly_2014 2.81, nixon_resignation_1974 23.6; range [2.81, 23.6] | 1.25 | per speaker: mobama_weekly_2014 0.743, nixon_resignation_1974 1.75; range [0.743, 1.75] | 78 | 200/234 | 0.855 | per speaker: mobama_weekly_2014 0.947, nixon_resignation_1974 0.767; range [0.767, 0.947] | 59/78 | 28.3 |
| val+test | gain +6 dB | R1 |  | 116 | [1] | 57.7 | 0.173 | per speaker: eisenhower_farewell_1961 0.346, lbush_radio_2001 0.069, mobama_weekly_2014 0.139, nixon_resignation_1974 0.138; range [0.069, 0.346] | 0.104 | per speaker: eisenhower_farewell_1961 0.069, lbush_radio_2001 0, mobama_weekly_2014 0, nixon_resignation_1974 0.346; range [0, 0.346] | 151 | 151/151 | 1 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1, mobama_weekly_2014 1, nixon_resignation_1974 1; range [1, 1] | 151/151 | 3.71 |
| val+test | gain -6 dB | R1 |  | 116 | [1] | 57.7 | 0.277 | per speaker: eisenhower_farewell_1961 0.415, lbush_radio_2001 0.139, mobama_weekly_2014 0.418, nixon_resignation_1974 0.138; range [0.138, 0.418] | 0.0867 | per speaker: eisenhower_farewell_1961 0.138, lbush_radio_2001 0.069, mobama_weekly_2014 0.07, nixon_resignation_1974 0.069; range [0.069, 0.138] | 151 | 151/151 | 1 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1, mobama_weekly_2014 1, nixon_resignation_1974 1; range [1, 1] | 151/151 | 15.5 |
| val+test | low-pass 3.4 kHz | R1 |  | 116 | [1] | 57.7 | 0.919 | per speaker: eisenhower_farewell_1961 0.484, lbush_radio_2001 0.278, mobama_weekly_2014 2.44, nixon_resignation_1974 0.484; range [0.278, 2.44] | 0.537 | per speaker: eisenhower_farewell_1961 0.623, lbush_radio_2001 0.208, mobama_weekly_2014 0.836, nixon_resignation_1974 0.484; range [0.208, 0.836] | 151 | 143/151 | 0.947 | per speaker: eisenhower_farewell_1961 0.973, lbush_radio_2001 0.944, mobama_weekly_2014 0.895, nixon_resignation_1974 0.975; range [0.895, 0.975] | 143/151 | 16.6 |
| val+test | white noise 20 dB SNR | R1 |  | 116 | [1, 2, 3] | 173 | 2.24 | per speaker: eisenhower_farewell_1961 1.96, lbush_radio_2001 3.31, mobama_weekly_2014 1.39, nixon_resignation_1974 2.31; range [1.39, 3.31] | 0.734 | per speaker: eisenhower_farewell_1961 0.6, lbush_radio_2001 0.879, mobama_weekly_2014 0.603, nixon_resignation_1974 0.853; range [0.6, 0.879] | 151 | 412/453 | 0.909 | per speaker: eisenhower_farewell_1961 0.928, lbush_radio_2001 0.889, mobama_weekly_2014 0.895, nixon_resignation_1974 0.925; range [0.889, 0.928] | 135/151 | 16.6 |
| val+test | MP3 64 kbit/s | R1 |  | 116 | [1] | 57.7 | 0.104 | per speaker: eisenhower_farewell_1961 0.138, lbush_radio_2001 0, mobama_weekly_2014 0.279, nixon_resignation_1974 0; range [0, 0.279] | 0.0867 | per speaker: eisenhower_farewell_1961 0.138, lbush_radio_2001 0, mobama_weekly_2014 0, nixon_resignation_1974 0.207; range [0, 0.207] | 151 | 151/151 | 1 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1, mobama_weekly_2014 1, nixon_resignation_1974 1; range [1, 1] | 151/151 | 11.8 |
| val+test | dynamic-range compression | R1 |  | 116 | [1] | 57.7 | 4.54 | per speaker: eisenhower_farewell_1961 8.03, lbush_radio_2001 4.93, mobama_weekly_2014 2.16, nixon_resignation_1974 3.04; range [2.16, 8.03] | 1.53 | per speaker: eisenhower_farewell_1961 1.94, lbush_radio_2001 1.18, mobama_weekly_2014 1.46, nixon_resignation_1974 1.52; range [1.18, 1.94] | 151 | 116/151 | 0.768 | per speaker: eisenhower_farewell_1961 0.757, lbush_radio_2001 0.806, mobama_weekly_2014 0.737, nixon_resignation_1974 0.775; range [0.737, 0.806] | 116/151 | 18.5 |
| val+test | room reverb RT60 0.4 s | R1 |  | 116 | [1, 2, 3] | 173 | 0.751 | per speaker: eisenhower_farewell_1961 0.969, lbush_radio_2001 0.81, mobama_weekly_2014 0.743, nixon_resignation_1974 0.484; range [0.484, 0.969] | 0.537 | per speaker: eisenhower_farewell_1961 0.784, lbush_radio_2001 0.486, mobama_weekly_2014 0.186, nixon_resignation_1974 0.691; range [0.186, 0.784] | 151 | 439/453 | 0.969 | per speaker: eisenhower_farewell_1961 0.964, lbush_radio_2001 0.935, mobama_weekly_2014 1, nixon_resignation_1974 0.975; range [0.935, 1] | 143/151 | 14.7 |
| val+test | phone band + mu-law (participant only) | R1 |  | 116 | [1] | 57.7 | 3.68 | per speaker: eisenhower_farewell_1961 2.91, lbush_radio_2001 0.764, mobama_weekly_2014 2.3, nixon_resignation_1974 8.71; range [0.764, 8.71] | 0.693 | per speaker: eisenhower_farewell_1961 0.623, lbush_radio_2001 0.625, mobama_weekly_2014 0.557, nixon_resignation_1974 0.968; range [0.557, 0.968] | 151 | 133/151 | 0.881 | per speaker: eisenhower_farewell_1961 0.946, lbush_radio_2001 0.833, mobama_weekly_2014 0.842, nixon_resignation_1974 0.9; range [0.833, 0.946] | 133/151 | 32.1 |
| val+test | WORLD speaker transform | R1 |  | 116 | [1] | 57.7 | 0.85 | per speaker: eisenhower_farewell_1961 1.45, lbush_radio_2001 0.417, mobama_weekly_2014 0.836, nixon_resignation_1974 0.691; range [0.417, 1.45] | 0.641 | per speaker: eisenhower_farewell_1961 0.692, lbush_radio_2001 0.278, mobama_weekly_2014 0.766, nixon_resignation_1974 0.83; range [0.278, 0.83] | 151 | 147/151 | 0.974 | per speaker: eisenhower_farewell_1961 0.973, lbush_radio_2001 0.944, mobama_weekly_2014 0.974, nixon_resignation_1974 1; range [0.944, 1] | 147/151 | 14.9 |
| val+test | babble 10 dB SNR | R1 |  | 116 | [1, 2, 3] | 173 | 25.3 | per speaker: eisenhower_farewell_1961 27.2, lbush_radio_2001 21.8, mobama_weekly_2014 20.4, nixon_resignation_1974 31.9; range [20.4, 31.9] | 2.5 | per speaker: eisenhower_farewell_1961 2.7, lbush_radio_2001 1.97, mobama_weekly_2014 1.81, nixon_resignation_1974 3.5; range [1.81, 3.5] | 151 | 284/453 | 0.627 | per speaker: eisenhower_farewell_1961 0.694, lbush_radio_2001 0.611, mobama_weekly_2014 0.693, nixon_resignation_1974 0.517; range [0.517, 0.694] | 78/151 | 28.9 |
| val+test | babble 20 dB SNR | R1 |  | 116 | [1, 2, 3] | 173 | 10.8 | per speaker: eisenhower_farewell_1961 10.6, lbush_radio_2001 6.18, mobama_weekly_2014 2.81, nixon_resignation_1974 23.6; range [2.81, 23.6] | 1.21 | per speaker: eisenhower_farewell_1961 1.5, lbush_radio_2001 0.856, mobama_weekly_2014 0.743, nixon_resignation_1974 1.75; range [0.743, 1.75] | 151 | 394/453 | 0.87 | per speaker: eisenhower_farewell_1961 0.91, lbush_radio_2001 0.861, mobama_weekly_2014 0.947, nixon_resignation_1974 0.767; range [0.767, 0.947] | 120/151 | 28.3 |
| check readers | gain +6 dB | R2 | single | 3 | [1] | 7.76 | 0 | 95% [0, 2.85] | 0 | 95% [0, 2.85] | 0 | 0/0 |  | n/a | 0/0 | 3.45 |
| check readers | gain +6 dB | R2 | consensus5 | 3 | [1] | 1.29 | 0 | 95% [0, 2.85] | 0 | 95% [0, 2.85] | 0 | 0/0 |  | n/a | 0/0 | 3.1 |
| check readers | gain -6 dB | R2 | single | 3 | [1] | 7.76 | 0 | 95% [0, 2.85] | 0 | 95% [0, 2.85] | 0 | 0/0 |  | n/a | 0/0 | 0.153 |
| check readers | gain -6 dB | R2 | consensus5 | 3 | [1] | 1.29 | 0 | 95% [0, 2.85] | 0 | 95% [0, 2.85] | 0 | 0/0 |  | n/a | 0/0 | 0.343 |
| check readers | low-pass 3.4 kHz | R2 | single | 3 | [1] | 7.76 | 0 | 95% [0, 2.85] | 0 | 95% [0, 2.85] | 0 | 0/0 |  | n/a | 0/0 | 1.19 |
| check readers | low-pass 3.4 kHz | R2 | consensus5 | 3 | [1] | 1.29 | 0 | 95% [0, 2.85] | 0 | 95% [0, 2.85] | 0 | 0/0 |  | n/a | 0/0 | 1.77 |
| check readers | white noise 20 dB SNR | R2 | single | 3 | [1, 2, 3] | 23.3 | 0.258 | per recording: gettysburg_dj 0, gettysburg_sa 0.662, gettysburg_tg 0; range [0, 0.662] | 0 | 95% [0, 2.85] | 0 | 0/0 |  | n/a | 0/0 | 3.21 |
| check readers | white noise 20 dB SNR | R2 | consensus5 | 3 | [1, 2, 3] | 3.88 | 0 | 95% [0, 2.85] | 0 | 95% [0, 2.85] | 0 | 0/0 |  | n/a | 0/0 | 1.32 |
| check readers | MP3 64 kbit/s | R2 | single | 3 | [1] | 7.76 | 0 | 95% [0, 2.85] | 0 | 95% [0, 2.85] | 0 | 0/0 |  | n/a | 0/0 | 0.058 |
| check readers | MP3 64 kbit/s | R2 | consensus5 | 3 | [1] | 1.29 | 0 | 95% [0, 2.85] | 0 | 95% [0, 2.85] | 0 | 0/0 |  | n/a | 0/0 | 1.02 |
| check readers | dynamic-range compression | R2 | single | 3 | [1] | 7.76 | 0 | 95% [0, 2.85] | 0 | 95% [0, 2.85] | 0 | 0/0 |  | n/a | 0/0 | 4.76 |
| check readers | dynamic-range compression | R2 | consensus5 | 3 | [1] | 1.29 | 0 | 95% [0, 2.85] | 0 | 95% [0, 2.85] | 0 | 0/0 |  | n/a | 0/0 | 2.41 |
| check readers | room reverb RT60 0.4 s | R2 | single | 3 | [1, 2, 3] | 23.3 | 0 | 95% [0, 2.85] | 0 | 95% [0, 2.85] | 0 | 0/0 |  | n/a | 0/0 | 15.5 |
| check readers | room reverb RT60 0.4 s | R2 | consensus5 | 3 | [1, 2, 3] | 3.88 | 0 | 95% [0, 2.85] | 0 | 95% [0, 2.85] | 0 | 0/0 |  | n/a | 0/0 | 8.28 |
| check readers | phone band + mu-law (participant only) | R2 | single | 3 | [1] | 7.76 | 0.387 | per recording: gettysburg_dj 0.437, gettysburg_sa 0.662, gettysburg_tg 0; range [0, 0.662] | 0 | 95% [0, 2.85] | 0 | 0/0 |  | n/a | 0/0 | 18.3 |
| check readers | phone band + mu-law (participant only) | R2 | consensus5 | 3 | [1] | 1.29 | 0 | 95% [0, 2.85] | 0 | 95% [0, 2.85] | 0 | 0/0 |  | n/a | 0/0 | 8.28 |
| check readers | WORLD speaker transform | R2 | single | 3 | [1] | 7.76 | 0 | 95% [0, 2.85] | 0 | 95% [0, 2.85] | 0 | 0/0 |  | n/a | 0/0 | 5.28 |
| check readers | WORLD speaker transform | R2 | consensus5 | 3 | [1] | 1.29 | 0 | 95% [0, 2.85] | 0 | 95% [0, 2.85] | 0 | 0/0 |  | n/a | 0/0 | 3.41 |
| check readers | babble 10 dB SNR | R2 | single | 3 | [1, 2, 3] | 23.3 | 2.06 | per recording: gettysburg_dj 3.79, gettysburg_sa 1.77, gettysburg_tg 0.817; range [0.817, 3.79] | 0.258 | per recording: gettysburg_dj 0, gettysburg_sa 0.662, gettysburg_tg 0; range [0, 0.662] | 0 | 0/0 |  | n/a | 0/0 | 20.6 |
| check readers | babble 10 dB SNR | R2 | consensus5 | 3 | [1, 2, 3] | 3.88 | 5.41 | per recording: gettysburg_dj 8.73, gettysburg_sa 5.3, gettysburg_tg 2.45; range [2.45, 8.73] | 1.55 | per recording: gettysburg_dj 2.62, gettysburg_sa 1.99, gettysburg_tg 0; range [0, 2.62] | 0 | 0/0 |  | n/a | 0/0 | 8.25 |
| check readers | babble 20 dB SNR | R2 | single | 3 | [1, 2, 3] | 23.3 | 0.129 | per recording: gettysburg_dj 0.146, gettysburg_sa 0, gettysburg_tg 0.272; range [0, 0.272] | 0.0859 | per recording: gettysburg_dj 0, gettysburg_sa 0.221, gettysburg_tg 0; range [0, 0.221] | 0 | 0/0 |  | n/a | 0/0 | 14.9 |
| check readers | babble 20 dB SNR | R2 | consensus5 | 3 | [1, 2, 3] | 3.88 | 1.8 | per recording: gettysburg_dj 0.873, gettysburg_sa 1.99, gettysburg_tg 2.45; range [0.873, 2.45] | 0.516 | per recording: gettysburg_dj 0.873, gettysburg_sa 0.662, gettysburg_tg 0; range [0, 0.873] | 0 | 0/0 |  | n/a | 0/0 | 15.6 |

Conditions that break keys (stated limits; added local regions above the per-key share of the false-region budget, or detections kept below 95%):

| split | condition | regime | reference mode | limit |
|---|---|---|---|---|
| train | low-pass 3.4 kHz | R1 |  | adds D1- regions: 1.21/min [0.96, 1.49] against the per-key share 0.0556/min |
| train | low-pass 3.4 kHz | R2 | single | loses D5- detections: kept 3/4 (0.75) (no interval: fewer than 5 recordings) |
| train | white noise 20 dB SNR | R1 |  | adds D1+ regions: 0.178/min [0.063, 0.336] against the per-key share 0.0556/min |
| train | white noise 20 dB SNR | R1 |  | adds D1- regions: 0.76/min [0.561, 0.998] against the per-key share 0.0556/min |
| train | white noise 20 dB SNR | R1 |  | adds D2+ regions: 0.485/min [0.226, 0.873] against the per-key share 0.0556/min |
| train | white noise 20 dB SNR | R1 |  | adds D9- regions: 0.837/min [0.555, 1.12] against the per-key share 0.0556/min |
| train | white noise 20 dB SNR | R1 |  | loses D5- detections: kept 99/135 (0.733) [0.626, 0.83] |
| train | white noise 20 dB SNR | R1 |  | loses D6- detections: kept 10/30 (0.333) [0.067, 0.6] |
| train | white noise 20 dB SNR | R1 |  | loses D9- detections: kept 6/9 (0.667) (no interval: fewer than 5 recordings) |
| train | white noise 20 dB SNR | R2 | single | loses D5- detections: kept 6/12 (0.5) (no interval: fewer than 5 recordings) |
| train | MP3 64 kbit/s | R1 |  | loses D9- detections: kept 2/3 (0.667) (no interval: fewer than 5 recordings) |
| train | dynamic-range compression | R1 |  | adds D1+ regions: 0.597/min [0.401, 0.804] against the per-key share 0.0556/min |
| train | dynamic-range compression | R1 |  | adds D2- regions: 0.857/min [0.577, 1.15] against the per-key share 0.0556/min |
| train | dynamic-range compression | R1 |  | adds D5- regions: 0.857/min [0.702, 1.04] against the per-key share 0.0556/min |
| train | dynamic-range compression | R1 |  | adds D9- regions: 0.306/min [0.172, 0.464] against the per-key share 0.0556/min |
| train | dynamic-range compression | R1 |  | loses D4- detections: kept 5/11 (0.455) [0.2, 0.727] |
| train | dynamic-range compression | R1 |  | loses D5- detections: kept 13/45 (0.289) [0.163, 0.444] |
| train | dynamic-range compression | R2 | single | loses D5- detections: kept 0/4 (0) (no interval: fewer than 5 recordings) |
| train | room reverb RT60 0.4 s | R1 |  | adds D1+ regions: 0.362/min [0.223, 0.524] against the per-key share 0.0556/min |
| train | room reverb RT60 0.4 s | R1 |  | adds D5- regions: 0.214/min [0.113, 0.339] against the per-key share 0.0556/min |
| train | room reverb RT60 0.4 s | R1 |  | adds D9- regions: 0.173/min [0.101, 0.253] against the per-key share 0.0556/min |
| train | room reverb RT60 0.4 s | R2 | single | loses D2+ detections: kept 3/12 (0.25) (no interval: fewer than 5 recordings) |
| train | phone band + mu-law (participant only) | R1 |  | adds D1- regions: 0.903/min [0.709, 1.12] against the per-key share 0.0556/min |
| train | phone band + mu-law (participant only) | R1 |  | adds D2+ regions: 0.214/min [0.12, 0.323] against the per-key share 0.0556/min |
| train | phone band + mu-law (participant only) | R1 |  | adds D5- regions: 0.199/min [0.104, 0.324] against the per-key share 0.0556/min |
| train | phone band + mu-law (participant only) | R1 |  | adds D9- regions: 0.428/min [0.247, 0.634] against the per-key share 0.0556/min |
| train | phone band + mu-law (participant only) | R1 |  | loses D5- detections: kept 38/45 (0.844) [0.744, 0.935] |
| train | phone band + mu-law (participant only) | R1 |  | loses D9- detections: kept 2/3 (0.667) (no interval: fewer than 5 recordings) |
| train | phone band + mu-law (participant only) | R2 | single | loses D5- detections: kept 2/4 (0.5) (no interval: fewer than 5 recordings) |
| train | WORLD speaker transform | R1 |  | adds D1+ regions: 0.168/min [0.078, 0.272] against the per-key share 0.0556/min |
| train | WORLD speaker transform | R1 |  | adds D5- regions: 0.153/min [0.076, 0.244] against the per-key share 0.0556/min |
| train | WORLD speaker transform | R1 |  | loses D9- detections: kept 2/3 (0.667) (no interval: fewer than 5 recordings) |
| train | WORLD speaker transform | R2 | single | loses D2+ detections: kept 2/4 (0.5) (no interval: fewer than 5 recordings) |
| train | babble 10 dB SNR | R1 |  | adds D1+ regions: 8.94/min [8.27, 9.63] against the per-key share 0.0556/min |
| train | babble 10 dB SNR | R1 |  | adds D1- regions: 3.76/min [3.04, 4.47] against the per-key share 0.0556/min |
| train | babble 10 dB SNR | R1 |  | adds D2- regions: 11.9/min [11.2, 12.6] against the per-key share 0.0556/min |
| train | babble 10 dB SNR | R1 |  | adds D3- regions: 0.24/min [0.09, 0.449] against the per-key share 0.0556/min |
| train | babble 10 dB SNR | R1 |  | adds D4- regions: 0.99/min [0.691, 1.34] against the per-key share 0.0556/min |
| train | babble 10 dB SNR | R1 |  | adds D5- regions: 2.59/min [2.21, 2.93] against the per-key share 0.0556/min |
| train | babble 10 dB SNR | R1 |  | adds D9- regions: 1.61/min [1.31, 1.9] against the per-key share 0.0556/min |
| train | babble 10 dB SNR | R1 |  | loses D1- detections: kept 67/81 (0.827) [0.716, 0.926] |
| train | babble 10 dB SNR | R1 |  | loses D2+ detections: kept 9/105 (0.0857) [0.027, 0.171] |
| train | babble 10 dB SNR | R1 |  | loses D3- detections: kept 11/36 (0.306) [0.139, 0.472] |
| train | babble 10 dB SNR | R1 |  | loses D4- detections: kept 22/33 (0.667) [0.5, 0.867] |
| train | babble 10 dB SNR | R1 |  | loses D5- detections: kept 74/135 (0.548) [0.435, 0.667] |
| train | babble 10 dB SNR | R1 |  | loses D6- detections: kept 9/30 (0.3) [0.133, 0.533] |
| train | babble 10 dB SNR | R1 |  | loses D9- detections: kept 6/9 (0.667) (no interval: fewer than 5 recordings) |
| train | babble 10 dB SNR | R2 | single | adds D1+ regions: 0.365/min [0.195, 0.543] against the per-key share 0.0833/min |
| train | babble 10 dB SNR | R2 | single | adds D5- regions: 0.477/min [0.304, 0.651] against the per-key share 0.0833/min |
| train | babble 10 dB SNR | R2 | single | loses D2+ detections: kept 0/12 (0) (no interval: fewer than 5 recordings) |
| train | babble 10 dB SNR | R2 | single | loses D5- detections: kept 1/12 (0.0833) (no interval: fewer than 5 recordings) |
| train | babble 20 dB SNR | R1 |  | adds D1+ regions: 4.38/min [3.84, 4.9] against the per-key share 0.0556/min |
| train | babble 20 dB SNR | R1 |  | adds D1- regions: 0.408/min [0.211, 0.659] against the per-key share 0.0556/min |
| train | babble 20 dB SNR | R1 |  | adds D2+ regions: 0.265/min [0.168, 0.373] against the per-key share 0.0556/min |
| train | babble 20 dB SNR | R1 |  | adds D2- regions: 5.71/min [4.85, 6.58] against the per-key share 0.0556/min |
| train | babble 20 dB SNR | R1 |  | adds D5- regions: 2.18/min [1.78, 2.56] against the per-key share 0.0556/min |
| train | babble 20 dB SNR | R1 |  | adds D9- regions: 0.536/min [0.372, 0.701] against the per-key share 0.0556/min |
| train | babble 20 dB SNR | R1 |  | loses D2+ detections: kept 75/105 (0.714) [0.616, 0.806] |
| train | babble 20 dB SNR | R1 |  | loses D5- detections: kept 110/135 (0.815) [0.723, 0.906] |
| train | babble 20 dB SNR | R2 | single | loses D2+ detections: kept 1/12 (0.0833) (no interval: fewer than 5 recordings) |
| train | babble 20 dB SNR | R2 | single | loses D5- detections: kept 4/12 (0.333) (no interval: fewer than 5 recordings) |
| val | gain +6 dB | R1 |  | adds D1+ regions: 0.0693/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| val | gain -6 dB | R1 |  | adds D1+ regions: 0.139/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| val | gain -6 dB | R1 |  | adds D9- regions: 0.104/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| val | low-pass 3.4 kHz | R1 |  | adds D1- regions: 0.104/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| val | low-pass 3.4 kHz | R1 |  | adds D2+ regions: 0.0693/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| val | low-pass 3.4 kHz | R1 |  | adds D9- regions: 0.139/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| val | low-pass 3.4 kHz | R1 |  | loses D6- detections: kept 1/4 (0.25) (no interval: fewer than 5 speakers) |
| val | white noise 20 dB SNR | R1 |  | adds D1+ regions: 0.15/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| val | white noise 20 dB SNR | R1 |  | adds D1- regions: 0.462/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| val | white noise 20 dB SNR | R1 |  | adds D2+ regions: 0.589/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| val | white noise 20 dB SNR | R1 |  | adds D4- regions: 0.0924/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| val | white noise 20 dB SNR | R1 |  | adds D5- regions: 0.0693/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| val | white noise 20 dB SNR | R1 |  | adds D9- regions: 1.2/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| val | white noise 20 dB SNR | R1 |  | loses D5- detections: kept 26/33 (0.788) (no interval: fewer than 5 speakers) |
| val | white noise 20 dB SNR | R1 |  | loses D6- detections: kept 1/12 (0.0833) (no interval: fewer than 5 speakers) |
| val | white noise 20 dB SNR | R1 |  | loses D9- detections: kept 8/9 (0.889) (no interval: fewer than 5 speakers) |
| val | MP3 64 kbit/s | R1 |  | adds D1+ regions: 0.0693/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| val | dynamic-range compression | R1 |  | adds D1+ regions: 1.49/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| val | dynamic-range compression | R1 |  | adds D1- regions: 0.173/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| val | dynamic-range compression | R1 |  | adds D2- regions: 1.98/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| val | dynamic-range compression | R1 |  | adds D4- regions: 0.346/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| val | dynamic-range compression | R1 |  | adds D5- regions: 2.22/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| val | dynamic-range compression | R1 |  | adds D9- regions: 0.139/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| val | dynamic-range compression | R1 |  | loses D1- detections: kept 7/9 (0.778) (no interval: fewer than 5 speakers) |
| val | dynamic-range compression | R1 |  | loses D2+ detections: kept 12/13 (0.923) (no interval: fewer than 5 speakers) |
| val | dynamic-range compression | R1 |  | loses D4- detections: kept 5/7 (0.714) (no interval: fewer than 5 speakers) |
| val | dynamic-range compression | R1 |  | loses D5- detections: kept 2/11 (0.182) (no interval: fewer than 5 speakers) |
| val | dynamic-range compression | R1 |  | loses D6- detections: kept 3/4 (0.75) (no interval: fewer than 5 speakers) |
| val | dynamic-range compression | R1 |  | loses D9- detections: kept 2/3 (0.667) (no interval: fewer than 5 speakers) |
| val | room reverb RT60 0.4 s | R1 |  | adds D1+ regions: 0.335/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| val | room reverb RT60 0.4 s | R1 |  | adds D2+ regions: 0.0578/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| val | room reverb RT60 0.4 s | R1 |  | adds D3- regions: 0.0924/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| val | room reverb RT60 0.4 s | R1 |  | adds D4- regions: 0.15/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| val | room reverb RT60 0.4 s | R1 |  | adds D9- regions: 0.15/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| val | room reverb RT60 0.4 s | R1 |  | loses D1- detections: kept 25/27 (0.926) (no interval: fewer than 5 speakers) |
| val | room reverb RT60 0.4 s | R1 |  | loses D2+ detections: kept 36/39 (0.923) (no interval: fewer than 5 speakers) |
| val | room reverb RT60 0.4 s | R1 |  | loses D6- detections: kept 9/12 (0.75) (no interval: fewer than 5 speakers) |
| val | room reverb RT60 0.4 s | R1 |  | loses D9- detections: kept 7/9 (0.778) (no interval: fewer than 5 speakers) |
| val | phone band + mu-law (participant only) | R1 |  | adds D1+ regions: 0.173/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| val | phone band + mu-law (participant only) | R1 |  | adds D2+ regions: 0.208/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| val | phone band + mu-law (participant only) | R1 |  | adds D2- regions: 0.104/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| val | phone band + mu-law (participant only) | R1 |  | adds D3- regions: 0.589/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| val | phone band + mu-law (participant only) | R1 |  | adds D4- regions: 0.243/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| val | phone band + mu-law (participant only) | R1 |  | adds D5- regions: 0.243/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| val | phone band + mu-law (participant only) | R1 |  | adds D9- regions: 0.243/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| val | phone band + mu-law (participant only) | R1 |  | loses D2+ detections: kept 12/13 (0.923) (no interval: fewer than 5 speakers) |
| val | phone band + mu-law (participant only) | R1 |  | loses D5- detections: kept 6/11 (0.545) (no interval: fewer than 5 speakers) |
| val | phone band + mu-law (participant only) | R1 |  | loses D6- detections: kept 2/4 (0.5) (no interval: fewer than 5 speakers) |
| val | WORLD speaker transform | R1 |  | adds D1+ regions: 0.104/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| val | WORLD speaker transform | R1 |  | adds D2+ regions: 0.0693/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| val | WORLD speaker transform | R1 |  | adds D4- regions: 0.0693/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| val | WORLD speaker transform | R1 |  | adds D9- regions: 0.589/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| val | WORLD speaker transform | R1 |  | loses D2+ detections: kept 12/13 (0.923) (no interval: fewer than 5 speakers) |
| val | WORLD speaker transform | R1 |  | loses D6- detections: kept 3/4 (0.75) (no interval: fewer than 5 speakers) |
| val | WORLD speaker transform | R1 |  | loses D9- detections: kept 2/3 (0.667) (no interval: fewer than 5 speakers) |
| val | babble 10 dB SNR | R1 |  | adds D1+ regions: 7.42/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| val | babble 10 dB SNR | R1 |  | adds D1- regions: 3.29/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| val | babble 10 dB SNR | R1 |  | adds D2+ regions: 0.0809/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| val | babble 10 dB SNR | R1 |  | adds D2- regions: 9.73/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| val | babble 10 dB SNR | R1 |  | adds D3- regions: 0.266/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| val | babble 10 dB SNR | R1 |  | adds D4- regions: 0.543/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| val | babble 10 dB SNR | R1 |  | adds D5- regions: 1.21/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| val | babble 10 dB SNR | R1 |  | adds D9- regions: 1.41/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| val | babble 10 dB SNR | R1 |  | loses D1+ detections: kept 9/12 (0.75) (no interval: fewer than 5 speakers) |
| val | babble 10 dB SNR | R1 |  | loses D1- detections: kept 22/27 (0.815) (no interval: fewer than 5 speakers) |
| val | babble 10 dB SNR | R1 |  | loses D2+ detections: kept 5/39 (0.128) (no interval: fewer than 5 speakers) |
| val | babble 10 dB SNR | R1 |  | loses D3- detections: kept 11/15 (0.733) (no interval: fewer than 5 speakers) |
| val | babble 10 dB SNR | R1 |  | loses D5- detections: kept 16/33 (0.485) (no interval: fewer than 5 speakers) |
| val | babble 10 dB SNR | R1 |  | loses D6- detections: kept 1/12 (0.0833) (no interval: fewer than 5 speakers) |
| val | babble 10 dB SNR | R1 |  | loses D9- detections: kept 8/9 (0.889) (no interval: fewer than 5 speakers) |
| val | babble 20 dB SNR | R1 |  | adds D1+ regions: 2.56/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| val | babble 20 dB SNR | R1 |  | adds D1- regions: 0.254/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| val | babble 20 dB SNR | R1 |  | adds D2+ regions: 0.543/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| val | babble 20 dB SNR | R1 |  | adds D2- regions: 3.4/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| val | babble 20 dB SNR | R1 |  | adds D4- regions: 0.127/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| val | babble 20 dB SNR | R1 |  | adds D5- regions: 0.878/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| val | babble 20 dB SNR | R1 |  | adds D9- regions: 0.578/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| val | babble 20 dB SNR | R1 |  | loses D1- detections: kept 24/27 (0.889) (no interval: fewer than 5 speakers) |
| val | babble 20 dB SNR | R1 |  | loses D2+ detections: kept 36/39 (0.923) (no interval: fewer than 5 speakers) |
| val | babble 20 dB SNR | R1 |  | loses D5- detections: kept 23/33 (0.697) (no interval: fewer than 5 speakers) |
| val | babble 20 dB SNR | R1 |  | loses D6- detections: kept 4/12 (0.333) (no interval: fewer than 5 speakers) |
| val | babble 20 dB SNR | R1 |  | loses D9- detections: kept 8/9 (0.889) (no interval: fewer than 5 speakers) |
| test | gain -6 dB | R1 |  | adds D1- regions: 0.0694/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| test | gain -6 dB | R1 |  | adds D2+ regions: 0.0694/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| test | gain -6 dB | R1 |  | adds D2- regions: 0.0694/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| test | gain -6 dB | R1 |  | adds D9- regions: 0.0694/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| test | low-pass 3.4 kHz | R1 |  | adds D1+ regions: 0.139/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| test | low-pass 3.4 kHz | R1 |  | adds D1- regions: 0.833/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| test | low-pass 3.4 kHz | R1 |  | adds D2+ regions: 0.173/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| test | low-pass 3.4 kHz | R1 |  | adds D2- regions: 0.0694/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| test | low-pass 3.4 kHz | R1 |  | adds D9- regions: 0.208/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| test | low-pass 3.4 kHz | R1 |  | loses D2- detections: kept 18/19 (0.947) (no interval: fewer than 5 speakers) |
| test | low-pass 3.4 kHz | R1 |  | loses D4- detections: kept 5/6 (0.833) (no interval: fewer than 5 speakers) |
| test | low-pass 3.4 kHz | R1 |  | loses D5- detections: kept 17/19 (0.895) (no interval: fewer than 5 speakers) |
| test | low-pass 3.4 kHz | R1 |  | loses D6- detections: kept 3/4 (0.75) (no interval: fewer than 5 speakers) |
| test | white noise 20 dB SNR | R1 |  | adds D1+ regions: 0.139/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| test | white noise 20 dB SNR | R1 |  | adds D1- regions: 0.497/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| test | white noise 20 dB SNR | R1 |  | adds D2+ regions: 0.625/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| test | white noise 20 dB SNR | R1 |  | adds D2- regions: 0.0694/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| test | white noise 20 dB SNR | R1 |  | adds D9- regions: 0.474/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| test | white noise 20 dB SNR | R1 |  | loses D2- detections: kept 54/57 (0.947) (no interval: fewer than 5 speakers) |
| test | white noise 20 dB SNR | R1 |  | loses D5- detections: kept 48/57 (0.842) (no interval: fewer than 5 speakers) |
| test | white noise 20 dB SNR | R1 |  | loses D6- detections: kept 3/12 (0.25) (no interval: fewer than 5 speakers) |
| test | dynamic-range compression | R1 |  | adds D1+ regions: 0.173/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| test | dynamic-range compression | R1 |  | adds D2- regions: 1.18/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| test | dynamic-range compression | R1 |  | adds D4- regions: 0.0694/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| test | dynamic-range compression | R1 |  | adds D5- regions: 1.01/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| test | dynamic-range compression | R1 |  | adds D9- regions: 0.104/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| test | dynamic-range compression | R1 |  | loses D4- detections: kept 2/6 (0.333) (no interval: fewer than 5 speakers) |
| test | dynamic-range compression | R1 |  | loses D5- detections: kept 4/19 (0.21) (no interval: fewer than 5 speakers) |
| test | room reverb RT60 0.4 s | R1 |  | adds D1+ regions: 0.139/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| test | room reverb RT60 0.4 s | R1 |  | adds D1- regions: 0.0694/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| test | room reverb RT60 0.4 s | R1 |  | adds D3- regions: 0.081/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| test | room reverb RT60 0.4 s | R1 |  | adds D5- regions: 0.0694/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| test | room reverb RT60 0.4 s | R1 |  | adds D9- regions: 0.127/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| test | room reverb RT60 0.4 s | R1 |  | loses D3- detections: kept 5/6 (0.833) (no interval: fewer than 5 speakers) |
| test | room reverb RT60 0.4 s | R1 |  | loses D9- detections: kept 2/3 (0.667) (no interval: fewer than 5 speakers) |
| test | phone band + mu-law (participant only) | R1 |  | adds D1+ regions: 0.139/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| test | phone band + mu-law (participant only) | R1 |  | adds D1- regions: 1.04/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| test | phone band + mu-law (participant only) | R1 |  | adds D2+ regions: 0.278/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| test | phone band + mu-law (participant only) | R1 |  | adds D3- regions: 2.84/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| test | phone band + mu-law (participant only) | R1 |  | adds D4- regions: 0.659/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| test | phone band + mu-law (participant only) | R1 |  | adds D5- regions: 0.173/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| test | phone band + mu-law (participant only) | R1 |  | adds D9- regions: 0.312/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| test | phone band + mu-law (participant only) | R1 |  | loses D1- detections: kept 9/10 (0.9) (no interval: fewer than 5 speakers) |
| test | phone band + mu-law (participant only) | R1 |  | loses D2- detections: kept 18/19 (0.947) (no interval: fewer than 5 speakers) |
| test | phone band + mu-law (participant only) | R1 |  | loses D3- detections: kept 0/2 (0) (no interval: fewer than 5 speakers) |
| test | phone band + mu-law (participant only) | R1 |  | loses D4- detections: kept 5/6 (0.833) (no interval: fewer than 5 speakers) |
| test | phone band + mu-law (participant only) | R1 |  | loses D5- detections: kept 15/19 (0.789) (no interval: fewer than 5 speakers) |
| test | phone band + mu-law (participant only) | R1 |  | loses D6- detections: kept 3/4 (0.75) (no interval: fewer than 5 speakers) |
| test | WORLD speaker transform | R1 |  | adds D1+ regions: 0.173/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| test | WORLD speaker transform | R1 |  | adds D1- regions: 0.0694/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| test | WORLD speaker transform | R1 |  | adds D2+ regions: 0.104/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| test | WORLD speaker transform | R1 |  | adds D2- regions: 0.0694/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| test | WORLD speaker transform | R1 |  | adds D3- regions: 0.0694/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| test | WORLD speaker transform | R1 |  | adds D9- regions: 0.208/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| test | WORLD speaker transform | R1 |  | loses D4- detections: kept 5/6 (0.833) (no interval: fewer than 5 speakers) |
| test | babble 10 dB SNR | R1 |  | adds D1+ regions: 7.17/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| test | babble 10 dB SNR | R1 |  | adds D1- regions: 3.1/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| test | babble 10 dB SNR | R1 |  | adds D2+ regions: 0.15/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| test | babble 10 dB SNR | R1 |  | adds D2- regions: 11.5/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| test | babble 10 dB SNR | R1 |  | adds D3- regions: 0.416/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| test | babble 10 dB SNR | R1 |  | adds D4- regions: 0.243/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| test | babble 10 dB SNR | R1 |  | adds D5- regions: 1.61/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| test | babble 10 dB SNR | R1 |  | adds D9- regions: 1.43/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| test | babble 10 dB SNR | R1 |  | loses D1+ detections: kept 6/12 (0.5) (no interval: fewer than 5 speakers) |
| test | babble 10 dB SNR | R1 |  | loses D1- detections: kept 21/30 (0.7) (no interval: fewer than 5 speakers) |
| test | babble 10 dB SNR | R1 |  | loses D2+ detections: kept 4/39 (0.103) (no interval: fewer than 5 speakers) |
| test | babble 10 dB SNR | R1 |  | loses D3- detections: kept 4/6 (0.667) (no interval: fewer than 5 speakers) |
| test | babble 10 dB SNR | R1 |  | loses D4- detections: kept 13/18 (0.722) (no interval: fewer than 5 speakers) |
| test | babble 10 dB SNR | R1 |  | loses D5- detections: kept 30/57 (0.526) (no interval: fewer than 5 speakers) |
| test | babble 10 dB SNR | R1 |  | loses D6- detections: kept 3/12 (0.25) (no interval: fewer than 5 speakers) |
| test | babble 20 dB SNR | R1 |  | adds D1+ regions: 3.34/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| test | babble 20 dB SNR | R1 |  | adds D1- regions: 0.37/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| test | babble 20 dB SNR | R1 |  | adds D2+ regions: 0.139/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| test | babble 20 dB SNR | R1 |  | adds D2- regions: 6.53/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| test | babble 20 dB SNR | R1 |  | adds D4- regions: 0.081/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| test | babble 20 dB SNR | R1 |  | adds D5- regions: 2.36/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| test | babble 20 dB SNR | R1 |  | adds D9- regions: 0.335/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| test | babble 20 dB SNR | R1 |  | loses D1+ detections: kept 11/12 (0.917) (no interval: fewer than 5 speakers) |
| test | babble 20 dB SNR | R1 |  | loses D1- detections: kept 24/30 (0.8) (no interval: fewer than 5 speakers) |
| test | babble 20 dB SNR | R1 |  | loses D2+ detections: kept 24/39 (0.615) (no interval: fewer than 5 speakers) |
| test | babble 20 dB SNR | R1 |  | loses D4- detections: kept 17/18 (0.944) (no interval: fewer than 5 speakers) |
| test | babble 20 dB SNR | R1 |  | loses D5- detections: kept 49/57 (0.86) (no interval: fewer than 5 speakers) |
| test | babble 20 dB SNR | R1 |  | loses D9- detections: kept 2/3 (0.667) (no interval: fewer than 5 speakers) |
| val+test | gain -6 dB | R1 |  | adds D1+ regions: 0.0693/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| val+test | gain -6 dB | R1 |  | adds D9- regions: 0.0867/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| val+test | low-pass 3.4 kHz | R1 |  | adds D1+ regions: 0.0867/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| val+test | low-pass 3.4 kHz | R1 |  | adds D1- regions: 0.468/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| val+test | low-pass 3.4 kHz | R1 |  | adds D2+ regions: 0.121/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| val+test | low-pass 3.4 kHz | R1 |  | adds D9- regions: 0.173/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| val+test | low-pass 3.4 kHz | R1 |  | loses D4- detections: kept 12/13 (0.923) (no interval: fewer than 5 speakers) |
| val+test | low-pass 3.4 kHz | R1 |  | loses D5- detections: kept 28/30 (0.933) (no interval: fewer than 5 speakers) |
| val+test | low-pass 3.4 kHz | R1 |  | loses D6- detections: kept 4/8 (0.5) (no interval: fewer than 5 speakers) |
| val+test | white noise 20 dB SNR | R1 |  | adds D1+ regions: 0.144/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| val+test | white noise 20 dB SNR | R1 |  | adds D1- regions: 0.48/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| val+test | white noise 20 dB SNR | R1 |  | adds D2+ regions: 0.607/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| val+test | white noise 20 dB SNR | R1 |  | adds D2- regions: 0.0578/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| val+test | white noise 20 dB SNR | R1 |  | adds D4- regions: 0.0636/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| val+test | white noise 20 dB SNR | R1 |  | adds D9- regions: 0.838/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| val+test | white noise 20 dB SNR | R1 |  | loses D5- detections: kept 74/90 (0.822) (no interval: fewer than 5 speakers) |
| val+test | white noise 20 dB SNR | R1 |  | loses D6- detections: kept 4/24 (0.167) (no interval: fewer than 5 speakers) |
| val+test | white noise 20 dB SNR | R1 |  | loses D9- detections: kept 11/12 (0.917) (no interval: fewer than 5 speakers) |
| val+test | dynamic-range compression | R1 |  | adds D1+ regions: 0.832/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| val+test | dynamic-range compression | R1 |  | adds D1- regions: 0.104/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| val+test | dynamic-range compression | R1 |  | adds D2- regions: 1.58/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| val+test | dynamic-range compression | R1 |  | adds D4- regions: 0.208/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| val+test | dynamic-range compression | R1 |  | adds D5- regions: 1.61/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| val+test | dynamic-range compression | R1 |  | adds D9- regions: 0.121/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| val+test | dynamic-range compression | R1 |  | loses D1- detections: kept 17/19 (0.895) (no interval: fewer than 5 speakers) |
| val+test | dynamic-range compression | R1 |  | loses D4- detections: kept 7/13 (0.538) (no interval: fewer than 5 speakers) |
| val+test | dynamic-range compression | R1 |  | loses D5- detections: kept 6/30 (0.2) (no interval: fewer than 5 speakers) |
| val+test | dynamic-range compression | R1 |  | loses D6- detections: kept 7/8 (0.875) (no interval: fewer than 5 speakers) |
| val+test | dynamic-range compression | R1 |  | loses D9- detections: kept 3/4 (0.75) (no interval: fewer than 5 speakers) |
| val+test | room reverb RT60 0.4 s | R1 |  | adds D1+ regions: 0.237/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| val+test | room reverb RT60 0.4 s | R1 |  | adds D3- regions: 0.0867/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| val+test | room reverb RT60 0.4 s | R1 |  | adds D4- regions: 0.0982/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| val+test | room reverb RT60 0.4 s | R1 |  | adds D9- regions: 0.139/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| val+test | room reverb RT60 0.4 s | R1 |  | loses D1- detections: kept 54/57 (0.947) (no interval: fewer than 5 speakers) |
| val+test | room reverb RT60 0.4 s | R1 |  | loses D6- detections: kept 21/24 (0.875) (no interval: fewer than 5 speakers) |
| val+test | room reverb RT60 0.4 s | R1 |  | loses D9- detections: kept 9/12 (0.75) (no interval: fewer than 5 speakers) |
| val+test | phone band + mu-law (participant only) | R1 |  | adds D1+ regions: 0.156/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| val+test | phone band + mu-law (participant only) | R1 |  | adds D1- regions: 0.537/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| val+test | phone band + mu-law (participant only) | R1 |  | adds D2+ regions: 0.243/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| val+test | phone band + mu-law (participant only) | R1 |  | adds D2- regions: 0.0693/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| val+test | phone band + mu-law (participant only) | R1 |  | adds D3- regions: 1.72/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| val+test | phone band + mu-law (participant only) | R1 |  | adds D4- regions: 0.451/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| val+test | phone band + mu-law (participant only) | R1 |  | adds D5- regions: 0.208/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| val+test | phone band + mu-law (participant only) | R1 |  | adds D9- regions: 0.277/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| val+test | phone band + mu-law (participant only) | R1 |  | loses D1- detections: kept 18/19 (0.947) (no interval: fewer than 5 speakers) |
| val+test | phone band + mu-law (participant only) | R1 |  | loses D3- detections: kept 5/7 (0.714) (no interval: fewer than 5 speakers) |
| val+test | phone band + mu-law (participant only) | R1 |  | loses D4- detections: kept 12/13 (0.923) (no interval: fewer than 5 speakers) |
| val+test | phone band + mu-law (participant only) | R1 |  | loses D5- detections: kept 21/30 (0.7) (no interval: fewer than 5 speakers) |
| val+test | phone band + mu-law (participant only) | R1 |  | loses D6- detections: kept 5/8 (0.625) (no interval: fewer than 5 speakers) |
| val+test | WORLD speaker transform | R1 |  | adds D1+ regions: 0.139/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| val+test | WORLD speaker transform | R1 |  | adds D2+ regions: 0.0867/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| val+test | WORLD speaker transform | R1 |  | adds D9- regions: 0.399/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| val+test | WORLD speaker transform | R1 |  | loses D4- detections: kept 12/13 (0.923) (no interval: fewer than 5 speakers) |
| val+test | WORLD speaker transform | R1 |  | loses D6- detections: kept 7/8 (0.875) (no interval: fewer than 5 speakers) |
| val+test | WORLD speaker transform | R1 |  | loses D9- detections: kept 3/4 (0.75) (no interval: fewer than 5 speakers) |
| val+test | babble 10 dB SNR | R1 |  | adds D1+ regions: 7.29/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| val+test | babble 10 dB SNR | R1 |  | adds D1- regions: 3.2/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| val+test | babble 10 dB SNR | R1 |  | adds D2+ regions: 0.116/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| val+test | babble 10 dB SNR | R1 |  | adds D2- regions: 10.6/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| val+test | babble 10 dB SNR | R1 |  | adds D3- regions: 0.341/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| val+test | babble 10 dB SNR | R1 |  | adds D4- regions: 0.393/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| val+test | babble 10 dB SNR | R1 |  | adds D5- regions: 1.41/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| val+test | babble 10 dB SNR | R1 |  | adds D9- regions: 1.42/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| val+test | babble 10 dB SNR | R1 |  | loses D1+ detections: kept 15/24 (0.625) (no interval: fewer than 5 speakers) |
| val+test | babble 10 dB SNR | R1 |  | loses D1- detections: kept 43/57 (0.754) (no interval: fewer than 5 speakers) |
| val+test | babble 10 dB SNR | R1 |  | loses D2+ detections: kept 9/78 (0.115) (no interval: fewer than 5 speakers) |
| val+test | babble 10 dB SNR | R1 |  | loses D3- detections: kept 15/21 (0.714) (no interval: fewer than 5 speakers) |
| val+test | babble 10 dB SNR | R1 |  | loses D4- detections: kept 33/39 (0.846) (no interval: fewer than 5 speakers) |
| val+test | babble 10 dB SNR | R1 |  | loses D5- detections: kept 46/90 (0.511) (no interval: fewer than 5 speakers) |
| val+test | babble 10 dB SNR | R1 |  | loses D6- detections: kept 4/24 (0.167) (no interval: fewer than 5 speakers) |
| val+test | babble 10 dB SNR | R1 |  | loses D9- detections: kept 11/12 (0.917) (no interval: fewer than 5 speakers) |
| val+test | babble 20 dB SNR | R1 |  | adds D1+ regions: 2.95/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| val+test | babble 20 dB SNR | R1 |  | adds D1- regions: 0.312/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| val+test | babble 20 dB SNR | R1 |  | adds D2+ regions: 0.341/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| val+test | babble 20 dB SNR | R1 |  | adds D2- regions: 4.96/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| val+test | babble 20 dB SNR | R1 |  | adds D4- regions: 0.104/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| val+test | babble 20 dB SNR | R1 |  | adds D5- regions: 1.62/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| val+test | babble 20 dB SNR | R1 |  | adds D9- regions: 0.457/min (no interval: fewer than 5 speakers) against the per-key share 0.0556/min |
| val+test | babble 20 dB SNR | R1 |  | loses D1- detections: kept 48/57 (0.842) (no interval: fewer than 5 speakers) |
| val+test | babble 20 dB SNR | R1 |  | loses D2+ detections: kept 60/78 (0.769) (no interval: fewer than 5 speakers) |
| val+test | babble 20 dB SNR | R1 |  | loses D5- detections: kept 72/90 (0.8) (no interval: fewer than 5 speakers) |
| val+test | babble 20 dB SNR | R1 |  | loses D6- detections: kept 16/24 (0.667) (no interval: fewer than 5 speakers) |
| val+test | babble 20 dB SNR | R1 |  | loses D9- detections: kept 10/12 (0.833) (no interval: fewer than 5 speakers) |
| check readers | white noise 20 dB SNR | R2 | single | adds D2+ regions: 0.258/min (no interval: fewer than 5 recordings) against the per-key share 0.0833/min |
| check readers | phone band + mu-law (participant only) | R2 | single | adds D2+ regions: 0.258/min (no interval: fewer than 5 recordings) against the per-key share 0.0833/min |
| check readers | phone band + mu-law (participant only) | R2 | single | adds D5- regions: 0.129/min (no interval: fewer than 5 recordings) against the per-key share 0.0833/min |
| check readers | babble 10 dB SNR | R2 | single | adds D1+ regions: 1.03/min (no interval: fewer than 5 recordings) against the per-key share 0.0833/min |
| check readers | babble 10 dB SNR | R2 | single | adds D1- regions: 0.0859/min (no interval: fewer than 5 recordings) against the per-key share 0.0833/min |
| check readers | babble 10 dB SNR | R2 | single | adds D2- regions: 0.902/min (no interval: fewer than 5 recordings) against the per-key share 0.0833/min |
| check readers | babble 10 dB SNR | R2 | consensus5 | adds D1+ regions: 1.29/min (no interval: fewer than 5 recordings) against the per-key share 0.0833/min |
| check readers | babble 10 dB SNR | R2 | consensus5 | adds D2- regions: 4.12/min (no interval: fewer than 5 recordings) against the per-key share 0.0833/min |
| check readers | babble 20 dB SNR | R2 | single | adds D2- regions: 0.0859/min (no interval: fewer than 5 recordings) against the per-key share 0.0833/min |
| check readers | babble 20 dB SNR | R2 | consensus5 | adds D2- regions: 1.8/min (no interval: fewer than 5 recordings) against the per-key share 0.0833/min |

Added regions per key:

| split | condition | regime | reference mode | key | added (all seeds) | per min | interval |
|---|---|---|---|---|---|---|---|
| train | gain +6 dB | R1 |  | D1+ | 2 | 0.0306 | 95% [0, 0.076] |
| train | gain +6 dB | R1 |  | D2+ | 2 | 0.0306 | 95% [0, 0.077] |
| train | gain +6 dB | R1 |  | D3- | 1 | 0.0153 | 95% [0, 0.047] |
| train | gain +6 dB | R1 |  | D4- | 2 | 0.0306 | 95% [0, 0.078] |
| train | gain +6 dB | R1 |  | D9- | 6 | 0.0918 | 95% [0.03, 0.17] |
| train | gain -6 dB | R1 |  | D1- | 1 | 0.0153 | 95% [0, 0.047] |
| train | gain -6 dB | R1 |  | D4- | 2 | 0.0306 | 95% [0, 0.078] |
| train | gain -6 dB | R1 |  | D9- | 3 | 0.0459 | 95% [0, 0.108] |
| train | low-pass 3.4 kHz | R1 |  | D1+ | 6 | 0.0918 | 95% [0.016, 0.185] |
| train | low-pass 3.4 kHz | R1 |  | D1+ whole clip | 1 | 0.0153 | 95% [0, 0.046] |
| train | low-pass 3.4 kHz | R1 |  | D1- | 79 | 1.21 | 95% [0.96, 1.49] |
| train | low-pass 3.4 kHz | R1 |  | D2+ | 5 | 0.0765 | 95% [0.015, 0.151] |
| train | low-pass 3.4 kHz | R1 |  | D2- | 1 | 0.0153 | 95% [0, 0.047] |
| train | low-pass 3.4 kHz | R1 |  | D4- | 2 | 0.0306 | 95% [0, 0.078] |
| train | low-pass 3.4 kHz | R1 |  | D5- | 3 | 0.0459 | 95% [0, 0.108] |
| train | low-pass 3.4 kHz | R1 |  | D9- | 8 | 0.122 | 95% [0.031, 0.224] |
| train | white noise 20 dB SNR | R1 |  | D1+ | 35 | 0.178 | 95% [0.063, 0.336] |
| train | white noise 20 dB SNR | R1 |  | D1- | 149 | 0.76 | 95% [0.561, 0.998] |
| train | white noise 20 dB SNR | R1 |  | D2+ | 95 | 0.485 | 95% [0.226, 0.873] |
| train | white noise 20 dB SNR | R1 |  | D2- | 1 | 0.0051 | 95% [0, 0.016] |
| train | white noise 20 dB SNR | R1 |  | D3- | 2 | 0.0102 | 95% [0, 0.03] |
| train | white noise 20 dB SNR | R1 |  | D4- | 15 | 0.0765 | 95% [0.015, 0.142] |
| train | white noise 20 dB SNR | R1 |  | D5- | 3 | 0.0153 | 95% [0, 0.047] |
| train | white noise 20 dB SNR | R1 |  | D6- | 5 | 0.0255 | 95% [0, 0.062] |
| train | white noise 20 dB SNR | R1 |  | D9- | 164 | 0.837 | 95% [0.555, 1.12] |
| train | MP3 64 kbit/s | R1 |  | D1+ | 1 | 0.0153 | 95% [0, 0.046] |
| train | MP3 64 kbit/s | R1 |  | D5- | 1 | 0.0153 | 95% [0, 0.047] |
| train | MP3 64 kbit/s | R1 |  | D9- | 3 | 0.0459 | 95% [0, 0.108] |
| train | MP3 64 kbit/s | R2 | single | D5- | 1 | 0.0842 | 95% [0, 0.26] |
| train | dynamic-range compression | R1 |  | D1+ | 39 | 0.597 | 95% [0.401, 0.804] |
| train | dynamic-range compression | R1 |  | D1+ whole clip | 2 | 0.0306 | 95% [0, 0.077] |
| train | dynamic-range compression | R1 |  | D1- | 6 | 0.0918 | 95% [0, 0.238] |
| train | dynamic-range compression | R1 |  | D2+ | 3 | 0.0459 | 95% [0, 0.105] |
| train | dynamic-range compression | R1 |  | D2- | 56 | 0.857 | 95% [0.577, 1.15] |
| train | dynamic-range compression | R1 |  | D3- | 5 | 0.0765 | 95% [0.015, 0.149] |
| train | dynamic-range compression | R1 |  | D4- | 5 | 0.0765 | 95% [0.015, 0.17] |
| train | dynamic-range compression | R1 |  | D5- | 56 | 0.857 | 95% [0.702, 1.04] |
| train | dynamic-range compression | R1 |  | D9- | 20 | 0.306 | 95% [0.172, 0.464] |
| train | room reverb RT60 0.4 s | R1 |  | D1+ | 71 | 0.362 | 95% [0.223, 0.524] |
| train | room reverb RT60 0.4 s | R1 |  | D1+ whole clip | 3 | 0.0153 | 95% [0, 0.046] |
| train | room reverb RT60 0.4 s | R1 |  | D1- | 19 | 0.0969 | 95% [0.03, 0.192] |
| train | room reverb RT60 0.4 s | R1 |  | D2+ | 2 | 0.0102 | 95% [0, 0.026] |
| train | room reverb RT60 0.4 s | R1 |  | D2- | 3 | 0.0153 | 95% [0, 0.047] |
| train | room reverb RT60 0.4 s | R1 |  | D3- | 7 | 0.0357 | 95% [0.005, 0.076] |
| train | room reverb RT60 0.4 s | R1 |  | D4- | 8 | 0.0408 | 95% [0.01, 0.077] |
| train | room reverb RT60 0.4 s | R1 |  | D5- | 42 | 0.214 | 95% [0.113, 0.339] |
| train | room reverb RT60 0.4 s | R1 |  | D9- | 34 | 0.173 | 95% [0.101, 0.253] |
| train | room reverb RT60 0.4 s | R2 | single | D5- | 13 | 0.365 | 95% [0.056, 0.754] |
| train | phone band + mu-law (participant only) | R1 |  | D1+ | 8 | 0.122 | 95% [0.016, 0.249] |
| train | phone band + mu-law (participant only) | R1 |  | D1+ whole clip | 1 | 0.0153 | 95% [0, 0.046] |
| train | phone band + mu-law (participant only) | R1 |  | D1- | 59 | 0.903 | 95% [0.709, 1.12] |
| train | phone band + mu-law (participant only) | R1 |  | D2+ | 14 | 0.214 | 95% [0.12, 0.323] |
| train | phone band + mu-law (participant only) | R1 |  | D2- | 3 | 0.0459 | 95% [0, 0.106] |
| train | phone band + mu-law (participant only) | R1 |  | D3- | 1 | 0.0153 | 95% [0, 0.047] |
| train | phone band + mu-law (participant only) | R1 |  | D4- | 3 | 0.0459 | 95% [0, 0.106] |
| train | phone band + mu-law (participant only) | R1 |  | D5- | 13 | 0.199 | 95% [0.104, 0.324] |
| train | phone band + mu-law (participant only) | R1 |  | D9- | 28 | 0.428 | 95% [0.247, 0.634] |
| train | phone band + mu-law (participant only) | R2 | single | D5- | 1 | 0.0842 | 95% [0, 0.26] |
| train | WORLD speaker transform | R1 |  | D1+ | 11 | 0.168 | 95% [0.078, 0.272] |
| train | WORLD speaker transform | R1 |  | D1- | 2 | 0.0306 | 95% [0, 0.077] |
| train | WORLD speaker transform | R1 |  | D2+ | 2 | 0.0306 | 95% [0, 0.077] |
| train | WORLD speaker transform | R1 |  | D2- | 1 | 0.0153 | 95% [0, 0.047] |
| train | WORLD speaker transform | R1 |  | D3- | 1 | 0.0153 | 95% [0, 0.047] |
| train | WORLD speaker transform | R1 |  | D4- | 3 | 0.0459 | 95% [0, 0.105] |
| train | WORLD speaker transform | R1 |  | D5- | 10 | 0.153 | 95% [0.076, 0.244] |
| train | WORLD speaker transform | R1 |  | D9- | 4 | 0.0612 | 95% [0.015, 0.123] |
| train | babble 10 dB SNR | R1 |  | D1+ | 1753 | 8.94 | 95% [8.27, 9.63] |
| train | babble 10 dB SNR | R1 |  | D1+ whole clip | 55 | 0.281 | 95% [0.186, 0.38] |
| train | babble 10 dB SNR | R1 |  | D1- | 737 | 3.76 | 95% [3.04, 4.47] |
| train | babble 10 dB SNR | R1 |  | D2+ | 11 | 0.0561 | 95% [0.021, 0.097] |
| train | babble 10 dB SNR | R1 |  | D2- | 2333 | 11.9 | 95% [11.2, 12.6] |
| train | babble 10 dB SNR | R1 |  | D3- | 47 | 0.24 | 95% [0.09, 0.449] |
| train | babble 10 dB SNR | R1 |  | D4- | 194 | 0.99 | 95% [0.691, 1.34] |
| train | babble 10 dB SNR | R1 |  | D5- | 507 | 2.59 | 95% [2.21, 2.93] |
| train | babble 10 dB SNR | R1 |  | D9- | 316 | 1.61 | 95% [1.31, 1.9] |
| train | babble 10 dB SNR | R2 | single | D1+ | 13 | 0.365 | 95% [0.195, 0.543] |
| train | babble 10 dB SNR | R2 | single | D3- | 5 | 0.14 | 95% [0, 0.448] |
| train | babble 10 dB SNR | R2 | single | D5- | 17 | 0.477 | 95% [0.304, 0.651] |
| train | babble 20 dB SNR | R1 |  | D1+ | 859 | 4.38 | 95% [3.84, 4.9] |
| train | babble 20 dB SNR | R1 |  | D1+ whole clip | 8 | 0.0408 | 95% [0, 0.096] |
| train | babble 20 dB SNR | R1 |  | D1- | 80 | 0.408 | 95% [0.211, 0.659] |
| train | babble 20 dB SNR | R1 |  | D2+ | 52 | 0.265 | 95% [0.168, 0.373] |
| train | babble 20 dB SNR | R1 |  | D2- | 1119 | 5.71 | 95% [4.85, 6.58] |
| train | babble 20 dB SNR | R1 |  | D3- | 6 | 0.0306 | 95% [0.005, 0.071] |
| train | babble 20 dB SNR | R1 |  | D4- | 19 | 0.0969 | 95% [0.036, 0.181] |
| train | babble 20 dB SNR | R1 |  | D5- | 427 | 2.18 | 95% [1.78, 2.56] |
| train | babble 20 dB SNR | R1 |  | D9- | 105 | 0.536 | 95% [0.372, 0.701] |
| train | babble 20 dB SNR | R2 | single | D1+ | 1 | 0.0281 | 95% [0, 0.086] |
| train | babble 20 dB SNR | R2 | single | D5- | 3 | 0.0842 | 95% [0, 0.224] |
| val | gain +6 dB | R1 |  | D1+ | 2 | 0.0693 | per speaker: eisenhower_farewell_1961 0.138, lbush_radio_2001 0; range [0, 0.138] |
| val | gain +6 dB | R1 |  | D2+ | 1 | 0.0347 | per speaker: eisenhower_farewell_1961 0.069, lbush_radio_2001 0; range [0, 0.069] |
| val | gain +6 dB | R1 |  | D2- | 1 | 0.0347 | per speaker: eisenhower_farewell_1961 0.069, lbush_radio_2001 0; range [0, 0.069] |
| val | gain +6 dB | R1 |  | D4- | 1 | 0.0347 | per speaker: eisenhower_farewell_1961 0.069, lbush_radio_2001 0; range [0, 0.069] |
| val | gain +6 dB | R1 |  | D9- | 1 | 0.0347 | per speaker: eisenhower_farewell_1961 0, lbush_radio_2001 0.069; range [0, 0.069] |
| val | gain -6 dB | R1 |  | D1+ | 4 | 0.139 | per speaker: eisenhower_farewell_1961 0.208, lbush_radio_2001 0.069; range [0.069, 0.208] |
| val | gain -6 dB | R1 |  | D2+ | 1 | 0.0347 | per speaker: eisenhower_farewell_1961 0.069, lbush_radio_2001 0; range [0, 0.069] |
| val | gain -6 dB | R1 |  | D9- | 3 | 0.104 | per speaker: eisenhower_farewell_1961 0.138, lbush_radio_2001 0.069; range [0.069, 0.138] |
| val | low-pass 3.4 kHz | R1 |  | D1+ | 1 | 0.0347 | per speaker: eisenhower_farewell_1961 0.069, lbush_radio_2001 0; range [0, 0.069] |
| val | low-pass 3.4 kHz | R1 |  | D1- | 3 | 0.104 | per speaker: eisenhower_farewell_1961 0.138, lbush_radio_2001 0.069; range [0.069, 0.138] |
| val | low-pass 3.4 kHz | R1 |  | D2+ | 2 | 0.0693 | per speaker: eisenhower_farewell_1961 0.138, lbush_radio_2001 0; range [0, 0.138] |
| val | low-pass 3.4 kHz | R1 |  | D5- | 1 | 0.0347 | per speaker: eisenhower_farewell_1961 0, lbush_radio_2001 0.069; range [0, 0.069] |
| val | low-pass 3.4 kHz | R1 |  | D9- | 4 | 0.139 | per speaker: eisenhower_farewell_1961 0.138, lbush_radio_2001 0.139; range [0.138, 0.139] |
| val | white noise 20 dB SNR | R1 |  | D1+ | 13 | 0.15 | per speaker: eisenhower_farewell_1961 0.138, lbush_radio_2001 0.162; range [0.138, 0.162] |
| val | white noise 20 dB SNR | R1 |  | D1- | 40 | 0.462 | per speaker: eisenhower_farewell_1961 0.6, lbush_radio_2001 0.324; range [0.324, 0.6] |
| val | white noise 20 dB SNR | R1 |  | D2+ | 51 | 0.589 | per speaker: eisenhower_farewell_1961 0.438, lbush_radio_2001 0.74; range [0.438, 0.74] |
| val | white noise 20 dB SNR | R1 |  | D2- | 4 | 0.0462 | per speaker: eisenhower_farewell_1961 0.092, lbush_radio_2001 0; range [0, 0.092] |
| val | white noise 20 dB SNR | R1 |  | D3- | 1 | 0.0116 | per speaker: eisenhower_farewell_1961 0, lbush_radio_2001 0.023; range [0, 0.023] |
| val | white noise 20 dB SNR | R1 |  | D4- | 8 | 0.0924 | per speaker: eisenhower_farewell_1961 0.115, lbush_radio_2001 0.069; range [0.069, 0.115] |
| val | white noise 20 dB SNR | R1 |  | D5- | 6 | 0.0693 | per speaker: eisenhower_farewell_1961 0, lbush_radio_2001 0.139; range [0, 0.139] |
| val | white noise 20 dB SNR | R1 |  | D6- | 1 | 0.0116 | per speaker: eisenhower_farewell_1961 0.023, lbush_radio_2001 0; range [0, 0.023] |
| val | white noise 20 dB SNR | R1 |  | D9- | 104 | 1.2 | per speaker: eisenhower_farewell_1961 0.553, lbush_radio_2001 1.85; range [0.553, 1.85] |
| val | MP3 64 kbit/s | R1 |  | D1+ | 2 | 0.0693 | per speaker: eisenhower_farewell_1961 0.138, lbush_radio_2001 0; range [0, 0.138] |
| val | dynamic-range compression | R1 |  | D1+ | 43 | 1.49 | per speaker: eisenhower_farewell_1961 2.84, lbush_radio_2001 0.139; range [0.139, 2.84] |
| val | dynamic-range compression | R1 |  | D1+ whole clip | 1 | 0.0347 | per speaker: eisenhower_farewell_1961 0.069, lbush_radio_2001 0; range [0, 0.069] |
| val | dynamic-range compression | R1 |  | D1- | 5 | 0.173 | per speaker: eisenhower_farewell_1961 0.346, lbush_radio_2001 0; range [0, 0.346] |
| val | dynamic-range compression | R1 |  | D2+ | 1 | 0.0347 | per speaker: eisenhower_farewell_1961 0.069, lbush_radio_2001 0; range [0, 0.069] |
| val | dynamic-range compression | R1 |  | D2- | 57 | 1.98 | per speaker: eisenhower_farewell_1961 3.94, lbush_radio_2001 0; range [0, 3.94] |
| val | dynamic-range compression | R1 |  | D3- | 1 | 0.0347 | per speaker: eisenhower_farewell_1961 0, lbush_radio_2001 0.069; range [0, 0.069] |
| val | dynamic-range compression | R1 |  | D4- | 10 | 0.346 | per speaker: eisenhower_farewell_1961 0.138, lbush_radio_2001 0.555; range [0.138, 0.555] |
| val | dynamic-range compression | R1 |  | D5- | 64 | 2.22 | per speaker: eisenhower_farewell_1961 0.484, lbush_radio_2001 3.96; range [0.484, 3.96] |
| val | dynamic-range compression | R1 |  | D6- | 1 | 0.0347 | per speaker: eisenhower_farewell_1961 0, lbush_radio_2001 0.069; range [0, 0.069] |
| val | dynamic-range compression | R1 |  | D9- | 4 | 0.139 | per speaker: eisenhower_farewell_1961 0.138, lbush_radio_2001 0.139; range [0.138, 0.139] |
| val | room reverb RT60 0.4 s | R1 |  | D1+ | 29 | 0.335 | per speaker: eisenhower_farewell_1961 0.323, lbush_radio_2001 0.347; range [0.323, 0.347] |
| val | room reverb RT60 0.4 s | R1 |  | D1- | 2 | 0.0231 | per speaker: eisenhower_farewell_1961 0.046, lbush_radio_2001 0; range [0, 0.046] |
| val | room reverb RT60 0.4 s | R1 |  | D2+ | 5 | 0.0578 | per speaker: eisenhower_farewell_1961 0.092, lbush_radio_2001 0.023; range [0.023, 0.092] |
| val | room reverb RT60 0.4 s | R1 |  | D2- | 4 | 0.0462 | per speaker: eisenhower_farewell_1961 0.092, lbush_radio_2001 0; range [0, 0.092] |
| val | room reverb RT60 0.4 s | R1 |  | D3- | 8 | 0.0924 | per speaker: eisenhower_farewell_1961 0.023, lbush_radio_2001 0.162; range [0.023, 0.162] |
| val | room reverb RT60 0.4 s | R1 |  | D4- | 13 | 0.15 | per speaker: eisenhower_farewell_1961 0.277, lbush_radio_2001 0.023; range [0.023, 0.277] |
| val | room reverb RT60 0.4 s | R1 |  | D5- | 3 | 0.0347 | per speaker: eisenhower_farewell_1961 0, lbush_radio_2001 0.069; range [0, 0.069] |
| val | room reverb RT60 0.4 s | R1 |  | D9- | 13 | 0.15 | per speaker: eisenhower_farewell_1961 0.115, lbush_radio_2001 0.185; range [0.115, 0.185] |
| val | phone band + mu-law (participant only) | R1 |  | D1+ | 5 | 0.173 | per speaker: eisenhower_farewell_1961 0.346, lbush_radio_2001 0; range [0, 0.346] |
| val | phone band + mu-law (participant only) | R1 |  | D1- | 1 | 0.0347 | per speaker: eisenhower_farewell_1961 0, lbush_radio_2001 0.069; range [0, 0.069] |
| val | phone band + mu-law (participant only) | R1 |  | D2+ | 6 | 0.208 | per speaker: eisenhower_farewell_1961 0.415, lbush_radio_2001 0; range [0, 0.415] |
| val | phone band + mu-law (participant only) | R1 |  | D2- | 3 | 0.104 | per speaker: eisenhower_farewell_1961 0.208, lbush_radio_2001 0; range [0, 0.208] |
| val | phone band + mu-law (participant only) | R1 |  | D3- | 17 | 0.589 | per speaker: eisenhower_farewell_1961 1.11, lbush_radio_2001 0.069; range [0.069, 1.11] |
| val | phone band + mu-law (participant only) | R1 |  | D4- | 7 | 0.243 | per speaker: eisenhower_farewell_1961 0.346, lbush_radio_2001 0.139; range [0.139, 0.346] |
| val | phone band + mu-law (participant only) | R1 |  | D5- | 7 | 0.243 | per speaker: eisenhower_farewell_1961 0.346, lbush_radio_2001 0.139; range [0.139, 0.346] |
| val | phone band + mu-law (participant only) | R1 |  | D9- | 7 | 0.243 | per speaker: eisenhower_farewell_1961 0.138, lbush_radio_2001 0.347; range [0.138, 0.347] |
| val | WORLD speaker transform | R1 |  | D1+ | 3 | 0.104 | per speaker: eisenhower_farewell_1961 0.138, lbush_radio_2001 0.069; range [0.069, 0.138] |
| val | WORLD speaker transform | R1 |  | D1- | 1 | 0.0347 | per speaker: eisenhower_farewell_1961 0.069, lbush_radio_2001 0; range [0, 0.069] |
| val | WORLD speaker transform | R1 |  | D2+ | 2 | 0.0693 | per speaker: eisenhower_farewell_1961 0.138, lbush_radio_2001 0; range [0, 0.138] |
| val | WORLD speaker transform | R1 |  | D2- | 1 | 0.0347 | per speaker: eisenhower_farewell_1961 0.069, lbush_radio_2001 0; range [0, 0.069] |
| val | WORLD speaker transform | R1 |  | D4- | 2 | 0.0693 | per speaker: eisenhower_farewell_1961 0.069, lbush_radio_2001 0.069; range [0.069, 0.069] |
| val | WORLD speaker transform | R1 |  | D5- | 1 | 0.0347 | per speaker: eisenhower_farewell_1961 0.069, lbush_radio_2001 0; range [0, 0.069] |
| val | WORLD speaker transform | R1 |  | D9- | 17 | 0.589 | per speaker: eisenhower_farewell_1961 0.899, lbush_radio_2001 0.278; range [0.278, 0.899] |
| val | babble 10 dB SNR | R1 |  | D1+ | 642 | 7.42 | per speaker: eisenhower_farewell_1961 6.66, lbush_radio_2001 8.17; range [6.66, 8.17] |
| val | babble 10 dB SNR | R1 |  | D1+ whole clip | 49 | 0.566 | per speaker: eisenhower_farewell_1961 0.992, lbush_radio_2001 0.139; range [0.139, 0.992] |
| val | babble 10 dB SNR | R1 |  | D1- | 285 | 3.29 | per speaker: eisenhower_farewell_1961 5.03, lbush_radio_2001 1.55; range [1.55, 5.03] |
| val | babble 10 dB SNR | R1 |  | D2+ | 7 | 0.0809 | per speaker: eisenhower_farewell_1961 0.023, lbush_radio_2001 0.139; range [0.023, 0.139] |
| val | babble 10 dB SNR | R1 |  | D2- | 842 | 9.73 | per speaker: eisenhower_farewell_1961 12, lbush_radio_2001 7.47; range [7.47, 12] |
| val | babble 10 dB SNR | R1 |  | D3- | 23 | 0.266 | per speaker: eisenhower_farewell_1961 0.208, lbush_radio_2001 0.324; range [0.208, 0.324] |
| val | babble 10 dB SNR | R1 |  | D4- | 47 | 0.543 | per speaker: eisenhower_farewell_1961 0.6, lbush_radio_2001 0.486; range [0.486, 0.6] |
| val | babble 10 dB SNR | R1 |  | D5- | 105 | 1.21 | per speaker: eisenhower_farewell_1961 1.25, lbush_radio_2001 1.18; range [1.18, 1.25] |
| val | babble 10 dB SNR | R1 |  | D9- | 122 | 1.41 | per speaker: eisenhower_farewell_1961 0.438, lbush_radio_2001 2.38; range [0.438, 2.38] |
| val | babble 20 dB SNR | R1 |  | D1+ | 222 | 2.56 | per speaker: eisenhower_farewell_1961 3.27, lbush_radio_2001 1.85; range [1.85, 3.27] |
| val | babble 20 dB SNR | R1 |  | D1+ whole clip | 3 | 0.0347 | per speaker: eisenhower_farewell_1961 0.069, lbush_radio_2001 0; range [0, 0.069] |
| val | babble 20 dB SNR | R1 |  | D1- | 22 | 0.254 | per speaker: eisenhower_farewell_1961 0.484, lbush_radio_2001 0.023; range [0.023, 0.484] |
| val | babble 20 dB SNR | R1 |  | D2+ | 47 | 0.543 | per speaker: eisenhower_farewell_1961 0.507, lbush_radio_2001 0.579; range [0.507, 0.579] |
| val | babble 20 dB SNR | R1 |  | D2- | 294 | 3.4 | per speaker: eisenhower_farewell_1961 4.87, lbush_radio_2001 1.92; range [1.92, 4.87] |
| val | babble 20 dB SNR | R1 |  | D3- | 2 | 0.0231 | per speaker: eisenhower_farewell_1961 0.023, lbush_radio_2001 0.023; range [0.023, 0.023] |
| val | babble 20 dB SNR | R1 |  | D4- | 11 | 0.127 | per speaker: eisenhower_farewell_1961 0.138, lbush_radio_2001 0.116; range [0.116, 0.138] |
| val | babble 20 dB SNR | R1 |  | D5- | 76 | 0.878 | per speaker: eisenhower_farewell_1961 1.04, lbush_radio_2001 0.717; range [0.717, 1.04] |
| val | babble 20 dB SNR | R1 |  | D6- | 1 | 0.0116 | per speaker: eisenhower_farewell_1961 0.023, lbush_radio_2001 0; range [0, 0.023] |
| val | babble 20 dB SNR | R1 |  | D9- | 50 | 0.578 | per speaker: eisenhower_farewell_1961 0.208, lbush_radio_2001 0.949; range [0.208, 0.949] |
| test | gain +6 dB | R1 |  | D1+ | 1 | 0.0347 | per speaker: mobama_weekly_2014 0, nixon_resignation_1974 0.069; range [0, 0.069] |
| test | gain +6 dB | R1 |  | D1- | 1 | 0.0347 | per speaker: mobama_weekly_2014 0.07, nixon_resignation_1974 0; range [0, 0.07] |
| test | gain +6 dB | R1 |  | D2- | 1 | 0.0347 | per speaker: mobama_weekly_2014 0, nixon_resignation_1974 0.069; range [0, 0.069] |
| test | gain +6 dB | R1 |  | D9- | 1 | 0.0347 | per speaker: mobama_weekly_2014 0.07, nixon_resignation_1974 0; range [0, 0.07] |
| test | gain -6 dB | R1 |  | D1- | 2 | 0.0694 | per speaker: mobama_weekly_2014 0.139, nixon_resignation_1974 0; range [0, 0.139] |
| test | gain -6 dB | R1 |  | D2+ | 2 | 0.0694 | per speaker: mobama_weekly_2014 0.07, nixon_resignation_1974 0.069; range [0.069, 0.07] |
| test | gain -6 dB | R1 |  | D2- | 2 | 0.0694 | per speaker: mobama_weekly_2014 0.07, nixon_resignation_1974 0.069; range [0.069, 0.07] |
| test | gain -6 dB | R1 |  | D9- | 2 | 0.0694 | per speaker: mobama_weekly_2014 0.139, nixon_resignation_1974 0; range [0, 0.139] |
| test | low-pass 3.4 kHz | R1 |  | D1+ | 4 | 0.139 | per speaker: mobama_weekly_2014 0.139, nixon_resignation_1974 0.138; range [0.138, 0.139] |
| test | low-pass 3.4 kHz | R1 |  | D1- | 24 | 0.833 | per speaker: mobama_weekly_2014 1.6, nixon_resignation_1974 0.069; range [0.069, 1.6] |
| test | low-pass 3.4 kHz | R1 |  | D2+ | 5 | 0.173 | per speaker: mobama_weekly_2014 0.279, nixon_resignation_1974 0.069; range [0.069, 0.279] |
| test | low-pass 3.4 kHz | R1 |  | D2- | 2 | 0.0694 | per speaker: mobama_weekly_2014 0.07, nixon_resignation_1974 0.069; range [0.069, 0.07] |
| test | low-pass 3.4 kHz | R1 |  | D5- | 1 | 0.0347 | per speaker: mobama_weekly_2014 0.07, nixon_resignation_1974 0; range [0, 0.07] |
| test | low-pass 3.4 kHz | R1 |  | D9- | 6 | 0.208 | per speaker: mobama_weekly_2014 0.279, nixon_resignation_1974 0.138; range [0.138, 0.279] |
| test | white noise 20 dB SNR | R1 |  | D1+ | 12 | 0.139 | per speaker: mobama_weekly_2014 0.139, nixon_resignation_1974 0.138; range [0.138, 0.139] |
| test | white noise 20 dB SNR | R1 |  | D1- | 43 | 0.497 | per speaker: mobama_weekly_2014 0.487, nixon_resignation_1974 0.507; range [0.487, 0.507] |
| test | white noise 20 dB SNR | R1 |  | D2+ | 54 | 0.625 | per speaker: mobama_weekly_2014 0.348, nixon_resignation_1974 0.899; range [0.348, 0.899] |
| test | white noise 20 dB SNR | R1 |  | D2- | 6 | 0.0694 | per speaker: mobama_weekly_2014 0.07, nixon_resignation_1974 0.069; range [0.069, 0.07] |
| test | white noise 20 dB SNR | R1 |  | D4- | 3 | 0.0347 | per speaker: mobama_weekly_2014 0, nixon_resignation_1974 0.069; range [0, 0.069] |
| test | white noise 20 dB SNR | R1 |  | D6- | 1 | 0.0116 | per speaker: mobama_weekly_2014 0.023, nixon_resignation_1974 0; range [0, 0.023] |
| test | white noise 20 dB SNR | R1 |  | D9- | 41 | 0.474 | per speaker: mobama_weekly_2014 0.325, nixon_resignation_1974 0.622; range [0.325, 0.622] |
| test | MP3 64 kbit/s | R1 |  | D1- | 1 | 0.0347 | per speaker: mobama_weekly_2014 0.07, nixon_resignation_1974 0; range [0, 0.07] |
| test | MP3 64 kbit/s | R1 |  | D2+ | 1 | 0.0347 | per speaker: mobama_weekly_2014 0.07, nixon_resignation_1974 0; range [0, 0.07] |
| test | MP3 64 kbit/s | R1 |  | D2- | 1 | 0.0347 | per speaker: mobama_weekly_2014 0.07, nixon_resignation_1974 0; range [0, 0.07] |
| test | MP3 64 kbit/s | R1 |  | D9- | 1 | 0.0347 | per speaker: mobama_weekly_2014 0.07, nixon_resignation_1974 0; range [0, 0.07] |
| test | dynamic-range compression | R1 |  | D1+ | 5 | 0.173 | per speaker: mobama_weekly_2014 0.07, nixon_resignation_1974 0.277; range [0.07, 0.277] |
| test | dynamic-range compression | R1 |  | D1- | 1 | 0.0347 | per speaker: mobama_weekly_2014 0.07, nixon_resignation_1974 0; range [0, 0.07] |
| test | dynamic-range compression | R1 |  | D2- | 34 | 1.18 | per speaker: mobama_weekly_2014 0, nixon_resignation_1974 2.35; range [0, 2.35] |
| test | dynamic-range compression | R1 |  | D3- | 1 | 0.0347 | per speaker: mobama_weekly_2014 0.07, nixon_resignation_1974 0; range [0, 0.07] |
| test | dynamic-range compression | R1 |  | D4- | 2 | 0.0694 | per speaker: mobama_weekly_2014 0.07, nixon_resignation_1974 0.069; range [0.069, 0.07] |
| test | dynamic-range compression | R1 |  | D5- | 29 | 1.01 | per speaker: mobama_weekly_2014 1.74, nixon_resignation_1974 0.277; range [0.277, 1.74] |
| test | dynamic-range compression | R1 |  | D9- | 3 | 0.104 | per speaker: mobama_weekly_2014 0.139, nixon_resignation_1974 0.069; range [0.069, 0.139] |
| test | room reverb RT60 0.4 s | R1 |  | D1+ | 12 | 0.139 | per speaker: mobama_weekly_2014 0.07, nixon_resignation_1974 0.207; range [0.07, 0.207] |
| test | room reverb RT60 0.4 s | R1 |  | D1- | 6 | 0.0694 | per speaker: mobama_weekly_2014 0.139, nixon_resignation_1974 0; range [0, 0.139] |
| test | room reverb RT60 0.4 s | R1 |  | D2+ | 4 | 0.0463 | per speaker: mobama_weekly_2014 0.07, nixon_resignation_1974 0.023; range [0.023, 0.07] |
| test | room reverb RT60 0.4 s | R1 |  | D2- | 3 | 0.0347 | per speaker: mobama_weekly_2014 0.07, nixon_resignation_1974 0; range [0, 0.07] |
| test | room reverb RT60 0.4 s | R1 |  | D3- | 7 | 0.081 | per speaker: mobama_weekly_2014 0.116, nixon_resignation_1974 0.046; range [0.046, 0.116] |
| test | room reverb RT60 0.4 s | R1 |  | D4- | 4 | 0.0463 | per speaker: mobama_weekly_2014 0.023, nixon_resignation_1974 0.069; range [0.023, 0.069] |
| test | room reverb RT60 0.4 s | R1 |  | D5- | 6 | 0.0694 | per speaker: mobama_weekly_2014 0.07, nixon_resignation_1974 0.069; range [0.069, 0.07] |
| test | room reverb RT60 0.4 s | R1 |  | D9- | 11 | 0.127 | per speaker: mobama_weekly_2014 0.186, nixon_resignation_1974 0.069; range [0.069, 0.186] |
| test | phone band + mu-law (participant only) | R1 |  | D1+ | 4 | 0.139 | per speaker: mobama_weekly_2014 0.139, nixon_resignation_1974 0.138; range [0.138, 0.139] |
| test | phone band + mu-law (participant only) | R1 |  | D1- | 30 | 1.04 | per speaker: mobama_weekly_2014 0.418, nixon_resignation_1974 1.66; range [0.418, 1.66] |
| test | phone band + mu-law (participant only) | R1 |  | D2+ | 8 | 0.278 | per speaker: mobama_weekly_2014 0.418, nixon_resignation_1974 0.138; range [0.138, 0.418] |
| test | phone band + mu-law (participant only) | R1 |  | D2- | 1 | 0.0347 | per speaker: mobama_weekly_2014 0.07, nixon_resignation_1974 0; range [0, 0.07] |
| test | phone band + mu-law (participant only) | R1 |  | D3- | 82 | 2.84 | per speaker: mobama_weekly_2014 0.139, nixon_resignation_1974 5.53; range [0.139, 5.53] |
| test | phone band + mu-law (participant only) | R1 |  | D4- | 19 | 0.659 | per speaker: mobama_weekly_2014 0.279, nixon_resignation_1974 1.04; range [0.279, 1.04] |
| test | phone band + mu-law (participant only) | R1 |  | D5- | 5 | 0.173 | per speaker: mobama_weekly_2014 0.279, nixon_resignation_1974 0.069; range [0.069, 0.279] |
| test | phone band + mu-law (participant only) | R1 |  | D6- | 1 | 0.0347 | per speaker: mobama_weekly_2014 0.07, nixon_resignation_1974 0; range [0, 0.07] |
| test | phone band + mu-law (participant only) | R1 |  | D9- | 9 | 0.312 | per speaker: mobama_weekly_2014 0.487, nixon_resignation_1974 0.138; range [0.138, 0.487] |
| test | WORLD speaker transform | R1 |  | D1+ | 5 | 0.173 | per speaker: mobama_weekly_2014 0.139, nixon_resignation_1974 0.207; range [0.139, 0.207] |
| test | WORLD speaker transform | R1 |  | D1- | 2 | 0.0694 | per speaker: mobama_weekly_2014 0.07, nixon_resignation_1974 0.069; range [0.069, 0.07] |
| test | WORLD speaker transform | R1 |  | D2+ | 3 | 0.104 | per speaker: mobama_weekly_2014 0.139, nixon_resignation_1974 0.069; range [0.069, 0.139] |
| test | WORLD speaker transform | R1 |  | D2- | 2 | 0.0694 | per speaker: mobama_weekly_2014 0.07, nixon_resignation_1974 0.069; range [0.069, 0.07] |
| test | WORLD speaker transform | R1 |  | D3- | 2 | 0.0694 | per speaker: mobama_weekly_2014 0.139, nixon_resignation_1974 0; range [0, 0.139] |
| test | WORLD speaker transform | R1 |  | D4- | 1 | 0.0347 | per speaker: mobama_weekly_2014 0, nixon_resignation_1974 0.069; range [0, 0.069] |
| test | WORLD speaker transform | R1 |  | D5- | 1 | 0.0347 | per speaker: mobama_weekly_2014 0.07, nixon_resignation_1974 0; range [0, 0.07] |
| test | WORLD speaker transform | R1 |  | D9- | 6 | 0.208 | per speaker: mobama_weekly_2014 0.209, nixon_resignation_1974 0.207; range [0.207, 0.209] |
| test | babble 10 dB SNR | R1 |  | D1+ | 620 | 7.17 | per speaker: mobama_weekly_2014 6.24, nixon_resignation_1974 8.09; range [6.24, 8.09] |
| test | babble 10 dB SNR | R1 |  | D1+ whole clip | 49 | 0.567 | per speaker: mobama_weekly_2014 0.116, nixon_resignation_1974 1.01; range [0.116, 1.01] |
| test | babble 10 dB SNR | R1 |  | D1- | 268 | 3.1 | per speaker: mobama_weekly_2014 0.998, nixon_resignation_1974 5.19; range [0.998, 5.19] |
| test | babble 10 dB SNR | R1 |  | D2+ | 13 | 0.15 | per speaker: mobama_weekly_2014 0.116, nixon_resignation_1974 0.184; range [0.116, 0.184] |
| test | babble 10 dB SNR | R1 |  | D2- | 993 | 11.5 | per speaker: mobama_weekly_2014 10.2, nixon_resignation_1974 12.7; range [10.2, 12.7] |
| test | babble 10 dB SNR | R1 |  | D3- | 36 | 0.416 | per speaker: mobama_weekly_2014 0.093, nixon_resignation_1974 0.738; range [0.093, 0.738] |
| test | babble 10 dB SNR | R1 |  | D4- | 21 | 0.243 | per speaker: mobama_weekly_2014 0.116, nixon_resignation_1974 0.369; range [0.116, 0.369] |
| test | babble 10 dB SNR | R1 |  | D5- | 139 | 1.61 | per speaker: mobama_weekly_2014 0.487, nixon_resignation_1974 2.72; range [0.487, 2.72] |
| test | babble 10 dB SNR | R1 |  | D9- | 124 | 1.43 | per speaker: mobama_weekly_2014 2.04, nixon_resignation_1974 0.83; range [0.83, 2.04] |
| test | babble 20 dB SNR | R1 |  | D1+ | 289 | 3.34 | per speaker: mobama_weekly_2014 0.72, nixon_resignation_1974 5.95; range [0.72, 5.95] |
| test | babble 20 dB SNR | R1 |  | D1+ whole clip | 6 | 0.0694 | per speaker: mobama_weekly_2014 0, nixon_resignation_1974 0.138; range [0, 0.138] |
| test | babble 20 dB SNR | R1 |  | D1- | 32 | 0.37 | per speaker: mobama_weekly_2014 0.209, nixon_resignation_1974 0.53; range [0.209, 0.53] |
| test | babble 20 dB SNR | R1 |  | D2+ | 12 | 0.139 | per speaker: mobama_weekly_2014 0.186, nixon_resignation_1974 0.092; range [0.092, 0.186] |
| test | babble 20 dB SNR | R1 |  | D2- | 565 | 6.53 | per speaker: mobama_weekly_2014 1.23, nixon_resignation_1974 11.8; range [1.23, 11.8] |
| test | babble 20 dB SNR | R1 |  | D4- | 7 | 0.081 | per speaker: mobama_weekly_2014 0.023, nixon_resignation_1974 0.138; range [0.023, 0.138] |
| test | babble 20 dB SNR | R1 |  | D5- | 204 | 2.36 | per speaker: mobama_weekly_2014 0.209, nixon_resignation_1974 4.5; range [0.209, 4.5] |
| test | babble 20 dB SNR | R1 |  | D9- | 29 | 0.335 | per speaker: mobama_weekly_2014 0.232, nixon_resignation_1974 0.438; range [0.232, 0.438] |
| val+test | gain +6 dB | R1 |  | D1+ | 3 | 0.052 | per speaker: eisenhower_farewell_1961 0.138, lbush_radio_2001 0, mobama_weekly_2014 0, nixon_resignation_1974 0.069; range [0, 0.138] |
| val+test | gain +6 dB | R1 |  | D1- | 1 | 0.0173 | per speaker: eisenhower_farewell_1961 0, lbush_radio_2001 0, mobama_weekly_2014 0.07, nixon_resignation_1974 0; range [0, 0.07] |
| val+test | gain +6 dB | R1 |  | D2+ | 1 | 0.0173 | per speaker: eisenhower_farewell_1961 0.069, lbush_radio_2001 0, mobama_weekly_2014 0, nixon_resignation_1974 0; range [0, 0.069] |
| val+test | gain +6 dB | R1 |  | D2- | 2 | 0.0347 | per speaker: eisenhower_farewell_1961 0.069, lbush_radio_2001 0, mobama_weekly_2014 0, nixon_resignation_1974 0.069; range [0, 0.069] |
| val+test | gain +6 dB | R1 |  | D4- | 1 | 0.0173 | per speaker: eisenhower_farewell_1961 0.069, lbush_radio_2001 0, mobama_weekly_2014 0, nixon_resignation_1974 0; range [0, 0.069] |
| val+test | gain +6 dB | R1 |  | D9- | 2 | 0.0347 | per speaker: eisenhower_farewell_1961 0, lbush_radio_2001 0.069, mobama_weekly_2014 0.07, nixon_resignation_1974 0; range [0, 0.07] |
| val+test | gain -6 dB | R1 |  | D1+ | 4 | 0.0693 | per speaker: eisenhower_farewell_1961 0.208, lbush_radio_2001 0.069, mobama_weekly_2014 0, nixon_resignation_1974 0; range [0, 0.208] |
| val+test | gain -6 dB | R1 |  | D1- | 2 | 0.0347 | per speaker: eisenhower_farewell_1961 0, lbush_radio_2001 0, mobama_weekly_2014 0.139, nixon_resignation_1974 0; range [0, 0.139] |
| val+test | gain -6 dB | R1 |  | D2+ | 3 | 0.052 | per speaker: eisenhower_farewell_1961 0.069, lbush_radio_2001 0, mobama_weekly_2014 0.07, nixon_resignation_1974 0.069; range [0, 0.07] |
| val+test | gain -6 dB | R1 |  | D2- | 2 | 0.0347 | per speaker: eisenhower_farewell_1961 0, lbush_radio_2001 0, mobama_weekly_2014 0.07, nixon_resignation_1974 0.069; range [0, 0.07] |
| val+test | gain -6 dB | R1 |  | D9- | 5 | 0.0867 | per speaker: eisenhower_farewell_1961 0.138, lbush_radio_2001 0.069, mobama_weekly_2014 0.139, nixon_resignation_1974 0; range [0, 0.139] |
| val+test | low-pass 3.4 kHz | R1 |  | D1+ | 5 | 0.0867 | per speaker: eisenhower_farewell_1961 0.069, lbush_radio_2001 0, mobama_weekly_2014 0.139, nixon_resignation_1974 0.138; range [0, 0.139] |
| val+test | low-pass 3.4 kHz | R1 |  | D1- | 27 | 0.468 | per speaker: eisenhower_farewell_1961 0.138, lbush_radio_2001 0.069, mobama_weekly_2014 1.6, nixon_resignation_1974 0.069; range [0.069, 1.6] |
| val+test | low-pass 3.4 kHz | R1 |  | D2+ | 7 | 0.121 | per speaker: eisenhower_farewell_1961 0.138, lbush_radio_2001 0, mobama_weekly_2014 0.279, nixon_resignation_1974 0.069; range [0, 0.279] |
| val+test | low-pass 3.4 kHz | R1 |  | D2- | 2 | 0.0347 | per speaker: eisenhower_farewell_1961 0, lbush_radio_2001 0, mobama_weekly_2014 0.07, nixon_resignation_1974 0.069; range [0, 0.07] |
| val+test | low-pass 3.4 kHz | R1 |  | D5- | 2 | 0.0347 | per speaker: eisenhower_farewell_1961 0, lbush_radio_2001 0.069, mobama_weekly_2014 0.07, nixon_resignation_1974 0; range [0, 0.07] |
| val+test | low-pass 3.4 kHz | R1 |  | D9- | 10 | 0.173 | per speaker: eisenhower_farewell_1961 0.138, lbush_radio_2001 0.139, mobama_weekly_2014 0.279, nixon_resignation_1974 0.138; range [0.138, 0.279] |
| val+test | white noise 20 dB SNR | R1 |  | D1+ | 25 | 0.144 | per speaker: eisenhower_farewell_1961 0.138, lbush_radio_2001 0.162, mobama_weekly_2014 0.139, nixon_resignation_1974 0.138; range [0.138, 0.162] |
| val+test | white noise 20 dB SNR | R1 |  | D1- | 83 | 0.48 | per speaker: eisenhower_farewell_1961 0.6, lbush_radio_2001 0.324, mobama_weekly_2014 0.487, nixon_resignation_1974 0.507; range [0.324, 0.6] |
| val+test | white noise 20 dB SNR | R1 |  | D2+ | 105 | 0.607 | per speaker: eisenhower_farewell_1961 0.438, lbush_radio_2001 0.74, mobama_weekly_2014 0.348, nixon_resignation_1974 0.899; range [0.348, 0.899] |
| val+test | white noise 20 dB SNR | R1 |  | D2- | 10 | 0.0578 | per speaker: eisenhower_farewell_1961 0.092, lbush_radio_2001 0, mobama_weekly_2014 0.07, nixon_resignation_1974 0.069; range [0, 0.092] |
| val+test | white noise 20 dB SNR | R1 |  | D3- | 1 | 0.0058 | per speaker: eisenhower_farewell_1961 0, lbush_radio_2001 0.023, mobama_weekly_2014 0, nixon_resignation_1974 0; range [0, 0.023] |
| val+test | white noise 20 dB SNR | R1 |  | D4- | 11 | 0.0636 | per speaker: eisenhower_farewell_1961 0.115, lbush_radio_2001 0.069, mobama_weekly_2014 0, nixon_resignation_1974 0.069; range [0, 0.115] |
| val+test | white noise 20 dB SNR | R1 |  | D5- | 6 | 0.0347 | per speaker: eisenhower_farewell_1961 0, lbush_radio_2001 0.139, mobama_weekly_2014 0, nixon_resignation_1974 0; range [0, 0.139] |
| val+test | white noise 20 dB SNR | R1 |  | D6- | 2 | 0.0116 | per speaker: eisenhower_farewell_1961 0.023, lbush_radio_2001 0, mobama_weekly_2014 0.023, nixon_resignation_1974 0; range [0, 0.023] |
| val+test | white noise 20 dB SNR | R1 |  | D9- | 145 | 0.838 | per speaker: eisenhower_farewell_1961 0.553, lbush_radio_2001 1.85, mobama_weekly_2014 0.325, nixon_resignation_1974 0.622; range [0.325, 1.85] |
| val+test | MP3 64 kbit/s | R1 |  | D1+ | 2 | 0.0347 | per speaker: eisenhower_farewell_1961 0.138, lbush_radio_2001 0, mobama_weekly_2014 0, nixon_resignation_1974 0; range [0, 0.138] |
| val+test | MP3 64 kbit/s | R1 |  | D1- | 1 | 0.0173 | per speaker: eisenhower_farewell_1961 0, lbush_radio_2001 0, mobama_weekly_2014 0.07, nixon_resignation_1974 0; range [0, 0.07] |
| val+test | MP3 64 kbit/s | R1 |  | D2+ | 1 | 0.0173 | per speaker: eisenhower_farewell_1961 0, lbush_radio_2001 0, mobama_weekly_2014 0.07, nixon_resignation_1974 0; range [0, 0.07] |
| val+test | MP3 64 kbit/s | R1 |  | D2- | 1 | 0.0173 | per speaker: eisenhower_farewell_1961 0, lbush_radio_2001 0, mobama_weekly_2014 0.07, nixon_resignation_1974 0; range [0, 0.07] |
| val+test | MP3 64 kbit/s | R1 |  | D9- | 1 | 0.0173 | per speaker: eisenhower_farewell_1961 0, lbush_radio_2001 0, mobama_weekly_2014 0.07, nixon_resignation_1974 0; range [0, 0.07] |
| val+test | dynamic-range compression | R1 |  | D1+ | 48 | 0.832 | per speaker: eisenhower_farewell_1961 2.84, lbush_radio_2001 0.139, mobama_weekly_2014 0.07, nixon_resignation_1974 0.277; range [0.07, 2.84] |
| val+test | dynamic-range compression | R1 |  | D1+ whole clip | 1 | 0.0173 | per speaker: eisenhower_farewell_1961 0.069, lbush_radio_2001 0, mobama_weekly_2014 0, nixon_resignation_1974 0; range [0, 0.069] |
| val+test | dynamic-range compression | R1 |  | D1- | 6 | 0.104 | per speaker: eisenhower_farewell_1961 0.346, lbush_radio_2001 0, mobama_weekly_2014 0.07, nixon_resignation_1974 0; range [0, 0.346] |
| val+test | dynamic-range compression | R1 |  | D2+ | 1 | 0.0173 | per speaker: eisenhower_farewell_1961 0.069, lbush_radio_2001 0, mobama_weekly_2014 0, nixon_resignation_1974 0; range [0, 0.069] |
| val+test | dynamic-range compression | R1 |  | D2- | 91 | 1.58 | per speaker: eisenhower_farewell_1961 3.94, lbush_radio_2001 0, mobama_weekly_2014 0, nixon_resignation_1974 2.35; range [0, 3.94] |
| val+test | dynamic-range compression | R1 |  | D3- | 2 | 0.0347 | per speaker: eisenhower_farewell_1961 0, lbush_radio_2001 0.069, mobama_weekly_2014 0.07, nixon_resignation_1974 0; range [0, 0.07] |
| val+test | dynamic-range compression | R1 |  | D4- | 12 | 0.208 | per speaker: eisenhower_farewell_1961 0.138, lbush_radio_2001 0.555, mobama_weekly_2014 0.07, nixon_resignation_1974 0.069; range [0.069, 0.555] |
| val+test | dynamic-range compression | R1 |  | D5- | 93 | 1.61 | per speaker: eisenhower_farewell_1961 0.484, lbush_radio_2001 3.96, mobama_weekly_2014 1.74, nixon_resignation_1974 0.277; range [0.277, 3.96] |
| val+test | dynamic-range compression | R1 |  | D6- | 1 | 0.0173 | per speaker: eisenhower_farewell_1961 0, lbush_radio_2001 0.069, mobama_weekly_2014 0, nixon_resignation_1974 0; range [0, 0.069] |
| val+test | dynamic-range compression | R1 |  | D9- | 7 | 0.121 | per speaker: eisenhower_farewell_1961 0.138, lbush_radio_2001 0.139, mobama_weekly_2014 0.139, nixon_resignation_1974 0.069; range [0.069, 0.139] |
| val+test | room reverb RT60 0.4 s | R1 |  | D1+ | 41 | 0.237 | per speaker: eisenhower_farewell_1961 0.323, lbush_radio_2001 0.347, mobama_weekly_2014 0.07, nixon_resignation_1974 0.207; range [0.07, 0.347] |
| val+test | room reverb RT60 0.4 s | R1 |  | D1- | 8 | 0.0462 | per speaker: eisenhower_farewell_1961 0.046, lbush_radio_2001 0, mobama_weekly_2014 0.139, nixon_resignation_1974 0; range [0, 0.139] |
| val+test | room reverb RT60 0.4 s | R1 |  | D2+ | 9 | 0.052 | per speaker: eisenhower_farewell_1961 0.092, lbush_radio_2001 0.023, mobama_weekly_2014 0.07, nixon_resignation_1974 0.023; range [0.023, 0.092] |
| val+test | room reverb RT60 0.4 s | R1 |  | D2- | 7 | 0.0405 | per speaker: eisenhower_farewell_1961 0.092, lbush_radio_2001 0, mobama_weekly_2014 0.07, nixon_resignation_1974 0; range [0, 0.092] |
| val+test | room reverb RT60 0.4 s | R1 |  | D3- | 15 | 0.0867 | per speaker: eisenhower_farewell_1961 0.023, lbush_radio_2001 0.162, mobama_weekly_2014 0.116, nixon_resignation_1974 0.046; range [0.023, 0.162] |
| val+test | room reverb RT60 0.4 s | R1 |  | D4- | 17 | 0.0982 | per speaker: eisenhower_farewell_1961 0.277, lbush_radio_2001 0.023, mobama_weekly_2014 0.023, nixon_resignation_1974 0.069; range [0.023, 0.277] |
| val+test | room reverb RT60 0.4 s | R1 |  | D5- | 9 | 0.052 | per speaker: eisenhower_farewell_1961 0, lbush_radio_2001 0.069, mobama_weekly_2014 0.07, nixon_resignation_1974 0.069; range [0, 0.07] |
| val+test | room reverb RT60 0.4 s | R1 |  | D9- | 24 | 0.139 | per speaker: eisenhower_farewell_1961 0.115, lbush_radio_2001 0.185, mobama_weekly_2014 0.186, nixon_resignation_1974 0.069; range [0.069, 0.186] |
| val+test | phone band + mu-law (participant only) | R1 |  | D1+ | 9 | 0.156 | per speaker: eisenhower_farewell_1961 0.346, lbush_radio_2001 0, mobama_weekly_2014 0.139, nixon_resignation_1974 0.138; range [0, 0.346] |
| val+test | phone band + mu-law (participant only) | R1 |  | D1- | 31 | 0.537 | per speaker: eisenhower_farewell_1961 0, lbush_radio_2001 0.069, mobama_weekly_2014 0.418, nixon_resignation_1974 1.66; range [0, 1.66] |
| val+test | phone band + mu-law (participant only) | R1 |  | D2+ | 14 | 0.243 | per speaker: eisenhower_farewell_1961 0.415, lbush_radio_2001 0, mobama_weekly_2014 0.418, nixon_resignation_1974 0.138; range [0, 0.418] |
| val+test | phone band + mu-law (participant only) | R1 |  | D2- | 4 | 0.0693 | per speaker: eisenhower_farewell_1961 0.208, lbush_radio_2001 0, mobama_weekly_2014 0.07, nixon_resignation_1974 0; range [0, 0.208] |
| val+test | phone band + mu-law (participant only) | R1 |  | D3- | 99 | 1.72 | per speaker: eisenhower_farewell_1961 1.11, lbush_radio_2001 0.069, mobama_weekly_2014 0.139, nixon_resignation_1974 5.53; range [0.069, 5.53] |
| val+test | phone band + mu-law (participant only) | R1 |  | D4- | 26 | 0.451 | per speaker: eisenhower_farewell_1961 0.346, lbush_radio_2001 0.139, mobama_weekly_2014 0.279, nixon_resignation_1974 1.04; range [0.139, 1.04] |
| val+test | phone band + mu-law (participant only) | R1 |  | D5- | 12 | 0.208 | per speaker: eisenhower_farewell_1961 0.346, lbush_radio_2001 0.139, mobama_weekly_2014 0.279, nixon_resignation_1974 0.069; range [0.069, 0.346] |
| val+test | phone band + mu-law (participant only) | R1 |  | D6- | 1 | 0.0173 | per speaker: eisenhower_farewell_1961 0, lbush_radio_2001 0, mobama_weekly_2014 0.07, nixon_resignation_1974 0; range [0, 0.07] |
| val+test | phone band + mu-law (participant only) | R1 |  | D9- | 16 | 0.277 | per speaker: eisenhower_farewell_1961 0.138, lbush_radio_2001 0.347, mobama_weekly_2014 0.487, nixon_resignation_1974 0.138; range [0.138, 0.487] |
| val+test | WORLD speaker transform | R1 |  | D1+ | 8 | 0.139 | per speaker: eisenhower_farewell_1961 0.138, lbush_radio_2001 0.069, mobama_weekly_2014 0.139, nixon_resignation_1974 0.207; range [0.069, 0.207] |
| val+test | WORLD speaker transform | R1 |  | D1- | 3 | 0.052 | per speaker: eisenhower_farewell_1961 0.069, lbush_radio_2001 0, mobama_weekly_2014 0.07, nixon_resignation_1974 0.069; range [0, 0.07] |
| val+test | WORLD speaker transform | R1 |  | D2+ | 5 | 0.0867 | per speaker: eisenhower_farewell_1961 0.138, lbush_radio_2001 0, mobama_weekly_2014 0.139, nixon_resignation_1974 0.069; range [0, 0.139] |
| val+test | WORLD speaker transform | R1 |  | D2- | 3 | 0.052 | per speaker: eisenhower_farewell_1961 0.069, lbush_radio_2001 0, mobama_weekly_2014 0.07, nixon_resignation_1974 0.069; range [0, 0.07] |
| val+test | WORLD speaker transform | R1 |  | D3- | 2 | 0.0347 | per speaker: eisenhower_farewell_1961 0, lbush_radio_2001 0, mobama_weekly_2014 0.139, nixon_resignation_1974 0; range [0, 0.139] |
| val+test | WORLD speaker transform | R1 |  | D4- | 3 | 0.052 | per speaker: eisenhower_farewell_1961 0.069, lbush_radio_2001 0.069, mobama_weekly_2014 0, nixon_resignation_1974 0.069; range [0, 0.069] |
| val+test | WORLD speaker transform | R1 |  | D5- | 2 | 0.0347 | per speaker: eisenhower_farewell_1961 0.069, lbush_radio_2001 0, mobama_weekly_2014 0.07, nixon_resignation_1974 0; range [0, 0.07] |
| val+test | WORLD speaker transform | R1 |  | D9- | 23 | 0.399 | per speaker: eisenhower_farewell_1961 0.899, lbush_radio_2001 0.278, mobama_weekly_2014 0.209, nixon_resignation_1974 0.207; range [0.207, 0.899] |
| val+test | babble 10 dB SNR | R1 |  | D1+ | 1262 | 7.29 | per speaker: eisenhower_farewell_1961 6.66, lbush_radio_2001 8.17, mobama_weekly_2014 6.24, nixon_resignation_1974 8.09; range [6.24, 8.17] |
| val+test | babble 10 dB SNR | R1 |  | D1+ whole clip | 98 | 0.566 | per speaker: eisenhower_farewell_1961 0.992, lbush_radio_2001 0.139, mobama_weekly_2014 0.116, nixon_resignation_1974 1.01; range [0.116, 1.01] |
| val+test | babble 10 dB SNR | R1 |  | D1- | 553 | 3.2 | per speaker: eisenhower_farewell_1961 5.03, lbush_radio_2001 1.55, mobama_weekly_2014 0.998, nixon_resignation_1974 5.19; range [0.998, 5.19] |
| val+test | babble 10 dB SNR | R1 |  | D2+ | 20 | 0.116 | per speaker: eisenhower_farewell_1961 0.023, lbush_radio_2001 0.139, mobama_weekly_2014 0.116, nixon_resignation_1974 0.184; range [0.023, 0.184] |
| val+test | babble 10 dB SNR | R1 |  | D2- | 1835 | 10.6 | per speaker: eisenhower_farewell_1961 12, lbush_radio_2001 7.47, mobama_weekly_2014 10.2, nixon_resignation_1974 12.7; range [7.47, 12.7] |
| val+test | babble 10 dB SNR | R1 |  | D3- | 59 | 0.341 | per speaker: eisenhower_farewell_1961 0.208, lbush_radio_2001 0.324, mobama_weekly_2014 0.093, nixon_resignation_1974 0.738; range [0.093, 0.738] |
| val+test | babble 10 dB SNR | R1 |  | D4- | 68 | 0.393 | per speaker: eisenhower_farewell_1961 0.6, lbush_radio_2001 0.486, mobama_weekly_2014 0.116, nixon_resignation_1974 0.369; range [0.116, 0.6] |
| val+test | babble 10 dB SNR | R1 |  | D5- | 244 | 1.41 | per speaker: eisenhower_farewell_1961 1.25, lbush_radio_2001 1.18, mobama_weekly_2014 0.487, nixon_resignation_1974 2.72; range [0.487, 2.72] |
| val+test | babble 10 dB SNR | R1 |  | D9- | 246 | 1.42 | per speaker: eisenhower_farewell_1961 0.438, lbush_radio_2001 2.38, mobama_weekly_2014 2.04, nixon_resignation_1974 0.83; range [0.438, 2.38] |
| val+test | babble 20 dB SNR | R1 |  | D1+ | 511 | 2.95 | per speaker: eisenhower_farewell_1961 3.27, lbush_radio_2001 1.85, mobama_weekly_2014 0.72, nixon_resignation_1974 5.95; range [0.72, 5.95] |
| val+test | babble 20 dB SNR | R1 |  | D1+ whole clip | 9 | 0.052 | per speaker: eisenhower_farewell_1961 0.069, lbush_radio_2001 0, mobama_weekly_2014 0, nixon_resignation_1974 0.138; range [0, 0.138] |
| val+test | babble 20 dB SNR | R1 |  | D1- | 54 | 0.312 | per speaker: eisenhower_farewell_1961 0.484, lbush_radio_2001 0.023, mobama_weekly_2014 0.209, nixon_resignation_1974 0.53; range [0.023, 0.53] |
| val+test | babble 20 dB SNR | R1 |  | D2+ | 59 | 0.341 | per speaker: eisenhower_farewell_1961 0.507, lbush_radio_2001 0.579, mobama_weekly_2014 0.186, nixon_resignation_1974 0.092; range [0.092, 0.579] |
| val+test | babble 20 dB SNR | R1 |  | D2- | 859 | 4.96 | per speaker: eisenhower_farewell_1961 4.87, lbush_radio_2001 1.92, mobama_weekly_2014 1.23, nixon_resignation_1974 11.8; range [1.23, 11.8] |
| val+test | babble 20 dB SNR | R1 |  | D3- | 2 | 0.0116 | per speaker: eisenhower_farewell_1961 0.023, lbush_radio_2001 0.023, mobama_weekly_2014 0, nixon_resignation_1974 0; range [0, 0.023] |
| val+test | babble 20 dB SNR | R1 |  | D4- | 18 | 0.104 | per speaker: eisenhower_farewell_1961 0.138, lbush_radio_2001 0.116, mobama_weekly_2014 0.023, nixon_resignation_1974 0.138; range [0.023, 0.138] |
| val+test | babble 20 dB SNR | R1 |  | D5- | 280 | 1.62 | per speaker: eisenhower_farewell_1961 1.04, lbush_radio_2001 0.717, mobama_weekly_2014 0.209, nixon_resignation_1974 4.5; range [0.209, 4.5] |
| val+test | babble 20 dB SNR | R1 |  | D6- | 1 | 0.0058 | per speaker: eisenhower_farewell_1961 0.023, lbush_radio_2001 0, mobama_weekly_2014 0, nixon_resignation_1974 0; range [0, 0.023] |
| val+test | babble 20 dB SNR | R1 |  | D9- | 79 | 0.457 | per speaker: eisenhower_farewell_1961 0.208, lbush_radio_2001 0.949, mobama_weekly_2014 0.232, nixon_resignation_1974 0.438; range [0.208, 0.949] |
| check readers | white noise 20 dB SNR | R2 | single | D2+ | 6 | 0.258 | per recording: gettysburg_dj 0, gettysburg_sa 0.662, gettysburg_tg 0; range [0, 0.662] |
| check readers | phone band + mu-law (participant only) | R2 | single | D2+ | 2 | 0.258 | per recording: gettysburg_dj 0, gettysburg_sa 0.662, gettysburg_tg 0; range [0, 0.662] |
| check readers | phone band + mu-law (participant only) | R2 | single | D5- | 1 | 0.129 | per recording: gettysburg_dj 0.437, gettysburg_sa 0, gettysburg_tg 0; range [0, 0.437] |
| check readers | babble 10 dB SNR | R2 | single | D1+ | 24 | 1.03 | per recording: gettysburg_dj 2.77, gettysburg_sa 0.552, gettysburg_tg 0; range [0, 2.77] |
| check readers | babble 10 dB SNR | R2 | single | D1- | 2 | 0.0859 | per recording: gettysburg_dj 0, gettysburg_sa 0.221, gettysburg_tg 0; range [0, 0.221] |
| check readers | babble 10 dB SNR | R2 | single | D2- | 21 | 0.902 | per recording: gettysburg_dj 0.873, gettysburg_sa 0.993, gettysburg_tg 0.817; range [0.817, 0.993] |
| check readers | babble 10 dB SNR | R2 | single | D5- | 1 | 0.043 | per recording: gettysburg_dj 0.146, gettysburg_sa 0, gettysburg_tg 0; range [0, 0.146] |
| check readers | babble 10 dB SNR | R2 | consensus5 | D1+ | 5 | 1.29 | per recording: gettysburg_dj 3.49, gettysburg_sa 0.662, gettysburg_tg 0; range [0, 3.49] |
| check readers | babble 10 dB SNR | R2 | consensus5 | D2- | 16 | 4.12 | per recording: gettysburg_dj 5.24, gettysburg_sa 4.64, gettysburg_tg 2.45; range [2.45, 5.24] |
| check readers | babble 20 dB SNR | R2 | single | D2- | 2 | 0.0859 | per recording: gettysburg_dj 0, gettysburg_sa 0, gettysburg_tg 0.272; range [0, 0.272] |
| check readers | babble 20 dB SNR | R2 | single | D5- | 1 | 0.043 | per recording: gettysburg_dj 0.146, gettysburg_sa 0, gettysburg_tg 0; range [0, 0.146] |
| check readers | babble 20 dB SNR | R2 | consensus5 | D2- | 7 | 1.8 | per recording: gettysburg_dj 0.873, gettysburg_sa 1.99, gettysburg_tg 2.45; range [0.873, 2.45] |

Detections kept per truth key:

| split | condition | regime | key | kept / found (all seeds) | fraction | interval | kept in every seed / unique |
|---|---|---|---|---|---|---|---|
| train | gain +6 dB | R1 | D1+ | 10/10 | 1 | degenerate [1, 1] (no spread across the resampled clusters) | 10/10 |
| train | gain +6 dB | R1 | D1- | 26/27 | 0.963 | 95% [0.889, 1] | 26/27 |
| train | gain +6 dB | R1 | D2+ | 35/35 | 1 | degenerate [1, 1] (no spread across the resampled clusters) | 35/35 |
| train | gain +6 dB | R1 | D2- | 45/45 | 1 | degenerate [1, 1] (no spread across the resampled clusters) | 45/45 |
| train | gain +6 dB | R1 | D3- | 12/12 | 1 | degenerate [1, 1] (no spread across the resampled clusters) | 12/12 |
| train | gain +6 dB | R1 | D4- | 11/11 | 1 | degenerate [1, 1] (no spread across the resampled clusters) | 11/11 |
| train | gain +6 dB | R1 | D5- | 44/45 | 0.978 | 95% [0.935, 1] | 44/45 |
| train | gain +6 dB | R1 | D6- | 9/10 | 0.9 | 95% [0.7, 1] | 9/10 |
| train | gain +6 dB | R1 | D9- | 3/3 | 1 | per recording: gwbush_911_2001__extra_L2A 1, harris_uncsw_2021__extra_botched_D1 1, hclinton_tomorrow_2010__extra_L3A 1; range [1, 1] | 3/3 |
| train | gain +6 dB | R2 | D2+ | 4/4 | 1 | per recording: greenman_reagan__extra_botched_D2 1, greenman_reagan__extra_x6_L3 1, greenman_reagan__x3_L3 1; range [1, 1] | 4/4 |
| train | gain +6 dB | R2 | D5- | 4/4 | 1 | per recording: greenman_reagan__G5 1, greenman_reagan__extra_x1_L2 1, greenman_reagan__x3_L3 1; range [1, 1] | 4/4 |
| train | gain -6 dB | R1 | D1+ | 10/10 | 1 | degenerate [1, 1] (no spread across the resampled clusters) | 10/10 |
| train | gain -6 dB | R1 | D1- | 27/27 | 1 | degenerate [1, 1] (no spread across the resampled clusters) | 27/27 |
| train | gain -6 dB | R1 | D2+ | 34/35 | 0.971 | 95% [0.903, 1] | 34/35 |
| train | gain -6 dB | R1 | D2- | 45/45 | 1 | degenerate [1, 1] (no spread across the resampled clusters) | 45/45 |
| train | gain -6 dB | R1 | D3- | 12/12 | 1 | degenerate [1, 1] (no spread across the resampled clusters) | 12/12 |
| train | gain -6 dB | R1 | D4- | 10/11 | 0.909 | 95% [0.769, 1] | 10/11 |
| train | gain -6 dB | R1 | D5- | 45/45 | 1 | degenerate [1, 1] (no spread across the resampled clusters) | 45/45 |
| train | gain -6 dB | R1 | D6- | 10/10 | 1 | degenerate [1, 1] (no spread across the resampled clusters) | 10/10 |
| train | gain -6 dB | R1 | D9- | 3/3 | 1 | per recording: gwbush_911_2001__extra_L2A 1, harris_uncsw_2021__extra_botched_D1 1, hclinton_tomorrow_2010__extra_L3A 1; range [1, 1] | 3/3 |
| train | gain -6 dB | R2 | D2+ | 4/4 | 1 | per recording: greenman_reagan__extra_botched_D2 1, greenman_reagan__extra_x6_L3 1, greenman_reagan__x3_L3 1; range [1, 1] | 4/4 |
| train | gain -6 dB | R2 | D5- | 4/4 | 1 | per recording: greenman_reagan__G5 1, greenman_reagan__extra_x1_L2 1, greenman_reagan__x3_L3 1; range [1, 1] | 4/4 |
| train | low-pass 3.4 kHz | R1 | D1+ | 10/10 | 1 | degenerate [1, 1] (no spread across the resampled clusters) | 10/10 |
| train | low-pass 3.4 kHz | R1 | D1- | 26/27 | 0.963 | 95% [0.889, 1] | 26/27 |
| train | low-pass 3.4 kHz | R1 | D2+ | 35/35 | 1 | degenerate [1, 1] (no spread across the resampled clusters) | 35/35 |
| train | low-pass 3.4 kHz | R1 | D2- | 45/45 | 1 | degenerate [1, 1] (no spread across the resampled clusters) | 45/45 |
| train | low-pass 3.4 kHz | R1 | D3- | 12/12 | 1 | degenerate [1, 1] (no spread across the resampled clusters) | 12/12 |
| train | low-pass 3.4 kHz | R1 | D4- | 10/11 | 0.909 | 95% [0.769, 1] | 10/11 |
| train | low-pass 3.4 kHz | R1 | D5- | 43/45 | 0.956 | 95% [0.898, 1] | 43/45 |
| train | low-pass 3.4 kHz | R1 | D6- | 8/10 | 0.8 | 95% [0.5, 1] | 8/10 |
| train | low-pass 3.4 kHz | R1 | D9- | 3/3 | 1 | per recording: gwbush_911_2001__extra_L2A 1, harris_uncsw_2021__extra_botched_D1 1, hclinton_tomorrow_2010__extra_L3A 1; range [1, 1] | 3/3 |
| train | low-pass 3.4 kHz | R2 | D2+ | 4/4 | 1 | per recording: greenman_reagan__extra_botched_D2 1, greenman_reagan__extra_x6_L3 1, greenman_reagan__x3_L3 1; range [1, 1] | 4/4 |
| train | low-pass 3.4 kHz | R2 | D5- | 3/4 | 0.75 | per recording: greenman_reagan__G5 1, greenman_reagan__extra_x1_L2 0, greenman_reagan__x3_L3 1; range [0, 1] | 3/4 |
| train | white noise 20 dB SNR | R1 | D1+ | 30/30 | 1 | degenerate [1, 1] (no spread across the resampled clusters) | 10/10 |
| train | white noise 20 dB SNR | R1 | D1- | 81/81 | 1 | degenerate [1, 1] (no spread across the resampled clusters) | 27/27 |
| train | white noise 20 dB SNR | R1 | D2+ | 102/105 | 0.971 | 95% [0.909, 1] | 34/35 |
| train | white noise 20 dB SNR | R1 | D2- | 132/135 | 0.978 | 95% [0.931, 1] | 44/45 |
| train | white noise 20 dB SNR | R1 | D3- | 36/36 | 1 | degenerate [1, 1] (no spread across the resampled clusters) | 12/12 |
| train | white noise 20 dB SNR | R1 | D4- | 29/33 | 0.879 | 95% [0.692, 1] | 9/11 |
| train | white noise 20 dB SNR | R1 | D5- | 99/135 | 0.733 | 95% [0.626, 0.83] | 31/45 |
| train | white noise 20 dB SNR | R1 | D6- | 10/30 | 0.333 | 95% [0.067, 0.6] | 3/10 |
| train | white noise 20 dB SNR | R1 | D9- | 6/9 | 0.667 | per recording: gwbush_911_2001__extra_L2A 0.333, harris_uncsw_2021__extra_botched_D1 0.667, hclinton_tomorrow_2010__extra_L3A 1; range [0.333, 1] | 1/3 |
| train | white noise 20 dB SNR | R2 | D2+ | 12/12 | 1 | per recording: greenman_reagan__extra_botched_D2 1, greenman_reagan__extra_x6_L3 1, greenman_reagan__x3_L3 1; range [1, 1] | 4/4 |
| train | white noise 20 dB SNR | R2 | D5- | 6/12 | 0.5 | per recording: greenman_reagan__G5 1, greenman_reagan__extra_x1_L2 0, greenman_reagan__x3_L3 0; range [0, 1] | 2/4 |
| train | MP3 64 kbit/s | R1 | D1+ | 10/10 | 1 | degenerate [1, 1] (no spread across the resampled clusters) | 10/10 |
| train | MP3 64 kbit/s | R1 | D1- | 27/27 | 1 | degenerate [1, 1] (no spread across the resampled clusters) | 27/27 |
| train | MP3 64 kbit/s | R1 | D2+ | 34/35 | 0.971 | 95% [0.903, 1] | 34/35 |
| train | MP3 64 kbit/s | R1 | D2- | 45/45 | 1 | degenerate [1, 1] (no spread across the resampled clusters) | 45/45 |
| train | MP3 64 kbit/s | R1 | D3- | 12/12 | 1 | degenerate [1, 1] (no spread across the resampled clusters) | 12/12 |
| train | MP3 64 kbit/s | R1 | D4- | 10/11 | 0.909 | 95% [0.769, 1] | 10/11 |
| train | MP3 64 kbit/s | R1 | D5- | 45/45 | 1 | degenerate [1, 1] (no spread across the resampled clusters) | 45/45 |
| train | MP3 64 kbit/s | R1 | D6- | 10/10 | 1 | degenerate [1, 1] (no spread across the resampled clusters) | 10/10 |
| train | MP3 64 kbit/s | R1 | D9- | 2/3 | 0.667 | per recording: gwbush_911_2001__extra_L2A 1, harris_uncsw_2021__extra_botched_D1 0, hclinton_tomorrow_2010__extra_L3A 1; range [0, 1] | 2/3 |
| train | MP3 64 kbit/s | R2 | D2+ | 4/4 | 1 | per recording: greenman_reagan__extra_botched_D2 1, greenman_reagan__extra_x6_L3 1, greenman_reagan__x3_L3 1; range [1, 1] | 4/4 |
| train | MP3 64 kbit/s | R2 | D5- | 4/4 | 1 | per recording: greenman_reagan__G5 1, greenman_reagan__extra_x1_L2 1, greenman_reagan__x3_L3 1; range [1, 1] | 4/4 |
| train | dynamic-range compression | R1 | D1+ | 10/10 | 1 | degenerate [1, 1] (no spread across the resampled clusters) | 10/10 |
| train | dynamic-range compression | R1 | D1- | 26/27 | 0.963 | 95% [0.889, 1] | 26/27 |
| train | dynamic-range compression | R1 | D2+ | 34/35 | 0.971 | 95% [0.903, 1] | 34/35 |
| train | dynamic-range compression | R1 | D2- | 45/45 | 1 | degenerate [1, 1] (no spread across the resampled clusters) | 45/45 |
| train | dynamic-range compression | R1 | D3- | 12/12 | 1 | degenerate [1, 1] (no spread across the resampled clusters) | 12/12 |
| train | dynamic-range compression | R1 | D4- | 5/11 | 0.455 | 95% [0.2, 0.727] | 5/11 |
| train | dynamic-range compression | R1 | D5- | 13/45 | 0.289 | 95% [0.163, 0.444] | 13/45 |
| train | dynamic-range compression | R1 | D6- | 9/10 | 0.9 | 95% [0.7, 1] | 9/10 |
| train | dynamic-range compression | R1 | D9- | 3/3 | 1 | per recording: gwbush_911_2001__extra_L2A 1, harris_uncsw_2021__extra_botched_D1 1, hclinton_tomorrow_2010__extra_L3A 1; range [1, 1] | 3/3 |
| train | dynamic-range compression | R2 | D2+ | 4/4 | 1 | per recording: greenman_reagan__extra_botched_D2 1, greenman_reagan__extra_x6_L3 1, greenman_reagan__x3_L3 1; range [1, 1] | 4/4 |
| train | dynamic-range compression | R2 | D5- | 0/4 | 0 | per recording: greenman_reagan__G5 0, greenman_reagan__extra_x1_L2 0, greenman_reagan__x3_L3 0; range [0, 0] | 0/4 |
| train | room reverb RT60 0.4 s | R1 | D1+ | 30/30 | 1 | degenerate [1, 1] (no spread across the resampled clusters) | 10/10 |
| train | room reverb RT60 0.4 s | R1 | D1- | 80/81 | 0.988 | 95% [0.963, 1] | 26/27 |
| train | room reverb RT60 0.4 s | R1 | D2+ | 90/105 | 0.857 | 95% [0.735, 0.952] | 29/35 |
| train | room reverb RT60 0.4 s | R1 | D2- | 135/135 | 1 | degenerate [1, 1] (no spread across the resampled clusters) | 45/45 |
| train | room reverb RT60 0.4 s | R1 | D3- | 36/36 | 1 | degenerate [1, 1] (no spread across the resampled clusters) | 12/12 |
| train | room reverb RT60 0.4 s | R1 | D4- | 26/33 | 0.788 | 95% [0.564, 1] | 7/11 |
| train | room reverb RT60 0.4 s | R1 | D5- | 127/135 | 0.941 | 95% [0.884, 1] | 42/45 |
| train | room reverb RT60 0.4 s | R1 | D6- | 30/30 | 1 | degenerate [1, 1] (no spread across the resampled clusters) | 10/10 |
| train | room reverb RT60 0.4 s | R1 | D9- | 9/9 | 1 | per recording: gwbush_911_2001__extra_L2A 1, harris_uncsw_2021__extra_botched_D1 1, hclinton_tomorrow_2010__extra_L3A 1; range [1, 1] | 3/3 |
| train | room reverb RT60 0.4 s | R2 | D2+ | 3/12 | 0.25 | per recording: greenman_reagan__extra_botched_D2 0, greenman_reagan__extra_x6_L3 0, greenman_reagan__x3_L3 1; range [0, 1] | 1/4 |
| train | room reverb RT60 0.4 s | R2 | D5- | 12/12 | 1 | per recording: greenman_reagan__G5 1, greenman_reagan__extra_x1_L2 1, greenman_reagan__x3_L3 1; range [1, 1] | 4/4 |
| train | phone band + mu-law (participant only) | R1 | D1+ | 10/10 | 1 | degenerate [1, 1] (no spread across the resampled clusters) | 10/10 |
| train | phone band + mu-law (participant only) | R1 | D1- | 27/27 | 1 | degenerate [1, 1] (no spread across the resampled clusters) | 27/27 |
| train | phone band + mu-law (participant only) | R1 | D2+ | 35/35 | 1 | degenerate [1, 1] (no spread across the resampled clusters) | 35/35 |
| train | phone band + mu-law (participant only) | R1 | D2- | 45/45 | 1 | degenerate [1, 1] (no spread across the resampled clusters) | 45/45 |
| train | phone band + mu-law (participant only) | R1 | D3- | 12/12 | 1 | degenerate [1, 1] (no spread across the resampled clusters) | 12/12 |
| train | phone band + mu-law (participant only) | R1 | D4- | 9/11 | 0.818 | 95% [0.545, 1] | 9/11 |
| train | phone band + mu-law (participant only) | R1 | D5- | 38/45 | 0.844 | 95% [0.744, 0.935] | 38/45 |
| train | phone band + mu-law (participant only) | R1 | D6- | 7/10 | 0.7 | 95% [0.4, 1] | 7/10 |
| train | phone band + mu-law (participant only) | R1 | D9- | 2/3 | 0.667 | per recording: gwbush_911_2001__extra_L2A 0, harris_uncsw_2021__extra_botched_D1 1, hclinton_tomorrow_2010__extra_L3A 1; range [0, 1] | 2/3 |
| train | phone band + mu-law (participant only) | R2 | D2+ | 4/4 | 1 | per recording: greenman_reagan__extra_botched_D2 1, greenman_reagan__extra_x6_L3 1, greenman_reagan__x3_L3 1; range [1, 1] | 4/4 |
| train | phone band + mu-law (participant only) | R2 | D5- | 2/4 | 0.5 | per recording: greenman_reagan__G5 0.5, greenman_reagan__extra_x1_L2 0, greenman_reagan__x3_L3 1; range [0, 1] | 2/4 |
| train | WORLD speaker transform | R1 | D1+ | 10/10 | 1 | degenerate [1, 1] (no spread across the resampled clusters) | 10/10 |
| train | WORLD speaker transform | R1 | D1- | 27/27 | 1 | degenerate [1, 1] (no spread across the resampled clusters) | 27/27 |
| train | WORLD speaker transform | R1 | D2+ | 34/35 | 0.971 | 95% [0.903, 1] | 34/35 |
| train | WORLD speaker transform | R1 | D2- | 45/45 | 1 | degenerate [1, 1] (no spread across the resampled clusters) | 45/45 |
| train | WORLD speaker transform | R1 | D3- | 11/12 | 0.917 | 95% [0.75, 1] | 11/12 |
| train | WORLD speaker transform | R1 | D4- | 10/11 | 0.909 | 95% [0.7, 1] | 10/11 |
| train | WORLD speaker transform | R1 | D5- | 44/45 | 0.978 | 95% [0.935, 1] | 44/45 |
| train | WORLD speaker transform | R1 | D6- | 10/10 | 1 | degenerate [1, 1] (no spread across the resampled clusters) | 10/10 |
| train | WORLD speaker transform | R1 | D9- | 2/3 | 0.667 | per recording: gwbush_911_2001__extra_L2A 0, harris_uncsw_2021__extra_botched_D1 1, hclinton_tomorrow_2010__extra_L3A 1; range [0, 1] | 2/3 |
| train | WORLD speaker transform | R2 | D2+ | 2/4 | 0.5 | per recording: greenman_reagan__extra_botched_D2 0.5, greenman_reagan__extra_x6_L3 0, greenman_reagan__x3_L3 1; range [0, 1] | 2/4 |
| train | WORLD speaker transform | R2 | D5- | 4/4 | 1 | per recording: greenman_reagan__G5 1, greenman_reagan__extra_x1_L2 1, greenman_reagan__x3_L3 1; range [1, 1] | 4/4 |
| train | babble 10 dB SNR | R1 | D1+ | 26/30 | 0.867 | 95% [0.667, 1] | 8/10 |
| train | babble 10 dB SNR | R1 | D1- | 67/81 | 0.827 | 95% [0.716, 0.926] | 18/27 |
| train | babble 10 dB SNR | R1 | D2+ | 9/105 | 0.0857 | 95% [0.027, 0.171] | 1/35 |
| train | babble 10 dB SNR | R1 | D2- | 135/135 | 1 | degenerate [1, 1] (no spread across the resampled clusters) | 45/45 |
| train | babble 10 dB SNR | R1 | D3- | 11/36 | 0.306 | 95% [0.139, 0.472] | 0/12 |
| train | babble 10 dB SNR | R1 | D4- | 22/33 | 0.667 | 95% [0.5, 0.867] | 4/11 |
| train | babble 10 dB SNR | R1 | D5- | 74/135 | 0.548 | 95% [0.435, 0.667] | 14/45 |
| train | babble 10 dB SNR | R1 | D6- | 9/30 | 0.3 | 95% [0.133, 0.533] | 1/10 |
| train | babble 10 dB SNR | R1 | D9- | 6/9 | 0.667 | per recording: gwbush_911_2001__extra_L2A 0, harris_uncsw_2021__extra_botched_D1 1, hclinton_tomorrow_2010__extra_L3A 1; range [0, 1] | 2/3 |
| train | babble 10 dB SNR | R2 | D2+ | 0/12 | 0 | per recording: greenman_reagan__extra_botched_D2 0, greenman_reagan__extra_x6_L3 0, greenman_reagan__x3_L3 0; range [0, 0] | 0/4 |
| train | babble 10 dB SNR | R2 | D5- | 1/12 | 0.0833 | per recording: greenman_reagan__G5 0.167, greenman_reagan__extra_x1_L2 0, greenman_reagan__x3_L3 0; range [0, 0.167] | 0/4 |
| train | babble 20 dB SNR | R1 | D1+ | 30/30 | 1 | degenerate [1, 1] (no spread across the resampled clusters) | 10/10 |
| train | babble 20 dB SNR | R1 | D1- | 77/81 | 0.951 | 95% [0.901, 0.988] | 23/27 |
| train | babble 20 dB SNR | R1 | D2+ | 75/105 | 0.714 | 95% [0.616, 0.806] | 16/35 |
| train | babble 20 dB SNR | R1 | D2- | 135/135 | 1 | degenerate [1, 1] (no spread across the resampled clusters) | 45/45 |
| train | babble 20 dB SNR | R1 | D3- | 36/36 | 1 | degenerate [1, 1] (no spread across the resampled clusters) | 12/12 |
| train | babble 20 dB SNR | R1 | D4- | 27/33 | 0.818 | 95% [0.667, 1] | 8/11 |
| train | babble 20 dB SNR | R1 | D5- | 110/135 | 0.815 | 95% [0.723, 0.906] | 33/45 |
| train | babble 20 dB SNR | R1 | D6- | 23/30 | 0.767 | 95% [0.567, 0.967] | 6/10 |
| train | babble 20 dB SNR | R1 | D9- | 9/9 | 1 | per recording: gwbush_911_2001__extra_L2A 1, harris_uncsw_2021__extra_botched_D1 1, hclinton_tomorrow_2010__extra_L3A 1; range [1, 1] | 3/3 |
| train | babble 20 dB SNR | R2 | D2+ | 1/12 | 0.0833 | per recording: greenman_reagan__extra_botched_D2 0.167, greenman_reagan__extra_x6_L3 0, greenman_reagan__x3_L3 0; range [0, 0.167] | 0/4 |
| train | babble 20 dB SNR | R2 | D5- | 4/12 | 0.333 | per recording: greenman_reagan__G5 0.667, greenman_reagan__extra_x1_L2 0, greenman_reagan__x3_L3 0; range [0, 0.667] | 1/4 |
| val | gain +6 dB | R1 | D1+ | 4/4 | 1 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1; range [1, 1] | 4/4 |
| val | gain +6 dB | R1 | D1- | 9/9 | 1 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1; range [1, 1] | 9/9 |
| val | gain +6 dB | R1 | D2+ | 13/13 | 1 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1; range [1, 1] | 13/13 |
| val | gain +6 dB | R1 | D2- | 17/17 | 1 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1; range [1, 1] | 17/17 |
| val | gain +6 dB | R1 | D3- | 5/5 | 1 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1; range [1, 1] | 5/5 |
| val | gain +6 dB | R1 | D4- | 7/7 | 1 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1; range [1, 1] | 7/7 |
| val | gain +6 dB | R1 | D5- | 11/11 | 1 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1; range [1, 1] | 11/11 |
| val | gain +6 dB | R1 | D6- | 4/4 | 1 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1; range [1, 1] | 4/4 |
| val | gain +6 dB | R1 | D9- | 3/3 | 1 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1; range [1, 1] | 3/3 |
| val | gain -6 dB | R1 | D1+ | 4/4 | 1 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1; range [1, 1] | 4/4 |
| val | gain -6 dB | R1 | D1- | 9/9 | 1 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1; range [1, 1] | 9/9 |
| val | gain -6 dB | R1 | D2+ | 13/13 | 1 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1; range [1, 1] | 13/13 |
| val | gain -6 dB | R1 | D2- | 17/17 | 1 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1; range [1, 1] | 17/17 |
| val | gain -6 dB | R1 | D3- | 5/5 | 1 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1; range [1, 1] | 5/5 |
| val | gain -6 dB | R1 | D4- | 7/7 | 1 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1; range [1, 1] | 7/7 |
| val | gain -6 dB | R1 | D5- | 11/11 | 1 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1; range [1, 1] | 11/11 |
| val | gain -6 dB | R1 | D6- | 4/4 | 1 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1; range [1, 1] | 4/4 |
| val | gain -6 dB | R1 | D9- | 3/3 | 1 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1; range [1, 1] | 3/3 |
| val | low-pass 3.4 kHz | R1 | D1+ | 4/4 | 1 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1; range [1, 1] | 4/4 |
| val | low-pass 3.4 kHz | R1 | D1- | 9/9 | 1 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1; range [1, 1] | 9/9 |
| val | low-pass 3.4 kHz | R1 | D2+ | 13/13 | 1 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1; range [1, 1] | 13/13 |
| val | low-pass 3.4 kHz | R1 | D2- | 17/17 | 1 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1; range [1, 1] | 17/17 |
| val | low-pass 3.4 kHz | R1 | D3- | 5/5 | 1 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1; range [1, 1] | 5/5 |
| val | low-pass 3.4 kHz | R1 | D4- | 7/7 | 1 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1; range [1, 1] | 7/7 |
| val | low-pass 3.4 kHz | R1 | D5- | 11/11 | 1 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1; range [1, 1] | 11/11 |
| val | low-pass 3.4 kHz | R1 | D6- | 1/4 | 0.25 | per speaker: eisenhower_farewell_1961 0.5, lbush_radio_2001 0; range [0, 0.5] | 1/4 |
| val | low-pass 3.4 kHz | R1 | D9- | 3/3 | 1 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1; range [1, 1] | 3/3 |
| val | white noise 20 dB SNR | R1 | D1+ | 12/12 | 1 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1; range [1, 1] | 4/4 |
| val | white noise 20 dB SNR | R1 | D1- | 26/27 | 0.963 | per speaker: eisenhower_farewell_1961 0.933, lbush_radio_2001 1; range [0.933, 1] | 8/9 |
| val | white noise 20 dB SNR | R1 | D2+ | 39/39 | 1 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1; range [1, 1] | 13/13 |
| val | white noise 20 dB SNR | R1 | D2- | 51/51 | 1 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1; range [1, 1] | 17/17 |
| val | white noise 20 dB SNR | R1 | D3- | 15/15 | 1 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1; range [1, 1] | 5/5 |
| val | white noise 20 dB SNR | R1 | D4- | 21/21 | 1 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1; range [1, 1] | 7/7 |
| val | white noise 20 dB SNR | R1 | D5- | 26/33 | 0.788 | per speaker: eisenhower_farewell_1961 0.917, lbush_radio_2001 0.714; range [0.714, 0.917] | 8/11 |
| val | white noise 20 dB SNR | R1 | D6- | 1/12 | 0.0833 | per speaker: eisenhower_farewell_1961 0.167, lbush_radio_2001 0; range [0, 0.167] | 0/4 |
| val | white noise 20 dB SNR | R1 | D9- | 8/9 | 0.889 | per speaker: eisenhower_farewell_1961 0.833, lbush_radio_2001 1; range [0.833, 1] | 2/3 |
| val | MP3 64 kbit/s | R1 | D1+ | 4/4 | 1 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1; range [1, 1] | 4/4 |
| val | MP3 64 kbit/s | R1 | D1- | 9/9 | 1 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1; range [1, 1] | 9/9 |
| val | MP3 64 kbit/s | R1 | D2+ | 13/13 | 1 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1; range [1, 1] | 13/13 |
| val | MP3 64 kbit/s | R1 | D2- | 17/17 | 1 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1; range [1, 1] | 17/17 |
| val | MP3 64 kbit/s | R1 | D3- | 5/5 | 1 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1; range [1, 1] | 5/5 |
| val | MP3 64 kbit/s | R1 | D4- | 7/7 | 1 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1; range [1, 1] | 7/7 |
| val | MP3 64 kbit/s | R1 | D5- | 11/11 | 1 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1; range [1, 1] | 11/11 |
| val | MP3 64 kbit/s | R1 | D6- | 4/4 | 1 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1; range [1, 1] | 4/4 |
| val | MP3 64 kbit/s | R1 | D9- | 3/3 | 1 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1; range [1, 1] | 3/3 |
| val | dynamic-range compression | R1 | D1+ | 4/4 | 1 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1; range [1, 1] | 4/4 |
| val | dynamic-range compression | R1 | D1- | 7/9 | 0.778 | per speaker: eisenhower_farewell_1961 0.6, lbush_radio_2001 1; range [0.6, 1] | 7/9 |
| val | dynamic-range compression | R1 | D2+ | 12/13 | 0.923 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 0.857; range [0.857, 1] | 12/13 |
| val | dynamic-range compression | R1 | D2- | 17/17 | 1 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1; range [1, 1] | 17/17 |
| val | dynamic-range compression | R1 | D3- | 5/5 | 1 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1; range [1, 1] | 5/5 |
| val | dynamic-range compression | R1 | D4- | 5/7 | 0.714 | per speaker: eisenhower_farewell_1961 0.333, lbush_radio_2001 1; range [0.333, 1] | 5/7 |
| val | dynamic-range compression | R1 | D5- | 2/11 | 0.182 | per speaker: eisenhower_farewell_1961 0, lbush_radio_2001 0.286; range [0, 0.286] | 2/11 |
| val | dynamic-range compression | R1 | D6- | 3/4 | 0.75 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 0.5; range [0.5, 1] | 3/4 |
| val | dynamic-range compression | R1 | D9- | 2/3 | 0.667 | per speaker: eisenhower_farewell_1961 0.5, lbush_radio_2001 1; range [0.5, 1] | 2/3 |
| val | room reverb RT60 0.4 s | R1 | D1+ | 12/12 | 1 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1; range [1, 1] | 4/4 |
| val | room reverb RT60 0.4 s | R1 | D1- | 25/27 | 0.926 | per speaker: eisenhower_farewell_1961 0.867, lbush_radio_2001 1; range [0.867, 1] | 8/9 |
| val | room reverb RT60 0.4 s | R1 | D2+ | 36/39 | 0.923 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 0.857; range [0.857, 1] | 12/13 |
| val | room reverb RT60 0.4 s | R1 | D2- | 51/51 | 1 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1; range [1, 1] | 17/17 |
| val | room reverb RT60 0.4 s | R1 | D3- | 15/15 | 1 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1; range [1, 1] | 5/5 |
| val | room reverb RT60 0.4 s | R1 | D4- | 21/21 | 1 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1; range [1, 1] | 7/7 |
| val | room reverb RT60 0.4 s | R1 | D5- | 32/33 | 0.97 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 0.952; range [0.952, 1] | 10/11 |
| val | room reverb RT60 0.4 s | R1 | D6- | 9/12 | 0.75 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 0.5; range [0.5, 1] | 3/4 |
| val | room reverb RT60 0.4 s | R1 | D9- | 7/9 | 0.778 | per speaker: eisenhower_farewell_1961 0.667, lbush_radio_2001 1; range [0.667, 1] | 2/3 |
| val | phone band + mu-law (participant only) | R1 | D1+ | 4/4 | 1 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1; range [1, 1] | 4/4 |
| val | phone band + mu-law (participant only) | R1 | D1- | 9/9 | 1 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1; range [1, 1] | 9/9 |
| val | phone band + mu-law (participant only) | R1 | D2+ | 12/13 | 0.923 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 0.857; range [0.857, 1] | 12/13 |
| val | phone band + mu-law (participant only) | R1 | D2- | 17/17 | 1 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1; range [1, 1] | 17/17 |
| val | phone band + mu-law (participant only) | R1 | D3- | 5/5 | 1 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1; range [1, 1] | 5/5 |
| val | phone band + mu-law (participant only) | R1 | D4- | 7/7 | 1 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1; range [1, 1] | 7/7 |
| val | phone band + mu-law (participant only) | R1 | D5- | 6/11 | 0.545 | per speaker: eisenhower_farewell_1961 0.5, lbush_radio_2001 0.571; range [0.5, 0.571] | 6/11 |
| val | phone band + mu-law (participant only) | R1 | D6- | 2/4 | 0.5 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 0; range [0, 1] | 2/4 |
| val | phone band + mu-law (participant only) | R1 | D9- | 3/3 | 1 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1; range [1, 1] | 3/3 |
| val | WORLD speaker transform | R1 | D1+ | 4/4 | 1 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1; range [1, 1] | 4/4 |
| val | WORLD speaker transform | R1 | D1- | 9/9 | 1 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1; range [1, 1] | 9/9 |
| val | WORLD speaker transform | R1 | D2+ | 12/13 | 0.923 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 0.857; range [0.857, 1] | 12/13 |
| val | WORLD speaker transform | R1 | D2- | 17/17 | 1 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1; range [1, 1] | 17/17 |
| val | WORLD speaker transform | R1 | D3- | 5/5 | 1 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1; range [1, 1] | 5/5 |
| val | WORLD speaker transform | R1 | D4- | 7/7 | 1 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1; range [1, 1] | 7/7 |
| val | WORLD speaker transform | R1 | D5- | 11/11 | 1 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1; range [1, 1] | 11/11 |
| val | WORLD speaker transform | R1 | D6- | 3/4 | 0.75 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 0.5; range [0.5, 1] | 3/4 |
| val | WORLD speaker transform | R1 | D9- | 2/3 | 0.667 | per speaker: eisenhower_farewell_1961 0.5, lbush_radio_2001 1; range [0.5, 1] | 2/3 |
| val | babble 10 dB SNR | R1 | D1+ | 9/12 | 0.75 | per speaker: eisenhower_farewell_1961 0.667, lbush_radio_2001 0.833; range [0.667, 0.833] | 1/4 |
| val | babble 10 dB SNR | R1 | D1- | 22/27 | 0.815 | per speaker: eisenhower_farewell_1961 0.667, lbush_radio_2001 1; range [0.667, 1] | 7/9 |
| val | babble 10 dB SNR | R1 | D2+ | 5/39 | 0.128 | per speaker: eisenhower_farewell_1961 0.111, lbush_radio_2001 0.143; range [0.111, 0.143] | 0/13 |
| val | babble 10 dB SNR | R1 | D2- | 51/51 | 1 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1; range [1, 1] | 17/17 |
| val | babble 10 dB SNR | R1 | D3- | 11/15 | 0.733 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 0.333; range [0.333, 1] | 3/5 |
| val | babble 10 dB SNR | R1 | D4- | 20/21 | 0.952 | per speaker: eisenhower_farewell_1961 0.889, lbush_radio_2001 1; range [0.889, 1] | 6/7 |
| val | babble 10 dB SNR | R1 | D5- | 16/33 | 0.485 | per speaker: eisenhower_farewell_1961 0.583, lbush_radio_2001 0.429; range [0.429, 0.583] | 2/11 |
| val | babble 10 dB SNR | R1 | D6- | 1/12 | 0.0833 | per speaker: eisenhower_farewell_1961 0.167, lbush_radio_2001 0; range [0, 0.167] | 0/4 |
| val | babble 10 dB SNR | R1 | D9- | 8/9 | 0.889 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 0.667; range [0.667, 1] | 2/3 |
| val | babble 20 dB SNR | R1 | D1+ | 12/12 | 1 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1; range [1, 1] | 4/4 |
| val | babble 20 dB SNR | R1 | D1- | 24/27 | 0.889 | per speaker: eisenhower_farewell_1961 0.8, lbush_radio_2001 1; range [0.8, 1] | 8/9 |
| val | babble 20 dB SNR | R1 | D2+ | 36/39 | 0.923 | per speaker: eisenhower_farewell_1961 0.889, lbush_radio_2001 0.952; range [0.889, 0.952] | 11/13 |
| val | babble 20 dB SNR | R1 | D2- | 51/51 | 1 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1; range [1, 1] | 17/17 |
| val | babble 20 dB SNR | R1 | D3- | 15/15 | 1 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1; range [1, 1] | 5/5 |
| val | babble 20 dB SNR | R1 | D4- | 21/21 | 1 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1; range [1, 1] | 7/7 |
| val | babble 20 dB SNR | R1 | D5- | 23/33 | 0.697 | per speaker: eisenhower_farewell_1961 0.833, lbush_radio_2001 0.619; range [0.619, 0.833] | 6/11 |
| val | babble 20 dB SNR | R1 | D6- | 4/12 | 0.333 | per speaker: eisenhower_farewell_1961 0.667, lbush_radio_2001 0; range [0, 0.667] | 1/4 |
| val | babble 20 dB SNR | R1 | D9- | 8/9 | 0.889 | per speaker: eisenhower_farewell_1961 0.833, lbush_radio_2001 1; range [0.833, 1] | 2/3 |
| test | gain +6 dB | R1 | D1+ | 4/4 | 1 | per speaker: mobama_weekly_2014 1, nixon_resignation_1974 1; range [1, 1] | 4/4 |
| test | gain +6 dB | R1 | D1- | 10/10 | 1 | per speaker: mobama_weekly_2014 1, nixon_resignation_1974 1; range [1, 1] | 10/10 |
| test | gain +6 dB | R1 | D2+ | 13/13 | 1 | per speaker: mobama_weekly_2014 1, nixon_resignation_1974 1; range [1, 1] | 13/13 |
| test | gain +6 dB | R1 | D2- | 19/19 | 1 | per speaker: mobama_weekly_2014 1, nixon_resignation_1974 1; range [1, 1] | 19/19 |
| test | gain +6 dB | R1 | D3- | 2/2 | 1 | per speaker: nixon_resignation_1974 1; range [1, 1] | 2/2 |
| test | gain +6 dB | R1 | D4- | 6/6 | 1 | per speaker: mobama_weekly_2014 1, nixon_resignation_1974 1; range [1, 1] | 6/6 |
| test | gain +6 dB | R1 | D5- | 19/19 | 1 | per speaker: mobama_weekly_2014 1, nixon_resignation_1974 1; range [1, 1] | 19/19 |
| test | gain +6 dB | R1 | D6- | 4/4 | 1 | per speaker: mobama_weekly_2014 1, nixon_resignation_1974 1; range [1, 1] | 4/4 |
| test | gain +6 dB | R1 | D9- | 1/1 | 1 | per speaker: nixon_resignation_1974 1; range [1, 1] | 1/1 |
| test | gain -6 dB | R1 | D1+ | 4/4 | 1 | per speaker: mobama_weekly_2014 1, nixon_resignation_1974 1; range [1, 1] | 4/4 |
| test | gain -6 dB | R1 | D1- | 10/10 | 1 | per speaker: mobama_weekly_2014 1, nixon_resignation_1974 1; range [1, 1] | 10/10 |
| test | gain -6 dB | R1 | D2+ | 13/13 | 1 | per speaker: mobama_weekly_2014 1, nixon_resignation_1974 1; range [1, 1] | 13/13 |
| test | gain -6 dB | R1 | D2- | 19/19 | 1 | per speaker: mobama_weekly_2014 1, nixon_resignation_1974 1; range [1, 1] | 19/19 |
| test | gain -6 dB | R1 | D3- | 2/2 | 1 | per speaker: nixon_resignation_1974 1; range [1, 1] | 2/2 |
| test | gain -6 dB | R1 | D4- | 6/6 | 1 | per speaker: mobama_weekly_2014 1, nixon_resignation_1974 1; range [1, 1] | 6/6 |
| test | gain -6 dB | R1 | D5- | 19/19 | 1 | per speaker: mobama_weekly_2014 1, nixon_resignation_1974 1; range [1, 1] | 19/19 |
| test | gain -6 dB | R1 | D6- | 4/4 | 1 | per speaker: mobama_weekly_2014 1, nixon_resignation_1974 1; range [1, 1] | 4/4 |
| test | gain -6 dB | R1 | D9- | 1/1 | 1 | per speaker: nixon_resignation_1974 1; range [1, 1] | 1/1 |
| test | low-pass 3.4 kHz | R1 | D1+ | 4/4 | 1 | per speaker: mobama_weekly_2014 1, nixon_resignation_1974 1; range [1, 1] | 4/4 |
| test | low-pass 3.4 kHz | R1 | D1- | 10/10 | 1 | per speaker: mobama_weekly_2014 1, nixon_resignation_1974 1; range [1, 1] | 10/10 |
| test | low-pass 3.4 kHz | R1 | D2+ | 13/13 | 1 | per speaker: mobama_weekly_2014 1, nixon_resignation_1974 1; range [1, 1] | 13/13 |
| test | low-pass 3.4 kHz | R1 | D2- | 18/19 | 0.947 | per speaker: mobama_weekly_2014 0.889, nixon_resignation_1974 1; range [0.889, 1] | 18/19 |
| test | low-pass 3.4 kHz | R1 | D3- | 2/2 | 1 | per speaker: nixon_resignation_1974 1; range [1, 1] | 2/2 |
| test | low-pass 3.4 kHz | R1 | D4- | 5/6 | 0.833 | per speaker: mobama_weekly_2014 1, nixon_resignation_1974 0; range [0, 1] | 5/6 |
| test | low-pass 3.4 kHz | R1 | D5- | 17/19 | 0.895 | per speaker: mobama_weekly_2014 0.778, nixon_resignation_1974 1; range [0.778, 1] | 17/19 |
| test | low-pass 3.4 kHz | R1 | D6- | 3/4 | 0.75 | per speaker: mobama_weekly_2014 0.5, nixon_resignation_1974 1; range [0.5, 1] | 3/4 |
| test | low-pass 3.4 kHz | R1 | D9- | 1/1 | 1 | per speaker: nixon_resignation_1974 1; range [1, 1] | 1/1 |
| test | white noise 20 dB SNR | R1 | D1+ | 12/12 | 1 | per speaker: mobama_weekly_2014 1, nixon_resignation_1974 1; range [1, 1] | 4/4 |
| test | white noise 20 dB SNR | R1 | D1- | 30/30 | 1 | per speaker: mobama_weekly_2014 1, nixon_resignation_1974 1; range [1, 1] | 10/10 |
| test | white noise 20 dB SNR | R1 | D2+ | 39/39 | 1 | per speaker: mobama_weekly_2014 1, nixon_resignation_1974 1; range [1, 1] | 13/13 |
| test | white noise 20 dB SNR | R1 | D2- | 54/57 | 0.947 | per speaker: mobama_weekly_2014 0.889, nixon_resignation_1974 1; range [0.889, 1] | 18/19 |
| test | white noise 20 dB SNR | R1 | D3- | 6/6 | 1 | per speaker: nixon_resignation_1974 1; range [1, 1] | 2/2 |
| test | white noise 20 dB SNR | R1 | D4- | 18/18 | 1 | per speaker: mobama_weekly_2014 1, nixon_resignation_1974 1; range [1, 1] | 6/6 |
| test | white noise 20 dB SNR | R1 | D5- | 48/57 | 0.842 | per speaker: mobama_weekly_2014 0.778, nixon_resignation_1974 0.9; range [0.778, 0.9] | 16/19 |
| test | white noise 20 dB SNR | R1 | D6- | 3/12 | 0.25 | per speaker: mobama_weekly_2014 0.5, nixon_resignation_1974 0; range [0, 0.5] | 1/4 |
| test | white noise 20 dB SNR | R1 | D9- | 3/3 | 1 | per speaker: nixon_resignation_1974 1; range [1, 1] | 1/1 |
| test | MP3 64 kbit/s | R1 | D1+ | 4/4 | 1 | per speaker: mobama_weekly_2014 1, nixon_resignation_1974 1; range [1, 1] | 4/4 |
| test | MP3 64 kbit/s | R1 | D1- | 10/10 | 1 | per speaker: mobama_weekly_2014 1, nixon_resignation_1974 1; range [1, 1] | 10/10 |
| test | MP3 64 kbit/s | R1 | D2+ | 13/13 | 1 | per speaker: mobama_weekly_2014 1, nixon_resignation_1974 1; range [1, 1] | 13/13 |
| test | MP3 64 kbit/s | R1 | D2- | 19/19 | 1 | per speaker: mobama_weekly_2014 1, nixon_resignation_1974 1; range [1, 1] | 19/19 |
| test | MP3 64 kbit/s | R1 | D3- | 2/2 | 1 | per speaker: nixon_resignation_1974 1; range [1, 1] | 2/2 |
| test | MP3 64 kbit/s | R1 | D4- | 6/6 | 1 | per speaker: mobama_weekly_2014 1, nixon_resignation_1974 1; range [1, 1] | 6/6 |
| test | MP3 64 kbit/s | R1 | D5- | 19/19 | 1 | per speaker: mobama_weekly_2014 1, nixon_resignation_1974 1; range [1, 1] | 19/19 |
| test | MP3 64 kbit/s | R1 | D6- | 4/4 | 1 | per speaker: mobama_weekly_2014 1, nixon_resignation_1974 1; range [1, 1] | 4/4 |
| test | MP3 64 kbit/s | R1 | D9- | 1/1 | 1 | per speaker: nixon_resignation_1974 1; range [1, 1] | 1/1 |
| test | dynamic-range compression | R1 | D1+ | 4/4 | 1 | per speaker: mobama_weekly_2014 1, nixon_resignation_1974 1; range [1, 1] | 4/4 |
| test | dynamic-range compression | R1 | D1- | 10/10 | 1 | per speaker: mobama_weekly_2014 1, nixon_resignation_1974 1; range [1, 1] | 10/10 |
| test | dynamic-range compression | R1 | D2+ | 13/13 | 1 | per speaker: mobama_weekly_2014 1, nixon_resignation_1974 1; range [1, 1] | 13/13 |
| test | dynamic-range compression | R1 | D2- | 19/19 | 1 | per speaker: mobama_weekly_2014 1, nixon_resignation_1974 1; range [1, 1] | 19/19 |
| test | dynamic-range compression | R1 | D3- | 2/2 | 1 | per speaker: nixon_resignation_1974 1; range [1, 1] | 2/2 |
| test | dynamic-range compression | R1 | D4- | 2/6 | 0.333 | per speaker: mobama_weekly_2014 0.4, nixon_resignation_1974 0; range [0, 0.4] | 2/6 |
| test | dynamic-range compression | R1 | D5- | 4/19 | 0.21 | per speaker: mobama_weekly_2014 0.222, nixon_resignation_1974 0.2; range [0.2, 0.222] | 4/19 |
| test | dynamic-range compression | R1 | D6- | 4/4 | 1 | per speaker: mobama_weekly_2014 1, nixon_resignation_1974 1; range [1, 1] | 4/4 |
| test | dynamic-range compression | R1 | D9- | 1/1 | 1 | per speaker: nixon_resignation_1974 1; range [1, 1] | 1/1 |
| test | room reverb RT60 0.4 s | R1 | D1+ | 12/12 | 1 | per speaker: mobama_weekly_2014 1, nixon_resignation_1974 1; range [1, 1] | 4/4 |
| test | room reverb RT60 0.4 s | R1 | D1- | 29/30 | 0.967 | per speaker: mobama_weekly_2014 1, nixon_resignation_1974 0.933; range [0.933, 1] | 9/10 |
| test | room reverb RT60 0.4 s | R1 | D2+ | 39/39 | 1 | per speaker: mobama_weekly_2014 1, nixon_resignation_1974 1; range [1, 1] | 13/13 |
| test | room reverb RT60 0.4 s | R1 | D2- | 57/57 | 1 | per speaker: mobama_weekly_2014 1, nixon_resignation_1974 1; range [1, 1] | 19/19 |
| test | room reverb RT60 0.4 s | R1 | D3- | 5/6 | 0.833 | per speaker: nixon_resignation_1974 0.833; range [0.833, 0.833] | 1/2 |
| test | room reverb RT60 0.4 s | R1 | D4- | 18/18 | 1 | per speaker: mobama_weekly_2014 1, nixon_resignation_1974 1; range [1, 1] | 6/6 |
| test | room reverb RT60 0.4 s | R1 | D5- | 57/57 | 1 | per speaker: mobama_weekly_2014 1, nixon_resignation_1974 1; range [1, 1] | 19/19 |
| test | room reverb RT60 0.4 s | R1 | D6- | 12/12 | 1 | per speaker: mobama_weekly_2014 1, nixon_resignation_1974 1; range [1, 1] | 4/4 |
| test | room reverb RT60 0.4 s | R1 | D9- | 2/3 | 0.667 | per speaker: nixon_resignation_1974 0.667; range [0.667, 0.667] | 0/1 |
| test | phone band + mu-law (participant only) | R1 | D1+ | 4/4 | 1 | per speaker: mobama_weekly_2014 1, nixon_resignation_1974 1; range [1, 1] | 4/4 |
| test | phone band + mu-law (participant only) | R1 | D1- | 9/10 | 0.9 | per speaker: mobama_weekly_2014 1, nixon_resignation_1974 0.8; range [0.8, 1] | 9/10 |
| test | phone band + mu-law (participant only) | R1 | D2+ | 13/13 | 1 | per speaker: mobama_weekly_2014 1, nixon_resignation_1974 1; range [1, 1] | 13/13 |
| test | phone band + mu-law (participant only) | R1 | D2- | 18/19 | 0.947 | per speaker: mobama_weekly_2014 0.889, nixon_resignation_1974 1; range [0.889, 1] | 18/19 |
| test | phone band + mu-law (participant only) | R1 | D3- | 0/2 | 0 | per speaker: nixon_resignation_1974 0; range [0, 0] | 0/2 |
| test | phone band + mu-law (participant only) | R1 | D4- | 5/6 | 0.833 | per speaker: mobama_weekly_2014 1, nixon_resignation_1974 0; range [0, 1] | 5/6 |
| test | phone band + mu-law (participant only) | R1 | D5- | 15/19 | 0.789 | per speaker: mobama_weekly_2014 0.556, nixon_resignation_1974 1; range [0.556, 1] | 15/19 |
| test | phone band + mu-law (participant only) | R1 | D6- | 3/4 | 0.75 | per speaker: mobama_weekly_2014 0.5, nixon_resignation_1974 1; range [0.5, 1] | 3/4 |
| test | phone band + mu-law (participant only) | R1 | D9- | 1/1 | 1 | per speaker: nixon_resignation_1974 1; range [1, 1] | 1/1 |
| test | WORLD speaker transform | R1 | D1+ | 4/4 | 1 | per speaker: mobama_weekly_2014 1, nixon_resignation_1974 1; range [1, 1] | 4/4 |
| test | WORLD speaker transform | R1 | D1- | 10/10 | 1 | per speaker: mobama_weekly_2014 1, nixon_resignation_1974 1; range [1, 1] | 10/10 |
| test | WORLD speaker transform | R1 | D2+ | 13/13 | 1 | per speaker: mobama_weekly_2014 1, nixon_resignation_1974 1; range [1, 1] | 13/13 |
| test | WORLD speaker transform | R1 | D2- | 19/19 | 1 | per speaker: mobama_weekly_2014 1, nixon_resignation_1974 1; range [1, 1] | 19/19 |
| test | WORLD speaker transform | R1 | D3- | 2/2 | 1 | per speaker: nixon_resignation_1974 1; range [1, 1] | 2/2 |
| test | WORLD speaker transform | R1 | D4- | 5/6 | 0.833 | per speaker: mobama_weekly_2014 0.8, nixon_resignation_1974 1; range [0.8, 1] | 5/6 |
| test | WORLD speaker transform | R1 | D5- | 19/19 | 1 | per speaker: mobama_weekly_2014 1, nixon_resignation_1974 1; range [1, 1] | 19/19 |
| test | WORLD speaker transform | R1 | D6- | 4/4 | 1 | per speaker: mobama_weekly_2014 1, nixon_resignation_1974 1; range [1, 1] | 4/4 |
| test | WORLD speaker transform | R1 | D9- | 1/1 | 1 | per speaker: nixon_resignation_1974 1; range [1, 1] | 1/1 |
| test | babble 10 dB SNR | R1 | D1+ | 6/12 | 0.5 | per speaker: mobama_weekly_2014 0.5, nixon_resignation_1974 0.5; range [0.5, 0.5] | 2/4 |
| test | babble 10 dB SNR | R1 | D1- | 21/30 | 0.7 | per speaker: mobama_weekly_2014 0.8, nixon_resignation_1974 0.6; range [0.6, 0.8] | 7/10 |
| test | babble 10 dB SNR | R1 | D2+ | 4/39 | 0.103 | per speaker: mobama_weekly_2014 0.167, nixon_resignation_1974 0.048; range [0.048, 0.167] | 0/13 |
| test | babble 10 dB SNR | R1 | D2- | 57/57 | 1 | per speaker: mobama_weekly_2014 1, nixon_resignation_1974 1; range [1, 1] | 19/19 |
| test | babble 10 dB SNR | R1 | D3- | 4/6 | 0.667 | per speaker: nixon_resignation_1974 0.667; range [0.667, 0.667] | 1/2 |
| test | babble 10 dB SNR | R1 | D4- | 13/18 | 0.722 | per speaker: mobama_weekly_2014 0.733, nixon_resignation_1974 0.667; range [0.667, 0.733] | 3/6 |
| test | babble 10 dB SNR | R1 | D5- | 30/57 | 0.526 | per speaker: mobama_weekly_2014 0.741, nixon_resignation_1974 0.333; range [0.333, 0.741] | 6/19 |
| test | babble 10 dB SNR | R1 | D6- | 3/12 | 0.25 | per speaker: mobama_weekly_2014 0.5, nixon_resignation_1974 0; range [0, 0.5] | 1/4 |
| test | babble 10 dB SNR | R1 | D9- | 3/3 | 1 | per speaker: nixon_resignation_1974 1; range [1, 1] | 1/1 |
| test | babble 20 dB SNR | R1 | D1+ | 11/12 | 0.917 | per speaker: mobama_weekly_2014 1, nixon_resignation_1974 0.833; range [0.833, 1] | 3/4 |
| test | babble 20 dB SNR | R1 | D1- | 24/30 | 0.8 | per speaker: mobama_weekly_2014 1, nixon_resignation_1974 0.6; range [0.6, 1] | 8/10 |
| test | babble 20 dB SNR | R1 | D2+ | 24/39 | 0.615 | per speaker: mobama_weekly_2014 0.944, nixon_resignation_1974 0.333; range [0.333, 0.944] | 5/13 |
| test | babble 20 dB SNR | R1 | D2- | 55/57 | 0.965 | per speaker: mobama_weekly_2014 0.926, nixon_resignation_1974 1; range [0.926, 1] | 18/19 |
| test | babble 20 dB SNR | R1 | D3- | 6/6 | 1 | per speaker: nixon_resignation_1974 1; range [1, 1] | 2/2 |
| test | babble 20 dB SNR | R1 | D4- | 17/18 | 0.944 | per speaker: mobama_weekly_2014 1, nixon_resignation_1974 0.667; range [0.667, 1] | 5/6 |
| test | babble 20 dB SNR | R1 | D5- | 49/57 | 0.86 | per speaker: mobama_weekly_2014 0.889, nixon_resignation_1974 0.833; range [0.833, 0.889] | 14/19 |
| test | babble 20 dB SNR | R1 | D6- | 12/12 | 1 | per speaker: mobama_weekly_2014 1, nixon_resignation_1974 1; range [1, 1] | 4/4 |
| test | babble 20 dB SNR | R1 | D9- | 2/3 | 0.667 | per speaker: nixon_resignation_1974 0.667; range [0.667, 0.667] | 0/1 |
| val+test | gain +6 dB | R1 | D1+ | 8/8 | 1 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1, mobama_weekly_2014 1, nixon_resignation_1974 1; range [1, 1] | 8/8 |
| val+test | gain +6 dB | R1 | D1- | 19/19 | 1 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1, mobama_weekly_2014 1, nixon_resignation_1974 1; range [1, 1] | 19/19 |
| val+test | gain +6 dB | R1 | D2+ | 26/26 | 1 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1, mobama_weekly_2014 1, nixon_resignation_1974 1; range [1, 1] | 26/26 |
| val+test | gain +6 dB | R1 | D2- | 36/36 | 1 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1, mobama_weekly_2014 1, nixon_resignation_1974 1; range [1, 1] | 36/36 |
| val+test | gain +6 dB | R1 | D3- | 7/7 | 1 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1, nixon_resignation_1974 1; range [1, 1] | 7/7 |
| val+test | gain +6 dB | R1 | D4- | 13/13 | 1 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1, mobama_weekly_2014 1, nixon_resignation_1974 1; range [1, 1] | 13/13 |
| val+test | gain +6 dB | R1 | D5- | 30/30 | 1 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1, mobama_weekly_2014 1, nixon_resignation_1974 1; range [1, 1] | 30/30 |
| val+test | gain +6 dB | R1 | D6- | 8/8 | 1 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1, mobama_weekly_2014 1, nixon_resignation_1974 1; range [1, 1] | 8/8 |
| val+test | gain +6 dB | R1 | D9- | 4/4 | 1 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1, nixon_resignation_1974 1; range [1, 1] | 4/4 |
| val+test | gain -6 dB | R1 | D1+ | 8/8 | 1 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1, mobama_weekly_2014 1, nixon_resignation_1974 1; range [1, 1] | 8/8 |
| val+test | gain -6 dB | R1 | D1- | 19/19 | 1 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1, mobama_weekly_2014 1, nixon_resignation_1974 1; range [1, 1] | 19/19 |
| val+test | gain -6 dB | R1 | D2+ | 26/26 | 1 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1, mobama_weekly_2014 1, nixon_resignation_1974 1; range [1, 1] | 26/26 |
| val+test | gain -6 dB | R1 | D2- | 36/36 | 1 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1, mobama_weekly_2014 1, nixon_resignation_1974 1; range [1, 1] | 36/36 |
| val+test | gain -6 dB | R1 | D3- | 7/7 | 1 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1, nixon_resignation_1974 1; range [1, 1] | 7/7 |
| val+test | gain -6 dB | R1 | D4- | 13/13 | 1 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1, mobama_weekly_2014 1, nixon_resignation_1974 1; range [1, 1] | 13/13 |
| val+test | gain -6 dB | R1 | D5- | 30/30 | 1 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1, mobama_weekly_2014 1, nixon_resignation_1974 1; range [1, 1] | 30/30 |
| val+test | gain -6 dB | R1 | D6- | 8/8 | 1 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1, mobama_weekly_2014 1, nixon_resignation_1974 1; range [1, 1] | 8/8 |
| val+test | gain -6 dB | R1 | D9- | 4/4 | 1 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1, nixon_resignation_1974 1; range [1, 1] | 4/4 |
| val+test | low-pass 3.4 kHz | R1 | D1+ | 8/8 | 1 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1, mobama_weekly_2014 1, nixon_resignation_1974 1; range [1, 1] | 8/8 |
| val+test | low-pass 3.4 kHz | R1 | D1- | 19/19 | 1 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1, mobama_weekly_2014 1, nixon_resignation_1974 1; range [1, 1] | 19/19 |
| val+test | low-pass 3.4 kHz | R1 | D2+ | 26/26 | 1 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1, mobama_weekly_2014 1, nixon_resignation_1974 1; range [1, 1] | 26/26 |
| val+test | low-pass 3.4 kHz | R1 | D2- | 35/36 | 0.972 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1, mobama_weekly_2014 0.889, nixon_resignation_1974 1; range [0.889, 1] | 35/36 |
| val+test | low-pass 3.4 kHz | R1 | D3- | 7/7 | 1 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1, nixon_resignation_1974 1; range [1, 1] | 7/7 |
| val+test | low-pass 3.4 kHz | R1 | D4- | 12/13 | 0.923 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1, mobama_weekly_2014 1, nixon_resignation_1974 0; range [0, 1] | 12/13 |
| val+test | low-pass 3.4 kHz | R1 | D5- | 28/30 | 0.933 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1, mobama_weekly_2014 0.778, nixon_resignation_1974 1; range [0.778, 1] | 28/30 |
| val+test | low-pass 3.4 kHz | R1 | D6- | 4/8 | 0.5 | per speaker: eisenhower_farewell_1961 0.5, lbush_radio_2001 0, mobama_weekly_2014 0.5, nixon_resignation_1974 1; range [0, 1] | 4/8 |
| val+test | low-pass 3.4 kHz | R1 | D9- | 4/4 | 1 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1, nixon_resignation_1974 1; range [1, 1] | 4/4 |
| val+test | white noise 20 dB SNR | R1 | D1+ | 24/24 | 1 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1, mobama_weekly_2014 1, nixon_resignation_1974 1; range [1, 1] | 8/8 |
| val+test | white noise 20 dB SNR | R1 | D1- | 56/57 | 0.983 | per speaker: eisenhower_farewell_1961 0.933, lbush_radio_2001 1, mobama_weekly_2014 1, nixon_resignation_1974 1; range [0.933, 1] | 18/19 |
| val+test | white noise 20 dB SNR | R1 | D2+ | 78/78 | 1 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1, mobama_weekly_2014 1, nixon_resignation_1974 1; range [1, 1] | 26/26 |
| val+test | white noise 20 dB SNR | R1 | D2- | 105/108 | 0.972 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1, mobama_weekly_2014 0.889, nixon_resignation_1974 1; range [0.889, 1] | 35/36 |
| val+test | white noise 20 dB SNR | R1 | D3- | 21/21 | 1 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1, nixon_resignation_1974 1; range [1, 1] | 7/7 |
| val+test | white noise 20 dB SNR | R1 | D4- | 39/39 | 1 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1, mobama_weekly_2014 1, nixon_resignation_1974 1; range [1, 1] | 13/13 |
| val+test | white noise 20 dB SNR | R1 | D5- | 74/90 | 0.822 | per speaker: eisenhower_farewell_1961 0.917, lbush_radio_2001 0.714, mobama_weekly_2014 0.778, nixon_resignation_1974 0.9; range [0.714, 0.917] | 24/30 |
| val+test | white noise 20 dB SNR | R1 | D6- | 4/24 | 0.167 | per speaker: eisenhower_farewell_1961 0.167, lbush_radio_2001 0, mobama_weekly_2014 0.5, nixon_resignation_1974 0; range [0, 0.5] | 1/8 |
| val+test | white noise 20 dB SNR | R1 | D9- | 11/12 | 0.917 | per speaker: eisenhower_farewell_1961 0.833, lbush_radio_2001 1, nixon_resignation_1974 1; range [0.833, 1] | 3/4 |
| val+test | MP3 64 kbit/s | R1 | D1+ | 8/8 | 1 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1, mobama_weekly_2014 1, nixon_resignation_1974 1; range [1, 1] | 8/8 |
| val+test | MP3 64 kbit/s | R1 | D1- | 19/19 | 1 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1, mobama_weekly_2014 1, nixon_resignation_1974 1; range [1, 1] | 19/19 |
| val+test | MP3 64 kbit/s | R1 | D2+ | 26/26 | 1 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1, mobama_weekly_2014 1, nixon_resignation_1974 1; range [1, 1] | 26/26 |
| val+test | MP3 64 kbit/s | R1 | D2- | 36/36 | 1 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1, mobama_weekly_2014 1, nixon_resignation_1974 1; range [1, 1] | 36/36 |
| val+test | MP3 64 kbit/s | R1 | D3- | 7/7 | 1 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1, nixon_resignation_1974 1; range [1, 1] | 7/7 |
| val+test | MP3 64 kbit/s | R1 | D4- | 13/13 | 1 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1, mobama_weekly_2014 1, nixon_resignation_1974 1; range [1, 1] | 13/13 |
| val+test | MP3 64 kbit/s | R1 | D5- | 30/30 | 1 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1, mobama_weekly_2014 1, nixon_resignation_1974 1; range [1, 1] | 30/30 |
| val+test | MP3 64 kbit/s | R1 | D6- | 8/8 | 1 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1, mobama_weekly_2014 1, nixon_resignation_1974 1; range [1, 1] | 8/8 |
| val+test | MP3 64 kbit/s | R1 | D9- | 4/4 | 1 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1, nixon_resignation_1974 1; range [1, 1] | 4/4 |
| val+test | dynamic-range compression | R1 | D1+ | 8/8 | 1 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1, mobama_weekly_2014 1, nixon_resignation_1974 1; range [1, 1] | 8/8 |
| val+test | dynamic-range compression | R1 | D1- | 17/19 | 0.895 | per speaker: eisenhower_farewell_1961 0.6, lbush_radio_2001 1, mobama_weekly_2014 1, nixon_resignation_1974 1; range [0.6, 1] | 17/19 |
| val+test | dynamic-range compression | R1 | D2+ | 25/26 | 0.962 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 0.857, mobama_weekly_2014 1, nixon_resignation_1974 1; range [0.857, 1] | 25/26 |
| val+test | dynamic-range compression | R1 | D2- | 36/36 | 1 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1, mobama_weekly_2014 1, nixon_resignation_1974 1; range [1, 1] | 36/36 |
| val+test | dynamic-range compression | R1 | D3- | 7/7 | 1 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1, nixon_resignation_1974 1; range [1, 1] | 7/7 |
| val+test | dynamic-range compression | R1 | D4- | 7/13 | 0.538 | per speaker: eisenhower_farewell_1961 0.333, lbush_radio_2001 1, mobama_weekly_2014 0.4, nixon_resignation_1974 0; range [0, 1] | 7/13 |
| val+test | dynamic-range compression | R1 | D5- | 6/30 | 0.2 | per speaker: eisenhower_farewell_1961 0, lbush_radio_2001 0.286, mobama_weekly_2014 0.222, nixon_resignation_1974 0.2; range [0, 0.286] | 6/30 |
| val+test | dynamic-range compression | R1 | D6- | 7/8 | 0.875 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 0.5, mobama_weekly_2014 1, nixon_resignation_1974 1; range [0.5, 1] | 7/8 |
| val+test | dynamic-range compression | R1 | D9- | 3/4 | 0.75 | per speaker: eisenhower_farewell_1961 0.5, lbush_radio_2001 1, nixon_resignation_1974 1; range [0.5, 1] | 3/4 |
| val+test | room reverb RT60 0.4 s | R1 | D1+ | 24/24 | 1 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1, mobama_weekly_2014 1, nixon_resignation_1974 1; range [1, 1] | 8/8 |
| val+test | room reverb RT60 0.4 s | R1 | D1- | 54/57 | 0.947 | per speaker: eisenhower_farewell_1961 0.867, lbush_radio_2001 1, mobama_weekly_2014 1, nixon_resignation_1974 0.933; range [0.867, 1] | 17/19 |
| val+test | room reverb RT60 0.4 s | R1 | D2+ | 75/78 | 0.962 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 0.857, mobama_weekly_2014 1, nixon_resignation_1974 1; range [0.857, 1] | 25/26 |
| val+test | room reverb RT60 0.4 s | R1 | D2- | 108/108 | 1 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1, mobama_weekly_2014 1, nixon_resignation_1974 1; range [1, 1] | 36/36 |
| val+test | room reverb RT60 0.4 s | R1 | D3- | 20/21 | 0.952 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1, nixon_resignation_1974 0.833; range [0.833, 1] | 6/7 |
| val+test | room reverb RT60 0.4 s | R1 | D4- | 39/39 | 1 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1, mobama_weekly_2014 1, nixon_resignation_1974 1; range [1, 1] | 13/13 |
| val+test | room reverb RT60 0.4 s | R1 | D5- | 89/90 | 0.989 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 0.952, mobama_weekly_2014 1, nixon_resignation_1974 1; range [0.952, 1] | 29/30 |
| val+test | room reverb RT60 0.4 s | R1 | D6- | 21/24 | 0.875 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 0.5, mobama_weekly_2014 1, nixon_resignation_1974 1; range [0.5, 1] | 7/8 |
| val+test | room reverb RT60 0.4 s | R1 | D9- | 9/12 | 0.75 | per speaker: eisenhower_farewell_1961 0.667, lbush_radio_2001 1, nixon_resignation_1974 0.667; range [0.667, 1] | 2/4 |
| val+test | phone band + mu-law (participant only) | R1 | D1+ | 8/8 | 1 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1, mobama_weekly_2014 1, nixon_resignation_1974 1; range [1, 1] | 8/8 |
| val+test | phone band + mu-law (participant only) | R1 | D1- | 18/19 | 0.947 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1, mobama_weekly_2014 1, nixon_resignation_1974 0.8; range [0.8, 1] | 18/19 |
| val+test | phone band + mu-law (participant only) | R1 | D2+ | 25/26 | 0.962 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 0.857, mobama_weekly_2014 1, nixon_resignation_1974 1; range [0.857, 1] | 25/26 |
| val+test | phone band + mu-law (participant only) | R1 | D2- | 35/36 | 0.972 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1, mobama_weekly_2014 0.889, nixon_resignation_1974 1; range [0.889, 1] | 35/36 |
| val+test | phone band + mu-law (participant only) | R1 | D3- | 5/7 | 0.714 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1, nixon_resignation_1974 0; range [0, 1] | 5/7 |
| val+test | phone band + mu-law (participant only) | R1 | D4- | 12/13 | 0.923 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1, mobama_weekly_2014 1, nixon_resignation_1974 0; range [0, 1] | 12/13 |
| val+test | phone band + mu-law (participant only) | R1 | D5- | 21/30 | 0.7 | per speaker: eisenhower_farewell_1961 0.5, lbush_radio_2001 0.571, mobama_weekly_2014 0.556, nixon_resignation_1974 1; range [0.5, 1] | 21/30 |
| val+test | phone band + mu-law (participant only) | R1 | D6- | 5/8 | 0.625 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 0, mobama_weekly_2014 0.5, nixon_resignation_1974 1; range [0, 1] | 5/8 |
| val+test | phone band + mu-law (participant only) | R1 | D9- | 4/4 | 1 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1, nixon_resignation_1974 1; range [1, 1] | 4/4 |
| val+test | WORLD speaker transform | R1 | D1+ | 8/8 | 1 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1, mobama_weekly_2014 1, nixon_resignation_1974 1; range [1, 1] | 8/8 |
| val+test | WORLD speaker transform | R1 | D1- | 19/19 | 1 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1, mobama_weekly_2014 1, nixon_resignation_1974 1; range [1, 1] | 19/19 |
| val+test | WORLD speaker transform | R1 | D2+ | 25/26 | 0.962 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 0.857, mobama_weekly_2014 1, nixon_resignation_1974 1; range [0.857, 1] | 25/26 |
| val+test | WORLD speaker transform | R1 | D2- | 36/36 | 1 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1, mobama_weekly_2014 1, nixon_resignation_1974 1; range [1, 1] | 36/36 |
| val+test | WORLD speaker transform | R1 | D3- | 7/7 | 1 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1, nixon_resignation_1974 1; range [1, 1] | 7/7 |
| val+test | WORLD speaker transform | R1 | D4- | 12/13 | 0.923 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1, mobama_weekly_2014 0.8, nixon_resignation_1974 1; range [0.8, 1] | 12/13 |
| val+test | WORLD speaker transform | R1 | D5- | 30/30 | 1 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1, mobama_weekly_2014 1, nixon_resignation_1974 1; range [1, 1] | 30/30 |
| val+test | WORLD speaker transform | R1 | D6- | 7/8 | 0.875 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 0.5, mobama_weekly_2014 1, nixon_resignation_1974 1; range [0.5, 1] | 7/8 |
| val+test | WORLD speaker transform | R1 | D9- | 3/4 | 0.75 | per speaker: eisenhower_farewell_1961 0.5, lbush_radio_2001 1, nixon_resignation_1974 1; range [0.5, 1] | 3/4 |
| val+test | babble 10 dB SNR | R1 | D1+ | 15/24 | 0.625 | per speaker: eisenhower_farewell_1961 0.667, lbush_radio_2001 0.833, mobama_weekly_2014 0.5, nixon_resignation_1974 0.5; range [0.5, 0.833] | 3/8 |
| val+test | babble 10 dB SNR | R1 | D1- | 43/57 | 0.754 | per speaker: eisenhower_farewell_1961 0.667, lbush_radio_2001 1, mobama_weekly_2014 0.8, nixon_resignation_1974 0.6; range [0.6, 1] | 14/19 |
| val+test | babble 10 dB SNR | R1 | D2+ | 9/78 | 0.115 | per speaker: eisenhower_farewell_1961 0.111, lbush_radio_2001 0.143, mobama_weekly_2014 0.167, nixon_resignation_1974 0.048; range [0.048, 0.167] | 0/26 |
| val+test | babble 10 dB SNR | R1 | D2- | 108/108 | 1 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1, mobama_weekly_2014 1, nixon_resignation_1974 1; range [1, 1] | 36/36 |
| val+test | babble 10 dB SNR | R1 | D3- | 15/21 | 0.714 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 0.333, nixon_resignation_1974 0.667; range [0.333, 1] | 4/7 |
| val+test | babble 10 dB SNR | R1 | D4- | 33/39 | 0.846 | per speaker: eisenhower_farewell_1961 0.889, lbush_radio_2001 1, mobama_weekly_2014 0.733, nixon_resignation_1974 0.667; range [0.667, 1] | 9/13 |
| val+test | babble 10 dB SNR | R1 | D5- | 46/90 | 0.511 | per speaker: eisenhower_farewell_1961 0.583, lbush_radio_2001 0.429, mobama_weekly_2014 0.741, nixon_resignation_1974 0.333; range [0.333, 0.741] | 8/30 |
| val+test | babble 10 dB SNR | R1 | D6- | 4/24 | 0.167 | per speaker: eisenhower_farewell_1961 0.167, lbush_radio_2001 0, mobama_weekly_2014 0.5, nixon_resignation_1974 0; range [0, 0.5] | 1/8 |
| val+test | babble 10 dB SNR | R1 | D9- | 11/12 | 0.917 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 0.667, nixon_resignation_1974 1; range [0.667, 1] | 3/4 |
| val+test | babble 20 dB SNR | R1 | D1+ | 23/24 | 0.958 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1, mobama_weekly_2014 1, nixon_resignation_1974 0.833; range [0.833, 1] | 7/8 |
| val+test | babble 20 dB SNR | R1 | D1- | 48/57 | 0.842 | per speaker: eisenhower_farewell_1961 0.8, lbush_radio_2001 1, mobama_weekly_2014 1, nixon_resignation_1974 0.6; range [0.6, 1] | 16/19 |
| val+test | babble 20 dB SNR | R1 | D2+ | 60/78 | 0.769 | per speaker: eisenhower_farewell_1961 0.889, lbush_radio_2001 0.952, mobama_weekly_2014 0.944, nixon_resignation_1974 0.333; range [0.333, 0.952] | 16/26 |
| val+test | babble 20 dB SNR | R1 | D2- | 106/108 | 0.982 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1, mobama_weekly_2014 0.926, nixon_resignation_1974 1; range [0.926, 1] | 35/36 |
| val+test | babble 20 dB SNR | R1 | D3- | 21/21 | 1 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1, nixon_resignation_1974 1; range [1, 1] | 7/7 |
| val+test | babble 20 dB SNR | R1 | D4- | 38/39 | 0.974 | per speaker: eisenhower_farewell_1961 1, lbush_radio_2001 1, mobama_weekly_2014 1, nixon_resignation_1974 0.667; range [0.667, 1] | 12/13 |
| val+test | babble 20 dB SNR | R1 | D5- | 72/90 | 0.8 | per speaker: eisenhower_farewell_1961 0.833, lbush_radio_2001 0.619, mobama_weekly_2014 0.889, nixon_resignation_1974 0.833; range [0.619, 0.889] | 20/30 |
| val+test | babble 20 dB SNR | R1 | D6- | 16/24 | 0.667 | per speaker: eisenhower_farewell_1961 0.667, lbush_radio_2001 0, mobama_weekly_2014 1, nixon_resignation_1974 1; range [0, 1] | 5/8 |
| val+test | babble 20 dB SNR | R1 | D9- | 10/12 | 0.833 | per speaker: eisenhower_farewell_1961 0.833, lbush_radio_2001 1, nixon_resignation_1974 0.667; range [0.667, 1] | 2/4 |

The result is the measured degradation; there is no pass rule. Rates and kept fractions pool every seed; the seeds of one recording are not independent trials, so each interval resamples participant recordings (a row with per-speaker values uses speakers as clusters). Babble, compression and phone-band conditions are not supported invariances. R2 flawed clips use the single-reference mode; the check readers (no injected flaw, so no retention) are measured with the single and the median-of-five references.

All transforms affect the participant only. Synthetic diffuse room RT60=0.4 s; babble uses four other dataset baseline speakers (ids below), seeded offsets, at 10/20 dB SNR. Phone: 300-3400 Hz, 8 kHz sampling, G.711 mu-law.

| clip | babble donor speakers |
|---|---|
| eisenhower_farewell_1961__G1 | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| eisenhower_farewell_1961__G3 | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| eisenhower_farewell_1961__G5 | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| eisenhower_farewell_1961__extra_L1A | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| eisenhower_farewell_1961__extra_L1B | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| eisenhower_farewell_1961__extra_L1C | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| eisenhower_farewell_1961__extra_L1D | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| eisenhower_farewell_1961__extra_L2A | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| eisenhower_farewell_1961__extra_L2B | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| eisenhower_farewell_1961__extra_L2C | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| eisenhower_farewell_1961__extra_L2D | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| eisenhower_farewell_1961__extra_L3A | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| eisenhower_farewell_1961__extra_L3B | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| eisenhower_farewell_1961__extra_L3C | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| eisenhower_farewell_1961__extra_L3D | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| eisenhower_farewell_1961__extra_botched_CONTOUR | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| eisenhower_farewell_1961__extra_botched_D1 | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| eisenhower_farewell_1961__extra_botched_D2 | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| eisenhower_farewell_1961__extra_botched_D4 | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| eisenhower_farewell_1961__extra_botched_D5 | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| eisenhower_farewell_1961__extra_botched_DISFLUENCY | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| eisenhower_farewell_1961__extra_botched_ENDINGS | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| eisenhower_farewell_1961__identity | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| eisenhower_farewell_1961__single_L1A | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| eisenhower_farewell_1961__single_L1B | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| eisenhower_farewell_1961__single_L2A | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| eisenhower_farewell_1961__single_L2B | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| eisenhower_farewell_1961__single_L3A | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| eisenhower_farewell_1961__single_L3B | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| gettysburg_amb>gettysburg_dj | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| gettysburg_amb>gettysburg_sa | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| gettysburg_amb>gettysburg_tg | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| gettysburg_dl,gettysburg_amb,gettysburg_pc,gettysburg_wt,gettysburg_jn>gettysburg_tg | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| gettysburg_dl>gettysburg_dj | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| gettysburg_dl>gettysburg_sa | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| gettysburg_dl>gettysburg_tg | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| gettysburg_fb,gettysburg_dl,gettysburg_pc,gettysburg_jn,gettysburg_wt>gettysburg_dj | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| gettysburg_fb,gettysburg_dl,gettysburg_wt,gettysburg_pc,gettysburg_amb>gettysburg_sa | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| gettysburg_fb>gettysburg_dj | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| gettysburg_fb>gettysburg_sa | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| gettysburg_fb>gettysburg_tg | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| gettysburg_jn>gettysburg_dj | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| gettysburg_jn>gettysburg_sa | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| gettysburg_jn>gettysburg_tg | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| gettysburg_pc>gettysburg_dj | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| gettysburg_pc>gettysburg_sa | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| gettysburg_pc>gettysburg_tg | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| gettysburg_wt>gettysburg_dj | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| gettysburg_wt>gettysburg_sa | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| gettysburg_wt>gettysburg_tg | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| greenman_reagan__G5 | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| greenman_reagan__extra_botched_CONTOUR | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| greenman_reagan__extra_botched_D1 | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| greenman_reagan__extra_botched_D2 | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| greenman_reagan__extra_botched_D4 | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| greenman_reagan__extra_botched_D5 | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| greenman_reagan__extra_botched_DISFLUENCY | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| greenman_reagan__extra_botched_ENDINGS | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| greenman_reagan__extra_x10_L3 | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| greenman_reagan__extra_x1_L2 | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| greenman_reagan__extra_x2_L2 | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| greenman_reagan__extra_x3_L2 | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| greenman_reagan__extra_x4_L2 | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| greenman_reagan__extra_x5_L3 | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| greenman_reagan__extra_x6_L3 | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| greenman_reagan__extra_x7_L3 | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| greenman_reagan__extra_x8_L3 | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| greenman_reagan__extra_x9_L3 | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| greenman_reagan__x1_L2 | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| greenman_reagan__x2_L3 | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| greenman_reagan__x3_L3 | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| greenman_reagan__x4_L3 | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| gwbush_911_2001__G1 | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'obama_weekly_2009', 'reagan_farewell_1989'] |
| gwbush_911_2001__G3 | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'obama_weekly_2009', 'reagan_farewell_1989'] |
| gwbush_911_2001__G5 | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'obama_weekly_2009', 'reagan_farewell_1989'] |
| gwbush_911_2001__extra_L1A | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'obama_weekly_2009', 'reagan_farewell_1989'] |
| gwbush_911_2001__extra_L1B | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'obama_weekly_2009', 'reagan_farewell_1989'] |
| gwbush_911_2001__extra_L1C | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'obama_weekly_2009', 'reagan_farewell_1989'] |
| gwbush_911_2001__extra_L1D | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'obama_weekly_2009', 'reagan_farewell_1989'] |
| gwbush_911_2001__extra_L2A | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'obama_weekly_2009', 'reagan_farewell_1989'] |
| gwbush_911_2001__extra_L2B | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'obama_weekly_2009', 'reagan_farewell_1989'] |
| gwbush_911_2001__extra_L2C | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'obama_weekly_2009', 'reagan_farewell_1989'] |
| gwbush_911_2001__extra_L2D | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'obama_weekly_2009', 'reagan_farewell_1989'] |
| gwbush_911_2001__extra_L3A | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'obama_weekly_2009', 'reagan_farewell_1989'] |
| gwbush_911_2001__extra_L3B | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'obama_weekly_2009', 'reagan_farewell_1989'] |
| gwbush_911_2001__extra_L3C | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'obama_weekly_2009', 'reagan_farewell_1989'] |
| gwbush_911_2001__extra_L3D | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'obama_weekly_2009', 'reagan_farewell_1989'] |
| gwbush_911_2001__extra_botched_CONTOUR | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'obama_weekly_2009', 'reagan_farewell_1989'] |
| gwbush_911_2001__extra_botched_D1 | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'obama_weekly_2009', 'reagan_farewell_1989'] |
| gwbush_911_2001__extra_botched_D2 | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'obama_weekly_2009', 'reagan_farewell_1989'] |
| gwbush_911_2001__extra_botched_D4 | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'obama_weekly_2009', 'reagan_farewell_1989'] |
| gwbush_911_2001__extra_botched_D5 | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'obama_weekly_2009', 'reagan_farewell_1989'] |
| gwbush_911_2001__extra_botched_DISFLUENCY | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'obama_weekly_2009', 'reagan_farewell_1989'] |
| gwbush_911_2001__extra_botched_ENDINGS | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'obama_weekly_2009', 'reagan_farewell_1989'] |
| gwbush_911_2001__identity | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'obama_weekly_2009', 'reagan_farewell_1989'] |
| gwbush_911_2001__single_L1A | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'obama_weekly_2009', 'reagan_farewell_1989'] |
| gwbush_911_2001__single_L1B | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'obama_weekly_2009', 'reagan_farewell_1989'] |
| gwbush_911_2001__single_L2A | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'obama_weekly_2009', 'reagan_farewell_1989'] |
| gwbush_911_2001__single_L2B | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'obama_weekly_2009', 'reagan_farewell_1989'] |
| gwbush_911_2001__single_L3A | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'obama_weekly_2009', 'reagan_farewell_1989'] |
| gwbush_911_2001__single_L3B | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'obama_weekly_2009', 'reagan_farewell_1989'] |
| harris_uncsw_2021__G1 | ['hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009', 'reagan_farewell_1989'] |
| harris_uncsw_2021__G3 | ['hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009', 'reagan_farewell_1989'] |
| harris_uncsw_2021__G5 | ['hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009', 'reagan_farewell_1989'] |
| harris_uncsw_2021__extra_L1A | ['hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009', 'reagan_farewell_1989'] |
| harris_uncsw_2021__extra_L1B | ['hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009', 'reagan_farewell_1989'] |
| harris_uncsw_2021__extra_L1C | ['hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009', 'reagan_farewell_1989'] |
| harris_uncsw_2021__extra_L1D | ['hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009', 'reagan_farewell_1989'] |
| harris_uncsw_2021__extra_L2A | ['hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009', 'reagan_farewell_1989'] |
| harris_uncsw_2021__extra_L2B | ['hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009', 'reagan_farewell_1989'] |
| harris_uncsw_2021__extra_L2C | ['hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009', 'reagan_farewell_1989'] |
| harris_uncsw_2021__extra_L2D | ['hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009', 'reagan_farewell_1989'] |
| harris_uncsw_2021__extra_L3A | ['hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009', 'reagan_farewell_1989'] |
| harris_uncsw_2021__extra_L3B | ['hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009', 'reagan_farewell_1989'] |
| harris_uncsw_2021__extra_L3C | ['hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009', 'reagan_farewell_1989'] |
| harris_uncsw_2021__extra_L3D | ['hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009', 'reagan_farewell_1989'] |
| harris_uncsw_2021__extra_botched_CONTOUR | ['hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009', 'reagan_farewell_1989'] |
| harris_uncsw_2021__extra_botched_D1 | ['hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009', 'reagan_farewell_1989'] |
| harris_uncsw_2021__extra_botched_D2 | ['hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009', 'reagan_farewell_1989'] |
| harris_uncsw_2021__extra_botched_D4 | ['hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009', 'reagan_farewell_1989'] |
| harris_uncsw_2021__extra_botched_D5 | ['hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009', 'reagan_farewell_1989'] |
| harris_uncsw_2021__extra_botched_DISFLUENCY | ['hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009', 'reagan_farewell_1989'] |
| harris_uncsw_2021__extra_botched_ENDINGS | ['hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009', 'reagan_farewell_1989'] |
| harris_uncsw_2021__identity | ['hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009', 'reagan_farewell_1989'] |
| harris_uncsw_2021__single_L1A | ['hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009', 'reagan_farewell_1989'] |
| harris_uncsw_2021__single_L1B | ['hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009', 'reagan_farewell_1989'] |
| harris_uncsw_2021__single_L2A | ['hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009', 'reagan_farewell_1989'] |
| harris_uncsw_2021__single_L2B | ['hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009', 'reagan_farewell_1989'] |
| harris_uncsw_2021__single_L3A | ['hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009', 'reagan_farewell_1989'] |
| harris_uncsw_2021__single_L3B | ['hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009', 'reagan_farewell_1989'] |
| hclinton_tomorrow_2010__G1 | ['harris_uncsw_2021', 'gwbush_911_2001', 'obama_weekly_2009', 'reagan_farewell_1989'] |
| hclinton_tomorrow_2010__G3 | ['harris_uncsw_2021', 'gwbush_911_2001', 'obama_weekly_2009', 'reagan_farewell_1989'] |
| hclinton_tomorrow_2010__G5 | ['harris_uncsw_2021', 'gwbush_911_2001', 'obama_weekly_2009', 'reagan_farewell_1989'] |
| hclinton_tomorrow_2010__extra_L1A | ['harris_uncsw_2021', 'gwbush_911_2001', 'obama_weekly_2009', 'reagan_farewell_1989'] |
| hclinton_tomorrow_2010__extra_L1B | ['harris_uncsw_2021', 'gwbush_911_2001', 'obama_weekly_2009', 'reagan_farewell_1989'] |
| hclinton_tomorrow_2010__extra_L1C | ['harris_uncsw_2021', 'gwbush_911_2001', 'obama_weekly_2009', 'reagan_farewell_1989'] |
| hclinton_tomorrow_2010__extra_L1D | ['harris_uncsw_2021', 'gwbush_911_2001', 'obama_weekly_2009', 'reagan_farewell_1989'] |
| hclinton_tomorrow_2010__extra_L2A | ['harris_uncsw_2021', 'gwbush_911_2001', 'obama_weekly_2009', 'reagan_farewell_1989'] |
| hclinton_tomorrow_2010__extra_L2B | ['harris_uncsw_2021', 'gwbush_911_2001', 'obama_weekly_2009', 'reagan_farewell_1989'] |
| hclinton_tomorrow_2010__extra_L2C | ['harris_uncsw_2021', 'gwbush_911_2001', 'obama_weekly_2009', 'reagan_farewell_1989'] |
| hclinton_tomorrow_2010__extra_L2D | ['harris_uncsw_2021', 'gwbush_911_2001', 'obama_weekly_2009', 'reagan_farewell_1989'] |
| hclinton_tomorrow_2010__extra_L3A | ['harris_uncsw_2021', 'gwbush_911_2001', 'obama_weekly_2009', 'reagan_farewell_1989'] |
| hclinton_tomorrow_2010__extra_L3B | ['harris_uncsw_2021', 'gwbush_911_2001', 'obama_weekly_2009', 'reagan_farewell_1989'] |
| hclinton_tomorrow_2010__extra_L3C | ['harris_uncsw_2021', 'gwbush_911_2001', 'obama_weekly_2009', 'reagan_farewell_1989'] |
| hclinton_tomorrow_2010__extra_L3D | ['harris_uncsw_2021', 'gwbush_911_2001', 'obama_weekly_2009', 'reagan_farewell_1989'] |
| hclinton_tomorrow_2010__extra_botched_CONTOUR | ['harris_uncsw_2021', 'gwbush_911_2001', 'obama_weekly_2009', 'reagan_farewell_1989'] |
| hclinton_tomorrow_2010__extra_botched_D1 | ['harris_uncsw_2021', 'gwbush_911_2001', 'obama_weekly_2009', 'reagan_farewell_1989'] |
| hclinton_tomorrow_2010__extra_botched_D2 | ['harris_uncsw_2021', 'gwbush_911_2001', 'obama_weekly_2009', 'reagan_farewell_1989'] |
| hclinton_tomorrow_2010__extra_botched_D4 | ['harris_uncsw_2021', 'gwbush_911_2001', 'obama_weekly_2009', 'reagan_farewell_1989'] |
| hclinton_tomorrow_2010__extra_botched_D5 | ['harris_uncsw_2021', 'gwbush_911_2001', 'obama_weekly_2009', 'reagan_farewell_1989'] |
| hclinton_tomorrow_2010__extra_botched_DISFLUENCY | ['harris_uncsw_2021', 'gwbush_911_2001', 'obama_weekly_2009', 'reagan_farewell_1989'] |
| hclinton_tomorrow_2010__extra_botched_ENDINGS | ['harris_uncsw_2021', 'gwbush_911_2001', 'obama_weekly_2009', 'reagan_farewell_1989'] |
| hclinton_tomorrow_2010__identity | ['harris_uncsw_2021', 'gwbush_911_2001', 'obama_weekly_2009', 'reagan_farewell_1989'] |
| hclinton_tomorrow_2010__single_L1A | ['harris_uncsw_2021', 'gwbush_911_2001', 'obama_weekly_2009', 'reagan_farewell_1989'] |
| hclinton_tomorrow_2010__single_L1B | ['harris_uncsw_2021', 'gwbush_911_2001', 'obama_weekly_2009', 'reagan_farewell_1989'] |
| hclinton_tomorrow_2010__single_L2A | ['harris_uncsw_2021', 'gwbush_911_2001', 'obama_weekly_2009', 'reagan_farewell_1989'] |
| hclinton_tomorrow_2010__single_L2B | ['harris_uncsw_2021', 'gwbush_911_2001', 'obama_weekly_2009', 'reagan_farewell_1989'] |
| hclinton_tomorrow_2010__single_L3A | ['harris_uncsw_2021', 'gwbush_911_2001', 'obama_weekly_2009', 'reagan_farewell_1989'] |
| hclinton_tomorrow_2010__single_L3B | ['harris_uncsw_2021', 'gwbush_911_2001', 'obama_weekly_2009', 'reagan_farewell_1989'] |
| lbush_radio_2001__G1 | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| lbush_radio_2001__G3 | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| lbush_radio_2001__G5 | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| lbush_radio_2001__extra_L1A | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| lbush_radio_2001__extra_L1B | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| lbush_radio_2001__extra_L1C | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| lbush_radio_2001__extra_L1D | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| lbush_radio_2001__extra_L2A | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| lbush_radio_2001__extra_L2B | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| lbush_radio_2001__extra_L2C | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| lbush_radio_2001__extra_L2D | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| lbush_radio_2001__extra_L3A | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| lbush_radio_2001__extra_L3B | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| lbush_radio_2001__extra_L3C | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| lbush_radio_2001__extra_L3D | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| lbush_radio_2001__extra_botched_CONTOUR | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| lbush_radio_2001__extra_botched_D1 | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| lbush_radio_2001__extra_botched_D2 | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| lbush_radio_2001__extra_botched_D4 | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| lbush_radio_2001__extra_botched_D5 | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| lbush_radio_2001__extra_botched_DISFLUENCY | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| lbush_radio_2001__extra_botched_ENDINGS | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| lbush_radio_2001__identity | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| lbush_radio_2001__single_L1A | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| lbush_radio_2001__single_L1B | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| lbush_radio_2001__single_L2A | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| lbush_radio_2001__single_L2B | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| lbush_radio_2001__single_L3A | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| lbush_radio_2001__single_L3B | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| mobama_weekly_2014__G1 | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| mobama_weekly_2014__G3 | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| mobama_weekly_2014__G5 | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| mobama_weekly_2014__extra_L1A | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| mobama_weekly_2014__extra_L1B | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| mobama_weekly_2014__extra_L1C | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| mobama_weekly_2014__extra_L1D | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| mobama_weekly_2014__extra_L2A | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| mobama_weekly_2014__extra_L2B | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| mobama_weekly_2014__extra_L2C | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| mobama_weekly_2014__extra_L2D | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| mobama_weekly_2014__extra_L3A | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| mobama_weekly_2014__extra_L3B | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| mobama_weekly_2014__extra_L3C | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| mobama_weekly_2014__extra_L3D | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| mobama_weekly_2014__extra_botched_CONTOUR | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| mobama_weekly_2014__extra_botched_D1 | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| mobama_weekly_2014__extra_botched_D2 | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| mobama_weekly_2014__extra_botched_D4 | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| mobama_weekly_2014__extra_botched_D5 | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| mobama_weekly_2014__extra_botched_DISFLUENCY | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| mobama_weekly_2014__extra_botched_ENDINGS | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| mobama_weekly_2014__identity | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| mobama_weekly_2014__single_L1A | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| mobama_weekly_2014__single_L1B | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| mobama_weekly_2014__single_L2A | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| mobama_weekly_2014__single_L2B | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| mobama_weekly_2014__single_L3A | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| mobama_weekly_2014__single_L3B | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| nixon_resignation_1974__G1 | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| nixon_resignation_1974__G3 | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| nixon_resignation_1974__G5 | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| nixon_resignation_1974__extra_L1A | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| nixon_resignation_1974__extra_L1B | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| nixon_resignation_1974__extra_L1C | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| nixon_resignation_1974__extra_L1D | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| nixon_resignation_1974__extra_L2A | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| nixon_resignation_1974__extra_L2B | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| nixon_resignation_1974__extra_L2C | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| nixon_resignation_1974__extra_L2D | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| nixon_resignation_1974__extra_L3A | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| nixon_resignation_1974__extra_L3B | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| nixon_resignation_1974__extra_L3C | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| nixon_resignation_1974__extra_L3D | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| nixon_resignation_1974__extra_botched_CONTOUR | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| nixon_resignation_1974__extra_botched_D1 | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| nixon_resignation_1974__extra_botched_D2 | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| nixon_resignation_1974__extra_botched_D4 | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| nixon_resignation_1974__extra_botched_D5 | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| nixon_resignation_1974__extra_botched_DISFLUENCY | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| nixon_resignation_1974__extra_botched_ENDINGS | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| nixon_resignation_1974__identity | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| nixon_resignation_1974__single_L1A | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| nixon_resignation_1974__single_L1B | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| nixon_resignation_1974__single_L2A | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| nixon_resignation_1974__single_L2B | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| nixon_resignation_1974__single_L3A | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| nixon_resignation_1974__single_L3B | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| obama_weekly_2009__G1 | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'reagan_farewell_1989'] |
| obama_weekly_2009__G3 | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'reagan_farewell_1989'] |
| obama_weekly_2009__G5 | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'reagan_farewell_1989'] |
| obama_weekly_2009__extra_L1A | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'reagan_farewell_1989'] |
| obama_weekly_2009__extra_L1B | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'reagan_farewell_1989'] |
| obama_weekly_2009__extra_L1C | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'reagan_farewell_1989'] |
| obama_weekly_2009__extra_L1D | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'reagan_farewell_1989'] |
| obama_weekly_2009__extra_L2A | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'reagan_farewell_1989'] |
| obama_weekly_2009__extra_L2B | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'reagan_farewell_1989'] |
| obama_weekly_2009__extra_L2C | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'reagan_farewell_1989'] |
| obama_weekly_2009__extra_L2D | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'reagan_farewell_1989'] |
| obama_weekly_2009__extra_L3A | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'reagan_farewell_1989'] |
| obama_weekly_2009__extra_L3B | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'reagan_farewell_1989'] |
| obama_weekly_2009__extra_L3C | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'reagan_farewell_1989'] |
| obama_weekly_2009__extra_L3D | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'reagan_farewell_1989'] |
| obama_weekly_2009__extra_botched_CONTOUR | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'reagan_farewell_1989'] |
| obama_weekly_2009__extra_botched_D1 | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'reagan_farewell_1989'] |
| obama_weekly_2009__extra_botched_D2 | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'reagan_farewell_1989'] |
| obama_weekly_2009__extra_botched_D4 | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'reagan_farewell_1989'] |
| obama_weekly_2009__extra_botched_D5 | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'reagan_farewell_1989'] |
| obama_weekly_2009__extra_botched_DISFLUENCY | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'reagan_farewell_1989'] |
| obama_weekly_2009__extra_botched_ENDINGS | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'reagan_farewell_1989'] |
| obama_weekly_2009__identity | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'reagan_farewell_1989'] |
| obama_weekly_2009__single_L1A | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'reagan_farewell_1989'] |
| obama_weekly_2009__single_L1B | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'reagan_farewell_1989'] |
| obama_weekly_2009__single_L2A | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'reagan_farewell_1989'] |
| obama_weekly_2009__single_L2B | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'reagan_farewell_1989'] |
| obama_weekly_2009__single_L3A | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'reagan_farewell_1989'] |
| obama_weekly_2009__single_L3B | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'reagan_farewell_1989'] |
| reagan_farewell_1989__G1 | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| reagan_farewell_1989__G3 | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| reagan_farewell_1989__G5 | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| reagan_farewell_1989__extra_L1A | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| reagan_farewell_1989__extra_L1B | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| reagan_farewell_1989__extra_L1C | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| reagan_farewell_1989__extra_L1D | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| reagan_farewell_1989__extra_L2A | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| reagan_farewell_1989__extra_L2B | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| reagan_farewell_1989__extra_L2C | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| reagan_farewell_1989__extra_L2D | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| reagan_farewell_1989__extra_L3A | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| reagan_farewell_1989__extra_L3B | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| reagan_farewell_1989__extra_L3C | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| reagan_farewell_1989__extra_L3D | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| reagan_farewell_1989__extra_botched_CONTOUR | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| reagan_farewell_1989__extra_botched_D1 | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| reagan_farewell_1989__extra_botched_D2 | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| reagan_farewell_1989__extra_botched_D4 | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| reagan_farewell_1989__extra_botched_D5 | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| reagan_farewell_1989__extra_botched_DISFLUENCY | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| reagan_farewell_1989__extra_botched_ENDINGS | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| reagan_farewell_1989__identity | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| reagan_farewell_1989__single_L1A | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| reagan_farewell_1989__single_L1B | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| reagan_farewell_1989__single_L2A | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| reagan_farewell_1989__single_L2B | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| reagan_farewell_1989__single_L3A | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |
| reagan_farewell_1989__single_L3B | ['harris_uncsw_2021', 'hclinton_tomorrow_2010', 'gwbush_911_2001', 'obama_weekly_2009'] |

Unperturbed identity-chain/null reference:

| clip | split | reference mode | minutes | flags | by key |
|---|---|---|---|---|---|
| eisenhower_farewell_1961__identity | val | single | 0.495 | 0 | [] |
| gwbush_911_2001__identity | train | single | 0.468 | 0 | [] |
| harris_uncsw_2021__identity | train | single | 0.518 | 0 | [] |
| hclinton_tomorrow_2010__identity | train | single | 0.39 | 0 | [] |
| lbush_radio_2001__identity | val | single | 0.494 | 0 | [] |
| mobama_weekly_2014__identity | test | single | 0.487 | 0 | [] |
| nixon_resignation_1974__identity | test | single | 0.495 | 0 | [] |
| obama_weekly_2009__identity | train | single | 0.357 | 0 | [] |
| reagan_farewell_1989__identity | train | single | 0.493 | 0 | [] |
| gettysburg_amb>gettysburg_dj | check readers | single | 0.382 | 0 | [] |
| gettysburg_amb>gettysburg_sa | check readers | single | 0.503 | 0 | [] |
| gettysburg_amb>gettysburg_tg | check readers | single | 0.408 | 0 | [] |
| gettysburg_dl>gettysburg_dj | check readers | single | 0.382 | 0 | [] |
| gettysburg_dl>gettysburg_sa | check readers | single | 0.503 | 1 | ['D3- whole clip'] |
| gettysburg_dl>gettysburg_tg | check readers | single | 0.408 | 0 | [] |
| gettysburg_fb>gettysburg_dj | check readers | single | 0.382 | 0 | [] |
| gettysburg_fb>gettysburg_sa | check readers | single | 0.503 | 0 | [] |
| gettysburg_fb>gettysburg_tg | check readers | single | 0.408 | 0 | [] |
| gettysburg_jn>gettysburg_dj | check readers | single | 0.382 | 0 | [] |
| gettysburg_jn>gettysburg_sa | check readers | single | 0.503 | 0 | [] |
| gettysburg_jn>gettysburg_tg | check readers | single | 0.408 | 0 | [] |
| gettysburg_pc>gettysburg_dj | check readers | single | 0.382 | 0 | [] |
| gettysburg_pc>gettysburg_sa | check readers | single | 0.503 | 1 | ['D3- whole clip'] |
| gettysburg_pc>gettysburg_tg | check readers | single | 0.408 | 0 | [] |
| gettysburg_wt>gettysburg_dj | check readers | single | 0.382 | 0 | [] |
| gettysburg_wt>gettysburg_sa | check readers | single | 0.503 | 0 | [] |
| gettysburg_wt>gettysburg_tg | check readers | single | 0.408 | 0 | [] |
| gettysburg_fb,gettysburg_dl,gettysburg_pc,gettysburg_jn,gettysburg_wt>gettysburg_dj | check readers | consensus5 | 0.382 | 1 | ['D3- whole clip'] |
| gettysburg_fb,gettysburg_dl,gettysburg_wt,gettysburg_pc,gettysburg_amb>gettysburg_sa | check readers | consensus5 | 0.503 | 1 | ['D3- whole clip'] |
| gettysburg_dl,gettysburg_amb,gettysburg_pc,gettysburg_wt,gettysburg_jn>gettysburg_tg | check readers | consensus5 | 0.408 | 0 | [] |
