#!/usr/bin/env python3
import argparse, re, pathlib, collections

def parse_stacktrace(text):
    exc = re.search(r'([A-Za-z0-9_.]+(?:Exception|Error))[:\s](.*)', text)
    cls = re.findall(r'at\s+([A-Za-z0-9_.]+)\(([^:]+):(\d+)\)', text)
    top = cls[0] if cls else None
    return (exc.group(1) if exc else "UnknownError",
            exc.group(2).strip() if exc else "",
            top)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--log"); ap.add_argument("--out",default="incident_issue.md")
    args=ap.parse_args()
    txt=pathlib.Path(args.log).read_text(errors="ignore")
    errors=collections.Counter(re.findall(r'[A-Za-z0-9_.]+(?:Exception|Error)',txt))
    common=", ".join([f"{k}({v})" for k,v in errors.most_common(5)]) or "n/a"
    exc,msg,top=parse_stacktrace(txt)
    suspect=f"{top[0]}:{top[1]}:{top[2]}" if top else "n/a"
    body=f"""### Semptom Özeti
- En sık hatalar: {common}
- Örnek: {exc} {msg}

### Şüpheli Konum
- {suspect}

### Copilot'tan İstenenler
- Minimal fix PR (gerekirse feature flag)
- 2 regresyon testi ekle
"""
    pathlib.Path(args.out).write_text(body)
if __name__=="__main__": main()
