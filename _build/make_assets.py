#!/usr/bin/env python3
"""Génère les logos SVG vectorisés (texte -> tracés, rendu identique partout),
le favicon et la police Inter sous-ensemble (woff2). Relançable.
Source logos : /workspace/as974-logos/svg (piste B noir + trait rouge)."""
import os, re, sys
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools import subset

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONT = "/usr/share/fonts/truetype/sand-box/google/Inter/Inter-VariableFont_opsz,wght.ttf"
OUT_LOGO = os.path.join(ROOT, "assets/img/logo")
OUT_FONT = os.path.join(ROOT, "assets/fonts")
os.makedirs(OUT_LOGO, exist_ok=True); os.makedirs(OUT_FONT, exist_ok=True)

_cache = {}
def font(wght):
    if wght not in _cache:
        f = TTFont(FONT)
        _cache[wght] = instancer.instantiateVariableFont(f, {"wght": wght, "opsz": 32})
    return _cache[wght]

def text_path(txt, x, y, size, wght, spacing=0, anchor="start"):
    f = font(wght); gs = f.getGlyphSet(); cmap = f.getBestCmap(); upm = f["head"].unitsPerEm
    sc = size / upm
    names = [cmap[ord(c)] for c in txt]
    adv = [f["hmtx"][n][0] * sc for n in names]
    width = sum(adv) + spacing * (len(txt) - 1)
    if anchor == "middle": x -= width / 2
    d = []; cx = x
    for n, a in zip(names, adv):
        pen = SVGPathPen(gs)
        gs[n].draw(TransformPen(pen, (sc, 0, 0, -sc, cx, y)))
        d.append(pen.getCommands()); cx += a + spacing
    return " ".join(d), x, width

def logo_horizontal(color, title):
    s974, sx, sw = text_path("S974", 168, 138, 110, 700, -4)
    # largeur du S pour le trait rouge
    _, _, s_w = text_path("S", 168, 138, 110, 700)
    sub, _, _ = text_path("ACTIVE SÉCURITÉ 974", 360, 190, 20, 500, 6, "middle")
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 720 220" width="720" height="220" role="img" aria-label="{title}">
<title>{title}</title>
<path fill="{color}" d="M48 148 L108 28 L168 148 H138 L108 82 L78 148 Z"/>
<path fill="{color}" d="{s974}"/>
<rect x="{sx+2:.1f}" y="148" width="{s_w-4:.1f}" height="10" rx="2" fill="#E10600"/>
<path fill="{color}" d="{sub}"/>
</svg>
'''

def logo_compact(color):
    s, _, _ = text_path("S", 210, 150, 110, 700, 0, "middle")
    n, _, _ = text_path("974", 160, 250, 96, 700, -2, "middle")
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 280" width="320" height="280" role="img" aria-label="AS974">
<title>AS974</title>
<path fill="{color}" transform="translate(40,20)" d="M48 148 L108 28 L168 148 H138 L108 82 L78 148 Z"/>
<path fill="{color}" d="{s}"/>
<rect x="178" y="158" width="64" height="10" rx="2" fill="#E10600"/>
<path fill="{color}" d="{n}"/>
</svg>
'''

def favicon():
    # Sigle : A (tracé d'origine) + trait rouge, sur carré noir arrondi
    return '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">
<rect width="64" height="64" rx="14" fill="#0B0B0C"/>
<path fill="#FFFFFF" transform="translate(-6.5,-2) scale(.32)" d="M48 148 L108 28 L168 148 H138 L108 82 L78 148 Z"/>
<rect x="16" y="48" width="32" height="5" rx="1.5" fill="#E10600"/>
</svg>
'''

open(os.path.join(OUT_LOGO, "as974-horizontal-noir-rouge.svg"), "w").write(logo_horizontal("#0B0B0C", "Active Sécurité 974"))
open(os.path.join(OUT_LOGO, "as974-horizontal-blanc-rouge.svg"), "w").write(logo_horizontal("#FFFFFF", "Active Sécurité 974"))
open(os.path.join(OUT_LOGO, "as974-compact-noir-rouge.svg"), "w").write(logo_compact("#0B0B0C"))
open(os.path.join(ROOT, "favicon.svg"), "w").write(favicon())

# Police Inter : sous-ensemble latin, variable (wght), woff2
opts = subset.Options(); opts.flavor = "woff2"; opts.layout_features = ["kern", "liga", "calt", "tnum"]
f = TTFont(FONT)
unicodes = list(range(0x20, 0x7F)) + list(range(0xA0, 0x180)) + [0x2013,0x2014,0x2018,0x2019,0x201C,0x201D,0x2022,0x2026,0x20AC,0x2192,0x2190,0x2713,0x00B7,0x202F,0x2009]
sub = subset.Subsetter(opts); sub.populate(unicodes=unicodes); sub.subset(f)
f = instancer.instantiateVariableFont(f, {"opsz": 32, "wght": (400, 800)})
f.flavor = "woff2"; f.save(os.path.join(OUT_FONT, "inter-latin-var.woff2"))
print("logos + favicon + police OK")
