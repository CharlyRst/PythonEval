# Exercice 1 · Comprendre le contrat HTTP

## 1. Une route GET /stations crée une station. Quel verbe et quel code HTTP faut-il utiliser pour cette création ?

Le verbe est POST et le code HTTP est 201.

## 2. GET /stations/999 demande une station inexistante. Quel code HTTP et quel type de réponse faut-il renvoyer ?

Le code HTTP à renvoyer est le 404 et la réponse doit une réponse JSON avec detail="Station introuvable".

## 3. Quelle est la différence entre les codes 401 et 403 ? Donnez un exemple de chaque cas.

Le code 401 précise le fait que l'utilisateur n'est pas authentifié et le 403 précise le fait que le serveur connait l'utilisateur mais ne lui donne pas les accès suite à ses permissions.

Pour le cas de 401 : Si un utilisateur non connecté décide de changer l'url et d'arriver à la page "/profil", cela sera décrit comme non autorisé car il n'est pas connecté.

Pour le cas de 403 : Si un utilisateur est connecté et veut accéder à des pages réservées aux administrateurs, le code 403 sera de sortie.

# Exercice 3 - étape 4

Test avec code HX-01, name Châtelet et capacity 12. Après redémarrage on constate que la station est enrégistré dans la database (dock_control.db).

Sortie : 
[
  {
    "id": 1,
    "code": "HX-01",
    "name": "Châtelet",
    "capacity": 12,
    "status": "open"
  }
]

#