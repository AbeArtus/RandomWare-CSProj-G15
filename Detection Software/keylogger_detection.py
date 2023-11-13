import ast
import os

class FileOpenVisitor(ast.NodeVisitor):
    def __init__(self):
        self.logging_filename = None
        self.variables = {}

    #Covers base imports
    def visit_Import(self, node):
        for alias in node.names:
            if alias.name == 'logging':
                print(f"Logging module imported at line {node.lineno}")
            elif alias.name == 'pynput':
                print(f"Monitoring or Control module imported at line {node.lineno}")
        self.generic_visit(node)

    #Covers Import ... from ...
    def visit_ImportFrom(self, node):
            if node.module == 'pynput':
                print(f"possible keyboard control/monitoring from {node.module} at line {node.lineno}")

    #Goes through all base level variables (variables with value attached)
    def visit_Assign(self, node):
        for target in node.targets:
            if isinstance(target, ast.Name) and isinstance(node.value, ast.Str):
                self.variables[target.id] = node.value.s
        self.generic_visit(node)

    #Covers any Calling function
    def visit_Call(self, node):
        if (
            isinstance(node.func, ast.Attribute) and
            isinstance(node.func.value, ast.Name) and
            node.func.value.id == 'logging' and
            node.func.attr == 'basicConfig'
        ):
            for keyword in node.keywords:
                if keyword.arg == 'filename':
                    variable_name = keyword.value.id
                    self.logging_filename = self.variables[variable_name]
                    print(f"Logging to file configured at line {node.lineno}, filename: {self.logging_filename}")

        self.generic_visit(node)

def check_python_file(filename):
    with open(filename, 'r') as file:
        code = file.read()
        tree = ast.parse(code, filename=filename)

    visitor = FileOpenVisitor()
    visitor.visit(tree)

if __name__ == '__main__':
    current_dir = os.getcwd()

    parent_dir = os.path.dirname(current_dir)
    os.chdir(parent_dir)

    keylogger_path = os.path.join(current_dir, 'RansomWare\keylogger.py')
    check_python_file(keylogger_path)