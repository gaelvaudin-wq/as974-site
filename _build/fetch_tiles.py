"""Relit les fiches Ajax FR et en tire des tuiles chiffre + légende, sans reformuler."""
import json, re
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

UNIT = r"heures|heure|secondes|seconde|minutes|minute|ans|an|mètres|metres|px|Go|mm|km|m(?![a-zà-ÿ])|h(?![a-zà-ÿ])|s(?![a-zà-ÿ])|dB|W|V|°C|°"
MEASURE = re.compile(
    rf"(Jusqu['’]à\s+\d[\d\s]*(?:[.,]\d+)?\s*(?:{UNIT})"
    rf"|\d[\d\s]*(?:[.,]\d+)?\s*(?:à|-|–)\s*\d[\d\s]*(?:[.,]\d+)?\s*(?:{UNIT})"
    rf"|\d+\s*°\s*(?:à|-|–)\s*\d+\s*°"
    rf"|\d[\d\s]*\s*×\s*\d[\d\s]*\s*px"
    rf"|\bIP\s?\d{{2}}\b"
    rf"|\d+\s*(?:Mp|MP)\b"
    rf"|(?<![\d.,])\d+(?:[.,]\d+)?\s*(?:{UNIT}))",
    re.I)
BAD = re.compile(r"^(bureau|maison|entrepôt|commerce|café|salle|gym|musée)\b|détecté", re.I)

def text_of(n):
    if isinstance(n, str):
        return n
    if isinstance(n, list):
        return "".join(text_of(x) for x in n)
    if isinstance(n, dict):
        return text_of(n.get("children"))
    return ""

def clean(s):
    s = re.sub(r"[¹²³⁴⁵⁶⁷⁸⁹⁰]", "", s or "")
    s = s.replace("\xa0", " ").replace("&nbsp;", " ")
    s = re.sub(r"(heures|heure|secondes|seconde|ans|an|px|m)(\d)\b", r"\1", s, flags=re.I)
    s = re.sub(r"(?<=[A-Za-zÀ-ÿ]{4})\d\b", "", s)
    return re.sub(r"\s+", " ", s).strip(" .")

def legend_for(sentence, match):
    before = sentence[:match.start()].strip(" :,-–/")
    after = sentence[match.end():].strip(" :,-–/")
    after = re.sub(r"^[\d\s]+ft\b\s*(de\s+)?", "", after, flags=re.I).strip()
    if " et " in before:
        before = before.split(" et ")[-1].strip()
    seg = re.split(r"[,:]", before)[-1].strip()
    if 2 <= len(seg) <= 70 and not re.fullmatch(r"[\d\s.]+", seg):
        return seg
    if 2 <= len(after) <= 80 and not re.match(r"^[\d\s]+ft", after, re.I):
        return after
    if 2 <= len(before) <= 80:
        return before
    return ""

def add_fact(bucket, sentence, seen):
    sentence = clean(sentence)
    if not sentence or len(sentence) > 240 or BAD.search(sentence):
        return
    # « 9 groupes », « 3 réseaux … » : le chiffre ouvre la phrase.
    lead = re.match(r"^(\d+)\s+([A-Za-zÀ-ÿ].{2,80})$", sentence)
    if lead and "ft" not in lead.group(2).lower():
        key = lead.group(1) + "|" + lead.group(2)[:24].lower()
        if key not in seen:
            seen.add(key)
            bucket.append({"v": lead.group(1), "l": lead.group(2).strip()})
    for m in MEASURE.finditer(sentence):
        value = re.sub(r"\s+", " ", m.group(0)).strip()
        if len(value) > 32:
            continue
        # « 8 mm » découpé dans « 2,8 mm »
        if re.search(r"mm$", value, re.I) and re.search(r"\d[.,]\d+\s*mm", sentence, re.I):
            if value.lstrip("0") not in re.findall(r"\d+[.,]\d+\s*mm", sentence, re.I):
                full = re.search(r"\d+[.,]\d+\s*mm", sentence, re.I)
                if full and value.replace(" ", "") in full.group(0).replace(" ", "")[-len(value.replace(" ", "")):]:
                    continue
        legend = legend_for(sentence, m)
        legend = re.sub(r"(?<=[A-Za-zÀ-ÿ])\d+$", "", legend).strip()
        if not legend:
            continue
        key = value.lower() + "|" + legend.lower()[:24]
        if key in seen:
            continue
        if len(legend) < 4 or legend.endswith("(") or re.search(r"\(\s*$", legend):
            continue
        seen.add(key)
        bucket.append({"v": value, "l": legend})

def walk(node, texts, alts):
    if isinstance(node, dict):
        tag = node.get("tag") or ""
        props = node.get("props") or {}
        if tag in ("p", "h3", "li"):
            t = clean(text_of(node))
            cls = str(props.get("className") or "")
            if t and len(t) < 220:
                texts.append((tag, cls, t))
        alt = props.get("alt")
        if isinstance(alt, str):
            alts.append(clean(alt))
        for v in node.values():
            if isinstance(v, (dict, list)):
                walk(v, texts, alts)
    elif isinstance(node, list):
        for v in node:
            walk(v, texts, alts)

def variant_key(name):
    mp = re.search(r"(\d)\s*Mp", name, re.I)
    mm = re.search(r"(\d+(?:[.,]\d+)?)\s*mm", name, re.I)
    if mp and mm:
        return f"{mp.group(1)}mp-{mm.group(1).replace(',', '.')}"
    return ""

def parse(content):
    texts, alts = [], []
    walk(content, texts, alts)
    common, seen = [], set()
    variants = {}
    seq = [(cls, t) for tag, cls, t in texts if tag == "p"]
    i = 0
    while i < len(seq):
        cls, head = seq[i]
        if "fw-bold" in cls and i + 1 < len(seq) and "fw-bold" not in seq[i + 1][0]:
            cap = seq[i + 1][1]
            vk = variant_key(head)
            if vk:
                box = variants.setdefault(vk, [])
                local = set()
                add_fact(box, head, local)
                add_fact(box, cap, local)
            else:
                if re.fullmatch(r"Jusqu['’]à\s+\d[\d\s]*(?:[.,]\d+)?\s*(?:m|mètres|metres|heures|heure|ans|s|secondes)?|\d+", head, re.I):
                    follows = bool(re.match(r"^(de |d['’]|distance|portée|avec |pour |peut )", cap, re.I) or (cap[:1].islower()))
                    key = head.lower() + "|" + cap[:24].lower()
                    if follows and key not in seen and cap and not BAD.search(cap) and "(" not in cap:
                        seen.add(key)
                        common.append({"v": head, "l": cap[:110]})
                else:
                    add_fact(common, head, seen)
                    add_fact(common, cap, seen)
                    if "(" not in head and len(head) <= 70 and MEASURE.search(cap):
                        value = re.sub(r"\s+", " ", MEASURE.search(cap).group(0)).strip()
                        key = value.lower() + "|" + head[:24].lower()
                        if key not in seen:
                            seen.add(key)
                            common.append({"v": value, "l": head[:90]})
            i += 2
            continue
        i += 1
    for tag, cls, t in texts:
        if "fw-bold" in cls or tag == "h3":
            add_fact(common, t, seen)
    for alt in alts:
        add_fact(common, alt, seen)
    for tag, cls, t in texts:
        if re.search(r"jusqu['’]à|\bIP\d|×\s*\d", t, re.I):
            add_fact(common, t, seen)
    def usable(t):
        legend = t["l"]
        return "(" not in legend and not re.search(r"\b(bulletcam|turretcam|domecam|indoorcam)\b", legend, re.I)
    common = [t for t in common if usable(t)][:12]
    variants = {k: [t for t in v if usable(t)][:6] for k, v in variants.items()}
    variants = {k: v for k, v in variants.items() if v}
    return common, variants

def fetch(slug):
    try:
        html = urllib.request.urlopen(urllib.request.Request(
            f"https://ajax.systems/fr/products/{slug}/",
            headers={"User-Agent": "Mozilla/5.0"}), timeout=25).read().decode("utf-8", "replace")
    except Exception:
        return slug, {"tiles": [], "variants": {}}
    i = html.find("__NEXT_DATA__")
    if i < 0:
        return slug, {"tiles": [], "variants": {}}
    j = html.find(">", i)
    k = html.find("</script>", j)
    try:
        content = json.loads(html[j + 1:k])["props"]["pageProps"].get("content") or []
    except Exception:
        return slug, {"tiles": [], "variants": {}}
    common, variants = parse(content)
    return slug, {"tiles": common, "variants": variants}

def main():
    cat = json.loads(Path("_build/data/AS974-Ajax-catalogue-complet.json").read_text())
    slugs = sorted({p.get("official_page_slug") for p in cat if p.get("official_page_slug")})
    out = {}
    with ThreadPoolExecutor(max_workers=8) as ex:
        for fut in as_completed([ex.submit(fetch, s) for s in slugs]):
            slug, entry = fut.result()
            if entry["tiles"] or entry["variants"]:
                out[slug] = entry
    Path("_build/data/tiles-fr.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print("pages", len(out), "/", len(slugs))

if __name__ == "__main__":
    main()
