# Acoustic Features: openSMILE

This repository contains scripts that show examples of how to use the [openSMILE Python library](https://audeering.github.io/opensmile-python/) to generate acoustic features via various feature levels from several feature sets. The scripts can be run with and without Docker.

## Installation

### Without Docker

The requirements.txt file can be used to install the necessary libraries without utilizing a Docker environment.

Check your Python version:
```sh
python --version
```
Install requirements for Python 3.9.18:
```sh
pip install -r python39_requirements.txt
```
Install requirements for Python 3.13.1:
```sh
pip install -r python313_requirements.txt
```
If you do not have the supported Python versions installed, you may run the following installation:
```sh
pip install opensmile
```
Alternatively, you can run the scripts in a Docker environment.

### With Docker

[Docker](https://docs.docker.com/engine/install/) is required for building and running the docker container. Docker version 24.0.6, build ed223bc was used to develop and test these scripts.

Run the necessary docker build and run commands provided in the build_docker.sh and run_docker.sh scripts. These .sh scripts were tested on Linux (CentOS 7).

```sh
./build_docker.sh
./run_docker.sh
```

## Extracting Acoustic Features

After installation, navigate to `extract_features.py`. In `main()`, you may adjust the arguments passed into `extract()` to include:
- A .WAV file for which you wish to generate features
- feat_level: an optional kwarg that determines which FeatureLevel is used
- feat_set: an optional kwarg that determines which FeatureSet is used

If no kwargs are defined, the script will default to the LowLevelDescriptors FeatureLevel and ComParE_2016 FeatureSet.

Once adjusted, run:
```sh
python extract_features.py
```
You will find your output in sample_out/

### FeatureLevel Options

| FeatureLevel Name          | Argument Mapping |
|----------------------------|------------------|
| LowLevelDescriptors        | lld              |
| Functionals                | func             |
| LowLevelDescriptors_Deltas | lld_de           |

The argument mappings are not case sensitive.
See [openSMILE's FeatureLevel documentation](https://audeering.github.io/opensmile-python/api/opensmile.FeatureLevel.html) for further details.

### FeatureSet Options

| FeatureSet Name | Argument Mapping |
|-----------------|------------------|
| ComParE_2016    | compare_2016     |
| eGeMAPSv02      | egemapsv02       |
| GeMAPSv01b      | gemapsv01b       |

The argument mappings are not case sensitive.
See [openSMILE's FeatureSet documentation](https://audeering.github.io/opensmile-python/api/opensmile.FeatureSet.html#opensmile.FeatureSet) for further details.

## Usage Example

The `extract_features.py` script generates the below and repeats it with resampling to 16KHz prior to feature generation:
- LLDs using ComParE_2016 as the on the provided sample WAV file.
- Functionals using ComParE_2016 as the on the provided sample WAV file.
- LLD_DE's using ComParE_2016 as the on the provided sample WAV file.
- LLDs using eGeMAPSv02 as the on the provided sample WAV file.
- Functionals using eGeMAPSv02 as the on the provided sample WAV file.
- LLDs using GeMAPSv01b as the on the provided sample WAV file.
- Functionals using GeMAPSv01b as the on the provided sample WAV file.

### Sample Input and Output Files

* Sample Input: 
    * sample_wav/
        * first_ten_Sample_HV_Clip.wav contains a 10-second WAV clip.
* Sample Output:
    * sample_out/
        * compare_2016/
            * first_ten_Sample_HV_Clip_lld_compare_2016.csv
            * first_ten_Sample_HV_Clip_func_compare_2016.csv
            * first_ten_Sample_HV_Clip_lld_de_Compare_2016.csv
            * 16KHz/
                * first_ten_Sample_HV_Clip_lld_compare_2016_16KHz.csv
                * first_ten_Sample_HV_Clip_func_compare_2016_16KHz.csv
                * first_ten_Sample_HV_Clip_lld_de_compare_2016_16KHz.csv
        * egemapsv02/
            * first_ten_Sample_HV_Clip_lld_egemapsv02.csv
            * first_ten_Sample_HV_Clip_func_egemapsv02.csv
            * 16KHz/
                * first_ten_Sample_HV_Clip_lld_egemapsv02_16KHz.csv
                * first_ten_Sample_HV_Clip_func_egemapsv02_16KHz.csv
        * gemapsv02b/
            * first_ten_Sample_HV_Clip_lld_gemapsv01b.csv
            * first_ten_Sample_HV_Clip_func_gemapsv01b.csv
            * 16KHz/
                * first_ten_Sample_HV_Clip_lld_gemapsv01b_16KHz.csv
                * first_ten_Sample_HV_Clip_func_gemapsv01b_16KHz.csv

Python usage:

```python
 from osm import extract_osm_features
 extract_osm_features(YOUR_WAV_FILEPATH, OPTIONAL_KWARGS)
```
For instance, you could run:
```python
 from osm import extract_osm_features
 extract_osm_features('sample_wav/first_ten_Sample_HV_Clip.wav', feat_level='func', feat_set='eGeMAPSv02', sampling_rate=16000)
```
This would output the features extracted using functionals as the FeatureLevel, eGeMAPSv02 as the FeatureSet and would resample the audio file to 16KHz.

You can see our examples described above by looking at `extract_features.main()`.

### Keyword Arguments and Default Values (osm.extract_osm_features()):

| Keyword Argument | Description | Default Value| 
| - | - | - |
| feat_level | Feature Level to be used. | lld |
| feat_set | Feature Set to be used. | compare_2016 |
| sampling_rate | Sampling Rate to resample to before generating features. | None (uses original sampling rate) |
| channels | The audio channel(s) to be processed. The default is the first channel. | [0] |
| resample | Set to True if sampling_rate is not None. | NA |
| out_root | Root folder that the output files are written to. | sample_out/ |
| csv_out | CSV filepath that the features are written to. | Combines the out_root, feat_set, sampling_rate (if any), original name of the input file into a filepath. |

## Acknowledgement
- [openSMILE](https://github.com/audeering/opensmile): Open-source Speech and Music Interpretation by Large-space Extraction (License audEERING GmbH)

## Citations
If you use this in your research, please cite the openSMILE paper:
```bibtex
@article{eyben2010opensmile,
  title={openSMILE - The Munich Versatile and Fast Open-Source Audio Feature Extractor},
  author={Eyben, Florian and Wöllmer, Martin and Schuller, Björn},
  booktitle={Proc. ACM Multimedia (MM)},
  organization={ACM},
  address={Florence, Italy},
  isbn={978-1-60558-933-6},
  pages={1459-1462},
  year={2010}
}
```