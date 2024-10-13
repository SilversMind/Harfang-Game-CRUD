# Harfang Game CRUD

## Note

Pendant l'entretien technique, j'ai implémenté la solution demandée sur la branche `master`, conformément aux consignes et dans le temps imparti de 2 heures. Après l'entretien, j'ai souhaité consacrer un peu plus de temps pour peaufiner le projet. Le travail réalisé sur la branche `master` reflète ce qui a été fait pendant l'entretien.

Cependant, si cela vous intéresse, j'ai créé une branche `dev` où j'ai :
- Couvert toutes les questions proposés dans l'exercice demandé.
- Amélioré la couverture des tests.
- Optimisé la gestion de la base de données.
- Ajouté une meilleure gestion des erreurs.
- Refactorisé certaines parties du code pour améliorer sa lisibilité et sa maintenabilité.

N'hésitez pas à consulter cette branche si vous souhaitez voir une version plus aboutie de mon travail. Bien entendu, le travail sur la branche `master` reste la référence principale pour ce qui a été réalisé durant l'entretien.

Merci pour votre temps et votre considération !

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

1. Télécharger et lancer une image docker mysql
    ```bash 
    docker pull mysql
    
    docker run -e MYSQL_USER=hl_user -e MYSQL_PASSWORD=hl_pass -e MYSQL_ROOT_PASSWORD=hl_pass -p 3306:3306 mysql 
    ```
2. Pour démarrer le serveur FastAPI localement, exécutez la commande suivante :

    ```bash
    uvicorn main:app --reload
    ```

3. L'API sera accessible à l'adresse `http://127.0.0.1:8000`.

4. Pour visualiser et tester l'API avec Swagger, ouvrez un navigateur et allez sur `http://127.0.0.1:8000/docs`.

### Lancement avec Docker (recommandé)

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

