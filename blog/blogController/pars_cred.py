import re


def init_cred():
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
