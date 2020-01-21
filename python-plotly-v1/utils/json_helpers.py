def write_json_to_file(json_data, filename, separators=(',',':')):
    """
    Write JSON data to a .json file
    """
    import json
    file = open(filename, 'w')
    file.write(json.dumps(json_data,separators=separators))

def read_json_from_file(json_file):
    """
    Read to a Python dictionary from a .json file
    """
    import json
    with open(json_file) as f:
        json_data = json.load(f)
    return(json_data)
