import librosa
import numpy as np
import matplotlib.pyplot as plt
import librosa.display
import pandas as pd
from scipy.signal import butter, lfilter
import os


class Config:
    def __init__(self):
        # Band filter parameters
        self.low_cutoff = 800
        self.high_cutoff = 8200

        # Sampling Parameters
        self.n_fft = 2048
        self.hop_length = 512
        self.sr = 44100
        self.n_mels = 256
        self.cmap = "coolwarm"
        self.window_type = "hann"
        self.fmin = 20
        self.fmax = 8000


def bandpass_filter(y, config, order=5):
    nyquist_freq = 0.5 * config.sr
    low = config.low_cutoff / nyquist_freq
    high = config.high_cutoff / nyquist_freq
    b, a = butter(order, [low, high], btype="band")
    y_filtered = lfilter(b, a, y)

    return y_filtered


def load_audio(file_path):
    y, sr = librosa.load(file_path, sr=None)
    return y, sr


def clean_audio(y):
    # Replace NaNs and infinite values with zero
    y = np.nan_to_num(y, nan=0.0, posinf=0.0, neginf=0.0)
    return y


def normalize_audio(y):
    max_val = np.max(np.abs(y))
    if max_val > 0:
        y = y / max_val
    return y


def extract_features(y, config):
    y = clean_audio(y)
    y = normalize_audio(y)

    # STFT
    stft = librosa.stft(
        y,
        n_fft=config.n_fft,
        hop_length=config.hop_length,
        win_length=config.n_fft,
        window=config.window_type,
    )
    magnitude, phase = librosa.magphase(stft)

    # Root Mean Square
    rms = librosa.feature.rms(y=y)

    # Spectral Centroid
    spectral_centroid = librosa.feature.spectral_centroid(
        y=y, sr=config.sr, n_fft=config.n_fft, hop_length=config.hop_length
    )

    # Spectral Bandwidth
    spectral_bandwidth = librosa.feature.spectral_bandwidth(
        y=y, sr=config.sr, n_fft=config.n_fft, hop_length=config.hop_length
    )

    # Spectral Rolloff
    spectral_rolloff = librosa.feature.spectral_rolloff(
        y=y, sr=config.sr, n_fft=config.n_fft, hop_length=config.hop_length
    )

    # Zero-Crossing Rate (ZCR)
    zcr = librosa.feature.zero_crossing_rate(y, hop_length=config.hop_length)

    # Mel-Frequency Cepstral Coefficients (MFCC)
    mfcc = librosa.feature.mfcc(y=y, sr=config.sr)

    features = pd.DataFrame(
        {
            "rms": rms[0],
            "spectral_centroid": spectral_centroid[0],
            "spectral_bandwidth": spectral_bandwidth[0],
            "spectral_rolloff": spectral_rolloff[0],
            "zcr": zcr[0],
        }
    )

    for i in range(mfcc.shape[0]):
        features[f"mfcc_{i+1}"] = mfcc[i]

    print(pd.DataFrame(features))
    return features


def display_audio(y, config):
    fig, ax = plt.subplots(2, 1, figsize=(12, 6), sharex=True, tight_layout=True)
    mel_spec = librosa.feature.melspectrogram(
        y=y,
        sr=config.sr,
        n_mels=config.n_mels,
        n_fft=config.n_fft,
        hop_length=config.hop_length,
        fmax=config.fmax,
        fmin=config.fmin,
    )
    db_mel_spec = librosa.power_to_db(mel_spec, ref=1.0)

    librosa.display.waveshow(
        y=y, sr=config.sr, ax=ax[0], color=plt.get_cmap(config.cmap)(0.1)
    )
    librosa.display.specshow(
        db_mel_spec,
        sr=config.sr,
        hop_length=config.hop_length,
        n_fft=config.n_fft,
        fmin=config.fmin,
        fmax=config.fmax,
        x_axis="time",
        y_axis="mel",
        cmap=config.cmap,
        ax=ax[1],
    )
    ax[0].set_xlabel("")
    plt.show()


def save_features(channel_name, save_path, features):
    df = pd.DataFrame(features)
    csv_path = os.path.join(save_path, f"{channel_name}.csv")
    # Save the DataFrame to CSV
    df.to_csv(csv_path, index=False)


def extract_audio_features(file_path, save_path):
    config = Config()
    y, sr = load_audio(file_path=file_path)
    y = bandpass_filter(y, config=config)
    y = clean_audio(y)
    y = normalize_audio(y)
    features = extract_features(y, config)

    # display_audio(y, config)
    save_features(
        channel_name=os.path.splitext(os.path.basename(file_path))[0],
        save_path=save_path,
        features=features,
    )
