import os
from google.colab import drive

def connect(folder:str):
  drive.mount("/content/gdrive")
  os.chdir(f"gdrive/MyDrive/{folder}")
