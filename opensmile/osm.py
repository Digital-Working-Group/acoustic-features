"""
osm.py
osm functions
"""
import os
import opensmile

def validate_input(feat_level, feat_set):
    """
    validate feat_level and feat_set inputs
    """
    assert feat_level in {'lld', 'func', 'lld_de'}, feat_level
    if feat_level == 'lld_de' and feat_set != 'compare_2016':
        raise AssertionError(f'LowLevelDescriptors_Deltas are not available for {feat_set}')
    assert feat_set in {'compare_2016', 'gemapsv01a', 'gemapsv01b', 'egemapsv01a', 'egemapsv01b',
        'egemapsv02'}, feat_set

def get_csv_out(audio_fp, out_root, fp_without_ext, feat_level, feat_set, sampling_rate):
    """
    get CSV out if not defined;
    """
    if out_root is None:
        out_root = 'output'
    basename = os.path.basename(fp_without_ext)
    csv_out = f'{out_root}/{feat_set}/{basename}_{feat_level}_{feat_set}.csv'
    if sampling_rate is not None:
        sr_ext = f'{int(sampling_rate / 1000)}KHz'
        csv_out = f'{out_root}/{feat_set}/'+\
            f'{sr_ext}/{basename}_{feat_level}_{feat_set}_{sr_ext}.csv'
    return csv_out

def map_feat_set(feat_set):
    """
    map the feat_set string to the openSMILE FeatureSet;
    """
    feature_set = None
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
    return feature_set

def extract_osm_features(audio_fp, **kwargs):
    """
    Extracts frequency characteristics of audio using OpenSMILE.
    Default: LowLevelDescriptors and ComParE_2016
    Writes the features to a CSV
    """
    feat_level = kwargs.get('feat_level', 'lld')
    feat_set = kwargs.get('feat_set', 'compare_2016')
    sampling_rate = kwargs.get('sampling_rate')
    channels = kwargs.get('channels', [0])
    resample = sampling_rate is not None
    out_root = kwargs.get('out_root')
    feat_level = feat_level.lower()
    feat_set = feat_set.lower()

    validate_input(feat_level, feat_set)

    csv_out = kwargs.get('csv_out')
    fp_without_ext, _ = os.path.splitext(audio_fp)
    csv_out = get_csv_out(audio_fp, out_root, fp_without_ext, feat_level, feat_set,
        sampling_rate) if csv_out is None else csv_out
    feature_set = map_feat_set(feat_set)

    smile = opensmile.Smile(
        feature_set=feature_set,
        feature_level=feat_level,
        sampling_rate=sampling_rate,
        channels=channels,
        resample=resample
    )

    features = smile.process_file(audio_fp)
    parent = os.path.dirname(csv_out)
    if not os.path.isdir(parent):
        os.makedirs(parent)
    features.to_csv(csv_out)
    print(csv_out)
    return csv_out
