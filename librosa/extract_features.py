"""
extract_features.py
generate Librosa spectral and rhythm features on WAV files;
"""
from librosa_feature_extraction import extract_librosa_features

def main():
    """
    main entrypoint generating Spectral and Rhythm features
    """
    wav_fp = '../sample_audio/first_ten_Sample_HV_Clip.wav'
    generate_features = ['chroma_stft', 'chroma_cqt', 'chroma_cens', 'chroma_vqt',
                         'melspectrogram', 'mfcc', 'rms', 'spectral_centroid', 'spectral_bandwidth',
                         'spectral_contrast', 'spectral_flatness', 'spectral_rolloff', 
                         'poly_features', 'tonnetz', 'zero_crossing_rate', 'tempo', 'tempogram',
                         'fourier_tempogram', 'tempogram_ratio']
    kwargs = {'sampling_rate': 16000,
              'to_mono': True}
    for feature in generate_features:
        extract_librosa_features(wav_fp, feature, **kwargs)

if __name__ == '__main__':
    main()