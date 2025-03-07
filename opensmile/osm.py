"""
osm.py
osm functions
"""
import os
import opensmile
import soundfile as sf

def extract_osm_features(audio_fn, csv_out, feat_level='lld', feat_set='ComParE_2016'):
    """
    Extracts frequency characteristics of audio using OpenSMILE.
    Default: LowLevelDescriptors and ComParE_2016
    Writes the features to a CSV
    """
    feat_level = feat_level.lower()
    feat_set = feat_set.lower()
    assert feat_level in {'lld', 'func', 'lld_de'}, feat_level
    if feat_level == 'lld_de' and feat_set != 'compare_2016':
        print('You selected the feature set LowLevelDescriptors_Deltas, which is only compatible with the feature set ComParE_2016. \
                  Please fix compatibility and re-run.')
        return
    assert feat_set in {'compare_2016', 
                        'gemapsv01a', 'gemapsv01b', 
                        'egemapsv01a', 'egemapsv01b', 'egemapsv02'}, feat_set
    if feat_set ==  'compare_2016':
        feature_set = opensmile.FeatureSet.ComParE_2016
    elif feat_set == 'gemapsv01a':
        feature_set = opensmile.FeatureSet.GeMAPSv01a
    elif feat_set == 'gemapsv01b':
        feature_set = opensmile.FeatureSet.GeMAPSv01b
    elif feat_set == 'egemapsv01a':
        feature_set = opensmile.FeatureSet.eGeMAPSv01a
    elif feat_set == 'egemapsv01b':
        feature_set = opensmile.FeatureSet.eGeMAPSv01b
    elif feat_set == 'egemapsv02':
        feature_set = opensmile.FeatureSet.eGeMAPSv02

    smile = opensmile.Smile(
        feature_set=feature_set,
        feature_level=feat_level,
    )

    audio_samples, audio_sample_rate = sf.read(audio_fn)
    if len(audio_samples.shape) == 2:
        audio_samples = audio_samples[:, 0]
    features = smile.process_signal(audio_samples, audio_sample_rate)
    parent = os.path.dirname(csv_out)
    if not os.path.isdir(parent):
        os.makedirs(parent)
    features.to_csv(csv_out)
    print(csv_out)
