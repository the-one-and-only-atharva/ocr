from multiprocessing import Value
from pathlib import Path

import requests

# magic to identify file format

PDF = (b"%PDF",)
IMAGE = (b"\x89PNG\r\n\x1a\n", b"\xff\xd8\xff")

def download(url, dest, prefixes):
    dest = Path(dest)
    dest.mkdir(parents=True, exist_ok=True)
    
    response = requests.get(url, timeout=60)
    response.raise_for_status()

    if prefixes and not any(response.content.startswith(prefix) for prefix in prefixes):
        raise ValueError("Invalid file format")

    dest.write_bytes(response.content)
    return dest


def download_pdf(url, dest):
    return download(url, dest, prefixes=PDF)

def download_image(url, dest):
    return download(url, dest, prefixes=IMAGE)