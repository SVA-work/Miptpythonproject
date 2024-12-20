import os
from os import path
from PIL import Image
from io import BytesIO


class CrypterException(Exception):
    pass


def _apply_coding(inp: bytes, key: bytes) -> bytes:
    if key == b"":
        return inp

    result = []
    for i, ch in enumerate(inp):
        result.append((ch ^ key[i % len(key)]).to_bytes(1, 'big', signed=False))
    return b''.join(result)


def encode_file(input_path: str, key: str, output_path: str, **kwargs):
    if not path.isfile(input_path):
        raise CrypterException("Input file doesn't exists")

    inp = open(input_path, 'rb').read()
    try:
        b_key = key.encode('utf-8')
    except UnicodeEncodeError:
        raise CrypterException("Key must contain only ascii chars")
    result = _apply_coding(inp, b_key)

    if not kwargs.get('allow_rewrite', False) and path.exists(output_path):
        raise CrypterException("Output file already exists. You can allow rewriting files with 'allow_rewrite=True'")
    if not path.exists(path.dirname(output_path)):
        raise CrypterException("Directory of output file doesn't exists")

    with open(output_path, 'wb') as out:
        out.write(result)

    if kwargs.get('delete_input', False):
        os.remove(input_path)


def decode_file(input_path: str, key: str) -> bytes:
    if not path.isfile(input_path):
        raise CrypterException("Input file doesn't exists")

    inp = open(input_path, 'rb').read()
    try:
        b_key = key.encode('utf-8')
    except UnicodeEncodeError:
        raise CrypterException("Key must contain only ascii chars")
    return _apply_coding(inp, b_key)


def decode_txt(input_path: str, key: str, encoding='utf-8') -> str:
    return decode_file(input_path, key).decode(encoding)


def decode_image(input_path: str, key: str) -> Image:
    return Image.open(BytesIO(decode_file(input_path, key)))


decode_to_file = encode_file
