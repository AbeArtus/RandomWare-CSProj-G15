import ast
import os
import json
import glob
import csv

config_items = {}
default_weight = 50

class FileOpenVisitor(ast.NodeVisitor):
    def __init__(self, csv_writer):
        self.csv_writer = csv_writer
        self.variables = {}

    # Combined visit_Import method
    def visit_Import(self, node):
        for alias in node.names:
            weight = config_items["Libraries"].get(alias.name, default_weight)
            self.csv_writer.writerow(['Import', alias.name, node.lineno, weight])
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        module = node.module
        if module in config_items["Libraries"]:
            for name in node.names:
                weight = config_items["Libraries"].get(name.name, default_weight)
                self.csv_writer.writerow(['Import ... from ...', f'From {module} import {name.name}', node.lineno, weight])
        self.generic_visit(node)


    #Goes through all base level variables (variables with value attached)
    def visit_Assign(self, node):
        for target in node.targets:
            if isinstance(target, ast.Name) and isinstance(node.value, ast.Str):
                self.variables[target.id] = node.value.s
        self.generic_visit(node)


    # Covers any Calling function
    '''def visit_Call(self, node):
        if isinstance(node.func, ast.Attribute) and isinstance(node.func.value, ast.Name):
            # Check for method call
            method_call = f"{node.func.value.id}.{node.func.attr}"
            if method_call in config_items["Functions"]:
                print(f"Method call '{method_call}' at line {node.lineno}")

        elif isinstance(node.func, ast.Name):
            # Check for direct function call
            if node.func.id in config_items["Functions"]:
                print(f"Direct function call '{node.func.id}' at line {node.lineno}")

        # Check for functions passed as arguments
        for arg in node.args:
            if isinstance(arg, ast.Name) and arg.id in config_items["Functions"]:
                print(f"Function '{arg.id}' used as argument at line {node.lineno}")

        for keyword in node.keywords:
            if isinstance(keyword.value, ast.Name) and keyword.value.id in config_items["Functions"]:
                print(f"Function '{keyword.value.id}' used as named argument '{keyword.arg}' at line {node.lineno}")

        self.generic_visit(node)'''

#### difference is this one can detect all functions from any of the imported libraries
    def visit_Call(self, node):
        if isinstance(node.func, ast.Attribute) and isinstance(node.func.value, ast.Name):
            library_name = node.func.value.id
            full_function_name = f"{library_name}.{node.func.attr}"
            weight = config_items["Functions"].get(full_function_name, default_weight)

            self.csv_writer.writerow(['Function call', full_function_name, node.lineno, weight])

        elif isinstance(node.func, ast.Name):
            weight = config_items["Functions"].get(node.func.id, default_weight)
            self.csv_writer.writerow(['Direct function call', node.func.id, node.lineno, weight])

        # Check for functions passed as arguments
        for arg in node.args:
            if isinstance(arg, ast.Attribute) and isinstance(arg.value, ast.Name):
                library_or_sublibrary_name = arg.value.id
                method_name = arg.attr
                full_function_name = f"{library_or_sublibrary_name}.{method_name}"
                weight = config_items["Functions"].get(full_function_name, default_weight)

                self.csv_writer.writerow(['Function as argument', full_function_name, node.lineno, weight])

            elif isinstance(arg, ast.Name) and arg.id in config_items["Functions"]:
                weight = config_items["Functions"].get(arg.id, default_weight)
                self.csv_writer.writerow(['Function as argument', arg.id, node.lineno, weight])

        for keyword in node.keywords:
            if isinstance(keyword.value, ast.Attribute) and isinstance(keyword.value.value, ast.Name):
                library_or_sublibrary_name = keyword.value.value.id
                method_name = keyword.value.attr
                full_function_name = f"{library_or_sublibrary_name}.{method_name}"
                weight = config_items["Functions"].get(full_function_name, default_weight)

                self.csv_writer.writerow(['Named function as argument', full_function_name, node.lineno, weight])

            elif isinstance(keyword.value, ast.Name) and keyword.value.id in config_items["Functions"]:
                weight = config_items["Functions"].get(keyword.value.id, default_weight)
                self.csv_writer.writerow(['Named function as argument', keyword.value.id, node.lineno, weight])

        self.generic_visit(node)

# Load Python File

def check_python_file(filename):
    with open(filename, 'r') as file:
        code = file.read()
        tree = ast.parse(code, filename=filename)

    visitor = FileOpenVisitor()
    visitor.visit(tree)

def read_config_file(filepath):
    global config_items
    with open(os.path.join(filepath, 'config.json'), 'r') as file:
        data = json.load(file)
        config_items = extract_config_items(data)

def extract_config_items(data):
    extracted_items = {"Libraries": {}, "Functions": {}}
    for category in ["Libraries", "Functions"]:
        for subcategory, items in data[category].items():
            for item in items:
                for key, value in item.items():
                    weight = value.get("weight", default_weight) 
                    extracted_items[category][key] = weight
    return extracted_items


def find_weight():
    return

def process_python_file(filename, directory_path):
    # Create a CSV file name based on the Python file name
    csv_filename = os.path.splitext(os.path.basename(filename))[0] + '.csv'
    csv_file_path = os.path.join(directory_path, csv_filename)

    with open(csv_file_path, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['Type', 'Detail', 'Line Number', 'Weight'])

        with open(filename, 'r') as file:
            code = file.read()
            tree = ast.parse(code, filename=filename)
            visitor = FileOpenVisitor(csv_writer)
            visitor.visit(tree)

def process_directory(directory_path):
    python_files = glob.glob(os.path.join(directory_path, '*.py'))

    for file in python_files:
        print(f"Processing file: {file}")
        process_python_file(file, directory_path)

if __name__ == '__main__':
    directory_path = input("Enter the path to the directory containing Python files: ")
    if os.path.isdir(directory_path):
        read_config_file(os.path.dirname(__file__))
        process_directory(directory_path)
    else:
        print("Invalid directory path")
# if __name__ == '__main__':
#     os.chdir(os.path.dirname(__file__))
#     os.chdir('../')
#     keylogger_path = os.path.join(os.getcwd(), 'RansomWare\python files\keylogger.py')
#     read_config_file(os.path.dirname(__file__))
#     check_python_file(keylogger_path)
