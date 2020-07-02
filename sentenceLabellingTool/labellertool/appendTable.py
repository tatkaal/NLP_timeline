import sys
import chilkat
from pathlib import Path
import os
path_to_download_folder = str(os.path.join(Path.home(), "Downloads"))
def loader(rowIndex, columnIndex, value, fileIndex):
    csv = chilkat.CkCsv()

    #  Prior to loading the CSV file, indicate that the 1st row
    #  should be treated as column names:
    csv.put_HasColumnNames(True)

    #  Load the CSV records from the file:
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

    csvDoc = csv.saveToString()
    print(csvDoc)

    #  Save the CSV to a file:
    success = csv.SaveFile(os.path.join(path_to_download_folder, f"test-{fileIndex}.csv"))
    if (success != True):
        print(csv.lastErrorText())