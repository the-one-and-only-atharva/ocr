from pathlib import Path

import requests

PDF = (b"%PDF",)
IMAGE = (b"\x89PNG\r\n\x1a\n", b"\xff\xd8\xff")
SUFFIX = {
    b"%PDF": ".pdf",
    b"\x89PNG\r\n\x1a\n": ".png",
    b"\xff\xd8\xff": ".jpg",
}


def _suffix(content, prefixes):
    for prefix in prefixes:
        if content.startswith(prefix):
            return SUFFIX[prefix]
    raise ValueError("Invalid file format")


def download(url, dest, prefixes):
    dest = Path(dest)
    dest.mkdir(parents=True, exist_ok=True)

    response = requests.get(url, timeout=60)
    response.raise_for_status()

    path = dest / f"file{_suffix(response.content, prefixes)}"
    path.write_bytes(response.content)
    return path


def download_pdf(url, dest):
    return download(url, dest, prefixes=PDF)


def download_image(url, dest):
    return download(url, dest, prefixes=IMAGE)