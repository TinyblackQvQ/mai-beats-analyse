import re
touchPattern = re.compile(r'[ABCDE][12345678]')
holdPattern = re.compile(r'[12345678]h')

file_path = 'map.mai'
file = open(file_path, "r")
output_file_path = 'output.bmai'
output_file = open(output_file_path, 'w+')

raw = ""
for line in file.readlines():
    raw += line
    
def str_replace(str, target, *args):
    for item in args:
        str = str.replace(item, target)
    return str

raw = str_replace(raw, '', ' ')
raw = str_replace(raw, '-', 'w', '<', '>', 'z', 'Z', 'v', 'V')

raw = re.sub(touchPattern, 'o', raw)
raw = re.sub(holdPattern, 'h', raw)

def check_is_number(char):
    try:
        int(char)
    except ValueError:
        return False
    return True

ignored = False
after = ""
for char in raw:
    if char == '(' or char == '{' or char == '[':
        ignored = True
    elif char == ')' or char == '}' or char == ']':
        ignored = False
    else:
        if not ignored:
            if check_is_number(char):
                after += 't'
                continue
    after += char

raw = after

output_file.write(raw)
output_file.flush()