"""
validate.py
validate OSM features generated against original sample output;
"""
import os
import csv
import hashlib
import pandas as pd
import numpy as np
from comparison.compare import get_cosine_similarity
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

def create_tmp_no_ws(file_path):
    """
    create a temporary filepath with no whitespace
    """
    with open(file_path, 'r') as infile, open('tmp', 'w') as outfile:
        for line in infile:
            line = line.rstrip('\r\n')
            outfile.write(line)

def hash_file(file_path):
    """
    Returns the SHA-256 hash of a file
    """
    create_tmp_no_ws(file_path)
    file_path = 'tmp'
    hasher = hashlib.sha256()
    with open(file_path, 'rb') as infile:
        for chunk in iter(lambda: infile.read(4096), b""):
            hasher.update(chunk)
    os.remove('tmp')
    return hasher.hexdigest()

def csv_walk(directory_path):
    """
    Recursively fetches all file paths from a given directory and stores them in a dictionary,
    with the file name as the key and the full path as the value.
    """
    file_map = {}
    for root, _, files in os.walk(directory_path):
        for file in files:
            if os.path.splitext(file)[1] != '.csv':
                continue
            file_map[file] = os.path.join(root, file)
    return file_map

def map_files(original_dir, test_dir):
    """
    Walks each directory and matches test files to original files based on their names.
    Returns a dictionary with file names as keys and a tuple of paths (generated, sample) as values.
    """
    # Get all files in both directories
    original_files = csv_walk(original_dir)
    test_files = csv_walk(test_dir)

    # Create a mapping of matching files
    matched_files = {}

    for file_name, test_outpath in test_files.items():
        if file_name in original_files:
            matched_files[file_name] = (original_files[file_name], test_outpath)
    return matched_files

def yield_csv_data(csv_in):
    """
    parameters:
        csv_in(str): path to a csv file
    """
    with open(csv_in, newline='') as infile:
        for row in csv.DictReader(infile, delimiter=','):
            yield row

def validate_files(sample_input, python_version):
    """
    Compare original sample output files with generated files using sha256
    Outputs a csv with comparison details
    """
    mapped_dict = map_files(f'sample_audio/wav/{python_version}', 'test_output')
    summary = [['sample_input', 'original_output', 'test_output', 'original_output_hash',
                 'test_output_hash', 'output_hashes_match', 'cosine_similarity']]

    hash_matches = {'hashes_match': 0, 'hashes_do_not_match': 0}
    for file, (original_output, test_output) in mapped_dict.items():
        try:
            ## Hash comparison
            original_hash = hash_file(original_output)
            test_hash = hash_file(test_output)
            hash_match = int(original_hash == test_hash)

            if hash_match == 1:
                hash_matches['hashes_match'] += 1
            else:
                hash_matches['hashes_do_not_match'] +=1

            # Cosine similarity
            original_df = pd.read_csv(original_output).drop(['file'], axis=1, errors='ignore')
            test_df = pd.read_csv(test_output).drop(['file'], axis=1, errors='ignore')
            file_no_ext = file.split('.')[0]
            cosine_similarity = get_cosine_similarity(original_df, test_df,
                                                  f'npy/{file_no_ext}.npy',
                                                  outdir=f'test_output/{python_version}')

            ## Append comparison results
            summary.append([sample_input, original_output, test_output,
                                original_hash, test_hash, hash_match, cosine_similarity])
        except Exception as error:
            print(f'Error processing {file}: {error}')
    write_validate_output(summary, hash_matches, python_version)

def write_validate_output(summary, hash_matches, python_version):
    """
    write validate output files and prints;
    """
    outpath = os.path.join('test_output', python_version, f'test_comparison_{python_version}.csv')
    lines = []
    with open(outpath, 'w', newline='') as outfile:
        writer = csv.writer(outfile)
        writer.writerows(summary)
    for row in yield_csv_data(outpath):
        for inp_idx in ['sample_input', 'original_output', 'test_output']:
            lines.append(f'{inp_idx} {row[inp_idx]}')
        lines.append(f'output_hashes_match: {row["output_hashes_match"]}')
        cos = row['cosine_similarity']
        if str(cos).endswith('npy'):
            cos_val = np.mean(np.abs(np.load(cos)))
            ## taking absolute value because there seems to be a bug with lld_de, where
            ## the np_arrs are 100% equivalent but some of the cos sim values are -1
            lines.append(f'\t{cos}\t\navg_cos_similarity: {cos_val}\n')
        else:
            lines.append(f'cos_similarity: {cos}\n')
    lines.append(f'Summary: {hash_matches}')
    lines.append(f'Validation CSV written to {outpath}.')
    lines = "\n".join(lines)
    txt_out = outpath.replace('.csv', '.txt')
    with open(txt_out, 'w') as outfile:
        outfile.write(lines)
    print(lines)
    print(f'wrote log to {txt_out}')
