# Comparison of feature extraction and sampling methods

`comparison/` holds files that include checks that we used when developing this script. The main comparisons are:
- Using [openSMILE](https://www.audeering.com/research/opensmile/)'s process_file and process_signal
- Resampling using sample_rate with openSMILE and resampling using [ffmpeg](https://ffmpeg.org/)
- Using a mono-channel audio file with the channels parameter

The outputs from running `compare.py` include CSVs comparing each FeatureSet and FeatureLevel combination and a CSV with a summary from taking the cosine similarity between the two files specified.

### In this directory
- Process signal versus process file
    - `process_file_out/`: output from extracting features using process_file
    - `process_signal_out/`: output from extracting features using process_signal
    - `process_signal_out_x_process_file_out/`: holds results from the running `comparison.py`
- openSMILE resample versus ffmpeg downsample
    - `resample_out/`: output from extracting features using process_file
    - `downsample_out/`: output from extracting features with a file already resampled using ffmpeg
    - `resample_out_x_downsample_out/`: holds results from the running `comparison.py`
- Process signal versus process file
    - `process_file_out/`: output from extracting features using process_file
    - `mono_out/`: output from extracting features on a file that has only one channel
    - `process_file_out_x_mono_out/`: holds results from the running `comparison.py`

If you wish to compare other files, please see `compare.py` and adjust as needed. Keep in mind that this script will only compare two CSVs with the same column headers. 
You will also additionally need to install [scikit-learn](https://scikit-learn.org/stable/install.html):
```sh
pip install -U scikit-learn
```