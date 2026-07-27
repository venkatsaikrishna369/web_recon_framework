# utils/helpers.py
import os

def ensure_output_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)