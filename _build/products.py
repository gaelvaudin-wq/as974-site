"""Fiches produit : une page par référence, générée depuis le JSON catalogue."""
import json
from core import *
from layout import write_page, crumbs
from components import rail, yt, video_ld
from sell import siblings, family_of

ICON_CHECK = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20 6L9 17l-5-5"/></svg>'
VIDEO_CATS = {"Caméras filaires", "Caméras Wi-Fi", "Enregistreurs vidéo", "Sonnettes"}

def video_line(p):
    if p["category"] not in VIDEO_CATS:
        return None
    blob = (p["name"] + " " + p["slug"]).lower()
    if "superior" in blob:
        return "superior"
    return "baseline"

def fiche_video(p, pre="../"):
    line = video_line(p)
    if line:
        return yt("o8VNaCPCydE", "De la détection à la réaction", "Les caméras Ajax, Baseline comme Superior, peuvent lancer une réaction. Vidéo Ajax Systems, en français.", pre)
    return ""

def video_ai_note(p, pre):
    line = video_line(p)
    if not line:
        return ""
    return f'''<aside class="ai-note"><p>Baseline et Superior reconnaissent personnes, véhicules et animaux, et peuvent lancer l’alarme.</p></aside>'''

def fiche(p, all_products):
    pre = "../"
    path = f"produits/{p['slug']}.html"
    g = GROUP[p["group"]]
    cr, ld_crumbs = crumbs(pre, [("catalogue.html", "Catalogue"), (f"catalogue-{p['group']}.html", g["label"]), (None, p["name"])])
    complement = ""
    if p["group"] == "alarme" and p["category"] == "Détecteurs d'incendie":
        complement = ('<p class="note">Ce détecteur complète une alarme intrusion Baseline. '
                      'Il n’appartient pas à la ligne EN54. '
                      f'<a href="{pre}gamme-alarme.html#completer">Compléter votre alarme</a>.</p>')
    ims = product_images(p)
    p["colors_ok"] = [c for c in p["colors_ok"] if c in ims]
    cur = p["default_color"] if p["default_color"] in p["colors_ok"] else (p["colors_ok"][0] if p["colors_ok"] else "")
    meta = ims.get(cur) if cur else ims.get("")
    sizes = "(max-width:980px) 88vw, 620px"
    stage = picture(meta, p["name"] + (f" — coloris {cur}" if cur else ""), pre, sizes, eager=True, idimg="pdp-img", idsrc="pdp-src")
    # données couleur pour le JS
    jsimgs = {}
    for c in p["colors_ok"]:
        m = ims[c]; ss, fb = img_urls(m, pre)
        jsimgs[c] = {"webp": ss, "png": fb, "w": m["w"], "h": m["h"]}
    data = {"slug": p["slug"], "name": p["name"], "ref": p["model"], "default": cur, "images": jsimgs, "contact": pre + "contact.html"}
    fam = siblings(p, all_products)
    if len(fam) > 1:
        opts = "".join(
            f'<option value="{pre}produits/{x["slug"]}.html"{" selected" if x["slug"]==p["slug"] else ""}>{E(x["name"])} — {E(x["model"])}</option>'
            for x in fam)
        variant = (f'<label class="variant">Version <select id="pdp-variant">{opts}</select></label>'
                   f'<p class="note">Autres versions officielles de la même famille (optique, format, Jeweller ou Fibra, alimentation). Le coloris choisi est repris sur la fiche suivante.</p>')
    else:
        variant = ""
    ralmap = p.get("color_ral") or {}
    def _title(c):
        r = ralmap.get(c)
        return f"{c} · {r}" if r else c
    # sélecteur couleur : uniquement les teintes documentées pour CETTE référence
    if len(p["colors_ok"]) > 1:
        sw = "".join(
            f'<div class="sw"><input type="radio" name="couleur" id="c-{slugify(c)}" value="{E(c)}"{" checked" if c == cur else ""}>'
            f'<label for="c-{slugify(c)}" title="{E(_title(c))}"><i style="background:{COLOR_HEX.get(c, "#ccc")}"></i><span class="sr-only">{E(_title(c))}</span></label></div>'
            for c in p["colors_ok"])
        colors = (f'<fieldset class="colors"><legend>Coloris <output id="pdp-color-name">{E(_title(cur))}</output></legend><div class="swatches">{sw}</div>'
                  f'<p class="note">{len(p["colors_ok"])} coloris officiels pour cette référence. Aucune teinte n’est ajoutée au-delà de la fiche Ajax. Les pastilles sont indicatives.</p></fieldset>')
    elif len(p["colors_ok"]) == 1:
        c = p["colors_ok"][0]
        colors = (f'<fieldset class="colors"><legend>Coloris <output id="pdp-color-name">{E(c)}</output></legend><div class="swatches">'
                  f'<div class="sw"><input type="radio" name="couleur" id="c-{slugify(c)}" value="{E(c)}" checked><label for="c-{slugify(c)}" title="{E(c)}"><i style="background:{COLOR_HEX.get(c, "#ccc")}"></i><span class="sr-only">{E(c)}</span></label></div></div>'
                  f'<p class="note">Coloris unique documenté par le fabricant.</p></fieldset>')
    else:
        note = "Sans objet pour cette référence." if p["color_status"] == "not-applicable" else "Coloris non documenté sur la fiche officielle : à préciser lors du devis."
        colors = f'<div class="colors"><p class="lbl" style="font-weight:650">Coloris</p><p class="note">{note}</p></div>'
    extra_comp = ""
    for comp in p.get("component_color_options") or []:
        extra_comp += f'<tr><th scope="row">{E(comp["title"])}</th><td>{E(", ".join(comp["colors_available"]))}</td></tr>'
    tags = tag_gamme(p["gk"])
    avail = f'<p class="avail">{E(p["avail_note"])}</p>' if p["avail_note"] else ""
    all_benefits = p.get("benefits") or []
    extra = [b for b in all_benefits if norm(b) != norm(p.get("hook") or "")]
    benefits = "".join(f"<li>{E(b)}</li>" for b in extra[:3])
    feats_rows = "".join(f"<li>{E(b)}</li>" for b in all_benefits[:3])
    related = [x for x in all_products if x["category"] == p["category"] and x["slug"] != p["slug"]]
    if len(related) < 4:
        related += [x for x in all_products if x["group"] == p["group"] and x["slug"] != p["slug"] and x not in related]
    related = related[:10]
    quote_href = f'{pre}contact.html?produit={p["slug"]}&amp;modele={E(p["name"]).replace(" ", "+")}&amp;ref={E(p["model"]).replace(" ", "+")}' + (f'&amp;couleur={E(cur)}' if cur else "") + "#devis"
    body = f'''<section class="pdp"><div class="wrap-wide">
{cr}
<div class="pdp-grid">
<div class="pdp-stage">{stage}</div>
<div class="pdp-info">
<div class="prod-tags">{tags}</div>
<h1 class="h1">{E(p["name"])}</h1>
<p class="fr-sub">{E(p["category"])}</p>
<p class="ref">Réf. fabricant {E(p["model"])} · Ajax Systems, marque partenaire</p>
<div class="pdp-price"><strong>Sur devis</strong><span>Étude, fourniture et installation par Active Sécurité 974</span></div>
<p class="pdp-desc">{E(p["hook"])}</p>
{f'<details class="more"><summary>En savoir plus</summary><ul class="benefits">{benefits}</ul></details>' if benefits else ''}
{variant}
{colors}
{complement}
{avail}
{video_ai_note(p, pre)}
{fiche_video(p, pre)}
<div class="pdp-actions">
<a class="btn btn-primary btn-lg js-quote" id="pdp-quote" href="{quote_href}">Demander un devis</a>
<button class="btn btn-outline btn-lg" type="button" id="pdp-add" aria-pressed="false">Ajouter à ma sélection devis</button>
</div>
<ul class="assure">
<li>{ICON_CHECK}Étude et devis gratuits, sans engagement</li>
<li>{ICON_CHECK}Installation chez vous, partout à La Réunion</li>
<li>{ICON_CHECK}Partenaire agréé Ajax Systems</li>
</ul>
</div>
</div>
</div></section>
<div class="pdp-bar"><a class="btn btn-primary js-quote" href="{quote_href}">Demander un devis</a></div>
<section class="section bg-off"><div class="wrap specs">
<div class="reveal"><p class="eyebrow">Caractéristiques</p><h2 class="h2">En bref.</h2>
<p class="src-note">Source : Ajax Systems</p></div>
<div class="reveal d1"><table class="spec">
<tr><th scope="row">Modèle</th><td>{E(p["name"])}</td></tr>
<tr><th scope="row">Référence fabricant</th><td>{E(p["model"])}</td></tr>
{f'<tr><th scope="row">Gamme</th><td>{E(GAMME_LABEL[p["gk"]])}</td></tr>' if p["gk"] != "a-confirmer" else ''}
<tr><th scope="row">Type</th><td>{E(p["category"])}</td></tr>
{f'<tr><th scope="row">Points clés</th><td><ul style="margin-left:18px">{feats_rows}</ul></td></tr>' if feats_rows else ''}
<tr><th scope="row">Coloris officiels</th><td>{E(", ".join(p["colors_ok"])) if p["colors_ok"] else "À préciser lors du devis"}</td></tr>
{extra_comp}
<tr><th scope="row">Prix</th><td>Sur devis</td></tr>
<tr><th scope="row">Disponibilité</th><td>{E(p["avail_tag"] or "Précisée dans le devis")}</td></tr>
</table></div>
</div></section>
<section class="section"><div class="wrap">
{rail(related, pre, "Dans la même famille", "Autres produits.", (f"catalogue-{p['group']}.html", "Tout l’univers " + g["label"]))}
</div></section>
<script type="application/json" id="pdp-data">{json.dumps(data, ensure_ascii=False)}</script>'''
    m0 = meta or default_image(p)
    ld_product = {"@context": "https://schema.org", "@type": "Product", "name": p["name"], "sku": p["model"], "mpn": p["model"],
                  "brand": {"@type": "Brand", "name": "Ajax Systems"}, "category": p["category"], "description": p["desc"],
                  "url": f"{SITE}/{path}"}
    if m0: ld_product["image"] = [abs_img(ims[c]) for c in p["colors_ok"]] or [abs_img(m0)]
    if p["colors_ok"]: ld_product["color"] = ", ".join(p["colors_ok"])
    title = f'{p["title_name"]} — {g["label"]} sur devis | AS974'
    desc = clip(f'{p["name"]} (réf. {p["model"]}) : {lcfirst(p["feats"][0]) if p["feats"] else p["category"]}. Sur devis, installation par Active Sécurité 974 à La Réunion.')
    lds = [ld_crumbs, ld_product]
    if video_line(p):
        lds.append(video_ld("o8VNaCPCydE", "De la détection à la réaction", "Les caméras Ajax peuvent lancer une réaction automatique."))
    write_page(path, title, desc, body, og_image=abs_img(m0) if m0 else None, og_type="product", jsonld=lds, priority="0.6")
