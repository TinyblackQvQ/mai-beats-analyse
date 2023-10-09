from keyType import keyType
import json

map = []
file_path = "output.bmai"
file = open(file_path, "r")
out_file_path = "output.bmaic"
out_file = open(out_file_path, "w+")

raw = ""

for item in file.readlines():
    raw += item

raw = raw.replace("\n", "").replace(" ", "").replace("-", "").replace("_", "")


def read_type(char, key: dict) -> str:
    if char == "t":
        key["type"] = keyType.tap
    elif char == "h":
        if key["type"] == keyType.touch:
            key["type"] = keyType.touchHold
        else:
            key["type"] = keyType.hold
    elif char == "s":
        key["type"] = keyType.slide
    elif char == "o":
        if key["type"] == keyType.hold:
            key["type"] = keyType.touchHold
        else:
            key["type"] = keyType.touch
    else:
        return char


def read_direction(char, key: dict) -> str:
    if char == "l":
        key["direction"] = "left"
        return
    elif char == "r":
        key["direction"] = "right"
        return
    else:
        return char


def read_c_b_x_f(char, key: dict) -> str:
    if char == "c":
        key["chain"] = True
        return
    elif char == "b":
        key["break"] = True
        return
    elif char == "x":
        key["protected"] = True
    elif char == "f":
        key["firework"] = True
    else:
        return char


def read_extra(char, key: dict) -> str:
    if char == "a":
        key["nohead"] = True
    elif char == "z":
        key["noend"] = True
    else:
        return char


def read_duration(raw: str, p: int, key: dict) -> int:
    if raw[p] == "<":
        result = read_until(raw, p + 1, ">")
        key["beat"] = int(result[0])
    elif raw[p] == "[":
        result = read_until(raw, p + 1, "]")
        mapped = result[0].split(":")
        key["duration"] = (mapped[0], mapped[1])
    return result[1]


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


# beats per minute
bpm = 0
offset = 0

time_per_beat = 0
time_stamp = 0
beats = 0
now_line = None

p = 0

line_map = []

while p < len(raw):
    ch = raw[p]
    if ch == "(":
        ## 设置bpm
        result = read_until(raw, p + 1, ")")
        bpm = int(result[0])
        p = result[1] + 1  # 移动pointer
        continue

    elif ch == "<":
        ## 设置新的line
        if now_line != None:
            line_map.append(now_line.copy())
        line = {"time": time_stamp, "contain": []}
        p = read_duration(raw, p, line) + 1
        now_line = line
        continue

    elif ch == "{":
        # 设置分音
        result = read_until(raw, p + 1, "}")
        beats = int(result[0])
        p = result[1] + 1
        time_per_beat = 60 * 4 * 1000 * 1000 / bpm / beats
        continue

    elif ch == ",":
        # 增加时间戳
        time_stamp += time_per_beat
        p += 1

    elif ch == "E":
        if now_line != None:
            line_map.append(now_line.copy())
        break

    else:
        # 添加按键
        result = read_until(raw, p, ",", "/")
        content = result[0]
        p = result[1]
        if raw[result[1]] == "/":
            p += 1
        key = {
            "time": time_stamp,
            "type": "default",
            "direction": "default",
            "duration": (0, 0),
            "combined": False,
            "chain": False,
            "protected": False,
            "break": False,
            "firework": False,
            "nohead": False,
            "noend": False,
        }
        i = 0
        while i < len(content):
            item = content[i]
            if item == "[":
                i = read_duration(content, i, key)
            else:
                read_extra(
                    read_c_b_x_f(read_direction(read_type(item, key), key), key), key
                )
            i += 1

        now_line["contain"].append(key.copy())

last_key = None
for line in line_map:
    for item in line["contain"]:
        if last_key is not None and item['time'] == last_key['time']:
            last_key['combined'] = True
            item['combined'] = True
        if last_key is not None:
            last_key['time'] = int(last_key["time"] / 1000)
        last_key = item

out_file.write(json.dumps(line_map, indent=4))