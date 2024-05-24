import os
import pandas as pd
import numpy as np
import pyedflib
import soundfile as sf
from Signal_Processing import ECG_processing as ecg
from Signal_Processing import EEG_processing as eeg
from Audio import Audio_processing as audio
from pathlib import Path

class DataLoader:
    def __init__(self, data_path):
        self.data_path = data_path
        self.audio_format = ['.mp3', '.ogg', '.flac', '.m4a']
        self.eeg_format = ['.edf']
        self.ecg_format = ['.dat']
        self.base_save_path = "Files"
    
    def get_file_type(self, file_path):
        _, file_extension = os.path.splitext(file_path)
        return file_extension.lower()
    
    def load_data(self):
        files = os.listdir(self.data_path)
        for file in files:
            file_path = os.path.join(self.data_path, file)
            file_type = self.get_file_type(file_path)

            if file_type in self.eeg_format:
                self.load_eeg(file_path)
            
            elif file_type in self.ecg_format:
                self.load_ecg(file_path)
            
            elif file_type in self.audio_format:
                self.load_audio(file_path)
            
            else:
                print(f"Unsupported file format: {file_type}")
            
    def load_eeg(self, file_path):
        # Create EEG_Save_path
        eeg_folder_path = Path(self.base_save_path) / "EEG"
        eeg_folder_path.mkdir(parents=True, exist_ok=True)
        
        eeg.extract_eeg_features(file_path, eeg_folder_path)
        
    def load_ecg(self, file_path):
        # Create ECG_Save_path
        ecg_folder_path = Path(self.base_save_path) / "ECG"
        ecg_folder_path.mkdir(parents=True, exist_ok=True)
        
        ecg.extract_ecg_features(file_path, ecg_folder_path)
        
    def load_audio(self, file_path):
        # Create Audio_Save_path
        audio_folder_path = Path(self.base_save_path) / "Audio"
        audio_folder_path.mkdir(parents=True, exist_ok=True)
        
        audio.extract_audio_features(file_path, audio_folder_path)


if __name__ == "__main__":
    dataloader = DataLoader("Data")
    dataloader.load_data()
