# Acoustic Features: Librosa

This repository contains scripts that show examples of how to use the [Librosa Python library](https://github.com/librosa/librosa) to generate acoustic features including [Spectral features and Rhythm features](https://librosa.org/doc/latest/feature.html). The scripts can be run without [Docker](https://docs.docker.com/engine/install/) or with it.

## Installation and Setup

### Python Requirements
```
librosa
   |-- requirements
   |   |-- py3-13-1
   |   |   |-- Dockerfile
   |   |   |-- build_docker.sh
   |   |   |-- requirements.txt
   |   |   |-- run_docker.sh
```
Check your Python version:
```sh
python --version
```
See [Anaconda](https://www.anaconda.com/download/success) as an option to switch between Python versions.

Install requirements for Python 3.13.1:
```sh
pip install -r requirements/py3-13-1/requirements.txt 
```

If using a different version of Python, run the following command:
```
pip install librosa
```

### Requirements.txt License Information
License information for each set of requirements.txt can be found in their respective `pip-licenses.md` file within the requirements/python[version] folders.

### Docker Support
[Docker](https://docs.docker.com/engine/install/) support can be found via the `Dockerfile` and `build_docker.sh` and `run_docker.sh` files.

Please see Docker's documentation for more information ([docker build](https://docs.docker.com/build/), [Dockerfile](https://docs.docker.com/build/concepts/dockerfile/), [docker run](https://docs.docker.com/reference/cli/docker/container/run/)).

## Extracting Acoustic Features

See `extract_features.main()` for usage examples. The `librosa_feature_extraction.extract_librosa_feature()` function takes in an input audio filepath (`audio_fp`), feature name (`feature_name`) and a set of keyword arguments:

audio_fp, feature_name, **kwargs

| Keyword Argument | Type | Description | Default Value| 
| - | - | - | - | 
| sampling_rate | int | Resample to this rate before generating features. | None (uses original sampling rate) |
| to_mono | boolean | Set to True to convert the file to mono. | False |
| out_root | str | Root folder that the output files are written to. | output/ |
| csv_out | str | CSV filepath that the features are written to. | Combines the out_root, feature_name, sampling_rate, and the input audio's filename into a filepath. |
| load_kwargs | dict | Any additional optional arguments to pass to librosa.load | None |
| extraction_kwargs | dict | Any additional optional arguments to pass to the librosa feature. | None |

Note: Each Librosa Feature includes unique optional KWARGS. Please see the the links to the Librosa Documentation assoicated with each feature for the full list. If using additional KWARGS, these should be included in extraction_kwargs.

### Spectral Features

| Feature Name | Description | Librosa Documentation |
|---|---|---|
| chroma_stft | Compute a chromagram from a waveform or power spectrogram. | [librosa.feature.chroma_stft](https://librosa.org/doc/latest/generated/librosa.feature.chroma_stft.html#librosa.feature.chroma_stft) |
| chroma_cqt | Constant-Q chromagram. | [librosa.feature.chroma_cqt](https://librosa.org/doc/latest/generated/librosa.feature.chroma_cqt.html#librosa.feature.chroma_cqt) |
| chroma_cens | Compute the chroma variant “Chroma Energy Normalized” (CENS). | [librosa.feature.chroma_cens](http://librosa.org/doc/latest/generated/librosa.feature.chroma_cens.html#librosa.feature.chroma_cens) |
| chroma_vqt | Variable-Q chromagram. | [librosa.feature.chroma_vqt](https://librosa.org/doc/latest/generated/librosa.feature.chroma_vqt.html#librosa.feature.chroma_vqt) |
| melspectrogram | Compute a mel-scaled spectrogram. | [librosa.feature.melspectrogram](http://librosa.org/doc/latest/generated/librosa.feature.melspectrogram.html#librosa.feature.melspectrogram) |
| mfcc | Mel-frequency cepstral coefficients (MFCCs). | [librosa.feature.mfcc](http://librosa.org/doc/latest/generated/librosa.feature.mfcc.html#librosa.feature.mfcc) |
| rms | Compute root-mean-square (RMS) value for each frame, either from the audio samples y or from a spectrogram S. | [librosa.feature.rms](https://librosa.org/doc/latest/generated/librosa.feature.rms.html#librosa.feature.rms) |
| spectral_centroid | Compute the spectral centroid. | [librosa.feature.spectral_centroid](https://librosa.org/doc/latest/generated/librosa.feature.spectral_centroid.html#librosa.feature.spectral_centroid) |
| spectral_bandwidth | Compute p’th-order spectral bandwidth. | [librosa.feature.spectral_bandwidth](https://librosa.org/doc/latest/generated/librosa.feature.spectral_bandwidth.html#librosa.feature.spectral_bandwidth) |
| spectral_contrast | Compute spectral contrast. | [librosa.feature.spectral_contrast](https://librosa.org/doc/latest/generated/librosa.feature.spectral_contrast.html#librosa.feature.spectral_contrast) |
| spectral_flatness | Compute spectral flatness. | [librosa.feature.spectral_flatness](https://librosa.org/doc/latest/generated/librosa.feature.spectral_flatness.html#librosa.feature.spectral_flatness) |
| spectral_rolloff | Compute roll-off frequency. | [librosa.feature.spectral_rolloff](https://librosa.org/doc/latest/generated/librosa.feature.spectral_rolloff.html#librosa.feature.spectral_rolloff) |
| poly_features | Get coefficients of fitting an nth-order polynomial to the columns of a spectrogram. | [librosa.feature.poly_features](https://librosa.org/doc/latest/generated/librosa.feature.poly_features.html#librosa.feature.poly_features) |
| tonnetz | Compute the tonal centroid features (tonnetz). | [librosa.feature.tonnetz](https://librosa.org/doc/latest/generated/librosa.feature.tonnetz.html#librosa.feature.tonnetz) |
| zero_crossing_rate | Compute the zero-crossing rate of an audio time series. | [librosa.feature.zero_crossing_rate](https://librosa.org/doc/latest/generated/librosa.feature.zero_crossing_rate.html#librosa.feature.zero_crossing_rate) |


### Rhythm Features

| Feature Name | Description | Librosa Documentation |
|---|---|---|
| tempo | Estimate the tempo (beats per minute). | [librosa.feature.tempo](https://librosa.org/doc/latest/generated/librosa.feature.tempo.html#librosa.feature.tempo) |
| tempogram | Compute the tempogram: local autocorrelation of the onset strength envelope. | [librosa.feature.tempogram](https://librosa.org/doc/latest/generated/librosa.feature.tempogram.html#librosa.feature.tempogram) |
| fourier_tempogram | Compute the Fourier tempogram: the short-time Fourier transform of the onset strength envelope. | [librosa.feature.fourier_tempogram](http://librosa.org/doc/latest/generated/librosa.feature.fourier_tempogram.html#librosa.feature.fourier_tempogram) |
| tempogram_ratio | Tempogram ratio features, also known as spectral rhythm patterns. | [librosa.feature.tempogram_ratio](https://librosa.org/doc/latest/generated/librosa.feature.tempogram_ratio.html#librosa.feature.tempogram_ratio) |

## Usage Example

The `extract_features.py` script generates each of the spectral and rhythm features described above on the provided sample WAV file.

If you would like to run feature extractions on the sample audio file using Docker, you must move any files into the `acoustic-features/librosa` path to ensure it is within the build context. Adjust the filepath in your call accordingly. 

```python
 from librosa_feature_extraction import extract_librosa_features
 extract_librosa_features(YOUR_WAV_FILEPATH, FEATURE_NAME, OPTIONAL_KWARGS)
```

For instance, you could run:
```python
 from librosa_feature_extraction import extract_librosa_features
 extract_librosa_features('../sample_audio/first_ten_Sample_HV_Clip.wav', 'melspectrogram', sampling_rate=16000)
```

This would output the computed mel-scaled spectrogram for the audio file resampled to 16KHz. Leaving sample_rate unset will use the original audio file's sampling rate instead.

You can an example of running the feature extraction for all supported features in `extract_features.main()`.

Please note that in our example shown in `extract_features.main()`, the features are all sharing the same value for `extraction_kwargs`, which is empty. If you wish to specify specific KWARGS for only certain features, you may wish to adjust main to provide unique `extraction_kwargs` for each feature. 

## Sample Input
```
sample_audio
   |-- first_ten_Sample_HV_Clip.wav
```

### Sample Output
The sample hierarchy below shows the files created in python3-13-1 (Windows). The files created in python3-9-6 (Windows) and debian_docker_python3-9-6 (Debian via Docker) follow the same structure.
```
librosa
   |-- output
   |   |-- first_ten_Sample_HV_Clip_chroma_cens_16KHz.npy
   |   |-- first_ten_Sample_HV_Clip_chroma_cqt_16KHz.npy
   |   |-- first_ten_Sample_HV_Clip_chroma_stft.npy
   |   |-- first_ten_Sample_HV_Clip_chroma_stft_16KHz.npy
   |   |-- first_ten_Sample_HV_Clip_chroma_vqt_16KHz.npy
   |   |-- first_ten_Sample_HV_Clip_fourier_tempogram_16KHz.npy
   |   |-- first_ten_Sample_HV_Clip_melspectrogram_16KHz.npy
   |   |-- first_ten_Sample_HV_Clip_mfcc_16KHz.npy
   |   |-- first_ten_Sample_HV_Clip_poly_features_16KHz.npy
   |   |-- first_ten_Sample_HV_Clip_rms_16KHz.npy
   |   |-- first_ten_Sample_HV_Clip_spectral_bandwidth_16KHz.npy
   |   |-- first_ten_Sample_HV_Clip_spectral_centroid_16KHz.npy
   |   |-- first_ten_Sample_HV_Clip_spectral_contrast_16KHz.npy
   |   |-- first_ten_Sample_HV_Clip_spectral_flatness_16KHz.npy
   |   |-- first_ten_Sample_HV_Clip_spectral_rolloff_16KHz.npy
   |   |-- first_ten_Sample_HV_Clip_tempo_16KHz.npy
   |   |-- first_ten_Sample_HV_Clip_tempogram_16KHz.npy
   |   |-- first_ten_Sample_HV_Clip_tempogram_ratio_16KHz.npy
   |   |-- first_ten_Sample_HV_Clip_tonnetz_16KHz.npy
   |   |-- first_ten_Sample_HV_Clip_zero_crossing_rate_16KHz.npy
```

## Citations
If you use this in your research, please cite:
```bibtex
@inproceedings{mcfee2015librosa,
  title={librosa: Audio and music signal analysis in Python},
  author={McFee, Brian and Raffel, Colin and Liang, Dawen and Ellis, Daniel PW and McVicar, Matt and Battenberg, Eric and Nieto, Oriol},
  booktitle={Proceedings of the 14th Python in Science Conference},
  pages={18--25},
  year={2015},
  doi={10.5281/zenodo.1172065},
  url={https://zenodo.org/badge/6309729.svg}
}
```