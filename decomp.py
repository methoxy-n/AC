import tools
import sys
import decimal
import pathlib


def decompress():
    raw = ''
    name = ''
    try:
        name = sys.argv[1]
        raw = open(name, "rb")
    except IndexError:
        print("Choose file to decompress")
        exit()
    if pathlib.Path(name).suffix != ".ac":
        print("File hasn't been compressed yet")
        exit()
    body_size = pathlib.Path(name).stat().st_size

    alph_size = int.from_bytes(raw.read(1), "big")
    unfilled = int.from_bytes(raw.read(1), "big")
    if alph_size == 0:
        alph_size = 256
    body_size -= 2
    counter = [0]
    symbols = []
    current_freq = 0
    for i in range(alph_size):
        symbols.append(raw.read(1))
        current_freq += int.from_bytes(raw.read(4), "big")
        counter.append(current_freq)
        body_size -= 5
    for i in range(alph_size + 1):
        counter[i] = decimal.Decimal(counter[i]) / current_freq
    #print(counter)

    #print(symbols)
    output = open(f"decompressed{pathlib.Path(name).stem}", "wb")
    if unfilled:
        point = tools.from_bytes(int.from_bytes(raw.read(tools.chunk_size), "big"))
        for i in range(unfilled):
            start = bin_search(counter, point)
            point = (point - counter[start]) / (counter[start + 1] - counter[start])
            output.write(symbols[start])
        body_size -= tools.chunk_size

    while body_size > 0:
        point = tools.from_bytes(int.from_bytes(raw.read(tools.chunk_size), "big"))
        chunk = 0
        while chunk < tools.num:
            chunk += 1
            start = bin_search(counter, point)
            #if symbols[start] == b'\x03':
                #break
            point = (point - counter[start]) / (counter[start + 1] - counter[start])
            output.write(symbols[start])
            #print(symbols[start], end='')
        body_size -= tools.chunk_size
    output.close()
    raw.close()
    # print()
    content = open(f"decompressed{pathlib.Path(name).stem}", "rb").read()
    tools.print_hashsum(content)


def bin_search(counter, num):
    low = 0
    high = len(counter) - 2
    while low <= high:
        middle = (low + high) // 2
        if counter[middle] <= num < counter[middle + 1]:
            return middle
        elif num < counter[middle]:
            high = middle - 1
        else:
            low = middle + 1
    raise ValueError


if __name__ == '__main__':
    decimal.getcontext().prec = 1500
    decompress()
