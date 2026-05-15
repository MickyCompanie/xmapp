# 🎄 xmapp - Backend API

Une API robuste construite avec FastAPI pour orchestrer la magie de Noël (gestion de listes de cadeaux et partages entre proches).

---

## 🚀 Stack Technique

*   **Framework :** FastAPI
*   **Base de Données :** PostgreSQL
*   **ORM :** SQLAlchemy 2.0 (avec support des types `Mapped`)
*   **Migrations :** Alembic
*   **Validation de Données :** Pydantic v2
*   **Tests :** Pytest avec base de données de test isolée
*   **Client API :** Bruno (Collection incluse)

---

## 🏛️ Architecture du Projet

Le projet suit une structure modulaire par domaine. Chaque module (user, auth, wish, etc.) est autonome et regroupe sa propre logique métier.

```text
app/
├── core/              # Configuration globale (config.py, security.py)
├── db/                # Session, base.py, setup de la base de données
├── auth/              # Logique d'authentification (JWT, login, deps)
├── user/              # Module Utilisateur
│   ├── model.py       # Définition de la table SQLAlchemy
│   ├── schemas.py     # Modèles Pydantic (validation In/Out)
│   ├── services.py    # Logique métier (CRUD, calculs)
│   └── router.py      # Définition des endpoints FastAPI
├── person/            # Module Profil (lié aux utilisateurs)
└── ...
tests/                 # Suite de tests Pytest (miroir de la structure app/)
```

## 🛠️ Installation & Configuration

### 1. Cloner le projet
```bash
git clone <url-du-repo>
cd xmapp/backend
```

### 2. Gérer l'environnement virtuel

```bs
python -m venv venv
# Windows
.\venv\Scripts\activate
# Linux/macOS
source venv/bin/activate
```

3. Installer les dépendances

```bs
pip install -r requirements.txt
```

4. Variables d'environnement
Créez un fichier .env dans le dossier backend/ :

```env
DATABASE_URL=postgresql://postgres:password@localhost:5432/xmapp_db
SECRET_KEY=votre_cle_secrete_super_secure
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
PREFIX=api/
VERSION=v0.1.0
```

## 🗄️Base de Données
Appliquez les dernières migrations pour structurer votre base locale :

```bs
alembic upgrade head
```

## 🧪 Test & Débogage

### 1. Tests automatisés

La suite de tests vérifie l'intégrité des routes, l'authentification et les contraintes de la base de données.

```bs
    pytest
```
Note : Les tests utilisent une session de base de données transactionnelle qui se rollback après chaque test pour garantir l'isolation.

## 2. Tests manuels (Bruno)

Une collection Bruno est disponible dans le dossier /bruno à la racine du projet pour faciliter le test des endpoints.