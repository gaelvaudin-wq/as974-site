"""Schémas SVG, charte AS974 : noir, rouge, jaune, bleu."""

def _svg(body, label):
    return (
        f'<svg class="schema" viewBox="0 0 640 360" role="img" aria-label="{label}">'
        f'<rect width="640" height="360" rx="28" fill="#F5F5F7"/>{body}</svg>'
    )

def chaine():
    nodes = [
        (70, "Détecteur", "#0B0B0C"),
        (210, "Centrale", "#E10600"),
        (350, "Application", "#0A4D8C"),
        (490, "Télésurveillance", "#F5C518"),
    ]
    parts = []
    for i, (x, name, color) in enumerate(nodes):
        ink = "#0B0B0C" if color == "#F5C518" else "#fff"
        parts.append(f'<rect x="{x}" y="120" width="110" height="88" rx="18" fill="{color}"/>')
        parts.append(f'<text x="{x+55}" y="170" text-anchor="middle" fill="{ink}" font-size="15" font-family="Inter,sans-serif">{name}</text>')
        if i < 3:
            parts.append(f'<path d="M{x+114} 164 H{x+150}" stroke="#0B0B0C" stroke-width="3" fill="none"/>')
    parts.append('<text x="320" y="280" text-anchor="middle" fill="#0B0B0C" font-size="16" font-family="Inter,sans-serif">Du capteur à la décision, dans une seule chaîne.</text>')
    return _svg("".join(parts), "Chaîne détecteur, centrale, application et télésurveillance")

def portee():
    return (
        '<svg class="schema schema-lg" viewBox="0 0 640 560" role="img" aria-label="Schéma de portée radio Jeweller">'
        '<rect width="640" height="560" rx="28" fill="#F5F5F7"/>'
        '<circle cx="300" cy="300" r="210" fill="none" stroke="#0A4D8C" stroke-width="4"/>'
        '<circle cx="300" cy="300" r="128" fill="none" stroke="#E10600" stroke-width="4"/>'
        '<circle cx="300" cy="300" r="18" fill="#0B0B0C"/>'
        '<text x="300" y="52" text-anchor="middle" fill="#0B0B0C" font-size="22" font-family="Inter,sans-serif">Portée radio en champ libre</text>'
        '<text x="430" y="130" fill="#0A4D8C" font-size="18" font-family="Inter,sans-serif">Hub 2 · 2 000 m</text>'
        '<text x="360" y="210" fill="#E10600" font-size="18" font-family="Inter,sans-serif">EN54 · 1 800 m</text>'
        '<text x="300" y="530" text-anchor="middle" fill="#5F5F64" font-size="16" font-family="Inter,sans-serif">Les murs se vérifient sur place.</text>'
        '</svg>'
    )

def ia():
    items = [("Personne", "#E10600"), ("Véhicule", "#0A4D8C"), ("Animal", "#F5C518")]
    bits = []
    for i, (name, color) in enumerate(items):
        x = 70 + i * 190
        ink = "#0B0B0C" if color == "#F5C518" else "#fff"
        bits.append(f'<rect x="{x}" y="90" width="160" height="140" rx="24" fill="{color}"/>')
        bits.append(f'<text x="{x+80}" y="170" text-anchor="middle" fill="{ink}" font-size="18" font-family="Inter,sans-serif">{name}</text>')
    bits.append('<text x="320" y="290" text-anchor="middle" fill="#0B0B0C" font-size="16" font-family="Inter,sans-serif">Baseline et Superior peuvent lancer l’alarme.</text>')
    return _svg("".join(bits), "Détection IA personnes, véhicules et animaux")

def en54():
    boxes = [
        (40, 40, "Centrale EN54"),
        (230, 40, "Détecteurs"),
        (420, 40, "Sirènes et flashs"),
        (40, 190, "Déclencheur rouge"),
        (230, 190, "Module E/S"),
        (420, 190, "Prolongateur"),
    ]
    bits = []
    for x, y, name in boxes:
        bits.append(f'<rect x="{x}" y="{y}" width="180" height="72" rx="16" fill="#0B0B0C"/>')
        bits.append(f'<text x="{x+90}" y="{y+42}" text-anchor="middle" fill="#fff" font-size="14" font-family="Inter,sans-serif">{name}</text>')
    return _svg("".join(bits), "Architecture de la ligne EN54")

def steps():
    items = [
        ("assets/img/ajax/ls_house_xl_1894a479bc.jpg", "Visite dans un salon", "Étude", "Nous venons voir le lieu."),
        ("assets/img/p/c-hub2-4g-white-e143ae613b.png", "Centrale Hub 2", "Devis", "Le prix est dans le devis."),
        ("assets/img/p/c-ss-black-1154b5ea2b.png", "Sirène extérieure", "Installation", "Pose et essais chez vous."),
        ("assets/img/ajax/pro-app.jpg", "Application Ajax", "Mise en service", "Vous armez depuis l’application."),
        ("assets/img/ajax/entrepot-kramp.jpg", "Entrepôt, cas client Ajax", "SAV", "Nous restons joignables."),
    ]
    lis = []
    for i, (src, alt, title, text) in enumerate(items, 1):
        lis.append(
            f'<li class="step"><img src="{src}" alt="{alt}">'
            f'<div><span>{i}</span><h3>{title}</h3><p>{text}</p></div></li>'
        )
    return f'<ol class="steps">{"".join(lis)}</ol>'


def frise():
    steps = ["Étude", "Devis", "Pose", "SAV"]
    colors = ["#0A4D8C", "#E10600", "#0B0B0C", "#F5C518"]
    bits = ['<path d="M50 180 H590" stroke="#0B0B0C" stroke-width="3"/>']
    for i, (name, color) in enumerate(zip(steps, colors)):
        x = 70 + i * 145
        ink = "#0B0B0C" if color == "#F5C518" else "#fff"
        bits.append(f'<circle cx="{x+40}" cy="180" r="28" fill="{color}"/>')
        bits.append(f'<text x="{x+40}" y="186" text-anchor="middle" fill="{ink}" font-size="14" font-family="Inter,sans-serif">{i+1}</text>')
        bits.append(f'<text x="{x+40}" y="250" text-anchor="middle" fill="#0B0B0C" font-size="16" font-family="Inter,sans-serif">{name}</text>')
    return _svg("".join(bits), "Parcours étude, devis, pose et SAV")

def comparatif():
    rows = [
        ("Kit à monter", "Le plan et les tests restent chez vous.", False),
        ("Multimarque", "Plusieurs catalogues, plusieurs logiques.", False),
        ("Abonnement lié", "Le matériel est parfois lié à un contrat.", False),
        ("AS974", "Étude, devis, pose, puis le SAV.", True),
    ]
    cards = []
    for title, text, ours in rows:
        cls = "cmp-card is-us" if ours else "cmp-card"
        mark = "✓" if ours else "–"
        cards.append(f'<li class="{cls}"><b>{mark}</b><strong>{title}</strong><span>{text}</span></li>')
    return f'<ul class="cmp" aria-label="Pourquoi choisir Active Sécurité 974">{"".join(cards)}</ul>'
