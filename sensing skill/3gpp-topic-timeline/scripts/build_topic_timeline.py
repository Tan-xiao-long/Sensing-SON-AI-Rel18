#!/usr/bin/env python3
"""Regroup parsed chairs-notes records by TOPIC (across meetings, in time order).

Input : records.json (from parse_chair_notes.py), topics.json
Output: topic_timeline.json
  {topic_key: {"title":…, "timeline": [
      {"meeting":…, "date":…, "subsection":…,
       "agreements_new": [...], "tdocs": [...], "cb_results": [...]}]},
   "_unassigned": [...] }

topics.json format (see references/topics.example.json):
{
  "topics": [{
     "key": "MRO",
     "title": "移动鲁棒性优化 (MRO)",
     "subsection_patterns": ["MRO"],            # regex on subsection heading
     "keyword_patterns": ["\\bMRO\\b", "CPAC"]  # regex on tdoc title / CB desc
  }],
  "section_labels": ["SON", "AI"]               # which parsed sections to use
}
Subsection match wins over keyword match. Keyword match is the fallback for
mixed sections (e.g. Rel-XX corrections agendas).
"""
import argparse
import json
import re


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--records", required=True)
    ap.add_argument("--topics", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    records = json.load(open(a.records, encoding="utf-8"))
    spec = json.load(open(a.topics, encoding="utf-8"))
    topics = spec["topics"]
    labels = set(spec.get("section_labels") or [])
    for t in topics:
        t["_sub_re"] = [re.compile(p) for p in t.get("subsection_patterns", [])]
        t["_kw_re"] = [re.compile(p) for p in t.get("keyword_patterns", [])]

    out = {t["key"]: {"title": t["title"], "timeline": []} for t in topics}
    unassigned = []

    def match_topic(subheading, text):
        for t in topics:
            if any(r.search(subheading) for r in t["_sub_re"]):
                return t["key"], "subsection"
        for t in topics:
            if any(r.search(text) for r in t["_kw_re"]):
                return t["key"], "keyword"
        return None, None

    # meetings assumed already in chronological order in records.json
    for mtg, mrec in records.items():
        for label, sec in mrec.get("sections", {}).items():
            if labels and label not in labels:
                continue
            for sub, data in sec["subsections"].items():
                bucket = {}  # topic -> collected
                # whole-subsection assignment first
                key, how = match_topic(sub, "")
                for td in data["tdocs"]:
                    k = key
                    if k is None:
                        k, _ = match_topic("", td["title"] + " " + " ".join(td["comments"][:3]))
                    if k is None:
                        unassigned.append({"meeting": mtg, "subsection": sub, "tdoc": td["tdoc"],
                                           "title": td["title"], "decision": td["decision"]})
                        continue
                    bucket.setdefault(k, {"tdocs": [], "cb_results": []})["tdocs"].append(td)
                for cb in data["cb_results"]:
                    k = key
                    if k is None:
                        k, _ = match_topic("", cb["desc"])
                    if k is None:
                        unassigned.append({"meeting": mtg, "subsection": sub, "tdoc": cb["final"],
                                           "title": cb["desc"], "decision": cb["decision"]})
                        continue
                    bucket.setdefault(k, {"tdocs": [], "cb_results": []})["cb_results"].append(cb)
                for k, got in bucket.items():
                    out[k]["timeline"].append({
                        "meeting": mtg, "date": mrec.get("date", ""), "section": label,
                        "subsection": sub,
                        "agreements_new": data["agreements_new"] if key == k else [],
                        "tdocs": got["tdocs"], "cb_results": got["cb_results"],
                    })
                # subsection matched but zero tdocs (agreements only)
                if key is not None and key not in bucket and (data["agreements_new"] or data["cb_results"]):
                    out[key]["timeline"].append({
                        "meeting": mtg, "date": mrec.get("date", ""), "section": label,
                        "subsection": sub, "agreements_new": data["agreements_new"],
                        "tdocs": [], "cb_results": data["cb_results"],
                    })

    result = dict(out)
    result["_unassigned"] = unassigned
    with open(a.out, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=1)
    for k, v in out.items():
        n = sum(len(e["tdocs"]) for e in v["timeline"])
        print(f"{k}: {len(v['timeline'])} meeting-entries, {n} tdocs")
    print(f"unassigned: {len(unassigned)}  -> {a.out}")


if __name__ == "__main__":
    main()
