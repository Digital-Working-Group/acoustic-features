"""
validate.py
validate OSM features generated against sample output;
"""
import os
import csv
import hashlib
import pandas as pd
from osm import extract_osm_features

def generate_comparison_files(sample_input):
    """
    extract features from sample file to produce same files as sample_output
    """
    audio_filepaths = [sample_input]
    for audio_fp in audio_filepaths:
        fname = os.path.basename(audio_fp).split('.')[0]

        ## FeatureSet: ComParE_2016
        extract_osm_features(audio_fp, out_root=f'test_output/{fname}')
        extract_osm_features(audio_fp, feat_level='func', out_root=f'test_output/{fname}')
        extract_osm_features(audio_fp, feat_level='lld_de', out_root=f'test_output/{fname}')

        ## FeatureSet: eGeMAPSv02
        extract_osm_features(audio_fp, feat_set='eGeMAPSv02', out_root=f'test_output/{fname}')
        extract_osm_features(audio_fp,
            feat_level='func', feat_set='eGeMAPSv02', out_root=f'test_output/{fname}')

        ## FeatureSet: GeMAPSv01b
        extract_osm_features(audio_fp, feat_set='GeMAPSv01b', out_root=f'test_output/{fname}')
        extract_osm_features(audio_fp,
            feat_level='func', feat_set='GeMAPSv01b', out_root=f'test_output/{fname}')

        ## resample to 16KHz
        ## FeatureSet: ComParE_2016
        sampling_rate = 16000
        extract_osm_features(audio_fp, sampling_rate=sampling_rate, out_root=f'test_output/{fname}')
        extract_osm_features(audio_fp, feat_level='func',
            sampling_rate=sampling_rate, out_root=f'test_output/{fname}')
        extract_osm_features(audio_fp, feat_level='lld_de',
            sampling_rate=sampling_rate, out_root=f'test_output/{fname}')

        ## FeatureSet: eGeMAPSv02
        extract_osm_features(audio_fp, feat_set='eGeMAPSv02',
            sampling_rate=sampling_rate, out_root=f'test_output/{fname}')
        extract_osm_features(audio_fp,
            feat_level='func', feat_set='eGeMAPSv02', sampling_rate=sampling_rate, out_root=f'test_output/{fname}')

        ## FeatureSet: GeMAPSv01b
        extract_osm_features(audio_fp, feat_set='GeMAPSv01b',
            sampling_rate=sampling_rate, out_root=f'test_output/{fname}')
        extract_osm_features(audio_fp,
            feat_level='func', feat_set='GeMAPSv01b', sampling_rate=sampling_rate, out_root=f'test_output/{fname}')

def hash_file(file_path):
    """
    Returns the SHA-256 hash of a file
    """
    hasher = hashlib.sha256()
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hasher.update(chunk)
    return hasher.hexdigest()

def compare_files(file1, file2):
    """
    Compares the SHA-256 hash of two files
    Returns True if they match
    """
    return hash_file(file1) == hash_file(file2)

def csv_walk(directory_path: str) -> dict:
    """
    Recursively fetches all file paths from a given directory and stores them in a dictionary,
    with the file name as the key and the full path as the value.
    """
    file_map = {}

    for root, dirs, files in os.walk(directory_path):
        for file in files:
            if os.path.splitext(file)[1] != '.csv':
                continue
            file_map[file] = os.path.join(root, file)
    
    return file_map

def map_files(generated_dir: str, sample_dir: str):
    """
    Matches generated files to sample files based on their names, irrespective of directory structure.
    Returns a dictionary with file names as keys and a tuple of paths (generated, sample) as values.
    """
    # Get all files in both directories
    sample_files = csv_walk(sample_dir)
    generated_files = csv_walk(generated_dir)
    
    
    # Create a mapping of matching files
    matched_files = {}
    
    for file_name in generated_files:
        if file_name in sample_files:
            matched_files[file_name] = (generated_files[file_name], sample_files[file_name])
    print(matched_files)
    return matched_files

def write_csv():
    """
    write comparison csv
    """

def validate_files(sample_input):
    """
    compare sample output files with generated files using sha256
    """
    
    mapped_dict = map_files('test_output', 'sample_audio')
    summary = [['sample_input', 'original_output', 'test_output', 'original_output_hash', 'test_output_hash', 'output_hashes_match']]
    for file, (original_output, test_output) in mapped_dict.items():
        comparison = [sample_input, original_output, test_output]
        comparison.append(hash_file(original_output))
        comparison.append(hash_file(test_output))
        if hash_file(original_output) == hash_file(test_output):
            comparison.append(1)
        else:
            comparison.append(0)
        summary.append(comparison)
    
    with open('test_comparison.csv', 'w', newline='') as outfile:
        writer = csv.writer(outfile)
        writer.writerows(summary)

def validate_pd():
    mapped_dict = map_files('test_output', 'sample_audio')
    for file, (original_output, test_output) in mapped_dict.items():
        original_df = pd.read_csv(original_output)
        test_df = pd.read_csv(test_output)
        comparison = original_df.compare(test_df)
        print(comparison)
        input()

if __name__ == '__main__':
    sample_input = 'sample_audio/wav/first_ten_Sample_HV_Clip.wav'
    # generate_comparison_files(sample_input)
    validate_files(sample_input)
    validate_pd()



