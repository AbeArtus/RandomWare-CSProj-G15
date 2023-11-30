import ast
import os
import json
import glob

config_items = {}

class FileOpenVisitor(ast.NodeVisitor):
    def __init__(self):
        self.variables = {}

    def visit_For(self, node):
        print(f"For loop detected at line {node.lineno}")
        self.generic_visit(node)

    def visit_While(self, node):
        print(f"While loop detected at line {node.lineno}")
        self.generic_visit(node)

    # Covers base imports
    def visit_Import(self, node):
        for alias in node.names:
            if alias.name in config_items["Libraries"]:
                print(f"{alias.name} module imported at line {node.lineno}")
        self.generic_visit(node)

    # Covers 'Import ... from ...'
    def visit_ImportFrom(self, node):
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
        if isinstance(node.func, ast.Attribute) and isinstance(node.func.value, ast.Name):
            # Check if the call is a method
            if node.func.value.id in config_items["Libraries"]:
                print(f"Method '{node.func.attr}' from the library '{node.func.value.id}' called at line {node.lineno}")
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
    extracted_items = {"Libraries": [], "Functions": []}
    for category in ["Libraries", "Functions"]:
        for subcategory, items in data[category].items():
            for item in items:
                extracted_items[category].extend(item.keys())
    return extracted_items

def find_weight():
    return

def process_python_file(filename):
    with open(filename, 'r') as file:
        code = file.read()
        tree = ast.parse(code, filename=filename)
        visitor = FileOpenVisitor()
        visitor.visit(tree)

def process_directory(directory_path):
    # Get a list of all Python files in the directory
    python_files = glob.glob(os.path.join(directory_path, '*.py'))
    
    # Process each file
    for file in python_files:
        print(f"Processing file: {file}")
        process_python_file(file)

if __name__ == '__main__':
    directory_path = 'C:/Users/Pause/Documents/Python Scripts' 
    read_config_file(os.path.dirname(__file__))
    process_directory(directory_path)