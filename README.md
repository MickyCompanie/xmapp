# xmapp
an app made to make christmass even more magical


structure du projet: 

```
├── app/
│   ├── api/            # Tes routes (endpoints)
│   ├── core/           # Config, sécurité (JWT), constantes
│   ├── models/         # Modèles SQLAlchemy
│   ├── schemas/        # Modèles Pydantic (validation)
│   ├── services/       # Logique métier (ex: algorithme Secret Santa)
│   └── main.py         # Point d'entrée de l'application
├── tests/              # Tes tests unitaires et d'intégration
├── migrations/         # Dossier généré par Alembic
├── .env                # Variables secrètes (DATABASE_URL, SECRET_KEY)
├── .gitignore
├── alembic.ini
└── requirements.txt
```