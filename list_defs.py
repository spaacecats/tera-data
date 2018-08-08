def list_files(dir):
    from os import listdir
    from os.path import isfile, join

    return [f for f in listdir(dir) if isfile(join(dir, f))]
    
import json

with open('defs.json', 'w') as fh:
    json.dump(list_files('./protocol'), fh)
