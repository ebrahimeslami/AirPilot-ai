import re
from typing import List, Dict

CFR_RE = re.compile(r"40\\s*CFR[^\\n\\r]*")

def chunk_text(text: str, max_len: int = 1000) -> List[Dict]:
    """
    Split long text into smaller, meaningful chunks.
    Each chunk keeps detected CFR citations if present.
    """
    chunks, buf, size = [], [], 0
    for line in text.splitlines():
        buf.append(line)
        size += len(line)
        if size >= max_len:
            segment = "\n".join(buf)
            chunks.append({"text": segment, "citations": CFR_RE.findall(segment)})
            buf, size = [], 0
    if buf:
        segment = "\n".join(buf)
        chunks.append({"text": segment, "citations": CFR_RE.findall(segment)})
    return chunks
