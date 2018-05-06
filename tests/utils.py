import hashlib
import re


def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def extract(f, filter=None):
    code_blocks = []
    while True:
        line = f.readline()
        if not line:
            break

        out = re.match('[^`]*```(.*)$', line)
        if out:
            if filter and filter.strip() != out.group(1).strip():
                continue
            code_block = [f.readline()]
            while re.search('```', code_block[-1]) is None:
                code_block.append(f.readline())
            code_blocks.append(''.join(code_block[:-1]))
    return code_blocks
