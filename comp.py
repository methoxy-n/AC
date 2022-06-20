import pathlib
import sys
import struct
import decimal
import tools


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

    tools.print_hashsum(content)

    output = open(f"{pathlib.Path(name)}.ac", "wb")
    output.write((len(prob) % 256).to_bytes(1, byteorder="big"))

    for key in prob:
        output.write(key)
        output.write(prob[key].to_bytes(4, byteorder="big"))
    for key in prob:
        prob[key] /= decimal.Decimal(counter)

    prob_id = {k: v for k, v in zip(prob.keys(), range(len(prob)))}
    prob = [v for v in prob.values()]
    for i in range(1, len(prob)):
        prob[i] += prob[i - 1]
    prob.insert(0, 0)
    prob[len(prob) - 1] = decimal.Decimal(1)
    print(prob)
    print(prob_id)
    chunk_size = 4
    start, end = decimal.Decimal(0), decimal.Decimal(1)
    chunk = 0
    result = 0
    for item in content:
        interval = end - start
        end = start + interval * prob[prob_id[item.to_bytes(1, byteorder="big")] + 1]
        start = start + interval * prob[prob_id[item.to_bytes(1, byteorder="big")]]
        chunk += 1
        if chunk == 8:
            chunk = 0
            result = int(256 ** chunk_size * (end + start) / 2)
            output.write(result.to_bytes(chunk_size, byteorder="big"))
            print(result, end=' ')
            start, end = decimal.Decimal(0), decimal.Decimal(1)
    if chunk:
        result = int(256 ** chunk_size * (end + start) / 2)
        output.write(result.to_bytes(chunk_size, byteorder="big"))
        print(result)


if __name__ == '__main__':
    compress()
