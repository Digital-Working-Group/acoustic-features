"""
osm.py
osm functions
"""
import os
import opensmile

def extract_osm_features(audio_fp, **kwargs):
    """
    Extracts frequency characteristics of audio using OpenSMILE.
    Default: LowLevelDescriptors and ComParE_2016
    Writes the features to a CSV
    """
    feat_level = kwargs.get('feat_level', 'lld')
    feat_set = kwargs.get('feat_set', 'ComParE_2016')
    sampling_rate = kwargs.get('sampling_rate')
    channels = kwargs.get('channels', [0])
    resample = sampling_rate is not None
    feat_level = feat_level.lower()
    feat_set = feat_set.lower()

    assert feat_level in {'lld', 'func', 'lld_de'}, feat_level
    if feat_level == 'lld_de' and feat_set != 'compare_2016':
        print(f'LowLevelDescriptors_Deltas are not available for {feat_set}')
        return None

    assert feat_set in {'compare_2016',
                        'gemapsv01a', 'gemapsv01b',
                        'egemapsv01a', 'egemapsv01b', 'egemapsv02'}, feat_set

    csv_out = kwargs.get('csv_out')
    if csv_out is None:
        basename = os.path.basename(audio_fp).split('.')[0]
        csv_out = f'sample_out/{feat_set}/{basename}_{feat_level}_{feat_set}.csv'
        if sampling_rate is not None:
            sr_ext = f'{int(sampling_rate / 1000)}KHz'
            csv_out = f'sample_out/{feat_set}/{sr_ext}/{basename}_{feat_level}_{feat_set}_{sr_ext}.csv'

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
        sampling_rate = sampling_rate,
        channels=channels,
        resample = resample
    )

    features = smile.process_file(audio_fp)

    parent = os.path.dirname(csv_out)
    if not os.path.isdir(parent):
        os.makedirs(parent)
    features.to_csv(csv_out)
    print(csv_out)
    return csv_out
