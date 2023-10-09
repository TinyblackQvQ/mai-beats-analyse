bpm = -1
beats = 0
offset = -43-40

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

def read_until(end_char):
    global p, time_stamp, time_per_beat
    buffer = ""
    p += 1
    while p < len(mai_map):
        try:
            char = mai_map[p]
        except IndexError:
            break
        if char == ',':
            time_stamp += time_per_beat
        if char == end_char:
            break
        else:
            buffer += char
            p += 1
    return buffer

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
    
    if char == '(':
        wait_for_input = True
        bpm = int(read_until(')'))

    elif char == '{':
        wait_for_input = True
        beats = int(read_until('}'))
        time_per_beat = 4 * 60 * 1000 * 1000 / bpm / beats
    
    elif char == 'h':
        append_to_map("hold", time_stamp, True)
        read_until(']')
    
    elif char == '/':
        read_until(',')
    
    elif char == ',':
        time_stamp += time_per_beat
    
    elif contains(char, ['A','B','C','D','E']):
        append_to_map("touch", time_stamp, False)
        read_until(',')
    
    elif contains(char, ['1','2','3','4','5','6','7','8']):
        if read_until(',').find('b') != -1:
            append_to_map("tap", time_stamp, True)
        else:
            append_to_map("tap", time_stamp, False)
    p += 1


for item in time_map:
    item['time'] = int(item['time'] / 1000 + offset)
    print(item)

out = open('output.txt','w+')

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
    elif item['time'] - last_time <= 10:
        out.write(f"192,192,{item['time']},1,0,0:0:0:0:\n")
    else:
        out.write(f"64,192,{item['time']},1,0,0:0:0:0:\n")
    last_time = item['time']