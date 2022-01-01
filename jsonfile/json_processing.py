#simplefield load and save json file
import json 

def load_json(filename):
    with open(filename) as json_file:
        data = json.load(json_file)
    return data

def save_json(data,filename):
    with open(filename,'w') as output_file:
        data = json.dump(data,output_file,indent=4)

