"""
compare.py
compares features generated using different methods;
"""
import os
import csv
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

def write_compare(filename, data):
    """
    Creates and writes a csv
    """
    with open(filename, 'w', newline='') as outfile:
        writer = csv.writer(outfile)
        writer.writerows(data)
    print(f'Created {filename}')

def verify_dir(root, path):
    """
    Checks that the path for a file exists and creates it if not
    Returns the filepath
    """
    out_dir = os.path.join(root, os.path.dirname(path))
    os.makedirs(out_dir, exist_ok=True)
    return os.path.join(out_dir, os.path.basename(path))

def get_cosine_similarity(control_df, test_df, np_arr_name):
    """
    Calculates the cosine similarity between two dataframes with the same columns
    Returns the cosine similarity if the array contains one element, else saves a numpy
            array and returns its location
    """
    test_df.drop(['start', 'end'], axis=1, inplace=True)
    control_df.drop(['start', 'end'], axis=1, inplace=True)
    similarity_arr = cosine_similarity(control_df, test_df)
    if similarity_arr.shape == (1,1):
        return similarity_arr[0,0]
    else:
        outpath = verify_dir('npy_arrays', np_arr_name)
        np.save(outpath, similarity_arr)
        return outpath

def compare_files(relative_path, control_folder, test_folder, prefix):
    """
    Compares two files with the same columns
    Outputs a comparison CSV of columns side-by-side
    """
    control_file = os.path.join(control_folder, relative_path)
    test_file = os.path.join(test_folder, relative_path)

    if prefix is not None:
        prefix_path = os.path.join(os.path.split(relative_path)[0], f'{prefix}_{os.path.split(relative_path)[1]}')
        test_file = os.path.join(test_folder, prefix_path)

    control_df = pd.read_csv(control_file)
    test_df = pd.read_csv(test_file)

    test_df.drop(['file'], axis=1, inplace=True, errors='ignore')
    control_df.drop(['file'], axis=1, inplace=True, errors='ignore')

    df_compare = control_df.compare(test_df)
    output_name = f'{control_folder}_x_{test_folder}'
    if df_compare.empty:
        identical = True
        print(f'Indentical dataframes:\n{control_file}\n{test_file}\n')

    else:
        identical = False
        outpath = verify_dir(output_name, relative_path)
        df_compare.to_csv(outpath)
        print(f'Comparison output to {outpath}')

    arr_outpath = os.path.splitext(os.path.basename(relative_path))[0]
    similarity = get_cosine_similarity(control_df, test_df, f'{output_name}/{arr_outpath}.npy')
    return [control_file, test_file, similarity, identical]

def all_features(control_type, test_type, prefix=None):
    """
    Calls the compare_files on all FeatureSet and FeatureLevel combinations
    Writes cosine similarities to a csv
    """
    summary = [['file_1', 'file_2', 'cosine_similarity', 'identical']]
    all_features_paths = ['ComParE_2016/first_ten_Sample_HV_Clip_func_ComParE_2016.csv',
                          'ComParE_2016/first_ten_Sample_HV_Clip_lld_ComParE_2016.csv',
                          'ComParE_2016/first_ten_Sample_HV_Clip_lld_de_ComParE_2016.csv', 
                          'eGeMAPSv02/first_ten_Sample_HV_Clip_func_eGeMAPSv02.csv',
                          'eGeMAPSv02/first_ten_Sample_HV_Clip_lld_eGeMAPSv02.csv',
                          'GeMAPSv01b/first_ten_Sample_HV_Clip_func_GeMAPSv01b.csv',
                          'GeMAPSv01b/first_ten_Sample_HV_Clip_lld_GeMAPSv01b.csv']
    for feature_path in all_features_paths:
        comparison = compare_files(feature_path, control_type, test_type, prefix)
        summary.append(comparison)
    write_compare(f'{control_type}_x_{test_type}/cosine_similarity.csv', summary)

if __name__ == '__main__':
    all_features('process_signal_out', 'process_file_out')
    all_features('process_file_out', 'mono_out', prefix='mono')
    all_features('resample_out', 'downsample_out', prefix='downsampled')