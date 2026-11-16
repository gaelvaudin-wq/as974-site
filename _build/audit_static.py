"""Audit statique : liens ajax, mots visibles, images, schémas, vidéos."""
import os, re, json, glob
from html.parser import HTMLParser

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class Visible(HTMLParser):
    def __init__(self):
        super().__init__()
        self.skip = 0
        self.ignore = 0
        self.parts = []
        self.ajax = 0
        self.imgs = 0
        self.svgs = 0
        self.videos = 0
        self.sections = []
        self._sec = None
        self._in_details = 0
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "details":
            self._in_details += 1
        if tag in ("script", "style", "header", "footer", "nav", "table", "article"):
            self.skip += 1
            self.ignore += 1 if tag in ("header", "footer", "nav", "table", "article") else 0
        if tag == "a":
            href = a.get("href") or ""
            if "ajax.systems" in href or "ajaxsystems.fr" in href:
                self.ajax += 1
        if tag == "img":
            self.imgs += 1
        if tag == "svg":
            self.svgs += 1
        if tag == "video" or (tag == "figure" and "data-yt" in a):
            self.videos += 1
        if tag == "section":
            self._sec = {"words": 0, "visual": 0, "cls": a.get("class", "")}
        if self._sec is not None and self._in_details == 0 and tag in ("img", "svg", "video", "table", "figure"):
            self._sec["visual"] += 1
    def handle_endtag(self, tag):
        if tag == "details" and self._in_details:
            self._in_details -= 1
        if tag in ("script", "style", "header", "footer", "nav", "table", "article") and self.skip:
            self.skip -= 1
        if tag == "section" and self._sec is not None:
            self.sections.append(self._sec)
            self._sec = None
    def handle_data(self, data):
        if self.skip or self._in_details:
            return
        text = data.strip()
        if not text:
            return
        self.parts.append(text)
        if self._sec is not None:
            self._sec["words"] += len(text.split())

def audit_file(path):
    raw = open(path, encoding="utf-8").read()
    p = Visible()
    p.feed(raw)
    long = [s for s in p.sections if "cta" not in s["cls"] and s["words"] > 80]
    bare = [s for s in p.sections if "cta" not in s["cls"] and "hero-film" not in s["cls"] and s["visual"] == 0 and s["words"] > 12]
    return {
        "ajax": p.ajax,
        "words": len(" ".join(p.parts).split()),
        "imgs": p.imgs,
        "svgs": p.svgs,
        "videos": p.videos,
        "long": len(long),
        "bare": len(bare),
    }

def main():
    files = sorted(glob.glob(os.path.join(ROOT, "*.html")) + glob.glob(os.path.join(ROOT, "produits", "*.html")))
    rows = {}
    for f in files:
        rel = os.path.relpath(f, ROOT)
        rows[rel] = audit_file(f)
    tot = {k: sum(r[k] for r in rows.values()) for k in ("ajax", "words", "imgs", "svgs", "videos", "long", "bare")}
    bad = {k: v for k, v in rows.items() if v["ajax"] or v["long"] or v["bare"]}
    out = {"pages": len(rows), "totals": tot, "defects": len(bad), "worst": sorted(bad.items(), key=lambda kv: -(kv[1]["long"]+kv[1]["bare"]+kv[1]["ajax"]))[:25]}
    print(json.dumps(out, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
