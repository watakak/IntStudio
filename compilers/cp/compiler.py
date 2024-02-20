import re

#C% COMPILER 0.1 UNWORKING VERSION.

input_file = 'compilers/main.cp'

replacement_dict = {
    r'console.out\(\'(.*?)\'\)': r'std::cout << "\1" << std::endl;',
    'import cp': '#include <iostream>',
    'return class': 'return 0;',
    'class': 'int',
    'def': 'void',
}

def compile():
    print("cp -run main.cp\nWARNING! Still doesn't work as compiler, wait till next updates.\n")
    print(modified_code)

def replace_print_with_console_out(code):
    for pattern, replacement in replacement_dict.items():
        code = re.sub(pattern, replacement, code)
    return code

with open(input_file, 'r') as file:
    code = file.read()

modified_code = replace_print_with_console_out(code)

compile()
