# Active Sécurité 974

Site vitrine statique d’Active Sécurité 974, installateur partenaire agréé Ajax Systems à La Réunion. Catalogue sur devis, sans panier ni paiement.

Adresse prévue : <https://gaelvaudin-wq.github.io/as974-site/>

## Publier

Le dépôt se déploie sur GitHub Pages à chaque push sur `main` (workflow `.github/workflows/pages.yml`, source GitHub Actions). Si la première exécution échoue faute d’environnement Pages, ouvrir **Settings → Pages → Source : GitHub Actions**, puis relancer le workflow.

## Régénérer

Les constantes (URL, coordonnées, action du formulaire) sont dans `_build/config.json`.

- `SITE_URL` : base canonique, sans slash final.
- `business.email`, `telephone`, `adresse`, `siret` : laisser `null` tant qu’ils ne sont pas connus. Le site affiche alors `[À COMPLÉTER]`.
- `form_action` : URL Formspree (`https://formspree.io/f/xxxx`). Tant que la valeur n’est pas une URL `http(s)`, le formulaire ouvre un `mailto` (`form_mailto`).

```bash
python3 _build/build.py
```

Le catalogue source est `_build/data/AS974-Ajax-catalogue-complet.json`. Les visuels déjà optimisés sont dans `assets/img/p/` ; ils ne sont recalculés que si les fichiers sources sont fournis dans `_build/data/images/`.
