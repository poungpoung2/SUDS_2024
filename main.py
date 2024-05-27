from interface import DataLoaderUI
import tkinter as tk

def main():
    root = tk.Tk()
    app = DataLoaderUI(root)
    
    # Center the main window
    window_width = 400
    window_height = 300
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    position_top = int(screen_height / 2 - window_height)
    position_right = int(screen_width / 2 - window_width / 2)
    root.geometry(f'{window_width}x{window_height}+{position_right}+{position_top}')
    
    root.mainloop()
    
    
if __name__ == "__main__":
    main()    