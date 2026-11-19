"""Tuiles de caractéristiques lues sur les fiches Ajax en français. Aucun chiffre ajouté."""
import json, os
from core import E, ROOT

_PATH = os.path.join(os.path.dirname(__file__), "data", "tiles-fr.json")
_TILES = None


def _load():
    global _TILES
    if _TILES is None:
        try:
            _TILES = json.load(open(_PATH, encoding="utf-8"))
        except OSError:
            _TILES = {}
    return _TILES


def _entry(slug):
    raw = _load().get(slug)
    if not raw:
        return [], {}
    if isinstance(raw, list):
        return raw, {}
    return raw.get("tiles") or [], raw.get("variants") or {}


def _variant_key(p):
    blob = f"{p.get('name','')} {p.get('slug','')}"
    mp = None
    import re
    mp = re.search(r"(\d)\s*Mp", blob, re.I)
    mm = re.search(r"(\d+(?:[.,]\d+)?)\s*mm", blob, re.I)
    if mp and mm:
        return f"{mp.group(1)}mp-{mm.group(1).replace(',', '.')}"
    return ""


def tiles_for(p):
    common, variants = _entry(p.get("official_page_slug") or "")
    chosen = list(variants.get(_variant_key(p)) or [])
    have = {t["v"].lower() for t in chosen}
    for t in common:
        if chosen and any(mark in t["v"] for mark in ("×", "°", "Mp", "MP", "mm")):
            continue
        if t["v"].lower() in have:
            continue
        chosen.append(t)
        have.add(t["v"].lower())
    return chosen[:8]


def system_html():
    """Chiffres repris tels quels des tuiles Hub Jeweller et MotionProtect."""
    data = _load()
    wanted = [
        ("hub", "Jusqu'à 2 000 m", "Hub Jeweller"),
        ("hub", "100", "Hub Jeweller"),
        ("hub", "Jusqu'à 15 heures", "Hub Jeweller"),
        ("hub", "50", "Hub Jeweller"),
        ("hub", "9", "Hub Jeweller"),
        ("motionprotect", "Jusqu'à 12 m", "MotionProtect"),
        ("motionprotect", "Jusqu'à 5 ans", "MotionProtect"),
        ("motionprotect", "Jusqu'à 1 700 m", "MotionProtect"),
    ]
    bits = []
    for slug, prefix, who in wanted:
        raw = data.get(slug) or []
        rows = raw if isinstance(raw, list) else (raw.get("tiles") or [])
        for t in rows:
            if t["v"] == prefix:
                bits.append(f'<li class="tile"><b>{E(t["v"])}</b><span>{E(t["l"])} · {E(who)}</span></li>')
                break
    if not bits:
        return ""
    return (f'<ul class="tiles" aria-label="Chiffres du système">{"".join(bits)}</ul>'
            f'<p class="src-note">Source : Ajax Systems</p>')


def tiles_html(p, limit=8, compact=False):
    items = tiles_for(p)[:limit]
    if not items:
        return ""
    bits = []
    for t in items:
        bits.append(f'<li class="tile"><b>{E(t["v"])}</b><span>{E(t["l"])}</span></li>')
    cls = "tiles is-compact" if compact else "tiles"
    return (f'<ul class="{cls}" aria-label="Caractéristiques officielles">{"".join(bits)}</ul>'
            f'<p class="src-note">Source : Ajax Systems</p>')
