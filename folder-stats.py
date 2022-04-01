#!/c/Users/steve/AppData/Local/Microsoft/WindowsApps/python

import os,sys
import time
import pandas as pandas
from PIL import Image, ExifTags
from dateutil import parser

# Show most recent taken timestamp for each folder in the path
class NewestJpgInFolder:
    def __init__(self, folder) -> None:
        self.records = []
        files = os.listdir(folder)
        count = 0
        most_recent = {"file": None, "modified_epoch": 0, "taken_epoch": 0}
        # TODO Need to default to taken.  If None, use modified
        for file in files:
            file = f"{folder}/{file}"
            if os.path.isdir(file):
                continue
            if file.endswith("jpg"):
                compare_epoch = self.get_date_taken_epoch(file)
                if compare_epoch is None:
                    # not defined so default to modified epoch
                    compare_epoch = os.path.getmtime(file)

                if compare_epoch > most_recent["taken_epoch"]:
                    most_recent["file"] = file
                    most_recent["modified_epoch"] = os.path.getmtime(file)
                    most_recent["modified_timestamp"] = time.ctime(most_recent["modified_epoch"])
                    most_recent["taken_timestamp"] = self.get_date_taken_string(file)
                    most_recent["taken_epoch"] = compare_epoch
                count = count + 1
        self.records.append(most_recent)

    def get_date_taken_string(self, path):
        with Image.open(path) as image:
            exif = image.getexif()
            taken = exif.get(306)
        return taken
    def get_date_taken_epoch(self, path):
        time_string = self.get_date_taken_string(path)
        if  time_string is None:
            return None
        try:
            return parser.parse(time_string).timestamp()
        except:
            return None
    
def recurse_folders_for_latest_jpg(path):
    all_records = []
    dirnames = []
    for root,d_names,f_names in os.walk(path):
        for d in d_names:
           dirnames.append(os.path.join(root, d))
    for d in dirnames:    
        f = NewestJpgInFolder(d)
        for record in f.records:
            all_records.append(record)
    return pandas.DataFrame.from_records(all_records,index=range(1,len(all_records) + 1))

def show_most_recent_file_by_folder():
    try:
        df = recurse_folders_for_latest_jpg(sys.argv[1])
        print(df.sort_values(by=["taken_epoch"],ascending=False))
    except IndexError:
        print("Usage: "+sys.argv[0]+" <Path>")

class FolderStats():
    def __init__(self,path) -> None:
        self.record = {"path": None, "count": 0, "size": 0}
        self.count = 0
        self.size = 0
        
        for entry in os.listdir(path):
            entry = f"{path}/{entry}"
            if os.path.isfile(entry):              
                self.count = self.count + 1
                self.size = self.size + os.path.getsize(entry)
        self.record["path"] = path
        self.record["count"] = self.count
        self.record["size"] = self.size
class FoldersStats():
    def __init__(self, path) -> None:
        all_records = []
        dirnames = []
        for root,d_names,f_names in os.walk(path):
            for d in d_names:
                dirnames.append(os.path.join(root, d))
        for d in dirnames:   
            f = FolderStats(d)
            all_records.append(f.record)
        df = pandas.DataFrame.from_records(all_records,index=range(1,len(all_records) + 1))
        df.loc[:, "size"] = df["size"].map('{:,d}'.format)
        self.folders = df.sort_values(by=["size"],ascending=False)

pandas.set_option('display.max_colwidth', None)

if __name__ == "__main__":
    print("1. Show most recent jpg timestamp by folder")
    print("2. Show folder stats")
    option = input("Enter an option from 1 to 2:")    
    if option == "1":
        show_most_recent_file_by_folder()
    elif option == "2":
        fs = FoldersStats(sys.argv[1])
        print(fs.folders)
