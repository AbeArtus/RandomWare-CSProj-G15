import ast
import os
import json
import glob
import csv

config_items = {}

class FileOpenVisitor(ast.NodeVisitor):
    def __init__(self, csv_writer):
        self.csv_writer = csv_writer

    # def visit_For(self, node):
    #     print(f"For loop detected at line {node.lineno}")
    #     self.generic_visit(node)

    # def visit_While(self, node):
    #     print(f"While loop detected at line {node.lineno}")
    #     self.generic_visit(node)

    # Covers base imports
    def visit_Import(self, node):
        for alias in node.names:
            if alias.name in config_items["Libraries"]:
                print(f"{alias.name} module imported at line {node.lineno}")
        self.generic_visit(node)

    # Covers 'Import ... from ...'
    def visit_Import(self, node):
        for alias in node.names:
            if alias.name in config_items["Libraries"]:
                self.csv_writer.writerow(['Import', alias.name, node.lineno])
        module = node.module
        if module in config_items["Libraries"]:
            for name in node.names:
                self.variables[name.name] = module
                print(f"From {module} imported {name.name} at line {node.lineno}")
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
        if isinstance(node.func, ast.Attribute):
            library_name = None
            if isinstance(node.func.value, ast.Name):
                library_name = node.func.value.id  # This is the library or sublibrary name

            full_function_name = f"{library_name}.{node.func.attr}" if library_name else node.func.attr
            print(f"Function call '{full_function_name}' at line {node.lineno}")

            if full_function_name in config_items["Functions"]:
                print(f"Tracked function call '{full_function_name}' at line {node.lineno}")
        elif isinstance(node.func, ast.Name):
            # Check for direct function call
            if node.func.id in config_items["Functions"]:
                print(f"Direct function call '{node.func.id}' at line {node.lineno}")

        # Check for functions passed as arguments
        for arg in node.args:
            if isinstance(arg, ast.Attribute) and isinstance(arg.value, ast.Name):
                library_or_sublibrary_name = arg.value.id
                method_name = arg.attr
                full_function_name = f"{library_or_sublibrary_name}.{method_name}"
                if full_function_name in config_items["Functions"]:
                    print(f"Method '{full_function_name}' used as argument at line {node.lineno}")

            elif isinstance(arg, ast.Name) and arg.id in config_items["Functions"]:
                print(f"Function '{arg.id}' used as argument at line {node.lineno}")

        for keyword in node.keywords:
            if isinstance(keyword.value, ast.Attribute) and isinstance(keyword.value.value, ast.Name):
                library_or_sublibrary_name = keyword.value.value.id
                method_name = keyword.value.attr
                full_function_name = f"{library_or_sublibrary_name}.{method_name}"
                if full_function_name in config_items["Functions"]:
                    print(f"Method '{full_function_name}' used as named argument '{keyword.arg}' at line {node.lineno}")

            elif isinstance(keyword.value, ast.Name) and keyword.value.id in config_items["Functions"]:
                print(f"Function '{keyword.value.id}' used as named argument '{keyword.arg}' at line {node.lineno}")

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
                    weight = value.get("weight", 50)  # Default weight is 50
                    extracted_items[category][key] = weight
    return extracted_items


def find_weight():
    return

def process_python_file(filename, csv_writer):
    with open(filename, 'r') as file:
        code = file.read()
        tree = ast.parse(code, filename=filename)
        visitor = FileOpenVisitor(csv_writer)
        visitor.visit(tree)

def process_directory(directory_path):
    python_files = glob.glob(os.path.join(directory_path, '*.py'))

    with open('output.csv', 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['Type', 'Detail', 'Line Number', 'Weight'])

        for file in python_files:
            process_python_file(file, csv_writer)


if __name__ == '__main__':
    directory_path = input("Enter the path to the directory containing Python files: ")
    if os.path.isdir(directory_path):
        read_config_file(os.path.dirname(__file__))
        process_directory(directory_path)
    else:
        print("Invalid directory path")
