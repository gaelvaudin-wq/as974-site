"""Noyau du générateur : configuration, données catalogue, images, gabarit HTML."""
import os, re, json, html, hashlib, unicodedata, datetime
from PIL import Image

BUILD = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(BUILD)
CFG = json.load(open(os.path.join(BUILD, "config.json"), encoding="utf-8"))
SITE = CFG["SITE_URL"].rstrip("/")

def resolve_path(p):
    """Chemin absolu, ou relatif à la racine du site / au dossier _build."""
    if not p:
        return p
    if os.path.isabs(p):
        return p
    for base in (ROOT, BUILD):
        cand = os.path.join(base, p)
        if os.path.exists(cand) or os.path.isdir(os.path.dirname(cand)):
            return cand
    return os.path.join(ROOT, p)
BRAND = CFG["brand"]
YEAR = datetime.date.today().year
E = html.escape

# ------------------------------------------------------------------ placeholders
def ph(label):
    """Ne jamais afficher de pastille. Les champs vides restent dans config.json."""
    return ""

def biz(key, label=None):
    v = CFG["business"].get(key)
    return E(v) if v else ""

def biz_txt(key, label=None):
    v = CFG["business"].get(key)
    return v if v else ""

def row(label, value):
    return f"<dt>{label}</dt><dd>{value}</dd>" if value else ""

def br_line(label, value):
    if not value:
        return ""
    return f"{label} : {value}<br>" if label else f"{value}<br>"

def telesurv():
    return "La télésurveillance peut compléter l’installation." if CFG.get("telesurveillance_confirmee") else ""

# ------------------------------------------------------------------ utilitaires
def slugify(s):
    s = unicodedata.normalize("NFD", s).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")

def norm(s):
    return unicodedata.normalize("NFD", s).encode("ascii", "ignore").decode().lower()

def lcfirst(s):
    return s[:1].lower() + s[1:] if s and not (len(s) > 1 and s[1].isupper()) else s

def clip(s, n=158):
    s = re.sub(r"\s+", " ", s).strip()
    return s if len(s) <= n else s[: n - 1].rsplit(" ", 1)[0].rstrip(",;:—-") + "…"

# ------------------------------------------------------------------ catalogue
GROUPS = [
    ("centrales", "Centrales & kits", "Le cœur du système : centrales, kits de démarrage et prolongateurs de portée.",
     ["Centrales", "Kits de démarrage", "Prolongateurs de portée"]),
    ("alarme", "Alarme intrusion", "Détecteurs, claviers, sirènes et commandes pour protéger chaque accès.",
     ["Détecteurs de mouvements", "Détecteurs d'ouverture", "Détecteurs de bris de glace", "Détecteurs sismiques", "Claviers", "Sirènes", "Boutons & télécommandes"]),
    ("incendie", "Incendie EN54", "Ligne professionnelle Ajax EN54 : centrale, détecteurs, déclencheurs, sirènes, flashs et modules pour les bâtiments.",
     ["Détecteurs d'incendie", "Dispositifs d'alarme incendie", "Déclencheurs manuels d'alarme"]),
    ("video", "Vidéosurveillance", "Caméras IP, enregistreurs, sonnette et interphonie reliés à l’alarme.",
     ["Caméras filaires", "Caméras Wi-Fi", "Enregistreurs vidéo", "Sonnettes", "Modules d'interphonie"]),
    ("domotique", "Domotique", "Éclairage, prises, relais, fuites d’eau et qualité de l’air dans la même application.",
     ["Interrupteurs d'éclairage", "Prises encastrées intelligentes", "Prises portables intelligentes", "Relais", "Vannes d'arrêt", "Détecteurs de fuites", "Détecteurs de qualité de l'air"]),
    ("accessoires", "Accessoires & intégration", "Modules d’intégration, alimentations, boîtiers et accessoires de pose.",
     ["Modules d'intégration", "Unités d'alimentation", "Boîtiers", "Accessoires", "Accessoires Fibra"]),
]
GROUP = {g[0]: {"key": g[0], "label": g[1], "intro": g[2], "cats": g[3]} for g in GROUPS}
CAT2GROUP = {c: g[0] for g in GROUPS for c in g[3]}

GAMME_KEY = {"Baseline": "baseline", "Superior": "superior", "Residence Line": "residence", "EN54 Line": "en54", "Type4 Line": "type4", "À confirmer": "a-confirmer"}
GAMME_LABEL = {"baseline": "Baseline", "superior": "Superior", "residence": "Residence Line", "en54": "EN54 Line", "type4": "Type4 Line", "a-confirmer": "Gamme à confirmer"}

COLOR_HEX = {  # teintes indicatives (RAL fabricant quand connu)
    "Noir": "#0E0E10", "Blanc": "#F7F7F7", "Graphite": "#474A51", "Gris": "#969992", "Ivoire": "#EAE6CA",
    "Fumée": "#D0D0D0", "Huître": "#E7EBDA", "Olive": "#B7B3A8", "Rouge": "#D0201A", "Bleu": "#1F5FAF",
    "Vert": "#2E7D4F", "Jaune": "#F2C200",
}
NOTE_PAT = re.compile(r"site Ajax France|Fiche officielle publique|Bientôt disponible", re.I)

def tag_gamme(gk):
    cls = {"baseline": "tag-base", "superior": "tag-sup", "a-confirmer": "tag-tbc"}.get(gk, "tag-line")
    if gk == "a-confirmer":
        return ""
    return f'<span class="tag {cls}">{E(GAMME_LABEL[gk])}</span>'

def avail_info(p):
    st = p["availability_status"]
    if st == "indisponible-region-france":
        return ("Disponibilité à confirmer", "Cette référence n’est pas proposée sur le site Ajax France à ce jour. Sa disponibilité à La Réunion sera confirmée lors de l’étude de votre devis.")
    if st == "bientot-disponible":
        return ("Bientôt disponible", "Annoncée prochainement par le fabricant. Commercialisation et disponibilité à La Réunion à confirmer lors du devis.")
    if p["catalogue_scope"] == "fiche-sitemap-hors-index":
        return (None, "Référence présente sur le site du fabricant hors catalogue principal : disponibilité à confirmer lors du devis.")
    return (None, None)

def load_catalogue():
    data = json.load(open(resolve_path(CFG["catalogue_json"]), encoding="utf-8"))
    names = {}
    for p in data:
        names[p["name"]] = names.get(p["name"], 0) + 1
    out = []
    for p in data:
        p = dict(p)
        p["group"] = CAT2GROUP[p["category"]]
        p["gk"] = GAMME_KEY.get(p["gamme"], "a-confirmer")
        # Incendie : la page dédiée est la ligne EN54. Les FireProtect grand public
        # (Residence Line) complètent l'alarme Baseline. Source : catalogues Ajax.
        fire_cats = {"Détecteurs d'incendie", "Dispositifs d'alarme incendie", "Déclencheurs manuels d'alarme"}
        slug = str(p["slug"])
        if p["gamme"] == "EN54 Line" or slug.startswith("en54-"):
            p["group"] = "incendie"
        elif slug.startswith("manualcallpoint-"):
            # Ajax les présente sur la page EN54. Seule la version rouge est certifiée EN 54-25.
            p["group"] = "incendie"
        elif p["gamme"] == "Type4 Line" or slug.startswith("type4-"):
            # Ligne distincte, pas EN 54 : hors du catalogue Incendie.
            if p["category"] in ("Centrales", "Prolongateurs de portée", "Kits de démarrage"):
                p["group"] = "centrales"
            else:
                p["group"] = "accessoires"
        elif p["gamme"] == "Residence Line" and p["category"] in fire_cats:
            p["group"] = "alarme"
        feats = [f.strip().rstrip(".") for f in (p["feature_1"], p["feature_2"], p["feature_3"]) if f and f.strip() and not NOTE_PAT.search(f)]
        p["feats"] = feats
        p["colors_ok"] = [c for c in p["colors_available"] if c in p["color_images"]]
        p["dup_name"] = names[p["name"]] > 1
        p["title_name"] = f'{p["name"]} ({p["model"]})' if p["dup_name"] else p["name"]
        # Accroche et bénéfices propres à la référence (pas de phrase répétée).
        p["hook"] = feats[0] if feats else p["category"]
        seen, benefits = set(), []
        for f in feats:
            key = norm(f)
            if key in seen:
                continue
            seen.add(key)
            benefits.append(f)
            if len(benefits) == 3:
                break
        p["benefits"] = benefits
        d = p["hook"].rstrip(".") + "."
        extra = [b for b in benefits[1:]]
        if extra:
            d += " " + " ".join(x.rstrip(".") + "." for x in extra)
        p["desc"] = d
        p["avail_tag"], p["avail_note"] = avail_info(p)
        out.append(p)
    return out

# ------------------------------------------------------------------ images
IMG_OUT = os.path.join(ROOT, "assets", "img", "p")
STAGE = (245, 245, 247)
IMG_REV = 4
_img_cache = {}

def _process(src_rel):
    """Recadre au produit, ne jamais agrandir ; WebP (2 tailles max) + PNG/JPG de repli."""
    if src_rel in _img_cache:
        return _img_cache[src_rel]
    src = os.path.join(resolve_path(CFG["catalogue_images_dir"]), src_rel)
    stem = ("c-" if "/couleurs/" in src_rel else "") + slugify(os.path.splitext(os.path.basename(src_rel))[0])
    meta_path = os.path.join(IMG_OUT, stem + ".json")
    def load_meta():
        try:
            return json.load(open(meta_path, encoding="utf-8"))
        except Exception:
            return None
    cached = load_meta() if os.path.exists(meta_path) else None
    source_ok = os.path.exists(src)
    if cached and cached.get("rev") == IMG_REV and (not source_ok or os.path.getmtime(meta_path) >= os.path.getmtime(src)):
        _img_cache[src_rel] = cached
        return cached
    if not source_ok:
        _img_cache[src_rel] = cached
        return cached
    os.makedirs(IMG_OUT, exist_ok=True)
    im = Image.open(src)
    im = im.convert("RGBA")
    alpha = im.split()[3]
    has_alpha = alpha.getextrema()[0] < 250
    if has_alpha:
        bbox = alpha.point(lambda a: 255 if a > 8 else 0).getbbox()
        opaque = False
    else:
        rgb = im.convert("RGB")
        # fond blanc : bbox des pixels non quasi-blancs
        mask = rgb.convert("L").point(lambda v: 255 if v < 246 else 0)
        bbox = mask.getbbox()
        opaque = True
    if bbox:
        w0, h0 = im.size
        pad = int(max(bbox[2] - bbox[0], bbox[3] - bbox[1]) * 0.04)
        bbox = (max(0, bbox[0] - pad), max(0, bbox[1] - pad), min(w0, bbox[2] + pad), min(h0, bbox[3] + pad))
        im = im.crop(bbox)
    W, H = im.size
    # 700 cartes, 1000 fiches, 1600 hero — jamais d’agrandissement.
    widths = sorted({w for w in (700, 1000, 1600) if w < W} | {W})
    srcset = []
    for w in widths:
        h = round(H * w / W)
        r = im if w == W else im.resize((w, h), Image.LANCZOS)
        fn = f"{stem}-{w}.webp"
        r.save(os.path.join(IMG_OUT, fn), "WEBP", quality=82, method=2)
        srcset.append((fn, w))
    fw = min(W, 1000); fh = round(H * fw / W)
    fb = im if fw == W else im.resize((fw, fh), Image.LANCZOS)
    fb_name = f"{stem}.png"
    out_img = fb if not opaque else fb.convert("RGBA")
    out_img.save(os.path.join(IMG_OUT, fb_name), "PNG", optimize=True)
    meta = {"rev": IMG_REV, "w": W, "h": H, "fw": fw, "fh": fh, "srcset": srcset, "fallback": fb_name, "opaque": opaque, "src": src_rel}
    json.dump(meta, open(meta_path, "w"))
    _img_cache[src_rel] = meta
    return meta

def product_images(p):
    """dict couleur -> meta ; clé '' = image par défaut."""
    res = {}
    for c in p["colors_ok"]:
        meta = _process(p["color_images"][c])
        if meta:
            res[c] = meta
    if p["image_path"]:
        meta = _process(p["image_path"])
        if meta:
            res[""] = meta
    elif res:
        res[""] = res.get(p["default_color"]) or next(iter(res.values()))
    return res

def default_image(p):
    ims = product_images(p)
    if p["default_color"] and p["default_color"] in ims:
        return ims[p["default_color"]]
    return ims.get("")

def color_image(p, color):
    ims = product_images(p)
    return ims.get(color) or default_image(p)

def img_urls(meta, pre):
    base = pre + "assets/img/p/"
    return (", ".join(f"{base}{fn} {w}w" for fn, w in meta["srcset"]), base + meta["fallback"])

def picture(meta, alt, pre, sizes, cls="", eager=False, idimg=None, idsrc=None):
    if not meta:
        return ('<div class="prod-noimg" role="img" aria-label="Visuel non disponible">'
                '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><rect x="3" y="4" width="18" height="16" rx="3"/><path d="M3 16l5-5 4 4 3-3 6 6"/><circle cx="15.5" cy="8.5" r="1.5"/></svg>'
                'Visuel officiel non disponible</div>')
    ss, fb = img_urls(meta, pre)
    load = 'fetchpriority="high"' if eager else 'loading="lazy"'
    ia = f' id="{idimg}"' if idimg else ""
    sa = f' id="{idsrc}"' if idsrc else ""
    matte = " is-matte" if meta.get("opaque") else ""
    c = f' class="{(cls + matte).strip()}"' if (cls or matte) else ""
    widest = max((w for _fn, w in meta.get("srcset") or []), default=meta["w"])
    return (f'<picture><source{sa} type="image/webp" srcset="{ss}" sizes="{sizes}">'
            f'<img{ia}{c} src="{fb}" alt="{E(alt)}" width="{meta["w"]}" height="{meta["h"]}" style="--w:{widest}px" {load} decoding="async"></picture>')

def abs_img(meta):
    return f"{SITE}/assets/img/p/{meta['fallback']}" if meta else f"{SITE}/assets/img/og-as974.jpg"
