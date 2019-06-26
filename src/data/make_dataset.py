import json
import os
import sys

def get_parent_dir():
    file_path = sys.argv[0]
    return os.path.dirname(file_path)

print(get_parent_dir())

print(sys.path.insert(0,'/data/raw'))
