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


def tiles_for(p):
    slug = p.get("official_page_slug") or ""
    return list(_load().get(slug) or [])


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
        for t in data.get(slug) or []:
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
