import json
import os
from pathlib import Path

import boto3

from download import detect

MODEL_ID = "qwen.qwen3-vl-235b-a22b"
REGION = "ap-south-1"
KEYS = ("name", "dob", "gender", "aadhaar_number")
PROMPT = """Extract fields from this Indian Aadhaar card.
Return only JSON with exactly these keys: name, dob, gender, aadhaar_number.
gender is Male or Female. Use null for anything you cannot read. No markdown."""


def load_key():
    for line in Path(".env").read_text().splitlines():
        key, _, value = line.partition("=")
        if key.strip() == "AWS_BEARER_TOKEN_BEDROCK":
            os.environ["AWS_BEARER_TOKEN_BEDROCK"] = value.strip().strip('"')
            return
    raise SystemExit("AWS_BEARER_TOKEN_BEDROCK missing from .env")


def content_block(path):
    data = Path(path).read_bytes()
    fmt = detect(data)
    if fmt == "pdf":
        return {"document": {"format": "pdf", "name": "aadhaar", "source": {"bytes": data}}}
    return {"image": {"format": fmt, "source": {"bytes": data}}}


def ocr(path):
    load_key()
    client = boto3.client("bedrock-runtime", region_name=REGION)
    response = client.converse(
        modelId=MODEL_ID,
        messages=[{"role": "user", "content": [{"text": PROMPT}, content_block(path)]}],
        inferenceConfig={"maxTokens": 1024, "temperature": 0},
    )
    text = response["output"]["message"]["content"][0]["text"]
    raw = json.loads(text[text.find("{") : text.rfind("}") + 1])
    return {key: raw.get(key) for key in KEYS}
