"""Pages éditoriales (textes repris des pages v1 validées, mise en page refondue)."""
from core import *
from layout import write_page, crumbs
from components import card, rail, filter_grid, cta, versus, yt, video_ld
import sell
from diagrams import portee, frise, ia, comparatif, en54

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
    n = sum(1 for p in ALL if default_image(p))
    hero = f'''<section class="hero-film on-dark">
<video class="is-hero" poster="assets/video/hero-ia.jpg" autoplay muted loop playsinline preload="auto" aria-label="Caméra Ajax : une personne est détectée dans le jardin">
<source src="assets/video/hero-ia.mp4" type="video/mp4">
</video>
<div class="hero-film-copy wrap">
<p class="eyebrow">Partenaire agréé · La Réunion</p>
<h1 class="display">La sécurité, chez vous.</h1>
<p class="lead">Étude, pose et suivi, sur toute l’île.</p>
<div class="btns"><a class="btn btn-primary btn-lg" href="contact.html#devis">Demander une étude gratuite</a></div>
</div>
</section>'''
    why = f'''<section class="section bg-off"><div class="wrap split-vis">
<div class="vis-copy"><h2 class="h2">Jusqu’à 2 000 m.</h2>
<p>Portée annoncée du Hub 2 en champ libre. Nous la mesurons chez vous.</p>
<p class="src-note">Source : Ajax Systems</p>
{sell.act(pre, "gamme-alarme.html", "Voir l’alarme")}
</div>
<div class="vis-media">{portee()}</div>
</div></section>'''
    duo = f'''<section class="section"><div class="wrap-wide">
<div class="head center"><h2 class="h2">Maison ou activité.</h2>
<p class="lead">La visite est la même. Le devis change avec le lieu.</p></div>
<div class="duo">
<div class="panel light"><h3 class="h2">Votre maison.</h3><p>Une étude chez vous, puis la pose.</p>
<div class="btns"><a class="btn btn-primary" href="contact.html?profil=particulier#devis">Étude pour mon logement</a></div>
<div class="panel-img"><img class="home-shot home-cover" src="assets/img/ajax/ls_house_xl_1894a479bc.jpg" alt="Interrupteur Ajax dans un salon" width="1600" height="900"></div></div>
<div class="panel blue on-dark"><h3 class="h2">Votre activité.</h3><p>Commerce, bureaux, entrepôt, plusieurs sites.</p>
<div class="btns"><a class="btn btn-light" href="contact.html?profil=professionnel#devis">Étude professionnelle</a></div>
<div class="panel-img"><img class="home-shot home-cover" src="assets/img/ajax/entrepot-kramp.jpg" alt="Entrepôt, cas client Ajax Systems" width="1600" height="900"></div></div>
</div></div></section>'''

    chapters = [
        ("alarme", "gamme-alarme.html", "Alarme.", "Détecteurs, claviers et sirènes.", "assets/img/p/c-mc-black-ccad3224b1.png", ""),
        ("incendie", "gamme-incendie.html", "Incendie EN54.", "La ligne des bâtiments.", "assets/img/p/c-en54-fire-hub-white-9fbd4eb73a.png", ""),
        ("video", "gamme-video.html", "Vidéo.", "L’image peut lancer l’alarme.", "assets/img/ajax/ia-pet.jpg", "dark cover"),
        ("domotique", "gamme-domotique.html", "Domotique.", "Lumières, prises, fuites d’eau.", "assets/img/ajax/ls_five_devices_3b8296cb8d.jpg", "cover"),
    ]
    rows = []
    for g, href, h, txt, src, st in chapters:
        cnt = len(group_products(g))
        cover = " home-cover" if "cover" in st else ""
        card = st.replace(" cover", "")
        rows.append(f'''<a class="range-card {card}" href="{href}"><div class="range-media"><img class="home-shot{cover}" src="{src}" alt="{h}"></div><div><h3>{h}</h3><p>{txt}</p><span class="count">{cnt} références</span></div></a>''')
    gammes = f'''<section class="section bg-off" id="gammes"><div class="wrap">
<div class="head"><h2 class="h2">Quatre familles.</h2>
<p class="lead">Une seule application pour tout le système.</p></div>
<div class="range-grid">{"".join(rows)}</div>
{sell.act(pre, "catalogue.html", f"Parcourir les {n} références et demander un devis")}
</div></section>'''

    video_home = ""
    railsec = ""
    process = f'''<section class="section"><div class="wrap split-vis">
<div class="vis-copy"><h2 class="h2">Étude, devis, pose, SAV.</h2>
<p>Quatre étapes. Un seul interlocuteur, chez vous.</p>
{sell.act(pre, "services-installation.html", "Voir l’installation")}
</div>
<div class="vis-media">{frise()}</div>
</div></section>'''
    day = f'''<section class="section bg-off" id="quotidien"><div class="wrap split-vis">
<div class="vis-copy"><h2 class="h2">L’application, au quotidien.</h2>
<p>Vous armez, vous lisez l’alerte, vous coupez une lumière.</p>
{sell.act(pre)}
</div>
<div class="app-stage">
<div class="app-screen is-arm"><header><b>Maison</b><em>Armé</em></header>
<ul><li><span>Entrée</span><strong>Fermée</strong></li><li><span>Salon</span><strong>Calme</strong></li><li><span>Jardin</span><strong>Calme</strong></li></ul></div>
<div class="app-screen is-alert"><header><b>Alerte</b><em>Maintenant</em></header>
<ul><li><span>Jardin</span><strong>Mouvement</strong></li><li><span>Sirène</span><strong>Active</strong></li><li><span>Photo</span><strong>En cours</strong></li></ul></div>
<div class="app-screen is-photo"><img src="assets/img/ajax/ia-human.jpg" alt=""><header><b>Levée de doute</b><em>Photo</em></header></div>
<div class="app-screen is-scene"><header><b>Scénario</b><em>Fait</em></header>
<ul><li><span>Salon</span><strong>Lumière coupée</strong></li><li><span>Déclencheur</span><strong>Armement</strong></li><li><span>Prise</span><strong>Coupée</strong></li></ul></div>
</div>
</div></section>'''
    ia_block = f'''<section class="section"><div class="wrap">
<div class="head"><h2 class="h2">Personne, véhicule, animal.</h2>
<p class="lead">La caméra peut lancer la sirène. Baseline et Superior.</p></div>
<div class="ia-row">
<figure><img src="assets/img/ajax/ia-human.jpg" alt="Détection d’une personne dans le jardin"><figcaption>Personne</figcaption></figure>
<figure><img src="assets/img/ajax/ia-pet.jpg" alt="Détection d’un animal"><figcaption>Animal</figcaption></figure>
<figure><img src="assets/img/ajax/ia-reglage.jpg" alt="Réglage officiel : personne, animal, véhicule"><figcaption>Véhicule, dans le réglage</figcaption></figure>
</div>
{sell.act(pre, "gamme-video.html", "Voir la vidéo")}
</div></section>'''
    why_as = f'''<section class="section bg-off"><div class="wrap split-vis">
<div class="vis-copy"><h2 class="h2">Pourquoi AS974.</h2>
<p>Une étude, un devis, une pose. Pas un kit à monter seul.</p>
{sell.act(pre, "a-propos.html", "À propos")}
</div>
<div class="vis-media">{comparatif()}</div>
</div></section>'''
    catalogue_band = f'''<section class="section"><div class="wrap">
<div class="head"><h2 class="h2">Le catalogue.</h2>
<p class="lead">{n} références, chacune avec ses coloris.</p></div>
<div class="range-grid home-picks">
<a class="range-card" href="produits/hub-2.html"><div class="range-media"><img class="home-shot" src="assets/img/p/c-hub2-4g-white-e143ae613b.png" alt="Hub 2"></div><div><h3>Hub 2</h3><p>La centrale.</p></div></a>
<a class="range-card" href="produits/motioncam-phod.html"><div class="range-media"><img class="home-shot" src="assets/img/p/c-mc-black-ccad3224b1.png" alt="MotionCam"></div><div><h3>MotionCam</h3><p>La photo en alarme.</p></div></a>
<a class="range-card" href="produits/streetsiren.html"><div class="range-media"><img class="home-shot" src="assets/img/p/c-ss-black-1154b5ea2b.png" alt="Sirène extérieure Ajax"></div><div><h3>Sirène</h3><p>Dehors, bien visible.</p></div></a>
<a class="range-card" href="catalogue.html"><div class="range-media"><img class="home-shot home-cover" src="assets/img/ajax/ls_four_devices_7d8b0f118d.jpg" alt="Ensemble d’interrupteurs et de prises Ajax"></div><div><h3>Et le reste.</h3><p>Tout le catalogue.</p></div></a>
</div>
{sell.act(pre, "catalogue.html", "Ouvrir le catalogue")}
</div></section>'''

    faq_home = "".join(
        f'<details class="faq"><summary>{E(q)}</summary><p>{E(a)}</p></details>'
        for q, a in (
            ("Où intervenez-vous ?", "Chez vous, sur toute l’île."),
            ("L’étude est-elle gratuite ?", "Oui, sans engagement."),
            ("Y a-t-il un prix affiché ?", "Non. Le prix est dans le devis."),
            ("Baseline et Superior voient-ils pareil ?", "Les deux reconnaissent personnes, véhicules et animaux."),
        )
    )
    faqsec = f'''<section class="section"><div class="wrap faq-home"><h2 class="h2">Questions fréquentes.</h2>{faq_home}<p class="act"><a class="btn btn-primary" href="faq.html">Toutes les questions</a></p></div></section>'''
    delay = biz("delai_reponse")
    cta_text = "Étude et devis gratuits. Partenaire agréé Ajax Systems." + (f" Réponse sous {delay}." if delay else "")
    final = f'''<section class="section cta-photo"><div class="wrap split-vis">
<div class="vis-media"><img class="home-shot" src="assets/img/p/c-hub2-4g-white-e143ae613b.png" alt="Centrale Hub 2"></div>
<div class="vis-copy"><h2 class="h2">Demandez l’étude.</h2>
<p>Gratuite, chez vous, sur toute l’île.</p>
<div class="btns"><a class="btn btn-primary btn-lg" href="contact.html#devis">Demander une étude gratuite</a></div>
</div></div></section>'''
    faqsec = faqsec.replace("<section class=\"section\">", "<section class=\"section bg-off\">", 1)
    body = hero + duo + why + ia_block + day + process + why_as + gammes + catalogue_band + faqsec + final
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
<p class="lead">Une étude chez vous, puis la pose.</p>
<div class="btns"><a class="btn btn-primary btn-lg" href="contact.html?profil=particulier#devis">Étude gratuite pour mon logement</a><a class="btn btn-outline btn-lg" href="catalogue.html">Explorer le catalogue</a></div></div>
<div class="phero-media reveal d1">{stage_img("motionprotect", "Blanc", pre, SZ_SPLIT, eager=True)}</div>
</div></section>
<section class="section bg-off"><div class="wrap">
<div class="head reveal"><p class="eyebrow">Besoins typiques</p><h2 class="h2">Ce que nous protégeons chez vous.</h2></div>
<ol class="numlist reveal">
<li><h3>Maison et appartement</h3><p>Ouvertures, volumes, abords.</p></li>
<li><h3>Résidence secondaire</h3><p>Alerte à distance, photo pour lever le doute.</p></li>
<li><h3>Absence</h3><p>Armement et scénarios, depuis l’application.</p></li>
<li><h3>Animaux</h3><p>Immunité animaux, selon le détecteur Ajax.</p></li>
<li><h3>Application</h3><p>Armement, historique, notifications.</p></li>
<li><h3>Photo</h3><p>Une image en cas d’alarme.</p></li>
</ol>
</div></section>
<section class="section"><div class="wrap">
<div class="split">
<div class="split-media dark reveal">{stage_img("motioncam-phod", "Noir", pre, SZ_SPLIT, need_alpha=True)}</div>
<div class="split-txt reveal d1"><p class="num">Photo-vérification</p><h2 class="h2">Une photo, pas seulement une alerte.</h2><p class="lead">Une image pour lever le doute, sans vous déplacer.</p>
<div class="btns"><a class="btn btn-dark" href="produits/motioncam-phod.html">Voir MotionCam (PhOD)</a></div></div>
</div>
<div class="split rev">
<div class="split-media reveal">{stage_img("doorbell", "Graphite", pre, SZ_SPLIT)}</div>
<div class="split-txt reveal d1"><p class="num">Au quotidien</p><h2 class="h2">Tout, depuis votre smartphone.</h2><p class="lead">Armement, alertes et scénarios, dans une application.</p>
<div class="btns"><a class="btn btn-dark" href="gamme-domotique.html">Découvrir la domotique</a></div></div>
</div>
</div></section>
<section class="section bg-off"><div class="wrap">
<div class="head reveal"><p class="eyebrow">Approche</p><h2 class="h2">Baseline pour l’essentiel, Superior si besoin.</h2><p class="lead">Baseline pour l’essentiel. Superior si le projet l’exige.</p></div>
{versus(pre, None, "gamme-alarme.html", "catalogue.html?gamme=superior#references")}
</div></section>
<section class="section"><div class="wrap">
{rail(pick(["hub-2", "doorprotect", "motioncam-phod", "homesiren", "keypad-touchscreen", "doorbell", "fireprotect-2-smoke-heat-co", "leaksprotect"]), pre, "Produits phares", "Matériel souvent recommandé.", ("catalogue.html", "Tout le catalogue"))}
</div></section>
{cta(pre, "Étude gratuite pour votre logement.", "Intervention à domicile sur toute l’île. Devis sans engagement.", href="contact.html?profil=particulier#devis")}'''
    body += sell.etude("alarme") + sell.pose("alarme") + sell.pourquoi("alarme")
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
{yt("o8VNaCPCydE", "De la détection à la réaction", "Les caméras peuvent déclencher une réaction. Vidéo Ajax Systems, en français.")}
<p class="mt-28"><a class="link" href="gamme-incendie.html">Système incendie professionnel EN54</a></p>
</div></section>
<section class="section bg-ink on-dark"><div class="wrap">
<p class="eyebrow reveal">Après la pose</p>
<p class="statement reveal">Un suivi dans la durée. <span class="dim">Maintenance selon le contrat défini ensemble.{(" " + telesurv()) if telesurv() else ""}</span></p>
<div class="btns reveal"><a class="btn btn-light" href="services.html">Voir les services</a></div>
</div></section>
{cta(pre, "Parlons de votre site.", "Étude professionnelle sur place, sur toute l’île.", "Demander une étude professionnelle", "contact.html?profil=professionnel#devis")}'''
    body += sell.etude("alarme") + sell.pose("alarme") + sell.pourquoi("alarme")
    write_page("professionnels.html", "Sécurité professionnelle Ajax à La Réunion — Superior et EN54 | AS974",
               "Sécurité pour commerces, bureaux et plusieurs sites à La Réunion : ligne vidéo Superior, incendie EN54 et applications Ajax PRO. Étude sur place par Active Sécurité 974.",
               body, jsonld=[ld, video_ld("o8VNaCPCydE", "De la détection à la réaction", "Les caméras Ajax peuvent lancer une réaction automatique.")], priority="0.9")

# ====================================================================== GAMMES
GAMME_PAGES = {
    "alarme": ("gamme-alarme.html", "Alarme intrusion", "Détecteurs, claviers et sirènes. Baseline sans fil, Superior si le site l’exige.",
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
    "domotique": ("gamme-domotique.html", "Domotique", "Prises, relais et interrupteurs, dans la même application que l’alarme.",
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
<p class="lead">Deux lignes, Baseline et Superior. Les deux peuvent lancer l’alarme.</p>
<div class="btns"><a class="btn btn-primary btn-lg" href="#ia">Voir la reconnaissance</a><a class="btn btn-outline btn-lg" href="catalogue-video.html">Voir les {len(prods)} références</a></div></div>
</div></section>
<section class="section flush-top" id="ia"><div class="wrap">
<div class="split">
<div class="reveal">{video_block(pre)}</div>
<div class="split-txt reveal d1"><p class="eyebrow">Commun aux deux lignes</p><h2 class="h2">Personnes, véhicules, animaux.</h2>
<p class="lead">Personnes, véhicules et animaux. Baseline comme Superior.</p>
<p class="src-note">Source : Ajax Systems</p>
</div>
</div>
</div></section>
<section class="section bg-off" id="baseline"><div class="wrap">
<div class="head reveal"><span class="tag tag-base">Baseline</span><h2 class="h2">La ligne essentielle.</h2>
<p class="lead">Caméras, sonnette et enregistreurs, pour la maison et les petits sites.</p>
<p class="src-note">Source : Ajax Systems</p></div>
<div class="feature-grid">
<article class="feature"><h3>Caméras</h3><p>BulletCam, TurretCam et DomeCam Mini.</p><details class="more"><summary>En savoir plus</summary><p>Infrarouge ou éclairage hybride. Les versions HLVF ajoutent un objectif 2,8–12 mm, le True WDR et des entrées audio et alarme. Le catalogue Baseline indique un matériel conforme NDAA.</p></details></article>
<article class="feature"><h3>Aussi dans Baseline</h3><p>IndoorCam et DoorBell, dans la même application.</p></article>
<article class="feature"><h3>Enregistreurs</h3><p>NVR, NVR H et NVR H2D.</p></article>
</div>
<p class="mt-28"><a class="btn btn-dark" href="catalogue-video.html?gamme=baseline#references">{len(base)} références Baseline</a></p>
</div></section>
<section class="section" id="superior"><div class="wrap">
<div class="head reveal"><span class="tag tag-sup">Superior</span><h2 class="h2">La ligne pour les sites exigeants.</h2>
<p class="lead">Une image plus fine, une IA enrichie, plus d’options.</p>
<details class="more"><summary>En savoir plus</summary><p>Ajax décrit une qualité visuelle plus haute et une IA enrichie. La reconnaissance des personnes, des véhicules et des animaux, et le déclenchement de l’alarme, restent ceux de Baseline.</p></details></div>
<div class="feature-grid">
<article class="feature"><h3>Caméras HLVF</h3><p>BulletCam, DomeCam et TurretCam, objectif 2,8–12 mm.</p><details class="more"><summary>En savoir plus</summary><p>Optique P-Iris, éclairage hybride, True WDR, microphone et haut-parleur, entrées audio et alarme, PoE ou 12 V.</p></details></article>
<article class="feature"><h3>Enregistreurs</h3><p>Superior NVR H2D, HDMI 4K, deux disques.</p><details class="more"><summary>En savoir plus</summary><p>IA intégrée, disques remplaçables à chaud, ports PoE ou double Gigabit selon le modèle, de 8 à 32 canaux.</p></details></article>
<article class="feature"><h3>Pour qui</h3><p>Sites professionnels et projets ambitieux.</p></article>
</div>
<p class="mt-28"><a class="btn btn-dark" href="catalogue-video.html?gamme=superior#references">{len(sup)} références Superior</a> <a class="btn btn-outline" href="professionnels.html#video-superior">Côté professionnels</a></p>
</div></section>
<section class="section bg-off"><div class="wrap">
<div class="head reveal"><p class="eyebrow">Ce qui change</p><h2 class="h2">Baseline et Superior détectent personnes, véhicules et animaux.</h2></div>
<table class="spec compare-video">
<tr><th scope="col"> </th><th scope="col">Baseline</th><th scope="col">Superior</th></tr>
<tr><th scope="row">IA personnes, véhicules, animaux</th><td>Oui, intégrée. Peut déclencher l’alarme.</td><td>Oui, la même base, avec une IA enrichie.</td></tr>
<tr><th scope="row">Caméras</th><td>BulletCam, TurretCam, DomeCam Mini, versions IR, HL et HLVF. IndoorCam, DoorBell.</td><td>Superior BulletCam, DomeCam et TurretCam HLVF.</td></tr>
<tr><th scope="row">Objectif</th><td>Fixe sur IR et HL. Varifocal motorisé 2,8–12 mm sur HLVF.</td><td>Varifocal motorisé P-Iris 2,8–12 mm.</td></tr>
<tr><th scope="row">Nuit et audio</th><td>Infrarouge, ou couleur avec l’éclairage hybride (HL / HLVF). Microphone.</td><td>Éclairage hybride, microphone et haut-parleur.</td></tr>
<tr><th scope="row">Enregistreurs</th><td>NVR, NVR H, NVR H2D.</td><td>Superior NVR H2D, HDMI 4K, deux disques, IA.</td></tr>
</table>
<p class="src-note">Source : Ajax Systems</p>
</div></section>
<section class="section"><div class="wrap">
{rail([p for p in base if p["slug"] in ("bulletcam","turretcam","domecam-mini","indoorcam","doorbell","nvr")] or base[:6], pre, "Baseline", "Caméras et enregistreurs essentiels.", ("catalogue-video.html?gamme=baseline#references", "Toute la ligne Baseline"))}
</div></section>
<section class="section bg-off"><div class="wrap">
{rail(sup[:8], pre, "Superior", "Caméras HLVF et NVR pour les sites exigeants.", ("catalogue-video.html?gamme=superior#references", "Toute la ligne Superior"))}
</div></section>
{cta(pre, "Un projet vidéo ?", "Étude chez vous, sur toute l’île. Baseline ou Superior, selon le site.")}
{sell.blocs("video", prods, pre)}'''
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
    prods = [p for p in ALL if p["gamme"] == "EN54 Line" or str(p["slug"]).startswith("en54-") or str(p["slug"]).startswith("manualcallpoint-")]
    cr, ld = crumbs(pre, [("professionnels.html", "Professionnels"), (None, "Incendie EN54")])
    arch = f'''<section class="section"><div class="wrap split-vis">
<div class="vis-copy"><h2 class="h2">La ligne des bâtiments.</h2>
<p>Centrale, détecteurs, sirènes, déclencheur rouge, module et prolongateur.</p>
<p class="src-note">Source : Ajax Systems</p>
{sell.act(pre, "contact.html?profil=professionnel#devis", "Demander une étude EN54")}
</div>
<div class="vis-media">{en54()}</div>
</div></section>
<section class="section bg-off"><div class="wrap split-vis">
<div class="vis-copy"><h2 class="h2">Étude, pose, maintenance.</h2>
<p>Nous venons sur le bâtiment, puis nous mettons en service.</p>
{sell.act(pre, "services-maintenance.html", "Voir le suivi")}
</div>
<div class="vis-media">{frise()}</div>
</div></section>'''
    body = f'''<section class="phero"><div class="wrap phero-split crumbs-first">
<div>{cr}<p class="eyebrow">Professionnels · EN54 Line</p><h1 class="h1">Incendie certifié EN 54, pour les bâtiments.</h1>
<p class="lead">Centrale, détecteurs, sirènes et modules, pour les bâtiments.</p>
<div class="btns"><a class="btn btn-primary btn-lg" href="contact.html?profil=professionnel#devis">Demander une étude EN54</a><a class="btn btn-outline btn-lg" href="catalogue-incendie.html">Voir les {len(prods)} références de la ligne</a></div></div>
<div class="phero-media">{stage_img("en54-fire-hub-jeweller", "Blanc", pre, SZ_SPLIT, eager=True)}</div>
</div></section>
{arch}
{sell.blocs("incendie", prods, pre)}'''
    itemlist = {"@context": "https://schema.org", "@type": "ItemList", "name": "Ajax EN54 Line",
                "itemListElement": [{"@type": "ListItem", "position": i, "name": p["name"], "url": f"{SITE}/produits/{p['slug']}.html"} for i, p in enumerate(prods, 1)]}
    write_page("gamme-incendie.html",
               "Incendie EN54 Ajax à La Réunion — centrale, détecteurs, déclencheurs | AS974",
               "Ligne professionnelle Ajax EN54 pour ERP, entreprises et bâtiments à La Réunion : centrale Fire Hub, détecteurs, déclencheurs, sirènes et modules. Étude par Active Sécurité 974.",
               body, jsonld=[ld, itemlist], priority="0.8")

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
        extra = f'''<section class="section bg-off" id="completer"><div class="wrap prose">
<h2 class="h2">Compléter votre alarme.</h2>
<p>Fumée, chaleur ou monoxyde, dans la même application que l’alarme.</p>
<details class="more"><summary>En savoir plus</summary><p>Ces détecteurs complètent une alarme Baseline. Un bâtiment se traite avec la ligne EN54.</p></details>
</div>
<div class="wrap">
{rail(fire, pre, "Avec l’alarme", "Les détecteurs de logement du catalogue.", ("catalogue-alarme.html?sous=detecteurs-d-incendie#references", "Toutes ces références dans le catalogue alarme"))}
{sell.act(pre, "contact.html#devis", "Les ajouter à une étude d’alarme")}
</div></section>'''
    if g == "domotique":
        extra = f'''<section class="section"><div class="wrap">
<div class="head reveal"><h2 class="h2">Scénarios dans l’application.</h2>
<p class="lead">Prises, relais et interrupteurs Ajax réagissent à l’armement, à une alarme ou à une température.</p></div>
<div class="duo-yt">{yt("o8VNaCPCydE", "De la détection à la réaction", "Les caméras Ajax peuvent lancer une réaction. Vidéo Ajax Systems, en français.")}</div>
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
    kind = {"alarme": "alarme", "domotique": "domotique"}.get(g, "alarme")
    extra_cfg = ""
    if g == "domotique":
        devices = []
        for p in prods:
            if not (p["slug"].startswith("lightswitch") or p["slug"].startswith("outlet")):
                continue
            ims = product_images(p)
            images = {}
            for col, meta in ims.items():
                if not col:
                    continue
                _ss, fb = img_urls(meta, pre)
                images[col] = fb
            devices.append({"slug": p["slug"], "name": p["name"], "model": p["model"],
                            "kind": "prise" if p["slug"].startswith("outlet") else "interrupteur", "images": images})
        extra_cfg = sell.configurateur(devices)
    body = body + extra_cfg + sell.blocs(kind, prods, pre)
    lds = [ld]
    if g == "domotique":
        lds.append(video_ld("o8VNaCPCydE", "De la détection à la réaction", "Les caméras Ajax peuvent lancer une réaction automatique."))
    write_page(path, title, desc, body, jsonld=lds, priority="0.8")

# ====================================================================== CATALOGUE
CAT_LEADS = {
    "centrales": "Le cœur de votre système Ajax Systems : centrales, kits et prolongateurs de portée. Dimensionnés et installés par Active Sécurité 974 sur toute l’île.",
    "alarme": "Détecteurs, claviers, sirènes et commandes. Baseline pour l’essentiel sans fil ; Superior pour les projets exigeants.",
    "incendie": "Uniquement la ligne professionnelle Ajax EN54 : centrale, détecteurs, déclencheurs, sirènes, flashs et modules. Les détecteurs de logement sont dans l’alarme.",
    "video": "Caméras, sonnette et NVR Ajax Systems, intégrés à l’écosystème alarme, sur devis et installation AS974.",
    "domotique": "Prises, relais, éclairage, détection de fuite et qualité de l’air : automatisez le quotidien dans la même application.",
    "accessoires": "Modules d’intégration, alimentations, boîtiers et accessoires de pose pour compléter et raccorder votre installation.",
}
CAT_IMG = {"centrales": ("starterkit", "Blanc"), "alarme": ("motioncam-phod", "Noir"), "incendie": ("en54-fire-hub-jeweller", "Blanc"),
           "video": ("turretcam", "Blanc"), "domotique": ("socket", "Blanc"), "accessoires": ("button", "Blanc")}

def gamme_acces():
    pre = ""
    prods = [p for p in ALL if p["category"] in ("Claviers", "Boutons & télécommandes") or p["slug"].startswith("tag-") or p["slug"].startswith("pass-")]
    cr, ld = crumbs(pre, [(None, "Contrôle d’accès")])
    body = f'''<section class="phero"><div class="wrap">
{cr}<h1 class="h1">Qui arme, qui entre, qui est prévenu.</h1>
<p class="lead">Claviers, badges et télécommandes. Une gâche seulement si l’étude la retient.</p>
<div class="btns"><a class="btn btn-primary btn-lg" href="contact.html#devis">Demander une étude des accès</a></div>
</div></section>
{sell.blocs("acces", prods, pre)}'''
    write_page("gamme-acces.html", "Contrôle d’accès Ajax à La Réunion — claviers, Tag, Pass | AS974",
               "Claviers, badges Tag et Pass, télécommandes Ajax. Droits utilisateurs et groupes, étudiés et posés par Active Sécurité 974 sur toute l’île.",
               body, jsonld=[ld], priority="0.8")


def catalogue_index():
    pre = ""
    cr, ld = crumbs(pre, [(None, "Catalogue")])
    layout = [("alarme", "w4 dark"), ("centrales", "w2 hubs"), ("video", "w3"), ("incendie", "w3"), ("domotique", "w3"), ("accessoires", "w3")]
    tiles = []
    for i, (g, cls) in enumerate(layout):
        s, c = CAT_IMG[g]
        n = len(group_products(g))
        tiles.append(f'''<article class="chap {cls} reveal{' d1' if i % 2 else ''}"><h3><a class="cover" href="catalogue-{g}.html">{E(GROUP[g]["label"])}</a></h3><p>{E(GROUP[g]["intro"])}</p><p class="count">{n} références →</p>
<div class="chap-img">{stage_img(s, c, pre, "(max-width:640px) 70vw, 360px", need_alpha=("dark" in cls))}</div></article>''')
    body = f'''<section class="phero"><div class="wrap">
<div class="reveal">{cr}<p class="eyebrow">Catalogue</p><h1 class="h1">Matériel Ajax Systems,<br>sur devis.</h1>
<p class="lead">Explorez {sum(1 for p in ALL if default_image(p))} références illustrées. Chaque fiche propose « Demander un devis ». Installation sur toute l’île par Active Sécurité 974, partenaire agréé Ajax Systems.</p>
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
    shown = sum(1 for p in ALL if default_image(p))
    write_page("catalogue.html", f"Catalogue Ajax Systems sur devis — {shown} références | AS974",
               f"Catalogue de {shown} références Ajax Systems : centrales, alarme, incendie, vidéosurveillance, domotique, accessoires. Sur devis, installation à La Réunion.",
               body, jsonld=[ld, itemlist], priority="0.9")

def catalogue_cat(g):
    pre = ""
    prods = group_products(g)
    if g == "incendie":
        prods = [p for p in prods if p["gamme"] == "EN54 Line" or str(p["slug"]).startswith("en54-") or str(p["slug"]).startswith("manualcallpoint-")]
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
{sell.blocs({"alarme":"alarme","video":"video","incendie":"incendie","domotique":"domotique","centrales":"alarme","accessoires":"accessoires"}.get(g,"alarme"), prods, pre)}
{cta(pre, "Besoin d’aide pour composer votre système ?", "Étude gratuite. Partenaire agréé. Intervention sur site, sur toute l’île.", "Demander un devis")}'''
    write_page(f"catalogue-{g}.html", f"{label} — catalogue Ajax Systems sur devis ({len(prods)} réf.) | AS974",
               clip(f"{label} : {len(prods)} références Ajax Systems sur devis. {GROUP[g]['intro']} Installation par Active Sécurité 974 à La Réunion."),
               body, jsonld=[ld], priority="0.8")

# ====================================================================== SERVICES / À PROPOS
def services():
    pre = ""
    cr, ld = crumbs(pre, [(None, "Services")])
    body = f'''<section class="phero"><div class="wrap">
<div class="reveal">{cr}<p class="eyebrow">Services</p><h1 class="h1">Étude, installation, suivi.</h1>
<p class="lead">De la visite à la mise en service, chez vous.</p></div>
</div></section>
<section class="section flush-top"><div class="wrap">
<div class="split">
<div class="split-media reveal">{stage_img("hub2-plus", "Blanc", pre, SZ_SPLIT)}</div>
<div class="split-txt reveal d1"><p class="num">01 — Étude &amp; devis gratuit</p><h2 class="h2">Comprendre avant de proposer.</h2><p class="lead">Visite chez vous. Devis clair, sans engagement.</p>
<div class="btns"><a class="btn btn-primary" href="contact.html#devis">Prendre rendez-vous d’étude</a></div></div>
</div>
<div class="split rev">
<div class="split-media dark reveal">{stage_img("keypad-touchscreen", "Noir", pre, SZ_SPLIT, need_alpha=True)}</div>
<div class="split-txt reveal d1"><p class="num">02 — Installation</p><h2 class="h2">Une pose soignée, chez vous.</h2><p class="lead">Pose, réglages, puis prise en main de l’application.</p>
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
<div class="duo-yt">{yt("o8VNaCPCydE", "De la détection à la réaction", "Les caméras Ajax peuvent lancer une réaction. Vidéo en français.")}{yt("NLnFmO16dXI", "Les applications Ajax", "Retrouver un appareil ou un utilisateur dans l’application.")}</div>
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
        shot = {"services-etude.html": ("hub-2", "Blanc"), "services-installation.html": ("keypad-touchscreen", "Noir"), "services-maintenance.html": ("streetsiren", "Blanc")}[path]
        write_page(path, f"{h1} — Active Sécurité 974 à La Réunion",
                   f"{h1} par Active Sécurité 974, chez vous, sur toute l’île de La Réunion.",
                   f'''<section class="phero"><div class="wrap phero-split">{cr2}<div><h1 class="h1">{h1}</h1><p class="lead">{lead}</p></div>
<div class="phero-media">{stage_img(shot[0], shot[1], pre, SZ_SPLIT, eager=True)}</div></div></section>
<section class="section flush-top"><div class="wrap"><ol class="numlist">{lis}</ol></div></section>
{sell.pose("alarme") if "installation" in path else sell.etude("alarme") if "etude" in path else sell.pourquoi("alarme")}
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
<li><h3>Approche conseil</h3><p>Baseline ou Superior selon le site, avec un devis clair.</p></li>
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
    ("Où sont les détecteurs de fumée pour une maison ?",
     "Sur la page Alarme, dans « Compléter votre alarme ». FireProtect, FireProtect Plus et FireProtect 2 ne font pas partie de la page Incendie. Cette page est réservée à la ligne professionnelle EN54, pour les bâtiments."),
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
<section class="section flush-top"><div class="wrap"><div class="faq-col">{blocks}</div>
<div class="duo-yt mt-28">{yt("NLnFmO16dXI", "Les applications Ajax", "Trouver un appareil ou un utilisateur dans les applications Ajax.")}{yt("o8VNaCPCydE", "De la détection à la réaction", "Les caméras peuvent lancer une réaction. Vidéo Ajax Systems, en français.")}</div>
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

def sources():
    pre = ""
    cr, ld = crumbs(pre, [(None, "Sources")])
    body = f'''<section class="phero"><div class="wrap">{cr}<h1 class="h1">Sources.</h1>
<p class="lead">Les chiffres et les normes cités sur ce site viennent des documents publics d’Ajax Systems. Ils ne sont pas des liens : le contenu utile est repris ici.</p></div></section>
<section class="section flush-top"><div class="wrap prose">
<ul class="ref-index">
<li><span>Fiche Hub 2</span></li>
<li><span>Fiche MotionProtect</span></li>
<li><span>Fiche LightSwitch (1-gang) et manuel des cadres</span></li>
<li><span>Catalogues vidéo Baseline et Superior</span></li>
<li><span>Page du système certifié EN 54</span></li>
</ul>
<p class="src-note">Source : Ajax Systems</p>
{sell.act(pre)}
</div></section>'''
    write_page("sources.html", "Sources — Active Sécurité 974",
               "Origine des chiffres et des normes cités sur le site Active Sécurité 974.",
               body, jsonld=[ld], priority="0.2")


def notfound():
    body = f'''<section class="phero notfound"><div class="wrap center">
<p class="eyebrow">Erreur 404</p><h1 class="display" style="font-size:clamp(56px,10vw,140px)">Page introuvable.</h1>
<p class="lead" style="margin:28px auto 0">La page demandée n’existe pas ou a été déplacée.</p>
<div class="btns" style="justify-content:center"><a class="btn btn-dark btn-lg" href="index.html">Retour à l’accueil</a><a class="btn btn-outline btn-lg" href="catalogue.html">Explorer le catalogue</a></div>
</div></section>'''
    # <base> : GitHub Pages sert 404.html sous l’URL manquante (/as974-site/…).
    write_page("404.html", "Page introuvable — Active Sécurité 974", "Cette page n’existe pas ou a été déplacée.", body, noindex=True, pre="", base=SITE + "/")
