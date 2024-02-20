import re

#C% COMPILER INTO C++ 1.0 STABLE VERSION.

input_file = 'compilers/main.cp'

replacement_dict = {
    r'console.out\(\'(.*?)\'\)': r'std::cout << "\1" << std::endl;',
    'import cp': '#include <iostream>',
    'return class': 'return 0;',
    'class': 'int',
    'def': 'void',
}

def compile():
    print('cp -code main.cp -cpp\n')
    print(modified_code)

def replace_print_with_console_out(code):
    for pattern, replacement in replacement_dict.items():
        code = re.sub(pattern, replacement, code)
    return code

with open(input_file, 'r') as file:
    code = file.read()

modified_code = replace_print_with_console_out(code)

compile()
