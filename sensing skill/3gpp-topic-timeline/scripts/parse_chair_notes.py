#!/usr/bin/env python3
"""Unzip downloaded TDocs, convert contained .doc/.docx to text, and build a
section index (heading -> position) per document for chapter/section citations.

Input : directory tree of <mtg>/<TDOC>.zip  (from download_tdocs.py)
Output: --out directory:
   <mtg>/<TDOC>/<original files...>       (extracted)
   <mtg>/<TDOC>.txt                       (concatenated plain text)
   <mtg>/<TDOC>.sections.json             (heading outline with line numbers)
Nested zip attachments are extracted one level deep.

Heading detection: numbered headings ("2", "2.1", "2.1.3") and annex headings
at line starts, plus docx Heading styles when python-docx is available.
"""
import argparse
import json
import os
import re
import sys
import zipfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from convert_doc import to_text  # noqa: E402

HEAD_TXT_RE = re.compile(r"^(\d{1,2}(?:\.\d{1,2}){0,4})\.?\s+(\S.{0,90})$")
ANNEX_RE = re.compile(r"^(Annex\s+[A-Z])[:.\s]\s*(.{0,90})$", re.I)


def docx_outline(path):
    """Return [(heading_text, level)] using python-docx styles, or None."""
    try:
        import docx  # type: ignore
    except ImportError:
        return None
    try:
        d = docx.Document(path)
    except Exception:
        return None
    out = []
    for p in d.paragraphs:
        st = (p.style.name or "") if p.style else ""
        m = re.match(r"Heading (\d)", st)
        if m and p.text.strip():
            out.append({"heading": p.text.strip(), "level": int(m.group(1))})
    return out or None


def txt_outline(text):
    out = []
    for i, l in enumerate(text.split("\n")):
        t = l.strip()
        m = HEAD_TXT_RE.match(t)
        if m and not t.endswith(".") and len(m.group(1)) <= 8:
            out.append({"heading": t, "num": m.group(1), "line": i + 1,
                        "level": m.group(1).count(".") + 1})
            continue
        m = ANNEX_RE.match(t)
        if m:
            out.append({"heading": t, "num": m.group(1), "line": i + 1, "level": 1})
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--in", dest="indir", required=True)
    ap.add_argument("--out", dest="outdir", required=True)
    a = ap.parse_args()
    n = 0
    for root, _dirs, files in os.walk(a.indir):
        for fn in files:
            if not fn.lower().endswith(".zip"):
                continue
            tdoc = os.path.splitext(fn)[0]
            rel = os.path.relpath(root, a.indir)
            exdir = os.path.join(a.outdir, rel, tdoc)
            os.makedirs(exdir, exist_ok=True)
            try:
                with zipfile.ZipFile(os.path.join(root, fn)) as z:
                    z.extractall(exdir)
            except Exception as ex:
                print(f"[WARN] {fn}: bad zip ({ex})", file=sys.stderr)
                continue
            # one level of nested zips (LS attachments)
            for sub in list(os.listdir(exdir)):
                if sub.lower().endswith(".zip"):
                    try:
                        with zipfile.ZipFile(os.path.join(exdir, sub)) as z:
                            z.extractall(os.path.join(exdir, "att_" + os.path.splitext(sub)[0]))
                    except Exception:
                        pass
            texts, outline = [], []
            for r2, _d2, f2 in os.walk(exdir):
                for doc in sorted(f2):
                    if doc.lower().endswith((".doc", ".docx")):
                        p = os.path.join(r2, doc)
                        try:
                            t = to_text(p)
                        except Exception as ex:
                            print(f"[WARN] {p}: {ex}", file=sys.stderr)
                            continue
                        texts.append(f"===== FILE: {doc} =====\n" + t)
                        o = docx_outline(p) if doc.lower().endswith(".docx") else None
                        outline.append({"file": doc, "headings": o or txt_outline(t)})
            base = os.path.join(a.outdir, rel, tdoc)
            with open(base + ".txt", "w", encoding="utf-8") as f:
                f.write("\n\n".join(texts))
            with open(base + ".sections.json", "w", encoding="utf-8") as f:
                json.dump(outline, f, ensure_ascii=False, indent=1)
            n += 1
    print(f"extracted {n} tdocs -> {a.outdir}")


if __name__ == "__main__":
    main()
