"""
extract_features.py
generate OSM features on WAV files;
"""
from osm import extract_osm_features

def main():
    """
    main entrypoint
    """
    ## FeatureSet: ComParE_2016
    extract_osm_features('sample_wav/first_ten_Sample_HV_Clip.wav')
    extract_osm_features('sample_wav/first_ten_Sample_HV_Clip.wav', feat_level='func')
    extract_osm_features('sample_wav/first_ten_Sample_HV_Clip.wav', feat_level='lld_de')

    ## FeatureSet: eGeMAPSv02
    extract_osm_features('sample_wav/first_ten_Sample_HV_Clip.wav', feat_set='eGeMAPSv02')
    extract_osm_features('sample_wav/first_ten_Sample_HV_Clip.wav',
        feat_level='func', feat_set='eGeMAPSv02')

    ## FeatureSet: GeMAPSv01b
    extract_osm_features('sample_wav/first_ten_Sample_HV_Clip.wav', feat_set='GeMAPSv01b')
    extract_osm_features('sample_wav/first_ten_Sample_HV_Clip.wav',
        feat_level='func', feat_set='GeMAPSv01b')

    ## resample to 16KHz
    ## FeatureSet: ComParE_2016
    sampling_rate = 16000
    extract_osm_features('sample_wav/first_ten_Sample_HV_Clip.wav', sampling_rate=sampling_rate)
    extract_osm_features('sample_wav/first_ten_Sample_HV_Clip.wav', feat_level='func',
        sampling_rate=sampling_rate)
    extract_osm_features('sample_wav/first_ten_Sample_HV_Clip.wav', feat_level='lld_de',
        sampling_rate=sampling_rate)

    ## FeatureSet: eGeMAPSv02
    extract_osm_features('sample_wav/first_ten_Sample_HV_Clip.wav', feat_set='eGeMAPSv02',
        sampling_rate=sampling_rate)
    extract_osm_features('sample_wav/first_ten_Sample_HV_Clip.wav',
        feat_level='func', feat_set='eGeMAPSv02', sampling_rate=sampling_rate)

    ## FeatureSet: GeMAPSv01b
    extract_osm_features('sample_wav/first_ten_Sample_HV_Clip.wav', feat_set='GeMAPSv01b',
        sampling_rate=sampling_rate)
    extract_osm_features('sample_wav/first_ten_Sample_HV_Clip.wav',
        feat_level='func', feat_set='GeMAPSv01b', sampling_rate=sampling_rate)

if __name__ == '__main__':
    main()
