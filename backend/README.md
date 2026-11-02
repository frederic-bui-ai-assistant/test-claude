# Backend Python — La Cave des Canuts

API Flask connectée au projet Supabase de la boutique.

## Installation locale

Depuis la racine du dépôt :

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate

pip install -r backend/requirements.txt
```

Copier `backend/.env.example` vers `.env`, puis renseigner la clé publishable Supabase.

```bash
python backend/app.py
```

Ouvrir http://127.0.0.1:5000.

## Routes disponibles

- `GET /` : page d'accueil actuelle.
- `GET /api/health` : état du service Flask.
- `GET /api/wines` : catalogue des vins publiés, trié par nom.

## Sécurité

- La clé publishable est utilisée avec les politiques RLS du catalogue public.
- Ne jamais placer de clé `sb_secret_*` ou `service_role` dans le navigateur ou dans Git.
- Les commandes, paiements et opérations de stock devront passer par des routes serveur authentifiées. Les données de carte bancaire ne doivent jamais être stockées dans Supabase.
- Les fiches ne remontent que si `is_published = true`.

Le site reste pour le moment alimenté par ses fiches de démonstration : l'API est prête, mais le raccordement dynamique du catalogue et le processus de commande restent à réaliser.
