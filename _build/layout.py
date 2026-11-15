"""Gabarit commun : <head> SEO, en-tête, pied de page."""
import os, json
from core import *

NAV = [
    ("particuliers.html", "Particuliers", "particuliers"),
    ("professionnels.html", "Professionnels", "pros"),
    ("__gammes__", "Gammes", "gammes"),
    ("catalogue.html", "Catalogue", "catalogue"),
    ("services.html", "Services", "services"),
    ("a-propos.html", "À propos", "apropos"),
]
GAMMES_MENU = [
    ("gamme-alarme.html", "Alarme intrusion", "Détection, claviers, sirènes"),
    ("gamme-incendie.html", "Incendie", "Fumée, chaleur, CO"),
    ("gamme-video.html", "Vidéosurveillance", "Caméras, NVR, sonnette"),
    ("gamme-domotique.html", "Domotique", "Éclairage, prises, fuites d’eau"),
]
PAGES = []  # (path, priority) pour le sitemap

ICON_LIST = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M8 3.5h6.5L19 8v12.5a1 1 0 0 1-1 1H8a1 1 0 0 1-1-1v-16a1 1 0 0 1 1-1z"/><path d="M14.5 3.5V8H19"/><path d="M9.5 13h6M9.5 16.5h4"/></svg>'

def local_business():
    b = CFG["business"]
    data = {
        "@context": "https://schema.org", "@type": "LocalBusiness", "@id": SITE + "/#entreprise",
        "name": BRAND, "alternateName": CFG["brand_short"], "url": SITE + "/",
        "logo": SITE + "/assets/img/logo/as974-wordmark-noir.svg",
        "image": SITE + "/assets/img/og-as974.jpg",
        "description": "Installateur partenaire agréé Ajax Systems à La Réunion : alarme, incendie, vidéosurveillance et domotique, en intervention chez le client sur toute l’île.",
        "areaServed": {"@type": "AdministrativeArea", "name": "La Réunion"},
    }
    if b.get("telephone"):
        data["telephone"] = b["telephone"]
    if b.get("email"):
        data["email"] = b["email"]
    if b.get("adresse"):
        data["address"] = {"@type": "PostalAddress", "streetAddress": b["adresse"], "addressRegion": "La Réunion", "addressCountry": "RE"}
    if b.get("siret"):
        data["identifier"] = {"@type": "PropertyValue", "propertyID": "SIRET", "value": b["siret"]}
    return data

def head(title, desc, path, pre, og_image=None, og_type="website", jsonld=None, noindex=False, base=None):
    url = SITE + "/" + (path if path != "index.html" else "")
    ld = [local_business()] + (jsonld or [])
    robots = '<meta name="robots" content="noindex,follow">' if noindex else ""
    return f'''<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{E(title)}</title>
<meta name="description" content="{E(desc)}">
<link rel="canonical" href="{E(url)}">
{f'<base href="{E(base)}">' if base else ''}
{robots}
<meta name="theme-color" content="#0B0B0C">
<meta property="og:type" content="{og_type}">
<meta property="og:locale" content="fr_FR">
<meta property="og:site_name" content="{E(BRAND)}">
<meta property="og:title" content="{E(title)}">
<meta property="og:description" content="{E(desc)}">
<meta property="og:url" content="{E(url)}">
<meta property="og:image" content="{E(og_image or SITE + '/assets/img/og-as974.jpg')}">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="{pre}favicon.svg" type="image/svg+xml">
<link rel="icon" href="{pre}favicon-32.png" sizes="32x32" type="image/png">
<link rel="apple-touch-icon" href="{pre}apple-touch-icon.png">
<link rel="preload" href="{pre}assets/fonts/inter-latin-var.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{pre}assets/css/site.css">
<script type="application/ld+json">{json.dumps(ld if len(ld) > 1 else ld[0], ensure_ascii=False)}</script>
</head>
'''

def header(pre, current):
    items = []
    for href, label, key in NAV:
        if href == "__gammes__":
            sub = "".join(f'<a href="{pre}{h}"{" aria-current=\"page\"" if current == h else ""}>{l}<small>{s}</small></a>' for h, l, s in GAMMES_MENU)
            cur = " is-current" if current.startswith("gamme-") else ""
            items.append(f'<div class="nav-drop{cur}"><button type="button" aria-expanded="false" aria-controls="menu-gammes">Gammes</button><div class="nav-menu" id="menu-gammes">{sub}</div></div>')
        else:
            on = current == href or (key == "catalogue" and (current.startswith("catalogue") or current.startswith("produits/")))
            items.append(f'<a href="{pre}{href}"{" aria-current=\"page\"" if on else ""}>{label}</a>')
    items.append(f'<a href="{pre}contact.html"{" aria-current=\"page\"" if current == "contact.html" else ""}>Contact</a>')
    items.append(f'<a class="nav-cta" href="{pre}contact.html#devis">Demander un devis gratuit</a>')
    return f'''<body>
<a class="skip-link" href="#contenu">Aller au contenu</a>
<header class="header">
<div class="header-inner">
<a class="logo-link" href="{pre}index.html" aria-label="{E(BRAND)} — accueil"><img class="logo" src="{pre}assets/img/logo/as974-wordmark-noir.svg" alt="AS974" width="168" height="48"></a>
<nav class="nav" id="site-nav" aria-label="Navigation principale">{"".join(items)}</nav>
<div class="header-actions">
<a class="icon-btn icon-devis" href="{pre}contact.html#devis" aria-label="Ma sélection devis"><span class="sr-only sl-label">Ma sélection devis</span>{ICON_LIST}<span class="icon-label">Devis</span><span class="sl-count" hidden>0</span></a>
<a class="btn btn-primary btn-quote" href="{pre}contact.html#devis">Devis gratuit</a>
<button class="icon-btn menu-toggle" type="button" aria-expanded="false" aria-controls="site-nav" aria-label="Ouvrir le menu"><span class="bars" aria-hidden="true"><i></i><i></i><i></i></span></button>
</div>
</div>
</header>
<main id="contenu">
'''

def footer(pre):
    b = CFG["business"]
    return f'''</main>
<footer class="footer on-dark">
<div class="wrap-wide">
<div class="footer-top">
<div>
<img class="logo" src="{pre}assets/img/logo/as974-wordmark-blanc.svg" alt="AS974" width="168" height="48" loading="lazy">
<address class="nap">
<strong style="color:#fff">{E(BRAND)}</strong><br>
{br_line("", biz("adresse"))}
{br_line("Tél.", biz("telephone"))}
{br_line("", biz("email"))}
{br_line("SIRET", biz("siret"))}
Interventions chez le client, sur toute l’île de La Réunion
</address>
</div>
<div><h2>Solutions</h2><ul>
<li><a href="{pre}particuliers.html">Particuliers</a></li>
<li><a href="{pre}professionnels.html">Professionnels</a></li>
<li><a href="{pre}services.html">Services</a></li>
<li><a href="{pre}a-propos.html">À propos</a></li>
<li><a href="{pre}contact.html">Contact &amp; devis</a></li>
</ul></div>
<div><h2>Gammes</h2><ul>
<li><a href="{pre}gamme-alarme.html">Alarme intrusion</a></li>
<li><a href="{pre}gamme-incendie.html">Incendie</a></li>
<li><a href="{pre}gamme-video.html">Vidéosurveillance</a></li>
<li><a href="{pre}gamme-domotique.html">Domotique</a></li>
<li><a href="{pre}catalogue.html">Catalogue complet</a></li>
</ul></div>
<div><h2>Informations</h2><ul>
<li><a href="{pre}mentions-legales.html">Mentions légales</a></li>
<li><a href="{pre}politique-confidentialite.html">Confidentialité</a></li>
<li><a href="{pre}cookies.html">Cookies</a></li>
</ul>
<p class="footer-legal">Partenaire agréé Ajax Systems. Active Sécurité 974 est une marque distincte ; Ajax Systems et ses visuels appartiennent à leur titulaire. Catalogue et devis uniquement, sans vente en ligne.</p>
</div>
</div>
<div class="footer-bottom"><span>© {YEAR} {E(BRAND)} · AS974</span><span>Alarme · Incendie · Vidéosurveillance · Domotique — La Réunion</span></div>
</div>
</footer>
<script src="{pre}assets/js/site.js" defer></script>
</body>
</html>
'''

def write_page(path, title, desc, body, og_image=None, og_type="website", jsonld=None, priority="0.7", noindex=False, sitemap=True, pre=None, base=None):
    depth = path.count("/")
    pre = ("../" * depth) if pre is None else pre
    out = head(title, desc, path, pre, og_image, og_type, jsonld, noindex, base) + header(pre, path) + body + footer(pre)
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    open(full, "w", encoding="utf-8").write(out)
    if sitemap and not noindex:
        PAGES.append((path, priority))

def crumbs(pre, items):
    """items: [(href|None, label)] ; produit aussi un BreadcrumbList JSON-LD."""
    parts = [f'<a href="{pre}index.html">Accueil</a>']
    ld = [{"@type": "ListItem", "position": 1, "name": "Accueil", "item": SITE + "/"}]
    for i, (h, l) in enumerate(items, start=2):
        parts.append('<span aria-hidden="true">/</span>')
        parts.append(f'<a href="{pre}{h}">{E(l)}</a>' if h else f'<span aria-current="page">{E(l)}</span>')
        it = {"@type": "ListItem", "position": i, "name": l}
        if h: it["item"] = SITE + "/" + h
        ld.append(it)
    return (f'<nav class="crumbs" aria-label="Fil d’Ariane">{"".join(parts)}</nav>',
            {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": ld})
