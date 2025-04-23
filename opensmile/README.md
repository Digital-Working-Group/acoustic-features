# Acoustic Features: openSMILE

This repository contains scripts that show examples of how to use the [openSMILE Python library](https://audeering.github.io/opensmile-python/) to generate acoustic features via various feature levels from several feature sets. The scripts can be run without [Docker](https://docs.docker.com/engine/install/) or with it.

## Installation

### Without Docker

Check your Python version:
```sh
python --version
```
Install requirements for Python 3.9.6:
```sh
pip install -r python3-9-6_requirements.txt
```
Install requirements for Python 3.13.1:
```sh
pip install -r python3-13-1_requirements.txt
```
If using a different Python version, you may run the following pip commands:
```sh
pip install opensmile
pip install scikit-learn
```
Alternatively, you can run the scripts in a Docker environment.

### With Docker

[Docker](https://docs.docker.com/engine/install/) is required for building and running the docker container. Docker version 24.0.6, build ed223bc was used to develop and test these scripts.

Run the necessary docker build and run commands provided in the build_docker.sh and run_docker.sh scripts. These .sh scripts were tested on Linux (CentOS 7).

```sh
./build_docker.sh
./run_docker.sh
```

The Docker commands included in the .sh scripts are:
```sh
docker build -t $docker_name .
## build the container image under the name 'docker_name' based on the Dockerfile specifications
docker run -v $(pwd):/scripts -it --rm --name $container_name $docker_name bash
## run the built container image ('docker_name') under the container name 'container_name'
## mounts the current working directory $(pwd) as a volume to /scripts within the container
```

Please see Docker's documentation for more information ([docker build](https://docs.docker.com/build/), [Dockerfile](https://docs.docker.com/build/concepts/dockerfile/), [docker run](https://docs.docker.com/reference/cli/docker/container/run/)).

## Extracting Acoustic Features

See `extract_features.main()` for usage examples. The `osm.extract_osm_features()` function takes in an input audio filepath (`audio_fp`) and a set of keyword arguments:

| Keyword Argument | Type | Description | Default Value| 
| - | - | - | - | 
| feat_level | str |FeatureLevel to be used. | lld |
| feat_set | str | FeatureSet to be used. | compare_2016 |
| sampling_rate | int | Sampling Rate to resample to before generating features. | None (uses original sampling rate) |
| channels | list\<int\> |The audio channel(s) to be processed. The default is the first channel. | [0] |
| resample | boolean | Set to True if sampling_rate is not None. | NA |
| out_root | str | Root folder that the output files are written to. | The parent directory of the input audio filepath (audio_fp). |
| csv_out | str | CSV filepath that the features are written to. | Combines the out_root, feat_set, sampling_rate, feat_level, and the input audio's filename into a filepath. |

### FeatureLevel Options

| FeatureLevel          | Argument Mapping |
|----------------------------|------------------|
| LowLevelDescriptors        | lld              |
| Functionals                | func             |
| LowLevelDescriptors_Deltas | lld_de           |

The argument mappings are not case sensitive.
See [openSMILE's FeatureLevel documentation](https://audeering.github.io/opensmile-python/api/opensmile.FeatureLevel.html) for further details.

### FeatureSet Options

| FeatureSet | Argument Mapping |
|-----------------|------------------|
| ComParE_2016    | compare_2016     |
| eGeMAPSv02      | egemapsv02       |
| GeMAPSv01b      | gemapsv01b       |

The argument mappings are not case sensitive.
See [openSMILE's FeatureSet documentation](https://audeering.github.io/opensmile-python/api/opensmile.FeatureSet.html#opensmile.FeatureSet) for further details.

## Usage Example

The `extract_features.py` script generates the below FeatureLevel and FeatureSet combinations and repeats it with resampling to 16KHz prior to feature generation on the provided sample WAV file.
| FeatureLevel | FeatureSet
| - | - |
| ComParE_2016 | lld, func, and lld_de |
| eGeMAPSv02 | lld, func |
| GeMAPSv01b | lld, func |

```python
 from osm import extract_osm_features
 extract_osm_features(YOUR_WAV_FILEPATH, OPTIONAL_KWARGS)
```
For instance, you could run:
```python
 from osm import extract_osm_features
 extract_osm_features('sample_audio/wav/first_ten_Sample_HV_Clip.wav', feat_level='func', feat_set='eGeMAPSv02', sampling_rate=16000)
```
This would output the features extracted using functionals as the FeatureLevel, eGeMAPSv02 as the FeatureSet and would resample the audio file to 16KHz. Leaving sample_rate unset will use the original audio file's sampling rate instead.

You can see several examples in `extract_features.main()`.

See further opensmile-python examples [here](https://audeering.github.io/opensmile-python/usage.html).

### Sample Input and Output Files
The sample hierarchy below shows the files created in python3-13-1 (Windows). The files created in python3-9-6 (Windows) and debian_docker_python3-9-6 (Debian via Docker) follow the same structure.
```
opensmile
   |-- sample_audio
   |   |-- wav
   |   |   |-- first_ten_Sample_HV_Clip.wav
   |   |   |-- python3-13-1
   |   |   |   |-- compare_2016
   |   |   |   |   |-- 16KHz
   |   |   |   |   |   |-- first_ten_Sample_HV_Clip_func_compare_2016_16KHz.csv
   |   |   |   |   |   |-- first_ten_Sample_HV_Clip_lld_compare_2016_16KHz.csv
   |   |   |   |   |   |-- first_ten_Sample_HV_Clip_lld_de_compare_2016_16KHz.csv
   |   |   |   |   |-- first_ten_Sample_HV_Clip_func_compare_2016.csv
   |   |   |   |   |-- first_ten_Sample_HV_Clip_lld_compare_2016.csv
   |   |   |   |   |-- first_ten_Sample_HV_Clip_lld_de_compare_2016.csv
   |   |   |   |-- egemapsv02
   |   |   |   |   |-- 16KHz
   |   |   |   |   |   |-- first_ten_Sample_HV_Clip_func_egemapsv02_16KHz.csv
   |   |   |   |   |   |-- first_ten_Sample_HV_Clip_lld_egemapsv02_16KHz.csv
   |   |   |   |   |-- first_ten_Sample_HV_Clip_func_egemapsv02.csv
   |   |   |   |   |-- first_ten_Sample_HV_Clip_lld_egemapsv02.csv
   |   |   |   |-- gemapsv01b
   |   |   |   |   |-- 16KHz
   |   |   |   |   |   |-- first_ten_Sample_HV_Clip_func_gemapsv01b_16KHz.csv
   |   |   |   |   |   |-- first_ten_Sample_HV_Clip_lld_gemapsv01b_16KHz.csv
   |   |   |   |   |-- first_ten_Sample_HV_Clip_func_gemapsv01b.csv
   |   |   |   |   |-- first_ten_Sample_HV_Clip_lld_gemapsv01b.csv
```
## Supported Input Types
This repository only supports audio files as inputs that are compatible with opensmile-python, which appears to include at least WAV and FLAC files. Further information about openSMILE's supported data input formats can be found [here](https://audeering.github.io/opensmile/about.html#data-input).

The opensmile-python package also supports the processing of audio signals directly (see [process_signal](https://stackoverflow.com/questions/44836653/ffmpegs-flac-compression-levels-defaults-settings)). 

Converting to a supported audio file format and using [process_file](https://audeering.github.io/opensmile-python/api/opensmile.Smile.html#process-signal) or reading the audio file format's audio signal and sampling rate and using [process_signal](https://audeering.github.io/opensmile-python/api/opensmile.Smile.html#process-signal) can both work.

## Validation
The scripts provided in `validate.py` allow you to check features extracted on your machine using the sample file [first_ten_Sample_HV_Clip.wav](sample_audio/wav/first_ten_Sample_HV_Clip.wav) against the provided sample output.

Differences in Python and/or library versions used to extract features may affect the comparison due to differences in float precision. `validate.py` checks against sample files that were generated using Python 3.13.1 and Python 3.9.6.

Files have carriage returns removed before the creation of hashes for comparison. The mean of the absolute value of the cosine similarity is reported for multi-dimension arrays. The absolute value is taken to address a potential bug, where two numpy arrays are equal, but some cosine similarity values are around -1.

To perform the validation check, see `run_validate.py`:

```python
from validate import generate_comparison_files, validate_files

def main():
    """
    main entrypoint for running the acoustic-features validation scripts
    """
    sample_filepath = 'sample_audio/wav/first_ten_Sample_HV_Clip.wav'
    generate_comparison_files(sample_filepath)
    validate_files(sample_filepath, 'python3-13-1')
    validate_files(sample_filepath, 'python3-9-6')
    validate_files(sample_filepath, 'debian_docker_python3-9-6')

if __name__ == '__main__':
    main()

```

This will write the feature extractions to test_output/ and will output a comparison CSV to test_output/python3-13-1, test_output/python3-9-6, and test_output/debian_docker_python3-9-6 respectively.

The comparison CSV has the following columns:

| Column | Description | Example | 
| - | - | - |
| sample_input | Filepath to the source audio file. | sample_audio/wav/first_ten_Sample_HV_Clip.wav |
| original_output | Filepath to the original output data, pre-generated on the repository. | sample_audio/wav/python3-13-1/compare_2016/first_ten_Sample_HV_Clip_func_compare_2016.csv |
| test_output | Filepath to the test_output data, generated from the source audio file, but on the user's machine. | test_output/first_ten_Sample_HV_Clip/compare_2016/first_ten_Sample_HV_Clip_func_compare_2016.csv |
| original_output_hash | sha256 hash generated on original_output. | a85... |
| test_output_hash | sha256 hash generated on test_output. | a85... |
| output_hashes_match | Indicates whether original_output_hash and test_output_hash are equal (1) or not (0). | 1 |
| cosine_similarity | The cosine similarity value if the features are a single row (func), otherwise a filepath to a numpy array (npy) file that has the cosine similarity performed between the matrices.  | 1 or test_output/python3-13-1/npy/first_ten_Sample_HV_Clip_lld_compare_2016.npy | 

Please see `windows_py3-13-1.md`, `windows_py3-9-6.md`, and `debian_docker_py3-9-6.md` for copies of the expected run_validate.py output for Windows (Python 3.13.1), Windows (Python 3.9.6), and Debian via Docker (Python 3.9.6) respectively.

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
