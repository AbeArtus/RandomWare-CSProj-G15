import sys
import os
import json

def menu():
    user_input = int(input('''Please select which an option from the list below:
          [1] Insert new item.
          [2] Edit existing item.
          [3] Edit existing weight.
          [4] Remove item.
          [5] Exit.
          '''))
    match user_input:
        case 1:
            add_item()
        case 2:
            edit_item()
        case 3:
            edit_weight()
        case 4:
            remove_item()
        case 5:
            sys.exit()
        case _:
            print("please insert 1 through 5.")
            menu()

def add_item():
    user_input = None
    while user_input not in (1,2):
        user_input = int(input('''Which topic would you like to edit?
                  [1] Import Calls
                  [2] Function Calls
                  '''))
        match user_input:
            case 1:
                data = open_json()
                name = input("Type input name: ").lower()
                weight = input("Type weight: ")
                new_entry = {
                    "name": name,
                    "weight": weight
                }
                if (json_check_key(data, name, 'config_imports') == False):
                    write_json(data, new_entry, 'config_imports')
                else:
                    print(f"key {name} already exists.")

            case 2:
                data = open_json()
                name = input("Type function name: ").lower()
                weight = input("Type weight: ")
                new_entry = {
                    "name": name,
                    "weight": weight
                }
                if (json_check_key(data, name, 'config_function') == False):
                    write_json(data, new_entry, 'config_function')
                else:
                    print(f"print {name} already exists.")

            case _:
                print("Please insert 1 or 2")
    menu()
def edit_item():
    return
def edit_weight():
    return
def remove_item():
    user_input = None
    while user_input not in (1,2):
        user_input = int(input('''Which topic would you like to edit?
                  [1] Import Calls
                  [2] Function Calls
                  '''))
        match user_input:
            case 1:
                data = open_json()
                i = 0
                print(f"which item would you like to remove? ")
                for item in data['config_imports']:
                    i+=1
                    print(f"[{i}] {item.get('name')}")
                index = int(input())
                del data['config_imports'][index - 1]
                write_json(data, None , 'config_imports')
                    
            case 2:
                data = open_json()
                i = 0
                print(f"which item would you like to remove? ")
                for item in data['config_function']:
                    i+=1
                    print(f"[{i}] {item.get('name')}")
                index = int(input())
                del data['config_function'][index - 1]
                write_json(data, None , 'config_function')
            case _:
                print("Please insert 1 or 2")

def open_json():
    try:
        with open(os.path.join(os.path.dirname(__file__), 'config.json'), 'r') as json_file:
            data = json.load(json_file)
    except Exception as e:
        print(f"error with json: {e}")
    return data

def write_json(data, new_entry, key):
    try:
        if new_entry != None:
            data[key].append(new_entry)
        with open(os.path.join(os.path.dirname(__file__), 'config.json'), 'w') as json_file:
            json.dump(data, json_file, indent=2)
    except Exception as e:
        print(f"error: {e}")

def json_check_key(data, name, key):
    for item in data[key]:
        if item.get('name') == name:
            return True
    return False


if __name__ == '__main__':
    menu()