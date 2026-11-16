"""Blocs qui vendent : performances sourcées, étude, pose, choix, différence AS974."""
from core import *
from diagrams import chaine, portee, ia, en54, frise, comparatif

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


def _src(*_links):
    return '<p class="src-note">Source : Ajax Systems</p>'


def band(title, short, more, visual, cta_html, alt=False):
    bg = " bg-off" if alt else ""
    extra = f'<details class="more"><summary>En savoir plus</summary><div class="more-body">{more}</div></details>' if more else ""
    return f'''<section class="section{bg}"><div class="wrap split-vis">
<div class="vis-copy"><h2 class="h2">{title}</h2>{short}{extra}{cta_html}</div>
<div class="vis-media">{visual}</div>
</div></section>'''


def performances(kind):
    if kind == "video":
        body = f'''<p>Ajax présente deux lignes, Baseline et Superior. Sur le catalogue Baseline, l’intelligence artificielle est intégrée aux caméras : elle reconnaît les personnes, les véhicules et les animaux, et peut lancer une réaction. Ajax indique aussi, pour cette ligne, un matériel conforme NDAA. Superior reprend cette base et ajoute, selon les modèles, une optique varifocal P-Iris, un haut-parleur et les enregistreurs NVR H2D. Ce n’est pas une promesse de zéro fausse alerte : le réglage des zones et le fait que le système soit armé se décident à l’étude.</p>
<p>La levée de doute ne concerne pas tous les détecteurs. Ajax indique, pour Hub 2 associé à MotionCam, une première photo en 9 secondes dans des conditions précises : résolution 320×240, signal à 2 ou 3 barres, centrale reliée en Ethernet ou en LTE. Un détecteur de mouvement sans photo n’envoie pas d’image.</p>'''
        src = _src(("catalogue Baseline", VID), ("catalogue Superior", VID_S), ("Hub 2", HUB))
    elif kind == "incendie":
        body = '''<p>Ajax décrit l’EN54 Line comme un système d’alarme et de détection incendie entièrement sans fil, pour les bâtiments commerciaux et municipaux. La centrale EN54 Fire Hub Jeweller est donnée pour EN 54-2, EN 54-4, EN 54-13, EN 54-21, EN 54-25 et EN 50131 Grade 2. Les détecteurs ponctuels de fumée et de chaleur, avec ou sans avertisseur, sont cités en EN 54-3, EN 54-5, EN 54-7 et EN 54-25. Les avertisseurs sonores et les dispositifs visuels (DAV) sont cités en EN 54-3, EN 54-23 et EN 54-25. Le module d’entrées-sorties est cité en EN 54-18 et EN 54-25. Le prolongateur EN54 Fire ReX est cité en EN 54-4, EN 54-18, EN 54-25 et EN 50131 Grade 2.</p>
<p>Ajax indique une alarme radio en moins de trois secondes vers les utilisateurs et un centre de télésurveillance, une portée jusqu’à 1 800 m, une communication bidirectionnelle chiffrée, et jusqu’à cinq prolongateurs. La centrale parle en Ethernet ou Wi-Fi, avec deux cartes SIM 2G/4G en secours. Le déclencheur manuel figure sur la même page : Ajax précise que seule la version rouge est certifiée EN 54-25. La détection de fumée s’appuie sur la chambre optique, un capteur à double spectre et l’algorithme HazeFlow 2, qui compare le signal à un modèle pour distinguer la fumée de la vapeur. Les diffuseurs annoncent un niveau de 100 dB, 32 tonalités, et un cadre lumineux rouge sur les versions visuelles.</p>'''
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
    visual = {"video": ia, "incendie": en54, "domotique": chaine, "acces": frise, "accessoires": chaine}.get(kind, portee)()
    short = "<p>Les chiffres du fabricant sont repris ici. Nous les vérifions chez vous avant le devis.</p>"
    return band("Performances annoncées.", short, src, visual, act(""))


def etude(kind):
    sujet = {
        "video": "les angles, la nuit et ce qui doit lancer l’alarme",
        "incendie": "le bâtiment, les circulations et les locaux techniques",
        "domotique": "les circuits, le neutre et les arrivées d’eau",
        "acces": "qui arme, et quelles zones se séparent",
        "alarme": "les accès, les volumes et la radio réelle",
    }.get(kind, "les accès et la façon dont le lieu est occupé")
    short = f"<p>Nous venons voir {sujet}. Le devis ne décrit que ce que le lieu demande.</p>"
    more = "<p>L’analyse porte sur les risques et les accès, pas sur une liste d’appareils à placer partout. Deux maisons voisines ne donnent pas le même chantier. Des photos peuvent préparer la visite. Elles ne remplacent pas un test radio.</p>"
    return band("L’étude se fait chez vous, avant le devis.", short, more, frise(), act("", "contact.html#devis", "Prendre rendez-vous pour l’étude"), True)


def pose(kind):
    short = "<p>Nous posons, nous testons, puis nous vous montrons comment armer, lire une alerte et repérer une pile faible.</p>"
    more = "<p>Les liaisons filaires et l’alimentation suivent le plan de l’étude. Les utilisateurs et les scénarios sont réglés avec vous. Le dépannage suit ce qui est écrit au devis. La télésurveillance, si vous la souhaitez, se discute à part. Elle n’est pas un service déjà ouvert.</p>"
    return band("La pose, le réglage, puis nous restons joignables.", short, more, frise(), act("", "services-installation.html", "Voir le déroulé de l’installation"))


def choix(products, pre, kind):
    n = len(products)
    colors = sorted({c for p in products for c in p.get("colors_ok") or []})
    col = ", ".join(colors) if colors else "les coloris indiqués sur chaque fiche"
    jew = sum(1 for p in products if "jeweller" in p["slug"] or "Jeweller" in p["name"])
    fib = sum(1 for p in products if "fibra" in p["slug"] or "Fibra" in p["name"])
    short = f"<p>Cette famille compte {n} références, dont {jew} en Jeweller et {fib} en Fibra. Chaque fiche montre uniquement les coloris documentés pour ce modèle.</p>"
    more = f"<p>Coloris rencontrés ici : {E(col)}. Le sélecteur de version ouvre les autres optiques, formats ou alimentations de la même famille. On agrandit le système dans la même application, sans changer de marque.</p>"
    return band("Le choix se fait dans le catalogue, pas dans deux coloris imposés.", short, more, ia(), act(pre, "contact.html#devis", "Demander un devis sur cette sélection"), True)


def pourquoi(kind, pre=""):
    short = "<p>Nous venons, nous chiffrons le système installé, puis nous le posons. Pas de classement, pas de nombre de clients, pas d’avis inventé.</p>"
    more = "<p>Un kit vous laisse le plan et les tests. Un installateur multimarque couvre plusieurs catalogues. Certaines offres lient le matériel à un abonnement. Ici, le devis porte d’abord sur l’installation. La télésurveillance, si vous la voulez, se discute à part et n’est pas un service déjà ouvert.</p>"
    return band("Pourquoi choisir Active Sécurité 974.", short, more, comparatif(), act(pre))


def index_produits(products, pre, titre="Toutes les références, pour choisir puis demander un devis."):
    items = []
    for p in products:
        cols = ", ".join(p["colors_ok"]) if p["colors_ok"] else "coloris à préciser au devis"
        feat = p["feats"][0] if p["feats"] else p["category"]
        items.append(
            f'<li><a href="{pre}produits/{p["slug"]}.html">{E(p["name"])}</a>'
            f'<span>Réf. {E(p["model"])} · {E(cols)}. {E(feat)}</span></li>'
        )
    return f'''<section class="section bg-off" id="references-gamme"><div class="wrap split-vis">
<div class="vis-copy"><h2 class="h2">{E(titre)}</h2>
<p>Ouvrez la liste, choisissez une fiche, puis le coloris. Le devis reprend exactement ce choix.</p>
<details class="more"><summary>En savoir plus</summary><ul class="ref-index">{"".join(items)}</ul></details>
{act(pre, "contact.html#devis", "Décrire mon besoin")}
</div>
<div class="vis-media">{chaine()}</div>
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
<div class="prose"><p>Choisissez le nombre de postes, le modèle et le coloris. La composition part dans le devis, sans prix.</p>
<details class="more"><summary>En savoir plus</summary><p>Huit teintes de panneau. Un poste seul se pose sans cadre. Les cadres existent en 2, 3, 4 et 5 postes. Ajax ne publie pas, dans les fichiers repris ici, une photo de cadre à trois postes seule. Les prises ne se combinent qu’à l’horizontale.</p></details>
<div class="cfg-official">
<img src="assets/img/ajax/ls_all_frames_f90723c216.jpg" alt="Cadres LightSwitch publiés par Ajax">
<img src="assets/img/ajax/ls_1_gang_27a92c6cc4.jpg" alt="Un poste, visuel officiel">
<img src="assets/img/ajax/ls_two_devices_d98e7ef76a.jpg" alt="Deux commandes, visuel officiel">
<img src="assets/img/ajax/ls_four_devices_7d8b0f118d.jpg" alt="Quatre postes, visuel officiel">
<img src="assets/img/ajax/ls_five_devices_3b8296cb8d.jpg" alt="Cinq postes, visuel officiel">
</div>
<p class="src-note">Source : Ajax Systems</p></div>
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
