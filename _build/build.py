#!/usr/bin/env python3
"""Générateur du site statique Active Sécurité 974.
Usage : python3 _build/build.py   (depuis la racine du site ou n'importe où)
- régénère toutes les pages, les 288 fiches produit, sitemap.xml, robots.txt, images optimisées (cache).
Dépendances : voir requirements.txt (Pillow). Les logos/police : _build/make_assets.py (une fois)."""
import os, sys, glob, shutil
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from core import *
from core import _process, resolve_path
import layout, pages, products
from PIL import Image, ImageDraw, ImageFont

def og_image():
    out = os.path.join(ROOT, "assets/img/og-as974.jpg")
    rel = pages.P["hub-2"]["color_images"].get("Blanc") or pages.P["hub-2"].get("image_path")
    src = os.path.join(resolve_path(CFG["catalogue_images_dir"]), rel) if rel else ""
    if not (src and os.path.exists(src)) and os.path.exists(out):
        print("Image Open Graph conservée (packshots sources absents, cache déjà en place).")
        return
    W, H = 1200, 630
    im = Image.new("RGB", (W, H), (11, 11, 12))
    glow = Image.new("RGB", (W, H), (0, 0, 0))
    d = ImageDraw.Draw(glow)
    for r in range(420, 0, -6):
        a = int(70 * (1 - r / 420))
        d.ellipse((860 - r, 420 - r, 860 + r, 420 + r), fill=(a, 0, 0))
    from PIL import ImageChops
    im = ImageChops.add(im, glow)
    font = "/usr/share/fonts/truetype/sand-box/google/Inter/Inter-VariableFont_opsz,wght.ttf"
    if not os.path.exists(font):
        font = "/usr/share/fonts/truetype/macos/Inter-Bold.ttf"
    def F(sz, w):
        f = ImageFont.truetype(font, sz)
        try: f.set_variation_by_axes([32, w])
        except Exception: pass
        return f
    dr = ImageDraw.Draw(im)
    dr.text((72, 150), "Active Sécurité 974", font=F(64, 750), fill="white")
    dr.rectangle((72, 236, 172, 244), fill=(225, 6, 0))
    dr.text((72, 280), "Alarme · Incendie · Vidéo · Domotique", font=F(34, 500), fill=(200, 200, 205))
    dr.text((72, 330), "Partenaire agréé Ajax Systems — La Réunion", font=F(30, 500), fill=(160, 160, 165))
    if src and os.path.exists(src):
        p = Image.open(src).convert("RGBA"); p = p.crop(p.split()[3].getbbox()); p.thumbnail((380, 380))
        im.paste(p, (780, 125), p)
    elif os.path.exists(out):
        return
    im.save(out, "JPEG", quality=86, optimize=True, progressive=True)

def favicons():
    """Recadrage du logo compact officiel, sans redessin."""
    src = os.path.join(ROOT, "assets/img/logo/as974-b-compact-noir-rouge.png")
    im = Image.open(src).convert("RGBA")
    for size, name in ((32, "favicon-32.png"), (180, "apple-touch-icon.png"), (512, "icon-512.png")):
        im.resize((size, size), Image.LANCZOS).save(os.path.join(ROOT, name))
    # le svg dessiné n'est plus la source : le navigateur utilise les PNG officiels
    open(os.path.join(ROOT, "favicon.svg"), "w").write(
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32"><image href="favicon-32.png" width="32" height="32"/></svg>\n')

def sitemap():
    today = datetime.date.today().isoformat()
    urls = []
    for path, prio in layout.PAGES:
        loc = SITE + "/" + ("" if path == "index.html" else path)
        urls.append(f"<url><loc>{E(loc)}</loc><lastmod>{today}</lastmod><priority>{prio}</priority></url>")
    open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8").write(
        '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "\n".join(urls) + "\n</urlset>\n")
    from urllib.parse import urlparse
    import re as _re
    base_path = urlparse(SITE).path.rstrip("/")
    bots = "\n".join(
        f"User-agent: {b}\nAllow: /\n" for b in
        ("GPTBot", "ChatGPT-User", "ClaudeBot", "anthropic-ai", "PerplexityBot", "Google-Extended", "Applebot-Extended", "CCBot")
    )
    open(os.path.join(ROOT, "robots.txt"), "w").write(
        bots + f"\nUser-agent: *\nAllow: /\nDisallow: {base_path}/merci.html\n\nSitemap: {SITE}/sitemap.xml\n")
    # sitemap images
    img_ns = ' xmlns:image="http://www.google.com/schemas/sitemap-image/1.1"'
    body_urls = []
    today = datetime.date.today().isoformat()
    for path, prio in layout.PAGES:
        loc = SITE + "/" + ("" if path == "index.html" else path)
        html = open(os.path.join(ROOT, path), encoding="utf-8").read()
        imgs = []
        tags = _re.findall(r'<img\b[^>]*>', html)[:8]
        for tag in tags:
            src_m = _re.search(r'src="([^"]+)"', tag)
            alt_m = _re.search(r'alt="([^"]*)"', tag)
            if not src_m:
                continue
            src, alt = src_m.group(1), alt_m.group(1) if alt_m else ""
            if src.startswith("data:"):
                continue
            absu = src if src.startswith("http") else SITE + "/" + src.lstrip("./").replace("../", "")
            if "assets/" in src or src.startswith("http"):
                # resolve relative
                if not src.startswith("http"):
                    depth = path.count("/")
                    base = "/".join([""] + path.split("/")[:-1]) if depth else ""
                    # simpler: urljoin
                    from urllib.parse import urljoin
                    absu = urljoin(loc if loc.endswith("/") else loc.rsplit("/", 1)[0] + "/", src)
                imgs.append(f'<image:image><image:loc>{E(absu)}</image:loc><image:title>{E(alt or BRAND)}</image:title></image:image>')
        body_urls.append(f"<url><loc>{E(loc)}</loc><lastmod>{today}</lastmod><priority>{prio}</priority>{''.join(imgs)}</url>")
    open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8").write(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        f'<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"{img_ns}>\n'
        + "\n".join(body_urls) + "\n</urlset>\n")
    llms = f"""# Active Sécurité 974 (AS974)
Installateur partenaire agréé Ajax Systems. Interventions chez le client sur toute l’île de La Réunion (Saint-Denis, Saint-Pierre, Saint-Paul, Le Port, Saint-Benoît et les Hauts). Pas de local ouvert au public. Devis uniquement, pas de vente en ligne.

Site : {SITE}/

## Pages
- Accueil : {SITE}/
- Particuliers : {SITE}/particuliers.html
- Professionnels : {SITE}/professionnels.html
- Vidéosurveillance Baseline et Superior : {SITE}/gamme-video.html
- Incendie professionnel EN54 : {SITE}/gamme-incendie.html
- Alarme (FireProtect logement en complément) : {SITE}/gamme-alarme.html
- Domotique : {SITE}/gamme-domotique.html
- Services : {SITE}/services.html
- Catalogue : {SITE}/catalogue.html
- FAQ : {SITE}/faq.html
- Contact : {SITE}/contact.html

## À retenir
Les lignes vidéo Baseline et Superior reconnaissent toutes deux personnes, véhicules et animaux, et peuvent déclencher l’alarme. Superior ajoute une IA enrichie, des optiques P-Iris et les NVR H2D.
Les FireProtect, FireProtect Plus et FireProtect 2 complètent une alarme de logement (page Alarme). Ils n’ont pas de page incendie. La page Incendie est uniquement la ligne professionnelle EN54.
Coordonnées légales non publiées tant qu’elles ne sont pas renseignées.
"""
    open(os.path.join(ROOT, "llms.txt"), "w", encoding="utf-8").write(llms)
    open(os.path.join(ROOT, "llms-full.txt"), "w", encoding="utf-8").write(llms + "\n## Références\n" + "\n".join(
        f"- {p['name']} ({p['gamme']}, {p['category']}) : {SITE}/produits/{p['slug']}.html" for p in pages.ALL
    ) + "\n")

def prune_images():
    used = set()
    folder = os.path.join(ROOT, "assets", "img", "p")
    for meta_path in glob.glob(os.path.join(folder, "*.json")):
        meta = json.load(open(meta_path, encoding="utf-8"))
        used.add(os.path.basename(meta_path))
        used.add(meta.get("fallback") or "")
        for fn, _w in meta.get("srcset") or []:
            used.add(fn)
    for path in glob.glob(os.path.join(folder, "*")):
        if os.path.basename(path) not in used:
            os.remove(path)

def assert_public_copy():
    banned = ("[À COMPLÉTER", "[À CONFIRMER", "Ma Protection IA", "Pas de tarifs inventés", "conformité non vérifiée", "conformité réglementaire non vérifiée")
    bad = []
    for path in glob.glob(os.path.join(ROOT, "*.html")) + glob.glob(os.path.join(ROOT, "produits", "*.html")):
        text = open(path, encoding="utf-8").read()
        for token in banned:
            if token in text:
                bad.append(f"{os.path.relpath(path, ROOT)} : {token}")
                break
    if bad:
        raise SystemExit("Textes internes visibles :\n" + "\n".join(bad[:30]))

def main():
    prods = load_catalogue()
    pages.init(prods)
    # nettoyage des fiches (les slugs supprimés du JSON disparaissent)
    for f in glob.glob(os.path.join(ROOT, "produits", "*.html")): os.remove(f)
    print(f"{len(prods)} références chargées — traitement des images…")
    srcs = sorted({p["color_images"][c] for p in prods for c in p["colors_ok"]} | {p["image_path"] for p in prods if p["image_path"]})
    from concurrent.futures import ProcessPoolExecutor
    with ProcessPoolExecutor() as ex:
        list(ex.map(_process, srcs, chunksize=4))
    for p in prods: product_images(p)
    pages.home(); pages.particuliers(); pages.professionnels()
    for g in pages.GAMME_PAGES: pages.gamme(g)
    pages.gamme_acces()
    pages.catalogue_index()
    for g in GROUP: pages.catalogue_cat(g)
    pages.services(); pages.a_propos(); pages.contact(); pages.faq(); pages.legal(); pages.sources(); pages.notfound()
    for p in prods: products.fiche(p, prods)
    og_image(); favicons(); sitemap()
    open(os.path.join(ROOT, ".nojekyll"), "w").close()
    prune_images()
    assert_public_copy()
    n_f = len(glob.glob(os.path.join(ROOT, "produits", "*.html")))
    n_p = len(glob.glob(os.path.join(ROOT, "*.html")))
    print(f"OK : {n_p} pages + {n_f} fiches produit, sitemap {len(layout.PAGES)} URL.")

if __name__ == "__main__":
    main()
