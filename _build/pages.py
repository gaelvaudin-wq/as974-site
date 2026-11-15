"""Pages éditoriales (textes repris des pages v1 validées, mise en page refondue)."""
from core import *
from layout import write_page, crumbs
from components import card, rail, filter_grid, cta, versus, yt, video_ld

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

SZ_HERO = "(max-width:640px) 70vw, 720px"
SZ_SPLIT = "(max-width:980px) 86vw, 640px"
SZ_CARD = "(max-width:640px) 80vw, 340px"

# ====================================================================== ACCUEIL
def home():
    pre = ""
    n = len(ALL)
    hero = f'''<section class="hero on-dark">
<div class="wrap">
<p class="eyebrow reveal">Toute l’île · Ajax Systems</p>
<h1 class="display reveal d1">La sécurité Ajax, chez vous.</h1>
<p class="lead reveal d2">Alarme, incendie, vidéo et domotique. Installés et suivis sur toute l’île de La Réunion, par un partenaire agréé Ajax Systems.</p>
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

    why = f'''<section class="section bg-ink on-dark" id="pourquoi"><div class="wrap">
<div class="head reveal"><p class="eyebrow">Pourquoi Ajax Systems</p><h2 class="h2">Une technologie simple à vivre.</h2>
<p class="lead">Concevoir, installer, accompagner : une seule application pour l’alarme, la vidéo, l’incendie et la domotique.</p></div>
<div class="bento">
<div class="tile w4 reveal"><p class="fig red">2 000<small>m</small></p><h3>Radio Jeweller longue portée</h3><p>Jusqu’à 2 000 m entre une centrale et un détecteur, ou avec un prolongateur de portée.</p><p class="src">ajax.systems/fr/products/hub-2/</p></div>
<div class="tile w2 reveal d1"><p class="fig">3<small>réseaux</small></p><h3>Toujours connectée</h3><p>Ethernet et deux cartes SIM : la centrale bascule d’un réseau à l’autre.</p><p class="src">ajax.systems/fr/products/hub-2/</p></div>
<div class="tile w2 reveal d1"><p class="fig">5<small>ans</small></p><h3>Piles longue durée</h3><p>MotionProtect annonce jusqu’à 5 ans d’autonomie. Beaucoup de détecteurs arrivent piles installées.</p><p class="src">ajax.systems/fr/products/motionprotect/</p></div>
<div class="tile w6 with-img reveal"><div class="tile-txt"><p class="fig" style="font-size:clamp(40px,4.4vw,68px)">Une app.<br>Tout le système.</p><h3>Pilotage au quotidien</h3><p>Smartphone ou ordinateur : armement, notifications, vidéo et scénarios au même endroit.</p><p class="src">ajax.systems/fr/products/hub-2/</p></div>{stage_img("hub-2", "Noir", pre, "(max-width:640px) 70vw, 420px", need_alpha=True)}</div>
</div>
</div></section>'''

    duo = f'''<section class="section"><div class="wrap-wide">
<div class="head center reveal"><p class="eyebrow">Pour qui</p><h2 class="h2">Particuliers &amp; professionnels.</h2></div>
<div class="duo">
<div class="panel light reveal"><p class="eyebrow">Particuliers</p><h3 class="h2">Votre maison, sereine.</h3><p>Maison ou appartement : une solution discrète, fiable, pilotable depuis le smartphone.</p>
<div class="btns"><a class="btn btn-primary" href="contact.html?profil=particulier#devis">Étude gratuite pour mon logement</a><a class="btn btn-outline" href="particuliers.html">En savoir plus</a></div>
<div class="panel-img">{stage_img("doorbell", "Blanc", pre, "(max-width:980px) 60vw, 360px", need_alpha=True)}</div></div>
<div class="panel blue on-dark reveal d1"><p class="eyebrow">Professionnels</p><h3 class="h2">Votre activité, protégée.</h3><p>Commerces, bureaux, entrepôts et plusieurs sites : une installation qui grandit avec vous.</p>
<div class="btns"><a class="btn btn-light" href="contact.html?profil=professionnel#devis">Demander une étude professionnelle</a><a class="btn btn-outline" href="professionnels.html">En savoir plus</a></div>
<div class="panel-img">{stage_img("superior-motioncam-phod-jeweller", "Noir", pre, "(max-width:980px) 60vw, 360px", need_alpha=True)}</div></div>
</div></div></section>'''

    chapters = [
        ("alarme", "gamme-alarme.html", "Chaque accès sous contrôle.", "Détection d’intrusion, commandes et sirènes Ajax Systems. Baseline pour l’essentiel sans fil ; Superior pour les architectures plus exigeantes.", "motionprotect", "Blanc", ""),
        ("incendie", "gamme-incendie.html", "Incendie, du logement au site.", "FireProtect en complément de l’alarme. Ligne EN54 pour les bâtiments professionnels.", "en54-fire-hub-jeweller", "Blanc", ""),
        ("video", "gamme-video.html", "Voir, pour lever le doute.", "Caméras, sonnette et enregistreurs, reliés à l’alarme.", "turretcam", "Noir", "dark"),
        ("domotique", "gamme-domotique.html", "Le confort, dans la même app.", "Prises, relais, éclairage et alertes de fuite d’eau.", "socket", "Blanc", ""),
    ]
    rows = []
    for i, (g, href, h, txt, slug, col, st) in enumerate(chapters):
        cnt = len(group_products(g))
        rows.append(f'''<a class="range-card {st}" href="{href}"><div class="range-media">{stage_img(slug, col, pre, "(max-width:640px) 70vw, 280px", need_alpha=(st == "dark"))}</div><div><p class="num">0{i+1}</p><h3>{h}</h3><p>{txt}</p><span class="count">{cnt} références</span></div></a>''')
    gammes = f'''<section class="section bg-off" id="gammes"><div class="wrap">
<div class="head reveal"><p class="eyebrow">Gammes</p><h2 class="h2">Quatre univers. Un seul système.</h2></div>
<div class="range-grid">{"".join(rows)}</div>
</div></section>'''

    video_home = '''<section class="section" id="video-ia"><div class="wrap">
<div class="head reveal"><p class="eyebrow">Vidéo · Baseline et Superior</p><h2 class="h2">L’IA déclenche l’alarme.</h2>
<p class="lead">Les deux lignes vidéo Ajax reconnaissent les personnes, les véhicules et les animaux, et peuvent déclencher l’alarme. Ce n’est pas réservé à Superior.</p></div>
<figure class="film reveal">
<video poster="assets/video/ia-sirene-dissuasion.jpg" controls playsinline preload="metadata" aria-label="Une caméra Ajax reconnaît une personne et déclenche la sirène">
<source src="assets/video/ia-sirene-dissuasion.webm" type="video/webm">
<source src="assets/video/ia-sirene-dissuasion.mp4" type="video/mp4">
<track kind="captions" src="assets/video/ia-sirene-dissuasion.fr.vtt" srclang="fr" label="Français" default>
</video>
<figcaption>Une caméra Ajax reconnaît une personne et déclenche la sirène.</figcaption>
</figure>
<figure class="hd-shot reveal"><picture>
<source type="image/webp" srcset="assets/img/hd/bulletcam-800.webp 800w, assets/img/hd/bulletcam-1200.webp 1200w, assets/img/hd/bulletcam-1600.webp 1600w" sizes="(max-width:800px) 100vw, 1200px">
<img src="assets/img/hd/bulletcam-1600.webp" alt="BulletCam Ajax, visuel officiel haute définition" width="1600" height="667" loading="lazy" decoding="async">
</picture></figure>
<div class="btns"><a class="btn btn-dark" href="gamme-video.html">Les deux lignes vidéo</a><a class="btn btn-outline" href="gamme-video.html#superior">Voir Superior</a></div>
</div></section>'''

    feat = pick(["hub-2", "motioncam-phod", "doorprotect", "bulletcam", "streetsiren", "keypad-touchscreen", "fireprotect-2-smoke-heat-co", "socket", "doorbell"])
    railsec = f'''<section class="section flush-top"><div class="wrap">
{rail(feat, pre, "Catalogue", "Matériel sur devis.", ("catalogue.html", f"Voir tout le catalogue ({n} références)"), lead="Packshots officiels Ajax Systems. Chaque fiche propose « Demander un devis » : pas de panier ni de paiement en ligne.")}
</div></section>'''

    process = f'''<section class="section bg-off"><div class="wrap">
<div class="head reveal"><p class="eyebrow">Toute l’île, chez vous</p><h2 class="h2">De la prise de contact au suivi.</h2>
<p class="lead">Nord, Sud, Est, Ouest et les Hauts. L’étude, la pose et le suivi se font à votre adresse.</p></div>
<ol class="timeline reveal">
<li><span class="dot">01</span><div><h3>Contact</h3><p>Échange sur votre besoin{(' au ' + biz('telephone')) if biz('telephone') else ''}.</p></div></li>
<li><span class="dot">02</span><div><h3>Étude gratuite</h3><p>Visite chez vous ou échanges à distance.</p></div></li>
<li><span class="dot">03</span><div><h3>Devis clair</h3><p>Sans engagement. Le prix est établi dans le devis.</p></div></li>
<li><span class="dot">04</span><div><h3>Installation</h3><p>Pose, configuration, formation.</p></div></li>
<li><span class="dot">05</span><div><h3>Suivi</h3><p>Maintenance selon le contrat défini ensemble.</p></div></li>
</ol>
</div></section>'''

    delay = biz("delai_reponse")
    cta_text = "Étude et devis gratuits. Partenaire agréé Ajax Systems." + (f" Réponse sous {delay}." if delay else "")
    body = hero + video_home + why + duo + gammes + railsec + process + cta(pre, text=cta_text)
    website = {"@context": "https://schema.org", "@type": "WebSite", "name": BRAND, "url": SITE + "/", "inLanguage": "fr-FR",
               "publisher": {"@id": SITE + "/#entreprise"}}
    org = {"@context": "https://schema.org", "@type": "Organization", "name": BRAND, "url": SITE + "/",
           "logo": SITE + "/assets/img/logo/as974-b-horizontal-noir-rouge.png",
           "areaServed": {"@type": "AdministrativeArea", "name": "La Réunion"}}
    write_page("index.html", "Alarme et vidéosurveillance Ajax à La Réunion — Active Sécurité 974",
               "Installateur partenaire agréé Ajax Systems à La Réunion (Saint-Denis, Saint-Pierre, Saint-Paul, Le Port, Saint-Benoît et toute l’île) : alarme, vidéo, incendie EN54 et domotique. Étude gratuite chez vous.",
               body, jsonld=[website, org, video_ld("o8VNaCPCydE", "De la détection à la réaction", "Les caméras Ajax peuvent lancer une réaction automatique.")], priority="1.0")

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
    body = f'''<section class="phero bg-blue on-dark"><div class="wrap phero-split crumbs-first">
<div class="reveal">{cr}<p class="eyebrow">Professionnels</p><h1 class="h1">Votre activité, protégée.</h1>
<p class="lead">Commerces, bureaux, entrepôts et plusieurs sites. Étude, installation et suivi par un partenaire agréé Ajax Systems, sur toute l’île.</p>
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
<li><h3>Plusieurs sites</h3><p>Un interlocuteur unique sur toute l’île, pour chaque adresse.</p></li>
<li><h3>Incendie</h3><p>Détecteurs de fumée, de chaleur et de monoxyde de carbone, étudiés selon votre site.</p></li>
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
<section class="section" id="video-superior"><div class="wrap">
<div class="head reveal"><span class="tag tag-sup">Superior · vidéo</span><h2 class="h2">La ligne vidéo des sites exigeants.</h2>
<p class="lead">Comme la ligne Baseline, les caméras Superior reconnaissent les personnes, les véhicules et les animaux, et peuvent déclencher l’alarme. Superior y ajoute une IA enrichie, des optiques P-Iris 2,8–12 mm, un haut-parleur, et les enregistreurs Superior NVR H2D.</p></div>
<div class="btns"><a class="btn btn-dark" href="gamme-video.html#superior">Voir la ligne Superior</a><a class="btn btn-outline" href="catalogue-video.html?gamme=superior#references">Références Superior</a></div>
{yt("c9dYVQLXWj4", "La vidéo dans Ajax PRO Desktop", "Intégration des flux vidéo dans Ajax PRO Desktop. Vidéo Ajax Systems.")}
<p class="mt-28"><a class="link" href="gamme-incendie.html">Système incendie professionnel EN54</a></p>
</div></section>
<section class="section bg-ink on-dark"><div class="wrap">
<p class="eyebrow reveal">Après la pose</p>
<p class="statement reveal">Un suivi dans la durée. <span class="dim">Maintenance selon le contrat défini ensemble.{(" " + telesurv()) if telesurv() else ""}</span></p>
<div class="btns reveal"><a class="btn btn-light" href="services.html">Voir les services</a></div>
</div></section>
{cta(pre, "Parlons de votre site.", "Étude professionnelle sur place — toute l’île.", "Demander une étude professionnelle", "contact.html?profil=professionnel#devis")}'''
    write_page("professionnels.html", "Sécurité professionnelle Ajax à La Réunion — Superior et EN54 | AS974",
               "Sécurité pour commerces, bureaux et plusieurs sites à La Réunion : ligne vidéo Superior, incendie EN54 et applications Ajax PRO. Étude sur place par Active Sécurité 974.",
               body, jsonld=[ld, video_ld("c9dYVQLXWj4", "La vidéo dans Ajax PRO Desktop", "Intégration des flux vidéo Ajax dans Ajax PRO Desktop.")], priority="0.9")

# ====================================================================== GAMMES
GAMME_PAGES = {
    "alarme": ("gamme-alarme.html", "Alarme intrusion", "Détection d’intrusion, commandes et sirènes Ajax Systems. Baseline pour l’essentiel sans fil ; Superior pour les architectures plus exigeantes.",
               "motioncam-phod", "Noir", "dark", ["doorprotect", "motionprotect", "motioncam-phod", "keypad-touchscreen", "streetsiren", "combiprotect"],
               "Alarme intrusion sans fil Ajax à La Réunion — détecteurs, claviers, sirènes | AS974",
               "Alarme intrusion Ajax Systems à La Réunion : détecteurs de mouvement et d’ouverture, claviers, sirènes. Gammes Baseline et Superior, installation par AS974."),
    "incendie": ("gamme-incendie.html", "Incendie", "Détecteurs de fumée, de chaleur et de monoxyde de carbone, étudiés selon votre site.",
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

def video_block(pre):
    return f'''<figure class="film">
<video poster="{pre}assets/video/ia-sirene-dissuasion.jpg" controls playsinline preload="metadata" aria-label="Une caméra Ajax reconnaît une personne et déclenche la sirène">
<source src="{pre}assets/video/ia-sirene-dissuasion.webm" type="video/webm">
<source src="{pre}assets/video/ia-sirene-dissuasion.mp4" type="video/mp4">
<track kind="captions" src="{pre}assets/video/ia-sirene-dissuasion.fr.vtt" srclang="fr" label="Français" default>
</video>
<figcaption>Une caméra Ajax reconnaît une personne et déclenche la sirène.</figcaption>
</figure>'''

def gamme_video():
    pre = ""
    prods = group_products("video")
    def line_of(p):
        n = (p["name"] + " " + p["slug"]).lower()
        if "superior" in n:
            return "superior"
        return "baseline"
    base = [p for p in prods if line_of(p) == "baseline"]
    sup = [p for p in prods if line_of(p) == "superior"]
    cr, ld = crumbs(pre, [("catalogue.html", "Catalogue"), (None, "Vidéosurveillance")])
    def names(pred):
        # one label per family, official order
        order = ["BulletCam", "TurretCam", "DomeCam", "IndoorCam", "DoorBell", "NVR"]
        found = []
        for key in order:
            if any(key.lower() in p["name"].lower() for p in pred):
                found.append(key if key != "DoorBell" else "DoorBell")
        return ", ".join(found)
    body = f'''<section class="phero"><div class="wrap">
<div class="reveal">{cr}<p class="eyebrow">Vidéosurveillance</p><h1 class="h1">Deux lignes. La même IA.</h1>
<p class="lead">Ajax présente deux lignes de vidéosurveillance : Baseline et Superior. Les deux intègrent une intelligence artificielle qui reconnaît les personnes, les véhicules et les animaux, et peut déclencher l’alarme.</p>
<div class="btns"><a class="btn btn-primary btn-lg" href="#ia">Voir la reconnaissance</a><a class="btn btn-outline btn-lg" href="catalogue-video.html">Voir les {len(prods)} références</a></div></div>
</div></section>
<section class="section flush-top" id="ia"><div class="wrap">
<div class="split">
<div class="reveal">{video_block(pre)}</div>
<div class="split-txt reveal d1"><p class="eyebrow">Commun aux deux lignes</p><h2 class="h2">Personnes, véhicules, animaux.</h2>
<p class="lead">Sur Baseline comme sur Superior, l’intelligence artificielle est intégrée aux caméras. Elle distingue les personnes, les véhicules et les animaux, et peut déclencher l’alarme. Ce n’est pas une option réservée à Superior.</p>
<p class="src-note">Sources : <a href="https://ajax.systems/fr/catalogue/video-surveillance/" rel="noopener">catalogue Baseline</a> et <a href="https://ajax.systems/fr/catalogue/superior-video-surveillance/" rel="noopener">catalogue Superior</a>, ajax.systems.</p>
</div>
</div>
</div></section>
<section class="section bg-off" id="baseline"><div class="wrap">
<div class="head reveal"><span class="tag tag-base">Baseline</span><h2 class="h2">La ligne essentielle.</h2>
<p class="lead">Caméras, sonnette et enregistreurs pour la maison et les petits sites. L’IA intégrée reconnaît les personnes, les véhicules et les animaux et peut déclencher l’alarme. Ajax indique que le matériel de cette ligne est conforme NDAA.</p></div>
<div class="feature-grid">
<article class="feature"><h3>Caméras</h3><p>BulletCam, TurretCam et DomeCam Mini, en infrarouge ou en éclairage hybride (HL). Les versions HLVF ajoutent un objectif varifocal motorisé de 2,8–12 mm, l’éclairage hybride, le True WDR et des entrées/sorties audio et alarme.</p></article>
<article class="feature"><h3>Aussi dans Baseline</h3><p>IndoorCam (Wi-Fi) et DoorBell. Même application Ajax que l’alarme, la même reconnaissance personnes, véhicules et animaux.</p></article>
<article class="feature"><h3>Enregistreurs</h3><p>NVR, NVR H et NVR H2D. L’alimentation 12 V pour NVR complète l’installation lorsque le site le demande.</p></article>
</div>
<p class="mt-28"><a class="btn btn-dark" href="catalogue-video.html?gamme=baseline#references">{len(base)} références Baseline</a></p>
</div></section>
<section class="section" id="superior"><div class="wrap">
<div class="head reveal"><span class="tag tag-sup">Superior</span><h2 class="h2">La ligne pour les sites exigeants.</h2>
<p class="lead">« Leurs fonctionnalités fondamentales sont sublimées par une qualité visuelle exceptionnelle, une intelligence artificielle enrichie, et un éventail d’options élargi. » La reconnaissance personnes, véhicules et animaux, et le déclenchement de l’alarme, restent ceux de la ligne Baseline : l’IA enrichie s’y ajoute, elle ne les remplace pas.</p></div>
<div class="feature-grid">
<article class="feature"><h3>Caméras HLVF</h3><p>Superior BulletCam, DomeCam et TurretCam HLVF : objectif varifocal motorisé P-Iris de 2,8–12 mm, éclairage hybride, True WDR, microphone et haut-parleur, entrées et sorties audio et alarme, PoE ou 12 V.</p></article>
<article class="feature"><h3>Enregistreurs</h3><p>Superior NVR H2D, doté d’IA : HDMI 4K, deux disques remplaçables à chaud, ports PoE ou double Gigabit selon le modèle, de 8 à 32 canaux.</p></article>
<article class="feature"><h3>Pour qui</h3><p>Sites professionnels et projets ambitieux. Ajax réserve cette ligne aux partenaires accrédités. Active Sécurité 974 est partenaire agréé.</p></article>
</div>
<p class="mt-28"><a class="btn btn-dark" href="catalogue-video.html?gamme=superior#references">{len(sup)} références Superior</a> <a class="btn btn-outline" href="professionnels.html#video-superior">Côté professionnels</a></p>
</div></section>
<section class="section bg-off"><div class="wrap">
<div class="head reveal"><p class="eyebrow">Ce qui change</p><h2 class="h2">Même IA. Plus d’optiques et d’options.</h2></div>
<table class="spec compare-video">
<tr><th scope="col"> </th><th scope="col">Baseline</th><th scope="col">Superior</th></tr>
<tr><th scope="row">IA personnes, véhicules, animaux</th><td>Oui, intégrée. Peut déclencher l’alarme.</td><td>Oui, la même base, avec une IA enrichie.</td></tr>
<tr><th scope="row">Caméras</th><td>BulletCam, TurretCam, DomeCam Mini, versions IR, HL et HLVF. IndoorCam, DoorBell.</td><td>Superior BulletCam, DomeCam et TurretCam HLVF.</td></tr>
<tr><th scope="row">Objectif</th><td>Fixe sur IR et HL. Varifocal motorisé 2,8–12 mm sur HLVF.</td><td>Varifocal motorisé P-Iris 2,8–12 mm.</td></tr>
<tr><th scope="row">Nuit et audio</th><td>Infrarouge, ou couleur avec l’éclairage hybride (HL / HLVF). Microphone.</td><td>Éclairage hybride, microphone et haut-parleur.</td></tr>
<tr><th scope="row">Enregistreurs</th><td>NVR, NVR H, NVR H2D.</td><td>Superior NVR H2D, HDMI 4K, deux disques, IA.</td></tr>
</table>
<p class="src-note"><a href="https://ajax.systems/fr/catalogue/video-surveillance/" rel="noopener">Catalogue Baseline</a> · <a href="https://ajax.systems/fr/catalogue/superior-video-surveillance/" rel="noopener">Catalogue Superior</a></p>
</div></section>
<section class="section"><div class="wrap">
{rail([p for p in base if p["slug"] in ("bulletcam","turretcam","domecam-mini","indoorcam","doorbell","nvr")] or base[:6], pre, "Baseline", "Caméras et enregistreurs essentiels.", ("catalogue-video.html?gamme=baseline#references", "Toute la ligne Baseline"))}
</div></section>
<section class="section bg-off"><div class="wrap">
{rail(sup[:8], pre, "Superior", "Caméras HLVF et NVR pour les sites exigeants.", ("catalogue-video.html?gamme=superior#references", "Toute la ligne Superior"))}
</div></section>
{cta(pre, "Un projet vidéo ?", "Étude chez vous, sur toute l’île. Baseline ou Superior, selon le site.")}'''
    write_page("gamme-video.html",
               "Vidéosurveillance Ajax à La Réunion — lignes Baseline et Superior | AS974",
               "Deux lignes vidéo Ajax, Baseline et Superior. Les deux reconnaissent personnes, véhicules et animaux et peuvent déclencher l’alarme. Caméras, NVR et étude à La Réunion.",
               body, jsonld=[ld, {"@context": "https://schema.org", "@type": "VideoObject",
                   "name": "Une caméra Ajax reconnaît une personne et déclenche la sirène",
                   "description": "Démonstration : la reconnaissance de personne peut déclencher la sirène, sur Baseline comme sur Superior.",
                   "contentUrl": SITE + "/assets/video/ia-sirene-dissuasion.mp4",
                   "thumbnailUrl": SITE + "/assets/video/ia-sirene-dissuasion.jpg",
                   "embedUrl": SITE + "/gamme-video.html#ia"}], priority="0.8")

def gamme_en54():
    pre = ""
    prods = [p for p in ALL if p["gamme"] == "EN54 Line" or str(p["slug"]).startswith("en54-")]
    cr, ld = crumbs(pre, [("professionnels.html", "Professionnels"), (None, "Incendie EN54")])
    hubs = [p for p in prods if p["category"] == "Centrales"]
    dets = [p for p in prods if p["category"] == "Détecteurs d'incendie"]
    sound = [p for p in prods if "sounder" in p["slug"] or "vad" in p["slug"] or p["category"] == "Dispositifs d'alarme incendie"]
    calls = [p for p in prods if "call" in p["slug"] or p["category"] == "Déclencheurs manuels d'alarme"]
    body = f'''<section class="phero"><div class="wrap phero-split crumbs-first">
<div class="reveal">{cr}<p class="eyebrow">Professionnels · EN54 Line</p><h1 class="h1">Incendie, du logement au bâtiment.</h1>
<p class="lead">Deux usages distincts chez Ajax : les détecteurs FireProtect pour compléter une alarme de logement, et la ligne EN54 pour les bâtiments professionnels.</p>
<div class="btns"><a class="btn btn-primary btn-lg" href="contact.html?profil=professionnel#devis">Étude incendie professionnelle</a><a class="btn btn-outline btn-lg" href="catalogue-incendie.html">Voir les {len(prods)} références EN54</a></div></div>
<div class="phero-media reveal d1">{stage_img("en54-fire-hub-jeweller", "Blanc", pre, SZ_SPLIT, eager=True)}</div>
</div></section>
<section class="section" id="logement"><div class="wrap">
<div class="head reveal"><h2 class="h2">Particuliers : FireProtect en complément de votre alarme.</h2>
<p class="lead">Fumée, chaleur et monoxyde de carbone, dans la même application que l’alarme intrusion. Ce n’est pas le système EN54 des bâtiments.</p>
<a class="btn btn-dark" href="gamme-alarme.html">Voir le complément alarme</a></div>
</div></section>
<section class="section bg-off" id="en54"><div class="wrap">
<div class="head reveal"><h2 class="h2">Professionnels : la ligne EN54.</h2>
<p class="lead">Ajax présente cette ligne comme un système d’alarme incendie sans fil conçu selon EN 54, pour les bâtiments commerciaux et municipaux.</p></div>
<div class="feature-grid">
<article class="feature"><h3>Centrale</h3><p>EN54 Fire Hub Jeweller. Ajax indique les normes EN 54-2, EN 54-4, EN 54-13, EN 54-21, EN 54-25 et EN 50131 (Grade 2). Pilotage par l’écran tactile ou les applications Ajax.</p></article>
<article class="feature"><h3>Détecteurs</h3><p>EN54 FireProtect chaleur, fumée, et versions avec diffuseur. Normes citées par Ajax : EN 54-3, EN 54-5, EN 54-7, EN 54-25. Détection de fumée HazeFlow 2 et détection de chaleur.</p></article>
<article class="feature"><h3>Alerte</h3><p>Diffuseurs, indicateurs visuels (VAD) et déclencheurs manuels. Ajax précise que seule la version rouge du ManualCallPoint est certifiée EN 54-25.</p></article>
<article class="feature"><h3>Autour de la centrale</h3><p>EN54 Fire ReX Jeweller prolonge la portée. Le module EN54 I/O (2×2) et les batteries internes 24 h ou 72 h complètent le système.</p></article>
</div>
<p class="src-note"><a href="https://ajax.systems/fr/solutions/en-54-certified-fire-and-life-safety-solution/" rel="noopener">Ligne EN54 sur ajax.systems</a></p>
{yt("5HO9wW5xYc8", "EN54 Line : système sans fil", "Vidéo officielle Ajax Systems : la ligne EN54, détection incendie sans fil pour les sites professionnels.")}
</div></section>
<section class="section bg-off"><div class="wrap">
{rail(prods[:8], pre, "Catalogue EN54", "Les références de la ligne.", ("catalogue-incendie.html", "Tout le catalogue incendie EN54"))}
<p class="mt-28">La ligne Type 4 d’Ajax est une autre offre professionnelle, distincte de l’EN54. <a class="link" href="catalogue-incendie.html?gamme=type4#references">Voir la ligne Type 4</a></p>
</div></section>
{cta(pre, "Un site professionnel à protéger.", "Étude incendie chez vous, sur toute l’île de La Réunion.", "Demander une étude", "contact.html?profil=professionnel#devis")}'''
    write_page("gamme-incendie.html",
               "Incendie EN54 Ajax à La Réunion — centrale, détecteurs, déclencheurs | AS974",
               "Ligne professionnelle Ajax EN54 à La Réunion : centrale Fire Hub, détecteurs, déclencheurs manuels et diffuseurs. Étude pour commerces et bâtiments, par Active Sécurité 974.",
               body, jsonld=[ld, video_ld("5HO9wW5xYc8", "EN54 Line : système sans fil", "Présentation officielle Ajax Systems de la ligne incendie EN54.")], priority="0.8")

def gamme(g):
    if g == "video":
        return gamme_video()
    if g == "incendie":
        return gamme_en54()
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
    others = [(gk, n) for gk, n in others if n and gk != "a-confirmer"]
    oth = ""
    if others:
        oth = '<p class="muted mt-28 reveal">Également au catalogue : ' + ", ".join(f'<a class="link" style="min-height:0" href="catalogue-{g}.html?gamme={gk}#references">{GAMME_LABEL[gk]} ({n})</a>' for gk, n in others) + ".</p>"
    base_rail = fill(g, "baseline", feat)
    sup_rail = fill(g, "superior", [])
    extra = ""
    if g == "alarme":
        fire = [p for p in ALL if p["group"] == "alarme" and p["category"] == "Détecteurs d'incendie"]
        extra = f'''<section class="section bg-off"><div class="wrap">
<div class="head reveal"><p class="eyebrow">Complément Baseline</p><h2 class="h2">Détecteurs incendie pour le logement.</h2>
<p class="lead">Fumée, chaleur et monoxyde de carbone dans la même application que l’alarme. Pour un bâtiment, la ligne EN54 est à part.</p></div>
{rail(fire[:6], pre, "Residence Line", "À ajouter à une alarme Baseline.", ("catalogue-alarme.html?sous=detecteurs-d-incendie#references", "Tous les détecteurs incendie logement"))}
<p class="mt-28"><a class="link" href="gamme-incendie.html">Système professionnel EN54</a></p>
</div></section>'''
    if g == "domotique":
        extra = f'''<section class="section"><div class="wrap">
<div class="head reveal"><h2 class="h2">Scénarios dans l’application.</h2>
<p class="lead">Prises, relais et interrupteurs Ajax réagissent à l’armement, à une alarme ou à une température. Les deux vidéos ci-dessous sont publiées par Ajax Systems.</p></div>
<div class="duo-yt">{yt("ms08SAie8Pg", "Scénario de température", "Un scénario d’automatisation dans l’application Ajax.")}{yt("o8VNaCPCydE", "De la détection à la réaction", "Les caméras peuvent lancer une réaction. Vidéo Ajax Systems.")}</div>
</div></section>'''
    body = f'''<section class="phero"><div class="wrap phero-split">
<div class="reveal">{cr}<p class="eyebrow">Gamme</p><h1 class="h1">{E(label)}</h1>
<p class="lead">{lead}</p>
<div class="btns"><a class="btn btn-primary btn-lg" href="contact.html#devis">Demander un devis</a><a class="btn btn-outline btn-lg" href="catalogue-{g}.html">Voir les {len(prods)} références</a></div></div>
<div class="phero-media {st} reveal d1">{stage_img(hslug, hcol, pre, SZ_SPLIT, eager=True, need_alpha=(st == "dark"))}</div>
</div></section>
{extra}
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
    lds = [ld]
    if g == "domotique":
        lds.append(video_ld("ms08SAie8Pg", "Scénario de température Ajax", "Réglage d’un scénario de température dans l’application Ajax."))
    write_page(path, title, desc, body, jsonld=lds, priority="0.8")

# ====================================================================== CATALOGUE
CAT_LEADS = {
    "centrales": "Le cœur de votre système Ajax Systems : centrales, kits et prolongateurs de portée. Dimensionnés et installés par Active Sécurité 974 sur toute l’île.",
    "alarme": "Détecteurs, claviers, sirènes et commandes. Baseline pour l’essentiel sans fil ; Superior pour les projets exigeants.",
    "incendie": "Ligne professionnelle Ajax EN54 : centrale, détecteurs, déclencheurs et diffuseurs. Les FireProtect du logement sont dans l’alarme intrusion.",
    "video": "Caméras, sonnette et NVR Ajax Systems, intégrés à l’écosystème alarme, sur devis et installation AS974.",
    "domotique": "Prises, relais, éclairage, détection de fuite et qualité de l’air : automatisez le quotidien dans la même application.",
    "accessoires": "Modules d’intégration, alimentations, boîtiers et accessoires de pose pour compléter et raccorder votre installation.",
}
CAT_IMG = {"centrales": ("hub2-plus", "Noir"), "alarme": ("motioncam-phod", "Noir"), "incendie": ("en54-fire-hub-jeweller", "Blanc"),
           "video": ("turretcam", "Blanc"), "domotique": ("socket", "Blanc"), "accessoires": ("button", "Blanc")}

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
{cta(pre, "Prêt à composer votre système ?", "Étude et devis gratuits, chez vous, sur toute l’île." + (f" Réponse sous {biz('delai_reponse')}." if biz('delai_reponse') else ""))}'''
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
<div class="split-txt reveal d1"><p class="num">01 — Étude &amp; devis gratuit</p><h2 class="h2">Comprendre avant de proposer.</h2><p class="lead">Visite chez vous ou échange à distance. Un devis clair, sans engagement. Le prix est établi après l’étude.</p>
<div class="btns"><a class="btn btn-primary" href="contact.html#devis">Prendre rendez-vous d’étude</a></div></div>
</div>
<div class="split rev">
<div class="split-media dark reveal">{stage_img("keypad-touchscreen", "Noir", pre, SZ_SPLIT, need_alpha=True)}</div>
<div class="split-txt reveal d1"><p class="num">02 — Installation</p><h2 class="h2">Une pose soignée, chez vous.</h2><p class="lead">Pose, paramétrage, tests radio, formation à l’application, documentation. Intervention chez le client.</p>
<div class="btns"><a class="btn btn-primary" href="contact.html#devis">Planifier mon installation</a></div></div>
</div>
<div class="split">
<div class="split-media reveal">{stage_img("streetsiren", "Blanc", pre, SZ_SPLIT)}</div>
<div class="split-txt reveal d1"><p class="num">03 — Maintenance / télésurveillance</p><h2 class="h2">Un suivi dans la durée.</h2><p class="lead">Maintenance et dépannage, selon le contrat défini ensemble. {telesurv()}</p>
<div class="btns"><a class="btn btn-outline" href="contact.html#devis">Me renseigner sur les options</a></div></div>
</div>
</div></section>
<section class="section"><div class="wrap">
<div class="head reveal"><h2 class="h2">Les applications Ajax, en images.</h2>
<p class="lead">Démonstrations publiées par Ajax Systems : comptes installateur, scénarios, et lecture des archives sur ordinateur.</p></div>
<div class="duo-yt">{yt("NLnFmO16dXI", "Les applications Ajax", "Trouver un appareil ou un utilisateur dans les applications Ajax.")}{yt("cD5_1sNxsVM", "Archives sur ordinateur", "Lecture des archives dans les applications de bureau Ajax.")}</div>
</div></section>
{cta(pre, "Prêt à démarrer ?", "Étude et devis gratuits sur toute l’île.")}'''
    for path, h1, lead, steps in (
        ("services-etude.html", "Étude et devis gratuit", "Une visite chez vous ou un échange à distance. La proposition reste sans engagement.",
         ["Nous venons voir les accès et les volumes.", "Pour un projet simple, des photos suffisent à préparer une première piste.", "Vous décidez ensuite, à votre rythme."]),
        ("services-installation.html", "Installation", "Pose, paramétrage et prise en main, avant que nous partions.",
         ["Les emplacements sont validés avec vous.", "Pose des appareils, sans fil ou filaires selon le projet.", "Zones, utilisateurs et notifications sont réglés.", "Prise en main de l’application.", "Un récapitulatif de l’installation vous est remis."]),
        ("services-maintenance.html", "Maintenance", "Après la mise en service, nous restons l’interlocuteur du système.",
         ["Vérification des appareils, des piles et des liaisons.", "Intervention chez vous si le système le demande.", "La télésurveillance se discute pendant l’étude. Elle n’est pas un service déjà ouvert."]),
    ):
        cr2, ld2 = crumbs(pre, [("services.html", "Services"), (None, h1)])
        lis = "".join(f"<li><h2>{E(s)}</h2></li>" for s in steps)
        write_page(path, f"{h1} — Active Sécurité 974 à La Réunion",
                   f"{h1} par Active Sécurité 974, chez vous, sur toute l’île de La Réunion.",
                   f'''<section class="phero"><div class="wrap">{cr2}<h1 class="h1">{h1}</h1><p class="lead">{lead}</p></div></section>
<section class="section flush-top"><div class="wrap"><ol class="numlist">{lis}</ol></div></section>
{cta(pre)}''', jsonld=[ld2], priority="0.6")
    write_page("services.html", "Services : étude, installation, maintenance — Active Sécurité 974",
               "Étude et devis gratuits, installation et paramétrage, maintenance selon contrat : Active Sécurité 974 vous accompagne chez vous, partout à La Réunion.",
               body, jsonld=[ld, video_ld("NLnFmO16dXI", "Les applications Ajax", "Recherche dans les applications Ajax."), video_ld("cD5_1sNxsVM", "Archives Ajax", "Lecture des archives dans les applications de bureau Ajax.")], priority="0.7")

def a_propos():
    pre = ""
    cr, ld = crumbs(pre, [(None, "À propos")])
    body = f'''<section class="phero"><div class="wrap">
<div class="reveal">{cr}<p class="eyebrow">À propos</p><h1 class="h1">Active Sécurité 974, votre installateur à La Réunion.</h1>
<p class="lead">Partenaire agréé Ajax Systems. Conseil, pose et suivi, chez vous, sur toute l’île.</p></div>
</div></section>
<section class="section bg-ink on-dark"><div class="wrap">
<p class="statement reveal">Un interlocuteur local. <span class="dim">Nord, Sud, Est, Ouest et Hauts : nous venons chez vous, de l’étude au suivi.</span></p>
</div></section>
<section class="section"><div class="wrap">
<div class="head reveal"><p class="eyebrow">Nos engagements</p><h2 class="h2">Ce qui nous guide.</h2></div>
<ol class="numlist reveal">
<li><h3>Ancrage local</h3><p>Intervention Nord, Sud, Est, Ouest et Hauts. Nous venons chez vous.</p></li>
<li><h3>Approche conseil</h3><p>Baseline ou Superior selon le site : pas de survente, devis clair.</p></li>
<li><h3>Matériel partenaire</h3><p>Partenaire agréé Ajax Systems. Les visuels et les références viennent du fabricant.</p></li>
<li><h3>Devis clair</h3><p>Le prix est établi dans le devis, après avoir vu votre site.</p></li>
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
    action = (CFG.get("form_action") or "").strip()
    if action.startswith("["):
        action = ""
    email = biz_txt("email")
    phone = biz("telephone")
    ready = action.startswith("http")
    aside = f'''<aside class="aside on-dark" aria-label="Coordonnées">
<h2>Active Sécurité 974</h2>
<p>Partenaire agréé Ajax Systems. Interventions chez vous, sur toute l’île.</p>
<dl>
{row("Adresse", biz("adresse"))}
{row("Téléphone", phone)}
{row("E-mail", biz("email"))}
{row("SIRET", biz("siret"))}
<dt>Zone</dt><dd>Toute l’île de La Réunion</dd>
</dl>
<div class="sl-box"><h3>Votre sélection devis</h3><ul class="sl-list" id="sl-list"><li>Aucun produit pour l’instant.</li></ul>
<p style="margin-top:12px"><a class="link" href="catalogue.html">Ajouter depuis le catalogue</a></p></div>
</aside>'''
    if ready or email:
        note_bits = ["Champs obligatoires <span class=\"req\">*</span>."]
        if biz("delai_reponse"):
            note_bits.insert(0, f"Nous vous répondons sous {biz('delai_reponse')}.")
        if biz("horaires"):
            note_bits.insert(0, biz("horaires") + ".")
        form = f'''<div class="prefill" id="prefill" role="status"></div>
<form class="form" id="form-devis" name="devis" method="POST" action="{E(action) if ready else ''}" data-mailto="{E(email)}">
<input type="hidden" name="_subject" value="Demande de devis — Active Sécurité 974">
<p class="hp"><label>Ne pas remplir <input name="_gotcha" tabindex="-1" autocomplete="off"></label></p>'''
        # the rest of fields is appended below via marker
        form_tail = f'''<div class="full"><button class="btn btn-primary btn-lg" type="submit">Envoyer ma demande de devis</button>
<p class="form-note">{' '.join(note_bits)}</p></div>
</form>'''
        main = "FIELDS"
    else:
        call = f' <a href="tel:{phone}">{phone}</a>' if phone else ""
        form = ""
        form_tail = ""
        main = f'''<div class="prefill" id="prefill" role="status"></div>
<div class="devis-soon" role="status">
<h2>Coordonnées bientôt disponibles.</h2>
<p>Téléphone, e-mail, WhatsApp et formulaire s’afficheront ici dès qu’ils seront renseignés. Vous pouvez déjà parcourir le catalogue.</p>
</div>'''
    fields = '''<div><label for="f-nom">Nom et prénom <span class="req" aria-hidden="true">*</span></label><input id="f-nom" name="nom" autocomplete="name" required placeholder="Votre nom"></div>
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
</div></fieldset>
<div class="full"><label for="f-gamme-souhaitee">Gamme souhaitée</label><select id="f-gamme-souhaitee" name="gamme"><option>Je ne sais pas</option><option>Baseline</option><option>Superior</option></select></div>
<div class="full"><label for="f-produits">Produits du catalogue</label><textarea id="f-produits" name="produits" rows="4" placeholder="Modèle, référence et coloris, préremplis depuis une fiche."></textarea></div>
<div class="full"><label for="f-message">Message</label><textarea id="f-message" name="message" placeholder="Décrivez brièvement votre besoin…"></textarea></div>
<div class="full"><label class="consent"><input type="checkbox" name="consentement" value="oui" required> <span>J’accepte que mes données soient utilisées pour répondre à ma demande, conformément à la <a href="politique-confidentialite.html">politique de confidentialité</a>. <span class="req" aria-hidden="true">*</span></span></label></div>
'''
    if ready or email:
        column = form + fields + form_tail
    else:
        column = main
    body = f'''<section class="phero" style="padding-bottom:clamp(40px,5vw,72px)"><div class="wrap">
<div class="reveal">{cr}<p class="eyebrow">Contact &amp; devis</p><h1 class="h1">Contactez Active Sécurité 974.</h1>
<p class="lead">Parlez-nous de votre projet : maison, appartement, commerce ou site professionnel. Nous venons chez vous, sur toute l’île, pour l’étude gratuite.</p></div>
</div></section>
<section class="section flush-top" id="devis"><div class="wrap contact-grid">
<div>
{column}
</div>
{aside}
</div></section>'''
    write_page("contact.html", "Contact et demande de devis gratuit — Active Sécurité 974",
               "Demandez votre devis gratuit : alarme, vidéosurveillance, incendie ou domotique Ajax Systems. Intervention chez vous sur toute l’île de La Réunion.",
               body, jsonld=[ld], priority="0.9")
    body2 = f'''<section class="phero notfound"><div class="wrap center">
<p class="eyebrow">Demande envoyée</p><h1 class="h1">Merci, votre demande est bien partie.</h1>
<p class="lead" style="margin:28px auto 0">Un conseiller Active Sécurité 974 revient vers vous{(' sous ' + biz('delai_reponse')) if biz('delai_reponse') else ''}.</p>
<div class="btns" style="justify-content:center"><a class="btn btn-dark btn-lg" href="index.html">Retour à l’accueil</a><a class="btn btn-outline btn-lg" href="catalogue.html">Explorer le catalogue</a></div>
</div></section>'''
    write_page("merci.html", "Merci — demande de devis envoyée | AS974", "Votre demande de devis a bien été transmise à Active Sécurité 974.", body2, noindex=True)

# ====================================================================== LÉGAL
FAQ = [
    ("Où intervenez-vous à La Réunion ?",
     "Chez le client, sur toute l’île : Saint-Denis, Saint-Pierre, Saint-Paul, Le Port, Saint-Benoît, les autres communes et les Hauts. Il n’y a pas de local ouvert au public."),
    ("Baseline et Superior vidéo ont-ils la même intelligence artificielle ?",
     "Oui. Ajax équipe les deux lignes d’une IA qui reconnaît les personnes, les véhicules et les animaux, et peut déclencher l’alarme. Superior ajoute une IA enrichie, des optiques P-Iris et des enregistreurs NVR H2D."),
    ("Les détecteurs FireProtect remplacent-ils un système incendie EN 54 ?",
     "Non. Les FireProtect et FireProtect 2 de la Residence Line complètent une alarme de logement. Le système professionnel certifié EN 54 est la ligne EN54 : centrale Fire Hub, détecteurs, déclencheurs manuels et diffuseurs."),
    ("Y a-t-il un prix sur le site ?",
     "Non. Chaque référence est sur devis. L’étude et le devis sont gratuits, sans engagement, après un échange ou une visite chez vous."),
    ("Quelles applications pilotent le système ?",
     "L’application Ajax Security System pour l’usage quotidien, les applications Ajax PRO et PRO Desktop pour l’installateur. Vidéo, notifications et scénarios y sont réunis."),
    ("Baseline ou Superior ?",
     "Baseline couvre la maison et les petits sites. Superior vise les sites plus exigeants : optique P-Iris, haut-parleur, NVR H2D, IA enrichie. Les deux lignes vidéo reconnaissent personnes, véhicules et animaux."),
    ("Quel délai pour une intervention ?",
     "Il est fixé avec vous, selon la commune et le type de site, de Saint-Denis à Saint-Pierre, Saint-Paul, Le Port, Saint-Benoît et les Hauts."),
    ("Proposez-vous la télésurveillance ?",
     "Elle peut être étudiée avec le projet. Elle n’est pas affichée comme un service déjà ouvert."),
]

def faq():
    pre = ""
    cr, ld = crumbs(pre, [(None, "Questions fréquentes")])
    blocks = "".join(f'<details class="faq"><summary>{E(q)}</summary><p>{E(a)}</p></details>' for q, a in FAQ)
    main = {"@context": "https://schema.org", "@type": "FAQPage",
            "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]}
    body = f'''<section class="phero"><div class="wrap">{cr}<p class="eyebrow">Questions fréquentes</p><h1 class="h1">Ce qu’il faut savoir avant l’étude.</h1>
<p class="lead">Réponses courtes sur l’intervention à La Réunion, les lignes Ajax Baseline, Superior et EN54, et les applications.</p></div></section>
<section class="section flush-top"><div class="wrap"><div class="feature-grid">{blocks}</div>
<div class="duo-yt mt-28">{yt("NLnFmO16dXI", "Applications Ajax", "Trouver un appareil ou un utilisateur dans les applications Ajax. Vidéo officielle Ajax Systems.")}{yt("ycQSM6qOXNw", "Notifications d’ouverture", "Réglage officiel des notifications de porte lorsque le système est désarmé.")}</div>
</div></section>
{cta(pre)}'''
    write_page("faq.html", "Questions fréquentes — alarme Ajax à La Réunion | AS974",
               "FAQ Active Sécurité 974 : intervention sur toute La Réunion, vidéo Baseline et Superior, incendie EN54, applications Ajax et devis gratuit.",
               body, jsonld=[ld, main, video_ld("NLnFmO16dXI", "Applications Ajax", "Recherche dans les applications Ajax Security System et Ajax PRO.")], priority="0.6")

def legal_page(path, title, h1, note, inner, desc):
    pre = ""
    cr, ld = crumbs(pre, [(None, h1)])
    notice = f'<div class="notice">{note}</div>' if note else ""
    body = f'''<section class="phero" style="padding-bottom:clamp(40px,5vw,64px)"><div class="wrap">{cr}<p class="eyebrow">Informations légales</p><h1 class="h1" style="font-size:clamp(36px,4.4vw,60px)">{h1}</h1>
{notice}</div></section>
<section class="section flush-top"><div class="wrap"><div class="prose">{inner}</div></div></section>'''
    write_page(path, title, desc, body, jsonld=[ld], priority="0.3")

def legal():
    h = CFG["hebergeur"]
    editor = "".join([
        br_line("Forme juridique", biz("forme_juridique")),
        br_line("Raison sociale", biz("raison_sociale")),
        br_line("Capital", biz("capital")),
        br_line("SIRET", biz("siret")),
        br_line("RCS", biz("rcs")),
        br_line("Adresse", biz("adresse")),
        br_line("Téléphone", biz("telephone")),
        br_line("E-mail", biz("email")),
        br_line("Directeur de la publication", biz("directeur_publication")),
    ])
    host = " — ".join(x for x in (h.get("nom"), h.get("adresse"), h.get("contact")) if x)
    legal_page("mentions-legales.html", "Mentions légales — Active Sécurité 974", "Mentions légales",
               "",
               f'''<h2>Éditeur</h2>
<p><strong>Active Sécurité 974</strong> (AS974)<br>
{editor}
Site : {E(SITE)}</p>
<h2>Hébergeur</h2>
<p>{E(host)}</p>
<h2>Propriété intellectuelle</h2>
<p>La marque Active Sécurité 974 / AS974 et les contenus originaux du site sont protégés. Les noms, logos et visuels Ajax Systems appartiennent à leurs titulaires ; utilisation dans le cadre du partenariat agréé et des autorisations accordées.</p>
<h2>Responsabilité</h2>
<p>Les informations sont fournies à titre indicatif. Les devis et prestations font l’objet d’échanges personnalisés. Aucune vente en ligne n’est proposée sur ce site. Les coloris affichés sont ceux documentés par le fabricant ; leur disponibilité à La Réunion est confirmée lors du devis.</p>''',
               "Mentions légales du site Active Sécurité 974 (AS974) : éditeur, hébergeur, propriété intellectuelle et responsabilité.")
    who = " — ".join(x for x in ("Active Sécurité 974", biz_txt("adresse"), biz_txt("email"), biz_txt("telephone")) if x)
    legal_page("politique-confidentialite.html", "Politique de confidentialité — Active Sécurité 974", "Politique de confidentialité",
               "",
               f'''<h2>Responsable de traitement</h2>
<p>{E(who)}</p>
<h2>Données collectées</h2>
<p>Via le formulaire de demande de devis : identité, coordonnées, commune, profil, type de site, besoins, message, produits du catalogue éventuellement sélectionnés (modèle, référence, coloris), consentement.</p>
<h2>Finalités</h2>
<p>Répondre aux demandes de devis et d’information ; organiser l’étude et l’installation ; suivi commercial lié à votre demande.</p>
<h2>Base légale</h2>
<p>Mesures précontractuelles / intérêt légitime / consentement (case du formulaire).</p>
<h2>Durée de conservation</h2>
<p>Les données sont conservées le temps de traiter votre demande, puis selon les obligations légales applicables.</p>
<h2>Destinataires</h2>
<p>Personnel habilité d’Active Sécurité 974 et, le cas échéant, l’hébergeur du site{(" (" + E(h["nom"]) + ")") if h.get("nom") else ""}.</p>
<h2>Vos droits</h2>
<p>Accès, rectification, suppression, limitation, opposition, portabilité.{(" Contact : " + biz("email") + ".") if biz("email") else ""} Réclamation possible auprès de la CNIL.</p>
<h2>Cookies</h2>
<p>Voir la page <a href="cookies.html">Cookies</a>.</p>''',
               "Politique de confidentialité d’Active Sécurité 974 : données du formulaire de devis, finalités, durée de conservation et droits RGPD.")
    legal_page("cookies.html", "Cookies — Active Sécurité 974", "Cookies",
               "",
               f'''<h2>Qu’est-ce qu’un cookie ?</h2>
<p>Petit fichier déposé sur votre terminal lors de la visite du site.</p>
<h2>Cookies utilisés</h2>
<p>Ce site ne dépose pas de cookie publicitaire. Aucun outil de mesure d’audience n’est actif pour le moment.</p>
<h2>Stockage local</h2>
<p>La fonction « sélection devis » mémorise uniquement dans votre navigateur (stockage local) les produits que vous ajoutez, pour préremplir le formulaire. Ces informations ne sont transmises que si vous envoyez le formulaire, et vous pouvez les retirer à tout moment depuis la page Contact.</p>
<h2>Gestion</h2>
<p>Vous pouvez configurer votre navigateur pour refuser les cookies. Un bandeau de consentement sera ajouté si des cookies non essentiels sont activés.</p>
{('<h2>Contact</h2><p>' + biz("email") + '</p>') if biz("email") else ''}''',
               "Politique cookies du site Active Sécurité 974 : cookies, stockage local de la sélection devis et gestion de vos préférences.")

def notfound():
    body = f'''<section class="phero notfound"><div class="wrap center">
<p class="eyebrow">Erreur 404</p><h1 class="display" style="font-size:clamp(56px,10vw,140px)">Page introuvable.</h1>
<p class="lead" style="margin:28px auto 0">La page demandée n’existe pas ou a été déplacée.</p>
<div class="btns" style="justify-content:center"><a class="btn btn-dark btn-lg" href="index.html">Retour à l’accueil</a><a class="btn btn-outline btn-lg" href="catalogue.html">Explorer le catalogue</a></div>
</div></section>'''
    # <base> : GitHub Pages sert 404.html sous l’URL manquante (/as974-site/…).
    write_page("404.html", "Page introuvable — Active Sécurité 974", "Cette page n’existe pas ou a été déplacée.", body, noindex=True, pre="", base=SITE + "/")
