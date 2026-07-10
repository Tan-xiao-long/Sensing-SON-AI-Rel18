#!/usr/bin/env python3
"""Download TDoc zips referenced in records.json from the 3GPP FTP (HTTP).

For each tdoc the URL tried is  <ftp_dir>/Docs/<TDOC>.zip  then
<ftp_dir>/Inbox/<TDOC>.zip  (in-meeting revisions usually live in Inbox).
Rate-limited and resumable (existing non-empty files are skipped).

Examples:
  python download_tdocs.py --records work/records.json --meetings meetings.json \
      --out work/tdocs --delay 2.0 --only-decisions agreed,endorsed --finals-only
"""
import argparse
import json
import os
import random
import sys
import time

try:
    import requests
except ImportError:
    print("pip install requests", file=sys.stderr)
    sys.exit(1)

UA = "Mozilla/5.0 (compatible; 3gpp-topic-timeline/1.0)"


def iter_tdocs(records, only_decisions, finals_only):
    for mtg, mrec in records.items():
        for sec in mrec.get("sections", {}).values():
            for data in sec["subsections"].values():
                for td in data["tdocs"]:
                    dec = td["decision"].split()[0] if td["decision"] else ""
                    if only_decisions and dec not in only_decisions:
                        continue
                    yield mtg, td["final"]
                    if not finals_only and td["origin"] not in ("(CB)", td["final"]):
                        yield mtg, td["origin"]
                for cb in data["cb_results"]:
                    dec = cb["decision"].split()[0] if cb["decision"] else ""
                    if only_decisions and dec not in only_decisions:
                        continue
                    yield mtg, cb["final"]


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--records", required=True)
    ap.add_argument("--meetings", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--delay", type=float, default=2.0,
                    help="base seconds between requests (jitter added); keep >= 1.5")
    ap.add_argument("--only-decisions", default="",
                    help="comma list, e.g. agreed,endorsed ; empty = all")
    ap.add_argument("--finals-only", action="store_true",
                    help="download only the final (post-revision) version of each tdoc")
    a = ap.parse_args()

    records = json.load(open(a.records, encoding="utf-8"))
    meetings = {m["meeting"]: m for m in json.load(open(a.meetings, encoding="utf-8"))}
    only = set(x.strip() for x in a.only_decisions.split(",") if x.strip())

    todo = {}
    for mtg, tdoc in iter_tdocs(records, only, a.finals_only):
        todo.setdefault(mtg, set()).add(tdoc)

    sess = requests.Session()
    sess.headers["User-Agent"] = UA
    ok = fail = skip = 0
    for mtg, tdocs in todo.items():
        base = meetings.get(mtg, {}).get("ftp_dir", "").rstrip("/")
        if not base:
            print(f"[WARN] no ftp_dir for {mtg}; skipping {len(tdocs)} tdocs", file=sys.stderr)
            continue
        outdir = os.path.join(a.out, mtg.replace("#", "_").replace("/", "_"))
        os.makedirs(outdir, exist_ok=True)
        for tdoc in sorted(tdocs):
            dst = os.path.join(outdir, tdoc + ".zip")
            if os.path.exists(dst) and os.path.getsize(dst) > 0:
                skip += 1
                continue
            got = False
            for sub in ("Docs", "Inbox"):
                url = f"{base}/{sub}/{tdoc}.zip"
                try:
                    r = sess.get(url, timeout=60)
                    if r.status_code == 200 and r.content[:2] == b"PK":
                        with open(dst, "wb") as f:
                            f.write(r.content)
                        print(f"  {tdoc} <- {sub} ({len(r.content)} B)")
                        got = True
                        break
                except Exception as ex:
                    print(f"  {tdoc}: {ex}", file=sys.stderr)
                time.sleep(a.delay / 2)
            if got:
                ok += 1
            else:
                fail += 1
                print(f"  {tdoc}: NOT FOUND in Docs/ or Inbox/ of {mtg}", file=sys.stderr)
            time.sleep(a.delay + random.random() * a.delay / 2)
    print(f"downloaded {ok}, skipped(existing) {skip}, failed {fail}")


if __name__ == "__main__":
    main()
