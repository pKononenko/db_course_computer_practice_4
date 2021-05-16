
from os import path, listdir

def get_filenames(dir_name):
    if not path.exists(dir_name):
        return []

    filenames = listdir(dir_name)
    filenames = [dir_name + f"/{dir_elem}" for dir_elem in filenames]
    return filenames

def float_int_check(elem):
    is_int, is_float = False, False
    try:
        d = int(elem)
        is_int = True
    except:
        pass

    if is_int:
        return int(elem)

    try:
        d = float(elem)
        is_float = True
    except:
        pass

    return float(elem) if is_float else elem

def create_dict(keys, values):
    result_dict = {}
    for key, value in zip(keys, values):
        result_dict[key] = value
    return result_dict

def query_to_csv(list_to_csv, filename="results.csv"):
    with open("results/" + filename, "w") as result_csv:
        result_csv.write("Region,MinResult,Year\n")
        for elem in list_to_csv:
            _id_dict = elem.get('_id')
            result_csv.write(f"{_id_dict.get('Region')},{elem.get('Min_Result')},{_id_dict.get('Year')}\n")
