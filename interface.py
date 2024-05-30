import tkinter as tk
from tkinter import filedialog
from config import Config
from data_loader import DataLoader

class DataLoaderUI:
    def __init__(self, master):
        # Set the master window
        self.master = master
        master.title("Data Loader")

        # Data Folder Selection
        self.data_label = tk.Label(master, text="Select the folder where your data is stored:")
        self.data_label.pack(pady=5)

        # Data Folder Selection Button
        self.data_button = tk.Button(master, text="Select Data Folder", command=self.select_data_folder)
        self.data_button.pack(pady=5)

        # Save Folder Selection
        self.save_label = tk.Label(master, text="Select the folder where processed data features will be stored:")
        self.save_label.pack(pady=5)

        # Save Folder Selection Button
        self.save_button = tk.Button(master, text="Select Save Folder", command=self.select_save_folder)
        self.save_button.pack(pady=5)

        # Parameters Label
        self.param_label = tk.Label(master, text="Set Parameters:")
        self.param_label.pack(pady=10)

        # EEG Parameters Frame
        eeg_frame = tk.LabelFrame(master, text="EEG Parameters", padx=10, pady=10)
        eeg_frame.pack(padx=10, pady=10)

        self.window_duration_label = tk.Label(eeg_frame, text="Window Duration (seconds):")
        self.window_duration_label.grid(row=0, column=0, sticky="e")
        self.window_duration_entry = tk.Entry(eeg_frame)
        self.window_duration_entry.grid(row=0, column=1)

        self.time_step_label = tk.Label(eeg_frame, text="Time Step (seconds):")
        self.time_step_label.grid(row=1, column=0, sticky="e")
        self.time_step_entry = tk.Entry(eeg_frame)
        self.time_step_entry.grid(row=1, column=1)

        # ECG Parameters Frame
        ecg_frame = tk.LabelFrame(master, text="ECG Parameters", padx=10, pady=10)
        ecg_frame.pack(padx=10, pady=10)

        self.ecg_low_cutoff_label = tk.Label(ecg_frame, text="ECG Low Cutoff Frequency (Hz):")
        self.ecg_low_cutoff_label.grid(row=0, column=0, sticky="e")
        self.ecg_low_cutoff_entry = tk.Entry(ecg_frame)
        self.ecg_low_cutoff_entry.grid(row=0, column=1)

        self.ecg_high_cutoff_label = tk.Label(ecg_frame, text="ECG High Cutoff Frequency (Hz):")
        self.ecg_high_cutoff_label.grid(row=1, column=0, sticky="e")
        self.ecg_high_cutoff_entry = tk.Entry(ecg_frame)
        self.ecg_high_cutoff_entry.grid(row=1, column=1)

        # Audio Parameters Frame
        audio_frame = tk.LabelFrame(master, text="Audio Parameters", padx=10, pady=10)
        audio_frame.pack(padx=10, pady=10)

        self.audio_low_cutoff_label = tk.Label(audio_frame, text="Audio Low Cutoff Frequency (Hz):")
        self.audio_low_cutoff_label.grid(row=0, column=0, sticky="e")
        self.audio_low_cutoff_entry = tk.Entry(audio_frame)
        self.audio_low_cutoff_entry.grid(row=0, column=1)

        self.audio_high_cutoff_label = tk.Label(audio_frame, text="Audio High Cutoff Frequency (Hz):")
        self.audio_high_cutoff_label.grid(row=1, column=0, sticky="e")
        self.audio_high_cutoff_entry = tk.Entry(audio_frame)
        self.audio_high_cutoff_entry.grid(row=1, column=1)

        self.sr_label = tk.Label(audio_frame, text="Sampling Rate (Hz):")
        self.sr_label.grid(row=2, column=0, sticky="e")
        self.sr_entry = tk.Entry(audio_frame)
        self.sr_entry.grid(row=2, column=1)

        self.hop_length_label = tk.Label(audio_frame, text="Hop Length (samples):")
        self.hop_length_label.grid(row=3, column=0, sticky="e")
        self.hop_length_entry = tk.Entry(audio_frame)
        self.hop_length_entry.grid(row=3, column=1)

        self.load_button = tk.Button(master, text="Load Data", command=self.load_data, state=tk.DISABLED)
        self.load_button.pack(pady=10)

        self.data_folder_path = ""
        self.save_folder_path = ""


    def select_data_folder(self):
        # Open the file dialog to select the data folder
        self.data_folder_path = filedialog.askdirectory()
        if self.data_folder_path:
            self.show_custom_message("Selected Folder", f"Data folder selected: {self.data_folder_path}")
            self.enable_load_button()
        else:
            self.show_custom_message("No Folder Selected", "Please select a folder to load data from.")

    def select_save_folder(self):
        # Open the file dialog to select the save folder
        self.save_folder_path = filedialog.askdirectory()
        if self.save_folder_path:
            self.show_custom_message("Selected Folder", f"Save folder selected: {self.save_folder_path}")
            self.enable_load_button()
        else:
            self.show_custom_message("No Folder Selected", "Please select a folder to save processed data to.")

    def enable_load_button(self):
        # Enable the load button if both data and save folders are selected
        if self.data_folder_path and self.save_folder_path:
            self.load_button.config(state=tk.NORMAL)

    def load_data(self):
        try:
            # Get the parameters from the user input
            window_duration = float(self.window_duration_entry.get())
            time_step = float(self.time_step_entry.get())
            ecg_low_cutoff = float(self.ecg_low_cutoff_entry.get())
            ecg_high_cutoff = float(self.ecg_high_cutoff_entry.get())
            audio_low_cutoff = float(self.audio_low_cutoff_entry.get())
            audio_high_cutoff = float(self.audio_high_cutoff_entry.get())
            sr = int(self.sr_entry.get())
            hop_length = int(self.hop_length_entry.get())
            config = Config(window_duration, time_step, ecg_low_cutoff, ecg_high_cutoff, audio_low_cutoff, audio_high_cutoff, sr, hop_length)
        except ValueError:
            self.show_custom_message("Invalid Input", "Please enter valid numbers for all parameters.")
            return

        # Load the data using the DataLoader class
        if self.data_folder_path and self.save_folder_path:
            dataloader = DataLoader(self.data_folder_path, self.save_folder_path, config)
            dataloader.load_data()
            self.show_custom_message("Data Loading", "Data loading completed.")
        # Show an error message if the data and save folders are not selected
        else:
            self.show_custom_message("Folder Selection Incomplete", "Please select both data and save folders.")

    def show_custom_message(self, title, message):
        CustomMessageBox(self.master, title, message)

# Custom message box class
class CustomMessageBox:
    def __init__(self, master, title, message):
        self.master = master
        self.title = title
        self.message = message
        self.create_message_box()
    # Create the message box window
    def create_message_box(self):
        # Create a new top-level window
        self.top = tk.Toplevel(self.master)
        self.top.title(self.title)
        window_width = 300
        window_height = 150
        screen_width = self.top.winfo_screenwidth()
        screen_height = self.top.winfo_screenheight()
        position_top = int(screen_height / 2 - window_height / 2)
        position_right = int(screen_width / 2 - window_width / 2)
        # Set the window size and position
        self.top.geometry(f'{window_width}x{window_height}+{position_right}+{position_top}')
        self.label = tk.Label(self.top, text=self.message, wraplength=280)
        self.label.pack(pady=20)
        self.ok_button = tk.Button(self.top, text="OK", command=self.top.destroy)
        self.ok_button.pack(pady=10)