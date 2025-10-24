import librosa
import numpy as np
import os

def get_np_out(out_root, fp_without_ext, feature, sampling_rate):
    """
    get NPY out if not defined;
    """
    if out_root is None:
        out_root = 'output'
    basename = os.path.basename(fp_without_ext)
    np_out = f'{out_root}/{basename}_{feature}.npy'
    if sampling_rate is not None:
        sr_ext = f'{int(sampling_rate / 1000)}KHz'
        np_out = f'{out_root}/{basename}_{feature}_{sr_ext}.npy'
    return np_out

def load_audio(filename, **kwargs):
    """
    Loads audio using librosa, returns the waveform and sampling rate
    """
    return librosa.load(filename, **kwargs)

def build_arguments(feature_name, waveform, sampling_rate, **kwargs):
    """
    adjusting kwargs to contain the required fields
    """
    ## features requiring intervals
    if feature_name == 'chroma_vqt' and "intervals" not in kwargs:
        feature_kwargs = {"y": waveform, "sr": sampling_rate, "intervals": "equal"}
        feature_kwargs.update(kwargs)
    ## features that don't take the sampling rate
    elif feature_name in ['rms', 'spectral_flatness', 'zero_crossing_rate']:
        feature_kwargs = {"y": waveform}
        feature_kwargs.update(kwargs)
    ## all other features
    else:
        feature_kwargs = {"y": waveform, "sr": sampling_rate}
        feature_kwargs.update(kwargs)
    return feature_kwargs

def extract_features(feature_name, **kwargs):
    """
    Extract Librosa Feature
    Supported features include
    """

    if hasattr(librosa.feature, feature_name):
        feature_func = getattr(librosa.feature, feature_name)
        features = feature_func(**kwargs)
        return features
    else:
        raise ValueError(f"Unknown feature: {feature_name}")
    
def extract_librosa_features(audio_fp, feature_name, **kwargs):
    """
    Extracts specified Librosa feature on provided audio file
    Writes the features to an NPY
    """
    sampling_rate = kwargs.get('sampling_rate', None)
    to_mono = kwargs.get('to_mono', False)
    load_kwargs = kwargs.get('load_kwargs', {})
    extraction_kwargs = kwargs.get('extraction_kwargs', {})
    np_out = kwargs.get('np_out')
    out_root = kwargs.get('out_root')
    fp_without_ext, _ = os.path.splitext(audio_fp)
    np_out = get_np_out(out_root, fp_without_ext, feature_name,
        sampling_rate) if np_out is None else np_out
    print(f'Loading audio file...')
    waveform, sr = load_audio(audio_fp, sr=sampling_rate, mono=to_mono, **load_kwargs)
    print(f'Extracting {feature_name}...')
    feature_kwargs = build_arguments(feature_name, waveform, sr, **extraction_kwargs)
    features = extract_features(feature_name, **feature_kwargs)
    parent = os.path.dirname(np_out)
    if not os.path.isdir(parent):
        os.makedirs(parent)
    print('Writing output...')
    np.save(np_out, features)
    print(f'Output written to {np_out}.')

