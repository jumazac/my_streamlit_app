

import zipfile
import json

import zipfile

with zipfile.ZipFile(r'C:\Users\JZ\Desktop\mygeodataUNIMAP.zip', 'r') as zip_ref:
    zip_ref.extractall(r'C:\Users\JZ\Desktop\unzipped_files')


