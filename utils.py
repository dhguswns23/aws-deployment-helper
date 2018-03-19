from termcolor import colored
import json, pprint

def read_json(file_name):
    return json.load(open(file_name))

def write_json(file_name, data):
    with open(file_name, 'w') as outfile:
        json.dump(data, outfile)

def tprint(title, func, *args, **kwargs):
    print(colored("[ON PROCESS] "+title, 'cyan'))
    result = func(*args, **kwargs)
    print(colored("result is ------", "green"))
    print(result)
    print(colored("----------------\n", "green"))
    return result

def tprint_end(msg):
    print(colored("[FINISH] "+msg, 'magenta'))

def tprint_error(error):
    print(+colored("[ERROR] "+error, 'red'))
