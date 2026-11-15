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
    # PNG dérivés du favicon.svg (rendu simple Pillow : carré noir + A blanc + trait rouge)
    for size, name in ((32, "favicon-32.png"), (180, "apple-touch-icon.png"), (512, "icon-512.png")):
        s = size / 64
        im = Image.new("RGBA", (size, size), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        d.rounded_rectangle((0, 0, size - 1, size - 1), radius=int(14 * s), fill=(11, 11, 12))
        pts = [(48, 148), (108, 28), (168, 148), (138, 148), (108, 82), (78, 148)]
        pts = [((x * .32 - 6.5) * s, (y * .32 - 2) * s) for x, y in pts]
        d.polygon(pts, fill="white")
        d.rounded_rectangle((16 * s, 48 * s, 48 * s, 53 * s), radius=max(1, int(1.5 * s)), fill=(225, 6, 0))
        im.save(os.path.join(ROOT, name))

def sitemap():
    today = datetime.date.today().isoformat()
    urls = []
    for path, prio in layout.PAGES:
        loc = SITE + "/" + ("" if path == "index.html" else path)
        urls.append(f"<url><loc>{E(loc)}</loc><lastmod>{today}</lastmod><priority>{prio}</priority></url>")
    open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8").write(
        '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "\n".join(urls) + "\n</urlset>\n")
    from urllib.parse import urlparse
    base_path = urlparse(SITE).path.rstrip("/")
    open(os.path.join(ROOT, "robots.txt"), "w").write(
        f"User-agent: *\nAllow: /\nDisallow: {base_path}/merci.html\n\nSitemap: {SITE}/sitemap.xml\n")

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
    pages.catalogue_index()
    for g in GROUP: pages.catalogue_cat(g)
    pages.services(); pages.a_propos(); pages.contact(); pages.legal(); pages.notfound()
    for p in prods: products.fiche(p, prods)
    og_image(); favicons(); sitemap()
    open(os.path.join(ROOT, ".nojekyll"), "w").close()
    n_f = len(glob.glob(os.path.join(ROOT, "produits", "*.html")))
    n_p = len(glob.glob(os.path.join(ROOT, "*.html")))
    print(f"OK : {n_p} pages + {n_f} fiches produit, sitemap {len(layout.PAGES)} URL.")

if __name__ == "__main__":
    main()
