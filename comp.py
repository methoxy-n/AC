import pathlib
import sys
import tools
import decimal


def compress():
    name = ''
    raw = ''
    try:
        name = sys.argv[1]
        raw = open(name, "rb")
    except IndexError:
        print("Choose file to compress")
        exit()
    if pathlib.Path(name).suffix == ".ac":
        print("File has already been compressed")
        exit()
    content = raw.read()
    content += (3).to_bytes(1, byteorder="big")
    prob = {}
    counter = 0
    for item in content:
        letter = item.to_bytes(1, byteorder="big")
        if prob.get(letter) is None:
            prob[letter] = 1
        else:
            prob[letter] += 1
        counter += 1

    output = open(f"{pathlib.Path(name)}.ac", "wb")
    output.write(len(prob).to_bytes(1, byteorder="big"))

    decimal.getcontext().prec = 1000

    for key in prob:
        output.write(key)
        output.write(prob[key].to_bytes(4, byteorder="big"))
    for key in prob:
        prob[key] /= decimal.Decimal(counter)

