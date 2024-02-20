from tkinter import filedialog
from tkinter import *
import ctypes
import re
import os

print(f'IntStudio | SNAPSHOT-1.0') # DON'T TOUCH THIS IF YOU CONTRIBUTE SOMETHING
print('Made by watakak | Forked from IntCode')
print('https://github.com/watakak/IntStudio')

#IntStudio is a complete rewrite of IntCode.
#It's based on Intcode's 1.3 version, because next ones are kinda buggy and not stable at all.

def cp_compile(event=True):
    with open('compilers/main.cp', 'w', encoding='utf-8') as f:
        f.write(editArea.get('1.0', END))

    os.system('start cmd /K "python compilers/cp/compiler.py"')  # or (Linux['ubuntu'])

def cp_code_cs(event=True):
    with open('compilers/main.cp', 'w', encoding='utf-8') as f:
        f.write(editArea.get('1.0', END))

    os.system('start cmd /K "python compilers/cp/cs_code.py"')  # or (Linux['ubuntu'])

def cp_code_cpp(event=True):
    with open('compilers/main.cp', 'w', encoding='utf-8') as f:
        f.write(editArea.get('1.0', END))

    os.system('start cmd /K "python compilers/cp/cpp_code.py"')  # or (Linux['ubuntu'])

def changes(event=True):
    global previousText, repl_italic, repl_bold

    if editArea.get('1.0', END) == previousText:
        return

    for tag in editArea.tag_names():
        editArea.tag_remove(tag, '1.0', 'end')

    i = 0
    for pattern, color in repl:
        for start, end in search_re(pattern, editArea.get('1.0', END)):
            editArea.tag_add(f'{i}', start, end)
            editArea.tag_config(f'{i}', foreground=color)

            i += 1

    previousText = editArea.get('1.0', END)

    pattern = re.compile(repl_italic)

    num_of_lines = int(editArea.index("end").split(".")[0])

    # Добавляем тег "italic" для каждой строки
    for line_num in range(1, num_of_lines + 1):
        line_start = f"{line_num}.0"
        line_end = f"{line_num}.end"
        for match in pattern.finditer(editArea.get(line_start, line_end)):
            start_index = match.start()
            end_index = match.end()
            editArea.tag_add("italic", f"{line_start}+{start_index}c", f"{line_start}+{end_index}c")
            editArea.tag_config("italic", font=(font, font_size, "italic"))

def search_re(pattern, text):
    matches = []
    text = text.splitlines()

    for i, line in enumerate(text):
        for match in re.finditer(pattern, line):
            matches.append((f'{i + 1}.{match.start()}', f'{i + 1}.{match.end()}'))

    return matches

def rgb(rgb):
    return '#%02x%02x%02x' % rgb

def handle_opening_bracket(event):
    opening_bracket = event.char

    brackets = {
        "(": ")",
        "{": "}",
        "[": "]",
        "'": "'",
        '"': '"',
        '<': '>'
    }

    if opening_bracket in brackets:
        closing_bracket = brackets[opening_bracket]
        editArea.insert(INSERT, closing_bracket)
        editArea.mark_set(INSERT, f"{INSERT}-1c")

def handle_tab(event):
    editArea.insert(INSERT, " " * 4)
    return 'break'

def handle_enter(event):
    cursor_position = editArea.index(INSERT)

    current_line_text = editArea.get(f"{cursor_position} linestart", cursor_position)

    if current_line_text.endswith(":"):
        indent = len(current_line_text) - len(current_line_text.lstrip())

        editArea.insert(INSERT, "\n" + " " * (indent + 4))
        return "break"
    else:
        indent = len(current_line_text) - len(current_line_text.lstrip())
        next_char = editArea.get(cursor_position)

        if next_char in [")", "]", "}"]:
            editArea.insert(INSERT, f"\n{' ' * (indent + 4)}\n")
            editArea.mark_set(INSERT, f"{cursor_position}+5c")
        else:
            editArea.insert(INSERT, "\n" + " " * indent)
        return "break"

def handle_backspace(event):
    cursor_position = editArea.index(INSERT)

    current_line_text = editArea.get(f"{cursor_position} linestart", cursor_position)

    if current_line_text.endswith("    "):
        editArea.delete(f"{cursor_position}-4c", cursor_position)
        return "break"

    prev_char = editArea.get(cursor_position + " - 1c")
    next_char = editArea.get(cursor_position)

    brackets = {
        "(": ")",
        "{": "}",
        "[": "]",
        "'": "'",
        '"': '"',
        '<': '>'
    }

    if prev_char in brackets and next_char in brackets.values() and brackets[prev_char] == next_char:
        editArea.delete(cursor_position, f"{cursor_position}+1c")

    return None

def handle_enter_second(event):
    sel_start, sel_end = editArea.tag_ranges("sel")

    if not sel_start or not sel_end:
        return

    text = editArea.get(sel_start, sel_end)

    if text in ["()", "[]", "{}"]:
        cursor = editArea.index(INSERT)

        row, col = map(int, cursor.split("."))
        new_row, new_col = row + 2, col

        editArea.delete(sel_start, sel_end)
        editArea.insert(f"{new_row}.{new_col}", text)

        editArea.insert(cursor, "\n" + " " * 4)

        editArea.mark_set(INSERT, f"{new_row}.{new_col + 4}")

def on_font_change(event):
    current_font_size = int(editArea['font'].split()[1])
    if event.num == 5 or event.delta == -120:
        new_font_size = max(current_font_size - 1, 10)
    elif event.num == 4 or event.delta == 120:
        new_font_size = min(current_font_size + 1, 45)
    else:
        return

    editArea.yview_moveto(editArea.yview()[0])
    editArea['yscrollcommand'] = None

    editArea.configure(font=(font, new_font_size))

def highlight_functions(text):
    pattern = r'\b\w+\('

    for match in re.finditer(pattern, text):
        func_name = match.group()[:-1]
        if func_name in globals() or func_name in locals():
            yield match.start(), match.end(), function

def new_file():
    editArea.delete("1.0", END)

def save_file():
    file = filedialog.asksaveasfile(mode="w", defaultextension=".txt")
    if file is not None:
        text = str(editArea.get(1.0, END))
        file.write(text)
        file.close()

def open_file():
    file = filedialog.askopenfile(mode="r")
    if file is not None:
        content = file.read()
        editArea.delete(1.0, END)
        editArea.insert(END, content)
        file.close()

def exit_program():
    root.destroy()

def about_github():
    os.system('start https://github.com/watakak/IntStudio')

ctypes.windll.shcore.SetProcessDpiAwareness(True)

sw = '700'
hw = '500'
shw = f'{sw}x{hw}'

root = Tk()
root.geometry(shw)
root.title(f'IntStudio | main.cp')
previousText = ''

background = rgb((48, 56, 65))
dark_background = rgb((30, 34, 42))
select_background = rgb((78, 86, 95))
normal = rgb((195, 195, 195))
w1 = rgb((198, 139, 198))
w2 = rgb((97, 175, 239))
w3 = rgb((249, 123, 87))
w4 = rgb((236, 96, 102))
w5 = rgb((102, 153, 204))
w6 = rgb((229, 192, 123))
w7 = rgb((249, 174, 87))
w8 = rgb((236, 96, 102))
comments = rgb((166, 172, 185))
string = rgb((153, 199, 148))
function = rgb((95, 211, 234))
font = 'Consolas'
font_size = 18

repl = [
    ['(?<=\.)\w+', w2],
    ['(^| )(and|as|assert|async|await|break|continue|del|else|except|finally'
     '|from|global|include|if|elif|import|is|lambda|nonlocal|not|or|pass|raise|return|try|while|with|yield|int|str|float|complex'
     'float|complex|list|tuple|range|dict|get|bool|set|frozeenset|using|func)($| )', w1],
    ['(public|args|const)', w4],
    ['(?<!self)(?=\w+)', w8],
    ['\w+(?=\()', w2],
    ['(self|False|True|System)', w8],
    [r'==|!=|>|<|>=|<=|=|\+|\-|\*|\/|\%', w3],
    ['(None)', w4],
    ['".*?"', string],
    ['\".*?\"', string],
    ['\'.*?\'', string],
    ['(?<=class\s)\w+', w2],
    ['(class)', w6],
    ['(let|static|var)', w1],
    ['(?<=let\s)\w+', w2],
    ['(?<=def\s)\w+', w2],
    ['def', w1],
    ['(?<!\w)\\d+(?!\w)', w7],
    ['(write|println|open|__init__|for)', w5],
    ['(print|log|input|void)', w5],
    ['(console\.log)', w5],
    ['#.*?$', comments],
    ['//.*?$', comments],
    ['"[^"]*"', string],
    ["'[^']*'", string],
    ['\\\\[ntrbftv0]', w4],
    ['f(?=[\'"])', string],
]

repl_italic_open = '(True|False|__main__|__name__|__init__|None|self|args|str|bool|float|int|println|print|open)'

repl_italic_static = '(^| )(if|elif|include|else|void|const|let|global|var|in|and|or|func|try|' \
              'class|def|with|import|as|from|break|continue|return)($| )'

repl_italic_f_stroke = 'f(?=[\'"])'

repl_italic_comments_sharp = '#.*?$'

repl_italic_comments_slashes = '//.*?$'

repl_italic = f"{repl_italic_open}|{repl_italic_static}|{repl_italic_f_stroke}|{repl_italic_comments_sharp}|{repl_italic_comments_slashes}"

editArea = Text(root, background=background, foreground=normal,
                insertbackground=normal, selectbackground=select_background,
                selectforeground=normal, relief=FLAT, borderwidth=10,
                font=(font, font_size), undo=True)

editArea.pack(fill=BOTH, expand=1)
editArea.insert('1.0', '''import cp

class main() {
    console.out('Welcome to IntStudio!')
    
    return class
}
''')

mmenu = Menu(root)
root.config(menu=mmenu)

file = Menu(mmenu, tearoff=False)
edit = Menu(mmenu, tearoff=False)
about = Menu(mmenu, tearoff=False)

mmenu.add_cascade(label="File", menu=file)
mmenu.add_cascade(label="Edit", menu=edit)
mmenu.add_cascade(label="About", menu=about)

editArea.bind('<KeyRelease>', changes)
editArea.bind("<KeyPress>", handle_opening_bracket)
editArea.bind("<Tab>", handle_tab)
editArea.bind('<Return>', handle_enter)
editArea.bind("<BackSpace>", handle_backspace)
editArea.bind('<Control-MouseWheel>', on_font_change)

file.add_command(label="New File", command=new_file, accelerator="Ctrl+N")
editArea.bind("<Control-n>", new_file)
file.add_command(label="Open File...", command=open_file, accelerator="Ctrl+O")
editArea.bind("<Control-o>", open_file)
file.add_command(label="Save As...", command=save_file, accelerator="Ctrl+S")
editArea.bind("<Control-s>", save_file)
file.add_separator()
file.add_command(label="Compile and Run", command=cp_compile, accelerator="F5")
editArea.bind("<F5>", cp_compile)

#file.add_command(label="Compile as C# Code", command=cp_code_cs)

file.add_command(label="Compile as C++ Code", command=cp_code_cpp, accelerator="F6")
editArea.bind("<F6>", cp_code_cpp)
file.add_separator()
file.add_command(label="Exit", command=exit_program, accelerator="Alt+F4")

def undo(event=None):
    editArea.edit_undo()
def redo(event=None):
    editArea.edit_redo()

edit.add_command(label='Undo', command=undo, accelerator="Ctrl+Z")
editArea.bind("<Control-Z>", undo)
edit.add_command(label='Redo', command=redo, accelerator="Ctrl+Shift+Z")
editArea.bind("<Control-Shift-Z>", redo)

about.add_command(label="GitHub Repo", command=about_github)

changes()

root.mainloop()
