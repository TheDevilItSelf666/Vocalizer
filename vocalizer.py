from spleeter.separator import Separator
import tensorflow as tf
import os
import customtkinter as tk
from customtkinter import filedialog


physical_devices = tf.config.list_physical_devices('GPU')
if physical_devices:
    for device in physical_devices:
        tf.config.experimental.set_memory_growth(device, True)


def select_audio_file():
    file_path = filedialog.askopenfilename(filetypes=[("Audio files", "*.mp3 *.wav")])
    audio_entry.delete(0, tk.END)
    audio_entry.insert(0, file_path)


def select_output_directory():
    directory = filedialog.askdirectory()
    output_entry.delete(0, tk.END)
    output_entry.insert(0, directory)


def separate_audio():
    audio_file = audio_entry.get()
    output_directory = output_entry.get()

    if audio_file and output_directory:
        separate_button.configure(state=tk.DISABLED)

        separator = Separator('spleeter:2stems')
        try:
            os.makedirs(output_directory, exist_ok=True)
            separator.separate_to_file(audio_file, output_directory)
            result_label.configure(text=f"Audio separation completed. Separated files saved in \n {output_directory}")

        except Exception as e:
            result_label.configure(text=f"An error occurred: {str(e)}")
        finally:
            separate_button.configure(state=tk.NORMAL)
    else:
        result_label.configure(text="Please select both an audio file and an output directory.")



if __name__ == '__main__':
    # Create a GUI window
    tk.set_appearance_mode("dark")
    tk.set_default_color_theme("blue")

    root = tk.CTk()
    root.geometry("500x500")
    root.title("Vocalizer")

    frame = tk.CTkFrame(master=root)
    frame.pack(pady=30, padx=60, fill="both", expand=True)


    # Create and configure GUI elements
    audio_label = tk.CTkLabel(master=frame, text="Select Audio File:")
    audio_label.pack(pady=12, padx=10)

    audio_entry = tk.CTkEntry(master=frame, width=90)
    audio_entry.pack(pady=12, padx=10)

    audio_button = tk.CTkButton(master=frame, text="Browse", command=select_audio_file)
    audio_button.pack(pady=12, padx=10)

    output_label = tk.CTkLabel(master=frame, text="Select Output Directory:")
    output_label.pack(pady=12, padx=10)

    output_entry = tk.CTkEntry(master=frame, width=90)
    output_entry.pack(pady=12, padx=10)

    output_button = tk.CTkButton(master=frame, text="Browse", command=select_output_directory)
    output_button.pack(pady=12, padx=10)

    separate_button = tk.CTkButton(master=frame, text="Separate Audio", command=separate_audio)
    separate_button.pack(pady=16, padx=10)

    result_label = tk.CTkLabel(master=frame, text="")
    result_label.pack(pady=12, padx=10)

    
    root.mainloop()
