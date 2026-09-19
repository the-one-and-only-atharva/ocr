from pathlib import Path

import requests

PDF = (b"%PDF",)
IMAGE = (b"\x89PNG\r\n\x1a\n", b"\xff\xd8\xff")
FORMAT = {
    b"%PDF": "pdf",
    b"\x89PNG\r\n\x1a\n": "png",
    b"\xff\xd8\xff": "jpeg",
}
SUFFIX = {
    "pdf": ".pdf",
    "png": ".png",
    "jpeg": ".jpg",
}


def detect(content, prefixes=PDF + IMAGE):
    for prefix in prefixes:
        if content.startswith(prefix):
            return FORMAT[prefix]
    raise ValueError("Invalid file format")


def download(url, dest, prefixes):
    dest = Path(dest)
    dest.mkdir(parents=True, exist_ok=True)

    response = requests.get(url, timeout=60)
    response.raise_for_status()

    fmt = detect(response.content, prefixes)
    path = dest / f"file{SUFFIX[fmt]}"
    path.write_bytes(response.content)
    return path


def download_pdf(url, dest):
    return download(url, dest, prefixes=PDF)


def download_image(url, dest):
    return download(url, dest, prefixes=IMAGE)
