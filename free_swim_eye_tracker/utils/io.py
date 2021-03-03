from pathlib import Path
from tkinter import Tk, filedialog


def create_root():
    root = Tk()
    root.attributes('-topmost', True)
    root.withdraw()
    return root


def ask_filename():
    root = create_root()
    filename = filedialog.askopenfilename()
    root.destroy()
    return filename


def ask_filenames():
    root = create_root()
    filenames = filedialog.askopenfilenames()
    root.destroy()
    return filenames


def ask_directory():
    root = create_root()
    directory = filedialog.askdirectory()
    root.destroy()
    return directory


def get_file(video_path, suffix):
    return Path(video_path).with_suffix('').as_posix() + suffix
