import hashlib
import pathlib

chunk_size = 4
num = 7


def print_hashsum(content):
    try:
        pathlib.Path(content).is_file()
        content = open(content, "rb").read()
    except TypeError:
        if isinstance(content, bytes):
            pass
    finally:
        md5 = hashlib.md5()
        md5.update(content)
        print(f'Checksum: {md5.hexdigest()}')

