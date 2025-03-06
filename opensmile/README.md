# openSMILE Docker Examples

> Examples of using the openSMILE Python library with and without [Docker.](https://docs.docker.com/engine/install/)

This repository contains scripts that show examples of how to use the [openSMILE Python library](https://audeering.github.io/opensmile-python/) to generate Low Level Descriptors (LLDs) and Functionals from the ComParE 2016 feature set. The scripts can be run with and without Docker.

## Installation

### Without Docker

The requirements.txt file can be used to install the necessary libraries without utilizing a Docker environment. Python 3.9.18 was used to develop and test these scripts. We currently have support for both Python 3.9.18 and 3.13.1.
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
If you do not have the supported Python versions installed, you may need to adjust the requirements.txt for compatibility with your Python version. Alternatively, you can run the scripts using Docker.

### With Docker

[Docker](https://docs.docker.com/engine/install/) is required for building and running the docker container. Docker version 24.0.6, build ed223bc was used to develop and test these scripts.

Run the necessary docker build and run commands provided in the build_docker.sh and run_docker.sh scripts.

```sh
./build_docker.sh
./run_docker.sh
```
These commands have been written to be run on Linux.

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

- LowLevelDescriptors (lld)
- Functionals (func)
- LowLevelDescriptors_Deltas (lld_de)

See [Opensmile's FeatureLevel documentation](https://audeering.github.io/opensmile-python/api/opensmile.FeatureLevel.html) for further details.

### FeatureSet Options

- ComParE_2016
- eGeMAPSv01a
- eGeMAPSv01b
- eGeMAPSv02
- GeMAPSv01a
- GeMAPSv01b

See [Opensmile's FeatureSet documentation](https://audeering.github.io/opensmile-python/api/opensmile.FeatureSet.html#opensmile.FeatureSet) for further details.

## Usage Example

The `extract_features.py` script generates:
- LLDs using ComParE_2016 as the on the provided sample WAV file.
- LLDs using eGeMAPSv02 as the on the provided sample WAV file.
- Functionals using ComParE_2016 as the on the provided sample WAV file.
- Functionals using GeMAPSv01b as the on the provided sample WAV file.

### Sample Input and Output Files

* Sample Input: 
    * sample_wav/
        * first_ten_Sample_HV_Clip.wav contains a 10-second WAV clip.
* Sample Output:
    * sample_out/
        * first_ten_Sample_HV_Clip_lld_ComParE_2016.csv
        * first_ten_Sample_HV_Clip_lld_eGeMAPSv02.csv
        * first_ten_Sample_HV_Clip_func_ComParE_2016.csv
        * first_ten_Sample_HV_Clip_func_GeMAPSv01b.csv

## Acknowledgement
- [openSMILE](https://github.com/audeering/opensmile): Open-source Speech and Music Interpretation by Large-space Extraction (License audEERING GmbH)

## Citations
If you use this in your research, please cite this repo:
```bibtex
@misc{fhsbap2024vfetopensmile,
  title={Voice-Feature-Extraction-Toolkit/opensmile},
  author={Karjadi, Cody},
  journal={GitHub repository},
  year={2024},
  publisher={GitHub},
  howpublished = {\url{https://github.com/FHS-BAP/Voice-Feature-Extraction-Toolkit/tree/main/opensmile}}
}
```
and the openSMILE paper:
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
