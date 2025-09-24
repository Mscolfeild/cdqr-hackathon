#!/usr/bin/env python3
import argparse, json, subprocess, re, math, pathlib

LANG_EXT = (".java",".py",".js",".ts",".go",".cs")

def sh(cmd): return subprocess.check_output(cmd, shell=True, text=True).strip()

def changed_files(base, head):
    out = sh(f"git diff --name-only {base} {head}")
    return [f for f in out.splitlines() if f.endswith(LANG_EXT)]

def numstat(base, head):
    out = sh(f"git diff --numstat {base} {head}")
    stats = {}
    for line in out.splitlines():
        parts = line.split("\t")
        if len(parts)==3:
            add, dele, path = parts
            if path.endswith(LANG_EXT) and add.isdigit():
                stats[path] = (int(add), int(dele))
    return stats

def commit_count(path):
    try: return int(sh(f"git rev-list --count HEAD -- '{path}'"))
    except: return 0

def approx_complexity(path):
    try: txt = pathlib.Path(path).read_text(errors="ignore")
    except: return 0
    return len(re.findall(r"\b(if|for|while|case|catch|&&|\|\||\?)\b", txt))

def risk_score(a,d,cx,cc):
    size=a+d
    s=min(1.0, math.log1p(size)/5)
    c=min(1.0, cc/50)
    x=min(1.0, cx/40)
    return round(100*(0.5*s+0.3*c+0.2*x),1)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--base"); ap.add_argument("--head")
    ap.add_argument("--out",default="risk.json"); ap.add_argument("--md",default="risk_issue.md")
    args=ap.parse_args()
    stats=numstat(args.base,args.head)
    items=[]
    for path in changed_files(args.base,args.head):
        a,d=stats.get(path,(0,0))
        cc=commit_count(path); cx=approx_complexity(path)
        r=risk_score(a,d,cx,cc)
        items.append({"file":path,"risk":r})
    items.sort(key=lambda x:x["risk"],reverse=True)
    pathlib.Path(args.out).write_text(json.dumps(items,indent=2))
    md=["### Değişen Dosyalar",""]
    for it in items[:10]:
        md.append(f"- `{it['file']}` → risk {it['risk']}")
    md+=["","### Copilot'tan İstenenler",
         "- Risk sırasına göre JUnit testleri yaz",
         "- Boundary/null/exception senaryoları ekle"]
    pathlib.Path(args.md).write_text("\n".join(md))
if __name__=="__main__": main()
