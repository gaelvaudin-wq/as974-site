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
    return _svg(
        '<circle cx="320" cy="190" r="120" fill="none" stroke="#0A4D8C" stroke-width="3"/>'
        '<circle cx="320" cy="190" r="70" fill="none" stroke="#E10600" stroke-width="3"/>'
        '<circle cx="320" cy="190" r="14" fill="#0B0B0C"/>'
        '<text x="320" y="48" text-anchor="middle" fill="#0B0B0C" font-size="18" font-family="Inter,sans-serif">Portée radio en champ libre</text>'
        '<text x="470" y="120" fill="#0A4D8C" font-size="14" font-family="Inter,sans-serif">Hub 2 · 2 000 m</text>'
        '<text x="400" y="168" fill="#E10600" font-size="14" font-family="Inter,sans-serif">EN54 · 1 800 m</text>'
        '<text x="320" y="320" text-anchor="middle" fill="#5F5F64" font-size="14" font-family="Inter,sans-serif">Les murs se vérifient sur place.</text>',
        "Schéma de portée radio Jeweller")

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
        (70, "Kit à monter", "Vous faites le plan"),
        (150, "Multimarque", "Plusieurs catalogues"),
        (230, "Avec engagement", "Matériel lié à un abonnement"),
        (310, "AS974", "Une étude, un devis, une pose"),
    ]
    bits = ['<rect x="24" y="300" width="592" height="4" fill="#E10600"/>']
    for y, title, text in rows:
        bits.append(f'<text x="40" y="{y}" fill="#0B0B0C" font-size="18" font-family="Inter,sans-serif" font-weight="700">{title}</text>')
        bits.append(f'<text x="280" y="{y}" fill="#0A4D8C" font-size="16" font-family="Inter,sans-serif">{text}</text>')
    return _svg("".join(bits), "Comparatif visuel : pourquoi choisir Active Sécurité 974")
