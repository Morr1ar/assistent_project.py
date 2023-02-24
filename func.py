def text_wrap(filename):
    text = ""
    text_list = [line.strip() for line in open(filename, encoding="utf-8").readlines()]
    if len(text_list) >= 15:
        count = 15
    else:
        count = len(text_list)
    for i in range(count):
        if len(text_list[i]) > 20:
            x = 0
            while x < len(text_list[i]):
                text += text_list[i][x:x + 20] + '\n'
                x += 20
        else:
            text += text_list[i] + '\n'
    return text
