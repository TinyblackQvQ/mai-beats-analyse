bpm = -1
beats = 0
offset = 0

global time_per_beat
time_per_beat = 0

mai_map = ""

while True:
    input_ = input()
    if input_ == "EOF":
        break
    else:
        mai_map += input_

print(mai_map)

global p
global time_stamp

p = 0
time_stamp = 0

global time_map
time_map = []


# def read_until(end_char):
#     global p, time_stamp, time_per_beat
#     buffer = ""
#     p += 1
#     while p < len(mai_map):
#         try:
#             char = mai_map[p]
#         except IndexError:
#             break
#         if char == ',':
#             time_stamp += time_per_beat
#         if char == end_char:
#             break
#         else:
#             buffer += char
#             p += 1
#     return buffer

def read_until(str: str, p: int, *args) -> tuple:
    """read something in string until faced specific chars

    Args:
        str (str): the whole string
        p (int): start point
        args (str): the specific chars

    Returns:
        tuple: (the content, the end point)

    Example:
        read_until('0[123]456', 2, ']') -> ('123', 5)
                               (1)                (])
    """
    buffer = ""
    b = False
    while p < len(str):
        ch = str[p]
        for item in args:
            if ch == item:
                b = True
        if b:
            break
        else:
            buffer += ch
            p += 1
    return (buffer, p)


def contains(obj, *args):
    if type(args[0]) is list:
        args = args[0]
    for item in args:
        if obj == item:
            return True
    return False


def append_to_map(key_type, time_stamp, is_break: bool):
    global time_map
    if len(time_map) != 0 and time_map[-1]['time'] == time_stamp:
        if is_break:
            time_map[-1]['break'] = True
    else:
        time_map.append({'time': time_stamp, 'type': key_type, 'break': is_break})


while p < len(mai_map):
    char = mai_map[p]

    if char == "(":
        ## 设置bpm
        result = read_until(mai_map, p + 1, ")")
        bpm = int(result[0])
        p = result[1] + 1  # 移动pointer
        continue

    elif char == '{':
        # 设置分音
        result = read_until(mai_map, p + 1, "}")
        beats = int(result[0])
        p = result[1] + 1
        time_per_beat = 60 * 4 * 1000 * 1000 / bpm / beats
        continue

    elif char == 'h':
        append_to_map("hold", time_stamp, True)
        p = read_until(mai_map, p, ']')[1] + 1

    elif char == '/':
        p = read_until(mai_map, p, ',')[1]

    elif char == ',':
        time_stamp += time_per_beat
        p += 1

    elif contains(char, ['A', 'B', 'C', 'D', 'E']):
        append_to_map("touch", time_stamp, False)
        p = read_until(mai_map, p, ',')[1]

    elif contains(char, ['1', '2', '3', '4', '5', '6', '7', '8']):
        result = read_until(mai_map, p, ',')
        p = result[1]
        if result[0].find('b') != -1:
            append_to_map("tap", time_stamp, True)
        else:
            append_to_map("tap", time_stamp, False)

for item in time_map:
    item['time'] = int(item['time'] / 1000 + offset)
    print(item)

out = open('../runtime/output.osu', 'w+')

# std out
# last_time = 0
# for item in time_map:
#     if item['break']:
#         out.write(f"400,200,{item['time']},5,2,0:0:0:0:\n")
#     elif item['time'] - last_time >= 150:
#         out.write(f"400,200,{item['time']},5,0,0:0:0:0:\n")
#     else:
#         out.write(f"400,200,{item['time']},1,0,0:0:0:0:\n")
#     last_time = item['time']

# mania out
last_time = 0
for item in time_map:
    if item['break']:
        out.write(f"320,192,{item['time']},1,2,0:0:0:0:\n")
    elif item['type'] == 'touch':
        out.write(f"192,192,{item['time']},1,8,0:0:0:0:\n")
    elif item['time'] - last_time <= 10:
        out.write(f"192,192,{item['time']},1,0,0:0:0:0:\n")
    else:
        out.write(f"64,192,{item['time']},1,0,0:0:0:0:\n")
    last_time = item['time']
