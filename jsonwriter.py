import json

def dump_data(data, file_name):
    with open(file_name,'w') as f:
        f.write(json.dumps(data))