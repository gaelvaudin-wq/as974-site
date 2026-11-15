"""Pages éditoriales (textes repris des pages v1 validées, mise en page refondue)."""
from core import *
from layout import write_page, crumbs
from components import card, rail, filter_grid, cta, versus

P = {}      # slug -> produit
ALL = []

def init(products):
    global ALL
    ALL = products
    for p in products: P[p["slug"]] = p

def pick(slugs):
    return [P[s] for s in slugs if s in P]

def stage_img(slug, color, pre, sizes, eager=False, need_alpha=False):
    p = P[slug]
    meta = color_image(p, color) if color else default_image(p)
    if need_alpha and meta and meta["opaque"]:
        for c in p["colors_ok"]:
            m = color_image(p, c)
            if not m["opaque"]: meta = m; break
    alt = p["name"] + (f" — coloris {color}" if color else "")
    return picture(meta, alt, pre, sizes, eager=eager)

def group_products(g):
    return [p for p in ALL if p["group"] == g]

def fill(group, gk, first, n=8):
    lst = [P[s] for s in first if s in P and P[s]["group"] == group]
    for p in ALL:
        if len(lst) >= n: break
        if p["group"] == group and p["gk"] == gk and p not in lst and not p["avail_tag"] and default_image(p):
            lst.append(p)
    return lst[:n]

SZ_HERO = "(max-width:640px) 40vw, 420px"
SZ_SPLIT = "(max-width:980px) 80vw, 520px"

# ====================================================================== ACCUEIL
def home():
    pre = ""
    n = len(ALL)
    hero = f'''<section class="hero on-dark">
<div class="wrap">
<p class="eyebrow reveal">Partenaire agréé Ajax Systems · Toute l’île</p>
<h1 class="display reveal d1">Sécurisez votre espace à La Réunion avec <span class="grad-text">Active Sécurité 974</span></h1>
<p class="lead reveal d2">Alarme intrusion, incendie, vidéosurveillance et domotique : un écosystème cohérent, installé et suivi sur toute l’île. Matériel Ajax Systems, marque partenaire.</p>
<div class="btns reveal d3" style="justify-content:center"><a class="btn btn-primary btn-lg" href="contact.html#devis">Demander mon devis gratuit</a><a class="btn btn-outline btn-lg" href="#pourquoi">Pourquoi Ajax Systems</a></div>
</div>
<div class="hero-visual reveal d2" aria-hidden="false">
<figure>{stage_img("motioncam-phod", "Blanc", pre, SZ_HERO, eager=True, need_alpha=True)}</figure>
<figure>{stage_img("hub-2", "Blanc", pre, "(max-width:640px) 46vw, 520px", eager=True, need_alpha=True)}</figure>
<figure>{stage_img("keypad-touchscreen", "Blanc", pre, SZ_HERO, eager=True, need_alpha=True)}</figure>
</div>
<div class="wrap"><div class="hero-badges"><span>Étude et devis gratuits</span><span>Intervention chez vous, partout sur l’île</span><span>{n} références sur devis</span></div></div>
<div class="hero-floor"></div>
</section>'''

    value = f'''<section class="section"><div class="wrap">
<p class="eyebrow reveal">Proposition de valeur</p>
<p class="statement reveal">Concevoir, installer, accompagner. <span class="dim">Active Sécurité 974 conçoit, installe et accompagne des systèmes de sécurité modernes pour particuliers et professionnels à La Réunion — de Baseline à Superior.</span></p>
<ul class="ticks reveal">
<li>Une seule interface pour alarme, vidéo, incendie et automatismes</li>
<li>Étude et devis gratuits, sans engagement</li>
<li>Intervention sur toute l’île de La Réunion</li>
<li>Conseil, pose, formation à l’usage, suivi</li>
</ul>
</div></section>'''

    why = f'''<section class="section bg-ink on-dark" id="pourquoi"><div class="wrap">
<div class="head reveal"><p class="eyebrow">Pourquoi Ajax Systems</p><h2 class="h2">Des avantages techniques vérifiés.</h2>
<p class="lead">Faits repris du site du fabricant (ajax.systems), reformulés. Chiffres uniquement lorsqu’ils y figurent.</p></div>
<div class="bento">
<div class="tile w4 reveal"><p class="fig red">2 000<small>m</small></p><h3>Radio Jeweller longue portée</h3><p>Jusqu’à 2 000 m de communication radio avec une centrale ou un prolongateur de portée, protocole bidirectionnel chiffré.</p><p class="src">Source : ajax.systems/fr/products/hub-2/</p></div>
<div class="tile w2 reveal d1"><p class="fig yellow">3<small>réseaux</small></p><h3>Multi-canal, toujours connecté</h3><p>Ethernet + deux cartes SIM (2G/3G/LTE) : jusqu’à trois réseaux indépendants, bascule automatique.</p><p class="src">Source : ajax.systems/fr/products/hub-2/</p></div>
<div class="tile w2 reveal"><p class="fig">~9<small>s</small></p><h3>Photo-vérification</h3><p>Levée de doute en photos : première image en ~9 s selon les conditions indiquées sur les fiches Hub 2 / MotionCam.</p><p class="src">Source : ajax.systems/fr/products/hub-2/ &amp; motioncam-phod/</p></div>
<div class="tile w2 reveal d1"><p class="fig blue">5<small>ans</small></p><h3>Autonomie des piles</h3><p>Ex. MotionProtect : jusqu’à 5 ans d’autonomie (annonce constructeur) ; piles préinstallées sur de nombreux détecteurs.</p><p class="src">Source : ajax.systems/fr/products/motionprotect/</p></div>
<div class="tile w2 reveal d2"><p class="fig" style="font-size:clamp(40px,4vw,60px)">Anti&#8209;<br>sabotage</p><h3>Immunité animaux &amp; protection</h3><p>Algorithmes d’immunité aux animaux de compagnie ; boutons anti-sabotage et chiffrement des échanges radio.</p><p class="src">Source : ajax.systems/fr/products/motionprotect/ &amp; motioncam-phod/</p></div>
<div class="tile w6 with-img reveal"><div class="tile-txt"><p class="fig" style="font-size:clamp(40px,4.4vw,68px)">Une app.<br>Tout l’écosystème.</p><h3>App + OS Malevich</h3><p>Pilotage smartphone / PC ; OS Malevich avec mises à jour OTA. Écosystème unifié : alarme, vidéo, incendie, domotique.</p><p class="src">Source : ajax.systems/fr/products/hub-2/</p></div>{stage_img("hub-2", "Noir", pre, "(max-width:640px) 70vw, 300px", need_alpha=True)}</div>
</div>
</div></section>'''

    duo = f'''<section class="section"><div class="wrap-wide">
<div class="head center reveal"><p class="eyebrow">Pour qui</p><h2 class="h2">Particuliers &amp; professionnels.</h2></div>
<div class="duo">
<div class="panel light reveal"><p class="eyebrow">Particuliers</p><h3 class="h2">Votre maison, sereine.</h3><p>Maison ou appartement : une solution discrète, fiable, pilotable depuis le smartphone.</p>
<div class="btns"><a class="btn btn-primary" href="contact.html?profil=particulier#devis">Étude gratuite pour mon logement</a><a class="btn btn-outline" href="particuliers.html">En savoir plus</a></div>
<div class="panel-img">{stage_img("doorbell", "Blanc", pre, "(max-width:980px) 60vw, 360px", need_alpha=True)}</div></div>
<div class="panel blue on-dark reveal d1"><p class="eyebrow">Professionnels</p><h3 class="h2">Votre activité, protégée.</h3><p>Commerces, bureaux, entrepôts, multi-sites : architecture évolutive, options Superior.</p>
<div class="btns"><a class="btn btn-light" href="contact.html?profil=professionnel#devis">Demander une étude professionnelle</a><a class="btn btn-outline" href="professionnels.html">En savoir plus</a></div>
<div class="panel-img">{stage_img("superior-motioncam-phod-jeweller", "Noir", pre, "(max-width:980px) 60vw, 360px", need_alpha=True)}</div></div>
</div></div></section>'''

    chapters = [
        ("alarme", "gamme-alarme.html", "Chaque accès sous contrôle.", "Détection d’intrusion, commandes et sirènes Ajax Systems. Baseline pour l’essentiel sans fil ; Superior pour les architectures plus exigeantes.", "motionprotect", "Blanc", ""),
        ("incendie", "gamme-incendie.html", "Détecter tôt. Alerter fort.", "Détecteurs de fumée, chaleur, CO et dispositifs associés. Pour les ERP, l’étude intègre vos contraintes sans affirmer une conformité non vérifiée.", "fireprotect-2-smoke-heat-co", "Blanc", ""),
        ("video", "gamme-video.html", "Voir, pour lever le doute.", "Caméras IP, sonnette et NVR Ajax Systems, intégrés à l’alarme pour une levée de doute visuelle.", "turretcam", "Noir", "dark"),
        ("domotique", "gamme-domotique.html", "Le confort, dans la même app.", "Automatismes, prises, relais, fuites d’eau et qualité de l’air : le confort dans la même application que la sécurité.", "lightswitch-1-gang-jeweller", "Olive", ""),
    ]
    rows = []
    for i, (g, href, h, txt, slug, col, st) in enumerate(chapters):
        cnt = len(group_products(g))
        rows.append(f'''<div class="split{' rev' if i % 2 else ''}">
<div class="split-media {st} reveal">{stage_img(slug, col, pre, SZ_SPLIT, need_alpha=(st == 'dark'))}</div>
<div class="split-txt reveal d1"><p class="num">0{i+1} — {E(GROUP[g]["label"])}</p><h2 class="h2">{h}</h2><p class="lead">{txt}</p>
<div class="btns"><a class="btn btn-dark" href="{href}">Découvrir la gamme</a><a class="btn btn-outline" href="catalogue-{g}.html">{cnt} références</a></div></div>
</div>''')
    gammes = f'''<section class="section bg-off" id="gammes"><div class="wrap">
<div class="head reveal"><p class="eyebrow">Gammes</p><h2 class="h2">Quatre univers. Un seul écosystème.</h2></div>
{"".join(rows)}
</div></section>'''

    vs = f'''<section class="section"><div class="wrap">
<div class="head reveal"><p class="eyebrow">Baseline ou Superior</p><h2 class="h2">Deux niveaux pour coller à votre site.</h2><p class="lead">De l’essentiel sans fil aux projets exigeants. Nous vous orientons lors de l’étude gratuite.</p></div>
{versus(pre, ALL, "catalogue.html?gamme=baseline#references", "catalogue.html?gamme=superior#references")}
</div></section>'''

    feat = pick(["hub-2", "motioncam-phod", "doorprotect", "bulletcam", "streetsiren", "keypad-touchscreen", "fireprotect-2-smoke-heat-co", "lightswitch-1-gang-jeweller", "doorbell"])
    railsec = f'''<section class="section flush-top"><div class="wrap">
{rail(feat, pre, "Catalogue", "Matériel sur devis.", ("catalogue.html", f"Voir tout le catalogue ({n} références)"), lead="Packshots officiels Ajax Systems. Chaque fiche propose « Demander un devis » : pas de panier ni de paiement en ligne.")}
</div></section>'''

    process = f'''<section class="section bg-off"><div class="wrap">
<div class="head reveal"><p class="eyebrow">Process</p><h2 class="h2">De la prise de contact au suivi.</h2></div>
<ol class="timeline reveal">
<li><span class="dot">01</span><div><h3>Contact</h3><p>Formulaire ou téléphone {biz("telephone", "téléphone")}.</p></div></li>
<li><span class="dot">02</span><div><h3>Étude gratuite</h3><p>Visite ou échanges à distance.</p></div></li>
<li><span class="dot">03</span><div><h3>Devis clair</h3><p>Sans engagement, prix sur devis.</p></div></li>
<li><span class="dot">04</span><div><h3>Installation</h3><p>Pose, configuration, formation.</p></div></li>
<li><span class="dot">05</span><div><h3>Suivi</h3><p>Options de maintenance <span class="ph">[À CONFIRMER]</span>.</p></div></li>
</ol>
</div></section>'''

    zone = f'''<section class="section bg-ink on-dark"><div class="wrap zone">
<div class="reveal"><p class="eyebrow">Zone d’intervention</p><h2 class="h2">Présents sur toute l’île.</h2><p class="lead" style="margin-top:24px">La Réunion, d’un bout à l’autre : Nord, Sud, Est, Ouest et Hauts. Un interlocuteur local pour l’étude, la pose et le suivi, chez vous.</p></div>
<ul class="zone-words reveal d1" aria-label="Secteurs couverts"><li>Nord</li><li>Est</li><li>Sud</li><li>Ouest</li><li>Hauts</li></ul>
</div></section>'''

    body = hero + value + why + duo + gammes + vs + railsec + process + zone + cta(pre, text=f"Étude et devis gratuits. Réponse sous {biz('delai_reponse', 'délai de réponse')}. Partenaire agréé Ajax Systems.")
    write_page("index.html", "Active Sécurité 974 — Alarme, vidéosurveillance, incendie et domotique à La Réunion",
               "Installateur partenaire agréé Ajax Systems à La Réunion : alarme, incendie, vidéosurveillance et domotique pour particuliers et professionnels. Étude et devis gratuits.",
               body, priority="1.0")

# ====================================================================== PARTICULIERS
def particuliers():
    pre = ""
    cr, ld = crumbs(pre, [(None, "Particuliers")])
    body = f'''<section class="phero"><div class="wrap phero-split">
<div class="reveal">{cr}<p class="eyebrow">Particuliers</p><h1 class="h1">Sécurité pour votre maison ou appartement à La Réunion.</h1>
<p class="lead">Solution discrète, fiable et pilotable depuis le smartphone : intrusion, alertes, vérification visuelle et scénarios du quotidien, adaptés à la vie sur l’île, y compris absences et résidences secondaires.</p>
<div class="btns"><a class="btn btn-primary btn-lg" href="contact.html?profil=particulier#devis">Étude gratuite pour mon logement</a><a class="btn btn-outline btn-lg" href="catalogue.html">Explorer le catalogue</a></div></div>
<div class="phero-media reveal d1">{stage_img("motionprotect", "Blanc", pre, SZ_SPLIT, eager=True)}</div>
</div></section>
<section class="section bg-off"><div class="wrap">
<div class="head reveal"><p class="eyebrow">Besoins typiques</p><h2 class="h2">Ce que nous protégeons chez vous.</h2></div>
<ol class="numlist reveal">
<li><h3>Maison &amp; appartement</h3><p>Ouvertures, volumes, abords. Pose soignée, esthétique discrète, formation à l’application.</p></li>
<li><h3>Résidences secondaires</h3><p>Alertes à distance, photo-vérification pour lever le doute sans vous déplacer inutilement.</p></li>
<li><h3>Absences prolongées</h3><p>Armement à distance, scénarios, suivi des événements, même depuis la métropole ou en voyage.</p></li>
<li><h3>Animaux de compagnie</h3><p>Détecteurs avec immunité animaux (selon modèles Ajax) pour limiter les fausses alertes.</p></li>
<li><h3>Application smartphone</h3><p>Armement, notifications, historique et pilotage dans l’application du fabricant.</p></li>
<li><h3>Photo-vérification</h3><p>MotionCam et équivalents : recevoir des photos en cas d’alarme pour évaluer la situation.</p></li>
</ol>
</div></section>
<section class="section"><div class="wrap">
<div class="split">
<div class="split-media dark reveal">{stage_img("motioncam-phod", "Noir", pre, SZ_SPLIT, need_alpha=True)}</div>
<div class="split-txt reveal d1"><p class="num">Photo-vérification</p><h2 class="h2">Une photo, pas seulement une alerte.</h2><p class="lead">En cas d’alarme, recevez des images pour évaluer la situation et lever le doute, sans vous déplacer inutilement.</p>
<div class="btns"><a class="btn btn-dark" href="produits/motioncam-phod.html">Voir MotionCam (PhOD)</a></div></div>
</div>
<div class="split rev">
<div class="split-media reveal">{stage_img("doorbell", "Graphite", pre, SZ_SPLIT)}</div>
<div class="split-txt reveal d1"><p class="num">Au quotidien</p><h2 class="h2">Tout, depuis votre smartphone.</h2><p class="lead">Armement, notifications, historique, vidéo et scénarios : une seule application pour toute la maison.</p>
<div class="btns"><a class="btn btn-dark" href="gamme-domotique.html">Découvrir la domotique</a></div></div>
</div>
</div></section>
<section class="section bg-off"><div class="wrap">
<div class="head reveal"><p class="eyebrow">Approche</p><h2 class="h2">Baseline pour l’essentiel, Superior si besoin.</h2><p class="lead">Pour la plupart des logements, la gamme Baseline (sans fil) couvre l’essentiel. Projet plus exigeant : étude Superior.</p></div>
{versus(pre, None, "gamme-alarme.html", "catalogue.html?gamme=superior#references")}
</div></section>
<section class="section"><div class="wrap">
{rail(pick(["hub-2", "doorprotect", "motioncam-phod", "homesiren", "keypad-touchscreen", "doorbell", "fireprotect-2-smoke-heat-co", "leaksprotect"]), pre, "Produits phares", "Matériel souvent recommandé.", ("catalogue.html", "Tout le catalogue"))}
</div></section>
{cta(pre, "Étude gratuite pour votre logement.", "Intervention à domicile sur toute l’île — devis sans engagement.", href="contact.html?profil=particulier#devis")}'''
    write_page("particuliers.html", "Alarme maison et appartement à La Réunion — Particuliers | AS974",
               "Alarme sans fil, photo-vérification, vidéo et domotique pour votre maison ou appartement à La Réunion. Étude gratuite et installation à domicile par Active Sécurité 974.",
               body, jsonld=[ld], priority="0.9")

# ====================================================================== PROFESSIONNELS
def professionnels():
    pre = ""
    cr, ld = crumbs(pre, [(None, "Professionnels")])
    sup = pick(["superior-hub-g3-jeweller", "superior-hub-hybrid-2", "superior-doorprotect-g3-jeweller", "superior-keypad-touchscreen-g3-jeweller", "superior-motioncam-phod-jeweller", "superior-streetsiren-doubledeck-jeweller", "superior-motionprotect-g3-jeweller", "superior-homesiren-g3-jeweller"])
    body = f'''<section class="phero bg-blue on-dark"><div class="wrap phero-split">
<div class="reveal">{cr}<p class="eyebrow">Professionnels</p><h1 class="h1">Sécurité pour commerces, bureaux et multi-sites à La Réunion.</h1>
<p class="lead">Architectures évolutives, option Superior pour les projets exigeants, interlocuteur local pour l’étude, l’installation sur site et le suivi. Partenaire agréé Ajax Systems.</p>
<div class="btns"><a class="btn btn-light btn-lg" href="contact.html?profil=professionnel#devis">Demander une étude professionnelle</a><a class="btn btn-outline btn-lg" href="catalogue.html?gamme=superior#references">Gamme Superior</a></div></div>
<div class="phero-media blue reveal d1">{stage_img("superior-keypad-touchscreen-g3-jeweller", "Noir", pre, SZ_SPLIT, eager=True, need_alpha=True)}</div>
</div></section>
<section class="section"><div class="wrap">
<div class="head reveal"><p class="eyebrow">Cas d’usage</p><h2 class="h2">Des sites très différents, une même exigence.</h2></div>
<ol class="numlist reveal">
<li><h3>Commerces &amp; retail</h3><p>Ouvertures, volumes, abords, sirènes, vidéo pour lever le doute.</p></li>
<li><h3>Bureaux</h3><p>Multi-zones, horaires, utilisateurs multiples, scénarios d’armement.</p></li>
<li><h3>Entrepôts &amp; locaux techniques</h3><p>Périmètres, portées radio, extensions de couverture.</p></li>
<li><h3>Restaurants &amp; CHR</h3><p>Protection hors service, alertes, automatismes utiles au quotidien.</p></li>
<li><h3>Multi-sites</h3><p>Vision consolidée, interlocuteur unique AS974 sur toute l’île.</p></li>
<li><h3>Incendie (ERP / sites sensibles)</h3><p>Nous étudions les dispositifs Ajax adaptés. Les obligations réglementaires (ERP, etc.) sont analysées au cas par cas : aucune conformité n’est affirmée sans étude dédiée.</p></li>
</ol>
</div></section>
<section class="section bg-off"><div class="wrap">
<div class="split">
<div class="split-media reveal">{stage_img("superior-streetsiren-doubledeck-jeweller", "Blanc", pre, SZ_SPLIT)}</div>
<div class="split-txt reveal d1"><p class="num">Superior</p><h2 class="h2">Quand Superior a du sens.</h2><p class="lead">Sites multi-zones, exigences élevées, complément filaire : la ligne Superior s’adresse aux projets ambitieux.</p>
<div class="btns"><a class="btn btn-dark" href="catalogue.html?gamme=superior#references">{sum(1 for p in ALL if p["gk"] == "superior")} références Superior</a></div></div>
</div>
</div></section>
<section class="section"><div class="wrap">
{rail(sup, pre, "Sélection Superior", "Le matériel des projets exigeants.", ("catalogue.html?gamme=superior#references", "Toute la gamme Superior"))}
</div></section>
<section class="section bg-ink on-dark"><div class="wrap">
<p class="eyebrow reveal">Options</p>
<p class="statement reveal">Maintenance &amp; télésurveillance. <span class="dim">Maintenance selon contrat. Télésurveillance : option</span> <span class="ph">[À CONFIRMER]</span><span class="dim">.</span></p>
<div class="btns reveal"><a class="btn btn-light" href="services.html">Voir les services</a></div>
</div></section>
{cta(pre, "Parlons de votre site.", "Étude professionnelle sur place — toute l’île.", "Demander une étude professionnelle", "contact.html?profil=professionnel#devis")}'''
    write_page("professionnels.html", "Sécurité pour professionnels à La Réunion — commerces, bureaux, multi-sites | AS974",
               "Alarme, vidéosurveillance et incendie pour commerces, bureaux, entrepôts et multi-sites à La Réunion. Gamme Ajax Superior, étude sur site par Active Sécurité 974.",
               body, jsonld=[ld], priority="0.9")

# ====================================================================== GAMMES
GAMME_PAGES = {
    "alarme": ("gamme-alarme.html", "Alarme intrusion", "Détection d’intrusion, commandes et sirènes Ajax Systems. Baseline pour l’essentiel sans fil ; Superior pour les architectures plus exigeantes.",
               "motioncam-phod", "Noir", "dark", ["doorprotect", "motionprotect", "motioncam-phod", "keypad-touchscreen", "streetsiren", "combiprotect"],
               "Alarme intrusion sans fil Ajax à La Réunion — détecteurs, claviers, sirènes | AS974",
               "Alarme intrusion Ajax Systems à La Réunion : détecteurs de mouvement et d’ouverture, claviers, sirènes. Gammes Baseline et Superior, installation par AS974."),
    "incendie": ("gamme-incendie.html", "Incendie", "Détecteurs de fumée, chaleur, CO et dispositifs associés. Pour les ERP, l’étude intègre vos contraintes sans affirmer une conformité non vérifiée.",
                 "fireprotect-2-smoke-heat-co", "Blanc", "", ["fireprotect-2-smoke-heat-co", "fireprotect", "type4-manualcallpoint-jeweller", "fireprotect-2-rb-heat-smoke-co-ul-jeweller"],
                 "Détection incendie Ajax à La Réunion — fumée, chaleur, CO | AS974",
                 "Détecteurs incendie Ajax Systems à La Réunion : fumée, chaleur, monoxyde de carbone, déclencheurs manuels. Étude au cas par cas et installation par AS974."),
    "video": ("gamme-video.html", "Vidéosurveillance", "Caméras IP, sonnette et NVR Ajax Systems, intégrés à l’alarme pour une levée de doute visuelle.",
              "bulletcam", "Blanc", "dark", ["bulletcam", "turretcam", "domecam-mini", "doorbell", "nvr", "bulletcam-hl"],
              "Vidéosurveillance Ajax à La Réunion — caméras IP, NVR, sonnette | AS974",
              "Caméras IP, enregistreurs NVR et sonnette vidéo Ajax Systems intégrés à l’alarme. Vidéosurveillance sur devis et installation à La Réunion par AS974."),
    "domotique": ("gamme-domotique.html", "Domotique", "Automatismes, prises, relais, fuites d’eau et qualité de l’air : le confort dans la même application que la sécurité.",
                  "socket", "Blanc", "", ["socket", "wallswitch", "leaksprotect", "waterstop", "lifequality", "relay", "lightswitch-1-gang-jeweller"],
                  "Domotique Ajax à La Réunion — éclairage, prises, fuites d’eau | AS974",
                  "Domotique Ajax Systems à La Réunion : interrupteurs, prises connectées, relais, détection de fuite et qualité de l’air, dans la même application que l’alarme."),
}

def gamme(g):
    pre = ""
    path, label, lead, hslug, hcol, st, feat, title, desc = GAMME_PAGES[g]
    prods = group_products(g)
    cr, ld = crumbs(pre, [("catalogue.html", "Catalogue"), (None, "Gamme " + label)])
    cats = []
    for c in GROUP[g]["cats"]:
        n = sum(1 for p in prods if p["category"] == c)
        if n: cats.append((c, n))
    idx = "".join(f'<li><a href="catalogue-{g}.html?sous={slugify(c)}#references"><span>{E(c)}</span><span class="n">{n} réf.</span></a></li>' for c, n in cats)
    others = [(gk, sum(1 for p in prods if p["gk"] == gk)) for gk in ("residence", "en54", "type4", "a-confirmer")]
    others = [(gk, n) for gk, n in others if n]
    oth = ""
    if others:
        oth = '<p class="muted mt-28 reveal">Également au catalogue : ' + ", ".join(f'<a class="link" style="min-height:0" href="catalogue-{g}.html?gamme={gk}#references">{GAMME_LABEL[gk]} ({n})</a>' for gk, n in others) + ".</p>"
    base_rail = fill(g, "baseline", feat)
    sup_rail = fill(g, "superior", [])
    body = f'''<section class="phero"><div class="wrap phero-split">
<div class="reveal">{cr}<p class="eyebrow">Gamme</p><h1 class="h1">{E(label)}</h1>
<p class="lead">{lead}</p>
<div class="btns"><a class="btn btn-primary btn-lg" href="contact.html#devis">Demander un devis</a><a class="btn btn-outline btn-lg" href="catalogue-{g}.html">Voir les {len(prods)} références</a></div></div>
<div class="phero-media {st} reveal d1">{stage_img(hslug, hcol, pre, SZ_SPLIT, eager=True, need_alpha=(st == "dark"))}</div>
</div></section>
<section class="section"><div class="wrap">
<div class="head reveal"><p class="eyebrow">Baseline vs Superior</p><h2 class="h2">Choisir le bon niveau.</h2><p class="lead">La disponibilité Superior dépend des références et du projet. Orientation lors de l’étude gratuite.</p></div>
{versus(pre, prods, f"catalogue-{g}.html?gamme=baseline#references", f"catalogue-{g}.html?gamme=superior#references")}
{oth}
</div></section>
<section class="section bg-off"><div class="wrap">
{rail(base_rail, pre, "Baseline", "Sélection du catalogue AS974.", (f"catalogue-{g}.html?gamme=baseline#references", "Toutes les références Baseline"))}
</div></section>
{f'<section class="section"><div class="wrap">' + rail(sup_rail, pre, "Superior", "Pour aller plus loin.", (f"catalogue-{g}.html?gamme=superior#references", "Toutes les références Superior")) + '</div></section>' if sup_rail else ''}
<section class="section{' bg-off' if not sup_rail else ' bg-off'}"><div class="wrap">
<div class="head reveal"><p class="eyebrow">Dans cette gamme</p><h2 class="h2">Tous les types de produits.</h2></div>
<ul class="index-list reveal">{idx}</ul>
</div></section>
{cta(pre)}'''
    write_page(path, title, desc, body, jsonld=[ld], priority="0.8")

# ====================================================================== CATALOGUE
CAT_LEADS = {
    "centrales": "Le cœur de votre système Ajax Systems : centrales, kits et prolongateurs de portée. Dimensionnés et installés par Active Sécurité 974 sur toute l’île.",
    "alarme": "Détecteurs, claviers, sirènes et commandes. Baseline pour l’essentiel sans fil ; Superior pour les projets exigeants.",
    "incendie": "Détecteurs et dispositifs de signalisation Ajax Systems. Pour les ERP et sites professionnels, étude au cas par cas : aucune conformité réglementaire non vérifiée n’est affirmée.",
    "video": "Caméras, sonnette et NVR Ajax Systems, intégrés à l’écosystème alarme, sur devis et installation AS974.",
    "domotique": "Prises, relais, éclairage, détection de fuite et qualité de l’air : automatisez le quotidien dans la même application.",
    "accessoires": "Modules d’intégration, alimentations, boîtiers et accessoires de pose pour compléter et raccorder votre installation.",
}
CAT_IMG = {"centrales": ("hub2-plus", "Noir"), "alarme": ("keypad-touchscreen", "Noir"), "incendie": ("fireprotect-2-smoke-heat-co", "Blanc"),
           "video": ("turretcam", "Blanc"), "domotique": ("lightswitch-1-gang-jeweller", "Ivoire"), "accessoires": ("button", "Blanc")}

def catalogue_index():
    pre = ""
    cr, ld = crumbs(pre, [(None, "Catalogue")])
    layout = [("alarme", "w4 dark"), ("centrales", "w2"), ("video", "w3"), ("incendie", "w3"), ("domotique", "w3"), ("accessoires", "w3")]
    tiles = []
    for i, (g, cls) in enumerate(layout):
        s, c = CAT_IMG[g]
        n = len(group_products(g))
        tiles.append(f'''<article class="chap {cls} reveal{' d1' if i % 2 else ''}"><h3><a class="cover" href="catalogue-{g}.html">{E(GROUP[g]["label"])}</a></h3><p>{E(GROUP[g]["intro"])}</p><p class="count">{n} références →</p>
<div class="chap-img">{stage_img(s, c, pre, "(max-width:640px) 70vw, 360px", need_alpha=("dark" in cls))}</div></article>''')
    body = f'''<section class="phero"><div class="wrap">
<div class="reveal">{cr}<p class="eyebrow">Catalogue</p><h1 class="h1">Matériel Ajax Systems,<br>sur devis.</h1>
<p class="lead">Explorez {len(ALL)} références officielles. Chaque fiche propose « Demander un devis » : pas de panier ni de paiement en ligne. Installation sur toute l’île par Active Sécurité 974, partenaire agréé.</p>
<div class="btns"><a class="btn btn-dark btn-lg" href="#references">Parcourir toutes les références</a></div></div>
</div></section>
<section class="section flush-top"><div class="wrap-wide"><div class="mosaic">{"".join(tiles)}</div></div></section>
<section class="section bg-off"><div class="wrap">
<div class="head reveal"><p class="eyebrow">Comment ça marche</p><h2 class="h2">Du catalogue au devis.</h2></div>
<ol class="numlist reveal">
<li><h3>Explorer</h3><p>Parcourez les univers et les fiches, filtrez par gamme, type ou coloris.</p></li>
<li><h3>Sélectionner</h3><p>Ajoutez des produits à votre sélection devis, avec le coloris souhaité.</p></li>
<li><h3>Échanger</h3><p>Nous établissons l’étude et le devis — intervention chez vous.</p></li>
</ol>
</div></section>
<section class="section" id="references"><div class="wrap">
<div class="head reveal"><p class="eyebrow">Toutes les références</p><h2 class="h2">Trouvez le bon matériel.</h2></div>
{filter_grid(ALL, pre, with_group=True)}
</div></section>
{cta(pre, "Prêt à composer votre système ?", f"Un conseiller AS974 vous répond sous {biz('delai_reponse', 'délai de réponse')}.")}'''
    itemlist = {"@context": "https://schema.org", "@type": "CollectionPage", "name": "Catalogue Active Sécurité 974", "url": SITE + "/catalogue.html",
                "hasPart": [{"@type": "CollectionPage", "name": GROUP[g]["label"], "url": f"{SITE}/catalogue-{g}.html"} for g in GROUP]}
    write_page("catalogue.html", f"Catalogue Ajax Systems sur devis — {len(ALL)} références | AS974",
               f"Catalogue de {len(ALL)} références Ajax Systems : centrales, alarme, incendie, vidéosurveillance, domotique, accessoires. Sur devis, installation à La Réunion.",
               body, jsonld=[ld, itemlist], priority="0.9")

def catalogue_cat(g):
    pre = ""
    prods = group_products(g)
    label = GROUP[g]["label"]
    cr, ld = crumbs(pre, [("catalogue.html", "Catalogue"), (None, label)])
    chips = "".join(f'<a class="chip" href="?sous={slugify(c)}#references">{E(c)}<span class="n">{sum(1 for p in prods if p["category"] == c)}</span></a>' for c in GROUP[g]["cats"] if any(p["category"] == c for p in prods))
    gl = {"alarme": "gamme-alarme.html", "incendie": "gamme-incendie.html", "video": "gamme-video.html", "domotique": "gamme-domotique.html"}.get(g)
    s, c = CAT_IMG[g]
    body = f'''<section class="phero"><div class="wrap phero-split">
<div class="reveal">{cr}<p class="eyebrow">Catalogue</p><h1 class="h1">{E(label)}</h1>
<p class="lead">{CAT_LEADS[g]}</p>
<div class="chips mt-28">{chips}</div>
{f'<p class="mt-24"><a class="link" href="{gl}">Découvrir la gamme {E(label)}</a></p>' if gl else ''}</div>
<div class="phero-media reveal d1">{stage_img(s, c, pre, SZ_SPLIT, eager=True)}</div>
</div></section>
<section class="section flush-top" id="references"><div class="wrap">
{filter_grid(prods, pre)}
</div></section>
{cta(pre, "Besoin d’aide pour composer votre système ?", "Étude gratuite · Partenaire agréé · Toute l’île · Intervention sur site.", "Demander un devis")}'''
    write_page(f"catalogue-{g}.html", f"{label} — catalogue Ajax Systems sur devis ({len(prods)} réf.) | AS974",
               clip(f"{label} : {len(prods)} références Ajax Systems sur devis. {GROUP[g]['intro']} Installation par Active Sécurité 974 à La Réunion."),
               body, jsonld=[ld], priority="0.8")

# ====================================================================== SERVICES / À PROPOS
def services():
    pre = ""
    cr, ld = crumbs(pre, [(None, "Services")])
    body = f'''<section class="phero"><div class="wrap">
<div class="reveal">{cr}<p class="eyebrow">Services</p><h1 class="h1">Étude, installation, suivi.</h1>
<p class="lead">Active Sécurité 974 vous accompagne de l’analyse du besoin à la mise en service chez vous, sur toute l’île.</p></div>
</div></section>
<section class="section flush-top"><div class="wrap">
<div class="split">
<div class="split-media reveal">{stage_img("hub2-plus", "Blanc", pre, SZ_SPLIT)}</div>
<div class="split-txt reveal d1"><p class="num">01 — Étude &amp; devis gratuit</p><h2 class="h2">Comprendre avant de proposer.</h2><p class="lead">Visite à domicile / sur site ou échanges à distance. Livrables clairs, sans engagement. Pas de tarifs inventés sur le site.</p>
<div class="btns"><a class="btn btn-primary" href="contact.html#devis">Prendre rendez-vous d’étude</a></div></div>
</div>
<div class="split rev">
<div class="split-media dark reveal">{stage_img("keypad-touchscreen", "Noir", pre, SZ_SPLIT, need_alpha=True)}</div>
<div class="split-txt reveal d1"><p class="num">02 — Installation</p><h2 class="h2">Une pose soignée, chez vous.</h2><p class="lead">Pose, paramétrage, tests radio, formation à l’application, documentation. Intervention chez le client.</p>
<div class="btns"><a class="btn btn-primary" href="contact.html#devis">Planifier mon installation</a></div></div>
</div>
<div class="split">
<div class="split-media reveal">{stage_img("streetsiren", "Blanc", pre, SZ_SPLIT)}</div>
<div class="split-txt reveal d1"><p class="num">03 — Maintenance / télésurveillance</p><h2 class="h2">Un suivi dans la durée.</h2><p class="lead">Maintenance préventive et intervention selon contrat. Télésurveillance : option {telesurv()}, non présentée comme active tant qu’elle n’est pas validée.</p>
<div class="btns"><a class="btn btn-outline" href="contact.html#devis">Me renseigner sur les options</a></div></div>
</div>
</div></section>
{cta(pre, "Prêt à démarrer ?", "Étude et devis gratuits sur toute l’île.")}'''
    write_page("services.html", "Services : étude, installation, maintenance — Active Sécurité 974",
               "Étude et devis gratuits, installation et paramétrage, maintenance selon contrat : Active Sécurité 974 vous accompagne chez vous, partout à La Réunion.",
               body, jsonld=[ld], priority="0.7")

def a_propos():
    pre = ""
    cr, ld = crumbs(pre, [(None, "À propos")])
    body = f'''<section class="phero"><div class="wrap">
<div class="reveal">{cr}<p class="eyebrow">À propos</p><h1 class="h1">Active Sécurité 974, votre installateur à La Réunion.</h1>
<p class="lead">Partenaire agréé Ajax Systems. Notre mission : devenir l’installateur de référence des systèmes Ajax Systems (marque partenaire) sur toute l’île, avec conseil, pose soignée et suivi.</p></div>
</div></section>
<section class="section bg-ink on-dark"><div class="wrap">
<p class="statement reveal">Un interlocuteur local. <span class="dim">Nord, Sud, Est, Ouest et Hauts : nous venons chez vous, de l’étude au suivi.</span></p>
</div></section>
<section class="section"><div class="wrap">
<div class="head reveal"><p class="eyebrow">Nos engagements</p><h2 class="h2">Ce qui nous guide.</h2></div>
<ol class="numlist reveal">
<li><h3>Ancrage local</h3><p>Intervention Nord, Sud, Est, Ouest et Hauts. Nous venons chez vous.</p></li>
<li><h3>Approche conseil</h3><p>Baseline ou Superior selon le site : pas de survente, devis clair.</p></li>
<li><h3>Matériel partenaire</h3><p>Ajax Systems, marque partenaire. Packshots et références officielles.</p></li>
<li><h3>Équipe</h3><p>{ph("présentation de l’équipe / photos avec droits")}</p></li>
<li><h3>Ma Protection IA</h3><p>Relation éventuelle : {ph("lien avec Ma Protection IA")}</p></li>
<li><h3>Transparence</h3><p>Aucun faux avis, chiffre ou certification sur ce site.</p></li>
</ol>
</div></section>
{cta(pre, "Discutons de votre projet.", "Contactez Active Sécurité 974.")}'''
    write_page("a-propos.html", "À propos — Active Sécurité 974, installateur Ajax Systems à La Réunion",
               "Active Sécurité 974, partenaire agréé Ajax Systems : conseil, pose soignée et suivi des systèmes de sécurité chez vous, sur toute l’île de La Réunion.",
               body, jsonld=[ld], priority="0.6")

# ====================================================================== CONTACT
def contact():
    pre = ""
    cr, ld = crumbs(pre, [(None, "Contact & devis")])
    action = CFG.get("form_action") or "[À COMPLÉTER]"
    mailto = CFG.get("form_mailto") or "[À COMPLÉTER]"
    body = f'''<section class="phero" style="padding-bottom:clamp(40px,5vw,72px)"><div class="wrap">
<div class="reveal">{cr}<p class="eyebrow">Contact &amp; devis</p><h1 class="h1">Contactez Active Sécurité 974.</h1>
<p class="lead">Parlez-nous de votre projet : maison, appartement, commerce ou site professionnel. Première analyse, puis visite sur site si besoin pour l’étude gratuite. Intervention sur toute l’île de La Réunion, chez vous.</p></div>
</div></section>
<section class="section flush-top" id="devis"><div class="wrap contact-grid">
<div>
<div class="prefill" id="prefill" role="status"></div>
<!-- Formspree : remplacer action (config form_action) par l’URL https://formspree.io/f/xxxx. Tant que l’action n’est pas une URL, le formulaire ouvre un mailto de repli (config form_mailto). -->
<form class="form" id="form-devis" name="devis" method="POST" action="{E(action)}" data-mailto="{E(mailto)}" data-formspree="{E(action)}">
<input type="hidden" name="_subject" value="Demande de devis — Active Sécurité 974">
<p class="hp"><label>Ne pas remplir : <input name="_gotcha" tabindex="-1" autocomplete="off"></label></p>
<div><label for="f-nom">Nom et prénom <span class="req" aria-hidden="true">*</span></label><input id="f-nom" name="nom" autocomplete="name" required placeholder="Votre nom"></div>
<div><label for="f-email">E-mail <span class="req" aria-hidden="true">*</span></label><input id="f-email" name="email" type="email" autocomplete="email" required placeholder="vous@exemple.fr"></div>
<div><label for="f-tel">Téléphone <span class="req" aria-hidden="true">*</span></label><input id="f-tel" name="telephone" type="tel" autocomplete="tel" required placeholder="0692 …"></div>
<div><label for="f-commune">Commune <span class="req" aria-hidden="true">*</span></label><input id="f-commune" name="commune" autocomplete="address-level2" required placeholder="Saint-Denis, Saint-Pierre…"></div>
<div><label for="f-profil">Profil <span class="req" aria-hidden="true">*</span></label><select id="f-profil" name="profil" required><option value="Particulier">Particulier</option><option value="Professionnel">Professionnel</option></select></div>
<div><label for="f-site">Type de site <span class="req" aria-hidden="true">*</span></label><select id="f-site" name="type_site" required><option>Maison</option><option>Appartement</option><option>Commerce</option><option>Bureau</option><option>Entrepôt</option><option>Restaurant / CHR</option><option>Autre</option></select></div>
<fieldset class="full" style="border:0"><legend class="lbl">Besoins</legend>
<div class="checks">
<label><input type="checkbox" name="besoins" value="Intrusion"> Intrusion</label>
<label><input type="checkbox" name="besoins" value="Incendie"> Incendie</label>
<label><input type="checkbox" name="besoins" value="Vidéo"> Vidéo</label>
<label><input type="checkbox" name="besoins" value="Domotique"> Domotique</label>
<label><input type="checkbox" name="besoins" value="Maintenance"> Maintenance</label>
<label><input type="checkbox" name="besoins" value="Télésurveillance"> Télésurveillance</label>
</div></fieldset>
<div class="full"><label for="f-gamme-souhaitee">Gamme souhaitée</label><select id="f-gamme-souhaitee" name="gamme"><option>Je ne sais pas</option><option>Baseline</option><option>Superior</option></select></div>
<div class="full"><label for="f-produits">Produits du catalogue (sélection)</label><textarea id="f-produits" name="produits" rows="4" placeholder="Prérempli depuis le catalogue : modèle, référence et coloris."></textarea></div>
<div class="full"><label for="f-message">Message</label><textarea id="f-message" name="message" placeholder="Décrivez brièvement votre besoin, vos disponibilités…"></textarea></div>
<div class="full"><label class="consent"><input type="checkbox" name="consentement" value="oui" required> <span>J’accepte que mes données soient utilisées pour répondre à ma demande, conformément à la <a href="politique-confidentialite.html">politique de confidentialité</a>. <span class="req" aria-hidden="true">*</span></span></label></div>
<div class="full"><button class="btn btn-primary btn-lg" type="submit">Envoyer ma demande de devis</button>
<p class="form-note">Nous vous répondons sous {biz("delai_reponse", "délai de réponse")}, {biz("horaires", "horaires d’ouverture")}. Champs obligatoires <span class="req">*</span>. Tant que l’adresse du formulaire n’est pas renseignée, l’envoi ouvre votre messagerie (destinataire {E(mailto)}).</p></div>
</form>
</div>
<aside class="aside on-dark" aria-label="Coordonnées">
<h2>Active Sécurité 974</h2>
<p>Partenaire agréé Ajax Systems. Interventions à domicile / sur site, sur toute l’île.</p>
<dl>
<dt>Adresse</dt><dd>{biz("adresse", "adresse")}</dd>
<dt>Téléphone</dt><dd>{biz("telephone", "téléphone")}</dd>
<dt>E-mail</dt><dd>{biz("email", "e-mail")}</dd>
<dt>SIRET</dt><dd>{biz("siret", "SIRET")}</dd>
<dt>Zone</dt><dd>Toute l’île de La Réunion (Nord, Sud, Est, Ouest, Hauts)</dd>
</dl>
<div class="sl-box"><h3>Votre sélection devis</h3><ul class="sl-list" id="sl-list"><li>Aucun produit pour l’instant.</li></ul>
<p style="margin-top:12px"><a class="link" href="catalogue.html">Ajouter depuis le catalogue</a></p></div>
</aside>
</div></section>'''
    write_page("contact.html", "Contact et demande de devis gratuit — Active Sécurité 974",
               "Demandez votre devis gratuit : alarme, vidéosurveillance, incendie ou domotique Ajax Systems. Intervention chez vous sur toute l’île de La Réunion.",
               body, jsonld=[ld], priority="0.9")
    body2 = f'''<section class="phero notfound"><div class="wrap center">
<p class="eyebrow">Demande envoyée</p><h1 class="h1">Merci, votre demande est bien partie.</h1>
<p class="lead" style="margin:28px auto 0">Un conseiller Active Sécurité 974 revient vers vous sous {biz("delai_reponse", "délai de réponse")}.</p>
<div class="btns" style="justify-content:center"><a class="btn btn-dark btn-lg" href="index.html">Retour à l’accueil</a><a class="btn btn-outline btn-lg" href="catalogue.html">Explorer le catalogue</a></div>
</div></section>'''
    write_page("merci.html", "Merci — demande de devis envoyée | AS974", "Votre demande de devis a bien été transmise à Active Sécurité 974.", body2, noindex=True)

# ====================================================================== LÉGAL
def legal_page(path, title, h1, note, inner, desc):
    pre = ""
    cr, ld = crumbs(pre, [(None, h1)])
    body = f'''<section class="phero" style="padding-bottom:clamp(40px,5vw,64px)"><div class="wrap">{cr}<p class="eyebrow">Informations légales</p><h1 class="h1" style="font-size:clamp(36px,4.4vw,60px)">{h1}</h1>
<div class="notice">{note}</div></div></section>
<section class="section flush-top"><div class="wrap"><div class="prose">{inner}</div></div></section>'''
    write_page(path, title, desc, body, jsonld=[ld], priority="0.3")

def legal():
    h = CFG["hebergeur"]
    legal_page("mentions-legales.html", "Mentions légales — Active Sécurité 974", "Mentions légales",
               "Texte à faire relire par un conseil avant mise en ligne. Placeholders uniquement, aucune donnée inventée. Pas de CGV e-commerce (catalogue + devis seulement).",
               f'''<h2>Éditeur</h2>
<p><strong>Active Sécurité 974</strong> (AS974)<br>
Forme juridique : {biz("forme_juridique", "forme juridique")}<br>
Raison sociale : {biz("raison_sociale", "raison sociale")}<br>
Capital : {biz("capital", "capital social")}<br>
SIRET : {biz("siret", "SIRET")}<br>
RCS : {biz("rcs", "RCS")}<br>
Adresse : {biz("adresse", "adresse")}<br>
Téléphone : {biz("telephone", "téléphone")} · E-mail : {biz("email", "e-mail")}<br>
Directeur de la publication : {biz("directeur_publication", "directeur de la publication")}<br>
Site : {E(SITE) if "[DOMAINE]" not in SITE else ph("domaine")}</p>
<h2>Hébergeur</h2>
<p>{E(h["nom"]) if h["nom"] else ph("hébergeur")} — {E(h["adresse"]) if h["adresse"] else ph("adresse de l’hébergeur")} — {E(h["contact"]) if h["contact"] else ph("contact de l’hébergeur")}</p>
<h2>Propriété intellectuelle</h2>
<p>La marque Active Sécurité 974 / AS974 et les contenus originaux du site sont protégés. Les noms, logos et visuels Ajax Systems appartiennent à leurs titulaires ; utilisation dans le cadre du partenariat agréé et des autorisations accordées.</p>
<h2>Responsabilité</h2>
<p>Les informations sont fournies à titre indicatif. Les devis et prestations font l’objet d’échanges personnalisés. Aucune vente en ligne n’est proposée sur ce site. Les coloris affichés sont ceux documentés par le fabricant ; leur disponibilité à La Réunion est confirmée lors du devis.</p>''',
               "Mentions légales du site Active Sécurité 974 (AS974) : éditeur, hébergeur, propriété intellectuelle et responsabilité.")
    legal_page("politique-confidentialite.html", "Politique de confidentialité — Active Sécurité 974", "Politique de confidentialité",
               "Document RGPD à faire relire avant mise en ligne. Placeholders pour les durées et contacts.",
               f'''<h2>Responsable de traitement</h2>
<p>Active Sécurité 974 — {biz("adresse", "adresse")} — {biz("email", "e-mail")} — {biz("telephone", "téléphone")}</p>
<h2>Données collectées</h2>
<p>Via le formulaire de demande de devis : identité, coordonnées, commune, profil, type de site, besoins, message, produits du catalogue éventuellement sélectionnés (modèle, référence, coloris), consentement.</p>
<h2>Finalités</h2>
<p>Répondre aux demandes de devis et d’information ; organiser l’étude et l’installation ; suivi commercial lié à votre demande.</p>
<h2>Base légale</h2>
<p>Mesures précontractuelles / intérêt légitime / consentement (case du formulaire).</p>
<h2>Durée de conservation</h2>
<p>{ph("durée de conservation, ex. durée après le dernier échange")}</p>
<h2>Destinataires</h2>
<p>Personnel habilité d’Active Sécurité 974 ; sous-traitants techniques (hébergement du site et du formulaire : {E(h["nom"]) if h["nom"] else ph("hébergeur / service de formulaire")} ; messagerie) le cas échéant.</p>
<h2>Vos droits</h2>
<p>Accès, rectification, suppression, limitation, opposition, portabilité : contactez {biz("email", "e-mail")}. Réclamation possible auprès de la CNIL.</p>
<h2>Cookies</h2>
<p>Voir la page <a href="cookies.html">Cookies</a>.</p>''',
               "Politique de confidentialité d’Active Sécurité 974 : données du formulaire de devis, finalités, durée de conservation et droits RGPD.")
    legal_page("cookies.html", "Cookies — Active Sécurité 974", "Cookies",
               "Politique cookies minimale à finaliser selon l’outil de mesure d’audience / bandeau réellement déployé. Texte à faire relire.",
               f'''<h2>Qu’est-ce qu’un cookie ?</h2>
<p>Petit fichier déposé sur votre terminal lors de la visite du site.</p>
<h2>Cookies utilisés</h2>
<p>{ph("cookies essentiels / mesure d’audience / autres")}. Aucun cookie publicitaire tiers n’est annoncé à ce stade.</p>
<h2>Stockage local</h2>
<p>La fonction « sélection devis » mémorise uniquement dans votre navigateur (stockage local) les produits que vous ajoutez, pour préremplir le formulaire. Ces informations ne sont transmises que si vous envoyez le formulaire, et vous pouvez les retirer à tout moment depuis la page Contact.</p>
<h2>Gestion</h2>
<p>Vous pouvez configurer votre navigateur pour refuser les cookies. Un bandeau de consentement sera ajouté si des cookies non essentiels sont activés.</p>
<h2>Contact</h2>
<p>{biz("email", "e-mail")}</p>''',
               "Politique cookies du site Active Sécurité 974 : cookies, stockage local de la sélection devis et gestion de vos préférences.")

def notfound():
    body = f'''<section class="phero notfound"><div class="wrap center">
<p class="eyebrow">Erreur 404</p><h1 class="display" style="font-size:clamp(56px,10vw,140px)">Page introuvable.</h1>
<p class="lead" style="margin:28px auto 0">La page demandée n’existe pas ou a été déplacée.</p>
<div class="btns" style="justify-content:center"><a class="btn btn-dark btn-lg" href="index.html">Retour à l’accueil</a><a class="btn btn-outline btn-lg" href="catalogue.html">Explorer le catalogue</a></div>
</div></section>'''
    # <base> : GitHub Pages sert 404.html sous l’URL manquante (/as974-site/…).
    write_page("404.html", "Page introuvable — Active Sécurité 974", "Cette page n’existe pas ou a été déplacée.", body, noindex=True, pre="", base=SITE + "/")
