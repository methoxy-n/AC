import tools
import sys
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
    body_size -= 1
    counter = {}
    for _ in range(alph_size):
        char = raw.read(1)
        body_size -= 1
        prob = int.from_bytes(raw.read(4), "big")
        body_size -= 4
        counter[char] = prob
    print(counter)

