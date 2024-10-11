# Harfang Game CRUD

## Description

**Harfang Game CRUD** est une API REST développée en Python qui permet de gérer une base de données de jeux vidéo. L'API permet d'ajouter, modifier, supprimer et lister des jeux avec des informations telles que le nom du jeu, la date de sortie, le studio de développement, les plateformes supportées et les évaluations.

## Fonctionnalités

- Ajouter un jeu
- Modifier un jeu existant
- Supprimer un jeu
- Lister/Filtrer des jeux
- Vérification de la validité des données ajoutées (par exemple, refus des noms de jeu vides)

## Technologies

- **Python 3.9+**
- **FastAPI** : Framework web rapide et performant pour créer l'API.
- **SQLAlchemy** : ORM utilisé pour interagir avec la base de données.
- **MySQL** : Base de données utilisée pour stocker les informations sur les jeux et les plateformes.
- **Docker** : Pour containeriser l'application et faciliter le déploiement.


## Prérequis

Avant de commencer, assurez-vous d'avoir installé les éléments suivants :

- [Python 3.9+](https://www.python.org/downloads/)
- [Docker](https://www.docker.com/products/docker-desktop)
- [Git](https://git-scm.com/)


## Utilisation

### Lancement du serveur

1. Pour démarrer le serveur FastAPI localement, exécutez la commande suivante :

    ```bash
    uvicorn main:app --reload
    ```

2. L'API sera accessible à l'adresse `http://127.0.0.1:8000`.

3. Pour visualiser et tester l'API avec Swagger, ouvrez un navigateur et allez sur `http://127.0.0.1:8000/docs`.

### Lancement avec Docker

1. Pour démarrer l'application avec Docker, exécutez la commande suivante :

    ```bash
    docker-compose up --build
    ```

2. L'API sera accessible à l'adresse `http://localhost:8000`.

## Points d'API

- `GET /games`: Lister tous les jeux
- `POST /games`: Ajouter un nouveau jeu
- `PUT /games/{id}`: Modifier un jeu existant
- `DELETE /games/{id}`: Supprimer un jeu
- `GET /platforms`: Lister toutes les plateformes

