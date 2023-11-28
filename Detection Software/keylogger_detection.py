import ast
import os

config_imports = []
config_functions = []

class FileOpenVisitor(ast.NodeVisitor):
    def __init__(self):
        self.logging_filename = None
        self.variables = {}

    #Covers base imports
    def visit_Import(self, node):
        for alias in node.names:
                for module in config_imports:
                    if alias.name == module:
                        print(f"{module} module imported at line {node.lineno}")
        self.generic_visit(node)

    #Covers Import ... from ...
    def visit_ImportFrom(self, node):
            for module in config_imports:
                if node.module == module:
                    print(f"{module} module imported at line {node.lineno}")

    #Goes through all base level variables (variables with value attached)
    def visit_Assign(self, node):
        for target in node.targets:
            if isinstance(target, ast.Name) and isinstance(node.value, ast.Str):
                self.variables[target.id] = node.value.s
        self.generic_visit(node)

    #Covers any Calling function
    def visit_Call(self, node):
        for function in config_functions:
            if (
                isinstance(node.func, ast.Attribute) and
                isinstance(node.func.value, ast.Name) and
                node.func.value.id == function
            ):
                print(f"Function call {function} called at {node.lineno}")

                #Configuration of a logging file
                for keyword in node.keywords:
                    if keyword.arg == 'filename':
                        variable_name = keyword.value.id
                        self.logging_filename = self.variables[variable_name]
                        print(f"Logging to file configured at line {node.lineno}, filename: {self.logging_filename}")

        self.generic_visit(node)

#Load Python File
def check_python_file(filename):
    with open(filename, 'r') as file:
        code = file.read()
        tree = ast.parse(code, filename=filename)

    visitor = FileOpenVisitor()
    visitor.visit(tree)

##TODO Improve the Logic FLow here
def read_config_file(filepath):
    config_import_boolean = False
    config_function_boolean = False
    with open(os.path.join(filepath, 'config.txt'), 'r') as file:
        for line in file:
            line = line.strip().lower()
            if "##" in line:
                config_function_boolean = False
                config_import_boolean = False
            if((line == '##imports') | config_import_boolean):
                config_import_boolean = True
                config_imports.append(line)
            if((line == '##function value id') | config_function_boolean):
                config_function_boolean = True
                config_functions.append(line)


    
    #Remove Headings in config file
    del config_imports[0]
    del config_functions[0]
    print(config_functions)

def find_weight():
    return

if __name__ == '__main__':
    os.chdir(os.path.dirname(__file__))
    os.chdir('../')
    keylogger_path = os.path.join(os.getcwd(), 'RansomWare\python files\keylogger.py')
    read_config_file(os.path.dirname(__file__))
    check_python_file(keylogger_path)