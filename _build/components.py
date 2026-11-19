"""Composants réutilisables : carte produit, rail, grille filtrable, CTA."""
from core import *
from tiles import tiles_html

def card(p, pre, sizes="(max-width:640px) 84vw, 340px"):
    meta = default_image(p)
    url = f"{pre}produits/{p['slug']}.html"
    tags = tag_gamme(p["gk"])
    dots = "".join(f'<i style="background:{COLOR_HEX.get(c, "#ccc")}" title="{E(c)}"></i>' for c in p["colors_ok"][:8])
    dots_html = f'<div class="dots" aria-label="Coloris : {E(", ".join(p["colors_ok"]))}">{dots}</div>' if dots else ""
    q = norm(" ".join([p["name"], p["model"], p["category"], p["gamme"], " ".join(p["feats"])]))
    cols = "|".join(slugify(c) for c in p["colors_ok"])
    return (f'<article class="prod" data-q="{E(q)}" data-g="{p["gk"]}" data-c="{slugify(p["category"])}" data-col="{cols}" data-grp="{p["group"]}">'
            f'<div class="prod-media">{picture(meta, p["name"], pre, sizes)}</div>'
            f'<div class="prod-body"><div class="prod-tags">{tags}</div>'
            f'<h3>{E(p["name"])}</h3>'
            f'<p class="sub">{E(p["category"])}</p>{dots_html}'
            f'{tiles_html(p, 4, compact=True)}'
            f'<div class="foot"><span>Sur devis</span><a class="quote" href="{url}">Voir la fiche</a></div></div></article>')

def rail(products, pre, eyebrow, title, more=None, dark=False, lead=None):
    if not products:
        return ""
    cards = "".join(card(p, pre, "(max-width:640px) 72vw, 340px") for p in products)
    more_html = f'<p class="mt-28"><a class="link" href="{pre}{more[0]}">{E(more[1])}</a></p>' if more else ""
    lead_html = f'<p class="lead" style="margin-top:18px">{lead}</p>' if lead else ""
    return f'''<div data-rail>
<div class="rail-head reveal"><div><p class="eyebrow">{eyebrow}</p><h2 class="h2">{title}</h2>{lead_html}</div>
<div class="rail-ctrl"><button type="button" data-prev aria-label="Produits précédents"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M15 18l-6-6 6-6"/></svg></button><button type="button" data-next aria-label="Produits suivants"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M9 18l6-6-6-6"/></svg></button></div></div>
<div class="rail" tabindex="0" role="region" aria-label="{E(re.sub('<[^>]+>', '', title))}">{cards}</div>
{more_html}
</div>'''

SEARCH_ICON = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="M20 20l-3.5-3.5"/></svg>'

def filter_grid(products, pre, with_group=False):
    products = [p for p in products if default_image(p)]
    gks = [g for g in GAMME_LABEL if g != "a-confirmer" and any(p["gk"] == g for p in products)]
    cats = []
    for p in products:
        if p["category"] not in cats: cats.append(p["category"])
    cols = sorted({c for p in products for c in p["colors_ok"]}, key=lambda c: list(COLOR_HEX).index(c) if c in COLOR_HEX else 99)
    opt_g = "".join(f'<option value="{g}">{GAMME_LABEL[g]} ({sum(1 for p in products if p["gk"] == g)})</option>' for g in gks)
    opt_c = "".join(f'<option value="{slugify(c)}">{E(c)} ({sum(1 for p in products if p["category"] == c)})</option>' for c in cats)
    opt_col = "".join(f'<option value="{slugify(c)}">{E(c)}</option>' for c in cols)
    grp = ""
    if with_group:
        grp = '<div><label class="sr-only" for="f-groupe">Univers</label><select id="f-groupe"><option value="">Tous les univers</option>' + "".join(
            f'<option value="{k}">{E(GROUP[k]["label"])} ({sum(1 for p in products if p["group"] == k)})</option>' for k in GROUP) + '</select></div>'
    sous = f'<div><label class="sr-only" for="f-sous">Type de produit</label><select id="f-sous"><option value="">Tous les types</option>{opt_c}</select></div>'
    cards = "".join(card(p, pre) for p in products)
    return f'''<div data-catalogue>
<div class="filters" role="search">
<div class="filter-row">
<div class="field-search">{SEARCH_ICON}<label class="sr-only" for="f-q">Rechercher un produit</label><input id="f-q" type="search" placeholder="Rechercher : nom, référence, usage…" autocomplete="off"></div>
{grp if with_group else sous}
<div><label class="sr-only" for="f-gamme">Gamme</label><select id="f-gamme"><option value="">Toutes les gammes</option>{opt_g}</select></div>
<div><label class="sr-only" for="f-couleur">Coloris</label><select id="f-couleur"><option value="">Tous les coloris</option>{opt_col}</select></div>
<button class="reset" type="button" id="f-reset">Réinitialiser</button>
</div>
</div>
<p class="result-count" id="f-count" aria-live="polite">{len(products)} références</p>
<div class="grid-prod">{cards}</div>
<p class="more-prod"><button type="button" class="btn btn-outline" id="f-more" hidden>Afficher plus de références</button></p>
<div class="empty" id="f-empty" hidden><p>Aucune référence ne correspond à ces critères.</p><p class="mt-24"><a class="link" href="{pre}contact.html#devis">Décrivez-nous votre besoin</a></p></div>
</div>'''

def yt(vid, title, caption, pre=""):
    """Lecteur YouTube au clic (youtube-nocookie), poster HD local."""
    thumb = f"{pre}assets/img/yt/{vid}.jpg"
    return f'''<figure class="yt" data-yt="{E(vid)}" data-yt-auto="1">
<button type="button" class="yt-btn" aria-label="Lire la vidéo : {E(title)}">
<img src="{thumb}" alt="" width="1280" height="720" loading="lazy" decoding="async">
<span class="yt-play" aria-hidden="true"></span>
</button>
<figcaption>{E(caption)}</figcaption>
</figure>'''

def video_ld(vid, title, desc):
    return {
        "@context": "https://schema.org", "@type": "VideoObject",
        "name": title, "description": desc,
        "thumbnailUrl": f"{SITE}/assets/img/yt/{vid}.jpg",
        "embedUrl": f"https://www.youtube-nocookie.com/embed/{vid}",
        "url": f"https://www.youtube.com/watch?v={vid}",
        "publisher": {"@type": "Organization", "name": "Ajax Systems"},
    }

def cta(pre, title="Prêt à sécuriser votre espace ?", text="Étude et devis gratuits, sans engagement. Intervention chez vous, partout à La Réunion.", btn="Demander mon devis gratuit", href="contact.html#devis"):
    return f'''<section class="cta"><div class="wrap reveal">
<h2 class="h2">{title}</h2>
<p>{text}</p>
<div class="btns" style="justify-content:center"><a class="btn btn-light btn-lg" href="{pre}{href}">{btn}</a><a class="btn btn-outline btn-lg" href="{pre}catalogue.html">Explorer le catalogue</a></div>
</div></section>'''

def versus(pre, products=None, base_link=None, sup_link=None):
    """Bloc Baseline / Superior (textes v1 validés) avec compteurs issus des données."""
    def cnt(gk):
        return sum(1 for p in products if p["gk"] == gk) if products is not None else None
    def rows(gk):
        if products is None: return ""
        cats = {}
        for p in products:
            if p["gk"] == gk: cats[p["category"]] = cats.get(p["category"], 0) + 1
        top = sorted(cats.items(), key=lambda x: -x[1])[:4]
        return "<ul>" + "".join(f"<li><span>{E(c)}</span><b>{n} réf.</b></li>" for c, n in top) + "</ul>" if top else ""
    bl = f'<a class="link" href="{pre}{base_link}">Voir les références Baseline</a>' if base_link else ""
    sl = f'<a class="link" href="{pre}{sup_link}">Voir les références Superior</a>' if sup_link else ""
    nb = f' · {cnt("baseline")} références' if products is not None else ""
    ns = f' · {cnt("superior")} références' if products is not None else ""
    return f'''<div class="versus reveal">
<div><span class="tag tag-base">Baseline{nb}</span><h3>L’essentiel, sans fil.</h3><p>Large choix sans fil pour les besoins standards. Déploiement rapide, interface unique, évolutif : idéal pour démarrer et faire grandir votre système.</p>{rows("baseline")}{bl}</div>
<div class="sup on-dark"><span class="tag tag-sup">Superior{ns}</span><h3>Pour les projets exigeants.</h3><p>Sans fil et/ou filaire, multi-zones, sites sensibles : options avancées selon les références. Sur étude Active Sécurité 974, partenaire agréé Ajax Systems.</p>{rows("superior")}{sl}</div>
</div>'''
