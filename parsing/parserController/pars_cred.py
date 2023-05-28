import re


def get_db():
    file_path = "../../vault/secrets/credentials.txt" 

    with open(file_path, "r") as file:
        data_string = file.read()

    pattern = r'(\w+):([\w-]+)'
    matches = re.findall(pattern, data_string)
    data_dict = {}

    for match in matches:
        key = match[0]
        value = match[1]
        data_dict[key] = value

    dbname = data_dict.get('dbname')
    dbpass = data_dict.get('dbpass')

    return [dbname, dbpass]


def get_gpt():
    file_path = "../../vault/secrets/credentials.txt" 

    with open(file_path, "r") as file:
        data_string = file.read()

    pattern = r'(\w+):([\w-]+)'
    matches = re.findall(pattern, data_string)
    data_dict = {}

    for match in matches:
        key = match[0]
        value = match[1]
        data_dict[key] = value

    gpt = data_dict.get('gpt')

    return gpt


def get_data():
    file_path = "../../vault/secrets/credentials.txt" 

    with open(file_path, "r") as file:
        data_string = file.read()

    pattern = r'(\w+):([\w-]+)'
    matches = re.findall(pattern, data_string)
    data_dict = {}

    for match in matches:
        key = match[0]
        value = match[1]
        data_dict[key] = value

    search = data_dict.get('search')
    dataio = data_dict.get('dataio')

    return [search, dataio]
