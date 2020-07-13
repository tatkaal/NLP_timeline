import sys
import chilkat
from pathlib import Path
import os
import logging
# import winreg
from labellertool.config import labelledDataPath

# def get_download_path():
#     """Returns the default downloads path for linux or windows"""
#     if os.name == 'nt':
#         sub_key = r'SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders'
#         downloads_guid = '{374DE290-123F-4565-9164-39C4925E467B}'
#         with winreg.OpenKey(winreg.HKEY_CURRENT_USER, sub_key) as key:
#             location = winreg.QueryValueEx(key, downloads_guid)[0]
#         return location
#     else:
#         return os.path.join(os.path.expanduser('~'), 'downloads')

# path_to_download_folder = str(os.path.join(Path.home(), "Downloads"))
# path_to_download_folder = get_download_path()
path_to_download_folder = labelledDataPath
# text_file = open("pathName.txt", "w")
# text_file.write('Downloads path ::'+path_to_download_folder)

# with open("Output.txt", "w") as text_file:
#     text_file.write("Write blablabla into a file")

def loader(rowIndex, columnIndex, value, fileIndex):
    csv = chilkat.CkCsv()

    #  Prior to loading the CSV file, indicate that the 1st row
    #  should be treated as column names:
    csv.put_HasColumnNames(True)

    #  Load the CSV records from the file:
    # print(os.path.join(path_to_download_folder, f"test-{fileIndex}.csv"))
    # text_file.write('loading file path ::'+os.path.join(path_to_download_folder, f"test-{fileIndex}.csv"))

    # print(os.path.join(path_to_download_folder, f"test-{fileIndex}.csv"))
    success = csv.LoadFile(os.path.join(path_to_download_folder, f"test-{fileIndex}.csv"))
    if (success != True):
        print(csv.lastErrorText())
        sys.exit()

    #  Change "cheese" to "baguette"
    #  ("cheese" is at row=0, column=3
    # success = csv.SetCell(0,3,"baguette")

    #  Change "blue" to "magenta"
    success = csv.SetCell(rowIndex, columnIndex, value)

    #  Write the updated CSV to a string and display:

    # csvDoc = csv.saveToString()
    # print(csvDoc)

    #  Save the CSV to a file:
    success = csv.SaveFile(os.path.join(path_to_download_folder, f"test-{fileIndex}.csv"))

    # text_file.write('saving file path ::'+os.path.join(path_to_download_folder, f"test-{fileIndex}.csv"))
    # text_file.close()

    if (success != True):
        print(csv.lastErrorText())