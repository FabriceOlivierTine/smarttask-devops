# SmartTask - DevOps Project

Application web de gestion de tâches, déployée avec une démarche DevOps complète (Docker, Docker Compose, GitHub, Jenkins CI/CD).

## Architecture

- **Frontend** : HTML / CSS / JavaScript, servi par Nginx (port 8080)
- **Backend** : API REST Python/Flask (port 5000)
- **Base de données** : PostgreSQL 16 (port 5432)

## Lancer le projet en local

```bash
git clone https://github.com/<ton-user>/smarttask-devops.git
cd smarttask-devops
docker compose up --build -d
```

- Frontend : http://localhost:8080
- API backend : http://localhost:5000/api/tasks
- Vérifier les conteneurs : `docker ps`
- Voir les logs : `docker compose logs -f`
- Arrêter : `docker compose down`

## Structure du dépôt

```
smarttask-devops/
├── backend/
│   ├── app.py
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── index.html
│   ├── style.css
│   ├── script.js
│   └── Dockerfile
├── docker-compose.yml
├── Jenkinsfile
├── .env
└── README.md
```

## CI/CD avec Jenkins

Le `Jenkinsfile` définit un pipeline multibranch qui :
1. Récupère le code depuis GitHub
2. Construit les images Docker (backend et frontend)
3. Tag les images
4. Se connecte à Docker Hub
5. Publie les images sur Docker Hub

## Branches

- `Dev` : développement
- `Prod` : version stable/production
