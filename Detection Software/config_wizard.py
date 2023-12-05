import sys
import os
import json

def menu():
    user_input = int(input('''Please select an option from the list below:
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
            print("Please insert a number from 1 through 5.")
            menu()

def get_category_input():
    category = input("Enter the category (Libraries or Functions): ").capitalize()
    if category not in ["Libraries", "Functions"]:
        print("Invalid category. Please enter either 'Libraries' or 'Functions'.")
        return get_category_input()
    return category

def get_subcategory_input(data, category):
    subcategories = list(data[category].keys())
    print("Subcategories:")
    for i, subcat in enumerate(subcategories, start=1):
        print(f"[{i}] {subcat}")
    choice = int(input("Select a subcategory: "))
    if 1 <= choice <= len(subcategories):
        return subcategories[choice - 1]
    else:
        print("Invalid choice. Please select a valid subcategory.")
        return get_subcategory_input(data, category)

def add_item():
    data = open_json()
    category = get_category_input()
    subcategory = get_subcategory_input(data, category)

    name = input("Enter the item name: ").lower()
    weight = int(input("Enter the weight: "))

    new_entry = {name: {"weight": weight}}
    
    if name not in data[category][subcategory]:
        data[category][subcategory].append(new_entry)
        write_json(data)
        print(f"Item '{name}' added successfully.")
    else:
        print(f"The item '{name}' already exists in {category} -> {subcategory}.")

    menu()

def edit_item():
    data = open_json()
    category = get_category_input()
    subcategory = get_subcategory_input(data, category)

    print("Items:")
    for i, item in enumerate(data[category][subcategory], start=1):
        item_name = list(item.keys())[0]
        print(f"[{i}] {item_name}")

    choice = int(input("Select an item to edit: "))
    if 1 <= choice <= len(data[category][subcategory]):
        new_name = input("Enter the new name for the item: ").lower()
        data[category][subcategory][choice - 1] = {new_name: data[category][subcategory][choice - 1][list(data[category][subcategory][choice - 1].keys())[0]]}
        write_json(data)
        print("Item name updated successfully.")
    else:
        print("Invalid choice. Please select a valid item.")

    menu()

def edit_weight():
    data = open_json()
    category = get_category_input()
    subcategory = get_subcategory_input(data, category)

    print("Items:")
    for i, item in enumerate(data[category][subcategory], start=1):
        item_name = list(item.keys())[0]
        print(f"[{i}] {item_name}")

    choice = int(input("Select an item to edit its weight: "))
    if 1 <= choice <= len(data[category][subcategory]):
        new_weight = int(input("Enter the new weight: "))
        item_name = list(data[category][subcategory][choice - 1].keys())[0]
        data[category][subcategory][choice - 1][item_name]["weight"] = new_weight
        write_json(data)
        print("Item weight updated successfully.")
    else:
        print("Invalid choice. Please select a valid item.")

    menu()

def remove_item():
    data = open_json()
    category = get_category_input()
    subcategory = get_subcategory_input(data, category)

    print("Items:")
    for i, item in enumerate(data[category][subcategory], start=1):
        item_name = list(item.keys())[0]
        print(f"[{i}] {item_name}")

    choice = int(input("Select an item to remove: "))
    if 1 <= choice <= len(data[category][subcategory]):
        del data[category][subcategory][choice - 1]
        write_json(data)
        print("Item removed successfully.")
    else:
        print("Invalid choice. Please select a valid item.")

    menu()

def open_json():
    try:
        os.chdir(os.path.dirname(__file__))
        os.chdir('../')
        directory_path = os.path.join(os.getcwd(), 'Detection Software/config.json')
        with open(directory_path, 'r') as json_file:
            return json.load(json_file)
    except Exception as e:
        print(f"Error with JSON: {e}")
        sys.exit()

def write_json(data):
    try:
        with open('Detection Software/config.json', 'w') as json_file:
            json.dump(data, json_file, indent=4)
    except Exception as e:
        print(f"Error writing to JSON: {e}")

if __name__ == '__main__':
    menu()
