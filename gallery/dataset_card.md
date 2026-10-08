# Contrastive Voice dataset

Controlled-perturbation dataset for reference-relative delivery analysis. Baselines are public-domain speeches (US government recordings) and public-domain LibriVox readings; flawed clips are DSP edits of them with analytic labels. No human has listened to the flawed clips; labels are exact for the edits, not human judgements.

Pipeline version 0.1.0. Audio: 16 kHz mono PCM16 WAV.

| id | split | speaker | passage (s) | words | licence basis | source |
|---|---|---|---|---|---|---|
| harris_uncsw_2021 | train | Kamala Harris | 31.1 | 64 | Public domain on Commons file page; US federal recording/official duties; inspect item provenance independently of speech text. | https://commons.wikimedia.org/wiki/File:Vice_President_Harris_Remarks_to_the_UN_at_the_65th_Session_of_the_Commission_on_the_Status_of_Women.webm |
| hclinton_tomorrow_2010 | train | Hillary Clinton | 23.42 | 51 | Commons PD-USGov-DOS; official State Department recording. | https://commons.wikimedia.org/wiki/File:Secretary_Clinton_-_Tomorrow_Will_Be_Better.ogv |
| gwbush_911_2001 | train | George W. Bush | 28.067 | 66 | Public domain on Commons file page; US federal recording/official duties; inspect item provenance independently of speech text. | https://commons.wikimedia.org/wiki/File:GWBush_Oval_Office_Address_20010911-1-.ogg |
| obama_weekly_2009 | train | Barack Obama | 21.4 | 58 | Public domain on Commons file page; US federal recording/official duties; inspect item provenance independently of speech text. | https://commons.wikimedia.org/wiki/File:Weekly_Address_(2009-01-24),_small.ogv |
| reagan_farewell_1989 | train | Ronald Reagan | 29.6 | 91 | Public domain on Commons file page; US federal recording/official duties; inspect item provenance independently of speech text. | https://commons.wikimedia.org/wiki/File:President_Ronald_Reagan%27s_Farewell_Address_to_the_Nation_from_the_Oval_Office_-_DPLA_-_64848a2be4a2a1c1ae29f72386cd6fa3.mp3 |
| lbush_radio_2001 | val | Laura Bush | 29.64 | 76 | Public domain on Commons file page; US federal recording/official duties; inspect item provenance independently of speech text. | https://commons.wikimedia.org/wiki/File:Weekly_Radio_Address_-_NARA_-_6171394.oga |
| eisenhower_farewell_1961 | val | Dwight D. Eisenhower | 29.68 | 55 | Public domain on Commons file page; US federal recording/official duties; inspect item provenance independently of speech text. | https://commons.wikimedia.org/wiki/File:Eisenhower_farewell_address.ogg |
| mobama_weekly_2014 | test | Michelle Obama | 29.2 | 73 | Official White House government recording; same address in Commons with PD-USGov-POTUS. | https://commons.wikimedia.org/wiki/File:Weekly_Address-_The_First_Lady_Marks_Mother%27s_Day_and_Speaks_Out_on_the_Tragic_Kidnapping_in_Nigeria.webm |
| nixon_resignation_1974 | test | Richard Nixon | 29.68 | 56 | Public domain on Commons file page; US federal recording/official duties; inspect item provenance independently of speech text. | https://commons.wikimedia.org/wiki/File:Nixon_resignation_audio.ogg |
| gettysburg_amb | calibration | Ann Boulais | 24.6 | 64 | LibriVox voluntary public-domain dedication in the USA; historical source text is public domain. Inspect linked item metadata for its mark; missing metadata is not evidence of a mark. | https://archive.org/details/gettysburgaddress_150anniv_1311_librivox |
| gettysburg_dl | calibration | David Lawrence | 28.68 | 64 | LibriVox voluntary public-domain dedication in the USA; historical source text is public domain. Inspect linked item metadata for its mark; missing metadata is not evidence of a mark. | https://archive.org/details/gettysburgaddress_150anniv_1311_librivox |
| gettysburg_fb | calibration | Frances Brown | 25.72 | 64 | LibriVox voluntary public-domain dedication in the USA; historical source text is public domain. Inspect linked item metadata for its mark; missing metadata is not evidence of a mark. | https://archive.org/details/gettysburgaddress_150anniv_1311_librivox |
| gettysburg_jn | calibration | Julia Niedermaier | 24.64 | 64 | LibriVox voluntary public-domain dedication in the USA; historical source text is public domain. Inspect linked item metadata for its mark; missing metadata is not evidence of a mark. | https://archive.org/details/gettysburgaddress_150anniv_1311_librivox |
| gettysburg_pc | calibration | Phil Chenevert | 28.66 | 64 | LibriVox voluntary public-domain dedication in the USA; historical source text is public domain. Inspect linked item metadata for its mark; missing metadata is not evidence of a mark. | https://archive.org/details/gettysburgaddress_150anniv_1311_librivox |
| gettysburg_wt | calibration | Winston Tharp | 30.88 | 64 | LibriVox voluntary public-domain dedication in the USA; historical source text is public domain. Inspect linked item metadata for its mark; missing metadata is not evidence of a mark. | https://archive.org/details/gettysburgaddress_150anniv_1311_librivox |
| gettysburg_dj | check | Drew Johnson | 22.9 | 64 | LibriVox voluntary public-domain dedication in the USA; historical source text is public domain. Inspect linked item metadata for its mark; missing metadata is not evidence of a mark. | https://archive.org/details/gettysburgaddress_150anniv_1311_librivox |
| gettysburg_sa | check | Sue Anderson | 30.2 | 64 | LibriVox voluntary public-domain dedication in the USA; historical source text is public domain. Inspect linked item metadata for its mark; missing metadata is not evidence of a mark. | https://archive.org/details/gettysburgaddress_150anniv_1311_librivox |
| gettysburg_tg | check | TriciaG | 24.48 | 64 | LibriVox voluntary public-domain dedication in the USA; historical source text is public domain. Inspect linked item metadata for its mark; missing metadata is not evidence of a mark. | https://archive.org/details/gettysburgaddress_150anniv_1311_librivox |
| greenman_reagan | train | John Greenman | 32.1 | 91 | LibriVox public-domain dedication in the USA; IA item has public-domain mark. | https://archive.org/details/presidential_farewell_last_addresses_jg_1504_librivox |
| null_8f984672e19f7ff9 | lockbox |  | 23.516063 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_7fe00fb976008e02 | fit |  | 22.33475 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_be3aaf015f5ac061 | fit |  | 25.16 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_fcd39f49b08d3a72 | select |  | 40.744813 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_45fd258855be8f7f | fit |  | 18.891687 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_0e41f45729c2fdea | lockbox |  | 28.632375 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_05bff75dc766b42e | select |  | 25.086375 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_acad703113ff3786 | fit |  | 26.285 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_e2c9bdc2e9a8559a | fit |  | 34.02825 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_6da6d5714a95d9fc | lockbox |  | 18.405562 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_cb4ae6a52ab61ddc | select |  | 18.638 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_63317b7b5aaffded | select |  | 22.814438 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_716d82870bb46a89 | fit |  | 25.951625 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_50b07cb03f78d375 | fit |  | 19.642625 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_c87bab0737b34046 | lockbox |  | 28.35625 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_069d095115ee5a56 | fit |  | 23.328437 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_32c765ae061682da | fit |  | 19.662 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_ba909c679016c7bd | select |  | 20.706937 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_a7ed10d5e7bdb246 | lockbox |  | 26.5 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_cd6c29d67cbeed29 | select |  | 22.0625 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_2848e9128e9f44dd | select |  | 18.909 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_a60ca3f4f2c4ed3f | fit |  | 26.672313 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_b91c44202d6ca9e7 | select |  | 23.153875 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_3b12370ed73934dc | select |  | 17.3885 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_9dbac94eda875518 | fit |  | 27.79325 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_44d5bd5b2c063b74 | fit |  | 28.844938 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_0beb32efd43a7411 | fit |  | 19.124 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_328d9a5cea401fc5 | fit |  | 22.224438 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_1f169249be30fede | fit |  | 37.165438 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_a0be3dfbf1cb96a5 | fit |  | 23.555 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_54975577f3252231 | lockbox |  | 17.716812 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_8b4b95ece830774a | fit |  | 29.22075 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_91ce7a88354a7bab | lockbox |  | 25.774188 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_f152944f421f2469 | lockbox |  | 23.505938 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_5899009792a8d89b | lockbox |  | 28.45025 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_dd1c6e13ce9e9ffb | fit |  | 21.340875 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_c3f4d3c39f8ea96e | select |  | 23.127 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_ecbe67d85c264069 | lockbox |  | 30.209187 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_bc47989ad578b7f3 | lockbox |  | 25.417437 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_c23d296ab00d15d2 | select |  | 32.128625 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_a578a279fe8b415a | fit |  | 20.568562 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_747e8086bdc20063 | select |  | 23.219938 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_d84460d802dacf64 | fit |  | 22.709125 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_45dea1b3c12ba748 | fit |  | 48.021062 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_11384ad745ae8006 | fit |  | 24.688063 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_7246d5b4a74ebb45 | fit |  | 23.312875 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_154f60a4200a137e | fit |  | 21.2695 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_7ec210d602164ec0 | lockbox |  | 28.119187 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_1dd46cff40304992 | lockbox |  | 19.1565 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_9abde6a27c3dde40 | fit |  | 25.786562 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_4a4a7aa03e20e665 | select |  | 19.240313 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_706afd0cbbe0cc8d | lockbox |  | 29.085438 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_75123c1a6e868fe4 | fit |  | 35.078 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_5030b11f81844cd6 | lockbox |  | 25.073875 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_24beae305d4317b8 | fit |  | 19.95175 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_9061cabe5335548f | fit |  | 29.739937 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_18e05ef41241c416 | lockbox |  | 22.458938 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_c807de892a6f0497 | fit |  | 35.102125 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_3feb2c0d047a68cb | fit |  | 22.776812 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_a67b8237b4138ba1 | select |  | 31.778063 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_5e1921cd35d023af | fit |  | 21.4 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_ebff541978815b14 | fit |  | 21.48225 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_4763e443d7585fbb | select |  | 21.534938 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_df8b24f16b2a45fe | lockbox |  | 24.17575 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_1c59936b52e60830 | lockbox |  | 24.907312 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_f309ab7a5181b641 | fit |  | 22.386937 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_7b30efb66a3aa15c | fit |  | 21.635437 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_e4308d69f776d794 | select |  | 22.2685 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_3d871ed3631bb415 | select |  | 21.77 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_e66bfd2285953678 | lockbox |  | 23.006375 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_1cabca0e7545d4d4 | lockbox |  | 23.40375 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_8e3f5e100669c7e7 | fit |  | 21.71225 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_f121b3a2c01548b0 | fit |  | 18.523812 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_b9af6303e0690eac | fit |  | 19.383875 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_4b16c8571fd38d73 | select |  | 21.121875 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_745de2e652879fe1 | fit |  | 19.964437 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_37cbe44fbeab0a5e | fit |  | 25.7665 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_f8f7a867ce51d39e | fit |  | 17.98025 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_3a331b427fab617e | lockbox |  | 24.032688 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_93b638e63fa5f339 | select |  | 29.38125 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_ccded33cc9396acc | fit |  | 39.195312 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_ffe8358f89724a75 | fit |  | 38.499437 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_8521e044e15a5431 | lockbox |  | 37.339937 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_e164d69389f7a4d3 | lockbox |  | 25.065 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_2639f6e9772f61a8 | fit |  | 27.150063 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_666cf5d9642bc0ad | lockbox |  | 23.266375 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_c744c1ca40bd787d | fit |  | 25.773375 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_615fc93c09a88c5d | fit |  | 24.86975 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_cfff2a5736b2f5b4 | fit |  | 23.488375 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_03d575823448a56e | select |  | 28.464375 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_d32b9b1eed55b4a0 | fit |  | 36.990938 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_f207a41fc826f574 | select |  | 25.186875 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_f7493d152ab458bd | fit |  | 25.588375 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_0ab2d1ae3a9542f5 | select |  | 30.038438 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_66e2283d0991b47c | fit |  | 19.411875 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_aebdbe088da62890 | select |  | 21.008813 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_574f284eac9b70cb | lockbox |  | 25.727313 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_39677a66c29c9f0a | select |  | 22.207687 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_708e164e296e2e8a | lockbox |  | 22.595938 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_3664c00de36496a9 | lockbox |  | 20.542375 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_3d12cfce800df080 | fit |  | 34.323625 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_095aafa764986a59 | fit |  | 22.492313 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_3d11a265e513dc39 | fit |  | 23.942688 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_55f86de66a2c6975 | fit |  | 18.523125 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_f45ba0fb168e7bd3 | fit |  | 20.917063 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_bc43a501ab544272 | select |  | 18.921688 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_f3dca97c1c336a8e | fit |  | 38.3125 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_f95fbf58b448f3a0 | select |  | 21.438875 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_1491979102edae34 | select |  | 30.36025 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_dc2d97990b1b26f0 | lockbox |  | 29.988625 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_16a3f0716e26d466 | select |  | 18.526563 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_0b973fe92296d151 | select |  | 23.19675 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_82dedd0d4cb94467 | fit |  | 25.194625 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_aeabd9ac48d2de50 | lockbox |  | 54.483375 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_57327746ede361fd | select |  | 19.341875 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_0533b3fbcad235fc | fit |  | 25.122937 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_89750476ba2ccdd4 | lockbox |  | 18.3125 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_2f0d8ce81585d00c | select |  | 41.670375 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_b864d897a7fa8f3d | lockbox |  | 21.820125 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_0bf43e02465a9292 | fit |  | 42.1515 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_7f18b30326cb6945 | fit |  | 31.4225 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_612380f96fc99b90 | fit |  | 29.95375 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_459d7b55642c9da3 | lockbox |  | 27.968438 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_979cd41282445788 | fit |  | 21.92525 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_033f09377fc21891 | lockbox |  | 26.708375 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_704030ec88b7619e | lockbox |  | 25.973688 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_d0ff61ce5c94915d | select |  | 20.900125 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_6051164f493b4819 | fit |  | 25.68125 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_8afdd428a9b25e3b | lockbox |  | 85.119187 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_11099955da8ffb8e | lockbox |  | 18.5885 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_e970e7919f829d96 | fit |  | 20.932813 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_be641418b886e0bb | lockbox |  | 20.816375 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_40bbe6e5e067d770 | fit |  | 30.25225 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_0bb6d66c8b7a04cd | lockbox |  | 20.433563 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_1aef3a987c7d2d3e | fit |  | 25.899062 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_0b41a5b4c00c1809 | lockbox |  | 24.93825 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_e42178d5c3f0c34c | fit |  | 26.981625 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_e7fdb80a5ba9b324 | fit |  | 22.534437 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_0c33cd422f80395f | lockbox |  | 36.54825 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_1b50f6475f214d43 | lockbox |  | 24.195062 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_a6bc5e415ed8a447 | fit |  | 32.638125 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_21ecf09b36e6bf69 | lockbox |  | 29.082125 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_e9b566254658bd4a | select |  | 66.113687 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_f5da44f93beea557 | select |  | 23.12225 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_f956727cae86240c | lockbox |  | 26.810562 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_f229eb09f6c80601 | lockbox |  | 23.060312 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_b36e99af6d5c1262 | select |  | 19.5 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_81374398de588bee | lockbox |  | 28.583375 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_e8a0000012b126dc | fit |  | 24.749875 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_e62879a0f7721a20 | lockbox |  | 25.4955 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_1b8f2b251a5bf6e1 | fit |  | 26.331437 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_0f84d66cb01593f3 | fit |  | 28.74 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_1bdfb4b47a940429 | fit |  | 37.772813 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_40b57f69cee32faf | lockbox |  | 17.832937 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_c2692bf80d7c50b5 | fit |  | 32.688437 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_61b3cbab83f8d3da | select |  | 21.179875 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_ea8b7330af71ec18 | select |  | 32.717125 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_4ca3f4e8cd311a76 | fit |  | 20.620188 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_9e9812030cd42ad2 | select |  | 19.53275 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_9335561ccc0d4f2e | fit |  | 20.252437 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_be7d9bfdf6b1510c | fit |  | 21.315938 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_f9c22ab275fd9b5f | select |  | 25.588375 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_5693bb9ef02d641a | fit |  | 23.359313 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_038b4f66856d740c | fit |  | 19.719062 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_5ffdac9129609578 | fit |  | 22.691188 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_2ec793feac2b2305 | lockbox |  | 31.573375 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_346103727a29520d | fit |  | 30.794375 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_a9eacb1eb8901021 | fit |  | 36.752 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_0a962ef6b135aaae | lockbox |  | 18.088125 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_773b5fc7023d3227 | select |  | 23.085438 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_698fca78e2bfa5de | lockbox |  | 23.091375 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_bc90f41557390717 | lockbox |  | 20.248438 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_e1ef42707eb47854 | fit |  | 24.41825 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_8ea99628aa506ded | select |  | 17.99475 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_a95fc20a3cb70d4a | select |  | 29.29625 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_a177b8e0010a31a8 | lockbox |  | 39.4275 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_f93d603afeaa9b25 | fit |  | 27.52725 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_b0bf54a47a690c64 | select |  | 20.609938 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_4de59cb0dd125a4e | fit |  | 20.6075 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_ea2e919d3e0389dc | select |  | 30.07525 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_38de2038b8aedd87 | fit |  | 33.275687 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_76cac5ee75608ff2 | lockbox |  | 23.008813 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_f8bcce802ac9f818 | fit |  | 30.1395 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_d2dfa46794861b5b | select |  | 28.647313 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_3936b3d9f2f16c90 | fit |  | 19.436312 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_eb14ecbffac5d1b5 | lockbox |  | 25.177375 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_b660e25f6d6ca154 | lockbox |  | 26.039188 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_bd755ed7db574166 | select |  | 24.328312 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_955298f536f9dd85 | fit |  | 19.955625 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_90e7a5f3e7259a76 | select |  | 22.190687 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_9a5170968d2f4bd5 | lockbox |  | 21.593187 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_e3775770e998c631 | fit |  | 19.750937 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_73286ae92d55112f | select |  | 21.538 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_f73ba1bc3c209db7 | fit |  | 19.005562 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_99795a7e3f0aa83c | fit |  | 35.284562 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_18dc7ee6b7c34006 | fit |  | 25.820625 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_6fe8eb0ad11eaf85 | fit |  | 21.97625 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_8e6b402cd3f8c814 | fit |  | 24.282812 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_f91e34143accd2b0 | fit |  | 30.12575 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_bea87fc52d47cbb6 | fit |  | 22.4045 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_f59f39115d50d6f9 | select |  | 18.9 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_0c90f13151169478 | fit |  | 27.058563 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_6541fb62b2ca1030 | select |  | 19.067187 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_a0dab6002e07579b | fit |  | 18.988625 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_870dd7149bdcddf1 | lockbox |  | 21.674187 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_8fe964e71b2a7262 | lockbox |  | 24.906312 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_a7fd564facb3970e | fit |  | 23.807875 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_43e74ec938cd2a78 | lockbox |  | 27.157 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_13167abd122f9b8b | select |  | 20.129938 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_018c2af958cb9cbd | fit |  | 30.0365 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_0dd1bda1b0bc9346 | select |  | 26.596062 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_410bd6d43ca8ad41 | select |  | 21.962438 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_c27b5963cda6ad21 | fit |  | 21.838375 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_5078aac989945aae | lockbox |  | 20.8565 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_bb3acb63ed9974a3 | lockbox |  | 22.352 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_aca64e87ac6fbaaf | lockbox |  | 24.286687 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_f6ab5c130f0297d2 | fit |  | 20.574188 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_77cf4eb4918c877e | lockbox |  | 22.72075 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_de52606b8f7fd20d | select |  | 21.228437 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_0eff94c84a09d8b9 | fit |  | 25.388625 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_a8da55eb692facb5 | fit |  | 45.44 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_00a1732d5734008d | fit |  | 21.658875 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_d3cb8d6df7617f12 | fit |  | 23.702 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_ebc7254203021ee2 | fit |  | 22.912437 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_d8c93f1e3824c397 | fit |  | 22.406875 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_d4e77ac9226d5b84 | lockbox |  | 35.66225 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_3986d9398e6cbad1 | fit |  | 22.61625 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_157e5d4dc3de71e3 | lockbox |  | 21.093625 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_a647d81c048b7b41 | fit |  | 36.6545 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_c56985e45598eb86 | fit |  | 20.432437 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_6b9dca43756067b2 | fit |  | 21.209125 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_69dbfd2fa3eba6f2 | lockbox |  | 19.181438 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_b644d100abbc469d | lockbox |  | 41.529562 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_bdfdadcaad7e22a7 | select |  | 20.086437 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_000ecf00ffc19eb7 | fit |  | 20.288187 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_552a46d3e3a6afb6 | fit |  | 22.0 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_6e84db157d4573e1 | select |  | 19.87225 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_e679958db1b7478b | fit |  | 25.4375 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_eb5ded1609ecc4c9 | fit |  | 23.124 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_126eeeb7bf16da1b | fit |  | 39.902625 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_cf60233e4b5cd497 | select |  | 43.705438 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_7e5d7702e47f2d14 | fit |  | 25.987625 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_c05b5189df9489d8 | select |  | 20.3175 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_7245f38bb32365ae | fit |  | 20.271438 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_700015f907137ac8 | fit |  | 21.926125 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_f03c8616196f9291 | fit |  | 23.284813 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_9ab1047dc4ee2260 | fit |  | 23.504562 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_15615c1fa64a3b6a | lockbox |  | 21.251938 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_5f8a4b2173ec4142 | lockbox |  | 25.122062 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_4707c654cd8777a7 | lockbox |  | 30.6455 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_641986a201336b12 | fit |  | 19.329875 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_5ee8cece318af853 | fit |  | 20.068938 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_7f113af1a4e7446b | lockbox |  | 27.120938 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_7e75bcf7e854df3d | fit |  | 18.75 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_280a578d41f677f8 | fit |  | 35.409438 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_c2e0b6480caf48b9 | select |  | 22.68775 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_2608310e5f36813f | select |  | 21.6845 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_0279ed0d9197e91e | fit |  | 22.141562 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_4227ceb7f8327d72 | select |  | 25.878625 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_50788186645a7354 | fit |  | 28.522813 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_2a83e209fe73fb73 | select |  | 19.458938 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_89adcbadf1d5f13e | lockbox |  | 23.726188 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_aca85473d269a436 | fit |  | 25.9515 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_a9cc6ae46784ef87 | fit |  | 28.048813 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_bfea8df8cb57ab3e | lockbox |  | 31.11675 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_3c831b704324ad45 | lockbox |  | 18.723625 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_23fb6db7b40516b9 | fit |  | 22.0 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_f0787a7e5e3e9938 | select |  | 15.768313 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_fa98010ba040c2a5 | fit |  | 24.003563 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_26010b3d1dec2bcf | fit |  | 18.955625 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_dff110b17e143307 | lockbox |  | 25.009125 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_8467c13a100efda2 | fit |  | 24.832438 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_be754627d44744b7 | lockbox |  | 17.555625 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_890e8e018f21a55f | fit |  | 21.178438 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_7828fab21cd33561 | fit |  | 21.272125 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_580d9903d817abad | fit |  | 31.093563 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_f2f25d34f595ddec | select |  | 25.641687 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_3cd7f291c33f8395 | fit |  | 21.773125 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_52026b2f55cbb0be | fit |  | 21.85225 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_92314870ce5368d3 | select |  | 28.761312 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_3de48fb3cbd1b70e | lockbox |  | 22.773 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_20b988027c494490 | fit |  | 35.25225 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_4a3fedb33f2083b7 | select |  | 17.031875 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_64e72566a1459c2b | fit |  | 21.6 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_97a927811ad69ac7 | fit |  | 44.315438 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_2501550f5d0db04f | fit |  | 16.4745 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_07fdf40f44be607a | fit |  | 20.609125 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_100d05eae4648480 | fit |  | 32.419688 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_3c5c30b7c28b299a | lockbox |  | 24.158375 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_6c37352d4a15d00d | select |  | 27.485437 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_6c72853582ef27b1 | fit |  | 21.857813 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_56228bb9e6294419 | fit |  | 16.809812 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_1e9905704b63f258 | lockbox |  | 22.361438 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_d1ad6ba02463bd01 | fit |  | 20.526438 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_213542de55e2c401 | select |  | 18.497125 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_2d3475895a8c0d35 | fit |  | 19.319 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_d3a22586594be4c1 | select |  | 28.486 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_c4637679d3b6ef49 | fit |  | 20.354125 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_f407c5aeec5d2e02 | fit |  | 28.317438 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_5dead321cdba6682 | fit |  | 20.830125 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_82cc899ceef504ee | select |  | 20.088562 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_1bc999432eb26217 | select |  | 29.602812 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_de9b1505df91b35e | fit |  | 34.075313 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_dd8d3d8e129bcee0 | fit |  | 22.919875 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_e07fed45971608c8 | select |  | 33.587 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_5e5f6ba2b095ffb7 | lockbox |  | 21.175937 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_d4b267ee430ed026 | fit |  | 17.846375 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_5d72312e01551da0 | fit |  | 21.0455 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_b05794f44b7f9a12 | select |  | 27.2715 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_3c0f1837c161d419 | fit |  | 27.732937 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_badb361be48bbf57 | lockbox |  | 21.281125 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_2b1e9052efaec526 | select |  | 21.329563 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_07286fbb0f43e4e1 | select |  | 19.280875 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_65ab14b8f7ce3d57 | fit |  | 22.70875 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_9ab0fa0cabec0dd6 | fit |  | 23.498375 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_f7ee368dd3c357bb | select |  | 18.180438 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_cfe25a17f7c04334 | select |  | 25.340438 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_39a2f9691e6a3ab0 | select |  | 26.130063 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_1ef25574add45c8e | select |  | 19.547375 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_8ccb512699dcb17d | fit |  | 25.669687 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_759c98d121e6cf84 | fit |  | 24.382625 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_9a519269902118c9 | lockbox |  | 22.795437 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_ebcda1df08b7723b | lockbox |  | 17.980062 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_1079475cf9b449ab | fit |  | 22.798687 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_4a677b09d97b792c | lockbox |  | 35.974063 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_741d67513fd4a35c | lockbox |  | 22.767187 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_cc4ef0cd34be5cca | lockbox |  | 21.084875 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_47ea8779ef333571 | fit |  | 27.322937 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_716af62de8ac8e72 | lockbox |  | 25.867313 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_511fd3a3fb8db032 | select |  | 20.362188 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_dd89ff6620a36b6a | lockbox |  | 28.207 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_f5f41594a0139947 | fit |  | 23.271937 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_7a2930fb7408581d | fit |  | 21.281125 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_94cb9e1c54c014b8 | fit |  | 22.291187 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_92748dbbed4e22f2 | fit |  | 23.754 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_6acf5d5012326137 | fit |  | 22.919375 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_77a47bee72400827 | select |  | 22.483812 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_cbce535932faa66b | select |  | 20.13475 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_b0c946d29ac57ffe | select |  | 20.414625 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_6c49d93486318a53 | fit |  | 41.099313 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_cff4f2dd7f2d5e39 | fit |  | 28.025688 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_2bbcc87be7af42ef | select |  | 21.274125 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_f04c48820f4b0f66 | fit |  | 18.753812 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_a94f6789a0322ca5 | lockbox |  | 19.094687 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_6bda9d011a81a6bc | fit |  | 18.981687 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_b890d26b8fd0deeb | fit |  | 39.676875 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_bf22d9581079ed85 | fit |  | 28.77475 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_f1994e23738dff5e | lockbox |  | 18.599187 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_a83f265206a7f7bf | select |  | 37.40425 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_fdae6150201425a4 | fit |  | 29.175625 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_8954f57a10a3160a | fit |  | 26.566562 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_2870e3468dc9bae3 | fit |  | 19.287 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_02384cdfd77b7461 | fit |  | 20.4805 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_1c3e0ecf98711e1a | fit |  | 22.829187 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_65d665f16d6ede0b | fit |  | 20.41075 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_f4bd5834dd3442ea | lockbox |  | 30.753625 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_be98511f6e2bdcf5 | select |  | 23.980563 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_710fb56d717cabf1 | lockbox |  | 25.0595 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_5ae356651dcb299f | select |  | 48.513438 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_130f20930d263db9 | fit |  | 31.254062 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_a7b12a32c7004318 | select |  | 21.687438 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_57650954c03f6938 | fit |  | 22.295938 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_c7a624e5042bbaaf | select |  | 20.732563 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_87600716799f9c63 | fit |  | 19.388687 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_94b9aee5bbec4c67 | fit |  | 23.843125 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_36a30e4f49abf8c3 | fit |  | 18.007062 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_61b32d63efc128c9 | select |  | 41.828 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_67135c05d0318e68 | fit |  | 21.004687 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_c3410a3b1f0bc2f2 | select |  | 53.116062 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_96497109585d0d6f | select |  | 17.663563 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_5a81080bdbae3bac | select |  | 26.528063 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_58185f7bc3a12d14 | select |  | 23.741688 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_215b2810111ce1dc | fit |  | 24.150312 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_764c76305c853a3a | lockbox |  | 21.418375 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_eb59ce7f471f7cb9 | fit |  | 25.554 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_c07882e24ea900b5 | select |  | 22.352187 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_2e5810418d21a4af | select |  | 22.119875 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_43461d2d73c71078 | fit |  | 26.746312 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_634e14a45e93b717 | lockbox |  | 25.776375 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_6d4feafe1da272ea | select |  | 23.359313 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_a2d693a09839eb02 | lockbox |  | 20.42375 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_797047fac95000e8 | fit |  | 27.339688 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_f87ce25c40abcc9a | fit |  | 26.095875 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_174792943930e105 | fit |  | 26.921625 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_784687909fa46034 | fit |  | 28.270312 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_2e038a711f2481d5 | select |  | 20.314563 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_10245664779b1eaa | select |  | 21.213375 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_aaf202f42028f35c | fit |  | 26.198625 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_798b78cbb67f0388 | lockbox |  | 21.408812 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_3644d55b1f711689 | lockbox |  | 32.207625 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_3d45169bb2fbacab | fit |  | 20.81775 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_e1e9250f5ea84ce9 | fit |  | 49.010875 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_8057ef964e607868 | fit |  | 19.098437 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_0af427b35c995c85 | fit |  | 24.908062 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_cfbc05d98e0f9b2c | lockbox |  | 24.550812 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_0a93e617649b1a94 | fit |  | 32.415062 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_0287ebed9891404d | fit |  | 34.357937 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_4770d3477a249bb3 | lockbox |  | 18.070312 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_49e20655708f411c | select |  | 21.123125 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_aa754f5cbd9e1abe | lockbox |  | 19.783438 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_5826a386a78607b5 | fit |  | 21.432 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_0b9f9c218a8c3aa9 | fit |  | 21.008875 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_d1630210b18ab77a | fit |  | 22.01975 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_b0abb9d1e1b0236e | fit |  | 31.857875 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_4eae95a2db84bf64 | lockbox |  | 20.32 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_1fffb50416bbc341 | lockbox |  | 23.780375 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_52f5f7a8e63bab16 | fit |  | 22.168437 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_ab6957970d7b0599 | fit |  | 17.743813 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_dbef01b197661455 | fit |  | 64.50325 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_5d2e10cd92ff421e | select |  | 43.003375 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_a3472abc5a15bc30 | fit |  | 17.823375 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_61286a8168c40d5c | select |  | 21.420375 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_6afb880ee5bbef5d | lockbox |  | 23.628937 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_d284bf9b027276b5 | fit |  | 20.886312 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_d0e2c36d01c8895a | fit |  | 64.179937 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_dc5dd337a9509156 | select |  | 28.802875 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_49122e3b28ad5de9 | fit |  | 27.549 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_e406db593d574070 | select |  | 17.836875 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_941c07f8c72466dd | fit |  | 26.092688 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_9bcc4d7c429425e4 | fit |  | 22.476937 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_59ac4057711986d3 | select |  | 27.225438 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_30ccc1be4a40cd78 | fit |  | 20.327125 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_d2247ade4ed3785e | lockbox |  | 20.559125 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_f4e2649dc07534b5 | select |  | 18.862188 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_e951375faf3da6b8 | fit |  | 33.010813 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_fddfe1a762db0d02 | select |  | 19.852812 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_269e3fa8ab1e4240 | lockbox |  | 29.975188 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_a0c5e91734ee5d6d | fit |  | 19.829875 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_1c7131367f3d43ab | fit |  | 20.822187 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_677c9219f4881115 | lockbox |  | 28.741125 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_f7450e05b9b082a3 | lockbox |  | 25.717125 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_632dfd192188304b | select |  | 26.92925 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_15497ad838478ebb | lockbox |  | 18.888063 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_c7a0c67f62bcdecf | select |  | 18.855812 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_7fbeba60a82e5bfe | fit |  | 19.96675 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_a72b81d5e5b6601e | fit |  | 17.345063 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_56e46551039a22b7 | lockbox |  | 21.283875 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_e29121229754885e | fit |  | 19.21475 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_43b16f9dde8f5741 | lockbox |  | 21.85 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_091ed654a5ca0215 | lockbox |  | 23.579875 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_7e99a8522e325e6c | fit |  | 20.75 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_3ecc31cefd0d294a | lockbox |  | 30.010313 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_fe5ff1194b67784c | fit |  | 22.2 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_2b78471de2d2898c | select |  | 26.070812 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_08c7432ef89dc0f4 | select |  | 32.542938 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_71ed52086c3c4c25 | lockbox |  | 26.908875 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_2e9aa6e4bc1f85ef | select |  | 35.054812 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_f5c3a1af159d063f | fit |  | 25.360625 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_6c715d81f4a83f31 | fit |  | 21.983687 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_fd4d2d2b4e815ef6 | lockbox |  | 22.555312 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_1519ea457858fe68 | select |  | 25.135625 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_ead160ec27bdde90 | lockbox |  | 16.75 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_ee6317cd2c630b9e | lockbox |  | 22.519375 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_d456e353a17dbbad | select |  | 37.776688 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_1541abbca7d907dc | fit |  | 49.963875 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_225116a2b88f386d | select |  | 26.302875 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_ffb98cfbd4329c60 | fit |  | 20.938188 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_16b04fb8db1c8425 | lockbox |  | 22.76 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_75c6ca0de676d127 | select |  | 20.558375 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_ccfcc1b3cd0e429f | select |  | 20.834875 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_615faa3c07ffcd27 | fit |  | 38.746625 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_171989d6995a7bbf | select |  | 41.14575 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_ebf57d9b2b0a3705 | lockbox |  | 31.411188 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_d84b4ec0beb6ad7d | fit |  | 23.135687 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_4d2cadda29f7d1af | fit |  | 27.585313 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_f681554458133bdc | lockbox |  | 34.688313 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_dd6c37c788777258 | select |  | 23.614062 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_f9168932a29899d1 | fit |  | 22.47825 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_bbcd051c94e1758f | fit |  | 33.3315 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_9123b7ad6d55d65c | fit |  | 24.722062 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_86dfcd8d1740032f | fit |  | 23.08 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_eda03cf9faf82292 | fit |  | 19.170875 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_6a7885e718767eb4 | select |  | 17.672563 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_a1c2226d545f268d | lockbox |  | 22.845188 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_d4d59e1875d8b9f5 | lockbox |  | 25.99475 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_09def32082a87add | lockbox |  | 21.645312 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_d77c38c2895b1f7d | select |  | 23.057437 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_2ec548a6fbbc71cb | fit |  | 19.172375 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_c37762ee0eaadacb | fit |  | 21.641 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_eb0b8e8facb1e754 | fit |  | 20.985625 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_30baca00bc77b8e9 | select |  | 24.903437 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_d31aa992348b3a11 | fit |  | 19.591875 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_251ccc90ba08cf3d | select |  | 26.506937 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_80b9c5140f6f7f54 | select |  | 20.75575 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_feeb68c824a7acbb | fit |  | 21.350375 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_6530bfc55ed28123 | select |  | 20.715 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_f131ab29a1c3e531 | fit |  | 21.00175 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_939d608d4948cec8 | fit |  | 48.862875 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_f48e88a12f81e21d | fit |  | 33.417125 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_8928b4c954da631d | lockbox |  | 47.162312 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_22b6e0e59e9fb0f1 | fit |  | 22.778938 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_6adfee1624d53aab | fit |  | 22.43 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_9da7c395418468cb | select |  | 38.280563 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_0a48f33303e23fab | fit |  | 16.460563 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_f40c34910fe19335 | select |  | 33.216375 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_fdcfcb6aae26be75 | fit |  | 21.2125 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_bb2b61f73de2bb55 | fit |  | 34.972375 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_cb1ab60e1e3719be | select |  | 22.567 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_14efc79d52b9b61a | fit |  | 26.26175 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_7866e6f8fb02bbd4 | lockbox |  | 23.269625 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_17f4e7a0315022da | fit |  | 22.177563 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_9e07eb2615f0622b | fit |  | 23.622625 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_038ace9be0a3954a | fit |  | 22.661812 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_f05b1949ffe4e435 | fit |  | 24.18 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_3536ce22bfd9a2dc | select |  | 31.756875 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_ac2b63635da7ffc3 | select |  | 21.9615 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_79f5e27290594337 | lockbox |  | 18.622937 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_39dea99868297372 | lockbox |  | 34.746 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_1c5c32a333ca3d97 | fit |  | 26.18875 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_041edb2eb5dcba80 | lockbox |  | 22.470188 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_2da50013c3e3f296 | fit |  | 20.686 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_a7cd3566fab0fb65 | fit |  | 18.610688 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_8ddbada24f339db7 | lockbox |  | 20.085062 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_c636b4ea34ea224a | select |  | 24.71825 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_957cb6c60da17248 | fit |  | 31.050563 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_8cba3f95cf1945cd | select |  | 20.25525 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_4930cf5b4b799766 | lockbox |  | 21.194312 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_09cac5915eac7bbd | fit |  | 22.04 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_3f778e845cebd662 | select |  | 28.04775 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_301da1a94e089f7a | fit |  | 21.3135 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_a16040ff4b29b53d | fit |  | 24.839688 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_27b2ab1fc3585505 | select |  | 39.113 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_1ca4eaba5113a36a | fit |  | 21.942875 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_3a3c205df320c621 | lockbox |  | 27.718 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_94b0dfc2fba182b0 | select |  | 23.281188 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_eb1a5148ff46cde5 | select |  | 21.925313 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_6196ed05cabaeb1d | select |  | 26.328 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_ed1b1b7c67186742 | fit |  | 31.739687 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_96fe08198b5e3852 | fit |  | 23.1285 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_d6d5818642b38229 | fit |  | 19.25175 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_9d05c43c68543443 | fit |  | 22.0 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_0d9f591bfb3dc92a | fit |  | 24.261063 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_f9ff604610bdf7b1 | fit |  | 27.841438 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_082b0c7b97cd2bd8 | fit |  | 23.471187 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_93c9dd351706017b | select |  | 30.231313 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_8553ae65a8ef538a | lockbox |  | 31.971438 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_15a5ac374f60e157 | lockbox |  | 19.976 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_7e1f5ec1b8fa87c4 | fit |  | 22.639437 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_b204feb186442ab6 | fit |  | 21.104125 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_a56b7addc896c053 | select |  | 24.294563 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_ecb28ba11bd1b3d8 | select |  | 32.415062 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_a0380ab83cb01238 | fit |  | 29.78875 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_f77c9d558c455572 | select |  | 22.775125 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_ff06c52a3d06f019 | select |  | 36.594687 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_2ccf62a501aa8ded | select |  | 21.072688 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_c2bb1931cbc48d84 | select |  | 18.387875 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_08676cff606fce2c | lockbox |  | 22.445687 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_a000cd2726a3450e | select |  | 27.871938 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_02bde2d150b264ca | fit |  | 33.126625 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_3d8a351a99d50f32 | fit |  | 20.28675 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_561f0047341d020c | fit |  | 23.754 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_7b002ddb5dae69d5 | lockbox |  | 24.012125 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_94dbff1d4797e712 | fit |  | 25.288125 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_b63ba4f6d516d1e0 | fit |  | 26.791125 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_c8e4e0f427087968 | lockbox |  | 32.516813 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_432fdae1d6122f8f | fit |  | 21.985 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_688e72cf0886c7e7 | fit |  | 18.389437 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_daeb5cd01e397542 | select |  | 20.322688 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_3e2c8ca1cbc3fea4 | fit |  | 26.7795 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_6e9adf501aeab3d5 | fit |  | 27.758063 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_18d6ee334cf691eb | fit |  | 29.559062 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_92b596d916777377 | fit |  | 28.600687 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_9739c68b4a83931c | fit |  | 19.70125 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_144a6af8674935c1 | select |  | 21.462438 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_df09a32d713119c3 | select |  | 24.582687 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_7ac4f12baff7f7bf | select |  | 21.476188 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_7ff6bbe2547c09a2 | fit |  | 23.417063 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_5d300a50ce973d16 | select |  | 23.212187 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_2e0ff9b34adf66af | fit |  | 22.762 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_45906b4219e969c3 | fit |  | 23.736375 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_d6f5c863261c3d76 | fit |  | 18.775938 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_66bb828535970188 | fit |  | 23.162875 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_fd6aea177067bd6f | lockbox |  | 36.193125 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_75f7fbd33862056b | fit |  | 19.6825 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_5c23f6b0048e7e1c | fit |  | 24.489187 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_c74e41c3e7be8726 | fit |  | 48.189312 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_ac4a1ebd27de77db | fit |  | 23.859 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_3750e326521b0fad | fit |  | 25.795 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_744f88fd6a6707f9 | fit |  | 23.334063 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_405dce34b139144a | fit |  | 21.214875 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_29b08b768c13ea54 | fit |  | 24.943562 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_9b2e1f8c2badc06f | fit |  | 21.526375 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_ac0c3f18e2dc5056 | fit |  | 36.709875 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_65e03412a6d0664e | lockbox |  | 21.945375 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_e9dcf6dfa88da683 | fit |  | 21.972625 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_e859360bab7026fe | lockbox |  | 25.021625 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_b9544deb61e08a13 | lockbox |  | 22.282125 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_7af7bf2d6f986f9e | select |  | 20.034125 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_12b8c260c5e89fb2 | lockbox |  | 38.859437 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_f9e3abd3dc6a5c31 | select |  | 29.872625 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_fc4c80ccd005fab2 | lockbox |  | 27.077 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_e42853b4ce300eb3 | fit |  | 22.416625 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_2c30ef3e8c69ff0b | lockbox |  | 22.53325 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_62ee2605b48e107c | fit |  | 21.848562 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_db15d351e2618b2a | fit |  | 24.06075 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_6a4e156d1fb57b33 | lockbox |  | 37.364625 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_f7f416dace600475 | fit |  | 18.796875 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_0eeb9e3692c147ac | select |  | 20.921187 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_702c9df762d82283 | fit |  | 21.468125 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_89e27e643cc7c0a9 | select |  | 32.625937 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_e377d4f41ff0ee4f | fit |  | 20.898 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_65369ae1f7cc561c | fit |  | 24.24425 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_a0e57be777765c1a | fit |  | 31.362063 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_c2cdb7bcfc7cbe25 | fit |  | 19.132687 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_fe34210206d80877 | fit |  | 23.512687 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_9f31aab1609123ac | lockbox |  | 28.811375 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_0e1642e0685c3168 | fit |  | 25.350562 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_9efa095bba54af64 | select |  | 28.334312 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_59ab3d0b2d76a599 | lockbox |  | 18.0 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_5b031aec393b4a77 | select |  | 26.801687 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_54f4055a617fa682 | lockbox |  | 47.4365 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_674e070db5385c3a | lockbox |  | 26.548375 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_2854c579f49bbf28 | lockbox |  | 25.081937 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_b68260941053c0b6 | select |  | 27.850375 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_25af90de4b4a7a83 | fit |  | 22.569813 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_27e40abbd61b2500 | fit |  | 28.631438 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_17e891acb8f4d60b | fit |  | 25.524438 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_597b7ebd4c96f451 | fit |  | 22.48225 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_abd94edaf86a108a | fit |  | 22.231125 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_b681b80e09cad261 | select |  | 24.16025 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_fc0542736b5f0734 | fit |  | 28.998313 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_099079199d07d111 | fit |  | 20.01575 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_d24b9afee6e7a6c1 | fit |  | 20.310125 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_1785043b07209700 | lockbox |  | 22.880063 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_495a461df20d207e | fit |  | 18.321562 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_9956ff56d2432ca2 | fit |  | 18.63275 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_8b9c477bc38c6c9f | fit |  | 22.3965 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_05bbf56e978e5f11 | fit |  | 28.192875 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_2eaf9b20983f13b2 | fit |  | 31.879562 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_f4e8323b015c39ce | select |  | 24.901125 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_41cf9c3cbc8c64fd | select |  | 18.886875 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_5147334eee9af6e7 | fit |  | 39.677062 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_b8215e0e10f64e59 | lockbox |  | 20.166187 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_2fc9fecc914ee81f | fit |  | 22.117812 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_6a09329cb2d19cf2 | select |  | 42.683125 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_3df90709d863a94c | select |  | 20.855687 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_41edbaa1ce60cf30 | select |  | 21.118562 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_b959e26eecc88901 | fit |  | 23.896625 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_de3527277b4dd86c | fit |  | 64.830125 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_c4e9859cecf0c7b9 | select |  | 18.660625 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_9dd0dbf56a2d2ee8 | fit |  | 28.328375 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_8509ad60aa0389a3 | lockbox |  | 23.829687 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_b276685b9521e52c | fit |  | 19.844375 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_140bc90a381a1e2c | fit |  | 21.871688 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_b69aefb234de3cd3 | lockbox |  | 18.819813 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_a6c6a533cfb75e5a | lockbox |  | 24.479312 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_ab26c632e87e26a3 | fit |  | 21.0 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_4f2a146d4f120728 | lockbox |  | 22.271375 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_54a4e8e556a6b60f | fit |  | 20.258813 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_1f4bc33e144e4105 | lockbox |  | 20.305875 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_b6d276e7b604f5ce | select |  | 29.229625 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_f79b0b1e5e963f08 | fit |  | 26.88 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_abe8545eea55f13b | fit |  | 26.6055 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_5b16a14df2550363 | lockbox |  | 22.45275 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_1f6ed314a2b8c38a | fit |  | 26.583 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_36d0794414483151 | fit |  | 30.634313 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_9991e9b1c61c200d | fit |  | 38.148875 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_3f43fe88d298f93f | fit |  | 23.022625 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_82c4cc6b482fe893 | select |  | 21.57275 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_7043fd178b10ff66 | fit |  | 23.127063 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_676aa0b98f7b401a | fit |  | 19.935125 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_bbc0f0c5d6321c8e | lockbox |  | 21.255688 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_760159defce19fab | fit |  | 26.357375 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_465ef1fce61580ce | lockbox |  | 22.510687 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_385ae663f1dd9bae | lockbox |  | 23.865562 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_614791f1a434cddf | fit |  | 17.132625 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_e61d72a1e1861638 | fit |  | 18.08 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_00b57a8c7a747642 | fit |  | 23.82 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_21fd18fedd8486b7 | fit |  | 21.2085 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_03c3381c2a0b3ac2 | lockbox |  | 34.142187 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_917a31c9c5372637 | lockbox |  | 21.078563 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_1ef76b27a49c85a2 | lockbox |  | 26.787625 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_831bb4115aded516 | lockbox |  | 20.341062 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_2e02a3f80179bee9 | lockbox |  | 23.342312 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_00afdfb39f89ec28 | select |  | 25.648812 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_115d7c0192e36c31 | fit |  | 23.755875 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_b73c16d25f505fe9 | lockbox |  | 20.77225 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_ef9abbf4abe7c814 | fit |  | 29.860875 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_f0a6321cccfd9e90 | fit |  | 21.6505 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_7339b3c5a3a61ecc | select |  | 21.912562 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_5443ec94f95a834a | fit |  | 22.720375 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_30fb47be66daabb3 | lockbox |  | 28.452625 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_7184062d56185462 | fit |  | 23.82 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_986b002d8befd07d | select |  | 23.451687 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_636293e044449e9f | lockbox |  | 21.321125 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_85ec0442fcfa9d54 | fit |  | 18.840125 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_31ec4b83ade52f56 | select |  | 24.040312 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_05d8a91621a9bdce | select |  | 18.459875 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_0793a17b170de54b | fit |  | 23.877688 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_1acc8d45ec4702c3 | fit |  | 23.0 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_c993e25636cfd069 | fit |  | 24.395813 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_67cd48b395346af6 | fit |  | 22.51 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_61a66557cc964715 | select |  | 20.41275 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_76ac2e13e9b81f87 | select |  | 21.260313 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_a8bd6e5f7570b5ab | fit |  | 25.267063 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_d243ab799e88159a | fit |  | 20.409063 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_8a22413e59b45394 | select |  | 20.108187 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_16b02472da884c90 | fit |  | 19.02475 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_40178cc8d93ccd32 | fit |  | 25.217063 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_510f6f8790bd3332 | lockbox |  | 17.54875 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_e0829b9061db43e9 | fit |  | 20.657625 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_02ef76cfa1882318 | fit |  | 21.768 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_dfcd56f69c09b884 | fit |  | 40.70375 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_80009b1ca580663b | select |  | 24.688375 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_a47d66678c99ada7 | lockbox |  | 22.925625 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_966042f04c5b379c | fit |  | 19.225 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_3d9f361b40337de7 | fit |  | 22.42775 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_b56868daaa5f2e67 | fit |  | 20.619312 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_871eb79339e89725 | lockbox |  | 19.95325 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_2c88aaae47cc6ebb | fit |  | 25.550875 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_a2ed91e21098a595 | fit |  | 26.495 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_f7bacf6174271c92 | fit |  | 31.485688 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_b87916deab19b00e | fit |  | 24.89 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_1c6ee6875360bce8 | select |  | 21.376062 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_0e78c4a9e6848f04 | select |  | 22.593 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_c24c928b3c514fdb | fit |  | 35.09525 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_15ef92d45f719e87 | fit |  | 23.723562 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_30f70823bce33c7b | lockbox |  | 24.437875 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_27d2b3450886ee19 | fit |  | 48.931188 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_94c6387f23718e79 | fit |  | 20.886688 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_c7fe1cf42e8a6b3f | select |  | 20.282125 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_6aa296196624bfca | select |  | 21.370812 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_98432ceb9e1b93a9 | lockbox |  | 35.062125 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_9e283bd9fa90022f | lockbox |  | 35.64225 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_681fed654e0f21b3 | fit |  | 32.09275 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_e6ebea8cfb1247c5 | fit |  | 19.435125 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_5bfae8213414fb40 | lockbox |  | 23.290312 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_4d95b3816ce40a1e | fit |  | 23.963 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_e90e02f6a552ec26 | select |  | 19.89175 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_1fb0c57f392172e7 | fit |  | 21.193 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_5c9c240e210ed9b9 | lockbox |  | 25.030313 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_9d333423dfd2868f | fit |  | 24.865687 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_ccc70ecdfab2efec | fit |  | 21.32275 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_c97db22648167718 | select |  | 17.714688 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_e86b196bd1432c4d | select |  | 20.708125 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_18354799e68bc10d | select |  | 21.59425 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_54d2c5c9e5ba3f27 | fit |  | 24.7065 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_f29e5eb2802942e3 | lockbox |  | 46.551375 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_c358f583ce0bcfed | lockbox |  | 18.156688 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_81d3c90ae1e4e8d4 | lockbox |  | 43.742125 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_3a115d9ab545b2f5 | fit |  | 19.112813 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_7a243f089089e1b0 | lockbox |  | 31.378688 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_083e88ea5f5f2aaa | fit |  | 21.803687 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_5c0475e679b172b4 | lockbox |  | 42.114562 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_e03e05250934798c | fit |  | 60.789125 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_67d41dd020afd307 | fit |  | 28.575937 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_f09bb6a34c8e7a86 | lockbox |  | 21.399188 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_cb90c5ce0a7831e5 | fit |  | 21.866813 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_1a25711b6a8bff39 | fit |  | 22.07475 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_60aa6c2e7137685a | select |  | 20.644938 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_6c247d6521a52fb5 | lockbox |  | 24.515625 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_295807b5f9daabde | lockbox |  | 17.697937 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_03efad6d23f427c2 | fit |  | 32.09 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_2cc9c271a9a69ce6 | fit |  | 23.138687 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_d5f308b31a74cbb9 | select |  | 18.423188 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_3c43aaa1c792d02c | select |  | 24.983375 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_e356b2c843b0b32c | lockbox |  | 23.093812 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_bbcf8bdb63ede50b | select |  | 29.682312 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_c0ee40f51400050f | fit |  | 21.981 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_9347fa9c2075aae9 | select |  | 55.92175 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_a39704bc7d537529 | select |  | 24.563188 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_81bdc8f54b137e92 | fit |  | 32.556063 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_8704757f660e1f1c | select |  | 19.002375 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_a9e53e4d3170621d | fit |  | 27.60775 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_270b8ff14b7628de | select |  | 30.077437 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_6a91922c4ce0604a | fit |  | 35.15375 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_1fdf95450b9ac372 | lockbox |  | 19.226125 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_7b3714bb5861a267 | lockbox |  | 22.078875 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_876c2298d1adfe6d | lockbox |  | 22.51175 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_fbe17844d0e48699 | lockbox |  | 21.092875 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_b07ecdd6945b7424 | lockbox |  | 26.78425 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_67626aa2198ed9ed | select |  | 22.0 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_df5b7795f3c20366 | lockbox |  | 25.95475 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_6f780e8a0c08da59 | fit |  | 20.143313 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_363757b1ea7f006a | fit |  | 33.724562 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_0b3519fcf78bf96b | select |  | 24.595562 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_d10bf2530122fbc2 | lockbox |  | 25.296312 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_b18f790ffbe22b33 | lockbox |  | 22.407 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_d761b32b5adddd27 | fit |  | 20.933375 | 69 | CC BY-NC-SA 4.0 | https://creativecommons.org/licenses/by-nc-sa/4.0/ |
| null_a68d0cec38607f69 | fit |  | 14.340563 | 44 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_844bbce4d11c19a1 | fit |  | 19.673375 | 44 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_59cefd4097747e65 | fit |  | 19.718 | 44 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_6220a28a9828475e | select |  | 12.479688 | 44 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_0bd38ecfa63f5a35 | fit |  | 16.918437 | 44 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_bb167762592f1918 | select |  | 17.805563 | 44 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_ac6597203f2d7269 | fit |  | 13.982563 | 44 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_a0573a470b3624b7 | select |  | 12.650937 | 44 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_33b4b9c2a1f37cca | select |  | 16.58925 | 44 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_7fd5a1ec5d2cbc5e | select |  | 15.245688 | 44 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_1eddf78b0f9b37b8 | fit |  | 19.110875 | 44 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_6ae97fcc4109e9a8 | fit |  | 12.750063 | 44 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_a753195c180629e2 | fit |  | 15.934938 | 44 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_7f5ec542956ac093 | select |  | 16.223562 | 44 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_925b34622e818f2d | fit |  | 15.941062 | 44 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_9c35eaf5be303a81 | select |  | 13.39425 | 44 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_c2aa74713b1c7809 | select |  | 16.675375 | 44 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_8f7ba5bc023e7a4b | select |  | 19.981125 | 44 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_8fba7182b8b3553a | fit |  | 14.950812 | 44 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_12c108e6143c3900 | fit |  | 20.120438 | 44 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_2a11f85e752e329e | fit |  | 16.748 | 44 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_314de80a668490db | select |  | 18.544937 | 44 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_9bd4ac61b69739f3 | select |  | 12.89225 | 44 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_ccbbf1f53b4896b4 | select |  | 13.703563 | 44 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_1276e37998cac3bf | select |  | 16.291438 | 44 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_28f9dd99c0d909d4 | select |  | 15.530938 | 44 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_e308c018bec40ab5 | select |  | 12.956437 | 44 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_56185b5a99dba066 | select |  | 16.609813 | 44 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_26dd2111d707598f | select |  | 17.714437 | 44 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_8512db5a13b0c001 | fit |  | 15.435187 | 44 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_e154cfbc4ee14f76 | fit |  | 19.467063 | 44 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_4a549ecd8c7652cf | select |  | 16.502688 | 44 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_79552a7f46277956 | fit |  | 16.34425 | 44 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_e6a99cd987c42499 | fit |  | 17.507375 | 44 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_1c0c472fece0b8f8 | select |  | 15.672375 | 44 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_b491be50d77ac99e | select |  | 17.643937 | 44 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_da6dde98bc64d10b | select |  | 20.297563 | 44 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_03d1890075812b10 | fit |  | 20.009687 | 44 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_82b34488ddfc92c0 | fit |  | 16.672125 | 44 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_804a65aa205a26a6 | fit |  | 18.533562 | 44 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_0b0474140601ca7c | select |  | 12.01225 | 44 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_f8641fe205b4dc16 | fit |  | 16.852563 | 44 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_a04663220529bc05 | fit |  | 17.06725 | 44 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_46e330304a8654b6 | select |  | 13.575688 | 44 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_68adcb9851afedcc | fit |  | 17.795125 | 44 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_ed97adf7957e59f4 | fit |  | 13.341625 | 44 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_019fb0ebb3fefe48 | fit |  | 14.67575 | 44 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_35916df758790330 | select |  | 13.587563 | 44 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_3220cec5c13e9065 | select |  | 17.922313 | 44 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_046d3581ffad363d | fit |  | 16.872625 | 44 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_969844d6f9960af6 | fit |  | 15.255812 | 44 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_e839327b5583a054 | select |  | 19.458875 | 44 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_4d86d84b6f214bb1 | fit |  | 16.42825 | 44 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_7b6fd1c3e196ec5d | fit |  | 15.9875 | 44 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_d1a4f39b223a2ba8 | fit |  | 18.985312 | 44 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_d5f4be12fe5db9e7 | fit |  | 19.770125 | 44 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_55b92a0337ec0c0f | select |  | 16.07 | 44 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_2cbf2f20ebea6dff | select |  | 13.996625 | 44 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_3af973edb4557d2d | select |  | 13.276875 | 44 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_4f75fa0061d248e8 | select |  | 15.791875 | 44 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_c133b03a7a09c09e | select |  | 12.932625 | 44 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_e4e2e1ab2650010f | fit |  | 12.639688 | 44 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_081fc627d139d215 | select |  | 12.37 | 44 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_2b339698032e4237 | select |  | 16.59775 | 44 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_30944a709e7e0e0e | select |  | 14.291438 | 44 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_46ea1cd03f85b4b4 | select |  | 13.215938 | 44 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_cf8edd539bda4b0e | select |  | 18.52025 | 44 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_a16ce366a4b7ca0b | select |  | 16.124375 | 44 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_692e4336cd91c549 | select |  | 16.706 | 44 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_046856dbfe190f69 | select |  | 17.473437 | 44 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_6a1d49ea7fe44cb5 | select |  | 13.75725 | 44 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_6e020d4f1534740d | select |  | 18.369937 | 44 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_31499dcba1487915 | fit |  | 14.177188 | 44 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_8b4db04b56688cdc | fit |  | 13.388188 | 44 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_adc28385f899f582 | fit |  | 11.230937 | 44 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_5f1e2436604c5c96 | fit |  | 17.742438 | 44 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_f189ed2e097d8da5 | fit |  | 19.817312 | 44 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_6c5a4597bec8c233 | fit |  | 16.384 | 44 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_cde81f72a726e84a | select |  | 18.713875 | 44 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_ba115ee6457d8860 | fit |  | 16.555375 | 44 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_3e9dcfa03015201e | fit |  | 16.78775 | 44 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_ae3955db98cb8173 | fit |  | 19.720813 | 44 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_345e754473a58d03 | fit |  | 18.052187 | 44 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_241f7b594681615e | select |  | 18.801063 | 44 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_277ed2b2064f13b3 | select |  | 14.175562 | 44 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_025966763f7e074b | fit |  | 17.833687 | 44 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_683760d0fe89f04c | select |  | 13.389313 | 44 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_245ff80dd64004e6 | select |  | 15.317187 | 44 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_e968741be0890c4d | select |  | 12.574687 | 44 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_e935c07c7478cca0 | select |  | 14.208 | 44 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_e982f01541163537 | fit |  | 18.213938 | 44 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_0ddfbb0c155a5e58 | select |  | 17.776375 | 44 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_9fa56c336f25aca8 | fit |  | 14.781562 | 44 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_75709d58955f8b6a | fit |  | 13.357563 | 44 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_0dbaa708e014a6a6 | fit |  | 22.973125 | 44 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_d1f2e1cd738df7dd | select |  | 14.841563 | 44 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_dddb77caaab1054f | select |  | 15.286437 | 44 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_14c74c4e14f22d01 | fit |  | 18.388375 | 44 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_5124216f881f1f63 | fit |  | 15.803375 | 44 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_781e3564ba80284e | fit |  | 14.745062 | 44 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_dfd28780a2cd1c37 | select |  | 15.854688 | 44 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_6fd3f346e91b4f72 | fit |  | 15.08825 | 44 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_ff8f5b35ee1be013 | select |  | 12.628063 | 44 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_c555e640704ae771 | fit |  | 15.541063 | 44 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_94e8e64595fc9e4b | fit |  | 13.877688 | 44 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_0bbb93f29ddea2f9 | select |  | 13.911875 | 44 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_6024a39aa2a70476 | fit |  | 18.150312 | 44 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_7101fcb49bbeef42 | select |  | 13.526188 | 28 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_c6c814b5567235c4 | fit |  | 9.43775 | 28 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_6336a851673a3392 | select |  | 13.55575 | 28 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_2066f0ab9d477e1c | fit |  | 15.80575 | 28 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_b1ff849684ecce2b | fit |  | 12.655563 | 28 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_a3761c252c6f4de2 | fit |  | 19.651125 | 28 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_3f35910a36dfdd01 | select |  | 11.498563 | 28 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_b9d3e11c9a612e68 | select |  | 13.012375 | 28 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_17b3679cdd6984b5 | select |  | 13.082688 | 28 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_8088d9f9fd9586c2 | fit |  | 9.72775 | 28 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_e3623ba95dfc6c5c | fit |  | 13.134562 | 28 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_a9bf71961483981e | select |  | 15.48575 | 28 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_b7f263818f91beb3 | select |  | 14.818312 | 28 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_92591216d57a8da3 | select |  | 15.345562 | 28 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_8fca1bef9e8cdbc7 | fit |  | 12.119438 | 28 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_2793580aeb05c399 | select |  | 10.967562 | 28 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_f58c9ee8d9fb9dd8 | select |  | 10.261688 | 28 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_677c5f331e2d4e1b | fit |  | 12.137 | 28 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_054ee36fac66a8a8 | fit |  | 13.185438 | 28 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_2746a2f2023ff21d | select |  | 11.348562 | 28 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_134409e62cd4b95c | fit |  | 10.434938 | 28 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_6b2e471991a532b6 | select |  | 12.405875 | 28 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_34804ac2ad64d3ed | fit |  | 13.234875 | 28 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_f12673888b2306b5 | select |  | 14.22775 | 28 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_e691e5f2fb54d2c7 | select |  | 10.39975 | 28 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_c4e635dc012cc3ff | fit |  | 15.271 | 28 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_7222385d2e9f3415 | select |  | 12.780313 | 28 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_2d97e2ab9ac80551 | select |  | 13.040812 | 28 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_e7d94559f722f88f | fit |  | 11.799812 | 28 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_c37a7d805531e6a2 | select |  | 10.0225 | 28 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_b858ab584c297aee | select |  | 12.163937 | 28 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_b311b82354503c4b | select |  | 11.199813 | 28 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_735a64a400258973 | select |  | 10.001188 | 28 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_a8511675dc799921 | fit |  | 12.07225 | 28 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_03cf91a11fd4d5f0 | select |  | 9.9245 | 28 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_1b4ed2158fe7de3a | fit |  | 15.013687 | 28 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_adf52e840c3b7dbc | select |  | 12.827188 | 28 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_9ee8ff2df3e9ae18 | fit |  | 10.361688 | 28 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_6a1e32b580ca268a | fit |  | 10.953 | 28 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_cdeee0ecccb72ee8 | fit |  | 15.821125 | 28 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_e257c5c2ca4786a4 | select |  | 14.908375 | 28 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_f6f652e5476dc300 | fit |  | 12.840563 | 28 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_2e351a758b2a9491 | fit |  | 16.369937 | 28 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_432d065e31338abf | fit |  | 16.452875 | 28 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_650cb1c2cae2549b | fit |  | 11.674125 | 28 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_de0e1100e5e2dd12 | select |  | 14.60975 | 28 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_17d9215bb9aaacff | fit |  | 10.654375 | 28 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_ba33ef233ad28321 | fit |  | 13.483688 | 28 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_e4030a1f124ec272 | fit |  | 13.33075 | 28 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_510c666359623ed1 | fit |  | 9.31225 | 28 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_a91c69616e23458f | select |  | 10.81625 | 28 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_2866e371bdbf85b2 | select |  | 11.448313 | 28 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_a001a79445f44c59 | select |  | 14.21625 | 28 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_b33f4daf6075020f | fit |  | 10.753813 | 28 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_bcce645ff5594c48 | select |  | 10.074438 | 28 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_232ea41745e274cc | fit |  | 11.986187 | 28 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_41723d52fde172de | fit |  | 13.227625 | 28 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_193162924dc55404 | select |  | 12.362125 | 28 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_aa57e13958f425e1 | fit |  | 12.407813 | 28 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_fb19a099c49864f3 | select |  | 13.628875 | 28 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_2be30873f326f9b3 | fit |  | 13.31675 | 28 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_e149c93bc8a4c036 | select |  | 11.25725 | 28 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_b683903d0b66b18a | select |  | 13.835 | 28 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_9e3f4df0f7126260 | fit |  | 11.58425 | 28 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_371abe14a49283af | select |  | 10.143437 | 28 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_dd7b11796f38ca60 | select |  | 12.208312 | 28 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_e75c5bd7a4e19179 | fit |  | 11.980813 | 28 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_efbfadfe97903df6 | fit |  | 15.20825 | 28 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_e726b83c29ec8e46 | fit |  | 11.46725 | 28 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_5bcc5da65ac43806 | select |  | 10.505688 | 28 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_bdffcbf2a061c2b6 | fit |  | 10.417 | 28 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_a2547b52da3e9681 | select |  | 16.39375 | 28 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_ed89cc4f713aba24 | select |  | 11.148188 | 28 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_b6968b6a4000b246 | fit |  | 13.62325 | 28 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_986e920bb39bf5ec | select |  | 10.991 | 28 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_08108a92c64e5c22 | select |  | 9.75175 | 28 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_f1dad3a2069af332 | fit |  | 15.08625 | 28 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_e9a520e6852b10c4 | select |  | 9.574125 | 28 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_191aee0faea47e5d | select |  | 13.571312 | 28 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_acbf854bec149149 | select |  | 14.144625 | 28 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_d55906be816af1f4 | select |  | 10.393875 | 28 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_bf057c047ecee4f5 | select |  | 14.421625 | 28 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_6775b6eb36103a9f | select |  | 16.670813 | 28 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_396e07320254539c | fit |  | 12.378125 | 28 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_b99e876f218fc85a | fit |  | 10.86775 | 28 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_fd66b69e77f24dbc | fit |  | 11.653438 | 28 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_a5806fff8a978083 | select |  | 15.786188 | 28 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_53a87be2d05d2a24 | fit |  | 12.778688 | 28 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_c8ca4270d3f99bcd | fit |  | 15.032312 | 28 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_ddff3c64679860af | select |  | 11.375875 | 28 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_497e5659eb916a8f | fit |  | 11.966062 | 28 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_d73458a9499e890a | select |  | 10.802312 | 28 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_1a498a29e07e41dc | fit |  | 13.39775 | 28 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_f9b4df23f8557870 | fit |  | 10.570813 | 28 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_3a5154e2064fb284 | fit |  | 9.5195 | 28 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_52379551df6f0a81 | select |  | 13.458125 | 28 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_b5276d4c50f9bc09 | select |  | 11.015063 | 28 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_4c7e5844ec4c0564 | fit |  | 11.951187 | 28 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_f1e39a84eaf4757c | select |  | 14.80175 | 28 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_a39218d67bed28c5 | fit |  | 13.623812 | 28 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_2ce091742cc62363 | fit |  | 11.4585 | 28 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_e9005d0ce62aaa74 | fit |  | 12.062875 | 28 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_e64795bf325bf423 | select |  | 14.341812 | 28 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_29f26aa4bbfefdfc | select |  | 10.471 | 28 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_9546612c64b44205 | select |  | 12.596687 | 28 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_1a925781fb998963 | fit |  | 15.525813 | 28 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_d831ab7d67821140 | fit |  | 12.5435 | 28 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_1269c796e0cabb69 | select |  | 12.388875 | 45 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_dd3aa616a4df309b | fit |  | 12.739313 | 45 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_0461bf2eebc5f158 | select |  | 13.032125 | 45 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_eb2490923e82d030 | fit |  | 15.347875 | 45 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_7d1a62c6702159b3 | select |  | 14.090938 | 45 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_58c0f277cf5613c7 | select |  | 16.991688 | 45 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_6ff9720ccee79c16 | select |  | 17.438375 | 45 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_761e2fed4a29c111 | fit |  | 14.317375 | 45 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_d6f9d5fa2e71e4a4 | fit |  | 14.88325 | 45 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_c7303b50357eaa2f | select |  | 17.275125 | 45 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_5d27220c404c184e | select |  | 20.461125 | 45 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_9c9fdb4c3cea7dc2 | select |  | 12.309625 | 45 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_1aac9b3389a03e07 | fit |  | 14.373875 | 45 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_c3f537147ab4fd75 | select |  | 12.577875 | 45 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_6fe904c5fe0a05a2 | fit |  | 15.650438 | 45 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_130cac47fed71c1b | fit |  | 16.578063 | 45 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_ad54068d0297a484 | select |  | 15.335625 | 45 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_01eef63a8bd0973d | fit |  | 15.576875 | 45 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_20c418dfa99fde78 | fit |  | 15.69875 | 45 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_8bc654e0be52b375 | fit |  | 16.92025 | 45 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_b285d559f08a13cb | fit |  | 16.987562 | 45 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_7741098f2dcda00d | select |  | 10.695625 | 45 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_898a1717a7ea87f2 | fit |  | 15.27875 | 45 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_d9762054aa50be73 | select |  | 14.205875 | 45 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_078f7d9bc6b4e9aa | select |  | 12.853687 | 45 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_ccef10d0393ae97b | fit |  | 15.434812 | 45 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_2f02cd4b5f1798a5 | select |  | 15.90375 | 45 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_f57f7614d4dd5484 | select |  | 19.392875 | 45 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_fa1f5d2c99d4e79d | select |  | 13.943125 | 45 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_9fad8a73c3d93abc | select |  | 13.276938 | 45 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_8256f8f392a15f88 | fit |  | 14.55425 | 45 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_d1bc76e9ec2bb9ed | select |  | 11.918375 | 45 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_14a164fa3a8f8201 | fit |  | 17.825125 | 45 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_de8885dd83aa3fd2 | select |  | 15.24 | 45 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_56e8a7e5fc26659a | select |  | 12.87225 | 45 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_77a474ca1d803772 | select |  | 14.92925 | 45 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_663eb6a4a7dcdb6e | fit |  | 11.956125 | 45 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_5eb04085bd3c11ae | select |  | 13.434375 | 45 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_f6502af5e933dabe | fit |  | 13.571063 | 45 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_e6babdcace971585 | fit |  | 17.087062 | 45 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_0d75595e1a53a155 | select |  | 16.27625 | 45 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_1061a706f4a7c1dc | fit |  | 15.22525 | 45 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_b0314184359fb148 | select |  | 11.800437 | 45 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_5f9bd7910bc21965 | fit |  | 14.693563 | 45 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_d649871cbde0a180 | fit |  | 15.130688 | 45 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_5893c013bd34812d | fit |  | 13.36125 | 45 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_c4f64a436da4af2f | fit |  | 13.2905 | 45 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_db6220d17efd5daf | fit |  | 19.323062 | 45 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_5b7cbb866046680b | select |  | 12.281812 | 45 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_e204e48319ffe21b | select |  | 17.467312 | 45 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_86ee433eb6077b54 | fit |  | 13.3635 | 45 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_97a22661ab71b782 | fit |  | 13.824 | 45 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_654832cd9897cc13 | select |  | 14.977125 | 45 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_8d7cde3ad7e7a8c7 | select |  | 14.228438 | 45 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_632ef2c975ba35de | fit |  | 13.77825 | 45 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_06450b315f29c368 | select |  | 16.750937 | 45 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_af43598df1fc8721 | select |  | 12.218125 | 45 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_5626293c152f737e | select |  | 21.060875 | 45 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_474b52a502b586f2 | fit |  | 16.54425 | 45 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_6d89bc4cdfe95ab9 | fit |  | 16.63075 | 45 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_4240d33d934caaf7 | fit |  | 16.96925 | 45 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_e6ded7a6dfa9604b | fit |  | 15.287125 | 45 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_c2ce1813b43b3068 | fit |  | 14.384187 | 45 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_3dbd28cb68a41dfc | fit |  | 13.432813 | 45 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_63d356bdc92e236b | select |  | 14.103188 | 45 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_a584c2529438f4b6 | select |  | 15.287688 | 45 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_893b841d31f9bad7 | fit |  | 16.916937 | 45 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_2c08570b552c4184 | select |  | 11.901188 | 45 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_e69e41adf71c415b | select |  | 15.139812 | 45 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_aa3303295c29d4aa | fit |  | 15.235812 | 45 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_20c2981a3d04f492 | fit |  | 17.766813 | 45 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_b90a09b586558ce0 | select |  | 16.49675 | 45 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_044a2d37402a382e | select |  | 14.317937 | 45 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_99a7cc8857335f23 | select |  | 13.23525 | 45 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_0c2120a2cf28abd6 | fit |  | 15.970313 | 45 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_31e7027ec6b1e31a | select |  | 14.64375 | 45 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_5fd90eacc6d71519 | fit |  | 16.916438 | 45 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_5c7945a7ed3d7696 | fit |  | 13.975375 | 45 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_0e5ffd704f253f19 | select |  | 13.10675 | 45 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_e604d1191638a06c | select |  | 15.622375 | 45 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_345c6f0471c8776f | fit |  | 16.707375 | 45 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_0276e20377708910 | fit |  | 14.505625 | 45 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_d0de05c50020728f | select |  | 13.671688 | 45 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_0af65ab61427de62 | select |  | 12.806437 | 45 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_8408d34d4ec8caa5 | fit |  | 21.47375 | 45 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_aaa16ff25596e8f7 | select |  | 13.719625 | 45 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_c3322d1fcfa45874 | fit |  | 14.056437 | 45 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_0786d1e06a60131b | fit |  | 11.437875 | 45 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_f486316503e6f691 | fit |  | 13.562625 | 45 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_b2c2c1270da7ba5b | fit |  | 15.648062 | 45 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_5f94aa515adffce2 | fit |  | 17.238 | 45 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_1e0b49df0f415768 | fit |  | 15.260687 | 45 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_7afe358137ffafdd | select |  | 13.042188 | 45 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_adeb211111288798 | select |  | 17.7135 | 45 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_bba5906fd9179f53 | fit |  | 14.15125 | 45 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_299e21c2642ebaad | select |  | 13.91975 | 45 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_383bce85fe172f85 | select |  | 16.029062 | 45 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_c21676477ebf0c67 | select |  | 16.873812 | 45 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_018215c7ded467f3 | select |  | 15.524875 | 45 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_55833b3628296db6 | fit |  | 20.63125 | 45 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_d1819b534096faa9 | select |  | 14.60125 | 45 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_bc40a8edc270446d | fit |  | 13.088875 | 45 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_1db9df646444140b | select |  | 16.802312 | 45 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_3ea2331d5d79c41c | fit |  | 14.856188 | 45 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_51ea53c19b2b8538 | select |  | 15.941875 | 45 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_9bf27aa8db570e07 | select |  | 12.444625 | 45 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_2c4c4e27051bb949 | fit |  | 12.212125 | 45 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_819cad33a03e13e2 | select |  | 9.592 | 29 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_021b3f03b4c9429d | select |  | 10.552375 | 29 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_5bdca13c42960b48 | select |  | 12.520875 | 29 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_3691272637fb393a | fit |  | 9.998188 | 29 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_39695436771313e4 | fit |  | 9.56125 | 29 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_eb1ca046ecc30cf0 | fit |  | 11.393688 | 29 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_42a020b206d083c3 | fit |  | 7.4915 | 29 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_c7156d6b62d52047 | fit |  | 13.67125 | 29 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_3dc9cdd2b510300d | select |  | 8.21375 | 29 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_3cc202164b0a89f4 | fit |  | 11.2835 | 29 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_36c7feeae7672624 | select |  | 12.718375 | 29 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_b97389419a8d83da | fit |  | 12.391937 | 29 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_2c6eb8865ad0b0be | select |  | 10.221875 | 29 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_2adb2699ec9acf1a | select |  | 8.875 | 29 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_f91cc56dd4e1426b | select |  | 8.915313 | 29 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_7960e1baf4511eeb | select |  | 10.107188 | 29 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_314e11aa19dbc9b4 | select |  | 13.966125 | 29 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_e15b6e4dc66da097 | fit |  | 11.098625 | 29 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_d4814a392a6e1376 | fit |  | 9.961688 | 29 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_ea9e0bd665ce6253 | select |  | 10.902313 | 29 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_085fa1bca5ea9d7d | fit |  | 12.595875 | 29 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_ec3f558c136a5e5d | fit |  | 9.070125 | 29 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_16242ef250075771 | fit |  | 10.4975 | 29 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_7e49717da051d519 | select |  | 10.975375 | 29 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_c06f1563454bde6d | fit |  | 9.658687 | 29 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_ca6d64d7bc6093e8 | select |  | 12.090375 | 29 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_128c39144b23c99e | fit |  | 12.17875 | 29 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_16b421786ac5606d | fit |  | 13.436625 | 29 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_364e2b8bfd047c29 | select |  | 11.32725 | 29 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_ac4bf95e9b2283b5 | select |  | 10.833562 | 29 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_90ba43b4763500f0 | fit |  | 13.83075 | 29 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_c7e85a11e5997e62 | fit |  | 9.998188 | 29 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_1903a837ee6af56e | fit |  | 9.305125 | 29 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_613ae62ba9c82826 | fit |  | 11.073438 | 29 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_a2621c4723bd54aa | fit |  | 8.165188 | 29 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_a13f8c8007a74a1c | select |  | 8.854563 | 29 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_12de241e1c6e63eb | select |  | 14.58775 | 29 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_ef9de52cf8235c5d | fit |  | 10.973187 | 29 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_e916fc8db2837244 | select |  | 11.358313 | 29 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_4045296b015d5918 | select |  | 10.291688 | 29 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_c04927ddefc91ace | fit |  | 11.413438 | 29 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_151a44c33faefc0c | select |  | 9.933125 | 29 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_966b68bad3ee7c53 | select |  | 11.447875 | 29 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_37d8a179a339d1e9 | select |  | 8.964375 | 29 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_f7a7e3be69c3a4e8 | select |  | 12.153875 | 29 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_be3669b312000356 | select |  | 11.99325 | 29 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_3d71c36f854d515c | fit |  | 9.293938 | 29 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_1c96f5828d36f1c4 | select |  | 8.86475 | 29 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_7ebb220544a0486f | fit |  | 11.071438 | 29 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_76f58f311e84c50e | select |  | 9.339375 | 29 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_a205174dd3796f7c | select |  | 11.10175 | 29 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_e1c6dae4378896a0 | fit |  | 10.26875 | 29 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_74e548a07675314d | select |  | 9.404125 | 29 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_8ea6960393c3122b | fit |  | 11.342688 | 29 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_2ded8af5007e4910 | fit |  | 9.6865 | 29 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_31de8e45f4b385b5 | fit |  | 11.030125 | 29 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_e196109cc91b5f99 | select |  | 10.127313 | 29 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_e28a5e7f0072e606 | fit |  | 11.786062 | 29 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_d23c0d99869b59c0 | fit |  | 14.248875 | 29 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_77e6a88d8bca5271 | fit |  | 9.848375 | 29 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_823c204a7e3d6559 | fit |  | 8.683125 | 29 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_026524107da74e7f | select |  | 8.590813 | 29 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_bdb0ee6dbb1e422e | select |  | 12.017062 | 29 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_3a15f9bd43c004cd | select |  | 10.754437 | 29 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_5c12b5dcd1aa7801 | fit |  | 11.497063 | 29 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_82afeab13cf749ca | select |  | 11.284125 | 29 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_46d3fa2e70946316 | fit |  | 10.74125 | 29 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_8994dd9f40fd7b7c | fit |  | 12.224375 | 29 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_217b76afd7e828e2 | fit |  | 10.497625 | 29 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_1a3b93c8d7512023 | fit |  | 10.5915 | 29 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_098eeab7cb0fc6bd | select |  | 9.323875 | 29 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_bfcec4b6dfe473c0 | fit |  | 11.40925 | 29 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_bf74150e7da20810 | fit |  | 10.151938 | 29 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_539862d8779dc044 | select |  | 9.142188 | 29 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_c32cd507e77812a6 | fit |  | 13.126812 | 29 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_2bfc8c58623d1fe0 | select |  | 10.239187 | 29 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_492d6a3ee933d6c4 | fit |  | 11.350437 | 29 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_8e72511beb9fc8a7 | fit |  | 11.979688 | 29 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_a1f2562df2e12fbf | select |  | 12.5705 | 29 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_0dcd1225327ac639 | select |  | 9.861437 | 29 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_5db9beaf0392947c | fit |  | 12.135813 | 29 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_05f62db49172717c | fit |  | 10.823 | 29 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_1f3d6ecd8c2141c7 | fit |  | 13.275187 | 29 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_075d0fd444d53aaf | select |  | 9.029625 | 29 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_3d37c2fa0cb084a7 | select |  | 8.621063 | 29 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_3fb4b01a45ddeea3 | select |  | 11.428125 | 29 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_6a9dbb873bcbc071 | select |  | 12.484875 | 29 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_caa0a2e405b39b1a | fit |  | 11.986625 | 29 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_886efddd099d16be | fit |  | 9.917063 | 29 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_6d0f52d82f3168cc | fit |  | 12.316437 | 29 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_3a340e9303895151 | select |  | 9.026063 | 29 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_99ed2c670c0c016c | select |  | 12.297437 | 29 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_745cf06fe1c04977 | select |  | 11.585688 | 29 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_6bae77a1220ea274 | select |  | 9.795375 | 29 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_3f47e4deae953414 | select |  | 9.467063 | 29 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_4efd6b6a728c09bd | select |  | 10.964562 | 29 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_c0838c58c03be17f | fit |  | 11.472375 | 29 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_e4409922bd556bdb | select |  | 9.551375 | 29 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_51db7a0604dba0f1 | select |  | 7.718438 | 29 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_3d6801169b42b771 | select |  | 10.6485 | 29 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_4da5f7ab588995fc | select |  | 12.911875 | 29 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_112b82d15e29513b | fit |  | 13.298187 | 29 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_61e2070a6c6b4dd1 | fit |  | 9.751563 | 29 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_75ddfa8f71d3c199 | select |  | 11.623563 | 29 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_94c29a672755af19 | fit |  | 11.217438 | 29 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_9d924b412216f1a3 | fit |  | 9.742125 | 29 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_36b4a91ec1370f93 | select |  | 10.12925 | 29 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_479623baaa4e56a5 | select |  | 13.546188 | 35 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_1a355b745b0652a6 | select |  | 14.499562 | 35 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_cefa6ecb01f6f500 | select |  | 13.977562 | 35 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_a9457c514778c49d | fit |  | 10.856687 | 35 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_dfee77ba2ecf15ca | fit |  | 13.143313 | 35 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_b994b46b34ccbc02 | select |  | 15.659688 | 35 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_c68a94db54c3333d | fit |  | 14.135563 | 35 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_627507c96e9dc83b | select |  | 11.0575 | 35 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_d5954386521b917d | fit |  | 13.6675 | 35 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_16ba30ac1805f508 | fit |  | 14.342875 | 35 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_fdca226b9ffcc83a | fit |  | 15.04975 | 35 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_0c0ab589fa5883cd | fit |  | 9.99525 | 35 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_08316b98c956180e | select |  | 15.326125 | 35 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_781f228affdd0e03 | fit |  | 15.9975 | 35 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_6e1ec6ed837cb44a | fit |  | 14.317562 | 35 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_9dd3bcf28179faed | select |  | 14.154563 | 35 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_b44329c0098385b8 | select |  | 11.602063 | 35 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_6d5aae8fb5f2a01c | select |  | 16.539437 | 35 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_8fab8b1a18078b8c | fit |  | 13.919125 | 35 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_9e425ec345ae9ba0 | select |  | 13.38425 | 35 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_33af7080a51c8187 | select |  | 14.949125 | 35 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_27288b2145dc1c12 | select |  | 14.135875 | 35 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_5b3a14982294a5fb | fit |  | 17.018812 | 35 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_466209a57b51f51c | fit |  | 12.076875 | 35 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_c731d79975b2211e | fit |  | 15.370688 | 35 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_a12140cff2447447 | select |  | 11.77325 | 35 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_66ddd8f3650fa025 | select |  | 12.563 | 35 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_d2406835473c177c | fit |  | 15.595937 | 35 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_04ef6c89daa6202c | fit |  | 12.415437 | 35 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_9d2fd5d85215ec0c | select |  | 11.754 | 35 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_6911bdf7d6b0d72c | select |  | 16.44575 | 35 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_9dbf6d5bcef76d90 | select |  | 14.4835 | 35 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_af4e716e6b4b3363 | select |  | 12.208687 | 35 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_1b77397ed4efcf3f | fit |  | 14.52325 | 35 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_42a5c353e721d399 | select |  | 17.29225 | 35 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_76bf448eae6a43c7 | select |  | 13.596375 | 35 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_3b05f27f993e9685 | select |  | 12.504375 | 35 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_e813b166b925f415 | fit |  | 14.31975 | 35 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_18a7496c6ee40ac6 | select |  | 12.363687 | 35 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_f41cf6ff3e85a271 | fit |  | 16.26375 | 35 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_9a7042bdcb047e7c | fit |  | 11.418313 | 35 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_f2fcfb4c0c61ba05 | select |  | 15.835562 | 35 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_0257308d0be70728 | select |  | 14.80775 | 35 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_db60dcf0d08127c1 | fit |  | 14.292687 | 35 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_315771167257de34 | select |  | 11.522 | 35 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_959f56bcd441f142 | select |  | 13.892563 | 35 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_196bf38534ae9dd1 | select |  | 15.597938 | 35 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_bd1656639d7f838c | select |  | 13.558687 | 35 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_4c9e05778d58fd2b | fit |  | 12.967125 | 35 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_a682075b112a7fa2 | fit |  | 10.69675 | 35 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_746fdecaf82e0432 | fit |  | 13.019937 | 35 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_085ac21c5f6e7643 | fit |  | 15.031375 | 35 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_a1c9b7f23a9835c6 | fit |  | 14.977125 | 35 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_f1d663fa7c7ee856 | fit |  | 14.29575 | 35 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_455b0803dae14507 | fit |  | 15.8985 | 35 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_f8158322e7498b6e | select |  | 12.609687 | 35 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_0c53212473df9528 | select |  | 16.4915 | 35 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_400fedc1f340ea52 | fit |  | 14.559938 | 35 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_ae9c86e3a267baca | fit |  | 13.501375 | 35 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_40cd21225a160d82 | select |  | 12.61275 | 35 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_32155b7c923d6013 | fit |  | 12.172625 | 35 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_132a81e2a6156def | select |  | 11.989313 | 35 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_1b72095996474a2e | fit |  | 12.308687 | 35 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_966e83c327fe875d | fit |  | 15.127313 | 35 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_ae96bd8de4fd10eb | select |  | 14.209375 | 35 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_dc044fe935eb5e6d | fit |  | 16.126438 | 35 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_a078b4c6b7c89273 | fit |  | 14.862875 | 35 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_2303e2f10aaa6056 | select |  | 9.383563 | 35 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_60cd2debd51dc497 | fit |  | 13.309 | 35 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_152b6a3e69c7615f | select |  | 16.357688 | 35 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_0b32c99c1e54c1be | fit |  | 13.747625 | 35 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_3145f5413d818605 | select |  | 11.809313 | 35 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_774f03ce6ae22a39 | select |  | 13.542375 | 35 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_37e3d4f342a2bd71 | select |  | 10.666813 | 35 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_7b1e8037ce279fa8 | fit |  | 11.901625 | 35 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_d0393a13659216c1 | fit |  | 13.861187 | 35 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_cdd28a56ad58716e | select |  | 13.58 | 35 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_d0f9212e38257341 | select |  | 11.11825 | 35 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_ba2f5e2f0043e26d | select |  | 17.618625 | 35 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_0eec263aec45abc3 | fit |  | 15.569 | 35 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_23beb0e36106b0e3 | fit |  | 19.79225 | 35 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_609a31bbe7d2a248 | select |  | 11.521688 | 35 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_c5041d8d215555b6 | select |  | 16.350438 | 35 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_5e37110dc9931bf4 | fit |  | 15.986688 | 35 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_3e0086f94a32db50 | fit |  | 17.1735 | 35 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_5d3e3c5e1a31a1ce | select |  | 14.581062 | 35 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_bc3cff742ea58aa4 | select |  | 13.114562 | 35 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_f5cb3865dbff7fc8 | select |  | 10.7485 | 35 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_77f11f8489a4f93e | select |  | 15.3315 | 35 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_efb3fe9fc22b479f | select |  | 14.60075 | 35 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_b32189f9321500b8 | select |  | 14.221 | 35 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_a59aa8a9380b7f4e | fit |  | 13.743125 | 35 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_2c80ed3b08c9c0f9 | fit |  | 17.984813 | 35 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_73298345d6e5daef | select |  | 12.261875 | 35 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_e9296d4c012caa18 | select |  | 14.816 | 35 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_88d9074029412629 | fit |  | 11.060438 | 35 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_90531f08706cfae2 | fit |  | 14.83925 | 35 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_aeea0da41523195c | fit |  | 11.481 | 35 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_0211d1d82056851c | select |  | 12.294562 | 35 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_e103294959166e16 | fit |  | 13.241375 | 35 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_cca5e882932a1f05 | fit |  | 13.396688 | 35 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_8595e2eb52b7df57 | select |  | 10.956 | 35 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_cd509bf2f6bfc308 | fit |  | 12.029813 | 35 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_4be80298957ba333 | fit |  | 11.664625 | 35 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_756af936514b28b0 | fit |  | 13.107188 | 35 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_0f1f308f5a686d3f | select |  | 13.139625 | 35 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_3609336fa24580e7 | fit |  | 13.7365 | 35 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_5acfbc56b9dd560f | select |  | 19.166875 | 47 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_9c1b3e26a5e4f57f | fit |  | 16.11975 | 47 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_54bebc695e054152 | fit |  | 19.2825 | 47 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_ffaa97ae18752a3f | fit |  | 21.1955 | 47 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_52011c3ef06c01aa | fit |  | 17.707812 | 47 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_c726b13eb874d5a6 | select |  | 17.733937 | 47 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_f140b20403f30479 | fit |  | 20.757125 | 47 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_a682d07157dbabb3 | select |  | 15.832375 | 47 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_f430c14f19367f09 | fit |  | 21.534813 | 47 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_736f8597ab066e65 | select |  | 22.080687 | 47 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_2cd903df81d682ae | select |  | 23.193875 | 47 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_355b5944dfd09f72 | fit |  | 18.533313 | 47 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_393b5d1cab5c76c4 | fit |  | 19.39225 | 47 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_85a2cdcba453c5bf | fit |  | 17.542375 | 47 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_3549f553dddfc440 | select |  | 19.166625 | 47 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_af5bb16461f7a510 | fit |  | 14.5635 | 47 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_01596350eabaf13f | fit |  | 15.091188 | 47 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_9866c0162308b3c4 | select |  | 16.501125 | 47 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_b693e67bbfffc75e | fit |  | 20.4 | 47 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_04e4ba6464675cc1 | fit |  | 17.123438 | 47 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_c9555ac0e063d8bb | select |  | 17.35525 | 47 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_924abe46d8f2ae7a | select |  | 19.656 | 47 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_d357727d81fa0016 | select |  | 14.969 | 47 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_3dbf0dd26773d7cb | select |  | 20.332438 | 47 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_3dc93f2226e758e9 | select |  | 15.0475 | 47 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_2dc341cd6900d220 | select |  | 14.028813 | 47 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_94ae9c69a58e3c1e | fit |  | 18.092625 | 47 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_761811cec74eff6d | fit |  | 23.0765 | 47 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_5e992cec85e0adbf | fit |  | 21.264312 | 47 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_e76f5563cd6102c9 | fit |  | 13.871625 | 47 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_4d81afbfc5b0881e | fit |  | 19.977125 | 47 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_ca83c739ac4d94c6 | fit |  | 15.903813 | 47 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_bc5fd08a35a61bac | fit |  | 14.849 | 47 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_4ee99415400f2a3a | select |  | 18.242062 | 47 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_a3a3a843eb3435de | select |  | 15.518625 | 47 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_c3fd120c0abd34ef | select |  | 16.149062 | 47 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_4bfb6741b2df846e | fit |  | 17.310063 | 47 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_4e14518c24ce8906 | select |  | 15.713188 | 47 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_9b25f00f6c395cc0 | fit |  | 16.473688 | 47 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_c1137f0cec6a777e | fit |  | 18.5685 | 47 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_272ab9d23ca52bb2 | select |  | 18.640187 | 47 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_3d942023cb8405d1 | fit |  | 19.31075 | 47 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_9c2f610de56cea34 | fit |  | 25.200813 | 47 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_23b55a56622e40fd | fit |  | 18.969313 | 47 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_fc2c804a2d61fdc5 | select |  | 20.1315 | 47 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_a5bccb915eecd1a7 | select |  | 22.820937 | 47 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_35580c5384c1265d | select |  | 17.234938 | 47 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_05a19c55474141b2 | select |  | 14.669063 | 47 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_4c7e51c420692732 | fit |  | 20.284 | 47 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_c4a762a55da96be1 | fit |  | 18.205313 | 47 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_cd9c737a9618649d | select |  | 18.611062 | 47 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_832a86e95b1eac68 | fit |  | 13.47425 | 47 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_726e79810adafd0d | fit |  | 18.46525 | 47 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_1cbc2ed6db0bb540 | fit |  | 18.450187 | 47 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_79080bf3eda7b7cd | select |  | 21.283812 | 47 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_b7d0724f9d280904 | select |  | 18.811937 | 47 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_7844c7e216df9ac8 | select |  | 20.333437 | 47 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_c3e587208aaad6c3 | fit |  | 16.921187 | 47 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_98c37d37d742d68b | select |  | 17.639063 | 47 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_bb01e78c2a3b6d9d | fit |  | 20.748313 | 47 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_367d11a8138f3f4c | select |  | 20.353813 | 47 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_f809c97cdc265df2 | fit |  | 19.503688 | 47 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_bb91a83535b42f2b | select |  | 18.180812 | 47 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_7bd6a125b2bd513e | select |  | 18.616688 | 47 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_a4ae31686fdb4e36 | select |  | 20.008625 | 47 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_08b5f8c46e762c79 | select |  | 18.979312 | 47 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_cfef43da3b48eeb5 | select |  | 20.631 | 47 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_34bf446f817139e9 | select |  | 21.453875 | 47 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_f279bdbe3cf2c558 | select |  | 19.554938 | 47 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_556b576fe562afb5 | fit |  | 14.246562 | 47 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_8ea27a2fca616d31 | fit |  | 17.435188 | 47 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_750d706754a128d8 | select |  | 16.036812 | 47 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_4474c7ab13377bc6 | select |  | 15.24025 | 47 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_a44abbe270d8c87d | fit |  | 17.979187 | 47 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_ead4f91557deaf75 | fit |  | 20.9895 | 47 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_b564905d7b0547a1 | fit |  | 19.998687 | 47 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_83cdf16b6096a08d | select |  | 23.17325 | 47 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_988113111aa80002 | select |  | 21.933688 | 47 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_159cf0087ed0eea0 | fit |  | 22.608187 | 47 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_1d2593d5e9fdfe35 | select |  | 15.679375 | 47 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_7e6b831241dda74c | select |  | 18.19525 | 47 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_410d19b1c0c2aa36 | fit |  | 14.395 | 47 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_f14a03d1e3827784 | fit |  | 25.226437 | 47 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_62833a86b0d61383 | select |  | 16.785688 | 47 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_2381fac097f61098 | select |  | 16.695812 | 47 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_acc1881caaa6edd7 | fit |  | 15.482625 | 47 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_d415a4ca2ebc0039 | fit |  | 16.917188 | 47 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_ba1e5681d792bcab | select |  | 15.012313 | 47 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_31cde4971109e340 | fit |  | 20.812687 | 47 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_17df8ebb5fa867a8 | select |  | 14.015875 | 47 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_8d0558ee5279f203 | fit |  | 17.61275 | 47 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_d31957da1f510f2f | fit |  | 14.324188 | 47 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_4744a5af15d748e8 | fit |  | 17.416187 | 47 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_f9a4170dcdced550 | fit |  | 19.795375 | 47 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_6db22eaa7c8508b2 | select |  | 15.661312 | 47 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_7f0b23ea82d7ce7e | select |  | 23.260125 | 47 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_bb4903de46c2b202 | select |  | 14.590875 | 47 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_32baffbf826ee10d | select |  | 22.396313 | 47 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_8a502a4b63c794f8 | select |  | 14.745688 | 47 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_f1f42555ec92d2c7 | fit |  | 18.462375 | 47 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_d0383c0b150756d3 | fit |  | 19.87775 | 47 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_394a851795430ca4 | select |  | 14.280437 | 47 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_b74b3cef7b0945e0 | fit |  | 18.66725 | 47 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_16a31c6f742ee28d | fit |  | 18.964 | 47 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_61edf89f01927abd | select |  | 18.067688 | 47 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_badd4e1ca330bff5 | select |  | 15.2425 | 47 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_6ea35b2cf6a733e8 | select |  | 14.001062 | 47 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_5ba912d112f3aa6b | select |  | 15.472563 | 57 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_19268171d488b55c | select |  | 20.49125 | 57 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_aa73224f14bf6526 | fit |  | 20.301813 | 57 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_343b8d9683b0b532 | fit |  | 24.2965 | 57 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_0074ce85a5fd8b06 | fit |  | 22.126875 | 57 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_4389afb8933321ae | fit |  | 14.93875 | 57 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_2d676ecc2c3fab65 | select |  | 23.398375 | 57 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_881b0befbb0e7564 | fit |  | 19.587812 | 57 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_4d194b799bbff6ba | select |  | 16.512625 | 57 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_e7b95b71119acd6a | select |  | 17.282062 | 57 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_a7bbeb1a23007440 | select |  | 22.619688 | 57 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_54c0a3de8ef27c20 | select |  | 18.178937 | 57 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_34367c64c4f81a86 | select |  | 16.897188 | 57 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_a12938547edf2898 | fit |  | 14.5175 | 57 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_86b5398daefe0c6c | fit |  | 17.350062 | 57 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_a3e1a021805b4d40 | fit |  | 19.2395 | 57 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_ff92bd6541f67a32 | select |  | 26.084625 | 57 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_031a33c60e90e4fb | select |  | 20.51275 | 57 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_2a450c4381f38f7b | fit |  | 21.136437 | 57 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_f79becb33e023ebe | fit |  | 14.417938 | 57 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_86e8ebc6890d5328 | fit |  | 22.882875 | 57 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_494453f52fbf2d81 | select |  | 18.409188 | 57 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_645e56dbf7ff06c4 | fit |  | 18.195625 | 57 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_ab3035e73a909375 | fit |  | 20.887812 | 57 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_345f846486f7817e | fit |  | 29.306625 | 57 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_7a54c0083407eba4 | fit |  | 15.35525 | 57 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_5d758aedde2431b6 | select |  | 22.5215 | 57 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_064acb01da28d690 | fit |  | 23.208188 | 57 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_cc4da6e433c547ff | select |  | 21.604563 | 57 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_f3bcbe8b8f6bf97d | select |  | 18.154312 | 57 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_00c06768106cd11f | select |  | 22.0785 | 57 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_f70957fefacc2649 | fit |  | 20.545 | 57 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_5df830718ca6de85 | select |  | 17.466125 | 57 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_0ece03e7b72e7a01 | fit |  | 20.058875 | 57 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_8e5ce93883f61a25 | select |  | 17.486875 | 57 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_17b2a4ce02f3cc26 | select |  | 16.572813 | 57 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_073ea69e777ff1b8 | select |  | 20.795375 | 57 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_15813df7ce5f952b | fit |  | 22.942812 | 57 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_29307c3530cbf052 | fit |  | 17.182688 | 57 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_9b128cac0db9ceaf | fit |  | 21.663062 | 57 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_c51a101b2c7b37bc | fit |  | 18.164813 | 57 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_6a2b67bad9ed1253 | select |  | 22.386312 | 57 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_bc3e5e79231f201c | select |  | 16.31975 | 57 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_43139bd63a10b018 | select |  | 23.777625 | 57 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_d06a071695df9e4b | select |  | 24.541125 | 57 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_91c75aa61777c59e | fit |  | 20.8985 | 57 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_3d0231830d3c86e0 | select |  | 23.25975 | 57 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_f50364432ff4d561 | fit |  | 19.683875 | 57 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_edc9a29357107cf6 | select |  | 24.047187 | 57 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_087de51376cac542 | fit |  | 28.021937 | 57 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_2febc1fa18d10fa8 | select |  | 27.680438 | 57 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_e7509abc81aa0fae | fit |  | 21.379125 | 57 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_16c157da49e70182 | fit |  | 22.481625 | 57 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_23d6ca2fd4717680 | fit |  | 21.617188 | 57 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_1c1e1af519d3de8a | select |  | 18.192937 | 57 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_b30f1981126a5486 | select |  | 23.0185 | 57 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_d117b86b7ecdcbbf | select |  | 20.484562 | 57 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_b40af6cf1a69003a | fit |  | 23.804063 | 57 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_712cd9d97ae754e1 | select |  | 25.39075 | 57 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_e80d55cf1fc24e4f | fit |  | 19.198375 | 57 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_d44bf5c045fb997b | select |  | 15.649125 | 57 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_3ef76c16a83fcccf | select |  | 21.691625 | 57 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_aaca5cad83bb038c | select |  | 22.945062 | 57 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_55e0841086aa89fa | fit |  | 22.80825 | 57 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_a511829464b52b25 | select |  | 16.761688 | 57 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_f50559b19055dd79 | select |  | 23.94775 | 57 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_77ebcc934a8b076b | select |  | 23.628375 | 57 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_07013ad535d0b845 | select |  | 18.958437 | 57 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_840fca8ed1502a40 | fit |  | 21.322 | 57 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_8fc4e7e3756a1cb9 | select |  | 22.776125 | 57 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_208d84069f75b3f3 | fit |  | 21.946313 | 57 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_8a178422fdd2fe23 | fit |  | 23.518062 | 57 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_c4e6c7197f062007 | select |  | 19.294875 | 57 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_70b3ca0529e48754 | fit |  | 20.893937 | 57 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_6b52337425ee020c | fit |  | 27.340375 | 57 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_de8c0d3e85ef897b | fit |  | 22.21025 | 57 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_6910e8d2d3d20516 | select |  | 19.95275 | 57 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_f7dd9e493575ee81 | select |  | 22.089688 | 57 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_15c74d965cd356e1 | select |  | 15.235 | 57 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_e412ba9c7f303fd0 | select |  | 33.627938 | 57 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_4374cee6adaee7f4 | fit |  | 19.195187 | 57 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_7c0f8aa4c655a6aa | fit |  | 24.944125 | 57 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_3f7482d0094f1bfa | select |  | 22.769 | 57 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_f189953467182a49 | fit |  | 17.428375 | 57 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_a8f357247242368e | select |  | 16.633063 | 57 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_606eead5af756aee | select |  | 16.648187 | 57 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_f374d19a4ad9fc2e | fit |  | 18.762313 | 57 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_ac921fcecc98f93d | fit |  | 22.201187 | 57 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_3f5057931acabb76 | fit |  | 21.401125 | 57 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_82679f694fc4dffd | fit |  | 20.664437 | 57 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_a075d8d42da6f975 | select |  | 20.090062 | 57 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_9cacc8bb2850104b | select |  | 15.75925 | 57 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_be0ff484994ac776 | select |  | 19.817937 | 57 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_08637188a65f9dc3 | fit |  | 19.300687 | 57 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_2836e2f36309046d | select |  | 18.029125 | 57 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_53e8aeba9a928292 | fit |  | 24.735875 | 57 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_9917a9fefd5e2889 | fit |  | 23.777875 | 57 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_0ef03657b70bed6c | select |  | 20.589813 | 57 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_fa8ddb0f4cf1d33e | fit |  | 19.522875 | 57 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_bdba711c4b7317e8 | select |  | 16.976937 | 57 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_bb6d7b1bb20fcaea | fit |  | 21.6605 | 57 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_d2d305682c092cf5 | fit |  | 24.2435 | 57 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_467dd37e3a16877e | select |  | 17.407312 | 57 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_e30728cfc721782c | fit |  | 16.126687 | 57 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_c8acb3e0ab55f30e | fit |  | 17.065625 | 57 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_9b414089687f50e9 | select |  | 19.945937 | 57 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_b909a7dfe8990fd5 | fit |  | 23.157937 | 57 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_37fd3ae3c219465c | fit |  | 18.283438 | 45 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_dad9b83d0a63bea6 | fit |  | 15.14475 | 45 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_581adeb76b084adb | select |  | 16.894063 | 45 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_5a45abdb67caa4dd | fit |  | 16.909375 | 45 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_ee0157e8b79b1a6c | select |  | 14.453125 | 45 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_726702d203f86569 | select |  | 20.476625 | 45 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_e9715a1a5d0fd3c5 | fit |  | 25.000688 | 45 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_1d80daafa6601a6f | select |  | 14.447688 | 45 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_7d33aa7cc16ec60b | select |  | 13.258 | 45 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_e0740d90294a9efe | fit |  | 14.2155 | 45 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_b74fb3a039f4c423 | select |  | 14.22425 | 45 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_a347ddedbcf152bc | fit |  | 15.131125 | 45 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_c9172e3901588f77 | fit |  | 19.816375 | 45 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_018a61b4aa63f87c | select |  | 18.039875 | 45 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_2818949a1980cc0f | select |  | 14.824375 | 45 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_4ec9b4feb639e087 | fit |  | 12.075688 | 45 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_3c5715b8d9c15899 | select |  | 15.52 | 45 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_8e650411728153a9 | fit |  | 15.523813 | 45 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_bcb919a2c6b283e9 | select |  | 17.465812 | 45 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_7fd0e9fbd972cfa2 | select |  | 20.7095 | 45 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_d9fbca3b1f2c482d | fit |  | 14.287125 | 45 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_2deab6c3ab7d505d | fit |  | 16.374625 | 45 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_2cc73f4ffa30938e | select |  | 16.81925 | 45 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_6a682d3b7a4a49ec | select |  | 17.017375 | 45 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_f97ceaefb5403dd3 | select |  | 16.992625 | 45 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_a7473ee1d98527ad | fit |  | 16.457687 | 45 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_38e49644a392697f | fit |  | 18.501625 | 45 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_91113ca63326decf | select |  | 20.013125 | 45 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_5a581d5fb36476ed | select |  | 17.22575 | 45 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_ed0dccf37cc0cf4d | select |  | 17.057813 | 45 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_ca39c7d27a7126c6 | select |  | 16.389688 | 45 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_9285b680f38a4fc0 | fit |  | 17.707125 | 45 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_6a97b1418223f691 | fit |  | 19.922375 | 45 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_ae6192a92ee52103 | fit |  | 13.560375 | 45 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_b14dde4e68596226 | select |  | 18.680812 | 45 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_611c6cc3cba739da | select |  | 18.213062 | 45 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_e89427b998f10159 | fit |  | 17.5465 | 45 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_0b36c1045d1da0fb | fit |  | 16.204937 | 45 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_4f5de355c0635ccd | fit |  | 26.155062 | 45 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_81c044dc8bb38a08 | select |  | 19.04 | 45 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_fcf0d9b9490e46e4 | fit |  | 16.50075 | 45 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_af4277a12d388207 | fit |  | 17.2685 | 45 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_eb5916614a9e98d1 | select |  | 14.383625 | 45 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_b4161ca919dd35b4 | fit |  | 19.690875 | 45 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_f408e248e9839d14 | fit |  | 14.161375 | 45 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_ac71bc2d8b9b93bb | fit |  | 18.147375 | 45 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_af69f34669c29022 | fit |  | 19.027812 | 45 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_7ab48ab9a57b8f6a | fit |  | 19.539625 | 45 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_988a3844090fd149 | select |  | 14.491188 | 45 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_848ec88010b6837b | select |  | 17.85325 | 45 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_008631fd8d2bfa4e | select |  | 19.0845 | 45 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_4198aa78eca2e274 | fit |  | 16.570625 | 45 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_633b64bfee977113 | fit |  | 20.121938 | 45 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_eded005950ca6b96 | fit |  | 17.087125 | 45 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_a2e085e998dace10 | select |  | 18.341812 | 45 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_74134c98dc35ede3 | fit |  | 17.437812 | 45 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_c8121b6a03260cec | fit |  | 15.065938 | 45 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_0bd464ff6bb7a5a9 | fit |  | 18.889125 | 45 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_641a323e09d7cf47 | select |  | 16.0035 | 45 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_c3179870d9305586 | fit |  | 17.059313 | 45 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_3fa2c559fd1674b9 | select |  | 13.100437 | 45 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_700796e231ebd708 | fit |  | 14.188562 | 45 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_3be60bbf06e5ce25 | select |  | 14.820438 | 45 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_9ce010dfc0c3af5a | select |  | 19.867687 | 45 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_ca48636d8c95423f | select |  | 16.14475 | 45 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_0077059313fa4d62 | fit |  | 17.346312 | 45 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_d3d58683b0125448 | fit |  | 18.019313 | 45 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_279b785a6596bb42 | select |  | 12.934688 | 45 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_5cf45b157aa3e7a2 | fit |  | 17.442312 | 45 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_a5603998c9f9374b | fit |  | 17.326875 | 45 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_f414bce78afa90fa | select |  | 14.768187 | 45 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_71a8c8dd68c1cf88 | fit |  | 17.772125 | 45 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_5164cfdad88b5eec | select |  | 20.53125 | 45 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_e4fa933e73fccef2 | fit |  | 18.122312 | 45 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_42d358cabf601491 | select |  | 14.832562 | 45 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_d01c1544bb9267e7 | select |  | 12.947625 | 45 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_49b5076173395a56 | select |  | 17.243375 | 45 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_52bdca07b431a2ea | select |  | 17.13325 | 45 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_659c8288352c7cdb | select |  | 19.131875 | 45 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_ef54b5c5bb2301ed | select |  | 13.508875 | 45 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_508a35a536ebc3c2 | select |  | 15.270563 | 45 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_5fb5efa16859544d | select |  | 20.043187 | 45 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_e8b99de48b350024 | select |  | 17.906875 | 45 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_bc28805a1a2b84b0 | fit |  | 20.878937 | 45 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_ed9325f119e96d68 | fit |  | 17.816188 | 45 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_79b7e37cce115ae4 | fit |  | 18.5865 | 45 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_8f272dcf523bca16 | select |  | 15.161437 | 45 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_26e06bb0fbaa83f8 | select |  | 13.553688 | 45 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_6c1a625d822e0fa0 | fit |  | 15.228 | 45 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_131f542167f0c4b4 | select |  | 17.476063 | 45 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_4d581ab62efb5254 | fit |  | 18.080562 | 45 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_1969c1a545a36019 | fit |  | 17.043563 | 45 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_afcea94b17c1b8b4 | select |  | 15.8935 | 45 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_09551aabcf6486dd | fit |  | 19.2615 | 45 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_aed200921a6f8ec5 | select |  | 13.675688 | 45 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_87a45399108117dd | select |  | 14.693062 | 45 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_72c1d73359c347c1 | select |  | 14.668938 | 45 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_5718aaa08209c83f | fit |  | 14.242125 | 45 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_aac895c4c4d42903 | fit |  | 18.458188 | 45 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_7895471d57ff4aec | fit |  | 16.151312 | 45 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_b946bc0c40eeb37e | fit |  | 17.69775 | 45 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_932abefbd80c1305 | select |  | 13.844812 | 45 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_94a5230d89a7c656 | select |  | 15.865 | 45 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_89d600c8bd063b2e | select |  | 19.796937 | 45 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_e6e0c616ed96e8bb | fit |  | 26.557875 | 45 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_f844f592b6aef7e8 | fit |  | 17.046688 | 45 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_3739e40dcb7a63f7 | select |  | 13.01075 | 45 | CC BY-NC 4.0 | https://creativecommons.org/licenses/by-nc/4.0/ |
| null_project_lv_gettysburg150_dj | select |  | 100.64 | 272 | LibriVox voluntary public-domain dedication in the USA; historical source text is public domain. Inspect linked item metadata for its mark; missing metadata is not evidence of a mark. | https://archive.org/details/gettysburgaddress_150anniv_1311_librivox |
| null_1dbb63ebeaeb3ad2 | fit |  | 124.7 | 272 | Public domain (item-specific mark/dedication) | http://creativecommons.org/licenses/publicdomain/ |
| null_project_lv_gettysburg150_amb | select |  | 106.64 | 272 | LibriVox voluntary public-domain dedication in the USA; historical source text is public domain. Inspect linked item metadata for its mark; missing metadata is not evidence of a mark. | https://archive.org/details/gettysburgaddress_150anniv_1311_librivox |
| null_633657385e2b428d | fit |  | 122.58 | 272 | Public domain (item-specific mark/dedication) | http://creativecommons.org/publicdomain/mark/1.0/ |
| null_a1df70b2b8131fc6 | fit |  | 106.94 | 272 | Public domain (item-specific mark/dedication) | http://creativecommons.org/licenses/publicdomain/ |
| null_project_lv_gettysburg150_pc | select |  | 118.08 | 272 | LibriVox voluntary public-domain dedication in the USA; historical source text is public domain. Inspect linked item metadata for its mark; missing metadata is not evidence of a mark. | https://archive.org/details/gettysburgaddress_150anniv_1311_librivox |
| null_cb9bc2e62348e5e6 | fit |  | 146.22 | 272 | Public domain (item-specific mark/dedication) | http://creativecommons.org/publicdomain/mark/1.0/ |
| null_0e0c21ccb971ce62 | fit |  | 114.56 | 272 | Public domain (item-specific mark/dedication) | http://creativecommons.org/licenses/publicdomain/ |
| null_00e4f8b8aaf80cf5 | fit |  | 118.06 | 272 | Public domain (item-specific mark/dedication) | http://creativecommons.org/publicdomain/mark/1.0/ |
| null_project_lv_gettysburg150_wt | select |  | 131.0 | 272 | LibriVox voluntary public-domain dedication in the USA; historical source text is public domain. Inspect linked item metadata for its mark; missing metadata is not evidence of a mark. | https://archive.org/details/gettysburgaddress_150anniv_1311_librivox |
| null_project_lv_gettysburg150_fb | select |  | 113.62 | 272 | LibriVox voluntary public-domain dedication in the USA; historical source text is public domain. Inspect linked item metadata for its mark; missing metadata is not evidence of a mark. | https://archive.org/details/gettysburgaddress_150anniv_1311_librivox |
| null_8085cc9a68da99f3 | fit |  | 195.46 | 272 | Public domain (item-specific mark/dedication) | http://creativecommons.org/publicdomain/mark/1.0/ |
| null_project_lv_gettysburg150_jn | select |  | 106.9 | 272 | LibriVox voluntary public-domain dedication in the USA; historical source text is public domain. Inspect linked item metadata for its mark; missing metadata is not evidence of a mark. | https://archive.org/details/gettysburgaddress_150anniv_1311_librivox |
| null_project_lv_gettysburg150_sa | select |  | 136.04 | 272 | LibriVox voluntary public-domain dedication in the USA; historical source text is public domain. Inspect linked item metadata for its mark; missing metadata is not evidence of a mark. | https://archive.org/details/gettysburgaddress_150anniv_1311_librivox |
| null_7de61cd652cd55f1 | fit |  | 145.62 | 272 | Public domain (item-specific mark/dedication) | http://creativecommons.org/publicdomain/mark/1.0/ |
| null_project_lv_gettysburg150_dl | select |  | 118.8 | 272 | LibriVox voluntary public-domain dedication in the USA; historical source text is public domain. Inspect linked item metadata for its mark; missing metadata is not evidence of a mark. | https://archive.org/details/gettysburgaddress_150anniv_1311_librivox |
| null_4298c1b1312a7b08 | fit |  | 103.48 | 272 | Public domain (item-specific mark/dedication) | http://creativecommons.org/publicdomain/mark/1.0/ |
| null_58be62b23ac1a914 | fit |  | 83.42 | 272 | Public domain (item-specific mark/dedication) | http://creativecommons.org/licenses/publicdomain/ |
| null_project_lv_gettysburg150_tg | select |  | 104.12 | 272 | LibriVox voluntary public-domain dedication in the USA; historical source text is public domain. Inspect linked item metadata for its mark; missing metadata is not evidence of a mark. | https://archive.org/details/gettysburgaddress_150anniv_1311_librivox |
| null_cc1c8f2d5fd870f8 | fit |  | 34.74 | 71 | Public domain (item-specific mark/dedication) | http://creativecommons.org/publicdomain/zero/1.0/ |
| null_ae564ef4752245dc | fit |  | 33.38 | 71 | Public domain (item-specific mark/dedication) | http://creativecommons.org/publicdomain/zero/1.0/ |
| null_286681f4fd60a2cb | select |  | 39.32 | 71 | Public domain (item-specific mark/dedication) | http://creativecommons.org/publicdomain/zero/1.0/ |
| null_b1767d1c64a5ac6f | select |  | 35.64 | 71 | Public domain (item-specific mark/dedication) | http://creativecommons.org/publicdomain/zero/1.0/ |
| null_c66c329ea49c96c7 | lockbox |  | 51.112563 | 71 | Public domain (item-specific mark/dedication) | http://creativecommons.org/publicdomain/zero/1.0/ |
| null_1c00b70860f0e969 | select |  | 31.9 | 71 | Public domain (item-specific mark/dedication) | http://creativecommons.org/publicdomain/zero/1.0/ |
| null_7a312234a78e44d9 | fit |  | 40.2 | 71 | Public domain (item-specific mark/dedication) | http://creativecommons.org/publicdomain/zero/1.0/ |
| null_9ec3e3ab0abd438d | fit |  | 37.6 | 71 | Public domain (item-specific mark/dedication) | http://creativecommons.org/publicdomain/zero/1.0/ |
| null_1b9b10c74e5e8bb2 | fit |  | 44.4 | 71 | Public domain (item-specific mark/dedication) | http://creativecommons.org/publicdomain/zero/1.0/ |
| null_ac6ce1a5cbe5f1d8 | fit |  | 38.64 | 71 | Public domain (item-specific mark/dedication) | http://creativecommons.org/publicdomain/zero/1.0/ |
| null_5314ef3d9ad2c6ac | lockbox |  | 46.419625 | 71 | Public domain (item-specific mark/dedication) | http://creativecommons.org/publicdomain/zero/1.0/ |
| null_1bc3efb7721698f3 | lockbox |  | 54.090875 | 71 | Public domain (item-specific mark/dedication) | http://creativecommons.org/publicdomain/zero/1.0/ |
| null_704d21fbd70ce4d1 | fit |  | 38.02 | 71 | Public domain (item-specific mark/dedication) | http://creativecommons.org/publicdomain/zero/1.0/ |
| null_4eee7bc3b9995fc2 | fit |  | 36.58 | 71 | Public domain (item-specific mark/dedication) | http://creativecommons.org/publicdomain/zero/1.0/ |
| null_afaacfb95c66e410 | select |  | 57.1 | 151 | Public domain (item-specific mark/dedication) | http://creativecommons.org/publicdomain/zero/1.0/ |
| null_107abf6bd39355af | fit |  | 64.22 | 151 | Public domain (item-specific mark/dedication) | http://creativecommons.org/publicdomain/zero/1.0/ |
| null_6be1379cccd125cb | fit |  | 74.82 | 151 | Public domain (item-specific mark/dedication) | http://creativecommons.org/publicdomain/zero/1.0/ |
| null_22e36a459912d47b | select |  | 64.16 | 151 | Public domain (item-specific mark/dedication) | http://creativecommons.org/publicdomain/zero/1.0/ |
| null_3bbd7ddfbe3965d8 | select |  | 61.88 | 151 | Public domain (item-specific mark/dedication) | http://creativecommons.org/publicdomain/zero/1.0/ |
| null_3d8fd74426662911 | fit |  | 63.08 | 151 | Public domain (item-specific mark/dedication) | http://creativecommons.org/publicdomain/zero/1.0/ |
| null_3480b3c5ccff74b7 | select |  | 64.54 | 151 | Public domain (item-specific mark/dedication) | http://creativecommons.org/publicdomain/zero/1.0/ |
| null_29fc92786158f343 | fit |  | 77.9 | 151 | Public domain (item-specific mark/dedication) | http://creativecommons.org/publicdomain/zero/1.0/ |
| null_cc1b889ed6823e74 | fit |  | 63.34 | 151 | Public domain (item-specific mark/dedication) | http://creativecommons.org/publicdomain/zero/1.0/ |
| null_363c684ae2638207 | fit |  | 66.92 | 151 | Public domain (item-specific mark/dedication) | http://creativecommons.org/publicdomain/zero/1.0/ |
| null_ead2f7d9c33aecce | fit |  | 73.9 | 151 | Public domain (item-specific mark/dedication) | http://creativecommons.org/publicdomain/zero/1.0/ |
| null_2af416944a87f925 | fit |  | 68.66 | 151 | Public domain (item-specific mark/dedication) | http://creativecommons.org/publicdomain/zero/1.0/ |
| null_2cfebdaa2686fbf2 | select |  | 60.34 | 151 | Public domain (item-specific mark/dedication) | http://creativecommons.org/publicdomain/zero/1.0/ |
| null_c2ae943ae1bb5f1a | fit |  | 120.52 | 231 | Public domain (item-specific mark/dedication) | http://creativecommons.org/publicdomain/mark/1.0/ |
| null_ee0ac949fae09999 | fit |  | 114.36 | 231 | Public domain (item-specific mark/dedication) | http://creativecommons.org/publicdomain/mark/1.0/ |
| null_9c36ac530c653452 | fit |  | 85.16 | 231 | Public domain (item-specific mark/dedication) | http://creativecommons.org/publicdomain/mark/1.0/ |
| null_cab602cc099dd20d | fit |  | 104.18 | 231 | Public domain (item-specific mark/dedication) | http://creativecommons.org/publicdomain/mark/1.0/ |
| null_df87b09002f877d7 | fit |  | 125.08 | 231 | Public domain (item-specific mark/dedication) | http://creativecommons.org/publicdomain/mark/1.0/ |
| null_fa147ffdb17349fd | select |  | 100.5 | 231 | Public domain (item-specific mark/dedication) | http://creativecommons.org/publicdomain/mark/1.0/ |
| null_d3fc84faa955325b | select |  | 79.5 | 231 | Public domain (item-specific mark/dedication) | http://creativecommons.org/publicdomain/mark/1.0/ |
| null_cb6c09e63987da8a | fit |  | 116.76 | 231 | Public domain (item-specific mark/dedication) | http://creativecommons.org/publicdomain/mark/1.0/ |
| null_5e8275232c0d22f4 | fit |  | 79.26 | 231 | Public domain (item-specific mark/dedication) | http://creativecommons.org/publicdomain/mark/1.0/ |
| null_f125e0dae5c2cebf | fit |  | 88.14 | 231 | Public domain (item-specific mark/dedication) | http://creativecommons.org/publicdomain/mark/1.0/ |
| null_58c33a7d39405844 | fit |  | 101.74 | 231 | Public domain (item-specific mark/dedication) | http://creativecommons.org/publicdomain/mark/1.0/ |
| null_b446d7de48ec8882 | lockbox |  | 48.014562 | 46 | Public domain (item-specific mark/dedication) | http://creativecommons.org/publicdomain/zero/1.0/ |
| null_5c9505ab5caa31c5 | lockbox |  | 38.656937 | 46 | Public domain (item-specific mark/dedication) | http://creativecommons.org/publicdomain/zero/1.0/ |
| null_9fd149beaa124ab0 | lockbox |  | 48.285938 | 46 | Public domain (item-specific mark/dedication) | http://creativecommons.org/publicdomain/zero/1.0/ |
| null_e331c753f847ac05 | lockbox |  | 44.953812 | 46 | Public domain (item-specific mark/dedication) | http://creativecommons.org/publicdomain/zero/1.0/ |
| null_ec0cb746319ed298 | lockbox |  | 49.475938 | 46 | Public domain (item-specific mark/dedication) | http://creativecommons.org/publicdomain/zero/1.0/ |
| null_457936e844b19740 | lockbox |  | 44.987125 | 46 | Public domain (item-specific mark/dedication) | http://creativecommons.org/publicdomain/zero/1.0/ |
| null_7b2753bd775a1b73 | fit |  | 104.18 | 179 | Public domain (item-specific mark/dedication) | http://creativecommons.org/publicdomain/zero/1.0/ |
| null_26fb9c30ef61946e | select |  | 89.7 | 179 | Public domain (item-specific mark/dedication) | http://creativecommons.org/publicdomain/zero/1.0/ |
| null_5ee5b3a9157ca8b1 | select |  | 105.22 | 179 | Public domain (item-specific mark/dedication) | http://creativecommons.org/publicdomain/zero/1.0/ |
| null_554cc6336f5b6991 | select |  | 84.24 | 179 | Public domain (item-specific mark/dedication) | http://creativecommons.org/publicdomain/zero/1.0/ |
| null_1f4562c04493dc0b | lockbox |  | 104.280812 | 179 | Public domain (item-specific mark/dedication) | http://creativecommons.org/publicdomain/zero/1.0/ |
| null_d758889ddc33571e | lockbox |  | 103.131438 | 179 | Public domain (item-specific mark/dedication) | http://creativecommons.org/publicdomain/zero/1.0/ |
| null_475c1eb0876561a3 | fit |  | 104.02 | 179 | Public domain (item-specific mark/dedication) | http://creativecommons.org/publicdomain/zero/1.0/ |
| null_0e3298f767088ad4 | fit |  | 86.22 | 179 | Public domain (item-specific mark/dedication) | http://creativecommons.org/publicdomain/zero/1.0/ |
| null_bfd634741ad2a658 | lockbox |  | 120.4245 | 179 | Public domain (item-specific mark/dedication) | http://creativecommons.org/publicdomain/zero/1.0/ |
| null_e6dc1ed45e904826 | fit |  | 93.38 | 179 | Public domain (item-specific mark/dedication) | http://creativecommons.org/publicdomain/zero/1.0/ |
| null_fc0bc6fc437f05c5 | fit |  | 83.02 | 179 | Public domain (item-specific mark/dedication) | http://creativecommons.org/publicdomain/zero/1.0/ |
| null_2acaddb02fd4ac3a | select |  | 97.6 | 179 | Public domain (item-specific mark/dedication) | http://creativecommons.org/publicdomain/zero/1.0/ |
| null_f0d7da892155385e | lockbox |  | 135.653875 | 179 | Public domain (item-specific mark/dedication) | http://creativecommons.org/publicdomain/zero/1.0/ |
| null_1617cb7e24e80059 | fit |  | 94.74 | 179 | Public domain (item-specific mark/dedication) | http://creativecommons.org/publicdomain/zero/1.0/ |
| null_1ef11262a4767a2d | fit |  | 80.26 | 179 | Public domain (item-specific mark/dedication) | http://creativecommons.org/publicdomain/zero/1.0/ |
| null_cdf1719d181c7a9c | lockbox |  | 95.425313 | 179 | Public domain (item-specific mark/dedication) | http://creativecommons.org/publicdomain/zero/1.0/ |
| null_de99cf42822505ea | lockbox |  | 109.818813 | 179 | Public domain (item-specific mark/dedication) | http://creativecommons.org/publicdomain/zero/1.0/ |
| null_34b9201d64b76f1a | lockbox |  | 96.391875 | 179 | Public domain (item-specific mark/dedication) | http://creativecommons.org/publicdomain/zero/1.0/ |
| null_554deaa967c9970e | select |  | 73.38 | 135 | Public domain (item-specific mark/dedication) | http://creativecommons.org/publicdomain/mark/1.0/ |
| null_669abd614785a1d7 | select |  | 65.72 | 135 | Public domain (item-specific mark/dedication) | http://creativecommons.org/publicdomain/mark/1.0/ |
| null_ab8b49453bd92efb | select |  | 59.32 | 135 | Public domain (item-specific mark/dedication) | http://creativecommons.org/publicdomain/mark/1.0/ |
| null_3e02a2ad4a998015 | fit |  | 62.08 | 135 | Public domain (item-specific mark/dedication) | http://creativecommons.org/publicdomain/mark/1.0/ |
| null_afb88e33fe33854b | select |  | 63.02 | 135 | Public domain (item-specific mark/dedication) | http://creativecommons.org/publicdomain/mark/1.0/ |
| null_4f9568f2b1a284ef | fit |  | 66.16 | 135 | Public domain (item-specific mark/dedication) | http://creativecommons.org/publicdomain/mark/1.0/ |
| null_d273e9b93d89334e | fit |  | 58.56 | 135 | Public domain (item-specific mark/dedication) | http://creativecommons.org/publicdomain/mark/1.0/ |
| null_e0bd6aa800fb1c1f | fit |  | 76.82 | 135 | Public domain (item-specific mark/dedication) | http://creativecommons.org/publicdomain/mark/1.0/ |
| null_7e00ed2054782ec2 | fit |  | 73.6 | 135 | Public domain (item-specific mark/dedication) | http://creativecommons.org/publicdomain/mark/1.0/ |
| null_f23c288c57306513 | fit |  | 76.48 | 135 | Public domain (item-specific mark/dedication) | http://creativecommons.org/publicdomain/mark/1.0/ |
| null_4d780ddae305dda9 | fit |  | 64.6 | 135 | Public domain (item-specific mark/dedication) | http://creativecommons.org/publicdomain/mark/1.0/ |
| null_17ad6ec1f07f6e7f | select |  | 58.14 | 135 | Public domain (item-specific mark/dedication) | http://creativecommons.org/publicdomain/mark/1.0/ |
| null_0491c2a822c824a3 | fit |  | 78.76 | 135 | Public domain (item-specific mark/dedication) | http://creativecommons.org/publicdomain/mark/1.0/ |
| null_3c217959fa9a5ba1 | fit |  | 65.4 | 135 | Public domain (item-specific mark/dedication) | http://creativecommons.org/publicdomain/mark/1.0/ |
| null_50d33cf3fff5efd0 | fit |  | 67.02 | 135 | Public domain (item-specific mark/dedication) | http://creativecommons.org/publicdomain/mark/1.0/ |
| null_8a48cea18294fd55 | fit |  | 54.56 | 120 | Public domain (item-specific mark/dedication) | http://creativecommons.org/publicdomain/zero/1.0/ |
| null_e7915123bf498969 | fit |  | 64.52 | 120 | Public domain (item-specific mark/dedication) | http://creativecommons.org/publicdomain/zero/1.0/ |
| null_5d2d30d6940f393b | lockbox |  | 77.01375 | 120 | Public domain (item-specific mark/dedication) | http://creativecommons.org/publicdomain/zero/1.0/ |
| null_63ad7078c5b3e310 | select |  | 49.54 | 120 | Public domain (item-specific mark/dedication) | http://creativecommons.org/publicdomain/zero/1.0/ |
| null_7d1ef57a88c6cd11 | fit |  | 66.38 | 120 | Public domain (item-specific mark/dedication) | http://creativecommons.org/publicdomain/zero/1.0/ |
| null_a72dfb6b7eb81902 | fit |  | 51.14 | 120 | Public domain (item-specific mark/dedication) | http://creativecommons.org/publicdomain/zero/1.0/ |
| null_08bcebbd31dd06dc | fit |  | 46.5 | 120 | Public domain (item-specific mark/dedication) | http://creativecommons.org/publicdomain/zero/1.0/ |
| null_7a21d6e1d942b886 | select |  | 48.78 | 120 | Public domain (item-specific mark/dedication) | http://creativecommons.org/publicdomain/zero/1.0/ |
| null_42b7fad7558c247c | select |  | 61.02 | 120 | Public domain (item-specific mark/dedication) | http://creativecommons.org/publicdomain/zero/1.0/ |
| null_38acffbd1447e859 | fit |  | 54.84 | 120 | Public domain (item-specific mark/dedication) | http://creativecommons.org/publicdomain/zero/1.0/ |
| null_edd3d86cb288593b | fit |  | 89.02 | 182 | Public domain (item-specific mark/dedication) | http://creativecommons.org/publicdomain/zero/1.0/ |
| null_a2935e9f5d0d2c64 | fit |  | 77.52 | 182 | Public domain (item-specific mark/dedication) | http://creativecommons.org/publicdomain/zero/1.0/ |
| null_b499622c78324cb1 | fit |  | 80.7 | 182 | Public domain (item-specific mark/dedication) | http://creativecommons.org/publicdomain/zero/1.0/ |
| null_5da248520aa01d3a | fit |  | 71.5 | 182 | Public domain (item-specific mark/dedication) | http://creativecommons.org/publicdomain/zero/1.0/ |
| null_9c264f5072b3365d | lockbox |  | 142.653188 | 182 | Public domain (item-specific mark/dedication) | http://creativecommons.org/publicdomain/zero/1.0/ |
| null_b48ff0d6e8b79707 | lockbox |  | 109.033687 | 182 | Public domain (item-specific mark/dedication) | http://creativecommons.org/publicdomain/zero/1.0/ |
| null_fa31db1b5ed87bef | lockbox |  | 117.776562 | 182 | Public domain (item-specific mark/dedication) | http://creativecommons.org/publicdomain/zero/1.0/ |
| null_ae63ece71750bb1f | fit |  | 86.24 | 182 | Public domain (item-specific mark/dedication) | http://creativecommons.org/publicdomain/zero/1.0/ |
| null_27f72e8ceb4a9cd6 | fit |  | 79.1 | 182 | Public domain (item-specific mark/dedication) | http://creativecommons.org/publicdomain/zero/1.0/ |
| null_ed1fb9ae0228a099 | select |  | 66.9 | 182 | Public domain (item-specific mark/dedication) | http://creativecommons.org/publicdomain/zero/1.0/ |
| null_d40b02ec3fc8a809 | lockbox |  | 109.92325 | 182 | Public domain (item-specific mark/dedication) | http://creativecommons.org/publicdomain/zero/1.0/ |
| null_881feaea25f8bbd7 | fit |  | 99.88 | 182 | Public domain (item-specific mark/dedication) | http://creativecommons.org/publicdomain/zero/1.0/ |
| null_d92350c656603c5d | lockbox |  | 70.086562 | 182 | Public domain (item-specific mark/dedication) | http://creativecommons.org/publicdomain/zero/1.0/ |
| null_ff9f085b12706be2 | fit |  | 10.02 | 19 | Public domain (item-specific mark/dedication) | http://creativecommons.org/licenses/publicdomain/ |
| null_18e5acf497e3d247 | select |  | 15.46 | 19 | Public domain (item-specific mark/dedication) | http://creativecommons.org/licenses/publicdomain/ |
| null_3f224dff77c84983 | select |  | 6.18 | 19 | Public domain (item-specific mark/dedication) | http://creativecommons.org/licenses/publicdomain/ |
| null_432116e6d791f4db | select |  | 8.3 | 19 | Public domain (item-specific mark/dedication) | http://creativecommons.org/licenses/publicdomain/ |
| null_e84af0052392816e | select |  | 10.56 | 19 | Public domain (item-specific mark/dedication) | http://creativecommons.org/licenses/publicdomain/ |
| null_0961b8b4ad605d68 | lockbox |  | 23.693062 | 19 | Public domain (item-specific mark/dedication) | http://creativecommons.org/licenses/publicdomain/ |
| null_8d2a7b9d7916491b | fit |  | 8.04 | 19 | Public domain (item-specific mark/dedication) | http://creativecommons.org/licenses/publicdomain/ |
| null_593b184c4cf81a01 | fit |  | 6.08 | 19 | Public domain (item-specific mark/dedication) | http://creativecommons.org/licenses/publicdomain/ |
| null_b180548664d04e38 | lockbox |  | 23.379625 | 19 | Public domain (item-specific mark/dedication) | http://creativecommons.org/licenses/publicdomain/ |
| null_b036d60e43d3f096 | lockbox |  | 27.350188 | 19 | Public domain (item-specific mark/dedication) | http://creativecommons.org/licenses/publicdomain/ |
| null_4984070cf7a2b19b | fit |  | 7.16 | 19 | Public domain (item-specific mark/dedication) | http://creativecommons.org/licenses/publicdomain/ |
| null_176e51a2bd38d64d | lockbox |  | 28.342875 | 19 | Public domain (item-specific mark/dedication) | http://creativecommons.org/licenses/publicdomain/ |
| null_a8782ae08c1d4e97 | lockbox |  | 20.088188 | 19 | Public domain (item-specific mark/dedication) | http://creativecommons.org/licenses/publicdomain/ |
| null_c2bb01c4ea323888 | fit |  | 9.36 | 19 | Public domain (item-specific mark/dedication) | http://creativecommons.org/licenses/publicdomain/ |
| null_4a66c956dfe025ae | fit |  | 9.14 | 19 | Public domain (item-specific mark/dedication) | http://creativecommons.org/licenses/publicdomain/ |
| null_7477f43b54305af9 | select |  | 6.74 | 19 | Public domain (item-specific mark/dedication) | http://creativecommons.org/licenses/publicdomain/ |
| null_2d28f3a958a09bf0 | fit |  | 8.52 | 19 | Public domain (item-specific mark/dedication) | http://creativecommons.org/licenses/publicdomain/ |
| null_0cf5a64d092e14e6 | fit |  | 7.22 | 19 | Public domain (item-specific mark/dedication) | http://creativecommons.org/licenses/publicdomain/ |
| null_70f34f6798e642b9 | lockbox |  | 28.708562 | 19 | Public domain (item-specific mark/dedication) | http://creativecommons.org/licenses/publicdomain/ |
| null_103fad6fcb3a3148 | fit |  | 13.64 | 19 | Public domain (item-specific mark/dedication) | http://creativecommons.org/licenses/publicdomain/ |
| null_451a39cffae4bf7a | select |  | 76.1 | 189 | Public domain (item-specific mark/dedication) | http://creativecommons.org/publicdomain/mark/1.0/ |
| null_0349f2923241b3cc | fit |  | 64.66 | 189 | Public domain (item-specific mark/dedication) | http://creativecommons.org/publicdomain/mark/1.0/ |
| null_17921411647f35a3 | fit |  | 61.76 | 189 | Public domain (item-specific mark/dedication) | http://creativecommons.org/publicdomain/mark/1.0/ |
| null_4b21918fa349d9e1 | fit |  | 78.42 | 189 | Public domain (item-specific mark/dedication) | http://creativecommons.org/publicdomain/mark/1.0/ |
| null_f6b013c6385898ae | fit |  | 87.54 | 189 | Public domain (item-specific mark/dedication) | http://creativecommons.org/publicdomain/mark/1.0/ |
| null_05654528badf2ed9 | select |  | 84.28 | 189 | Public domain (item-specific mark/dedication) | http://creativecommons.org/publicdomain/mark/1.0/ |
| null_af7b4e532ffa88ef | select |  | 84.74 | 189 | Public domain (item-specific mark/dedication) | http://creativecommons.org/publicdomain/mark/1.0/ |
| null_c5ef866bf5355669 | fit |  | 64.32 | 189 | Public domain (item-specific mark/dedication) | http://creativecommons.org/publicdomain/mark/1.0/ |
| null_a24070cad2dfb8c6 | fit |  | 67.74 | 189 | Public domain (item-specific mark/dedication) | http://creativecommons.org/publicdomain/mark/1.0/ |
| null_64af9855c18f979c | fit |  | 48.62 | 189 | Public domain (item-specific mark/dedication) | http://creativecommons.org/publicdomain/mark/1.0/ |
| null_76d61ac83d11e7bf | select |  | 65.72 | 189 | Public domain (item-specific mark/dedication) | http://creativecommons.org/publicdomain/mark/1.0/ |
| null_c7edcc4b6755d58a | fit |  | 57.34 | 189 | Public domain (item-specific mark/dedication) | http://creativecommons.org/publicdomain/mark/1.0/ |
| null_5bc14673aeee5d75 | fit |  | 66.58 | 189 | Public domain (item-specific mark/dedication) | http://creativecommons.org/publicdomain/mark/1.0/ |
| null_42859e3f7128ceb3 | fit |  | 64.64 | 189 | Public domain (item-specific mark/dedication) | http://creativecommons.org/publicdomain/mark/1.0/ |
| null_1a4ecee00f93cd33 | fit |  | 41.9 | 130 | Public domain (item-specific mark/dedication) | http://creativecommons.org/licenses/publicdomain/ |
| null_b221088a45fed1d7 | lockbox |  | 81.841625 | 130 | Public domain (item-specific mark/dedication) | http://creativecommons.org/licenses/publicdomain/ |
| null_dbdb732682d42922 | fit |  | 50.22 | 130 | Public domain (item-specific mark/dedication) | http://creativecommons.org/licenses/publicdomain/ |
| null_95ec96cdfe6da9c7 | fit |  | 56.68 | 130 | Public domain (item-specific mark/dedication) | http://creativecommons.org/licenses/publicdomain/ |
| null_33b5d48805ba23f6 | fit |  | 56.72 | 130 | Public domain (item-specific mark/dedication) | http://creativecommons.org/licenses/publicdomain/ |
| null_1d43bf1c0c0f0362 | select |  | 52.16 | 130 | Public domain (item-specific mark/dedication) | http://creativecommons.org/licenses/publicdomain/ |
| null_a5e93c886eb0fade | select |  | 46.68 | 130 | Public domain (item-specific mark/dedication) | http://creativecommons.org/licenses/publicdomain/ |
| null_933ef8a6bc5ebc63 | lockbox |  | 71.131438 | 130 | Public domain (item-specific mark/dedication) | http://creativecommons.org/licenses/publicdomain/ |
| null_2bb11e7c04cf389c | lockbox |  | 76.617125 | 130 | Public domain (item-specific mark/dedication) | http://creativecommons.org/licenses/publicdomain/ |
| null_ae818918b573fa8a | fit |  | 58.6 | 130 | Public domain (item-specific mark/dedication) | http://creativecommons.org/licenses/publicdomain/ |
| null_ae60dbe0772ba1f8 | fit |  | 47.26 | 130 | Public domain (item-specific mark/dedication) | http://creativecommons.org/licenses/publicdomain/ |
| null_9ec3dc54886d86c4 | select |  | 59.72 | 130 | Public domain (item-specific mark/dedication) | http://creativecommons.org/licenses/publicdomain/ |
| null_15fd0028b82f5472 | fit |  | 56.32 | 130 | Public domain (item-specific mark/dedication) | http://creativecommons.org/licenses/publicdomain/ |
| null_a92855dc07fea3e2 | fit |  | 57.44 | 130 | Public domain (item-specific mark/dedication) | http://creativecommons.org/licenses/publicdomain/ |
| null_0ef9093827d6928c | lockbox |  | 82.416313 | 130 | Public domain (item-specific mark/dedication) | http://creativecommons.org/licenses/publicdomain/ |
| null_ee66c78c6def99f3 | select |  | 58.58 | 130 | Public domain (item-specific mark/dedication) | http://creativecommons.org/licenses/publicdomain/ |
| null_52e24d8d716e9fd4 | select |  | 42.0 | 98 | Public domain (item-specific mark/dedication) | http://creativecommons.org/publicdomain/zero/1.0/ |
| null_d93b56f1077d5c7c | lockbox |  | 77.519813 | 98 | Public domain (item-specific mark/dedication) | http://creativecommons.org/publicdomain/zero/1.0/ |
| null_4df3d466d7ac6495 | select |  | 43.2 | 98 | Public domain (item-specific mark/dedication) | http://creativecommons.org/publicdomain/zero/1.0/ |
| null_7c0e8cca8b428884 | lockbox |  | 66.095625 | 98 | Public domain (item-specific mark/dedication) | http://creativecommons.org/publicdomain/zero/1.0/ |
| null_449dbd411b000ce7 | fit |  | 54.02 | 98 | Public domain (item-specific mark/dedication) | http://creativecommons.org/publicdomain/zero/1.0/ |
| null_4723c759c67a528d | lockbox |  | 77.926187 | 98 | Public domain (item-specific mark/dedication) | http://creativecommons.org/publicdomain/zero/1.0/ |
| null_a08175b0073af338 | fit |  | 48.12 | 98 | Public domain (item-specific mark/dedication) | http://creativecommons.org/publicdomain/zero/1.0/ |
| null_910ffba6c85bf065 | fit |  | 44.72 | 98 | Public domain (item-specific mark/dedication) | http://creativecommons.org/publicdomain/zero/1.0/ |
| null_3fbfa6e5477f27b9 | fit |  | 43.5 | 98 | Public domain (item-specific mark/dedication) | http://creativecommons.org/publicdomain/zero/1.0/ |
| null_1104c75a5effb400 | select |  | 49.34 | 98 | Public domain (item-specific mark/dedication) | http://creativecommons.org/publicdomain/zero/1.0/ |
| null_90760250d1c83aaa | lockbox |  | 64.772063 | 98 | Public domain (item-specific mark/dedication) | http://creativecommons.org/publicdomain/zero/1.0/ |
| null_cf9cd03c3d91d9d0 | fit |  | 39.94 | 98 | Public domain (item-specific mark/dedication) | http://creativecommons.org/publicdomain/zero/1.0/ |
| null_361599c1a5dc04dc | lockbox |  | 43.30675 | 98 | Public domain (item-specific mark/dedication) | http://creativecommons.org/publicdomain/zero/1.0/ |
| null_6add442e33375a34 | fit |  | 48.58 | 98 | Public domain (item-specific mark/dedication) | http://creativecommons.org/publicdomain/zero/1.0/ |
| null_a3d893a9cae6a6fa | lockbox |  | 104.489812 | 167 | Public domain (item-specific mark/dedication) | http://creativecommons.org/licenses/publicdomain/ |
| null_4e6ff1e36a8fb548 | lockbox |  | 89.208187 | 167 | Public domain (item-specific mark/dedication) | http://creativecommons.org/licenses/publicdomain/ |
| null_4b35c1fed9a743d6 | lockbox |  | 89.025312 | 167 | Public domain (item-specific mark/dedication) | http://creativecommons.org/licenses/publicdomain/ |
| null_653ada6db89e839d | fit |  | 107.78 | 167 | Public domain (item-specific mark/dedication) | http://creativecommons.org/licenses/publicdomain/ |
| null_2cebacd28ceade73 | lockbox |  | 95.268563 | 167 | Public domain (item-specific mark/dedication) | http://creativecommons.org/licenses/publicdomain/ |
| null_98677eb40c748ed8 | lockbox |  | 94.040813 | 167 | Public domain (item-specific mark/dedication) | http://creativecommons.org/licenses/publicdomain/ |
| null_ea0fd99a566d95de | select |  | 78.32 | 167 | Public domain (item-specific mark/dedication) | http://creativecommons.org/licenses/publicdomain/ |
| null_29730374d5b3410e | lockbox |  | 83.35675 | 167 | Public domain (item-specific mark/dedication) | http://creativecommons.org/licenses/publicdomain/ |
| null_9251280f2a319317 | lockbox |  | 77.400813 | 167 | Public domain (item-specific mark/dedication) | http://creativecommons.org/licenses/publicdomain/ |
| null_e87033511eded005 | lockbox |  | 91.480812 | 167 | Public domain (item-specific mark/dedication) | http://creativecommons.org/licenses/publicdomain/ |
| null_8f597a5fc4429350 | fit |  | 66.2 | 167 | Public domain (item-specific mark/dedication) | http://creativecommons.org/licenses/publicdomain/ |
| null_8e3fb58528ec3a7d | fit |  | 102.48 | 167 | Public domain (item-specific mark/dedication) | http://creativecommons.org/licenses/publicdomain/ |
| null_5a8698a90c76bbb2 | select |  | 89.56 | 167 | Public domain (item-specific mark/dedication) | http://creativecommons.org/licenses/publicdomain/ |
| null_30461721b761bb36 | fit |  | 68.52 | 167 | Public domain (item-specific mark/dedication) | http://creativecommons.org/licenses/publicdomain/ |
| null_6538ef3378db1f76 | fit |  | 86.64 | 167 | Public domain (item-specific mark/dedication) | http://creativecommons.org/licenses/publicdomain/ |
| null_04e5d7ca7b0481cc | lockbox |  | 106.684062 | 167 | Public domain (item-specific mark/dedication) | http://creativecommons.org/licenses/publicdomain/ |
| null_2983112643803fb0 | fit |  | 70.42 | 167 | Public domain (item-specific mark/dedication) | http://creativecommons.org/licenses/publicdomain/ |
| null_45e2681e49a42689 | lockbox |  | 79.804063 | 167 | Public domain (item-specific mark/dedication) | http://creativecommons.org/licenses/publicdomain/ |
| null_3aeb35fb92c54e35 | select |  | 72.4 | 167 | Public domain (item-specific mark/dedication) | http://creativecommons.org/licenses/publicdomain/ |
| null_300b7f280eaea3b3 | lockbox |  | 80.770625 | 167 | Public domain (item-specific mark/dedication) | http://creativecommons.org/licenses/publicdomain/ |
| null_3cc538a0ec0642a8 | select |  | 68.94 | 167 | Public domain (item-specific mark/dedication) | http://creativecommons.org/licenses/publicdomain/ |
| null_64e9f6c6f13cf668 | lockbox |  | 109.479187 | 167 | Public domain (item-specific mark/dedication) | http://creativecommons.org/licenses/publicdomain/ |
| null_9a760ebcc2a1d4e7 | fit |  | 91.8 | 167 | Public domain (item-specific mark/dedication) | http://creativecommons.org/licenses/publicdomain/ |
| null_41b6a5fa2d3903ff | lockbox |  | 81.293063 | 167 | Public domain (item-specific mark/dedication) | http://creativecommons.org/licenses/publicdomain/ |
| null_90322011988c56e5 | lockbox |  | 100.231875 | 167 | Public domain (item-specific mark/dedication) | http://creativecommons.org/licenses/publicdomain/ |
| null_77fc746ae7a9e95d | fit |  | 88.52 | 170 | Public domain (item-specific mark/dedication) | http://creativecommons.org/publicdomain/zero/1.0/ |
| null_59dcb603b7186773 | fit |  | 105.8 | 170 | Public domain (item-specific mark/dedication) | http://creativecommons.org/publicdomain/zero/1.0/ |
| null_58662421c24da2f4 | fit |  | 77.6 | 170 | Public domain (item-specific mark/dedication) | http://creativecommons.org/publicdomain/zero/1.0/ |
| null_34e47ac12f3b2760 | select |  | 80.26 | 170 | Public domain (item-specific mark/dedication) | http://creativecommons.org/publicdomain/zero/1.0/ |
| null_d44206037543c767 | fit |  | 95.44 | 170 | Public domain (item-specific mark/dedication) | http://creativecommons.org/publicdomain/zero/1.0/ |
| null_38aa75164cf89b4c | fit |  | 56.46 | 170 | Public domain (item-specific mark/dedication) | http://creativecommons.org/publicdomain/zero/1.0/ |
| null_7e961d2a41f33b0e | select |  | 82.76 | 170 | Public domain (item-specific mark/dedication) | http://creativecommons.org/publicdomain/zero/1.0/ |
| null_a8d05de59b88d065 | lockbox |  | 116.166562 | 170 | Public domain (item-specific mark/dedication) | http://creativecommons.org/publicdomain/zero/1.0/ |
| null_ef342ddd98875dd4 | select |  | 67.72 | 170 | Public domain (item-specific mark/dedication) | http://creativecommons.org/publicdomain/zero/1.0/ |
| null_ca9f320d0ad95f78 | select |  | 78.28 | 170 | Public domain (item-specific mark/dedication) | http://creativecommons.org/publicdomain/zero/1.0/ |
| null_1aac2f11f5fc0a83 | select |  | 71.6 | 170 | Public domain (item-specific mark/dedication) | http://creativecommons.org/publicdomain/zero/1.0/ |
| null_a54188a4569d2b8a | fit |  | 81.1 | 170 | Public domain (item-specific mark/dedication) | http://creativecommons.org/publicdomain/zero/1.0/ |
| null_8fda07ccebc0c7fb | fit |  | 60.44 | 108 | Public domain (item-specific mark/dedication) | http://creativecommons.org/publicdomain/mark/1.0/ |
| null_783b077dc5e50bdd | fit |  | 47.4 | 108 | Public domain (item-specific mark/dedication) | http://creativecommons.org/publicdomain/mark/1.0/ |
| null_10a8ea8e5c042133 | fit |  | 64.62 | 108 | Public domain (item-specific mark/dedication) | http://creativecommons.org/publicdomain/mark/1.0/ |
| null_87cc45996fca66fe | fit |  | 60.98 | 108 | Public domain (item-specific mark/dedication) | http://creativecommons.org/publicdomain/mark/1.0/ |
| null_b363ee86928cc559 | fit |  | 62.02 | 108 | Public domain (item-specific mark/dedication) | http://creativecommons.org/publicdomain/mark/1.0/ |
| null_5a139f4b7252d119 | select |  | 57.46 | 108 | Public domain (item-specific mark/dedication) | http://creativecommons.org/publicdomain/mark/1.0/ |
| null_6566456f5fa076f8 | select |  | 58.36 | 108 | Public domain (item-specific mark/dedication) | http://creativecommons.org/publicdomain/mark/1.0/ |
| null_96b18631796b0482 | fit |  | 55.58 | 108 | Public domain (item-specific mark/dedication) | http://creativecommons.org/publicdomain/mark/1.0/ |
| null_a7e27cbc42ffa929 | select |  | 47.0 | 108 | Public domain (item-specific mark/dedication) | http://creativecommons.org/publicdomain/mark/1.0/ |
| null_1c47f3d8a7245fc4 | fit |  | 63.44 | 108 | Public domain (item-specific mark/dedication) | http://creativecommons.org/publicdomain/mark/1.0/ |
| null_b8d0189c3a2d633a | fit |  | 51.92 | 108 | Public domain (item-specific mark/dedication) | http://creativecommons.org/publicdomain/mark/1.0/ |
| null_730e866f2c6fec5f | fit |  | 52.26 | 108 | Public domain (item-specific mark/dedication) | http://creativecommons.org/publicdomain/mark/1.0/ |
| null_11bb148f05aaf071 | fit |  | 56.06 | 108 | Public domain (item-specific mark/dedication) | http://creativecommons.org/publicdomain/mark/1.0/ |
| null_2699e47f1dea9873 | select |  | 55.08 | 108 | Public domain (item-specific mark/dedication) | http://creativecommons.org/publicdomain/mark/1.0/ |
| null_48865703378d8370 | fit |  | 57.86 | 108 | Public domain (item-specific mark/dedication) | http://creativecommons.org/publicdomain/mark/1.0/ |
| null_4dd49e3da09de282 | select |  | 46.8 | 108 | Public domain (item-specific mark/dedication) | http://creativecommons.org/publicdomain/mark/1.0/ |
| null_a04f220982e73227 | fit |  | 93.64 | 194 | Public domain (item-specific mark/dedication) | http://creativecommons.org/licenses/publicdomain/ |
| null_32a33f2d065d3f29 | fit |  | 95.92 | 194 | Public domain (item-specific mark/dedication) | http://creativecommons.org/licenses/publicdomain/ |
| null_b21fa3e00ac3c2bb | lockbox |  | 107.88575 | 194 | Public domain (item-specific mark/dedication) | http://creativecommons.org/licenses/publicdomain/ |
| null_7b0d777f09ea04c1 | select |  | 97.32 | 194 | Public domain (item-specific mark/dedication) | http://creativecommons.org/licenses/publicdomain/ |
| null_5cc20b4e314bb52b | fit |  | 76.56 | 194 | Public domain (item-specific mark/dedication) | http://creativecommons.org/licenses/publicdomain/ |
| null_d2c5e146c5edfc70 | fit |  | 101.98 | 194 | Public domain (item-specific mark/dedication) | http://creativecommons.org/licenses/publicdomain/ |
| null_bcf7a917d18f1411 | lockbox |  | 126.798375 | 194 | Public domain (item-specific mark/dedication) | http://creativecommons.org/licenses/publicdomain/ |
| null_5c3816b8d467d784 | fit |  | 91.22 | 194 | Public domain (item-specific mark/dedication) | http://creativecommons.org/licenses/publicdomain/ |
| null_6b8d259befed413a | fit |  | 107.54 | 194 | Public domain (item-specific mark/dedication) | http://creativecommons.org/licenses/publicdomain/ |
| null_b9c64d4378c877b9 | select |  | 89.06 | 194 | Public domain (item-specific mark/dedication) | http://creativecommons.org/licenses/publicdomain/ |
| null_e86b764e6feaba8f | select |  | 80.34 | 194 | Public domain (item-specific mark/dedication) | http://creativecommons.org/licenses/publicdomain/ |
| null_96fa3a1a15d19968 | fit |  | 69.8 | 194 | Public domain (item-specific mark/dedication) | http://creativecommons.org/licenses/publicdomain/ |
| null_97f4b5ed53ad1315 | lockbox |  | 69.903688 | 112 | Public domain (item-specific mark/dedication) | http://creativecommons.org/publicdomain/zero/1.0/ |
| null_fd50274af9c67d1c | select |  | 59.92 | 112 | Public domain (item-specific mark/dedication) | http://creativecommons.org/publicdomain/zero/1.0/ |
| null_184c5b471621ea83 | fit |  | 43.38 | 112 | Public domain (item-specific mark/dedication) | http://creativecommons.org/publicdomain/zero/1.0/ |
| null_60dc06e2b4aaba5c | fit |  | 52.36 | 112 | Public domain (item-specific mark/dedication) | http://creativecommons.org/publicdomain/zero/1.0/ |
| null_faded9a4b632c5b0 | fit |  | 49.72 | 112 | Public domain (item-specific mark/dedication) | http://creativecommons.org/publicdomain/zero/1.0/ |
| null_597b5df3d63926a3 | lockbox |  | 90.035375 | 112 | Public domain (item-specific mark/dedication) | http://creativecommons.org/publicdomain/zero/1.0/ |
| null_f37af13817e7ca50 | fit |  | 54.34 | 112 | Public domain (item-specific mark/dedication) | http://creativecommons.org/publicdomain/zero/1.0/ |
| null_8b5b4ccc159a04f0 | fit |  | 55.02 | 112 | Public domain (item-specific mark/dedication) | http://creativecommons.org/publicdomain/zero/1.0/ |
| null_e236cdddaf77c2a5 | fit |  | 65.98 | 112 | Public domain (item-specific mark/dedication) | http://creativecommons.org/publicdomain/zero/1.0/ |
| null_7d96ac872cd4a374 | select |  | 49.26 | 112 | Public domain (item-specific mark/dedication) | http://creativecommons.org/publicdomain/zero/1.0/ |
| null_3e5508c61100bfe0 | fit |  | 58.0 | 112 | Public domain (item-specific mark/dedication) | http://creativecommons.org/publicdomain/zero/1.0/ |
| null_afd5d1b794b990e2 | select |  | 51.78 | 112 | Public domain (item-specific mark/dedication) | http://creativecommons.org/publicdomain/zero/1.0/ |
| null_174c545b236bf6e1 | fit |  | 60.56 | 112 | Public domain (item-specific mark/dedication) | http://creativecommons.org/publicdomain/zero/1.0/ |
| null_1cf3032f631c2f15 | fit |  | 32.5 | 74 | Public domain (item-specific mark/dedication) | http://creativecommons.org/publicdomain/zero/1.0/ |
| null_319592e8c2eddb46 | select |  | 32.06 | 74 | Public domain (item-specific mark/dedication) | http://creativecommons.org/publicdomain/zero/1.0/ |
| null_04c0a9e8492e64d9 | fit |  | 35.9 | 74 | Public domain (item-specific mark/dedication) | http://creativecommons.org/publicdomain/zero/1.0/ |
| null_e2e1dfb53933d01a | select |  | 33.6 | 74 | Public domain (item-specific mark/dedication) | http://creativecommons.org/publicdomain/zero/1.0/ |
| null_7b63aa33d8908651 | fit |  | 29.28 | 74 | Public domain (item-specific mark/dedication) | http://creativecommons.org/publicdomain/zero/1.0/ |
| null_d5f59d33a00bf1c9 | fit |  | 41.98 | 74 | Public domain (item-specific mark/dedication) | http://creativecommons.org/publicdomain/zero/1.0/ |
| null_161a6e82e4588e4f | fit |  | 32.94 | 74 | Public domain (item-specific mark/dedication) | http://creativecommons.org/publicdomain/zero/1.0/ |
| null_69679ba22afea9a2 | fit |  | 28.58 | 74 | Public domain (item-specific mark/dedication) | http://creativecommons.org/publicdomain/zero/1.0/ |
| null_15a0e10444e40bd0 | select |  | 32.68 | 74 | Public domain (item-specific mark/dedication) | http://creativecommons.org/publicdomain/zero/1.0/ |
| null_cbe8a74ee97a195b | fit |  | 37.5 | 74 | Public domain (item-specific mark/dedication) | http://creativecommons.org/publicdomain/zero/1.0/ |
| null_4e04a97e891f6fd6 | select |  | 35.76 | 74 | Public domain (item-specific mark/dedication) | http://creativecommons.org/publicdomain/zero/1.0/ |
| null_e93f032ea48ba9ed | select |  | 31.28 | 74 | Public domain (item-specific mark/dedication) | http://creativecommons.org/publicdomain/zero/1.0/ |
| null_ab709760ac93a459 | fit |  | 29.12 | 74 | Public domain (item-specific mark/dedication) | http://creativecommons.org/publicdomain/zero/1.0/ |
| null_3a8a41260856a8f8 | fit |  | 27.14 | 74 | Public domain (item-specific mark/dedication) | http://creativecommons.org/publicdomain/zero/1.0/ |
| null_ec651ea07bd1c466 | fit |  | 33.48 | 74 | Public domain (item-specific mark/dedication) | http://creativecommons.org/publicdomain/zero/1.0/ |
| null_bd23f46112211a20 | fit |  | 40.3 | 75 | Public domain (item-specific mark/dedication) | http://creativecommons.org/publicdomain/zero/1.0/ |
| null_1077ad58c6e3eda0 | lockbox |  | 68.250375 | 75 | Public domain (item-specific mark/dedication) | http://creativecommons.org/publicdomain/zero/1.0/ |
| null_12fb6b9a20b7a9da | fit |  | 38.4 | 75 | Public domain (item-specific mark/dedication) | http://creativecommons.org/publicdomain/zero/1.0/ |
| null_b077b5bb5de03811 | fit |  | 32.96 | 75 | Public domain (item-specific mark/dedication) | http://creativecommons.org/publicdomain/zero/1.0/ |
| null_48ec00aed6f1bb35 | fit |  | 35.8 | 75 | Public domain (item-specific mark/dedication) | http://creativecommons.org/publicdomain/zero/1.0/ |
| null_0eab000ef2dccdab | select |  | 28.56 | 75 | Public domain (item-specific mark/dedication) | http://creativecommons.org/publicdomain/zero/1.0/ |
| null_4dff6480a76eb95e | fit |  | 27.94 | 75 | Public domain (item-specific mark/dedication) | http://creativecommons.org/publicdomain/zero/1.0/ |
| null_204f2a7ac93c9429 | lockbox |  | 64.098687 | 75 | Public domain (item-specific mark/dedication) | http://creativecommons.org/publicdomain/zero/1.0/ |
| null_b15b66aac39b6f53 | select |  | 34.94 | 75 | Public domain (item-specific mark/dedication) | http://creativecommons.org/publicdomain/zero/1.0/ |
| null_1dcddd4492811e53 | select |  | 36.02 | 75 | Public domain (item-specific mark/dedication) | http://creativecommons.org/publicdomain/zero/1.0/ |
| null_f7891e6ffeab1de7 | fit |  | 31.02 | 75 | Public domain (item-specific mark/dedication) | http://creativecommons.org/publicdomain/zero/1.0/ |
| null_95e268cabbfc52f6 | fit |  | 29.7 | 75 | Public domain (item-specific mark/dedication) | http://creativecommons.org/publicdomain/zero/1.0/ |
| null_a1325e0d4bb5b349 | select |  | 35.98 | 75 | Public domain (item-specific mark/dedication) | http://creativecommons.org/publicdomain/zero/1.0/ |
| null_f06729b75fed3d88 | fit |  | 37.72 | 75 | Public domain (item-specific mark/dedication) | http://creativecommons.org/publicdomain/zero/1.0/ |
| null_af3cebecc533c257 | fit |  | 32.48 | 75 | Public domain (item-specific mark/dedication) | http://creativecommons.org/publicdomain/zero/1.0/ |
| null_5e0cbb0d389e09bf | lockbox |  | 51.93 | 75 | Public domain (item-specific mark/dedication) | http://creativecommons.org/publicdomain/zero/1.0/ |
| null_cd034ce567b1bf57 | fit |  | 33.48 | 75 | Public domain (item-specific mark/dedication) | http://creativecommons.org/publicdomain/zero/1.0/ |
| null_66bc0e646cc5afb3 | select |  | 36.68 | 75 | Public domain (item-specific mark/dedication) | http://creativecommons.org/publicdomain/zero/1.0/ |
| null_aef967af6665de35 | fit |  | 42.0 | 73 | Public domain (item-specific mark/dedication) | http://creativecommons.org/publicdomain/mark/1.0/ |
| null_072561841089453f | fit |  | 41.56 | 73 | Public domain (item-specific mark/dedication) | http://creativecommons.org/publicdomain/mark/1.0/ |
| null_98db710d928bbc74 | select |  | 32.18 | 73 | Public domain (item-specific mark/dedication) | http://creativecommons.org/publicdomain/mark/1.0/ |
| null_8949cf9f1106cb05 | fit |  | 39.64 | 73 | Public domain (item-specific mark/dedication) | http://creativecommons.org/publicdomain/mark/1.0/ |
| null_552dbaab37e97d79 | select |  | 29.62 | 73 | Public domain (item-specific mark/dedication) | http://creativecommons.org/publicdomain/mark/1.0/ |
| null_c06d34393e08b32d | select |  | 44.88 | 73 | Public domain (item-specific mark/dedication) | http://creativecommons.org/publicdomain/mark/1.0/ |
| null_c87c87eb5840f519 | select |  | 39.9 | 73 | Public domain (item-specific mark/dedication) | http://creativecommons.org/publicdomain/mark/1.0/ |
| null_247d18b560bda399 | fit |  | 34.78 | 73 | Public domain (item-specific mark/dedication) | http://creativecommons.org/publicdomain/mark/1.0/ |
| null_05c144613b36ed93 | fit |  | 35.68 | 73 | Public domain (item-specific mark/dedication) | http://creativecommons.org/publicdomain/mark/1.0/ |
| null_a59e9921fa6279f5 | fit |  | 31.54 | 73 | Public domain (item-specific mark/dedication) | http://creativecommons.org/publicdomain/mark/1.0/ |
| null_732573b3d8c52d27 | fit |  | 40.12 | 73 | Public domain (item-specific mark/dedication) | http://creativecommons.org/publicdomain/mark/1.0/ |
| null_4faa65c4f8e46dc0 | fit |  | 35.26 | 73 | Public domain (item-specific mark/dedication) | http://creativecommons.org/publicdomain/mark/1.0/ |
| null_c6d1d0ce99d5e27d | fit |  | 38.12 | 73 | Public domain (item-specific mark/dedication) | http://creativecommons.org/publicdomain/mark/1.0/ |
| null_b2d893519bcb4845 | fit |  | 30.92 | 73 | Public domain (item-specific mark/dedication) | http://creativecommons.org/publicdomain/mark/1.0/ |

Flawed clips: 448 (core and extra single-level, identity / placebo, ladder G1 / G3 / G5, cross-speaker edits, and extra family botched readings); files: 2410.

Labels (`labels/<clip>.json`) hold the parent hash, recipe, seed, chain, word alignment carried through the analytic time map, and per flaw: type, dimension, level, physical magnitude, realised change, expected secondary dimensions, word span, and half-open sample spans in the clip and in the parent.

Coverage is capped at 35 % edited-word coverage (boundary edits excluded; G5, identity and extra family botched clips exempt).
Edit-support time shares are separate and include boundary edits and release supports.
Recipe names label controlled acoustic departures from the reference rendition; Clarity (spectral-change proxy) does not measure intelligibility.
Scores are a reference-relative delivery index.

| clip | edit-support time share |
|---|---|
| eisenhower_farewell_1961__G1 | 8.9% |
| eisenhower_farewell_1961__G3 | 20.8% |
| eisenhower_farewell_1961__G5 | 93.6% |
| eisenhower_farewell_1961__extra_L1A | 22.4% |
| eisenhower_farewell_1961__extra_L1B | 7.4% |
| eisenhower_farewell_1961__extra_L1C | 12.2% |
| eisenhower_farewell_1961__extra_L1D | 8.5% |
| eisenhower_farewell_1961__extra_L2A | 21.7% |
| eisenhower_farewell_1961__extra_L2B | 8.9% |
| eisenhower_farewell_1961__extra_L2C | 13.5% |
| eisenhower_farewell_1961__extra_L2D | 11.5% |
| eisenhower_farewell_1961__extra_L3A | 20.9% |
| eisenhower_farewell_1961__extra_L3B | 10.9% |
| eisenhower_farewell_1961__extra_L3C | 14.9% |
| eisenhower_farewell_1961__extra_L3D | 14.5% |
| eisenhower_farewell_1961__extra_botched_CONTOUR | 24.3% |
| eisenhower_farewell_1961__extra_botched_D1 | 43.3% |
| eisenhower_farewell_1961__extra_botched_D2 | 39.8% |
| eisenhower_farewell_1961__extra_botched_D4 | 3.3% |
| eisenhower_farewell_1961__extra_botched_D5 | 37.5% |
| eisenhower_farewell_1961__extra_botched_DISFLUENCY | 24.4% |
| eisenhower_farewell_1961__extra_botched_ENDINGS | 0.9% |
| eisenhower_farewell_1961__identity | 40.7% |
| eisenhower_farewell_1961__single_L1A | 22.7% |
| eisenhower_farewell_1961__single_L1B | 21.7% |
| eisenhower_farewell_1961__single_L2A | 17.1% |
| eisenhower_farewell_1961__single_L2B | 25.8% |
| eisenhower_farewell_1961__single_L3A | 33.5% |
| eisenhower_farewell_1961__single_L3B | 25.1% |
| gettysburg_amb__extra_botched_CONTOUR | 40.4% |
| gettysburg_amb__extra_botched_D1 | 53.7% |
| gettysburg_amb__extra_botched_D2 | 40.2% |
| gettysburg_amb__extra_botched_D4 | 5.6% |
| gettysburg_amb__extra_botched_D5 | 39.3% |
| gettysburg_amb__extra_botched_DISFLUENCY | 23.8% |
| gettysburg_amb__extra_botched_ENDINGS | 4.4% |
| gettysburg_amb__extra_x10_L3 | 29.8% |
| gettysburg_amb__extra_x1_L2 | 18.5% |
| gettysburg_amb__extra_x2_L2 | 10.6% |
| gettysburg_amb__extra_x3_L2 | 15.8% |
| gettysburg_amb__extra_x4_L2 | 15.2% |
| gettysburg_amb__extra_x5_L3 | 18.7% |
| gettysburg_amb__extra_x6_L3 | 13.2% |
| gettysburg_amb__extra_x7_L3 | 18.0% |
| gettysburg_amb__extra_x8_L3 | 18.6% |
| gettysburg_amb__extra_x9_L3 | 4.2% |
| gettysburg_dj__G5 | 91.1% |
| gettysburg_dj__extra_botched_CONTOUR | 18.1% |
| gettysburg_dj__extra_botched_D1 | 33.4% |
| gettysburg_dj__extra_botched_D2 | 43.4% |
| gettysburg_dj__extra_botched_D4 | 3.7% |
| gettysburg_dj__extra_botched_D5 | 34.2% |
| gettysburg_dj__extra_botched_DISFLUENCY | 26.4% |
| gettysburg_dj__extra_botched_ENDINGS | 4.1% |
| gettysburg_dj__extra_x10_L3 | 9.7% |
| gettysburg_dj__extra_x1_L2 | 19.1% |
| gettysburg_dj__extra_x2_L2 | 9.9% |
| gettysburg_dj__extra_x3_L2 | 14.6% |
| gettysburg_dj__extra_x4_L2 | 15.4% |
| gettysburg_dj__extra_x5_L3 | 18.7% |
| gettysburg_dj__extra_x6_L3 | 12.6% |
| gettysburg_dj__extra_x7_L3 | 17.0% |
| gettysburg_dj__extra_x8_L3 | 19.2% |
| gettysburg_dj__extra_x9_L3 | 3.9% |
| gettysburg_dj__x1_L2 | 7.9% |
| gettysburg_dj__x2_L3 | 25.0% |
| gettysburg_dj__x3_L3 | 15.5% |
| gettysburg_dj__x4_L3 | 12.9% |
| gettysburg_dl__extra_botched_CONTOUR | 62.1% |
| gettysburg_dl__extra_botched_D1 | 45.9% |
| gettysburg_dl__extra_botched_D2 | 36.8% |
| gettysburg_dl__extra_botched_D5 | 30.4% |
| gettysburg_dl__extra_botched_DISFLUENCY | 26.1% |
| gettysburg_dl__extra_botched_ENDINGS | 3.6% |
| gettysburg_dl__extra_x10_L3 | 29.1% |
| gettysburg_dl__extra_x1_L2 | 19.3% |
| gettysburg_dl__extra_x2_L2 | 7.8% |
| gettysburg_dl__extra_x3_L2 | 12.0% |
| gettysburg_dl__extra_x4_L2 | 12.5% |
| gettysburg_dl__extra_x5_L3 | 19.3% |
| gettysburg_dl__extra_x6_L3 | 10.1% |
| gettysburg_dl__extra_x7_L3 | 13.6% |
| gettysburg_dl__extra_x8_L3 | 15.5% |
| gettysburg_dl__extra_x9_L3 | 0.9% |
| gettysburg_fb__extra_botched_CONTOUR | 20.1% |
| gettysburg_fb__extra_botched_D1 | 45.6% |
| gettysburg_fb__extra_botched_D2 | 28.2% |
| gettysburg_fb__extra_botched_D4 | 1.3% |
| gettysburg_fb__extra_botched_D5 | 35.1% |
| gettysburg_fb__extra_botched_DISFLUENCY | 27.4% |
| gettysburg_fb__extra_botched_ENDINGS | 3.0% |
| gettysburg_fb__extra_x10_L3 | 11.8% |
| gettysburg_fb__extra_x1_L2 | 26.1% |
| gettysburg_fb__extra_x2_L2 | 9.3% |
| gettysburg_fb__extra_x3_L2 | 8.9% |
| gettysburg_fb__extra_x4_L2 | 14.4% |
| gettysburg_fb__extra_x5_L3 | 26.2% |
| gettysburg_fb__extra_x6_L3 | 11.7% |
| gettysburg_fb__extra_x7_L3 | 10.5% |
| gettysburg_fb__extra_x8_L3 | 17.7% |
| gettysburg_fb__extra_x9_L3 | 2.1% |
| gettysburg_jn__extra_botched_CONTOUR | 23.3% |
| gettysburg_jn__extra_botched_D1 | 48.8% |
| gettysburg_jn__extra_botched_D2 | 41.0% |
| gettysburg_jn__extra_botched_D4 | 3.4% |
| gettysburg_jn__extra_botched_D5 | 36.7% |
| gettysburg_jn__extra_botched_DISFLUENCY | 28.1% |
| gettysburg_jn__extra_botched_ENDINGS | 3.9% |
| gettysburg_jn__extra_x10_L3 | 29.6% |
| gettysburg_jn__extra_x1_L2 | 21.1% |
| gettysburg_jn__extra_x2_L2 | 11.0% |
| gettysburg_jn__extra_x3_L2 | 10.5% |
| gettysburg_jn__extra_x4_L2 | 16.7% |
| gettysburg_jn__extra_x5_L3 | 21.0% |
| gettysburg_jn__extra_x6_L3 | 13.7% |
| gettysburg_jn__extra_x7_L3 | 12.3% |
| gettysburg_jn__extra_x8_L3 | 19.9% |
| gettysburg_jn__extra_x9_L3 | 2.8% |
| gettysburg_pc__extra_botched_CONTOUR | 38.3% |
| gettysburg_pc__extra_botched_D1 | 44.3% |
| gettysburg_pc__extra_botched_D2 | 26.3% |
| gettysburg_pc__extra_botched_D5 | 28.8% |
| gettysburg_pc__extra_botched_DISFLUENCY | 26.0% |
| gettysburg_pc__extra_botched_ENDINGS | 2.7% |
| gettysburg_pc__extra_x10_L3 | 10.2% |
| gettysburg_pc__extra_x1_L2 | 26.6% |
| gettysburg_pc__extra_x2_L2 | 9.8% |
| gettysburg_pc__extra_x3_L2 | 10.3% |
| gettysburg_pc__extra_x4_L2 | 16.2% |
| gettysburg_pc__extra_x5_L3 | 26.5% |
| gettysburg_pc__extra_x6_L3 | 12.1% |
| gettysburg_pc__extra_x7_L3 | 11.9% |
| gettysburg_pc__extra_x8_L3 | 19.1% |
| gettysburg_pc__extra_x9_L3 | 0.9% |
| gettysburg_sa__G5 | 93.6% |
| gettysburg_sa__extra_botched_CONTOUR | 65.3% |
| gettysburg_sa__extra_botched_D1 | 34.9% |
| gettysburg_sa__extra_botched_D2 | 23.7% |
| gettysburg_sa__extra_botched_D4 | 3.4% |
| gettysburg_sa__extra_botched_D5 | 32.2% |
| gettysburg_sa__extra_botched_DISFLUENCY | 24.8% |
| gettysburg_sa__extra_botched_ENDINGS | 3.5% |
| gettysburg_sa__extra_x10_L3 | 29.8% |
| gettysburg_sa__extra_x1_L2 | 14.9% |
| gettysburg_sa__extra_x2_L2 | 8.1% |
| gettysburg_sa__extra_x3_L2 | 9.9% |
| gettysburg_sa__extra_x4_L2 | 19.3% |
| gettysburg_sa__extra_x5_L3 | 14.3% |
| gettysburg_sa__extra_x6_L3 | 10.4% |
| gettysburg_sa__extra_x7_L3 | 11.7% |
| gettysburg_sa__extra_x8_L3 | 21.8% |
| gettysburg_sa__extra_x9_L3 | 4.3% |
| gettysburg_sa__x1_L2 | 5.4% |
| gettysburg_sa__x2_L3 | 20.0% |
| gettysburg_sa__x3_L3 | 12.6% |
| gettysburg_sa__x4_L3 | 8.1% |
| gettysburg_tg__G5 | 93.2% |
| gettysburg_tg__extra_botched_CONTOUR | 61.2% |
| gettysburg_tg__extra_botched_D1 | 39.4% |
| gettysburg_tg__extra_botched_D2 | 45.2% |
| gettysburg_tg__extra_botched_D4 | 2.6% |
| gettysburg_tg__extra_botched_D5 | 31.7% |
| gettysburg_tg__extra_botched_DISFLUENCY | 24.5% |
| gettysburg_tg__extra_botched_ENDINGS | 4.4% |
| gettysburg_tg__extra_x10_L3 | 11.2% |
| gettysburg_tg__extra_x1_L2 | 23.2% |
| gettysburg_tg__extra_x2_L2 | 13.4% |
| gettysburg_tg__extra_x3_L2 | 12.6% |
| gettysburg_tg__extra_x4_L2 | 14.2% |
| gettysburg_tg__extra_x5_L3 | 23.0% |
| gettysburg_tg__extra_x6_L3 | 16.3% |
| gettysburg_tg__extra_x7_L3 | 14.7% |
| gettysburg_tg__extra_x8_L3 | 17.8% |
| gettysburg_tg__extra_x9_L3 | 3.7% |
| gettysburg_tg__x1_L2 | 4.3% |
| gettysburg_tg__x2_L3 | 19.8% |
| gettysburg_tg__x3_L3 | 11.3% |
| gettysburg_tg__x4_L3 | 5.1% |
| gettysburg_wt__extra_botched_CONTOUR | 35.4% |
| gettysburg_wt__extra_botched_D1 | 47.2% |
| gettysburg_wt__extra_botched_D2 | 37.0% |
| gettysburg_wt__extra_botched_D5 | 27.9% |
| gettysburg_wt__extra_botched_DISFLUENCY | 24.0% |
| gettysburg_wt__extra_botched_ENDINGS | 3.3% |
| gettysburg_wt__extra_x10_L3 | 9.8% |
| gettysburg_wt__extra_x1_L2 | 17.7% |
| gettysburg_wt__extra_x2_L2 | 9.9% |
| gettysburg_wt__extra_x3_L2 | 13.5% |
| gettysburg_wt__extra_x4_L2 | 12.0% |
| gettysburg_wt__extra_x5_L3 | 17.5% |
| gettysburg_wt__extra_x6_L3 | 12.0% |
| gettysburg_wt__extra_x7_L3 | 15.3% |
| gettysburg_wt__extra_x8_L3 | 15.0% |
| gettysburg_wt__extra_x9_L3 | 0.9% |
| greenman_reagan__G5 | 94.7% |
| greenman_reagan__extra_botched_CONTOUR | 42.7% |
| greenman_reagan__extra_botched_D1 | 37.8% |
| greenman_reagan__extra_botched_D2 | 33.3% |
| greenman_reagan__extra_botched_D4 | 3.3% |
| greenman_reagan__extra_botched_D5 | 22.2% |
| greenman_reagan__extra_botched_DISFLUENCY | 14.9% |
| greenman_reagan__extra_botched_ENDINGS | 3.3% |
| greenman_reagan__extra_x10_L3 | 22.8% |
| greenman_reagan__extra_x1_L2 | 13.2% |
| greenman_reagan__extra_x2_L2 | 8.1% |
| greenman_reagan__extra_x3_L2 | 10.8% |
| greenman_reagan__extra_x4_L2 | 12.3% |
| greenman_reagan__extra_x5_L3 | 13.1% |
| greenman_reagan__extra_x6_L3 | 10.1% |
| greenman_reagan__extra_x7_L3 | 12.4% |
| greenman_reagan__extra_x8_L3 | 15.1% |
| greenman_reagan__extra_x9_L3 | 2.0% |
| greenman_reagan__x1_L2 | 2.9% |
| greenman_reagan__x2_L3 | 12.2% |
| greenman_reagan__x3_L3 | 9.5% |
| greenman_reagan__x4_L3 | 5.1% |
| gwbush_911_2001__G1 | 4.0% |
| gwbush_911_2001__G3 | 14.2% |
| gwbush_911_2001__G5 | 92.8% |
| gwbush_911_2001__extra_L1A | 17.0% |
| gwbush_911_2001__extra_L1B | 5.2% |
| gwbush_911_2001__extra_L1C | 13.8% |
| gwbush_911_2001__extra_L1D | 17.3% |
| gwbush_911_2001__extra_L2A | 16.5% |
| gwbush_911_2001__extra_L2B | 6.6% |
| gwbush_911_2001__extra_L2C | 15.8% |
| gwbush_911_2001__extra_L2D | 20.3% |
| gwbush_911_2001__extra_L3A | 15.9% |
| gwbush_911_2001__extra_L3B | 8.7% |
| gwbush_911_2001__extra_L3C | 17.7% |
| gwbush_911_2001__extra_L3D | 23.2% |
| gwbush_911_2001__extra_botched_CONTOUR | 41.0% |
| gwbush_911_2001__extra_botched_D1 | 28.6% |
| gwbush_911_2001__extra_botched_D2 | 8.4% |
| gwbush_911_2001__extra_botched_D4 | 2.6% |
| gwbush_911_2001__extra_botched_D5 | 31.6% |
| gwbush_911_2001__extra_botched_DISFLUENCY | 25.9% |
| gwbush_911_2001__extra_botched_ENDINGS | 3.8% |
| gwbush_911_2001__identity | 29.5% |
| gwbush_911_2001__single_L1A | 19.4% |
| gwbush_911_2001__single_L1B | 15.5% |
| gwbush_911_2001__single_L2A | 19.0% |
| gwbush_911_2001__single_L2B | 16.8% |
| gwbush_911_2001__single_L3A | 23.9% |
| gwbush_911_2001__single_L3B | 22.1% |
| harris_uncsw_2021__G1 | 5.3% |
| harris_uncsw_2021__G3 | 29.8% |
| harris_uncsw_2021__G5 | 94.4% |
| harris_uncsw_2021__extra_L1A | 19.9% |
| harris_uncsw_2021__extra_L1B | 3.9% |
| harris_uncsw_2021__extra_L1C | 17.4% |
| harris_uncsw_2021__extra_L1D | 21.8% |
| harris_uncsw_2021__extra_L2A | 19.9% |
| harris_uncsw_2021__extra_L2B | 5.6% |
| harris_uncsw_2021__extra_L2C | 19.1% |
| harris_uncsw_2021__extra_L2D | 24.2% |
| harris_uncsw_2021__extra_L3A | 19.9% |
| harris_uncsw_2021__extra_L3B | 10.1% |
| harris_uncsw_2021__extra_L3C | 20.8% |
| harris_uncsw_2021__extra_L3D | 26.6% |
| harris_uncsw_2021__extra_botched_CONTOUR | 37.3% |
| harris_uncsw_2021__extra_botched_D1 | 51.3% |
| harris_uncsw_2021__extra_botched_D2 | 10.6% |
| harris_uncsw_2021__extra_botched_D4 | 4.9% |
| harris_uncsw_2021__extra_botched_D5 | 33.6% |
| harris_uncsw_2021__extra_botched_DISFLUENCY | 23.8% |
| harris_uncsw_2021__extra_botched_ENDINGS | 2.5% |
| harris_uncsw_2021__identity | 34.1% |
| harris_uncsw_2021__single_L1A | 24.9% |
| harris_uncsw_2021__single_L1B | 26.6% |
| harris_uncsw_2021__single_L2A | 25.9% |
| harris_uncsw_2021__single_L2B | 23.1% |
| harris_uncsw_2021__single_L3A | 23.1% |
| harris_uncsw_2021__single_L3B | 27.7% |
| hclinton_tomorrow_2010__G1 | 14.1% |
| hclinton_tomorrow_2010__G3 | 21.7% |
| hclinton_tomorrow_2010__G5 | 91.3% |
| hclinton_tomorrow_2010__extra_L1A | 20.8% |
| hclinton_tomorrow_2010__extra_L1B | 7.6% |
| hclinton_tomorrow_2010__extra_L1C | 13.9% |
| hclinton_tomorrow_2010__extra_L1D | 13.0% |
| hclinton_tomorrow_2010__extra_L2A | 20.9% |
| hclinton_tomorrow_2010__extra_L2B | 9.6% |
| hclinton_tomorrow_2010__extra_L2C | 15.8% |
| hclinton_tomorrow_2010__extra_L2D | 16.7% |
| hclinton_tomorrow_2010__extra_L3A | 20.9% |
| hclinton_tomorrow_2010__extra_L3B | 12.2% |
| hclinton_tomorrow_2010__extra_L3C | 17.7% |
| hclinton_tomorrow_2010__extra_L3D | 20.1% |
| hclinton_tomorrow_2010__extra_botched_CONTOUR | 38.1% |
| hclinton_tomorrow_2010__extra_botched_D1 | 28.0% |
| hclinton_tomorrow_2010__extra_botched_D2 | 30.2% |
| hclinton_tomorrow_2010__extra_botched_D4 | 7.1% |
| hclinton_tomorrow_2010__extra_botched_D5 | 39.0% |
| hclinton_tomorrow_2010__extra_botched_DISFLUENCY | 29.9% |
| hclinton_tomorrow_2010__extra_botched_ENDINGS | 3.8% |
| hclinton_tomorrow_2010__identity | 44.0% |
| hclinton_tomorrow_2010__single_L1A | 23.4% |
| hclinton_tomorrow_2010__single_L1B | 33.7% |
| hclinton_tomorrow_2010__single_L2A | 22.7% |
| hclinton_tomorrow_2010__single_L2B | 28.8% |
| hclinton_tomorrow_2010__single_L3A | 23.2% |
| hclinton_tomorrow_2010__single_L3B | 28.6% |
| lbush_radio_2001__G1 | 4.9% |
| lbush_radio_2001__G3 | 25.7% |
| lbush_radio_2001__G5 | 94.2% |
| lbush_radio_2001__extra_L1A | 22.4% |
| lbush_radio_2001__extra_L1B | 5.6% |
| lbush_radio_2001__extra_L1C | 8.7% |
| lbush_radio_2001__extra_L1D | 16.4% |
| lbush_radio_2001__extra_L2A | 22.5% |
| lbush_radio_2001__extra_L2B | 7.1% |
| lbush_radio_2001__extra_L2C | 10.1% |
| lbush_radio_2001__extra_L2D | 17.2% |
| lbush_radio_2001__extra_L3A | 22.5% |
| lbush_radio_2001__extra_L3B | 9.1% |
| lbush_radio_2001__extra_L3C | 11.5% |
| lbush_radio_2001__extra_L3D | 18.1% |
| lbush_radio_2001__extra_botched_CONTOUR | 70.9% |
| lbush_radio_2001__extra_botched_D1 | 32.0% |
| lbush_radio_2001__extra_botched_D2 | 35.4% |
| lbush_radio_2001__extra_botched_D4 | 2.1% |
| lbush_radio_2001__extra_botched_D5 | 28.7% |
| lbush_radio_2001__extra_botched_DISFLUENCY | 16.3% |
| lbush_radio_2001__extra_botched_ENDINGS | 2.3% |
| lbush_radio_2001__identity | 25.3% |
| lbush_radio_2001__single_L1A | 23.0% |
| lbush_radio_2001__single_L1B | 19.9% |
| lbush_radio_2001__single_L2A | 28.2% |
| lbush_radio_2001__single_L2B | 17.3% |
| lbush_radio_2001__single_L3A | 26.6% |
| lbush_radio_2001__single_L3B | 21.3% |
| mobama_weekly_2014__G1 | 9.6% |
| mobama_weekly_2014__G3 | 24.9% |
| mobama_weekly_2014__G5 | 94.2% |
| mobama_weekly_2014__extra_L1A | 20.8% |
| mobama_weekly_2014__extra_L1B | 4.5% |
| mobama_weekly_2014__extra_L1C | 14.7% |
| mobama_weekly_2014__extra_L1D | 27.5% |
| mobama_weekly_2014__extra_L2A | 20.7% |
| mobama_weekly_2014__extra_L2B | 8.1% |
| mobama_weekly_2014__extra_L2C | 16.6% |
| mobama_weekly_2014__extra_L2D | 29.8% |
| mobama_weekly_2014__extra_L3A | 20.6% |
| mobama_weekly_2014__extra_L3B | 10.4% |
| mobama_weekly_2014__extra_L3C | 18.5% |
| mobama_weekly_2014__extra_L3D | 32.2% |
| mobama_weekly_2014__extra_botched_CONTOUR | 35.1% |
| mobama_weekly_2014__extra_botched_D1 | 44.8% |
| mobama_weekly_2014__extra_botched_D2 | 37.4% |
| mobama_weekly_2014__extra_botched_D4 | 3.7% |
| mobama_weekly_2014__extra_botched_D5 | 27.0% |
| mobama_weekly_2014__extra_botched_DISFLUENCY | 25.5% |
| mobama_weekly_2014__extra_botched_ENDINGS | 3.4% |
| mobama_weekly_2014__identity | 28.6% |
| mobama_weekly_2014__single_L1A | 22.8% |
| mobama_weekly_2014__single_L1B | 18.3% |
| mobama_weekly_2014__single_L2A | 15.7% |
| mobama_weekly_2014__single_L2B | 14.8% |
| mobama_weekly_2014__single_L3A | 16.3% |
| mobama_weekly_2014__single_L3B | 23.2% |
| nixon_resignation_1974__G1 | 10.9% |
| nixon_resignation_1974__G3 | 18.9% |
| nixon_resignation_1974__G5 | 91.8% |
| nixon_resignation_1974__extra_L1A | 21.4% |
| nixon_resignation_1974__extra_L1B | 6.6% |
| nixon_resignation_1974__extra_L1C | 12.7% |
| nixon_resignation_1974__extra_L1D | 23.0% |
| nixon_resignation_1974__extra_L2A | 19.9% |
| nixon_resignation_1974__extra_L2B | 8.2% |
| nixon_resignation_1974__extra_L2C | 14.7% |
| nixon_resignation_1974__extra_L2D | 25.3% |
| nixon_resignation_1974__extra_L3A | 18.2% |
| nixon_resignation_1974__extra_L3B | 10.3% |
| nixon_resignation_1974__extra_L3C | 16.6% |
| nixon_resignation_1974__extra_L3D | 27.7% |
| nixon_resignation_1974__extra_botched_CONTOUR | 41.4% |
| nixon_resignation_1974__extra_botched_D1 | 28.8% |
| nixon_resignation_1974__extra_botched_D2 | 37.2% |
| nixon_resignation_1974__extra_botched_D4 | 4.5% |
| nixon_resignation_1974__extra_botched_D5 | 31.9% |
| nixon_resignation_1974__extra_botched_DISFLUENCY | 24.9% |
| nixon_resignation_1974__extra_botched_ENDINGS | 2.7% |
| nixon_resignation_1974__identity | 31.7% |
| nixon_resignation_1974__single_L1A | 20.1% |
| nixon_resignation_1974__single_L1B | 24.9% |
| nixon_resignation_1974__single_L2A | 22.0% |
| nixon_resignation_1974__single_L2B | 25.3% |
| nixon_resignation_1974__single_L3A | 21.5% |
| nixon_resignation_1974__single_L3B | 33.9% |
| obama_weekly_2009__G1 | 8.4% |
| obama_weekly_2009__G3 | 33.5% |
| obama_weekly_2009__G5 | 92.1% |
| obama_weekly_2009__extra_L1A | 20.2% |
| obama_weekly_2009__extra_L1B | 7.2% |
| obama_weekly_2009__extra_L1C | 12.2% |
| obama_weekly_2009__extra_L1D | 22.5% |
| obama_weekly_2009__extra_L2A | 20.1% |
| obama_weekly_2009__extra_L2B | 9.5% |
| obama_weekly_2009__extra_L2C | 14.3% |
| obama_weekly_2009__extra_L2D | 26.0% |
| obama_weekly_2009__extra_L3A | 19.9% |
| obama_weekly_2009__extra_L3B | 12.4% |
| obama_weekly_2009__extra_L3C | 16.3% |
| obama_weekly_2009__extra_L3D | 29.4% |
| obama_weekly_2009__extra_botched_CONTOUR | 3.3% |
| obama_weekly_2009__extra_botched_D1 | 62.8% |
| obama_weekly_2009__extra_botched_D2 | 31.8% |
| obama_weekly_2009__extra_botched_D4 | 5.7% |
| obama_weekly_2009__extra_botched_D5 | 36.0% |
| obama_weekly_2009__extra_botched_DISFLUENCY | 20.5% |
| obama_weekly_2009__extra_botched_ENDINGS | 1.3% |
| obama_weekly_2009__identity | 36.4% |
| obama_weekly_2009__single_L1A | 29.5% |
| obama_weekly_2009__single_L1B | 27.8% |
| obama_weekly_2009__single_L2A | 23.9% |
| obama_weekly_2009__single_L2B | 19.8% |
| obama_weekly_2009__single_L3A | 26.6% |
| obama_weekly_2009__single_L3B | 36.6% |
| reagan_farewell_1989__G1 | 4.1% |
| reagan_farewell_1989__G3 | 18.8% |
| reagan_farewell_1989__G5 | 94.0% |
| reagan_farewell_1989__extra_L1A | 11.7% |
| reagan_farewell_1989__extra_L1B | 5.4% |
| reagan_farewell_1989__extra_L1C | 9.9% |
| reagan_farewell_1989__extra_L1D | 31.5% |
| reagan_farewell_1989__extra_L2A | 11.9% |
| reagan_farewell_1989__extra_L2B | 7.0% |
| reagan_farewell_1989__extra_L2C | 11.5% |
| reagan_farewell_1989__extra_L2D | 32.2% |
| reagan_farewell_1989__extra_L3A | 12.1% |
| reagan_farewell_1989__extra_L3B | 9.1% |
| reagan_farewell_1989__extra_L3C | 13.1% |
| reagan_farewell_1989__extra_L3D | 32.9% |
| reagan_farewell_1989__extra_botched_CONTOUR | 43.8% |
| reagan_farewell_1989__extra_botched_D1 | 42.5% |
| reagan_farewell_1989__extra_botched_D2 | 34.3% |
| reagan_farewell_1989__extra_botched_D4 | 3.2% |
| reagan_farewell_1989__extra_botched_D5 | 22.0% |
| reagan_farewell_1989__extra_botched_DISFLUENCY | 16.2% |
| reagan_farewell_1989__extra_botched_ENDINGS | 3.6% |
| reagan_farewell_1989__identity | 27.0% |
| reagan_farewell_1989__single_L1A | 16.3% |
| reagan_farewell_1989__single_L1B | 13.3% |
| reagan_farewell_1989__single_L2A | 17.1% |
| reagan_farewell_1989__single_L2B | 19.4% |
| reagan_farewell_1989__single_L3A | 20.5% |
| reagan_farewell_1989__single_L3B | 22.0% |

| type | family / primary | secondary | event |
|---|---|---|---|
| RUSH | D1 | D4 | span |
| DRAG | D1 | D2, D4, D6, D7 | span |
| PAUSE_DROPPED | D2 | D1 | boundary |
| PAUSE_INTRUSIVE | D2 | D1 | boundary |
| MONOTONE | D3 | D4, D8 | span |
| DEEMPHASIS | D4 | D1, D3, D5 | word |
| FADE | D5 | D4 | span |
| MUMBLE | D6 |  | span |
| NATURAL_RUSH | D1 | D2, D4 | span |
| HESITATION | D2 | D1, D4, D7 | word |
| WORD_BY_WORD | D2 | D1 | span |
| UNEVEN_TEMPO | D1 | D4, D6, D7 | clip |
| WORD_REPETITION | DISFLUENCY | D1, D2 | word |
| SOUND_REPETITION | DISFLUENCY | D1, D2, D6 | word |
| RHYME_PROLONGATION | DISFLUENCY | D1, D4 | word |
| ONSET_PROLONGATION | DISFLUENCY | D1, D6 | word |
| BLOCK | DISFLUENCY | D1, D2, D6 | word |
| LOW_EFFORT | D5 | D3, D4, D6 | span |
| TRAILING_OFF | D5 | D4, D6 | span |
| MISPLACED_EMPHASIS | D4 | D1, D3, D5, D7 | span |
| RISING_ENDING | ENDINGS | D3, D4 | word |
| FLAT_FINAL_FALL | ENDINGS | D3, D4 | word |
| REPEATED_CONTOUR | CONTOUR | D4 | span |

| split | type | L1 | L2 | L3 |
|---|---|---|---|---|
| calibration | RUSH | 0 | 0 | 0 |
| calibration | DRAG | 0 | 0 | 0 |
| calibration | PAUSE_DROPPED | 0 | 0 | 0 |
| calibration | PAUSE_INTRUSIVE | 0 | 0 | 0 |
| calibration | MONOTONE | 0 | 0 | 0 |
| calibration | DEEMPHASIS | 0 | 0 | 0 |
| calibration | FADE | 0 | 0 | 0 |
| calibration | MUMBLE | 0 | 0 | 0 |
| calibration | NATURAL_RUSH | 0 | 6 | 18 |
| calibration | HESITATION | 0 | 6 | 18 |
| calibration | WORD_BY_WORD | 0 | 6 | 16 |
| calibration | UNEVEN_TEMPO | 0 | 6 | 18 |
| calibration | WORD_REPETITION | 0 | 6 | 18 |
| calibration | SOUND_REPETITION | 0 | 6 | 18 |
| calibration | RHYME_PROLONGATION | 0 | 6 | 18 |
| calibration | ONSET_PROLONGATION | 0 | 6 | 18 |
| calibration | BLOCK | 0 | 6 | 17 |
| calibration | LOW_EFFORT | 0 | 6 | 18 |
| calibration | TRAILING_OFF | 0 | 6 | 18 |
| calibration | MISPLACED_EMPHASIS | 0 | 0 | 7 |
| calibration | RISING_ENDING | 0 | 0 | 18 |
| calibration | FLAT_FINAL_FALL | 0 | 0 | 16 |
| calibration | REPEATED_CONTOUR | 0 | 0 | 18 |
| check | RUSH | 0 | 3 | 6 |
| check | DRAG | 0 | 0 | 3 |
| check | PAUSE_DROPPED | 0 | 3 | 17 |
| check | PAUSE_INTRUSIVE | 0 | 0 | 3 |
| check | MONOTONE | 0 | 0 | 6 |
| check | DEEMPHASIS | 0 | 0 | 0 |
| check | FADE | 0 | 0 | 9 |
| check | MUMBLE | 0 | 0 | 0 |
| check | NATURAL_RUSH | 0 | 3 | 6 |
| check | HESITATION | 0 | 3 | 9 |
| check | WORD_BY_WORD | 0 | 3 | 8 |
| check | UNEVEN_TEMPO | 0 | 3 | 9 |
| check | WORD_REPETITION | 0 | 3 | 9 |
| check | SOUND_REPETITION | 0 | 3 | 9 |
| check | RHYME_PROLONGATION | 0 | 3 | 9 |
| check | ONSET_PROLONGATION | 0 | 3 | 9 |
| check | BLOCK | 0 | 3 | 7 |
| check | LOW_EFFORT | 0 | 3 | 9 |
| check | TRAILING_OFF | 0 | 3 | 9 |
| check | MISPLACED_EMPHASIS | 0 | 0 | 6 |
| check | RISING_ENDING | 0 | 0 | 9 |
| check | FLAT_FINAL_FALL | 0 | 0 | 9 |
| check | REPEATED_CONTOUR | 0 | 0 | 9 |
| test | RUSH | 4 | 4 | 4 |
| test | DRAG | 2 | 2 | 2 |
| test | PAUSE_DROPPED | 2 | 2 | 15 |
| test | PAUSE_INTRUSIVE | 2 | 2 | 2 |
| test | MONOTONE | 2 | 4 | 4 |
| test | DEEMPHASIS | 2 | 2 | 2 |
| test | FADE | 2 | 4 | 6 |
| test | MUMBLE | 2 | 2 | 2 |
| test | NATURAL_RUSH | 2 | 2 | 5 |
| test | HESITATION | 2 | 2 | 6 |
| test | WORD_BY_WORD | 2 | 2 | 6 |
| test | UNEVEN_TEMPO | 2 | 2 | 6 |
| test | WORD_REPETITION | 2 | 2 | 6 |
| test | SOUND_REPETITION | 2 | 2 | 6 |
| test | RHYME_PROLONGATION | 2 | 2 | 6 |
| test | ONSET_PROLONGATION | 2 | 2 | 6 |
| test | BLOCK | 2 | 2 | 6 |
| test | LOW_EFFORT | 2 | 2 | 6 |
| test | TRAILING_OFF | 2 | 2 | 6 |
| test | MISPLACED_EMPHASIS | 1 | 2 | 6 |
| test | RISING_ENDING | 2 | 2 | 6 |
| test | FLAT_FINAL_FALL | 2 | 2 | 5 |
| test | REPEATED_CONTOUR | 2 | 2 | 6 |
| train | RUSH | 10 | 11 | 12 |
| train | DRAG | 5 | 5 | 6 |
| train | PAUSE_DROPPED | 5 | 6 | 41 |
| train | PAUSE_INTRUSIVE | 5 | 5 | 6 |
| train | MONOTONE | 5 | 10 | 12 |
| train | DEEMPHASIS | 5 | 5 | 5 |
| train | FADE | 5 | 10 | 18 |
| train | MUMBLE | 5 | 5 | 5 |
| train | NATURAL_RUSH | 5 | 6 | 17 |
| train | HESITATION | 5 | 6 | 18 |
| train | WORD_BY_WORD | 5 | 6 | 12 |
| train | UNEVEN_TEMPO | 5 | 6 | 16 |
| train | WORD_REPETITION | 5 | 6 | 18 |
| train | SOUND_REPETITION | 5 | 6 | 18 |
| train | RHYME_PROLONGATION | 5 | 6 | 18 |
| train | ONSET_PROLONGATION | 5 | 6 | 18 |
| train | BLOCK | 4 | 5 | 11 |
| train | LOW_EFFORT | 5 | 6 | 18 |
| train | TRAILING_OFF | 5 | 6 | 17 |
| train | MISPLACED_EMPHASIS | 4 | 4 | 18 |
| train | RISING_ENDING | 5 | 5 | 17 |
| train | FLAT_FINAL_FALL | 5 | 5 | 15 |
| train | REPEATED_CONTOUR | 5 | 5 | 17 |
| val | RUSH | 4 | 4 | 4 |
| val | DRAG | 2 | 2 | 2 |
| val | PAUSE_DROPPED | 2 | 2 | 13 |
| val | PAUSE_INTRUSIVE | 2 | 2 | 2 |
| val | MONOTONE | 2 | 4 | 4 |
| val | DEEMPHASIS | 2 | 2 | 2 |
| val | FADE | 2 | 4 | 6 |
| val | MUMBLE | 2 | 2 | 2 |
| val | NATURAL_RUSH | 2 | 2 | 6 |
| val | HESITATION | 2 | 2 | 6 |
| val | WORD_BY_WORD | 2 | 2 | 6 |
| val | UNEVEN_TEMPO | 2 | 2 | 4 |
| val | WORD_REPETITION | 2 | 2 | 6 |
| val | SOUND_REPETITION | 2 | 2 | 6 |
| val | RHYME_PROLONGATION | 2 | 2 | 6 |
| val | ONSET_PROLONGATION | 2 | 2 | 6 |
| val | BLOCK | 1 | 1 | 3 |
| val | LOW_EFFORT | 2 | 2 | 6 |
| val | TRAILING_OFF | 2 | 2 | 6 |
| val | MISPLACED_EMPHASIS | 2 | 2 | 5 |
| val | RISING_ENDING | 2 | 2 | 5 |
| val | FLAT_FINAL_FALL | 2 | 2 | 3 |
| val | REPEATED_CONTOUR | 1 | 1 | 4 |

| split | clips | minutes | extra clips | extra minutes |
|---|---|---|---|---|
| calibration | 99 | 47.24 | 99 | 47.24 |
| check | 66 | 28.96 | 51 | 23.22 |
| test | 58 | 28.82 | 38 | 19.56 |
| train | 167 | 77.22 | 112 | 53.69 |
| val | 58 | 28.86 | 38 | 19.49 |

| null group | fit | select | lockbox | minutes |
|---|---|---|---|---|
| accent:d12f66c99b9417ed | 394 | 193 | 192 | 329.16 |
| ears:3825fab09f9edeb6 | 53 | 54 | 0 | 28.69 |
| ears:4428cc3c1705cb4c | 53 | 54 | 0 | 22.45 |
| ears:66c54084bf880e57 | 53 | 54 | 0 | 26.77 |
| ears:7ba92d3759e56588 | 53 | 54 | 0 | 19.29 |
| ears:897beef0d37ff06f | 53 | 54 | 0 | 24.61 |
| ears:a884d4498ff32795 | 53 | 54 | 0 | 32.55 |
| ears:bf98be6a09cee920 | 53 | 54 | 0 | 36.87 |
| ears:fb5cb9991c4066e2 | 53 | 54 | 0 | 30.31 |
| gettysburg:85cfe5e6a2f096f8 | 10 | 9 | 0 | 38.28 |
| poetry:0b9245cdebfbf44c | 8 | 3 | 3 | 9.37 |
| poetry:0c2aeee5f58847a1 | 8 | 5 | 0 | 14.35 |
| poetry:16bd8225a7d9f6bc | 9 | 2 | 0 | 18.59 |
| poetry:17429495b4b38264 | 0 | 0 | 6 | 4.57 |
| poetry:26ac2c806c74bd5f | 7 | 4 | 7 | 29.80 |
| poetry:271fb6118cf32610 | 10 | 5 | 0 | 16.82 |
| poetry:2aca1e8164c5dd58 | 6 | 3 | 1 | 9.57 |
| poetry:2e70971ef8318cce | 7 | 1 | 5 | 20.01 |
| poetry:38099e0a312c2f84 | 9 | 5 | 6 | 4.63 |
| poetry:3ab30b14a30a7fd9 | 10 | 4 | 0 | 16.21 |
| poetry:46d7cd4d473a03b7 | 8 | 4 | 4 | 15.90 |
| poetry:49d6bc9aab15e8b4 | 6 | 3 | 5 | 12.38 |
| poetry:655860d7c2f83223 | 7 | 4 | 14 | 36.43 |
| poetry:876e061a7c1a83e4 | 6 | 5 | 1 | 16.70 |
| poetry:996e6cc206ede6ad | 11 | 5 | 0 | 14.95 |
| poetry:ae5bc544ccfd8515 | 7 | 3 | 2 | 18.97 |
| poetry:c85bc3544d7a893b | 8 | 3 | 2 | 12.67 |
| poetry:d297216899a03cfd | 10 | 5 | 0 | 8.23 |
| poetry:db44753104f4c80d | 10 | 5 | 3 | 11.60 |
| poetry:ebd0ee76249157cf | 10 | 4 | 0 | 8.60 |

R2 partition SHA-256: 50d5c5c563915580b110d9feb69ef87b5e772d6dde4efbc1b4225490c47de3c9
LibriVox poetry/Gettysburg only: outer passage anchors, overall coverage, require_match, first/last word +/- CLIP_PAD_S; EARS/Accent/VCTK whole; lockbox deferred
Gettysburg v10 required every sentence endpoint in greedy ASR. The CPU replay of all 19 readers failed this rule despite 89.7–97.4% overall coverage; FOUR was unanchored in 16, EARTH in 15, and the can-not clause failed in 19. The null crop now uses outer passage anchors and overall coverage, then checks alignment.
EARS readers were seen by the lab and have no lockbox; lockbox source coverage differs from fit. No missing source is assigned a zero false rate. Lockbox preparation is deferred.

| excluded null reading | reason |
|---|---|
| null_06159cc21f28e791 | text not located: outer passage anchors or overall coverage below criterion |
| null_c00f94db26340a4c | text not located: outer passage anchors or overall coverage below criterion |
| null_9637a087ce25f7c8 | text not located: outer passage anchors or overall coverage below criterion |
| null_50b27c0cdaec3363 | text not located: outer passage anchors or overall coverage below criterion |
| null_aaa90f77c77d7b4e | text not located: outer passage anchors or overall coverage below criterion |
| null_7664bf146aaf6f9a | text not located: outer passage anchors or overall coverage below criterion |
| null_42cfcbce9fdd7050 | text not located: outer passage anchors or overall coverage below criterion |
| null_4a7e009b83ba5058 | text not located: outer passage anchors or overall coverage below criterion |
| null_dafc4385bac48a29 | text not located: outer passage anchors or overall coverage below criterion |
| null_550a2b54ab9e5dd1 | text not located: outer passage anchors or overall coverage below criterion |
| null_da44b12085098ef6 | text not located: outer passage anchors or overall coverage below criterion |
| null_675f9ec92eb7963f | text not located: outer passage anchors or overall coverage below criterion |
| null_5573896e8aab6378 | text not located: outer passage anchors or overall coverage below criterion |
| null_680759802dab1d7f | text not located: outer passage anchors or overall coverage below criterion |
| null_086f479785f6ac0f | text not located: outer passage anchors or overall coverage below criterion |
| null_86410b8e87f369de | text not located: outer passage anchors or overall coverage below criterion |
| null_6a2075f790214dff | text not located: outer passage anchors or overall coverage below criterion |
| null_60b9957a24d48667 | text not located: outer passage anchors or overall coverage below criterion |
| null_4fb2d179d523eed9 | text not located: outer passage anchors or overall coverage below criterion |
| null_bc9d12c5fb9f6fc0 | text not located: outer passage anchors or overall coverage below criterion |
| null_e0b5e93daa745d4b | text not located: outer passage anchors or overall coverage below criterion |
| null_13124b63bae9e8d7 | text not located: outer passage anchors or overall coverage below criterion |
| null_9cc0d8090c782a68 | text not located: outer passage anchors or overall coverage below criterion |
| null_a7672977e2ab2ca7 | text not located: outer passage anchors or overall coverage below criterion |
| null_229e16f98c39e44e | text not located: outer passage anchors or overall coverage below criterion |
| null_7162bf5a0bc90d6d | text not located: outer passage anchors or overall coverage below criterion |
| null_ddc27a24c483e33c | text not located: outer passage anchors or overall coverage below criterion |
| null_ff8070defaf5e375 | text not located: outer passage anchors or overall coverage below criterion |
| null_2a25d14b7e27a52d | text not located: outer passage anchors or overall coverage below criterion |
| null_67f626ddb5c86794 | text not located: outer passage anchors or overall coverage below criterion |
| null_f89fe7a46b2f7c46 | text not located: outer passage anchors or overall coverage below criterion |

Accent is stratified by first language and lab-seen status, with integer rounding per stratum. The Accent lockbox includes lab-seen readers to match composition; it is not an unseen-lab estimate.

| first language | lab seen | fit | select | lockbox |
|---|---|---|---|---|
| afrikaans | False | 3 | 1 | 1 |
| agni | False | 1 | 0 | 0 |
| akan | False | 1 | 0 | 0 |
| albanian | False | 5 | 2 | 2 |
| amazigh | False | 1 | 1 | 0 |
| amharic | False | 10 | 5 | 5 |
| arabic | False | 51 | 25 | 26 |
| armenian | False | 4 | 2 | 2 |
| ashanti | False | 1 | 0 | 0 |
| azerbaijani | False | 1 | 1 | 1 |
| bafang | False | 1 | 1 | 0 |
| baga | False | 1 | 0 | 0 |
| bai | False | 1 | 0 | 0 |
| bambara | False | 3 | 1 | 1 |
| bamun | False | 1 | 0 | 0 |
| bari | False | 1 | 0 | 1 |
| basque | False | 1 | 1 | 0 |
| bavarian | False | 1 | 0 | 1 |
| belarusan | False | 1 | 1 | 1 |
| bengali | False | 9 | 4 | 4 |
| bosnian | False | 5 | 2 | 2 |
| bulgarian | False | 1 | 1 | 1 |
| english | False | 37 | 19 | 18 |
| english | True | 253 | 126 | 126 |

| source | fit/select attempted | excluded | exclusion rate | reasons / rule |
|---|---|---|---|---|
| accent | 587 | 0 | 0.0% | {}; whole passage; no text-location exclusion |
| ears | 856 | 0 | 0.0% | {}; whole passage; no text-location exclusion |
| gettysburg | 19 | 0 | 0.0% | {}; spoken introductions/closings removed; failed anchors or alignment are recorded |
| poetry | 261 | 31 | 11.9% | {'text not located: outer passage anchors or overall coverage below criterion': 31}; spoken introductions/closings removed; failed anchors or alignment are recorded |

Inventory exclusions (before fit/select crop; separate denominator):
| source | inventoried readings | inventory exclusions | rate | reasons |
|---|---|---|---|---|
| accent | 779 | 0 | 0.0% | {} |
| ears | 856 | 0 | 0.0% | {} |
| gettysburg | 19 | 0 | 0.0% | {} |
| poetry | 320 | 0 | 0.0% | {} |

Missing independent prompts: []

Sources: build/work/research/chain/{pace_pauses,disfluency,pitch_emphasis,volume_clarity}/REPORT.md §4; SYNTHESIS.md §4; alpha coupling from volume_clarity §2.1. Numeric signal gates, jitter, fit tolerances and release are engineering choices.

| extra type | family / primary | L1 / L2 / L3 named parameters (s, dB, st, factors) | source / chosen values | approximation / omissions |
|---|---|---|---|---|
| NATURAL_RUSH | D1 / D9 | speech_rate=1.13, pause_kept_fraction=0.6 / speech_rate=1.15, pause_kept_fraction=0.3 / speech_rate=1.18, pause_kept_fraction=0 | pace_pauses §1/§4: rate 13–18%; pause fractions chosen | uniform word compression omits selective unstressed/vowel shortening; short unclassified gaps unchanged |
| HESITATION | D2 / D2 | word_duration_factor=1.2, silence_s=0.2 / word_duration_factor=1.5, silence_s=0.5 / word_duration_factor=1.8, silence_s=1 | pace_pauses §4: silence 0.2–1 s; stretch factors chosen | content word; 30 ms non-pausal gap energy minimum; no retrieval physiology |
| WORD_BY_WORD | D2 / D2 | silence_s=0.15, every_words=1 / silence_s=0.225, every_words=1 / silence_s=0.3, every_words=1 | pace_pauses §4: silence 0.15–0.3 s | internal eligible gaps only; L1 may be below 200 ms pause threshold |
| UNEVEN_TEMPO | D1 / D7 | max_duration_deviation=0.15 / max_duration_deviation=0.3 / max_duration_deviation=0.45 | pace_pauses §4: mean-one factors; deviation chosen | nominal mean one; integer rounding; no syllable rhythm model |
| WORD_REPETITION | DISFLUENCY / D7 | first_token_duration_factor=1.3, silence_s=0.1, inserted_copies=1 / first_token_duration_factor=1.6, silence_s=0.225, inserted_copies=1 / first_token_duration_factor=1.9, silence_s=0.35, inserted_copies=1 | disfluency §2.2/§4: first token lengthened; factors chosen; gap 100–350 ms | function-word copy; duration ±8% and gain ±1 dB chosen; no tension/F0 variation |
| SOUND_REPETITION | DISFLUENCY / D7 | inserted_copies=2, silence_s=0.1 / inserted_copies=3, silence_s=0.1 / inserted_copies=4, silence_s=0.1 | disfluency §2.1/§4: 2–5 copies; gap 100–350 ms | first 20% onset copy; stress fallback recorded; no tension; duration/level variation chosen |
| RHYME_PROLONGATION | DISFLUENCY / D7 | added_duration_s=0.18 / added_duration_s=0.36 / added_duration_s=0.54 | disfluency §4: phones 2–4x, WSOLA 5–10x; added seconds chosen above 89 ms error | voiced stable edge run ≥90 ms; actual pause context recorded; no phone identity; unvoiced continuants omitted |
| ONSET_PROLONGATION | DISFLUENCY / D7 | onset_target_s=0.35 / onset_target_s=0.65 / onset_target_s=1 | disfluency §2.1/§4: up to about 1 s; 2–10x bound; targets chosen | 100 ms voiced stable onset run; stress fallback; unvoiced continuants omitted |
| BLOCK | DISFLUENCY / D7 | silence_s=0.5 / silence_s=1.25 / silence_s=2 | disfluency §2.1/§4: gap 0.5–2 s | signal closure-to-burst energy/flux rise within 80 ms; no tense closure or enhanced burst |
| LOW_EFFORT | D5 / D5 | attenuation_db=3, alpha_drop_per_db=0.55, pitch_lowering_st=0.5 / attenuation_db=6, alpha_drop_per_db=0.55, pitch_lowering_st=1 / attenuation_db=9, alpha_drop_per_db=0.55, pitch_lowering_st=1.5 | volume_clarity §2.1/§4: alpha/level 0.4–0.7; 0.55 chosen; gain and F0 shift chosen | tilt fitted after room mixing on parent voiced speech above floor; source/formants/vowel duration omitted; 5 Hz/dB not established for sentences |
| TRAILING_OFF | D5 / D5 | final_attenuation_db=4, alpha_drop_per_db=0.55 / final_attenuation_db=8, alpha_drop_per_db=0.55 / final_attenuation_db=12, alpha_drop_per_db=0.55 | volume_clarity §2.2/§4: end-word gain/tilt ramp; magnitudes chosen | last three words; 100 ms release; tilt fitted after mixing; lax/irregular phonation omitted |
| MISPLACED_EMPHASIS | D4 / D4 | function_duration_factor=1.1, function_pitch_st=2, function_gain_db=2, stressed_removal_strength=0.3 / function_duration_factor=1.2, function_pitch_st=4, function_gain_db=4, stressed_removal_strength=0.6 / function_duration_factor=1.3, function_pitch_st=6, function_gain_db=6, stressed_removal_strength=0.9 | pitch_emphasis §4: boost function word and remove stressed prominence; magnitudes chosen | stress/text prior; no accent dictionary; natural legitimate function-word accents not modelled |
| RISING_ENDING | ENDINGS / D8 | rise_st=2 / rise_st=4 / rise_st=6 | pitch_emphasis §4: last 200–300 ms; 250 ms and rises chosen | add ramp to natural contour; clipped to final word; PSOLA approximate; no syllable annotation |
| FLAT_FINAL_FALL | ENDINGS / D8 | strength=0.333333 / strength=0.666667 / strength=1 | pitch_emphasis §4: preceding-word target; strengths chosen | last 250 ms clipped to final word; preceding median; PSOLA approximate |
| REPEATED_CONTOUR | CONTOUR / NO_DETECTOR | contour_strength=0.333333 / contour_strength=0.666667 / contour_strength=1 | pitch_emphasis §4: time-normalised sentence contour; strengths chosen | template/target ≥0.5 s chosen; linear time warp; interpolate across unvoiced template gaps; no syntactic matching |

Placement counts include extra family botched instances. Empty cells are retained.
| regime | split | type | level | planned | placed | skipped by reason | placement Wilson 95% |
|---|---|---|---|---|---|---|---|
| R1 | test | NATURAL_RUSH | 1 | 2 | 2 | {} | 0.342–1.000 |
| R1 | test | NATURAL_RUSH | 2 | 2 | 2 | {} | 0.342–1.000 |
| R1 | test | NATURAL_RUSH | 3 | 6 | 5 | {'no eligible disjoint botched placement': 1} | 0.436–0.970 |
| R1 | test | HESITATION | 1 | 2 | 2 | {} | 0.342–1.000 |
| R1 | test | HESITATION | 2 | 2 | 2 | {} | 0.342–1.000 |
| R1 | test | HESITATION | 3 | 6 | 6 | {} | 0.610–1.000 |
| R1 | test | WORD_BY_WORD | 1 | 2 | 2 | {} | 0.342–1.000 |
| R1 | test | WORD_BY_WORD | 2 | 2 | 2 | {} | 0.342–1.000 |
| R1 | test | WORD_BY_WORD | 3 | 6 | 6 | {} | 0.610–1.000 |
| R1 | test | UNEVEN_TEMPO | 1 | 2 | 2 | {} | 0.342–1.000 |
| R1 | test | UNEVEN_TEMPO | 2 | 2 | 2 | {} | 0.342–1.000 |
| R1 | test | UNEVEN_TEMPO | 3 | 6 | 6 | {} | 0.610–1.000 |
| R1 | test | WORD_REPETITION | 1 | 2 | 2 | {} | 0.342–1.000 |
| R1 | test | WORD_REPETITION | 2 | 2 | 2 | {} | 0.342–1.000 |
| R1 | test | WORD_REPETITION | 3 | 6 | 6 | {} | 0.610–1.000 |
| R1 | test | SOUND_REPETITION | 1 | 2 | 2 | {} | 0.342–1.000 |
| R1 | test | SOUND_REPETITION | 2 | 2 | 2 | {} | 0.342–1.000 |
| R1 | test | SOUND_REPETITION | 3 | 6 | 6 | {} | 0.610–1.000 |
| R1 | test | RHYME_PROLONGATION | 1 | 2 | 2 | {} | 0.342–1.000 |
| R1 | test | RHYME_PROLONGATION | 2 | 2 | 2 | {} | 0.342–1.000 |
| R1 | test | RHYME_PROLONGATION | 3 | 6 | 6 | {} | 0.610–1.000 |
| R1 | test | ONSET_PROLONGATION | 1 | 2 | 2 | {} | 0.342–1.000 |
| R1 | test | ONSET_PROLONGATION | 2 | 2 | 2 | {} | 0.342–1.000 |
| R1 | test | ONSET_PROLONGATION | 3 | 6 | 6 | {} | 0.610–1.000 |
| R1 | test | BLOCK | 1 | 2 | 2 | {} | 0.342–1.000 |
| R1 | test | BLOCK | 2 | 2 | 2 | {} | 0.342–1.000 |
| R1 | test | BLOCK | 3 | 6 | 6 | {} | 0.610–1.000 |
| R1 | test | LOW_EFFORT | 1 | 2 | 2 | {} | 0.342–1.000 |
| R1 | test | LOW_EFFORT | 2 | 2 | 2 | {} | 0.342–1.000 |
| R1 | test | LOW_EFFORT | 3 | 6 | 6 | {} | 0.610–1.000 |
| R1 | test | TRAILING_OFF | 1 | 2 | 2 | {} | 0.342–1.000 |
| R1 | test | TRAILING_OFF | 2 | 2 | 2 | {} | 0.342–1.000 |
| R1 | test | TRAILING_OFF | 3 | 6 | 6 | {} | 0.610–1.000 |
| R1 | test | MISPLACED_EMPHASIS | 1 | 2 | 1 | {'too few voiced frames to measure the recipe': 1} | 0.095–0.905 |
| R1 | test | MISPLACED_EMPHASIS | 2 | 2 | 2 | {} | 0.342–1.000 |
| R1 | test | MISPLACED_EMPHASIS | 3 | 6 | 6 | {} | 0.610–1.000 |
| R1 | test | RISING_ENDING | 1 | 2 | 2 | {} | 0.342–1.000 |
| R1 | test | RISING_ENDING | 2 | 2 | 2 | {} | 0.342–1.000 |
| R1 | test | RISING_ENDING | 3 | 6 | 6 | {} | 0.610–1.000 |
| R1 | test | FLAT_FINAL_FALL | 1 | 2 | 2 | {} | 0.342–1.000 |
| R1 | test | FLAT_FINAL_FALL | 2 | 2 | 2 | {} | 0.342–1.000 |
| R1 | test | FLAT_FINAL_FALL | 3 | 6 | 5 | {'no eligible disjoint botched placement': 1} | 0.436–0.970 |
| R1 | test | REPEATED_CONTOUR | 1 | 2 | 2 | {} | 0.342–1.000 |
| R1 | test | REPEATED_CONTOUR | 2 | 2 | 2 | {} | 0.342–1.000 |
| R1 | test | REPEATED_CONTOUR | 3 | 6 | 6 | {} | 0.610–1.000 |
| R1 | train | NATURAL_RUSH | 1 | 5 | 5 | {} | 0.566–1.000 |
| R1 | train | NATURAL_RUSH | 2 | 5 | 5 | {} | 0.566–1.000 |
| R1 | train | NATURAL_RUSH | 3 | 15 | 14 | {'no eligible disjoint botched placement': 1} | 0.702–0.988 |
| R1 | train | HESITATION | 1 | 5 | 5 | {} | 0.566–1.000 |
| R1 | train | HESITATION | 2 | 5 | 5 | {} | 0.566–1.000 |
| R1 | train | HESITATION | 3 | 15 | 15 | {} | 0.796–1.000 |
| R1 | train | WORD_BY_WORD | 1 | 5 | 5 | {} | 0.566–1.000 |
| R1 | train | WORD_BY_WORD | 2 | 5 | 5 | {} | 0.566–1.000 |
| R1 | train | WORD_BY_WORD | 3 | 15 | 9 | {'no eligible disjoint botched placement': 6} | 0.357–0.802 |
| R1 | train | UNEVEN_TEMPO | 1 | 5 | 5 | {} | 0.566–1.000 |
| R1 | train | UNEVEN_TEMPO | 2 | 5 | 5 | {} | 0.566–1.000 |
| R1 | train | UNEVEN_TEMPO | 3 | 15 | 13 | {'no eligible disjoint botched placement': 2} | 0.621–0.963 |
| R1 | train | WORD_REPETITION | 1 | 5 | 5 | {} | 0.566–1.000 |
| R1 | train | WORD_REPETITION | 2 | 5 | 5 | {} | 0.566–1.000 |
| R1 | train | WORD_REPETITION | 3 | 15 | 15 | {} | 0.796–1.000 |
| R1 | train | SOUND_REPETITION | 1 | 5 | 5 | {} | 0.566–1.000 |
| R1 | train | SOUND_REPETITION | 2 | 5 | 5 | {} | 0.566–1.000 |
| R1 | train | SOUND_REPETITION | 3 | 15 | 15 | {} | 0.796–1.000 |
| R1 | train | RHYME_PROLONGATION | 1 | 5 | 5 | {} | 0.566–1.000 |
| R1 | train | RHYME_PROLONGATION | 2 | 5 | 5 | {} | 0.566–1.000 |
| R1 | train | RHYME_PROLONGATION | 3 | 15 | 15 | {} | 0.796–1.000 |
| R1 | train | ONSET_PROLONGATION | 1 | 5 | 5 | {} | 0.566–1.000 |
| R1 | train | ONSET_PROLONGATION | 2 | 5 | 5 | {} | 0.566–1.000 |
| R1 | train | ONSET_PROLONGATION | 3 | 15 | 15 | {} | 0.796–1.000 |
| R1 | train | BLOCK | 1 | 5 | 4 | {'no eligible position': 1} | 0.376–0.964 |
| R1 | train | BLOCK | 2 | 5 | 4 | {'no eligible position': 1} | 0.376–0.964 |
| R1 | train | BLOCK | 3 | 15 | 10 | {'no eligible disjoint botched placement': 4, 'no eligible position': 1} | 0.417–0.848 |
| R1 | train | LOW_EFFORT | 1 | 5 | 5 | {} | 0.566–1.000 |
| R1 | train | LOW_EFFORT | 2 | 5 | 5 | {} | 0.566–1.000 |
| R1 | train | LOW_EFFORT | 3 | 15 | 15 | {} | 0.796–1.000 |
| R1 | train | TRAILING_OFF | 1 | 5 | 5 | {} | 0.566–1.000 |
| R1 | train | TRAILING_OFF | 2 | 5 | 5 | {} | 0.566–1.000 |
| R1 | train | TRAILING_OFF | 3 | 15 | 14 | {'no eligible disjoint botched placement': 1} | 0.702–0.988 |
| R1 | train | MISPLACED_EMPHASIS | 1 | 5 | 4 | {'too few voiced frames to measure the recipe': 1} | 0.376–0.964 |
| R1 | train | MISPLACED_EMPHASIS | 2 | 5 | 4 | {'too few voiced frames to measure the recipe': 1} | 0.376–0.964 |
| R1 | train | MISPLACED_EMPHASIS | 3 | 15 | 15 | {} | 0.796–1.000 |
| R1 | train | RISING_ENDING | 1 | 5 | 5 | {} | 0.566–1.000 |
| R1 | train | RISING_ENDING | 2 | 5 | 5 | {} | 0.566–1.000 |
| R1 | train | RISING_ENDING | 3 | 15 | 14 | {'no eligible disjoint botched placement': 1} | 0.702–0.988 |
| R1 | train | FLAT_FINAL_FALL | 1 | 5 | 5 | {} | 0.566–1.000 |
| R1 | train | FLAT_FINAL_FALL | 2 | 5 | 5 | {} | 0.566–1.000 |
| R1 | train | FLAT_FINAL_FALL | 3 | 15 | 12 | {'no eligible disjoint botched placement': 3} | 0.548–0.930 |
| R1 | train | REPEATED_CONTOUR | 1 | 5 | 5 | {} | 0.566–1.000 |
| R1 | train | REPEATED_CONTOUR | 2 | 5 | 5 | {} | 0.566–1.000 |
| R1 | train | REPEATED_CONTOUR | 3 | 15 | 14 | {'no eligible disjoint botched placement': 1} | 0.702–0.988 |
| R1 | val | NATURAL_RUSH | 1 | 2 | 2 | {} | 0.342–1.000 |
| R1 | val | NATURAL_RUSH | 2 | 2 | 2 | {} | 0.342–1.000 |
| R1 | val | NATURAL_RUSH | 3 | 6 | 6 | {} | 0.610–1.000 |
| R1 | val | HESITATION | 1 | 2 | 2 | {} | 0.342–1.000 |
| R1 | val | HESITATION | 2 | 2 | 2 | {} | 0.342–1.000 |
| R1 | val | HESITATION | 3 | 6 | 6 | {} | 0.610–1.000 |
| R1 | val | WORD_BY_WORD | 1 | 2 | 2 | {} | 0.342–1.000 |
| R1 | val | WORD_BY_WORD | 2 | 2 | 2 | {} | 0.342–1.000 |
| R1 | val | WORD_BY_WORD | 3 | 6 | 6 | {} | 0.610–1.000 |
| R1 | val | UNEVEN_TEMPO | 1 | 2 | 2 | {} | 0.342–1.000 |
| R1 | val | UNEVEN_TEMPO | 2 | 2 | 2 | {} | 0.342–1.000 |
| R1 | val | UNEVEN_TEMPO | 3 | 6 | 4 | {'no eligible disjoint botched placement': 2} | 0.300–0.903 |
| R1 | val | WORD_REPETITION | 1 | 2 | 2 | {} | 0.342–1.000 |
| R1 | val | WORD_REPETITION | 2 | 2 | 2 | {} | 0.342–1.000 |
| R1 | val | WORD_REPETITION | 3 | 6 | 6 | {} | 0.610–1.000 |
| R1 | val | SOUND_REPETITION | 1 | 2 | 2 | {} | 0.342–1.000 |
| R1 | val | SOUND_REPETITION | 2 | 2 | 2 | {} | 0.342–1.000 |
| R1 | val | SOUND_REPETITION | 3 | 6 | 6 | {} | 0.610–1.000 |
| R1 | val | RHYME_PROLONGATION | 1 | 2 | 2 | {} | 0.342–1.000 |
| R1 | val | RHYME_PROLONGATION | 2 | 2 | 2 | {} | 0.342–1.000 |
| R1 | val | RHYME_PROLONGATION | 3 | 6 | 6 | {} | 0.610–1.000 |
| R1 | val | ONSET_PROLONGATION | 1 | 2 | 2 | {} | 0.342–1.000 |
| R1 | val | ONSET_PROLONGATION | 2 | 2 | 2 | {} | 0.342–1.000 |
| R1 | val | ONSET_PROLONGATION | 3 | 6 | 6 | {} | 0.610–1.000 |
| R1 | val | BLOCK | 1 | 2 | 1 | {'no eligible position': 1} | 0.095–0.905 |
| R1 | val | BLOCK | 2 | 2 | 1 | {'no eligible position': 1} | 0.095–0.905 |
| R1 | val | BLOCK | 3 | 6 | 3 | {'no eligible position': 1, 'no eligible disjoint botched placement': 2} | 0.188–0.812 |
| R1 | val | LOW_EFFORT | 1 | 2 | 2 | {} | 0.342–1.000 |
| R1 | val | LOW_EFFORT | 2 | 2 | 2 | {} | 0.342–1.000 |
| R1 | val | LOW_EFFORT | 3 | 6 | 6 | {} | 0.610–1.000 |
| R1 | val | TRAILING_OFF | 1 | 2 | 2 | {} | 0.342–1.000 |
| R1 | val | TRAILING_OFF | 2 | 2 | 2 | {} | 0.342–1.000 |
| R1 | val | TRAILING_OFF | 3 | 6 | 6 | {} | 0.610–1.000 |
| R1 | val | MISPLACED_EMPHASIS | 1 | 2 | 2 | {} | 0.342–1.000 |
| R1 | val | MISPLACED_EMPHASIS | 2 | 2 | 2 | {} | 0.342–1.000 |
| R1 | val | MISPLACED_EMPHASIS | 3 | 6 | 5 | {'too few voiced frames to measure the recipe': 1} | 0.436–0.970 |
| R1 | val | RISING_ENDING | 1 | 2 | 2 | {} | 0.342–1.000 |
| R1 | val | RISING_ENDING | 2 | 2 | 2 | {} | 0.342–1.000 |
| R1 | val | RISING_ENDING | 3 | 6 | 5 | {'no eligible disjoint botched placement': 1} | 0.436–0.970 |
| R1 | val | FLAT_FINAL_FALL | 1 | 2 | 2 | {} | 0.342–1.000 |
| R1 | val | FLAT_FINAL_FALL | 2 | 2 | 2 | {} | 0.342–1.000 |
| R1 | val | FLAT_FINAL_FALL | 3 | 6 | 3 | {'no eligible disjoint botched placement': 3} | 0.188–0.812 |
| R1 | val | REPEATED_CONTOUR | 1 | 2 | 1 | {'no eligible position': 1} | 0.095–0.905 |
| R1 | val | REPEATED_CONTOUR | 2 | 2 | 1 | {'no eligible position': 1} | 0.095–0.905 |
| R1 | val | REPEATED_CONTOUR | 3 | 6 | 4 | {'no eligible position': 1, 'no eligible disjoint botched placement': 1} | 0.300–0.903 |
| R2 | calibration | NATURAL_RUSH | 1 | 0 | 0 | {} | unplanned |
| R2 | calibration | NATURAL_RUSH | 2 | 6 | 6 | {} | 0.610–1.000 |
| R2 | calibration | NATURAL_RUSH | 3 | 18 | 18 | {} | 0.824–1.000 |
| R2 | calibration | HESITATION | 1 | 0 | 0 | {} | unplanned |
| R2 | calibration | HESITATION | 2 | 6 | 6 | {} | 0.610–1.000 |
| R2 | calibration | HESITATION | 3 | 18 | 18 | {} | 0.824–1.000 |
| R2 | calibration | WORD_BY_WORD | 1 | 0 | 0 | {} | unplanned |
| R2 | calibration | WORD_BY_WORD | 2 | 6 | 6 | {} | 0.610–1.000 |
| R2 | calibration | WORD_BY_WORD | 3 | 18 | 16 | {'no eligible disjoint botched placement': 2} | 0.672–0.969 |
| R2 | calibration | UNEVEN_TEMPO | 1 | 0 | 0 | {} | unplanned |
| R2 | calibration | UNEVEN_TEMPO | 2 | 6 | 6 | {} | 0.610–1.000 |
| R2 | calibration | UNEVEN_TEMPO | 3 | 18 | 18 | {} | 0.824–1.000 |
| R2 | calibration | WORD_REPETITION | 1 | 0 | 0 | {} | unplanned |
| R2 | calibration | WORD_REPETITION | 2 | 6 | 6 | {} | 0.610–1.000 |
| R2 | calibration | WORD_REPETITION | 3 | 18 | 18 | {} | 0.824–1.000 |
| R2 | calibration | SOUND_REPETITION | 1 | 0 | 0 | {} | unplanned |
| R2 | calibration | SOUND_REPETITION | 2 | 6 | 6 | {} | 0.610–1.000 |
| R2 | calibration | SOUND_REPETITION | 3 | 18 | 18 | {} | 0.824–1.000 |
| R2 | calibration | RHYME_PROLONGATION | 1 | 0 | 0 | {} | unplanned |
| R2 | calibration | RHYME_PROLONGATION | 2 | 6 | 6 | {} | 0.610–1.000 |
| R2 | calibration | RHYME_PROLONGATION | 3 | 18 | 18 | {} | 0.824–1.000 |
| R2 | calibration | ONSET_PROLONGATION | 1 | 0 | 0 | {} | unplanned |
| R2 | calibration | ONSET_PROLONGATION | 2 | 6 | 6 | {} | 0.610–1.000 |
| R2 | calibration | ONSET_PROLONGATION | 3 | 18 | 18 | {} | 0.824–1.000 |
| R2 | calibration | BLOCK | 1 | 0 | 0 | {} | unplanned |
| R2 | calibration | BLOCK | 2 | 6 | 6 | {} | 0.610–1.000 |
| R2 | calibration | BLOCK | 3 | 18 | 17 | {'no eligible disjoint botched placement': 1} | 0.742–0.990 |
| R2 | calibration | LOW_EFFORT | 1 | 0 | 0 | {} | unplanned |
| R2 | calibration | LOW_EFFORT | 2 | 6 | 6 | {} | 0.610–1.000 |
| R2 | calibration | LOW_EFFORT | 3 | 18 | 18 | {} | 0.824–1.000 |
| R2 | calibration | TRAILING_OFF | 1 | 0 | 0 | {} | unplanned |
| R2 | calibration | TRAILING_OFF | 2 | 6 | 6 | {} | 0.610–1.000 |
| R2 | calibration | TRAILING_OFF | 3 | 18 | 18 | {} | 0.824–1.000 |
| R2 | calibration | MISPLACED_EMPHASIS | 1 | 0 | 0 | {} | unplanned |
| R2 | calibration | MISPLACED_EMPHASIS | 2 | 0 | 0 | {} | unplanned |
| R2 | calibration | MISPLACED_EMPHASIS | 3 | 18 | 7 | {'no eligible position': 3, 'no eligible disjoint botched placement': 8} | 0.203–0.614 |
| R2 | calibration | RISING_ENDING | 1 | 0 | 0 | {} | unplanned |
| R2 | calibration | RISING_ENDING | 2 | 0 | 0 | {} | unplanned |
| R2 | calibration | RISING_ENDING | 3 | 18 | 18 | {} | 0.824–1.000 |
| R2 | calibration | FLAT_FINAL_FALL | 1 | 0 | 0 | {} | unplanned |
| R2 | calibration | FLAT_FINAL_FALL | 2 | 0 | 0 | {} | unplanned |
| R2 | calibration | FLAT_FINAL_FALL | 3 | 18 | 16 | {'no eligible disjoint botched placement': 2} | 0.672–0.969 |
| R2 | calibration | REPEATED_CONTOUR | 1 | 0 | 0 | {} | unplanned |
| R2 | calibration | REPEATED_CONTOUR | 2 | 0 | 0 | {} | unplanned |
| R2 | calibration | REPEATED_CONTOUR | 3 | 18 | 18 | {} | 0.824–1.000 |
| R2 | check | NATURAL_RUSH | 1 | 0 | 0 | {} | unplanned |
| R2 | check | NATURAL_RUSH | 2 | 3 | 3 | {} | 0.439–1.000 |
| R2 | check | NATURAL_RUSH | 3 | 9 | 6 | {'no eligible disjoint botched placement': 3} | 0.354–0.879 |
| R2 | check | HESITATION | 1 | 0 | 0 | {} | unplanned |
| R2 | check | HESITATION | 2 | 3 | 3 | {} | 0.439–1.000 |
| R2 | check | HESITATION | 3 | 9 | 9 | {} | 0.701–1.000 |
| R2 | check | WORD_BY_WORD | 1 | 0 | 0 | {} | unplanned |
| R2 | check | WORD_BY_WORD | 2 | 3 | 3 | {} | 0.439–1.000 |
| R2 | check | WORD_BY_WORD | 3 | 9 | 8 | {'no eligible disjoint botched placement': 1} | 0.565–0.980 |
| R2 | check | UNEVEN_TEMPO | 1 | 0 | 0 | {} | unplanned |
| R2 | check | UNEVEN_TEMPO | 2 | 3 | 3 | {} | 0.439–1.000 |
| R2 | check | UNEVEN_TEMPO | 3 | 9 | 9 | {} | 0.701–1.000 |
| R2 | check | WORD_REPETITION | 1 | 0 | 0 | {} | unplanned |
| R2 | check | WORD_REPETITION | 2 | 3 | 3 | {} | 0.439–1.000 |
| R2 | check | WORD_REPETITION | 3 | 9 | 9 | {} | 0.701–1.000 |
| R2 | check | SOUND_REPETITION | 1 | 0 | 0 | {} | unplanned |
| R2 | check | SOUND_REPETITION | 2 | 3 | 3 | {} | 0.439–1.000 |
| R2 | check | SOUND_REPETITION | 3 | 9 | 9 | {} | 0.701–1.000 |
| R2 | check | RHYME_PROLONGATION | 1 | 0 | 0 | {} | unplanned |
| R2 | check | RHYME_PROLONGATION | 2 | 3 | 3 | {} | 0.439–1.000 |
| R2 | check | RHYME_PROLONGATION | 3 | 9 | 9 | {} | 0.701–1.000 |
| R2 | check | ONSET_PROLONGATION | 1 | 0 | 0 | {} | unplanned |
| R2 | check | ONSET_PROLONGATION | 2 | 3 | 3 | {} | 0.439–1.000 |
| R2 | check | ONSET_PROLONGATION | 3 | 9 | 9 | {} | 0.701–1.000 |
| R2 | check | BLOCK | 1 | 0 | 0 | {} | unplanned |
| R2 | check | BLOCK | 2 | 3 | 3 | {} | 0.439–1.000 |
| R2 | check | BLOCK | 3 | 9 | 7 | {'no eligible disjoint botched placement': 2} | 0.453–0.937 |
| R2 | check | LOW_EFFORT | 1 | 0 | 0 | {} | unplanned |
| R2 | check | LOW_EFFORT | 2 | 3 | 3 | {} | 0.439–1.000 |
| R2 | check | LOW_EFFORT | 3 | 9 | 9 | {} | 0.701–1.000 |
| R2 | check | TRAILING_OFF | 1 | 0 | 0 | {} | unplanned |
| R2 | check | TRAILING_OFF | 2 | 3 | 3 | {} | 0.439–1.000 |
| R2 | check | TRAILING_OFF | 3 | 9 | 9 | {} | 0.701–1.000 |
| R2 | check | MISPLACED_EMPHASIS | 1 | 0 | 0 | {} | unplanned |
| R2 | check | MISPLACED_EMPHASIS | 2 | 0 | 0 | {} | unplanned |
| R2 | check | MISPLACED_EMPHASIS | 3 | 9 | 6 | {'no eligible disjoint botched placement': 3} | 0.354–0.879 |
| R2 | check | RISING_ENDING | 1 | 0 | 0 | {} | unplanned |
| R2 | check | RISING_ENDING | 2 | 0 | 0 | {} | unplanned |
| R2 | check | RISING_ENDING | 3 | 9 | 9 | {} | 0.701–1.000 |
| R2 | check | FLAT_FINAL_FALL | 1 | 0 | 0 | {} | unplanned |
| R2 | check | FLAT_FINAL_FALL | 2 | 0 | 0 | {} | unplanned |
| R2 | check | FLAT_FINAL_FALL | 3 | 9 | 9 | {} | 0.701–1.000 |
| R2 | check | REPEATED_CONTOUR | 1 | 0 | 0 | {} | unplanned |
| R2 | check | REPEATED_CONTOUR | 2 | 0 | 0 | {} | unplanned |
| R2 | check | REPEATED_CONTOUR | 3 | 9 | 9 | {} | 0.701–1.000 |
| R2 | train | NATURAL_RUSH | 1 | 0 | 0 | {} | unplanned |
| R2 | train | NATURAL_RUSH | 2 | 1 | 1 | {} | 0.207–1.000 |
| R2 | train | NATURAL_RUSH | 3 | 3 | 3 | {} | 0.439–1.000 |
| R2 | train | HESITATION | 1 | 0 | 0 | {} | unplanned |
| R2 | train | HESITATION | 2 | 1 | 1 | {} | 0.207–1.000 |
| R2 | train | HESITATION | 3 | 3 | 3 | {} | 0.439–1.000 |
| R2 | train | WORD_BY_WORD | 1 | 0 | 0 | {} | unplanned |
| R2 | train | WORD_BY_WORD | 2 | 1 | 1 | {} | 0.207–1.000 |
| R2 | train | WORD_BY_WORD | 3 | 3 | 3 | {} | 0.439–1.000 |
| R2 | train | UNEVEN_TEMPO | 1 | 0 | 0 | {} | unplanned |
| R2 | train | UNEVEN_TEMPO | 2 | 1 | 1 | {} | 0.207–1.000 |
| R2 | train | UNEVEN_TEMPO | 3 | 3 | 3 | {} | 0.439–1.000 |
| R2 | train | WORD_REPETITION | 1 | 0 | 0 | {} | unplanned |
| R2 | train | WORD_REPETITION | 2 | 1 | 1 | {} | 0.207–1.000 |
| R2 | train | WORD_REPETITION | 3 | 3 | 3 | {} | 0.439–1.000 |
| R2 | train | SOUND_REPETITION | 1 | 0 | 0 | {} | unplanned |
| R2 | train | SOUND_REPETITION | 2 | 1 | 1 | {} | 0.207–1.000 |
| R2 | train | SOUND_REPETITION | 3 | 3 | 3 | {} | 0.439–1.000 |
| R2 | train | RHYME_PROLONGATION | 1 | 0 | 0 | {} | unplanned |
| R2 | train | RHYME_PROLONGATION | 2 | 1 | 1 | {} | 0.207–1.000 |
| R2 | train | RHYME_PROLONGATION | 3 | 3 | 3 | {} | 0.439–1.000 |
| R2 | train | ONSET_PROLONGATION | 1 | 0 | 0 | {} | unplanned |
| R2 | train | ONSET_PROLONGATION | 2 | 1 | 1 | {} | 0.207–1.000 |
| R2 | train | ONSET_PROLONGATION | 3 | 3 | 3 | {} | 0.439–1.000 |
| R2 | train | BLOCK | 1 | 0 | 0 | {} | unplanned |
| R2 | train | BLOCK | 2 | 1 | 1 | {} | 0.207–1.000 |
| R2 | train | BLOCK | 3 | 3 | 1 | {'no eligible disjoint botched placement': 2} | 0.061–0.792 |
| R2 | train | LOW_EFFORT | 1 | 0 | 0 | {} | unplanned |
| R2 | train | LOW_EFFORT | 2 | 1 | 1 | {} | 0.207–1.000 |
| R2 | train | LOW_EFFORT | 3 | 3 | 3 | {} | 0.439–1.000 |
| R2 | train | TRAILING_OFF | 1 | 0 | 0 | {} | unplanned |
| R2 | train | TRAILING_OFF | 2 | 1 | 1 | {} | 0.207–1.000 |
| R2 | train | TRAILING_OFF | 3 | 3 | 3 | {} | 0.439–1.000 |
| R2 | train | MISPLACED_EMPHASIS | 1 | 0 | 0 | {} | unplanned |
| R2 | train | MISPLACED_EMPHASIS | 2 | 0 | 0 | {} | unplanned |
| R2 | train | MISPLACED_EMPHASIS | 3 | 3 | 3 | {} | 0.439–1.000 |
| R2 | train | RISING_ENDING | 1 | 0 | 0 | {} | unplanned |
| R2 | train | RISING_ENDING | 2 | 0 | 0 | {} | unplanned |
| R2 | train | RISING_ENDING | 3 | 3 | 3 | {} | 0.439–1.000 |
| R2 | train | FLAT_FINAL_FALL | 1 | 0 | 0 | {} | unplanned |
| R2 | train | FLAT_FINAL_FALL | 2 | 0 | 0 | {} | unplanned |
| R2 | train | FLAT_FINAL_FALL | 3 | 3 | 3 | {} | 0.439–1.000 |
| R2 | train | REPEATED_CONTOUR | 1 | 0 | 0 | {} | unplanned |
| R2 | train | REPEATED_CONTOUR | 2 | 0 | 0 | {} | unplanned |
| R2 | train | REPEATED_CONTOUR | 3 | 3 | 3 | {} | 0.439–1.000 |

Empty held-out cells: R2/check/NATURAL_RUSH/1 (unplanned); R2/check/HESITATION/1 (unplanned); R2/check/WORD_BY_WORD/1 (unplanned); R2/check/UNEVEN_TEMPO/1 (unplanned); R2/check/WORD_REPETITION/1 (unplanned); R2/check/SOUND_REPETITION/1 (unplanned); R2/check/RHYME_PROLONGATION/1 (unplanned); R2/check/ONSET_PROLONGATION/1 (unplanned); R2/check/BLOCK/1 (unplanned); R2/check/LOW_EFFORT/1 (unplanned); R2/check/TRAILING_OFF/1 (unplanned); R2/check/MISPLACED_EMPHASIS/1 (unplanned); R2/check/MISPLACED_EMPHASIS/2 (unplanned); R2/check/RISING_ENDING/1 (unplanned); R2/check/RISING_ENDING/2 (unplanned); R2/check/FLAT_FINAL_FALL/1 (unplanned); R2/check/FLAT_FINAL_FALL/2 (unplanned); R2/check/REPEATED_CONTOUR/1 (unplanned); R2/check/REPEATED_CONTOUR/2 (unplanned)

| regime | split | type | level | n | realised median | unit | median bootstrap 95% |
|---|---|---|---|---|---|---|---|
| R1 | test | NATURAL_RUSH | 1 | 2 | -0.764094 | s | insufficient n |
| R1 | test | NATURAL_RUSH | 2 | 2 | -1.22366 | s | insufficient n |
| R1 | test | NATURAL_RUSH | 3 | 5 | -0.890375 | s | -2.64119–-0.566125 |
| R1 | test | HESITATION | 1 | 2 | 0.268 | s | insufficient n |
| R1 | test | HESITATION | 2 | 2 | 0.67 | s | insufficient n |
| R1 | test | HESITATION | 3 | 6 | 1.304 | s | 1.216–1.344 |
| R1 | test | WORD_BY_WORD | 1 | 2 | 1.05 | s | insufficient n |
| R1 | test | WORD_BY_WORD | 2 | 2 | 1.575 | s | insufficient n |
| R1 | test | WORD_BY_WORD | 3 | 6 | 2.7 | s | 2.1–2.7 |
| R1 | test | UNEVEN_TEMPO | 1 | 2 | 0.0872046 | ratio | insufficient n |
| R1 | test | UNEVEN_TEMPO | 2 | 2 | 0.174398 | ratio | insufficient n |
| R1 | test | UNEVEN_TEMPO | 3 | 6 | 0.252993 | ratio | 0.225869–0.303616 |
| R1 | test | WORD_REPETITION | 1 | 2 | 0.282281 | s | insufficient n |
| R1 | test | WORD_REPETITION | 2 | 2 | 0.449375 | s | insufficient n |
| R1 | test | WORD_REPETITION | 3 | 6 | 0.596594 | s | 0.504281–0.637437 |
| R1 | test | SOUND_REPETITION | 1 | 2 | 0.327844 | s | insufficient n |
| R1 | test | SOUND_REPETITION | 2 | 2 | 0.490812 | s | insufficient n |
| R1 | test | SOUND_REPETITION | 3 | 6 | 0.654375 | s | 0.577406–0.657938 |
| R1 | test | RHYME_PROLONGATION | 1 | 2 | 0.18 | s | insufficient n |
| R1 | test | RHYME_PROLONGATION | 2 | 2 | 0.36 | s | insufficient n |
| R1 | test | RHYME_PROLONGATION | 3 | 6 | 0.54 | s | 0.54–0.54 |
| R1 | test | ONSET_PROLONGATION | 1 | 2 | 0.25 | s | insufficient n |
| R1 | test | ONSET_PROLONGATION | 2 | 2 | 0.55 | s | insufficient n |
| R1 | test | ONSET_PROLONGATION | 3 | 6 | 0.9 | s | 0.9–0.9 |
| R1 | test | BLOCK | 1 | 2 | 0.5 | s | insufficient n |
| R1 | test | BLOCK | 2 | 2 | 1.25 | s | insufficient n |
| R1 | test | BLOCK | 3 | 6 | 2 | s | 2–2 |
| R1 | test | LOW_EFFORT | 1 | 2 | -2.81117 | dB | insufficient n |
| R1 | test | LOW_EFFORT | 2 | 2 | -5.37081 | dB | insufficient n |
| R1 | test | LOW_EFFORT | 3 | 6 | -7.13874 | dB | -7.68787–-6.20176 |
| R1 | test | TRAILING_OFF | 1 | 2 | -1.33591 | dB | insufficient n |
| R1 | test | TRAILING_OFF | 2 | 2 | -2.46778 | dB | insufficient n |
| R1 | test | TRAILING_OFF | 3 | 6 | -3.43582 | dB | -4.29096–-3.15048 |
| R1 | test | MISPLACED_EMPHASIS | 1 | 1 | 0.788829 | p | insufficient n |
| R1 | test | MISPLACED_EMPHASIS | 2 | 2 | 1.87525 | p | insufficient n |
| R1 | test | MISPLACED_EMPHASIS | 3 | 6 | 2.71452 | p | 2.50204–3.01557 |
| R1 | test | RISING_ENDING | 1 | 2 | 1.89119 | st | insufficient n |
| R1 | test | RISING_ENDING | 2 | 2 | 3.91187 | st | insufficient n |
| R1 | test | RISING_ENDING | 3 | 6 | 5.59915 | st | 0.694703–6.00464 |
| R1 | test | FLAT_FINAL_FALL | 1 | 2 | -0.920324 | st | insufficient n |
| R1 | test | FLAT_FINAL_FALL | 2 | 2 | -1.78261 | st | insufficient n |
| R1 | test | FLAT_FINAL_FALL | 3 | 5 | -1.51444 | st | -3.12998–-0.175198 |
| R1 | test | REPEATED_CONTOUR | 1 | 2 | -1.26704 | st | insufficient n |
| R1 | test | REPEATED_CONTOUR | 2 | 2 | -2.5431 | st | insufficient n |
| R1 | test | REPEATED_CONTOUR | 3 | 6 | -3.33979 | st | -4.38439–-1.9031 |
| R1 | train | NATURAL_RUSH | 1 | 5 | -0.366812 | s | -0.567438–-0.184062 |
| R1 | train | NATURAL_RUSH | 2 | 5 | -0.544 | s | -0.8825–-0.255625 |
| R1 | train | NATURAL_RUSH | 3 | 14 | -0.876656 | s | -1.24567–-0.715125 |
| R1 | train | HESITATION | 1 | 5 | 0.248 | s | 0.224–0.256 |
| R1 | train | HESITATION | 2 | 5 | 0.62 | s | 0.56–0.64 |
| R1 | train | HESITATION | 3 | 15 | 1.208 | s | 1.112–1.288 |
| R1 | train | WORD_BY_WORD | 1 | 5 | 0.75 | s | 0.75–1.05 |
| R1 | train | WORD_BY_WORD | 2 | 5 | 1.125 | s | 1.125–1.575 |
| R1 | train | WORD_BY_WORD | 3 | 9 | 2.1 | s | 1.5–2.7 |
| R1 | train | UNEVEN_TEMPO | 1 | 5 | 0.103797 | ratio | 0.0923776–0.110814 |
| R1 | train | UNEVEN_TEMPO | 2 | 5 | 0.207846 | ratio | 0.184721–0.221395 |
| R1 | train | UNEVEN_TEMPO | 3 | 13 | 0.311674 | ratio | 0.277099–0.318743 |
| R1 | train | WORD_REPETITION | 1 | 5 | 0.205875 | s | 0.148625–0.392437 |
| R1 | train | WORD_REPETITION | 2 | 5 | 0.355375 | s | 0.284875–0.584937 |
| R1 | train | WORD_REPETITION | 3 | 15 | 0.490812 | s | 0.459688–0.51125 |
| R1 | train | SOUND_REPETITION | 1 | 5 | 0.307312 | s | 0.27325–0.38425 |
| R1 | train | SOUND_REPETITION | 2 | 5 | 0.460688 | s | 0.406625–0.57875 |
| R1 | train | SOUND_REPETITION | 3 | 15 | 0.609437 | s | 0.572562–0.661125 |
| R1 | train | RHYME_PROLONGATION | 1 | 5 | 0.18 | s | 0.18–0.18 |
| R1 | train | RHYME_PROLONGATION | 2 | 5 | 0.36 | s | 0.36–0.36 |
| R1 | train | RHYME_PROLONGATION | 3 | 15 | 0.54 | s | 0.54–0.54 |
| R1 | train | ONSET_PROLONGATION | 1 | 5 | 0.25 | s | 0.25–0.25 |
| R1 | train | ONSET_PROLONGATION | 2 | 5 | 0.55 | s | 0.55–0.55 |
| R1 | train | ONSET_PROLONGATION | 3 | 15 | 0.9 | s | 0.9–0.9 |
| R1 | train | BLOCK | 1 | 4 | 0.5 | s | 0.5–0.5 |
| R1 | train | BLOCK | 2 | 4 | 1.25 | s | 1.25–1.25 |
| R1 | train | BLOCK | 3 | 10 | 2 | s | 2–2 |
| R1 | train | LOW_EFFORT | 1 | 5 | -2.66516 | dB | -3.16515–-2.00719 |
| R1 | train | LOW_EFFORT | 2 | 5 | -5.24916 | dB | -6.24394–-3.94437 |
| R1 | train | LOW_EFFORT | 3 | 15 | -6.9134 | dB | -7.12438–-6.0429 |
| R1 | train | TRAILING_OFF | 1 | 5 | -1.07753 | dB | -1.67506–-0.876134 |
| R1 | train | TRAILING_OFF | 2 | 5 | -2.00235 | dB | -3.15813–-1.6018 |
| R1 | train | TRAILING_OFF | 3 | 14 | -2.91197 | dB | -3.4078–-2.66885 |
| R1 | train | MISPLACED_EMPHASIS | 1 | 4 | 0.74093 | p | 0.734141–0.832948 |
| R1 | train | MISPLACED_EMPHASIS | 2 | 4 | 1.42377 | p | 1.32845–1.62328 |
| R1 | train | MISPLACED_EMPHASIS | 3 | 15 | 2.14044 | p | 2.07419–2.39558 |
| R1 | train | RISING_ENDING | 1 | 4 | 1.72901 | st | 0.507441–2.40601 |
| R1 | train | RISING_ENDING | 2 | 4 | 3.45676 | st | 0.318439–4.40479 |
| R1 | train | RISING_ENDING | 3 | 13 | 5.52502 | st | 5.12554–5.86454 |
| R1 | train | FLAT_FINAL_FALL | 1 | 5 | -0.521276 | st | -0.967723–-0.183122 |
| R1 | train | FLAT_FINAL_FALL | 2 | 5 | -1.30437 | st | -2.36025–0.525133 |
| R1 | train | FLAT_FINAL_FALL | 3 | 12 | -2.55219 | st | -2.86692–-2.08947 |
| R1 | train | REPEATED_CONTOUR | 1 | 5 | -0.968384 | st | -1.09149–-0.328586 |
| R1 | train | REPEATED_CONTOUR | 2 | 5 | -1.99589 | st | -2.14923–-0.32251 |
| R1 | train | REPEATED_CONTOUR | 3 | 14 | -2.38443 | st | -2.73934–-1.59563 |
| R1 | val | NATURAL_RUSH | 1 | 2 | -0.513969 | s | insufficient n |
| R1 | val | NATURAL_RUSH | 2 | 2 | -0.795906 | s | insufficient n |
| R1 | val | NATURAL_RUSH | 3 | 6 | -1.17256 | s | -2.08778–-0.712094 |
| R1 | val | HESITATION | 1 | 2 | 0.238 | s | insufficient n |
| R1 | val | HESITATION | 2 | 2 | 0.595 | s | insufficient n |
| R1 | val | HESITATION | 3 | 6 | 1.184 | s | 1.112–1.328 |
| R1 | val | WORD_BY_WORD | 1 | 2 | 0.6 | s | insufficient n |
| R1 | val | WORD_BY_WORD | 2 | 2 | 0.9 | s | insufficient n |
| R1 | val | WORD_BY_WORD | 3 | 6 | 2.7 | s | 1.2–2.7 |
| R1 | val | UNEVEN_TEMPO | 1 | 2 | 0.101207 | ratio | insufficient n |
| R1 | val | UNEVEN_TEMPO | 2 | 2 | 0.202204 | ratio | insufficient n |
| R1 | val | UNEVEN_TEMPO | 3 | 4 | 0.256408 | ratio | 0.232592–0.337773 |
| R1 | val | WORD_REPETITION | 1 | 2 | 0.193344 | s | insufficient n |
| R1 | val | WORD_REPETITION | 2 | 2 | 0.339875 | s | insufficient n |
| R1 | val | WORD_REPETITION | 3 | 6 | 0.462156 | s | 0.409719–0.499313 |
| R1 | val | SOUND_REPETITION | 1 | 2 | 0.272156 | s | insufficient n |
| R1 | val | SOUND_REPETITION | 2 | 2 | 0.406938 | s | insufficient n |
| R1 | val | SOUND_REPETITION | 3 | 6 | 0.627875 | s | 0.50525–0.731625 |
| R1 | val | RHYME_PROLONGATION | 1 | 2 | 0.18 | s | insufficient n |
| R1 | val | RHYME_PROLONGATION | 2 | 2 | 0.36 | s | insufficient n |
| R1 | val | RHYME_PROLONGATION | 3 | 6 | 0.54 | s | 0.54–0.54 |
| R1 | val | ONSET_PROLONGATION | 1 | 2 | 0.25 | s | insufficient n |
| R1 | val | ONSET_PROLONGATION | 2 | 2 | 0.55 | s | insufficient n |
| R1 | val | ONSET_PROLONGATION | 3 | 6 | 0.9 | s | 0.9–0.9 |
| R1 | val | BLOCK | 1 | 1 | 0.5 | s | insufficient n |
| R1 | val | BLOCK | 2 | 1 | 1.25 | s | insufficient n |
| R1 | val | BLOCK | 3 | 3 | 2 | s | 2–2 |
| R1 | val | LOW_EFFORT | 1 | 2 | -2.71535 | dB | insufficient n |
| R1 | val | LOW_EFFORT | 2 | 2 | -5.30451 | dB | insufficient n |
| R1 | val | LOW_EFFORT | 3 | 6 | -6.68895 | dB | -8.67738–-5.328 |
| R1 | val | TRAILING_OFF | 1 | 2 | -1.40841 | dB | insufficient n |
| R1 | val | TRAILING_OFF | 2 | 2 | -2.69943 | dB | insufficient n |
| R1 | val | TRAILING_OFF | 3 | 6 | -3.36472 | dB | -4.78595–-2.53744 |
| R1 | val | MISPLACED_EMPHASIS | 1 | 2 | 0.852965 | p | insufficient n |
| R1 | val | MISPLACED_EMPHASIS | 2 | 2 | 1.61943 | p | insufficient n |
| R1 | val | MISPLACED_EMPHASIS | 3 | 5 | 2.29088 | p | 1.75996–2.51459 |
| R1 | val | RISING_ENDING | 1 | 2 | 2.30227 | st | insufficient n |
| R1 | val | RISING_ENDING | 2 | 2 | -2.00404 | st | insufficient n |
| R1 | val | RISING_ENDING | 3 | 5 | 5.20828 | st | 0.128894–6.2427 |
| R1 | val | FLAT_FINAL_FALL | 1 | 2 | 0.618006 | st | insufficient n |
| R1 | val | FLAT_FINAL_FALL | 2 | 2 | 0.993119 | st | insufficient n |
| R1 | val | FLAT_FINAL_FALL | 3 | 3 | -1.88496 | st | -3.06763–-0.0833785 |
| R1 | val | REPEATED_CONTOUR | 1 | 1 | -1.34088 | st | insufficient n |
| R1 | val | REPEATED_CONTOUR | 2 | 1 | -2.66406 | st | insufficient n |
| R1 | val | REPEATED_CONTOUR | 3 | 4 | -3.452 | st | -3.84342–-2.83598 |
| R2 | calibration | NATURAL_RUSH | 1 | 0 | missing | — | insufficient n |
| R2 | calibration | NATURAL_RUSH | 2 | 6 | -0.547719 | s | -0.618313–-0.402094 |
| R2 | calibration | NATURAL_RUSH | 3 | 18 | -0.814625 | s | -1.37938–-0.659312 |
| R2 | calibration | HESITATION | 1 | 0 | missing | — | insufficient n |
| R2 | calibration | HESITATION | 2 | 6 | 0.68 | s | 0.65–0.715 |
| R2 | calibration | HESITATION | 3 | 18 | 1.256 | s | 1.24–1.288 |
| R2 | calibration | WORD_BY_WORD | 1 | 0 | missing | — | insufficient n |
| R2 | calibration | WORD_BY_WORD | 2 | 6 | 1.125 | s | 1.0125–1.575 |
| R2 | calibration | WORD_BY_WORD | 3 | 16 | 2.7 | s | 2.1–2.7 |
| R2 | calibration | UNEVEN_TEMPO | 1 | 0 | missing | — | insufficient n |
| R2 | calibration | UNEVEN_TEMPO | 2 | 6 | 0.183901 | ratio | 0.179786–0.232433 |
| R2 | calibration | UNEVEN_TEMPO | 3 | 18 | 0.2758 | ratio | 0.254915–0.315285 |
| R2 | calibration | WORD_REPETITION | 1 | 0 | missing | — | insufficient n |
| R2 | calibration | WORD_REPETITION | 2 | 6 | 0.377344 | s | 0.293375–0.514062 |
| R2 | calibration | WORD_REPETITION | 3 | 18 | 0.482438 | s | 0.425281–0.569125 |
| R2 | calibration | SOUND_REPETITION | 1 | 0 | missing | — | insufficient n |
| R2 | calibration | SOUND_REPETITION | 2 | 6 | 0.473969 | s | 0.427438–0.5345 |
| R2 | calibration | SOUND_REPETITION | 3 | 18 | 0.661531 | s | 0.583531–0.689438 |
| R2 | calibration | RHYME_PROLONGATION | 1 | 0 | missing | — | insufficient n |
| R2 | calibration | RHYME_PROLONGATION | 2 | 6 | 0.36 | s | 0.36–0.36 |
| R2 | calibration | RHYME_PROLONGATION | 3 | 18 | 0.54 | s | 0.54–0.54 |
| R2 | calibration | ONSET_PROLONGATION | 1 | 0 | missing | — | insufficient n |
| R2 | calibration | ONSET_PROLONGATION | 2 | 6 | 0.55 | s | 0.55–0.55 |
| R2 | calibration | ONSET_PROLONGATION | 3 | 18 | 0.9 | s | 0.9–0.9 |
| R2 | calibration | BLOCK | 1 | 0 | missing | — | insufficient n |
| R2 | calibration | BLOCK | 2 | 6 | 1.25 | s | 1.25–1.25 |
| R2 | calibration | BLOCK | 3 | 17 | 2 | s | 2–2 |
| R2 | calibration | LOW_EFFORT | 1 | 0 | missing | — | insufficient n |
| R2 | calibration | LOW_EFFORT | 2 | 6 | -4.04735 | dB | -5.59603–-3.17581 |
| R2 | calibration | LOW_EFFORT | 3 | 18 | -6.08697 | dB | -7.37179–-5.69991 |
| R2 | calibration | TRAILING_OFF | 1 | 0 | missing | — | insufficient n |
| R2 | calibration | TRAILING_OFF | 2 | 6 | -3.26565 | dB | -3.62623–-2.02278 |
| R2 | calibration | TRAILING_OFF | 3 | 18 | -4.53757 | dB | -5.05892–-3.59999 |
| R2 | calibration | MISPLACED_EMPHASIS | 1 | 0 | missing | — | insufficient n |
| R2 | calibration | MISPLACED_EMPHASIS | 2 | 0 | missing | — | insufficient n |
| R2 | calibration | MISPLACED_EMPHASIS | 3 | 7 | 2.32373 | p | 2.12772–2.59069 |
| R2 | calibration | RISING_ENDING | 1 | 0 | missing | — | insufficient n |
| R2 | calibration | RISING_ENDING | 2 | 0 | missing | — | insufficient n |
| R2 | calibration | RISING_ENDING | 3 | 18 | 5.76662 | st | 5.62421–5.98908 |
| R2 | calibration | FLAT_FINAL_FALL | 1 | 0 | missing | — | insufficient n |
| R2 | calibration | FLAT_FINAL_FALL | 2 | 0 | missing | — | insufficient n |
| R2 | calibration | FLAT_FINAL_FALL | 3 | 16 | -2.40886 | st | -3.08609–-1.60633 |
| R2 | calibration | REPEATED_CONTOUR | 1 | 0 | missing | — | insufficient n |
| R2 | calibration | REPEATED_CONTOUR | 2 | 0 | missing | — | insufficient n |
| R2 | calibration | REPEATED_CONTOUR | 3 | 18 | -3.87833 | st | -4.89085–-3.40823 |
| R2 | check | NATURAL_RUSH | 1 | 0 | missing | — | insufficient n |
| R2 | check | NATURAL_RUSH | 2 | 3 | -0.73275 | s | -1.07763–-0.664312 |
| R2 | check | NATURAL_RUSH | 3 | 6 | -1.23906 | s | -1.65744–-0.879656 |
| R2 | check | HESITATION | 1 | 0 | missing | — | insufficient n |
| R2 | check | HESITATION | 2 | 3 | 0.72 | s | 0.59–0.89 |
| R2 | check | HESITATION | 3 | 9 | 1.288 | s | 1.192–1.624 |
| R2 | check | WORD_BY_WORD | 1 | 0 | missing | — | insufficient n |
| R2 | check | WORD_BY_WORD | 2 | 3 | 1.35 | s | 1.35–1.575 |
| R2 | check | WORD_BY_WORD | 3 | 8 | 2.7 | s | 1.8–2.7 |
| R2 | check | UNEVEN_TEMPO | 1 | 0 | missing | — | insufficient n |
| R2 | check | UNEVEN_TEMPO | 2 | 3 | 0.199706 | ratio | 0.185254–0.228617 |
| R2 | check | UNEVEN_TEMPO | 3 | 9 | 0.276461 | ratio | 0.26871–0.299636 |
| R2 | check | WORD_REPETITION | 1 | 0 | missing | — | insufficient n |
| R2 | check | WORD_REPETITION | 2 | 3 | 0.389437 | s | 0.25525–0.537625 |
| R2 | check | WORD_REPETITION | 3 | 9 | 0.533937 | s | 0.4555–0.72125 |
| R2 | check | SOUND_REPETITION | 1 | 0 | missing | — | insufficient n |
| R2 | check | SOUND_REPETITION | 2 | 3 | 0.536312 | s | 0.527937–0.560688 |
| R2 | check | SOUND_REPETITION | 3 | 9 | 0.699875 | s | 0.665375–0.748687 |
| R2 | check | RHYME_PROLONGATION | 1 | 0 | missing | — | insufficient n |
| R2 | check | RHYME_PROLONGATION | 2 | 3 | 0.36 | s | 0.36–0.36 |
| R2 | check | RHYME_PROLONGATION | 3 | 9 | 0.54 | s | 0.54–0.54 |
| R2 | check | ONSET_PROLONGATION | 1 | 0 | missing | — | insufficient n |
| R2 | check | ONSET_PROLONGATION | 2 | 3 | 0.55 | s | 0.55–0.55 |
| R2 | check | ONSET_PROLONGATION | 3 | 9 | 0.9 | s | 0.9–0.9 |
| R2 | check | BLOCK | 1 | 0 | missing | — | insufficient n |
| R2 | check | BLOCK | 2 | 3 | 1.25 | s | 1.25–1.25 |
| R2 | check | BLOCK | 3 | 7 | 2 | s | 2–2 |
| R2 | check | LOW_EFFORT | 1 | 0 | missing | — | insufficient n |
| R2 | check | LOW_EFFORT | 2 | 3 | -5.07838 | dB | -5.33543–-4.49879 |
| R2 | check | LOW_EFFORT | 3 | 9 | -6.57532 | dB | -7.37177–-5.78103 |
| R2 | check | TRAILING_OFF | 1 | 0 | missing | — | insufficient n |
| R2 | check | TRAILING_OFF | 2 | 3 | -2.76553 | dB | -4.91113–-2.10831 |
| R2 | check | TRAILING_OFF | 3 | 9 | -3.79419 | dB | -6.8738–-2.77823 |
| R2 | check | MISPLACED_EMPHASIS | 1 | 0 | missing | — | insufficient n |
| R2 | check | MISPLACED_EMPHASIS | 2 | 0 | missing | — | insufficient n |
| R2 | check | MISPLACED_EMPHASIS | 3 | 6 | 2.34613 | p | 2.16327–2.47834 |
| R2 | check | RISING_ENDING | 1 | 0 | missing | — | insufficient n |
| R2 | check | RISING_ENDING | 2 | 0 | missing | — | insufficient n |
| R2 | check | RISING_ENDING | 3 | 9 | 5.9393 | st | 5.19185–5.97252 |
| R2 | check | FLAT_FINAL_FALL | 1 | 0 | missing | — | insufficient n |
| R2 | check | FLAT_FINAL_FALL | 2 | 0 | missing | — | insufficient n |
| R2 | check | FLAT_FINAL_FALL | 3 | 9 | -1.81144 | st | -2.85472–-0.301292 |
| R2 | check | REPEATED_CONTOUR | 1 | 0 | missing | — | insufficient n |
| R2 | check | REPEATED_CONTOUR | 2 | 0 | missing | — | insufficient n |
| R2 | check | REPEATED_CONTOUR | 3 | 9 | -2.23088 | st | -3.06759–-1.81765 |
| R2 | train | NATURAL_RUSH | 1 | 0 | missing | — | insufficient n |
| R2 | train | NATURAL_RUSH | 2 | 1 | -0.60425 | s | insufficient n |
| R2 | train | NATURAL_RUSH | 3 | 3 | -0.811875 | s | -1.03113–-0.613688 |
| R2 | train | HESITATION | 1 | 0 | missing | — | insufficient n |
| R2 | train | HESITATION | 2 | 1 | 0.67 | s | insufficient n |
| R2 | train | HESITATION | 3 | 3 | 1.272 | s | 1.16–1.32 |
| R2 | train | WORD_BY_WORD | 1 | 0 | missing | — | insufficient n |
| R2 | train | WORD_BY_WORD | 2 | 1 | 1.35 | s | insufficient n |
| R2 | train | WORD_BY_WORD | 3 | 3 | 2.7 | s | 1.8–2.7 |
| R2 | train | UNEVEN_TEMPO | 1 | 0 | missing | — | insufficient n |
| R2 | train | UNEVEN_TEMPO | 2 | 1 | 0.14902 | ratio | insufficient n |
| R2 | train | UNEVEN_TEMPO | 3 | 3 | 0.258483 | ratio | 0.22357–0.297838 |
| R2 | train | WORD_REPETITION | 1 | 0 | missing | — | insufficient n |
| R2 | train | WORD_REPETITION | 2 | 1 | 0.421187 | s | insufficient n |
| R2 | train | WORD_REPETITION | 3 | 3 | 0.579438 | s | 0.420375–0.582937 |
| R2 | train | SOUND_REPETITION | 1 | 0 | missing | — | insufficient n |
| R2 | train | SOUND_REPETITION | 2 | 1 | 0.423438 | s | insufficient n |
| R2 | train | SOUND_REPETITION | 3 | 3 | 0.561688 | s | 0.542188–0.66825 |
| R2 | train | RHYME_PROLONGATION | 1 | 0 | missing | — | insufficient n |
| R2 | train | RHYME_PROLONGATION | 2 | 1 | 0.36 | s | insufficient n |
| R2 | train | RHYME_PROLONGATION | 3 | 3 | 0.54 | s | 0.54–0.54 |
| R2 | train | ONSET_PROLONGATION | 1 | 0 | missing | — | insufficient n |
| R2 | train | ONSET_PROLONGATION | 2 | 1 | 0.55 | s | insufficient n |
| R2 | train | ONSET_PROLONGATION | 3 | 3 | 0.9 | s | 0.9–0.9 |
| R2 | train | BLOCK | 1 | 0 | missing | — | insufficient n |
| R2 | train | BLOCK | 2 | 1 | 1.25 | s | insufficient n |
| R2 | train | BLOCK | 3 | 1 | 2 | s | insufficient n |
| R2 | train | LOW_EFFORT | 1 | 0 | missing | — | insufficient n |
| R2 | train | LOW_EFFORT | 2 | 1 | -4.562 | dB | insufficient n |
| R2 | train | LOW_EFFORT | 3 | 3 | -7.71428 | dB | -8.08853–-6.25012 |
| R2 | train | TRAILING_OFF | 1 | 0 | missing | — | insufficient n |
| R2 | train | TRAILING_OFF | 2 | 1 | -2.98857 | dB | insufficient n |
| R2 | train | TRAILING_OFF | 3 | 3 | -4.20335 | dB | -4.98673–-4.20335 |
| R2 | train | MISPLACED_EMPHASIS | 1 | 0 | missing | — | insufficient n |
| R2 | train | MISPLACED_EMPHASIS | 2 | 0 | missing | — | insufficient n |
| R2 | train | MISPLACED_EMPHASIS | 3 | 3 | 2.61727 | p | 2.1935–3.01701 |
| R2 | train | RISING_ENDING | 1 | 0 | missing | — | insufficient n |
| R2 | train | RISING_ENDING | 2 | 0 | missing | — | insufficient n |
| R2 | train | RISING_ENDING | 3 | 3 | 6.01733 | st | 5.25739–6.03456 |
| R2 | train | FLAT_FINAL_FALL | 1 | 0 | missing | — | insufficient n |
| R2 | train | FLAT_FINAL_FALL | 2 | 0 | missing | — | insufficient n |
| R2 | train | FLAT_FINAL_FALL | 3 | 3 | -2.80289 | st | -8.27884–-2.80275 |
| R2 | train | REPEATED_CONTOUR | 1 | 0 | missing | — | insufficient n |
| R2 | train | REPEATED_CONTOUR | 2 | 0 | missing | — | insufficient n |
| R2 | train | REPEATED_CONTOUR | 3 | 3 | -3.74777 | st | -3.74777–-3.50971 |

Realisation shortfalls (wrong sign, below half target, coupling, or non-monotone ladder):
- {"clip": "harris_uncsw_2021__extra_L1A", "level": 1, "parent_span": [486080, 489600], "reason": "final contour does not rise by at least 1 st", "type": "RISING_ENDING", "words": [63, 63]}
- {"clip": "harris_uncsw_2021__extra_L1A", "field": "alpha_change_db", "levels": [1, 2, 3], "parent": "harris_uncsw_2021", "reason": "non-monotone realised ladder", "type": "LOW_EFFORT", "values": [-1.7408456698591728, -3.40831896154641, -1.482409515806518]}
- {"clip": "harris_uncsw_2021__extra_L1B", "level": 1, "parent_span": [347040, 351040], "reason": "realised change below half target or wrong sign", "target": 0.9812487099931972, "type": "FLAT_FINAL_FALL", "value": 0.18312178882097863, "words": [47, 47]}
- {"clip": "harris_uncsw_2021__extra_L2A", "level": 2, "parent_span": [486080, 489600], "reason": "final contour does not rise by at least 1 st", "type": "RISING_ENDING", "words": [63, 63]}
- {"clip": "harris_uncsw_2021__extra_L2A", "field": "alpha_change_db", "levels": [1, 2, 3], "parent": "harris_uncsw_2021", "reason": "non-monotone realised ladder", "type": "LOW_EFFORT", "values": [-1.7408456698591728, -3.40831896154641, -1.482409515806518]}
- {"clip": "harris_uncsw_2021__extra_L3A", "level": 3, "parent_span": [415680, 472640], "ratio": 0.16759729810199536, "reason": "alpha/level coupling outside 0.4\u20130.7", "type": "LOW_EFFORT", "words": [54, 59]}
- {"clip": "harris_uncsw_2021__extra_L3A", "field": "alpha_change_db", "levels": [1, 2, 3], "parent": "harris_uncsw_2021", "reason": "non-monotone realised ladder", "type": "LOW_EFFORT", "values": [-1.7408456698591728, -3.40831896154641, -1.482409515806518]}
- {"clip": "hclinton_tomorrow_2010__extra_L1A", "level": 1, "parent_span": [172960, 176960], "reason": "final contour does not rise by at least 1 st", "type": "RISING_ENDING", "words": [26, 26]}
- {"clip": "hclinton_tomorrow_2010__extra_L1A", "level": 1, "parent_span": [172960, 176960], "reason": "realised change below half target or wrong sign", "target": 2.0, "type": "RISING_ENDING", "value": 0.507440745906495, "words": [26, 26]}
- {"clip": "hclinton_tomorrow_2010__extra_L1A", "field": "value", "levels": [1, 2, 3], "parent": "hclinton_tomorrow_2010", "reason": "non-monotone realised ladder", "type": "RISING_ENDING", "values": [0.507440745906495, 0.3184390263232326, 0.7249796526185305]}
- {"clip": "hclinton_tomorrow_2010__extra_L1B", "field": "value", "levels": [1, 2, 3], "parent": "hclinton_tomorrow_2010", "reason": "non-monotone realised ladder", "type": "FLAT_FINAL_FALL", "values": [-0.7561139622566464, 0.5251328010350993, -2.4035220604651046]}
- {"clip": "hclinton_tomorrow_2010__extra_L1D", "field": "value", "levels": [1, 2, 3], "parent": "hclinton_tomorrow_2010", "reason": "non-monotone realised ladder", "type": "REPEATED_CONTOUR", "values": [-0.6033083884045198, -0.3225099434625309, -1.5894613401658284]}
- {"clip": "hclinton_tomorrow_2010__extra_L2A", "level": 2, "parent_span": [172960, 176960], "reason": "final contour does not rise by at least 1 st", "type": "RISING_ENDING", "words": [26, 26]}
- {"clip": "hclinton_tomorrow_2010__extra_L2A", "level": 2, "parent_span": [172960, 176960], "reason": "realised change below half target or wrong sign", "target": 4.0, "type": "RISING_ENDING", "value": 0.3184390263232326, "words": [26, 26]}
- {"clip": "hclinton_tomorrow_2010__extra_L2A", "field": "value", "levels": [1, 2, 3], "parent": "hclinton_tomorrow_2010", "reason": "non-monotone realised ladder", "type": "RISING_ENDING", "values": [0.507440745906495, 0.3184390263232326, 0.7249796526185305]}
- {"clip": "hclinton_tomorrow_2010__extra_L2B", "level": 2, "parent_span": [332480, 335040], "reason": "realised change below half target or wrong sign", "target": 1.6745870316575273, "type": "FLAT_FINAL_FALL", "value": -0.5251328010350993, "words": [46, 46]}
- {"clip": "hclinton_tomorrow_2010__extra_L2B", "field": "value", "levels": [1, 2, 3], "parent": "hclinton_tomorrow_2010", "reason": "non-monotone realised ladder", "type": "FLAT_FINAL_FALL", "values": [-0.7561139622566464, 0.5251328010350993, -2.4035220604651046]}
- {"clip": "hclinton_tomorrow_2010__extra_L2D", "level": 2, "parent_span": [313600, 335040], "reason": "realised change below half target or wrong sign", "target": 1.168917006492916, "type": "REPEATED_CONTOUR", "value": 0.3225099434625309, "words": [43, 46]}
- {"clip": "hclinton_tomorrow_2010__extra_L2D", "field": "value", "levels": [1, 2, 3], "parent": "hclinton_tomorrow_2010", "reason": "non-monotone realised ladder", "type": "REPEATED_CONTOUR", "values": [-0.6033083884045198, -0.3225099434625309, -1.5894613401658284]}
- {"clip": "hclinton_tomorrow_2010__extra_L3A", "level": 3, "parent_span": [172960, 176960], "reason": "final contour does not rise by at least 1 st", "type": "RISING_ENDING", "words": [26, 26]}
- {"clip": "hclinton_tomorrow_2010__extra_L3A", "level": 3, "parent_span": [172960, 176960], "reason": "realised change below half target or wrong sign", "target": 6.0, "type": "RISING_ENDING", "value": 0.7249796526185305, "words": [26, 26]}
- {"clip": "hclinton_tomorrow_2010__extra_L3A", "field": "value", "levels": [1, 2, 3], "parent": "hclinton_tomorrow_2010", "reason": "non-monotone realised ladder", "type": "RISING_ENDING", "values": [0.507440745906495, 0.3184390263232326, 0.7249796526185305]}
- {"clip": "hclinton_tomorrow_2010__extra_L3B", "field": "value", "levels": [1, 2, 3], "parent": "hclinton_tomorrow_2010", "reason": "non-monotone realised ladder", "type": "FLAT_FINAL_FALL", "values": [-0.7561139622566464, 0.5251328010350993, -2.4035220604651046]}
- {"clip": "hclinton_tomorrow_2010__extra_L3D", "field": "value", "levels": [1, 2, 3], "parent": "hclinton_tomorrow_2010", "reason": "non-monotone realised ladder", "type": "REPEATED_CONTOUR", "values": [-0.6033083884045198, -0.3225099434625309, -1.5894613401658284]}
- {"clip": "hclinton_tomorrow_2010__extra_botched_ENDINGS", "level": 3, "parent_span": [172960, 176960], "reason": "final contour does not rise by at least 1 st", "type": "RISING_ENDING", "words": [26, 26]}
- {"clip": "hclinton_tomorrow_2010__extra_botched_ENDINGS", "level": 3, "parent_span": [172960, 176960], "reason": "realised change below half target or wrong sign", "target": 6.0, "type": "RISING_ENDING", "value": -0.3119371609723009, "words": [26, 26]}
- {"clip": "hclinton_tomorrow_2010__extra_botched_ENDINGS", "level": 3, "parent_span": [292320, 296320], "reason": "realised change below half target or wrong sign", "target": 1.2018732675077073, "type": "FLAT_FINAL_FALL", "value": 0.24686584696631508, "words": [42, 42]}
- {"clip": "gwbush_911_2001__extra_L1A", "level": 1, "parent_span": [358880, 362880], "reason": "final contour does not rise by at least 1 st", "type": "RISING_ENDING", "words": [57, 57]}
- {"clip": "gwbush_911_2001__extra_L1B", "level": 1, "parent_span": [237440, 240320], "reason": "realised change below half target or wrong sign", "target": 0.7953507728033262, "type": "FLAT_FINAL_FALL", "value": 0.39654383167111296, "words": [40, 40]}
- {"clip": "gwbush_911_2001__extra_L2A", "level": 2, "parent_span": [358880, 362880], "reason": "final contour does not rise by at least 1 st", "type": "RISING_ENDING", "words": [57, 57]}
- {"clip": "gwbush_911_2001__extra_L3A", "level": 3, "parent_span": [358880, 362880], "reason": "final contour does not rise by at least 1 st", "type": "RISING_ENDING", "words": [57, 57]}
- {"clip": "gwbush_911_2001__extra_botched_ENDINGS", "level": 3, "parent_span": [183040, 186880], "reason": "final contour does not rise by at least 1 st", "type": "RISING_ENDING", "words": [32, 32]}
- {"clip": "obama_weekly_2009__extra_L1A", "level": 1, "parent_span": [303200, 307200], "reason": "missing realised measurement", "type": "RISING_ENDING", "words": [54, 54]}
- {"clip": "obama_weekly_2009__extra_L1A", "field": "value", "levels": [1, 2, 3], "parent": "obama_weekly_2009", "reason": "non-monotone realised ladder", "type": "RISING_ENDING", "values": [null, null, null]}
- {"clip": "obama_weekly_2009__extra_L1D", "field": "value", "levels": [1, 2, 3], "parent": "obama_weekly_2009", "reason": "non-monotone realised ladder", "type": "REPEATED_CONTOUR", "values": [-0.9683837811265787, -2.1492269987510153, -1.424366527318469]}
- {"clip": "obama_weekly_2009__extra_L2A", "level": 2, "parent_span": [303200, 307200], "reason": "missing realised measurement", "type": "RISING_ENDING", "words": [54, 54]}
- {"clip": "obama_weekly_2009__extra_L2A", "field": "value", "levels": [1, 2, 3], "parent": "obama_weekly_2009", "reason": "non-monotone realised ladder", "type": "RISING_ENDING", "values": [null, null, null]}
- {"clip": "obama_weekly_2009__extra_L2D", "field": "value", "levels": [1, 2, 3], "parent": "obama_weekly_2009", "reason": "non-monotone realised ladder", "type": "REPEATED_CONTOUR", "values": [-0.9683837811265787, -2.1492269987510153, -1.424366527318469]}
- {"clip": "obama_weekly_2009__extra_L3A", "level": 3, "parent_span": [303200, 307200], "reason": "missing realised measurement", "type": "RISING_ENDING", "words": [54, 54]}
- {"clip": "obama_weekly_2009__extra_L3A", "field": "value", "levels": [1, 2, 3], "parent": "obama_weekly_2009", "reason": "non-monotone realised ladder", "type": "RISING_ENDING", "values": [null, null, null]}
- {"clip": "obama_weekly_2009__extra_L3D", "level": 3, "parent_span": [323520, 334400], "reason": "realised change below half target or wrong sign", "target": 4.980311119955209, "type": "REPEATED_CONTOUR", "value": 1.424366527318469, "words": [55, 57]}
- {"clip": "obama_weekly_2009__extra_L3D", "field": "value", "levels": [1, 2, 3], "parent": "obama_weekly_2009", "reason": "non-monotone realised ladder", "type": "REPEATED_CONTOUR", "values": [-0.9683837811265787, -2.1492269987510153, -1.424366527318469]}
- {"clip": "obama_weekly_2009__extra_botched_CONTOUR", "level": 3, "parent_span": [323520, 334400], "reason": "realised change below half target or wrong sign", "target": 4.980311119955209, "type": "REPEATED_CONTOUR", "value": 1.103642274398398, "words": [55, 57]}
- {"clip": "obama_weekly_2009__extra_botched_D5", "level": 3, "parent_span": [118080, 171200], "ratio": 0.2956947980316075, "reason": "alpha/level coupling outside 0.4\u20130.7", "type": "LOW_EFFORT", "words": [20, 29]}
- {"clip": "reagan_farewell_1989__extra_L1A", "level": 1, "parent_span": [333600, 337600], "reason": "final contour does not rise by at least 1 st", "type": "RISING_ENDING", "words": [67, 67]}
- {"clip": "reagan_farewell_1989__extra_L2A", "level": 2, "parent_span": [333600, 337600], "reason": "final contour does not rise by at least 1 st", "type": "RISING_ENDING", "words": [67, 67]}
- {"clip": "reagan_farewell_1989__extra_L3A", "level": 3, "parent_span": [333600, 337600], "reason": "final contour does not rise by at least 1 st", "type": "RISING_ENDING", "words": [67, 67]}
- {"clip": "reagan_farewell_1989__extra_botched_ENDINGS", "level": 3, "parent_span": [461600, 465600], "reason": "final contour does not rise by at least 1 st", "type": "RISING_ENDING", "words": [90, 90]}
- {"clip": "reagan_farewell_1989__extra_botched_ENDINGS", "level": 3, "parent_span": [333600, 337600], "reason": "final contour does not rise by at least 1 st", "type": "RISING_ENDING", "words": [67, 67]}
- {"clip": "lbush_radio_2001__extra_L1A", "level": 1, "parent_span": [400480, 404480], "reason": "final contour does not rise by at least 1 st", "type": "RISING_ENDING", "words": [67, 67]}
- {"clip": "lbush_radio_2001__extra_L1A", "field": "pitch_change_st", "levels": [1, 2, 3], "parent": "lbush_radio_2001", "reason": "non-monotone realised ladder", "type": "LOW_EFFORT", "values": [0.1745824091706396, 0.509722384771294, 0.06035005716614705]}
- {"clip": "lbush_radio_2001__extra_L1B", "level": 1, "parent_span": [400480, 404480], "reason": "realised change below half target or wrong sign", "target": 0.685060198452054, "type": "FLAT_FINAL_FALL", "value": -0.6900310507307017, "words": [67, 67]}
- {"clip": "lbush_radio_2001__extra_L1B", "field": "value", "levels": [1, 2, 3], "parent": "lbush_radio_2001", "reason": "non-monotone realised ladder", "type": "FLAT_FINAL_FALL", "values": [0.6900310507307017, 1.3191607850394789, -1.8849640941401147]}
- {"clip": "lbush_radio_2001__extra_L2A", "level": 2, "parent_span": [400480, 404480], "reason": "final contour does not rise by at least 1 st", "type": "RISING_ENDING", "words": [67, 67]}
- {"clip": "lbush_radio_2001__extra_L2A", "field": "pitch_change_st", "levels": [1, 2, 3], "parent": "lbush_radio_2001", "reason": "non-monotone realised ladder", "type": "LOW_EFFORT", "values": [0.1745824091706396, 0.509722384771294, 0.06035005716614705]}
- {"clip": "lbush_radio_2001__extra_L2B", "level": 2, "parent_span": [400480, 404480], "reason": "realised change below half target or wrong sign", "target": 1.370120396904108, "type": "FLAT_FINAL_FALL", "value": -1.3191607850394789, "words": [67, 67]}
- {"clip": "lbush_radio_2001__extra_L2B", "field": "value", "levels": [1, 2, 3], "parent": "lbush_radio_2001", "reason": "non-monotone realised ladder", "type": "FLAT_FINAL_FALL", "values": [0.6900310507307017, 1.3191607850394789, -1.8849640941401147]}
- {"clip": "lbush_radio_2001__extra_L3A", "field": "pitch_change_st", "levels": [1, 2, 3], "parent": "lbush_radio_2001", "reason": "non-monotone realised ladder", "type": "LOW_EFFORT", "values": [0.1745824091706396, 0.509722384771294, 0.06035005716614705]}
- {"clip": "lbush_radio_2001__extra_L3B", "field": "value", "levels": [1, 2, 3], "parent": "lbush_radio_2001", "reason": "non-monotone realised ladder", "type": "FLAT_FINAL_FALL", "values": [0.6900310507307017, 1.3191607850394789, -1.8849640941401147]}
- {"clip": "lbush_radio_2001__extra_botched_ENDINGS", "level": 3, "parent_span": [462240, 466240], "reason": "final contour does not rise by at least 1 st", "type": "RISING_ENDING", "words": [75, 75]}
- {"clip": "eisenhower_farewell_1961__extra_L1A", "field": "pitch_change_st", "levels": [1, 2, 3], "parent": "eisenhower_farewell_1961", "reason": "non-monotone realised ladder", "type": "LOW_EFFORT", "values": [-0.5962806939666621, -0.5399865561599029, -0.9028597681617185]}
- {"clip": "eisenhower_farewell_1961__extra_L1A", "field": "value", "levels": [1, 2, 3], "parent": "eisenhower_farewell_1961", "reason": "non-monotone realised ladder", "type": "RISING_ENDING", "values": [2.2386897745892544, -8.736504341760956, 2.1088357969951876]}
- {"clip": "eisenhower_farewell_1961__extra_L1B", "level": 1, "parent_span": [462880, 466880], "reason": "realised change below half target or wrong sign", "target": 0.5156747285475753, "type": "FLAT_FINAL_FALL", "value": -0.5459816035525276, "words": [54, 54]}
- {"clip": "eisenhower_farewell_1961__extra_L1B", "field": "value", "levels": [1, 2, 3], "parent": "eisenhower_farewell_1961", "reason": "non-monotone realised ladder", "type": "FLAT_FINAL_FALL", "values": [0.5459816035525276, 0.6670778061666389, -0.08337846988585862]}
- {"clip": "eisenhower_farewell_1961__extra_L2A", "level": 2, "parent_span": [462880, 466880], "reason": "final contour does not rise by at least 1 st", "type": "RISING_ENDING", "words": [54, 54]}
- {"clip": "eisenhower_farewell_1961__extra_L2A", "level": 2, "parent_span": [462880, 466880], "reason": "realised change below half target or wrong sign", "target": 4.0, "type": "RISING_ENDING", "value": -8.736504341760956, "words": [54, 54]}
- {"clip": "eisenhower_farewell_1961__extra_L2A", "field": "pitch_change_st", "levels": [1, 2, 3], "parent": "eisenhower_farewell_1961", "reason": "non-monotone realised ladder", "type": "LOW_EFFORT", "values": [-0.5962806939666621, -0.5399865561599029, -0.9028597681617185]}
- {"clip": "eisenhower_farewell_1961__extra_L2A", "field": "value", "levels": [1, 2, 3], "parent": "eisenhower_farewell_1961", "reason": "non-monotone realised ladder", "type": "RISING_ENDING", "values": [2.2386897745892544, -8.736504341760956, 2.1088357969951876]}
- {"clip": "eisenhower_farewell_1961__extra_L2B", "level": 2, "parent_span": [462880, 466880], "reason": "realised change below half target or wrong sign", "target": 1.0313494570951507, "type": "FLAT_FINAL_FALL", "value": -0.6670778061666389, "words": [54, 54]}
- {"clip": "eisenhower_farewell_1961__extra_L2B", "field": "value", "levels": [1, 2, 3], "parent": "eisenhower_farewell_1961", "reason": "non-monotone realised ladder", "type": "FLAT_FINAL_FALL", "values": [0.5459816035525276, 0.6670778061666389, -0.08337846988585862]}
- {"clip": "eisenhower_farewell_1961__extra_L3A", "level": 3, "parent_span": [462880, 466880], "reason": "realised change below half target or wrong sign", "target": 6.0, "type": "RISING_ENDING", "value": 2.1088357969951876, "words": [54, 54]}
- {"clip": "eisenhower_farewell_1961__extra_L3A", "field": "pitch_change_st", "levels": [1, 2, 3], "parent": "eisenhower_farewell_1961", "reason": "non-monotone realised ladder", "type": "LOW_EFFORT", "values": [-0.5962806939666621, -0.5399865561599029, -0.9028597681617185]}
- {"clip": "eisenhower_farewell_1961__extra_L3A", "field": "value", "levels": [1, 2, 3], "parent": "eisenhower_farewell_1961", "reason": "non-monotone realised ladder", "type": "RISING_ENDING", "values": [2.2386897745892544, -8.736504341760956, 2.1088357969951876]}
- {"clip": "eisenhower_farewell_1961__extra_L3B", "level": 3, "parent_span": [462880, 466880], "reason": "realised change below half target or wrong sign", "target": 1.5470241856427263, "type": "FLAT_FINAL_FALL", "value": 0.08337846988585862, "words": [54, 54]}
- {"clip": "eisenhower_farewell_1961__extra_L3B", "field": "value", "levels": [1, 2, 3], "parent": "eisenhower_farewell_1961", "reason": "non-monotone realised ladder", "type": "FLAT_FINAL_FALL", "values": [0.5459816035525276, 0.6670778061666389, -0.08337846988585862]}
- {"clip": "eisenhower_farewell_1961__extra_botched_ENDINGS", "level": 3, "parent_span": [462880, 466880], "reason": "realised change below half target or wrong sign", "target": 6.0, "type": "RISING_ENDING", "value": 0.12889373224245965, "words": [54, 54]}
- {"clip": "mobama_weekly_2014__extra_L1A", "level": 1, "parent_span": [455200, 459200], "reason": "final contour does not rise by at least 1 st", "type": "RISING_ENDING", "words": [72, 72]}
- {"clip": "mobama_weekly_2014__extra_L1A", "field": "pitch_change_st", "levels": [1, 2, 3], "parent": "mobama_weekly_2014", "reason": "non-monotone realised ladder", "type": "LOW_EFFORT", "values": [-0.372372002646955, -0.7208369566944839, -0.3576799003609352]}
- {"clip": "mobama_weekly_2014__extra_L1C", "level": 1, "parent_span": [352000, 374400], "ratio": -0.22341481117434023, "reason": "alpha/level coupling outside 0.4\u20130.7", "type": "TRAILING_OFF", "words": [58, 60]}
- {"clip": "mobama_weekly_2014__extra_L1C", "field": "alpha_change_db", "levels": [1, 2, 3], "parent": "mobama_weekly_2014", "reason": "non-monotone realised ladder", "type": "TRAILING_OFF", "values": [0.3288190581257755, 1.6244353293164195, 2.706050856647251]}
- {"clip": "mobama_weekly_2014__extra_L2A", "level": 2, "parent_span": [455200, 459200], "reason": "final contour does not rise by at least 1 st", "type": "RISING_ENDING", "words": [72, 72]}
- {"clip": "mobama_weekly_2014__extra_L2A", "field": "pitch_change_st", "levels": [1, 2, 3], "parent": "mobama_weekly_2014", "reason": "non-monotone realised ladder", "type": "LOW_EFFORT", "values": [-0.372372002646955, -0.7208369566944839, -0.3576799003609352]}
- {"clip": "mobama_weekly_2014__extra_L2C", "level": 2, "parent_span": [352000, 374400], "ratio": -0.6110942504500475, "reason": "alpha/level coupling outside 0.4\u20130.7", "type": "TRAILING_OFF", "words": [58, 60]}
- {"clip": "mobama_weekly_2014__extra_L2C", "field": "alpha_change_db", "levels": [1, 2, 3], "parent": "mobama_weekly_2014", "reason": "non-monotone realised ladder", "type": "TRAILING_OFF", "values": [0.3288190581257755, 1.6244353293164195, 2.706050856647251]}
- {"clip": "mobama_weekly_2014__extra_L3A", "field": "pitch_change_st", "levels": [1, 2, 3], "parent": "mobama_weekly_2014", "reason": "non-monotone realised ladder", "type": "LOW_EFFORT", "values": [-0.372372002646955, -0.7208369566944839, -0.3576799003609352]}
- {"clip": "mobama_weekly_2014__extra_L3C", "level": 3, "parent_span": [352000, 374400], "ratio": -0.7476806517358737, "reason": "alpha/level coupling outside 0.4\u20130.7", "type": "TRAILING_OFF", "words": [58, 60]}
- {"clip": "mobama_weekly_2014__extra_L3C", "field": "alpha_change_db", "levels": [1, 2, 3], "parent": "mobama_weekly_2014", "reason": "non-monotone realised ladder", "type": "TRAILING_OFF", "values": [0.3288190581257755, 1.6244353293164195, 2.706050856647251]}
- {"clip": "mobama_weekly_2014__extra_botched_ENDINGS", "level": 3, "parent_span": [370400, 374400], "reason": "final contour does not rise by at least 1 st", "type": "RISING_ENDING", "words": [60, 60]}
- {"clip": "mobama_weekly_2014__extra_botched_ENDINGS", "level": 3, "parent_span": [370400, 374400], "reason": "realised change below half target or wrong sign", "target": 6.0, "type": "RISING_ENDING", "value": -4.072350217142101, "words": [60, 60]}
- {"clip": "mobama_weekly_2014__extra_botched_ENDINGS", "level": 3, "parent_span": [120640, 124160], "reason": "realised change below half target or wrong sign", "target": 1.0931121565519504, "type": "FLAT_FINAL_FALL", "value": 0.17519809307152268, "words": [18, 18]}
- {"clip": "nixon_resignation_1974__extra_L1A", "level": 1, "parent_span": [462880, 466880], "reason": "final contour does not rise by at least 1 st", "type": "RISING_ENDING", "words": [55, 55]}
- {"clip": "nixon_resignation_1974__extra_L2A", "level": 2, "parent_span": [462880, 466880], "reason": "final contour does not rise by at least 1 st", "type": "RISING_ENDING", "words": [55, 55]}
- {"clip": "nixon_resignation_1974__extra_botched_D5", "level": 3, "parent_span": [302720, 378880], "ratio": 0.228256262379939, "reason": "alpha/level coupling outside 0.4\u20130.7", "type": "LOW_EFFORT", "words": [33, 42]}
- {"clip": "nixon_resignation_1974__extra_botched_ENDINGS", "level": 3, "parent_span": [35680, 39680], "reason": "final contour does not rise by at least 1 st", "type": "RISING_ENDING", "words": [5, 5]}
- {"clip": "gettysburg_amb__extra_x1_L2", "field": "pitch_change_st", "levels": [2, 3], "parent": "gettysburg_amb", "reason": "non-monotone realised ladder", "type": "LOW_EFFORT", "values": [-0.5750630045638445, 0.828549747045102]}
- {"clip": "gettysburg_amb__extra_x5_L3", "field": "pitch_change_st", "levels": [2, 3], "parent": "gettysburg_amb", "reason": "non-monotone realised ladder", "type": "LOW_EFFORT", "values": [-0.5750630045638445, 0.828549747045102]}
- {"clip": "gettysburg_amb__extra_botched_D5", "level": 3, "parent_span": [279680, 360960], "ratio": 0.09427926416072534, "reason": "alpha/level coupling outside 0.4\u20130.7", "type": "LOW_EFFORT", "words": [50, 59]}
- {"clip": "gettysburg_fb__extra_x1_L2", "level": 2, "parent_span": [299840, 366400], "reason": "realised change below half target or wrong sign", "target": 6.0, "type": "LOW_EFFORT", "value": 2.6993443227852865, "words": [51, 58]}
- {"clip": "gettysburg_fb__extra_x1_L2", "level": 2, "parent_span": [299840, 366400], "ratio": 0.34408517760741775, "reason": "alpha/level coupling outside 0.4\u20130.7", "type": "LOW_EFFORT", "words": [51, 58]}
- {"clip": "gettysburg_fb__extra_x1_L2", "field": "alpha_change_db", "levels": [2, 3], "parent": "gettysburg_fb", "reason": "non-monotone realised ladder", "type": "LOW_EFFORT", "values": [-0.92880437072915, -0.584811758588522]}
- {"clip": "gettysburg_fb__extra_x1_L2", "field": "pitch_change_st", "levels": [2, 3], "parent": "gettysburg_fb", "reason": "non-monotone realised ladder", "type": "LOW_EFFORT", "values": [-0.7786032335547617, 1.1797682162223708]}
- {"clip": "gettysburg_fb__extra_x5_L3", "level": 3, "parent_span": [299840, 366400], "reason": "realised change below half target or wrong sign", "target": 9.0, "type": "LOW_EFFORT", "value": 3.604515394019508, "words": [51, 58]}
- {"clip": "gettysburg_fb__extra_x5_L3", "level": 3, "parent_span": [299840, 366400], "ratio": 0.16224421167927933, "reason": "alpha/level coupling outside 0.4\u20130.7", "type": "LOW_EFFORT", "words": [51, 58]}
- {"clip": "gettysburg_fb__extra_x5_L3", "field": "alpha_change_db", "levels": [2, 3], "parent": "gettysburg_fb", "reason": "non-monotone realised ladder", "type": "LOW_EFFORT", "values": [-0.92880437072915, -0.584811758588522]}
- {"clip": "gettysburg_fb__extra_x5_L3", "field": "pitch_change_st", "levels": [2, 3], "parent": "gettysburg_fb", "reason": "non-monotone realised ladder", "type": "LOW_EFFORT", "values": [-0.7786032335547617, 1.1797682162223708]}
- {"clip": "gettysburg_pc__extra_x9_L3", "level": 3, "parent_span": [46560, 50560], "reason": "final contour does not rise by at least 1 st", "type": "RISING_ENDING", "words": [9, 9]}
- {"clip": "gettysburg_pc__extra_botched_ENDINGS", "level": 3, "parent_span": [225280, 228800], "reason": "final contour does not rise by at least 1 st", "type": "RISING_ENDING", "words": [36, 36]}
- {"clip": "gettysburg_pc__extra_botched_ENDINGS", "level": 3, "parent_span": [446560, 450560], "reason": "final contour does not rise by at least 1 st", "type": "RISING_ENDING", "words": [63, 63]}
- {"clip": "gettysburg_wt__extra_x1_L2", "field": "pitch_change_st", "levels": [2, 3], "parent": "gettysburg_wt", "reason": "non-monotone realised ladder", "type": "LOW_EFFORT", "values": [-0.8382107461739849, -0.030746037464737697]}
- {"clip": "gettysburg_wt__extra_x5_L3", "field": "pitch_change_st", "levels": [2, 3], "parent": "gettysburg_wt", "reason": "non-monotone realised ladder", "type": "LOW_EFFORT", "values": [-0.8382107461739849, -0.030746037464737697]}
- {"clip": "gettysburg_dj__extra_x10_L3", "level": 3, "parent_span": [354400, 358400], "reason": "realised change below half target or wrong sign", "target": 0.6693749667612127, "type": "FLAT_FINAL_FALL", "value": 0.30109304545787846, "words": [63, 63]}
- {"clip": "gettysburg_dj__extra_botched_ENDINGS", "level": 3, "parent_span": [354400, 358400], "reason": "realised change below half target or wrong sign", "target": 0.6693749667612127, "type": "FLAT_FINAL_FALL", "value": 0.3012916972433144, "words": [63, 63]}
- {"clip": "gettysburg_sa__extra_botched_D5", "level": 3, "parent_span": [454720, 475200], "ratio": 0.36776220635249873, "reason": "alpha/level coupling outside 0.4\u20130.7", "type": "TRAILING_OFF", "words": [61, 63]}
- {"clip": "gettysburg_tg__extra_x9_L3", "level": 3, "parent_span": [188640, 192640], "reason": "final contour does not rise by at least 1 st", "type": "RISING_ENDING", "words": [36, 36]}
- {"clip": "gettysburg_tg__extra_botched_ENDINGS", "level": 3, "parent_span": [379680, 383680], "reason": "final contour does not rise by at least 1 st", "type": "RISING_ENDING", "words": [63, 63]}
- {"clip": "greenman_reagan__extra_x9_L3", "level": 3, "parent_span": [235680, 239680], "reason": "final contour does not rise by at least 1 st", "type": "RISING_ENDING", "words": [48, 48]}
- {"clip": "greenman_reagan__extra_botched_ENDINGS", "level": 3, "parent_span": [501600, 505600], "reason": "final contour does not rise by at least 1 st", "type": "RISING_ENDING", "words": [90, 90]}
- {"clip": "greenman_reagan__extra_botched_ENDINGS", "level": 3, "parent_span": [235680, 239680], "reason": "final contour does not rise by at least 1 st", "type": "RISING_ENDING", "words": [48, 48]}

Realised label approximations:
- BLOCK: {"alignment_error_s_empirical": [0.048, 0.089], "limitation": "gap only; no tense closure or enhanced release burst is synthesised", "method": "closure-to-burst energy/flux rise in first 80 ms", "omissions": "signal closure-to-burst energy/flux rise within 80 ms; no tense closure or enhanced burst", "own_stressed": false, "search_window_s": 0.08, "selection": "shared stress preferred, own stress then eligible content fallback; signal eligibility", "stress_fallback": "content fallback"}
- BLOCK: {"alignment_error_s_empirical": [0.048, 0.089], "limitation": "gap only; no tense closure or enhanced release burst is synthesised", "method": "closure-to-burst energy/flux rise in first 80 ms", "omissions": "signal closure-to-burst energy/flux rise within 80 ms; no tense closure or enhanced burst", "own_stressed": false, "search_window_s": 0.08, "selection": "shared stress preferred, own stress then eligible content fallback; signal eligibility"}
- BLOCK: {"alignment_error_s_empirical": [0.048, 0.089], "limitation": "gap only; no tense closure or enhanced release burst is synthesised", "method": "closure-to-burst energy/flux rise in first 80 ms", "omissions": "signal closure-to-burst energy/flux rise within 80 ms; no tense closure or enhanced burst", "own_stressed": true, "search_window_s": 0.08, "selection": "shared stress preferred, own stress then eligible content fallback; signal eligibility", "stress_fallback": "own stress fallback"}
- BLOCK: {"alignment_error_s_empirical": [0.048, 0.089], "limitation": "gap only; no tense closure or enhanced release burst is synthesised", "method": "closure-to-burst energy/flux rise in first 80 ms", "omissions": "signal closure-to-burst energy/flux rise within 80 ms; no tense closure or enhanced burst", "own_stressed": true, "search_window_s": 0.08, "selection": "shared stress preferred, own stress then eligible content fallback; signal eligibility", "stress_fallback": "shared stress"}
- BLOCK: {"alignment_error_s_empirical": [0.048, 0.089], "limitation": "gap only; no tense closure or enhanced release burst is synthesised", "method": "closure-to-burst energy/flux rise in first 80 ms", "omissions": "signal closure-to-burst energy/flux rise within 80 ms; no tense closure or enhanced burst", "own_stressed": true, "search_window_s": 0.08, "selection": "shared stress preferred, own stress then eligible content fallback; signal eligibility"}
- FLAT_FINAL_FALL: {"actual_window_s": 0.12, "alignment_error_s_empirical": [0.048, 0.089], "method": "last 250 ms, clipped to final word; no syllable boundary assumed", "omissions": "last 250 ms clipped to final word; preceding median; PSOLA approximate", "rise_extent": "first to last parent voiced frame inside window"}
- FLAT_FINAL_FALL: {"actual_window_s": 0.16, "alignment_error_s_empirical": [0.048, 0.089], "method": "last 250 ms, clipped to final word; no syllable boundary assumed", "omissions": "last 250 ms clipped to final word; preceding median; PSOLA approximate", "rise_extent": "first to last parent voiced frame inside window"}
- FLAT_FINAL_FALL: {"actual_window_s": 0.18, "alignment_error_s_empirical": [0.048, 0.089], "method": "last 250 ms, clipped to final word; no syllable boundary assumed", "omissions": "last 250 ms clipped to final word; preceding median; PSOLA approximate", "rise_extent": "first to last parent voiced frame inside window"}
- FLAT_FINAL_FALL: {"actual_window_s": 0.2, "alignment_error_s_empirical": [0.048, 0.089], "method": "last 250 ms, clipped to final word; no syllable boundary assumed", "omissions": "last 250 ms clipped to final word; preceding median; PSOLA approximate", "rise_extent": "first to last parent voiced frame inside window"}
- FLAT_FINAL_FALL: {"actual_window_s": 0.22, "alignment_error_s_empirical": [0.048, 0.089], "method": "last 250 ms, clipped to final word; no syllable boundary assumed", "omissions": "last 250 ms clipped to final word; preceding median; PSOLA approximate", "rise_extent": "first to last parent voiced frame inside window"}
- FLAT_FINAL_FALL: {"actual_window_s": 0.24, "alignment_error_s_empirical": [0.048, 0.089], "method": "last 250 ms, clipped to final word; no syllable boundary assumed", "omissions": "last 250 ms clipped to final word; preceding median; PSOLA approximate", "rise_extent": "first to last parent voiced frame inside window"}
- FLAT_FINAL_FALL: {"actual_window_s": 0.25, "alignment_error_s_empirical": [0.048, 0.089], "method": "last 250 ms, clipped to final word; no syllable boundary assumed", "omissions": "last 250 ms clipped to final word; preceding median; PSOLA approximate", "rise_extent": "first to last parent voiced frame inside window"}
- HESITATION: {"method": "30 ms non-pausal gap energy minimum before content word", "omissions": "content word; 30 ms non-pausal gap energy minimum; no retrieval physiology"}
- LOW_EFFORT: {"limitation": "small F0 shift chosen; isolated-vowel 5 Hz/dB not imposed; glottal source, formants and vowel duration omitted", "method": "alpha fitted after room-tone mixing on parent voiced speech above floor", "omissions": "tilt fitted after room mixing on parent voiced speech above floor; source/formants/vowel duration omitted; 5 Hz/dB not established for sentences"}
- MISPLACED_EMPHASIS: {"method": "aligned word spans", "omissions": "stress/text prior; no accent dictionary; natural legitimate function-word accents not modelled"}
- NATURAL_RUSH: {"method": "uniform word compression omits greater shortening of unstressed syllables and vowels; short unclassified gaps unchanged", "omissions": "uniform word compression omits selective unstressed/vowel shortening; short unclassified gaps unchanged"}
- ONSET_PROLONGATION: {"alignment_error_s_empirical": [0.048, 0.089], "limitation": "no phone identity or tension synthesis; unvoiced continuants excluded", "method": "voiced stable-spectrum edge run", "omissions": "100 ms voiced stable onset run; stress fallback; unvoiced continuants omitted", "own_stressed": false, "realised_factor": 10.0, "selection": "shared stress preferred, own stress then eligible content fallback; signal eligibility", "stress_fallback": "content fallback"}
- ONSET_PROLONGATION: {"alignment_error_s_empirical": [0.048, 0.089], "limitation": "no phone identity or tension synthesis; unvoiced continuants excluded", "method": "voiced stable-spectrum edge run", "omissions": "100 ms voiced stable onset run; stress fallback; unvoiced continuants omitted", "own_stressed": false, "realised_factor": 10.0, "selection": "shared stress preferred, own stress then eligible content fallback; signal eligibility", "stress_fallback": "shared stress"}
- ONSET_PROLONGATION: {"alignment_error_s_empirical": [0.048, 0.089], "limitation": "no phone identity or tension synthesis; unvoiced continuants excluded", "method": "voiced stable-spectrum edge run", "omissions": "100 ms voiced stable onset run; stress fallback; unvoiced continuants omitted", "own_stressed": false, "realised_factor": 10.0, "selection": "shared stress preferred, own stress then eligible content fallback; signal eligibility"}
- ONSET_PROLONGATION: {"alignment_error_s_empirical": [0.048, 0.089], "limitation": "no phone identity or tension synthesis; unvoiced continuants excluded", "method": "voiced stable-spectrum edge run", "omissions": "100 ms voiced stable onset run; stress fallback; unvoiced continuants omitted", "own_stressed": false, "realised_factor": 6.5, "selection": "shared stress preferred, own stress then eligible content fallback; signal eligibility", "stress_fallback": "content fallback"}
- ONSET_PROLONGATION: {"alignment_error_s_empirical": [0.048, 0.089], "limitation": "no phone identity or tension synthesis; unvoiced continuants excluded", "method": "voiced stable-spectrum edge run", "omissions": "100 ms voiced stable onset run; stress fallback; unvoiced continuants omitted", "own_stressed": false, "realised_factor": 6.5, "selection": "shared stress preferred, own stress then eligible content fallback; signal eligibility", "stress_fallback": "shared stress"}
- ONSET_PROLONGATION: {"alignment_error_s_empirical": [0.048, 0.089], "limitation": "no phone identity or tension synthesis; unvoiced continuants excluded", "method": "voiced stable-spectrum edge run", "omissions": "100 ms voiced stable onset run; stress fallback; unvoiced continuants omitted", "own_stressed": true, "realised_factor": 10.0, "selection": "shared stress preferred, own stress then eligible content fallback; signal eligibility", "stress_fallback": "own stress fallback"}
- ONSET_PROLONGATION: {"alignment_error_s_empirical": [0.048, 0.089], "limitation": "no phone identity or tension synthesis; unvoiced continuants excluded", "method": "voiced stable-spectrum edge run", "omissions": "100 ms voiced stable onset run; stress fallback; unvoiced continuants omitted", "own_stressed": true, "realised_factor": 10.0, "selection": "shared stress preferred, own stress then eligible content fallback; signal eligibility", "stress_fallback": "shared stress"}
- ONSET_PROLONGATION: {"alignment_error_s_empirical": [0.048, 0.089], "limitation": "no phone identity or tension synthesis; unvoiced continuants excluded", "method": "voiced stable-spectrum edge run", "omissions": "100 ms voiced stable onset run; stress fallback; unvoiced continuants omitted", "own_stressed": true, "realised_factor": 10.0, "selection": "shared stress preferred, own stress then eligible content fallback; signal eligibility"}
- ONSET_PROLONGATION: {"alignment_error_s_empirical": [0.048, 0.089], "limitation": "no phone identity or tension synthesis; unvoiced continuants excluded", "method": "voiced stable-spectrum edge run", "omissions": "100 ms voiced stable onset run; stress fallback; unvoiced continuants omitted", "own_stressed": true, "realised_factor": 3.5, "selection": "shared stress preferred, own stress then eligible content fallback; signal eligibility", "stress_fallback": "shared stress"}
- ONSET_PROLONGATION: {"alignment_error_s_empirical": [0.048, 0.089], "limitation": "no phone identity or tension synthesis; unvoiced continuants excluded", "method": "voiced stable-spectrum edge run", "omissions": "100 ms voiced stable onset run; stress fallback; unvoiced continuants omitted", "own_stressed": true, "realised_factor": 6.5, "selection": "shared stress preferred, own stress then eligible content fallback; signal eligibility", "stress_fallback": "own stress fallback"}
- ONSET_PROLONGATION: {"alignment_error_s_empirical": [0.048, 0.089], "limitation": "no phone identity or tension synthesis; unvoiced continuants excluded", "method": "voiced stable-spectrum edge run", "omissions": "100 ms voiced stable onset run; stress fallback; unvoiced continuants omitted", "own_stressed": true, "realised_factor": 6.5, "selection": "shared stress preferred, own stress then eligible content fallback; signal eligibility", "stress_fallback": "shared stress"}
- REPEATED_CONTOUR: {"method": "linear time-normalised voiced F0; interpolation across unvoiced template gaps", "omissions": "template/target \u22650.5 s chosen; linear time warp; interpolate across unvoiced template gaps; no syntactic matching", "pitch_measurement_grid_s": 0.01}
- RHYME_PROLONGATION: {"alignment_error_s_empirical": [0.048, 0.089], "context_rule": "at least 30 ms aligned gap; typical pre-interruption context not synthesised", "following_gap_s": 0.03999999999999915, "limitation": "no phone identity or tension synthesis; unvoiced continuants excluded", "method": "voiced stable-spectrum edge run", "omissions": "voiced stable edge run \u226590 ms; actual pause context recorded; no phone identity; unvoiced continuants omitted", "pre_pausal": false, "realised_factor": 3.0}
- RHYME_PROLONGATION: {"alignment_error_s_empirical": [0.048, 0.089], "context_rule": "at least 30 ms aligned gap; typical pre-interruption context not synthesised", "following_gap_s": 0.03999999999999915, "limitation": "no phone identity or tension synthesis; unvoiced continuants excluded", "method": "voiced stable-spectrum edge run", "omissions": "voiced stable edge run \u226590 ms; actual pause context recorded; no phone identity; unvoiced continuants omitted", "pre_pausal": false, "realised_factor": 5.0}
- RHYME_PROLONGATION: {"alignment_error_s_empirical": [0.048, 0.089], "context_rule": "at least 30 ms aligned gap; typical pre-interruption context not synthesised", "following_gap_s": 0.03999999999999915, "limitation": "no phone identity or tension synthesis; unvoiced continuants excluded", "method": "voiced stable-spectrum edge run", "omissions": "voiced stable edge run \u226590 ms; actual pause context recorded; no phone identity; unvoiced continuants omitted", "pre_pausal": false, "realised_factor": 7.0}
- RHYME_PROLONGATION: {"alignment_error_s_empirical": [0.048, 0.089], "context_rule": "at least 30 ms aligned gap; typical pre-interruption context not synthesised", "following_gap_s": 0.040000000000000036, "limitation": "no phone identity or tension synthesis; unvoiced continuants excluded", "method": "voiced stable-spectrum edge run", "omissions": "voiced stable edge run \u226590 ms; actual pause context recorded; no phone identity; unvoiced continuants omitted", "pre_pausal": false, "realised_factor": 7.0}
- RHYME_PROLONGATION: {"alignment_error_s_empirical": [0.048, 0.089], "context_rule": "at least 30 ms aligned gap; typical pre-interruption context not synthesised", "following_gap_s": 0.05999999999999872, "limitation": "no phone identity or tension synthesis; unvoiced continuants excluded", "method": "voiced stable-spectrum edge run", "omissions": "voiced stable edge run \u226590 ms; actual pause context recorded; no phone identity; unvoiced continuants omitted", "pre_pausal": false, "realised_factor": 7.0}
- RHYME_PROLONGATION: {"alignment_error_s_empirical": [0.048, 0.089], "context_rule": "at least 30 ms aligned gap; typical pre-interruption context not synthesised", "following_gap_s": 0.05999999999999961, "limitation": "no phone identity or tension synthesis; unvoiced continuants excluded", "method": "voiced stable-spectrum edge run", "omissions": "voiced stable edge run \u226590 ms; actual pause context recorded; no phone identity; unvoiced continuants omitted", "pre_pausal": false, "realised_factor": 7.0}
- RHYME_PROLONGATION: {"alignment_error_s_empirical": [0.048, 0.089], "context_rule": "at least 30 ms aligned gap; typical pre-interruption context not synthesised", "following_gap_s": 0.06000000000000005, "limitation": "no phone identity or tension synthesis; unvoiced continuants excluded", "method": "voiced stable-spectrum edge run", "omissions": "voiced stable edge run \u226590 ms; actual pause context recorded; no phone identity; unvoiced continuants omitted", "pre_pausal": false, "realised_factor": 7.0}
- RHYME_PROLONGATION: {"alignment_error_s_empirical": [0.048, 0.089], "context_rule": "at least 30 ms aligned gap; typical pre-interruption context not synthesised", "following_gap_s": 0.0600000000000005, "limitation": "no phone identity or tension synthesis; unvoiced continuants excluded", "method": "voiced stable-spectrum edge run", "omissions": "voiced stable edge run \u226590 ms; actual pause context recorded; no phone identity; unvoiced continuants omitted", "pre_pausal": false, "realised_factor": 7.0}
- RHYME_PROLONGATION: {"alignment_error_s_empirical": [0.048, 0.089], "context_rule": "at least 30 ms aligned gap; typical pre-interruption context not synthesised", "following_gap_s": 0.0799999999999983, "limitation": "no phone identity or tension synthesis; unvoiced continuants excluded", "method": "voiced stable-spectrum edge run", "omissions": "voiced stable edge run \u226590 ms; actual pause context recorded; no phone identity; unvoiced continuants omitted", "pre_pausal": false, "realised_factor": 5.0}
- RHYME_PROLONGATION: {"alignment_error_s_empirical": [0.048, 0.089], "context_rule": "at least 30 ms aligned gap; typical pre-interruption context not synthesised", "following_gap_s": 0.0799999999999983, "limitation": "no phone identity or tension synthesis; unvoiced continuants excluded", "method": "voiced stable-spectrum edge run", "omissions": "voiced stable edge run \u226590 ms; actual pause context recorded; no phone identity; unvoiced continuants omitted", "pre_pausal": false, "realised_factor": 7.0}
- RHYME_PROLONGATION: {"alignment_error_s_empirical": [0.048, 0.089], "context_rule": "at least 30 ms aligned gap; typical pre-interruption context not synthesised", "following_gap_s": 0.07999999999999985, "limitation": "no phone identity or tension synthesis; unvoiced continuants excluded", "method": "voiced stable-spectrum edge run", "omissions": "voiced stable edge run \u226590 ms; actual pause context recorded; no phone identity; unvoiced continuants omitted", "pre_pausal": false, "realised_factor": 3.0}
- RHYME_PROLONGATION: {"alignment_error_s_empirical": [0.048, 0.089], "context_rule": "at least 30 ms aligned gap; typical pre-interruption context not synthesised", "following_gap_s": 0.07999999999999985, "limitation": "no phone identity or tension synthesis; unvoiced continuants excluded", "method": "voiced stable-spectrum edge run", "omissions": "voiced stable edge run \u226590 ms; actual pause context recorded; no phone identity; unvoiced continuants omitted", "pre_pausal": false, "realised_factor": 5.0}
- RHYME_PROLONGATION: {"alignment_error_s_empirical": [0.048, 0.089], "context_rule": "at least 30 ms aligned gap; typical pre-interruption context not synthesised", "following_gap_s": 0.07999999999999985, "limitation": "no phone identity or tension synthesis; unvoiced continuants excluded", "method": "voiced stable-spectrum edge run", "omissions": "voiced stable edge run \u226590 ms; actual pause context recorded; no phone identity; unvoiced continuants omitted", "pre_pausal": false, "realised_factor": 7.0}
- RHYME_PROLONGATION: {"alignment_error_s_empirical": [0.048, 0.089], "context_rule": "at least 30 ms aligned gap; typical pre-interruption context not synthesised", "following_gap_s": 0.08000000000000007, "limitation": "no phone identity or tension synthesis; unvoiced continuants excluded", "method": "voiced stable-spectrum edge run", "omissions": "voiced stable edge run \u226590 ms; actual pause context recorded; no phone identity; unvoiced continuants omitted", "pre_pausal": false, "realised_factor": 3.0}
- RHYME_PROLONGATION: {"alignment_error_s_empirical": [0.048, 0.089], "context_rule": "at least 30 ms aligned gap; typical pre-interruption context not synthesised", "following_gap_s": 0.08000000000000007, "limitation": "no phone identity or tension synthesis; unvoiced continuants excluded", "method": "voiced stable-spectrum edge run", "omissions": "voiced stable edge run \u226590 ms; actual pause context recorded; no phone identity; unvoiced continuants omitted", "pre_pausal": false, "realised_factor": 5.0}
- RHYME_PROLONGATION: {"alignment_error_s_empirical": [0.048, 0.089], "context_rule": "at least 30 ms aligned gap; typical pre-interruption context not synthesised", "following_gap_s": 0.08000000000000007, "limitation": "no phone identity or tension synthesis; unvoiced continuants excluded", "method": "voiced stable-spectrum edge run", "omissions": "voiced stable edge run \u226590 ms; actual pause context recorded; no phone identity; unvoiced continuants omitted", "pre_pausal": false, "realised_factor": 7.0}
- RHYME_PROLONGATION: {"alignment_error_s_empirical": [0.048, 0.089], "context_rule": "at least 30 ms aligned gap; typical pre-interruption context not synthesised", "following_gap_s": 0.09999999999999964, "limitation": "no phone identity or tension synthesis; unvoiced continuants excluded", "method": "voiced stable-spectrum edge run", "omissions": "voiced stable edge run \u226590 ms; actual pause context recorded; no phone identity; unvoiced continuants omitted", "pre_pausal": false, "realised_factor": 3.0}
- RHYME_PROLONGATION: {"alignment_error_s_empirical": [0.048, 0.089], "context_rule": "at least 30 ms aligned gap; typical pre-interruption context not synthesised", "following_gap_s": 0.09999999999999964, "limitation": "no phone identity or tension synthesis; unvoiced continuants excluded", "method": "voiced stable-spectrum edge run", "omissions": "voiced stable edge run \u226590 ms; actual pause context recorded; no phone identity; unvoiced continuants omitted", "pre_pausal": false, "realised_factor": 5.0}
- RHYME_PROLONGATION: {"alignment_error_s_empirical": [0.048, 0.089], "context_rule": "at least 30 ms aligned gap; typical pre-interruption context not synthesised", "following_gap_s": 0.09999999999999964, "limitation": "no phone identity or tension synthesis; unvoiced continuants excluded", "method": "voiced stable-spectrum edge run", "omissions": "voiced stable edge run \u226590 ms; actual pause context recorded; no phone identity; unvoiced continuants omitted", "pre_pausal": false, "realised_factor": 7.0}
- RHYME_PROLONGATION: {"alignment_error_s_empirical": [0.048, 0.089], "context_rule": "at least 30 ms aligned gap; typical pre-interruption context not synthesised", "following_gap_s": 0.10000000000000009, "limitation": "no phone identity or tension synthesis; unvoiced continuants excluded", "method": "voiced stable-spectrum edge run", "omissions": "voiced stable edge run \u226590 ms; actual pause context recorded; no phone identity; unvoiced continuants omitted", "pre_pausal": false, "realised_factor": 7.0}
- RHYME_PROLONGATION: {"alignment_error_s_empirical": [0.048, 0.089], "context_rule": "at least 30 ms aligned gap; typical pre-interruption context not synthesised", "following_gap_s": 0.10000000000000142, "limitation": "no phone identity or tension synthesis; unvoiced continuants excluded", "method": "voiced stable-spectrum edge run", "omissions": "voiced stable edge run \u226590 ms; actual pause context recorded; no phone identity; unvoiced continuants omitted", "pre_pausal": false, "realised_factor": 5.0}
- RHYME_PROLONGATION: {"alignment_error_s_empirical": [0.048, 0.089], "context_rule": "at least 30 ms aligned gap; typical pre-interruption context not synthesised", "following_gap_s": 0.10000000000000142, "limitation": "no phone identity or tension synthesis; unvoiced continuants excluded", "method": "voiced stable-spectrum edge run", "omissions": "voiced stable edge run \u226590 ms; actual pause context recorded; no phone identity; unvoiced continuants omitted", "pre_pausal": false, "realised_factor": 7.0}
- RHYME_PROLONGATION: {"alignment_error_s_empirical": [0.048, 0.089], "context_rule": "at least 30 ms aligned gap; typical pre-interruption context not synthesised", "following_gap_s": 0.1200000000000001, "limitation": "no phone identity or tension synthesis; unvoiced continuants excluded", "method": "voiced stable-spectrum edge run", "omissions": "voiced stable edge run \u226590 ms; actual pause context recorded; no phone identity; unvoiced continuants omitted", "pre_pausal": false, "realised_factor": 7.0}
- RHYME_PROLONGATION: {"alignment_error_s_empirical": [0.048, 0.089], "context_rule": "at least 30 ms aligned gap; typical pre-interruption context not synthesised", "following_gap_s": 0.120000000000001, "limitation": "no phone identity or tension synthesis; unvoiced continuants excluded", "method": "voiced stable-spectrum edge run", "omissions": "voiced stable edge run \u226590 ms; actual pause context recorded; no phone identity; unvoiced continuants omitted", "pre_pausal": false, "realised_factor": 7.0}
- RHYME_PROLONGATION: {"alignment_error_s_empirical": [0.048, 0.089], "context_rule": "at least 30 ms aligned gap; typical pre-interruption context not synthesised", "following_gap_s": 0.13999999999999702, "limitation": "no phone identity or tension synthesis; unvoiced continuants excluded", "method": "voiced stable-spectrum edge run", "omissions": "voiced stable edge run \u226590 ms; actual pause context recorded; no phone identity; unvoiced continuants omitted", "pre_pausal": false, "realised_factor": 3.0}
- RHYME_PROLONGATION: {"alignment_error_s_empirical": [0.048, 0.089], "context_rule": "at least 30 ms aligned gap; typical pre-interruption context not synthesised", "following_gap_s": 0.13999999999999702, "limitation": "no phone identity or tension synthesis; unvoiced continuants excluded", "method": "voiced stable-spectrum edge run", "omissions": "voiced stable edge run \u226590 ms; actual pause context recorded; no phone identity; unvoiced continuants omitted", "pre_pausal": false, "realised_factor": 5.0}
- RHYME_PROLONGATION: {"alignment_error_s_empirical": [0.048, 0.089], "context_rule": "at least 30 ms aligned gap; typical pre-interruption context not synthesised", "following_gap_s": 0.13999999999999702, "limitation": "no phone identity or tension synthesis; unvoiced continuants excluded", "method": "voiced stable-spectrum edge run", "omissions": "voiced stable edge run \u226590 ms; actual pause context recorded; no phone identity; unvoiced continuants omitted", "pre_pausal": false, "realised_factor": 7.0}
- RHYME_PROLONGATION: {"alignment_error_s_empirical": [0.048, 0.089], "context_rule": "at least 30 ms aligned gap; typical pre-interruption context not synthesised", "following_gap_s": 0.14000000000000057, "limitation": "no phone identity or tension synthesis; unvoiced continuants excluded", "method": "voiced stable-spectrum edge run", "omissions": "voiced stable edge run \u226590 ms; actual pause context recorded; no phone identity; unvoiced continuants omitted", "pre_pausal": false, "realised_factor": 3.0}
- RHYME_PROLONGATION: {"alignment_error_s_empirical": [0.048, 0.089], "context_rule": "at least 30 ms aligned gap; typical pre-interruption context not synthesised", "following_gap_s": 0.14000000000000057, "limitation": "no phone identity or tension synthesis; unvoiced continuants excluded", "method": "voiced stable-spectrum edge run", "omissions": "voiced stable edge run \u226590 ms; actual pause context recorded; no phone identity; unvoiced continuants omitted", "pre_pausal": false, "realised_factor": 5.0}
- RHYME_PROLONGATION: {"alignment_error_s_empirical": [0.048, 0.089], "context_rule": "at least 30 ms aligned gap; typical pre-interruption context not synthesised", "following_gap_s": 0.14000000000000057, "limitation": "no phone identity or tension synthesis; unvoiced continuants excluded", "method": "voiced stable-spectrum edge run", "omissions": "voiced stable edge run \u226590 ms; actual pause context recorded; no phone identity; unvoiced continuants omitted", "pre_pausal": false, "realised_factor": 7.0}
- RHYME_PROLONGATION: {"alignment_error_s_empirical": [0.048, 0.089], "context_rule": "at least 30 ms aligned gap; typical pre-interruption context not synthesised", "following_gap_s": 0.16000000000000014, "limitation": "no phone identity or tension synthesis; unvoiced continuants excluded", "method": "voiced stable-spectrum edge run", "omissions": "voiced stable edge run \u226590 ms; actual pause context recorded; no phone identity; unvoiced continuants omitted", "pre_pausal": false, "realised_factor": 5.0}
- RHYME_PROLONGATION: {"alignment_error_s_empirical": [0.048, 0.089], "context_rule": "at least 30 ms aligned gap; typical pre-interruption context not synthesised", "following_gap_s": 0.16000000000000014, "limitation": "no phone identity or tension synthesis; unvoiced continuants excluded", "method": "voiced stable-spectrum edge run", "omissions": "voiced stable edge run \u226590 ms; actual pause context recorded; no phone identity; unvoiced continuants omitted", "pre_pausal": false, "realised_factor": 7.0}
- RHYME_PROLONGATION: {"alignment_error_s_empirical": [0.048, 0.089], "context_rule": "at least 30 ms aligned gap; typical pre-interruption context not synthesised", "following_gap_s": 0.17999999999999972, "limitation": "no phone identity or tension synthesis; unvoiced continuants excluded", "method": "voiced stable-spectrum edge run", "omissions": "voiced stable edge run \u226590 ms; actual pause context recorded; no phone identity; unvoiced continuants omitted", "pre_pausal": false, "realised_factor": 7.0}
- RHYME_PROLONGATION: {"alignment_error_s_empirical": [0.048, 0.089], "context_rule": "at least 30 ms aligned gap; typical pre-interruption context not synthesised", "following_gap_s": 0.1999999999999993, "limitation": "no phone identity or tension synthesis; unvoiced continuants excluded", "method": "voiced stable-spectrum edge run", "omissions": "voiced stable edge run \u226590 ms; actual pause context recorded; no phone identity; unvoiced continuants omitted", "pre_pausal": false, "realised_factor": 5.0}
- RHYME_PROLONGATION: {"alignment_error_s_empirical": [0.048, 0.089], "context_rule": "at least 30 ms aligned gap; typical pre-interruption context not synthesised", "following_gap_s": 0.1999999999999993, "limitation": "no phone identity or tension synthesis; unvoiced continuants excluded", "method": "voiced stable-spectrum edge run", "omissions": "voiced stable edge run \u226590 ms; actual pause context recorded; no phone identity; unvoiced continuants omitted", "pre_pausal": false, "realised_factor": 7.0}
- RHYME_PROLONGATION: {"alignment_error_s_empirical": [0.048, 0.089], "context_rule": "at least 30 ms aligned gap; typical pre-interruption context not synthesised", "following_gap_s": 0.19999999999999996, "limitation": "no phone identity or tension synthesis; unvoiced continuants excluded", "method": "voiced stable-spectrum edge run", "omissions": "voiced stable edge run \u226590 ms; actual pause context recorded; no phone identity; unvoiced continuants omitted", "pre_pausal": false, "realised_factor": 7.0}
- RHYME_PROLONGATION: {"alignment_error_s_empirical": [0.048, 0.089], "context_rule": "at least 30 ms aligned gap; typical pre-interruption context not synthesised", "following_gap_s": 0.21999999999999975, "limitation": "no phone identity or tension synthesis; unvoiced continuants excluded", "method": "voiced stable-spectrum edge run", "omissions": "voiced stable edge run \u226590 ms; actual pause context recorded; no phone identity; unvoiced continuants omitted", "pre_pausal": false, "realised_factor": 5.0}
- RHYME_PROLONGATION: {"alignment_error_s_empirical": [0.048, 0.089], "context_rule": "at least 30 ms aligned gap; typical pre-interruption context not synthesised", "following_gap_s": 0.21999999999999975, "limitation": "no phone identity or tension synthesis; unvoiced continuants excluded", "method": "voiced stable-spectrum edge run", "omissions": "voiced stable edge run \u226590 ms; actual pause context recorded; no phone identity; unvoiced continuants omitted", "pre_pausal": false, "realised_factor": 7.0}
- RHYME_PROLONGATION: {"alignment_error_s_empirical": [0.048, 0.089], "context_rule": "at least 30 ms aligned gap; typical pre-interruption context not synthesised", "following_gap_s": 0.2200000000000002, "limitation": "no phone identity or tension synthesis; unvoiced continuants excluded", "method": "voiced stable-spectrum edge run", "omissions": "voiced stable edge run \u226590 ms; actual pause context recorded; no phone identity; unvoiced continuants omitted", "pre_pausal": false, "realised_factor": 5.0}
- RHYME_PROLONGATION: {"alignment_error_s_empirical": [0.048, 0.089], "context_rule": "at least 30 ms aligned gap; typical pre-interruption context not synthesised", "following_gap_s": 0.2200000000000002, "limitation": "no phone identity or tension synthesis; unvoiced continuants excluded", "method": "voiced stable-spectrum edge run", "omissions": "voiced stable edge run \u226590 ms; actual pause context recorded; no phone identity; unvoiced continuants omitted", "pre_pausal": false, "realised_factor": 7.0}
- RHYME_PROLONGATION: {"alignment_error_s_empirical": [0.048, 0.089], "context_rule": "at least 30 ms aligned gap; typical pre-interruption context not synthesised", "following_gap_s": 0.240000000000002, "limitation": "no phone identity or tension synthesis; unvoiced continuants excluded", "method": "voiced stable-spectrum edge run", "omissions": "voiced stable edge run \u226590 ms; actual pause context recorded; no phone identity; unvoiced continuants omitted", "pre_pausal": false, "realised_factor": 7.0}
- RHYME_PROLONGATION: {"alignment_error_s_empirical": [0.048, 0.089], "context_rule": "at least 30 ms aligned gap; typical pre-interruption context not synthesised", "following_gap_s": 0.2599999999999998, "limitation": "no phone identity or tension synthesis; unvoiced continuants excluded", "method": "voiced stable-spectrum edge run", "omissions": "voiced stable edge run \u226590 ms; actual pause context recorded; no phone identity; unvoiced continuants omitted", "pre_pausal": false, "realised_factor": 7.0}
- RHYME_PROLONGATION: {"alignment_error_s_empirical": [0.048, 0.089], "context_rule": "at least 30 ms aligned gap; typical pre-interruption context not synthesised", "following_gap_s": 0.3200000000000003, "limitation": "no phone identity or tension synthesis; unvoiced continuants excluded", "method": "voiced stable-spectrum edge run", "omissions": "voiced stable edge run \u226590 ms; actual pause context recorded; no phone identity; unvoiced continuants omitted", "pre_pausal": true, "realised_factor": 7.0}
- RHYME_PROLONGATION: {"alignment_error_s_empirical": [0.048, 0.089], "context_rule": "at least 30 ms aligned gap; typical pre-interruption context not synthesised", "following_gap_s": 0.40000000000000036, "limitation": "no phone identity or tension synthesis; unvoiced continuants excluded", "method": "voiced stable-spectrum edge run", "omissions": "voiced stable edge run \u226590 ms; actual pause context recorded; no phone identity; unvoiced continuants omitted", "pre_pausal": false, "realised_factor": 7.0}
- RHYME_PROLONGATION: {"alignment_error_s_empirical": [0.048, 0.089], "context_rule": "at least 30 ms aligned gap; typical pre-interruption context not synthesised", "following_gap_s": 0.40000000000000213, "limitation": "no phone identity or tension synthesis; unvoiced continuants excluded", "method": "voiced stable-spectrum edge run", "omissions": "voiced stable edge run \u226590 ms; actual pause context recorded; no phone identity; unvoiced continuants omitted", "pre_pausal": true, "realised_factor": 3.0}
- RHYME_PROLONGATION: {"alignment_error_s_empirical": [0.048, 0.089], "context_rule": "at least 30 ms aligned gap; typical pre-interruption context not synthesised", "following_gap_s": 0.40000000000000213, "limitation": "no phone identity or tension synthesis; unvoiced continuants excluded", "method": "voiced stable-spectrum edge run", "omissions": "voiced stable edge run \u226590 ms; actual pause context recorded; no phone identity; unvoiced continuants omitted", "pre_pausal": true, "realised_factor": 5.0}
- RHYME_PROLONGATION: {"alignment_error_s_empirical": [0.048, 0.089], "context_rule": "at least 30 ms aligned gap; typical pre-interruption context not synthesised", "following_gap_s": 0.40000000000000213, "limitation": "no phone identity or tension synthesis; unvoiced continuants excluded", "method": "voiced stable-spectrum edge run", "omissions": "voiced stable edge run \u226590 ms; actual pause context recorded; no phone identity; unvoiced continuants omitted", "pre_pausal": true, "realised_factor": 7.0}
- RHYME_PROLONGATION: {"alignment_error_s_empirical": [0.048, 0.089], "context_rule": "at least 30 ms aligned gap; typical pre-interruption context not synthesised", "following_gap_s": 0.5399999999999991, "limitation": "no phone identity or tension synthesis; unvoiced continuants excluded", "method": "voiced stable-spectrum edge run", "omissions": "voiced stable edge run \u226590 ms; actual pause context recorded; no phone identity; unvoiced continuants omitted", "pre_pausal": true, "realised_factor": 7.0}
- RHYME_PROLONGATION: {"alignment_error_s_empirical": [0.048, 0.089], "context_rule": "at least 30 ms aligned gap; typical pre-interruption context not synthesised", "following_gap_s": 0.5999999999999979, "limitation": "no phone identity or tension synthesis; unvoiced continuants excluded", "method": "voiced stable-spectrum edge run", "omissions": "voiced stable edge run \u226590 ms; actual pause context recorded; no phone identity; unvoiced continuants omitted", "pre_pausal": true, "realised_factor": 7.0}
- RHYME_PROLONGATION: {"alignment_error_s_empirical": [0.048, 0.089], "context_rule": "at least 30 ms aligned gap; typical pre-interruption context not synthesised", "following_gap_s": 0.5999999999999996, "limitation": "no phone identity or tension synthesis; unvoiced continuants excluded", "method": "voiced stable-spectrum edge run", "omissions": "voiced stable edge run \u226590 ms; actual pause context recorded; no phone identity; unvoiced continuants omitted", "pre_pausal": true, "realised_factor": 7.0}
- RHYME_PROLONGATION: {"alignment_error_s_empirical": [0.048, 0.089], "context_rule": "at least 30 ms aligned gap; typical pre-interruption context not synthesised", "following_gap_s": 0.7199999999999989, "limitation": "no phone identity or tension synthesis; unvoiced continuants excluded", "method": "voiced stable-spectrum edge run", "omissions": "voiced stable edge run \u226590 ms; actual pause context recorded; no phone identity; unvoiced continuants omitted", "pre_pausal": true, "realised_factor": 5.0}
- RHYME_PROLONGATION: {"alignment_error_s_empirical": [0.048, 0.089], "context_rule": "at least 30 ms aligned gap; typical pre-interruption context not synthesised", "following_gap_s": 0.7199999999999989, "limitation": "no phone identity or tension synthesis; unvoiced continuants excluded", "method": "voiced stable-spectrum edge run", "omissions": "voiced stable edge run \u226590 ms; actual pause context recorded; no phone identity; unvoiced continuants omitted", "pre_pausal": true, "realised_factor": 7.0}
- RHYME_PROLONGATION: {"alignment_error_s_empirical": [0.048, 0.089], "context_rule": "at least 30 ms aligned gap; typical pre-interruption context not synthesised", "following_gap_s": 0.9800000000000004, "limitation": "no phone identity or tension synthesis; unvoiced continuants excluded", "method": "voiced stable-spectrum edge run", "omissions": "voiced stable edge run \u226590 ms; actual pause context recorded; no phone identity; unvoiced continuants omitted", "pre_pausal": true, "realised_factor": 7.0}
- RHYME_PROLONGATION: {"alignment_error_s_empirical": [0.048, 0.089], "context_rule": "at least 30 ms aligned gap; typical pre-interruption context not synthesised", "following_gap_s": 1.0599999999999996, "limitation": "no phone identity or tension synthesis; unvoiced continuants excluded", "method": "voiced stable-spectrum edge run", "omissions": "voiced stable edge run \u226590 ms; actual pause context recorded; no phone identity; unvoiced continuants omitted", "pre_pausal": true, "realised_factor": 3.0}
- RHYME_PROLONGATION: {"alignment_error_s_empirical": [0.048, 0.089], "context_rule": "at least 30 ms aligned gap; typical pre-interruption context not synthesised", "following_gap_s": 1.0599999999999996, "limitation": "no phone identity or tension synthesis; unvoiced continuants excluded", "method": "voiced stable-spectrum edge run", "omissions": "voiced stable edge run \u226590 ms; actual pause context recorded; no phone identity; unvoiced continuants omitted", "pre_pausal": true, "realised_factor": 5.0}
- RHYME_PROLONGATION: {"alignment_error_s_empirical": [0.048, 0.089], "context_rule": "at least 30 ms aligned gap; typical pre-interruption context not synthesised", "following_gap_s": 1.0599999999999996, "limitation": "no phone identity or tension synthesis; unvoiced continuants excluded", "method": "voiced stable-spectrum edge run", "omissions": "voiced stable edge run \u226590 ms; actual pause context recorded; no phone identity; unvoiced continuants omitted", "pre_pausal": true, "realised_factor": 7.0}
- RHYME_PROLONGATION: {"alignment_error_s_empirical": [0.048, 0.089], "context_rule": "at least 30 ms aligned gap; typical pre-interruption context not synthesised", "following_gap_s": 1.1600000000000001, "limitation": "no phone identity or tension synthesis; unvoiced continuants excluded", "method": "voiced stable-spectrum edge run", "omissions": "voiced stable edge run \u226590 ms; actual pause context recorded; no phone identity; unvoiced continuants omitted", "pre_pausal": true, "realised_factor": 5.0}
- RHYME_PROLONGATION: {"alignment_error_s_empirical": [0.048, 0.089], "context_rule": "at least 30 ms aligned gap; typical pre-interruption context not synthesised", "following_gap_s": 1.1600000000000001, "limitation": "no phone identity or tension synthesis; unvoiced continuants excluded", "method": "voiced stable-spectrum edge run", "omissions": "voiced stable edge run \u226590 ms; actual pause context recorded; no phone identity; unvoiced continuants omitted", "pre_pausal": true, "realised_factor": 7.0}
- RHYME_PROLONGATION: {"alignment_error_s_empirical": [0.048, 0.089], "context_rule": "at least 30 ms aligned gap; typical pre-interruption context not synthesised", "following_gap_s": null, "limitation": "no phone identity or tension synthesis; unvoiced continuants excluded", "method": "voiced stable-spectrum edge run", "omissions": "voiced stable edge run \u226590 ms; actual pause context recorded; no phone identity; unvoiced continuants omitted", "pre_pausal": true, "realised_factor": 7.0}
- RISING_ENDING: {"actual_window_s": 0.16, "alignment_error_s_empirical": [0.048, 0.089], "method": "last 250 ms, clipped to final word; no syllable boundary assumed", "omissions": "add ramp to natural contour; clipped to final word; PSOLA approximate; no syllable annotation", "rise_extent": "first to last parent voiced frame inside window"}
- RISING_ENDING: {"actual_window_s": 0.18, "alignment_error_s_empirical": [0.048, 0.089], "method": "last 250 ms, clipped to final word; no syllable boundary assumed", "omissions": "add ramp to natural contour; clipped to final word; PSOLA approximate; no syllable annotation", "rise_extent": "first to last parent voiced frame inside window"}
- RISING_ENDING: {"actual_window_s": 0.2, "alignment_error_s_empirical": [0.048, 0.089], "method": "last 250 ms, clipped to final word; no syllable boundary assumed", "omissions": "add ramp to natural contour; clipped to final word; PSOLA approximate; no syllable annotation", "rise_extent": "first to last parent voiced frame inside window"}
- RISING_ENDING: {"actual_window_s": 0.22, "alignment_error_s_empirical": [0.048, 0.089], "method": "last 250 ms, clipped to final word; no syllable boundary assumed", "omissions": "add ramp to natural contour; clipped to final word; PSOLA approximate; no syllable annotation", "rise_extent": "first to last parent voiced frame inside window"}
- RISING_ENDING: {"actual_window_s": 0.24, "alignment_error_s_empirical": [0.048, 0.089], "method": "last 250 ms, clipped to final word; no syllable boundary assumed", "omissions": "add ramp to natural contour; clipped to final word; PSOLA approximate; no syllable annotation", "rise_extent": "first to last parent voiced frame inside window"}
- RISING_ENDING: {"actual_window_s": 0.25, "alignment_error_s_empirical": [0.048, 0.089], "method": "last 250 ms, clipped to final word; no syllable boundary assumed", "omissions": "add ramp to natural contour; clipped to final word; PSOLA approximate; no syllable annotation", "rise_extent": "first to last parent voiced frame inside window"}
- SOUND_REPETITION: {"alignment_error_s_empirical": [0.048, 0.089], "limitation": "no articulatory tension synthesis; onset may include more than one phone", "method": "first 20% onset copy; phone boundary unknown", "omissions": "first 20% onset copy; stress fallback recorded; no tension; duration/level variation chosen", "own_stressed": false, "selection": "shared stress preferred, own stress then eligible content fallback; signal eligibility", "stress_fallback": "shared stress"}
- SOUND_REPETITION: {"alignment_error_s_empirical": [0.048, 0.089], "limitation": "no articulatory tension synthesis; onset may include more than one phone", "method": "first 20% onset copy; phone boundary unknown", "omissions": "first 20% onset copy; stress fallback recorded; no tension; duration/level variation chosen", "own_stressed": false, "selection": "shared stress preferred, own stress then eligible content fallback; signal eligibility"}
- SOUND_REPETITION: {"alignment_error_s_empirical": [0.048, 0.089], "limitation": "no articulatory tension synthesis; onset may include more than one phone", "method": "first 20% onset copy; phone boundary unknown", "omissions": "first 20% onset copy; stress fallback recorded; no tension; duration/level variation chosen", "own_stressed": true, "selection": "shared stress preferred, own stress then eligible content fallback; signal eligibility", "stress_fallback": "own stress fallback"}
- SOUND_REPETITION: {"alignment_error_s_empirical": [0.048, 0.089], "limitation": "no articulatory tension synthesis; onset may include more than one phone", "method": "first 20% onset copy; phone boundary unknown", "omissions": "first 20% onset copy; stress fallback recorded; no tension; duration/level variation chosen", "own_stressed": true, "selection": "shared stress preferred, own stress then eligible content fallback; signal eligibility", "stress_fallback": "shared stress"}
- SOUND_REPETITION: {"alignment_error_s_empirical": [0.048, 0.089], "limitation": "no articulatory tension synthesis; onset may include more than one phone", "method": "first 20% onset copy; phone boundary unknown", "omissions": "first 20% onset copy; stress fallback recorded; no tension; duration/level variation chosen", "own_stressed": true, "selection": "shared stress preferred, own stress then eligible content fallback; signal eligibility"}
- TRAILING_OFF: {"limitation": "lax/irregular phonation omitted; tilt fitted to alpha coupling; no published severity cutoffs", "method": "last three words gain/tilt ramp with 100 ms release; final-waveform alpha on parent speech", "omissions": "last three words; 100 ms release; tilt fitted after mixing; lax/irregular phonation omitted"}
- UNEVEN_TEMPO: {"method": "aligned word spans", "omissions": "nominal mean one; integer rounding; no syllable rhythm model"}
- WORD_BY_WORD: {"limitation": "L1 inserted 150 ms can be below 200 ms pause threshold including raw gap", "method": "internal 30 ms non-pausal gap energy minima", "omissions": "internal eligible gaps only; L1 may be below 200 ms pause threshold"}
- WORD_REPETITION: {"method": "function-word prior; copied waveform", "omissions": "function-word copy; duration \u00b18% and gain \u00b11 dB chosen; no tension/F0 variation"}

Extra L1–L3 share a placement plan per parent and set; botched family clips use repeated L3 edits and longer windows.
Wrong-sign, below-half-target, missing-measurement and non-monotone edits are excluded from evaluation truth and h selection; counts are reported in a separate shortfall stratum. Coupling warnings alone remain eligible for level-only evaluation.
Burst/continuant signal gates are heuristic; skipped placements record missing acoustic eligibility.
Total audio minutes (including clean recordings): 1109.2. Filled pauses are excluded.
