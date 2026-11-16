"""Blocs qui vendent : performances sourcées, étude, pose, choix, différence AS974."""
from core import *

HUB = "https://ajax.systems/fr/products/hub-2/"
MP = "https://ajax.systems/fr/products/motionprotect/"
LS = "https://ajax.systems/fr/products/lightswitch-1-gang-jeweller/"
LS_MAN = "https://ajax.systems/support/manuals/lightswitch/"
VID = "https://ajax.systems/fr/catalogue/video-surveillance/"
VID_S = "https://ajax.systems/fr/catalogue/superior-video-surveillance/"
EN54 = "https://ajax.systems/fr/solutions/en-54-certified-fire-and-life-safety-solution/"

LS_COLORS = [
    ("Noir", "#0E0E10", "RAL 9005"),
    ("Graphite", "#474A51", "RAL 7024"),
    ("Blanc", "#F7F7F7", "RAL 9003"),
    ("Ivoire", "#EAE6CA", "RAL 1013"),
    ("Fumée", "#D0D0D0", "RAL 7047"),
    ("Huître", "#E7EBDA", "RAL 9002"),
    ("Gris", "#969992", "RAL 7004"),
    ("Olive", "#B7B3A8", "RAL 7044"),
]


def act(pre, href="contact.html#devis", label="Demander une étude gratuite"):
    return f'<p class="act"><a class="btn btn-primary" href="{pre}{href}">{E(label)}</a></p>'


def _src(*links):
    bits = " · ".join(f'<a href="{u}" rel="noopener">{E(t)}</a>' for t, u in links)
    return f'<p class="src-note">Sources Ajax : {bits}.</p>'


def performances(kind):
    if kind == "video":
        body = f'''<p>Ajax présente deux lignes, Baseline et Superior. Sur le catalogue Baseline, l’intelligence artificielle est intégrée aux caméras : elle reconnaît les personnes, les véhicules et les animaux, et peut lancer une réaction. Ajax indique aussi, pour cette ligne, un matériel conforme NDAA. Superior reprend cette base et ajoute, selon les modèles, une optique varifocal P-Iris, un haut-parleur et les enregistreurs NVR H2D. Ce n’est pas une promesse de zéro fausse alerte : le réglage des zones et le fait que le système soit armé se décident à l’étude.</p>
<p>La levée de doute ne concerne pas tous les détecteurs. Ajax indique, pour Hub 2 associé à MotionCam, une première photo en 9 secondes dans des conditions précises : résolution 320×240, signal à 2 ou 3 barres, centrale reliée en Ethernet ou en LTE. Un détecteur de mouvement sans photo n’envoie pas d’image.</p>'''
        src = _src(("catalogue Baseline", VID), ("catalogue Superior", VID_S), ("Hub 2", HUB))
    elif kind == "incendie":
        body = '''<p>Deux usages, qu’Ajax sépare. Les détecteurs FireProtect et FireProtect 2 de la Residence Line complètent une alarme de logement : fumée, chaleur ou monoxyde selon le modèle, dans la même application que l’intrusion. Ils ne remplacent pas un système incendie de bâtiment. Pour les sites professionnels, Ajax présente la ligne EN54 comme un système d’alarme incendie sans fil conçu selon EN 54. Sur la fiche de la centrale EN54 Fire Hub, Ajax cite EN 54-2, EN 54-4, EN 54-13, EN 54-21, EN 54-25 et EN 50131 Grade 2. Les détecteurs de la ligne citent EN 54-3, EN 54-5, EN 54-7 et EN 54-25 selon les versions. Ajax précise que seule la version rouge du déclencheur manuel est certifiée EN 54-25. La ligne Type 4 est une autre offre professionnelle, distincte de l’EN54.</p>'''
        src = _src(("solution EN 54", EN54))
    elif kind == "domotique":
        body = f'''<p>LightSwitch est un interrupteur tactile. Ajax indique qu’il ne nécessite pas de fil neutre, qu’il commande des lampes de 5 à 600 W, et que le panneau réagit au toucher et à l’approche de la main jusqu’à 15 mm. La portée radio annoncée pour ce modèle est de 1 100 m avec une centrale Ajax, en champ libre : ce n’est pas la portée de 2 000 m du Hub 2, qui concerne d’autres appareils. Huit coloris de panneau tactile sont documentés, avec un code RAL donné comme approximation, pas comme une garantie de teinte.</p>
<p>Les cadres officiels accueillent 2, 3, 4 ou 5 appareils, à l’horizontale, et il existe des cadres verticaux. Un interrupteur seul se pose sans cadre multiple. Ajax précise que les combinaisons avec prises ne se font qu’à l’horizontale. Outlet Jeweller mesure la consommation ; les Outlet basic sont des prises encastrées sans radio. Socket est une prise portable, en noir ou blanc selon la fiche. Relay et WallSwitch pilotent un circuit. LeaksProtect signale l’eau au sol. WaterStop, en trois diamètres, est une vanne télécommandée. LifeQuality mesure la température, l’humidité et, sur le modèle complet, le CO₂.</p>'''
        src = _src(("LightSwitch (1-gang)", LS), ("manuel LightSwitch", LS_MAN))
    elif kind == "acces":
        body = f'''<p>L’accès au système se fait par le clavier, un code, un badge Tag ou Pass, ou l’application. Ajax indique que Hub 2 gère jusqu’à 50 utilisateurs et 9 groupes de sécurité. On peut donc séparer une zone bureau d’une zone réserve, ou donner un droit limité à une personne, sans partager le code du propriétaire. Les claviers existent en Jeweller et, pour plusieurs modèles, en Fibra. KeyPad Plus et les versions Superior lisent les badges. Tag et Pass sont proposés par lots de 3, 10 ou 100.</p>
<p>Le contrôle d’accès dont nous parlons ici est celui du système Ajax : armer, désarmer, identifier qui a agi. Ce n’est pas un contrôle d’accès de porte d’immeuble avec gâche, sauf si l’étude retient un relais pour piloter un équipement compatible.</p>'''
        src = _src(("Hub 2", HUB))
    elif kind == "accessoires":
        body = '''<p>Les accessoires ne portent pas, à eux seuls, les chiffres de portée du Hub 2. Ce sont les alimentations, les boîtiers, les modules d’intégration et les pièces de pose qui rendent une installation tenable : un MultiTransmitter pour reprendre une ancienne ligne filaire, une alimentation pour une centrale ou un NVR, un boîtier quand l’appareil est livré sans coffret. Le choix se fait à l’étude, à partir de la fiche Ajax de chaque référence, pas à partir d’un kit figé.</p>'''
        src = _src(("Hub 2", HUB))
    else:
        body = f'''<p>Ajax indique, pour Hub 2, jusqu’à 2 000 m de communication radio avec une centrale ou un prolongateur de portée, en champ libre, et la possibilité de raccorder jusqu’à cinq prolongateurs. La centrale se relie en Ethernet et par deux cartes SIM : si un réseau tombe, elle bascule. La batterie de secours annoncée va jusqu’à 16 heures pour Hub 2 (2G) et jusqu’à 15 heures pour Hub 2 (4G), lorsque l’Ethernet est coupé. Ajax Cloud peut signaler une perte de liaison en 60 secondes. Les échanges sont décrits comme chiffrés : Ajax parle, pour MotionProtect, d’un chiffrement par blocs avec une clé dynamique. La centrale interroge les détecteurs toutes les 12 à 300 secondes, intervalle réglable.</p>
<p>MotionProtect couvre jusqu’à 12 m, avec un angle de 88,5°. Installé à 2,4 m, Ajax indique une immunité aux animaux jusqu’à 20 kg et moins de 50 cm. L’autonomie mise en avant est de 5 ans ; la description technique de la même fiche évoque aussi jusqu’à 7 ans avec une pile CR123A. La portée radio de ce détecteur est indiquée jusqu’à 1 700 m en champ ouvert, pas 2 000 m. Ces chiffres sont ceux du fabricant, en conditions qu’il précise. Les murs, la tôle et l’humidité de La Réunion se vérifient sur place, au test radio.</p>'''
        src = _src(("Hub 2", HUB), ("MotionProtect", MP))
    return f'''<section class="section"><div class="wrap prose">
<h2 class="h2">Ce que le matériel tient, selon Ajax.</h2>
{body}
{src}
{act("")}
</div></section>'''


def etude(kind):
    sujet = {
        "video": "les angles morts, la nuit, l’alimentation des caméras et ce qui doit, ou non, déclencher l’alarme",
        "incendie": "les pièces de vie, les locaux techniques, et le fait qu’un logement et un bâtiment n’appellent pas la même ligne",
        "domotique": "les circuits d’éclairage, le neutre disponible ou non, les prises à mesurer et les arrivées d’eau",
        "acces": "qui doit armer, qui ne doit pas tout voir, et quelles zones se séparent",
        "alarme": "chaque accès, chaque volume, les animaux, les ouvrants et la qualité radio réelle",
    }.get(kind, "les accès, les volumes et la façon dont le lieu est occupé")
    return f'''<section class="section bg-off"><div class="wrap prose">
<h2 class="h2">L’étude se fait chez vous, avant le devis.</h2>
<p>Active Sécurité 974 commence par une visite sur place, sur toute l’île. Nous regardons {sujet}. L’analyse porte sur les risques du lieu et sur les accès, pas sur une liste d’appareils à placer partout. Le dimensionnement vient ensuite : combien de détecteurs, quelle centrale, quelles caméras, quels automatismes, et seulement là où ils servent.</p>
<p>Le devis est gratuit et sans engagement. Il décrit le matériel, la pose et le paramétrage. Aucun prix n’est affiché sur ce site, parce que deux maisons voisines ne donnent pas le même chantier. Pour un échange simple, des photos peuvent préparer la visite. Elles ne la remplacent pas quand il faut mesurer la radio ou voir une charpente.</p>
{act("", "contact.html#devis", "Prendre rendez-vous pour l’étude")}
</div></section>'''


def pose(kind):
    return f'''<section class="section"><div class="wrap prose">
<h2 class="h2">La pose, le réglage, puis nous restons joignables.</h2>
<p>L’installation est faite chez vous. Les appareils sans fil se posent sur leur support, les liaisons filaires Fibra ou l’alimentation des caméras suivent le plan de l’étude. Nous testons la radio ou le bus, les zones de détection, les sirènes et les notifications avant de partir. Les utilisateurs, les groupes, les droits et les scénarios sont paramétrés avec vous, pas laissés sur les réglages d’usine.</p>
<p>Vous repartez en sachant armer, désarmer, lire une alerte et reconnaître une panne de pile. Un récapitulatif de ce qui a été posé vous est remis. Ensuite, la maintenance et le dépannage se font selon ce qui est écrit au devis. La télésurveillance peut être étudiée à ce moment-là. Elle n’est pas un service déjà ouvert sur ce site.</p>
{act("", "services-installation.html", "Voir le déroulé de l’installation")}
</div></section>'''


def choix(products, pre, kind):
    n = len(products)
    colors = sorted({c for p in products for c in p.get("colors_ok") or []})
    col = ", ".join(colors) if colors else "les coloris indiqués sur chaque fiche"
    jew = sum(1 for p in products if "jeweller" in p["slug"] or "Jeweller" in p["name"])
    fib = sum(1 for p in products if "fibra" in p["slug"] or "Fibra" in p["name"])
    return f'''<section class="section bg-off"><div class="wrap prose">
<h2 class="h2">Le choix se fait dans le catalogue officiel, pas dans deux coloris imposés.</h2>
<p>Cette page couvre {n} références du catalogue AS974 pour cette famille. Sur chaque fiche, le sélecteur de version propose les autres modèles de la même famille, par exemple une autre optique, un autre nombre de gangs, une alimentation différente, ou la déclinaison Jeweller et Fibra quand Ajax les publie toutes les deux. Le sélecteur de coloris n’affiche que les teintes documentées pour cette référence, avec leur visuel officiel quand Ajax le fournit. Ici, cela représente {jew} références radio Jeweller et {fib} références filaires Fibra. Les coloris rencontrés dans la famille : {E(col)}.</p>
<p>Le système peut s’agrandir ensuite : un prolongateur de portée, une caméra, un détecteur incendie de logement ou un automatisme rejoignent la même application. On ne change pas de marque pour ajouter une pièce.</p>
{act(pre, "contact.html#devis", "Demander un devis sur cette sélection")}
</div></section>'''


def pourquoi(kind, pre=""):
    return f'''<section class="section"><div class="wrap prose">
<h2 class="h2">Pourquoi choisir Active Sécurité 974.</h2>
<p>Nous sommes partenaire agréé Ajax Systems, et nous n’installons pas un mélange de marques sur le même devis. Alarme, vidéo, incendie de logement et automatismes restent dans une seule application, celle du fabricant. L’étude, la pose et le suivi sont faits par le même interlocuteur, chez vous, de Saint-Denis à Saint-Pierre, du littoral aux Hauts.</p>
<p>Un kit à monter soi-même vous laisse le plan, le test radio et les droits utilisateurs. Cela peut suffire à quelqu’un qui veut bricoler. Ce n’est pas ce que nous vendons : nous venons voir le lieu, nous dimensionnons, nous posons et nous formons. Un installateur qui mélange plusieurs marques peut couvrir plus de catalogues. La contrepartie, chez nous, est l’inverse : un seul écosystème, dont nous répondons après la mise en service.</p>
<p>Certaines offres du marché lient le matériel à un abonnement de télésurveillance, parfois avec une durée d’engagement. Ici, le devis porte d’abord sur le système installé chez vous. Si vous voulez un centre de télésurveillance, nous le regardons à part, pendant l’étude. Nous ne l’affichons pas comme un service déjà souscrit, et nous n’annonçons pas de durée de contrat que nous n’avons pas publiée.</p>
<p>Nous ne publions ni classement, ni nombre de clients, ni avis. La différence à juger est celle du déroulé : visite, analyse, devis détaillé, pose, tests, formation, puis un SAV prévu au devis.</p>
{act(pre)}
</div></section>'''


def index_produits(products, pre, titre="Toutes les références, pour choisir puis demander un devis."):
    items = []
    for p in products:
        cols = ", ".join(p["colors_ok"]) if p["colors_ok"] else "coloris à préciser au devis"
        feat = p["feats"][0] if p["feats"] else p["category"]
        items.append(
            f'<li><a href="{pre}produits/{p["slug"]}.html">{E(p["name"])}</a>'
            f'<span>Réf. {E(p["model"])} · {E(cols)}. {E(feat)}</span></li>'
        )
    return f'''<section class="section bg-off" id="references-gamme"><div class="wrap">
<h2 class="h2">{E(titre)}</h2>
<p class="lead">Chaque lien ouvre la fiche, avec le sélecteur de version et de coloris, et le bouton de devis.</p>
<ul class="ref-index">{"".join(items)}</ul>
{act(pre, "contact.html#devis", "Aucune référence ne convient telle quelle : décrire mon besoin")}
</div></section>'''


def blocs(kind, products, pre=""):
    return performances(kind) + etude(kind) + pose(kind) + choix(products, pre, kind) + pourquoi(kind, pre) + index_produits(products, pre)


def family_of(p):
    import re
    if p["slug"].startswith("lightswitch"):
        return "lightswitch"
    if p["slug"].startswith("outlet"):
        return "outlet"
    if p["slug"].startswith("socket"):
        return "socket"
    if "waterstop" in p["slug"]:
        return "waterstop"
    n = p["name"].lower()
    n = re.sub(r"\b(jeweller|fibra|superior|ajax)\b", " ", n)
    n = re.sub(r"\[.*?\]|\(.*?\)", " ", n)
    n = re.sub(r"\b\d+\s*mp\b.*", " ", n)
    n = re.sub(r"\btype\s+[a-z]\b", " ", n)
    n = re.sub(r"[^a-z0-9]+", " ", n).strip()
    return n or p["slug"]


def configurateur(devices):
    """devices: [{slug,name,model,kind,images:{color:url}}] — visuels officiels déjà au catalogue."""
    import json as _json
    payload = {"colors": [{"name": n, "hex": h, "ral": r} for n, h, r in LS_COLORS], "devices": devices}
    sw = "".join(
        f'<button type="button" class="cfg-color" data-color="{E(n)}" style="--c:{h}" aria-pressed="{"true" if n=="Blanc" else "false"}">'
        f'<span class="sr-only">{E(n)} {E(r)}</span></button>' for n, h, r in LS_COLORS)
    return f'''<section class="section" id="configurateur"><div class="wrap">
<h2 class="h2">Composer un ensemble d’interrupteurs et de prises.</h2>
<div class="prose"><p>Choisissez le nombre de postes, le modèle de chaque poste et le coloris du panneau. Les huit teintes sont celles publiées par Ajax pour LightSwitch et Outlet : noir, graphite, blanc, ivoire, fumée, huître, gris et olive. Un poste seul se pose sans cadre. Les cadres Ajax existent en 2, 3, 4 et 5 postes. Les cadres verticaux existent. Ajax indique que les prises ne se combinent qu’en cadre horizontal. Le rendu utilise les visuels officiels du catalogue. La composition part dans la demande de devis, sans prix.</p></div>
<div class="cfg" id="cfg" data-cfg>
<div class="cfg-controls">
<label>Postes <select id="cfg-seats"><option>1</option><option selected>2</option><option>3</option><option>4</option><option>5</option></select></label>
<div class="cfg-colors" role="group" aria-label="Coloris du panneau">{sw}</div>
<p class="note" id="cfg-color-name">Blanc · RAL 9003. Le RAL est une approximation indiquée par Ajax.</p>
<div id="cfg-slots"></div>
</div>
<div class="cfg-stage" id="cfg-stage" aria-live="polite"></div>
</div>
<p class="act"><button type="button" class="btn btn-primary" id="cfg-quote">Ajouter cet ensemble à ma demande de devis</button></p>
<script type="application/json" id="cfg-data">{_json.dumps(payload, ensure_ascii=False)}</script>
</div></section>'''


def siblings(p, products):
    key = family_of(p)
    group = [x for x in products if family_of(x) == key]
    group.sort(key=lambda x: x["name"])
    return group if len(group) > 1 else [p]
