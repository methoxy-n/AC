import hashlib
import pathlib

chunk_size = 128
num = 150


def print_hashsum(content):
    md5 = hashlib.md5()
    md5.update(content)
    print(f'Checksum: {md5.hexdigest()}')

def from_bytes(a):