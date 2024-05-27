import tkinter as tk
from tkinter import filedialog, messagebox
from data_loader import DataLoader


class DataLoaderUI:
    def __init__(self, master):
        self.master = master
        master.title("Data Loader")

        self.data_label = tk.Label(master, text="Select the folder where your data is stored:")
        self.data_label.pack(pady=10)

        self.data_button = tk.Button(master, text="Select Data Folder", command=self.select_data_folder)
        self.data_button.pack(pady=10)

        self.save_label = tk.Label(master, text="Select the folder where processed data features will be stored:")
        self.save_label.pack(pady=10)

        self.save_button = tk.Button(master, text="Select Save Folder", command=self.select_save_folder)
        self.save_button.pack(pady=10)

        self.load_button = tk.Button(master, text="Load Data", command=self.load_data, state=tk.DISABLED)
        self.load_button.pack(pady=10)

        self.data_folder_path = ""
        self.save_folder_path = ""

    def select_data_folder(self):
        self.data_folder_path = filedialog.askdirectory()
        if self.data_folder_path:
            show_custom_message(self.master, "Selected Folder", f"Data folder selected: {self.data_folder_path}")
            self.enable_load_button()
        else:
            show_custom_message(self.master, "No Folder Selected", "Please select a folder to load data from.")

    def select_save_folder(self):
        self.save_folder_path = filedialog.askdirectory()
        if self.save_folder_path:
            show_custom_message(self.master, "Selected Folder", f"Save folder selected: {self.save_folder_path}")
            self.enable_load_button()
        else:
            show_custom_message(self.master, "No Folder Selected", "Please select a folder to save processed data to.")

    def enable_load_button(self):
        if self.data_folder_path and self.save_folder_path:
            self.load_button.config(state=tk.NORMAL)

    def load_data(self):
        if self.data_folder_path and self.save_folder_path:
            dataloader = DataLoader(self.data_folder_path, self.save_folder_path)
            dataloader.load_data()
            show_custom_message(self.master, "Data Loading", "Data loading completed.")
        else:
            show_custom_message(self.master, "Folder Selection Incomplete", "Please select both data and save folders.")


class CustomMessageBox:
    def __init__(self, master, title, message):
        self.master = master
        self.title = title
        self.message = message
        self.create_message_box()

    def create_message_box(self):
        # Create a new top-level window
        self.top = tk.Toplevel(self.master)
        self.top.title(self.title)
        
        # Calculate position to center the window on the screen
        window_width = 300
        window_height = 150
        screen_width = self.top.winfo_screenwidth()
        screen_height = self.top.winfo_screenheight()
        position_top = int(screen_height / 2 - window_height / 2)
        position_right = int(screen_width / 2 - window_width / 2)
        
        # Set the dimensions and position of the window
        self.top.geometry(f'{window_width}x{window_height}+{position_right}+{position_top}')
        
        # Create a label with the message
        self.label = tk.Label(self.top, text=self.message, wraplength=280)
        self.label.pack(pady=20)
        
        # Create an OK button to close the message box
        self.ok_button = tk.Button(self.top, text="OK", command=self.top.destroy)
        self.ok_button.pack(pady=10)

def show_custom_message(master, title, message):
    CustomMessageBox(master, title, message)


