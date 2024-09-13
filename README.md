# Mesures de confiance par confrontation des sources

## Détails des dossiers

Dans ce dépôt nous trouvons les différentes implémentations des nos méthodes ainsi que des méthodes de la littérature.

Le dossier `belms` est l'implémentation des méthodes de fusion de croyances.
  - Les fichiers ont le même nom que la méthode
  - Les fichiers commençant par `sf` sont les méthodes utilisant la fiabilité pour prendre une décision

Le fichier `constants/constants.py` permet de changer le type d'expérimentation à lancer.

Le dossier `examples` regroupe tous les fichiers qui permettent de tester une méthode sur un graphe spécifique. Toutes les méthodes utilisent un graphe avec un format particulier.

Dans le dossier `generation` nous avons le code pour générer et lancer les tests sur les jeux de données ainsi que le dossier `xp` avec tous les jeux de données. Pour l'agrégation de jugements, les agendas qui sont générés sont stockés dans le dossier `prop_files`.

Les dossiers `graph` et `vote` concernent la création de nos méthodes S\&F. 
  - `derive.py` est la méthode qui utilise une mise à jour contrôlée de la fiabilité
  - `prio.py` pour la méthode qui permet d'activer les objets pendant le processus
  - `mylog.py` qui utilise la règle optimale

Le dossier `judag` est l'implémentation de nos méthode pour l'agrégation de jugements ainsi que les méthodes de la littérature. 
  - Le nom des fichiers est le même que le nom de la méthode sauf pour les méthodes basées sur le support qui sont `COUNTMAX.py`, `COUNTMIN.py` et `COUNTSUM.py` pour respectivement le leximax, leximin et la somme

Le dossier `main` permet de tester toutes les méthodes sur un graphe en particulier.

Le dossier `other_methods` regroupe les méthodes de découverte de la vérité de la littérature.
  -  Les fichiers ont le même nom que la méthode
  -  - Les fichiers commençant par `sf` sont les méthodes utilisant la fiabilité pour prendre une décision

Les graphiques qui sont générés sont stockés dans le dossier `png` et les fichiers avec les résultats des différentes métriques sont stockés dans le dossier `results`.

Les fichiers dans `priors_file` permettent d'associer une probabilité a priori aux sources avec une génération spécifique.

`tests_datasets` permet de lancer les tests sur un jeux de données réelles.

## Besoin

pip3 install scipy

## Exemple de commande

Avec Python3, à la racine du projet (`these/`)  :
- Pour Lancer la méthode S\&F avec la Plurality rule et la normalisation A ainsi que le graphe sur les capitales : `python3 -m v4.main.main_plurality A v4/examples/graphes/capital.txt`
