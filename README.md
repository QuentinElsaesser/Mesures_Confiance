# Mesures de confiance par confrontation des sources

## Détails des dossiers

Dans ce dépôt nous trouvons les différentes implémentations des nos méthodes ainsi que des méthodes de la littérature.

Le dossier `belms` est l'implémentation des méthodes de fusion de croyances.

Le fichier `constants/constants.py` permet de changer le type d'expérimentation à lancer.

Le dossier `examples` regroupe tous les fichiers qui permettent de tester une méthode sur un graphe spécifique. Toutes les méthodes utilisent un graphe avec un format particulier.

Dans le dossier `generation` nous avons le code pour générer et lancer les tests sur les jeux de données ainsi que le dossier `xp` avec tous les jeux de données. Pour l'agrégation de jugements, les agendas qui sont générés sont stockés dans le dossier `prop_files`.

Les dossiers `graph` et `vote` concernent la création de nos méthodes S\&F. 

Le dossier `judag` est l'implémentation de nos méthode pour l'agrégation de jugements ainsi que les méthodes de la littérature. 

Le dossier `main` permet de tester toutes les méthodes sur un graphe en particulier.

Le dossier `other_methods` regroupe les méthodes de découverte de la vérité de la littérature.

Les graphiques qui sont générés sont stockés dans le dossier `png` et les fichiers avec les résultats des différentes métriques sont stockés dans le dossier `results`.

Les fichiers dans `priors_file` permettent d'associer une probabilité a priori aux sources avec une génération spécifique.

`tests_datasets` permet de lancer les tests sur un jeux de données réelles.

## Besoin

pip3 install scipy

## Exemple de commande

Avec Python3, à la racine du projet (`these/`)  :
- Pour Lancer la méthode S\&F avec la Plurality rule et la normalisation A ainsi que le graphe sur les capitales : `python3 -m v4.main.main_plurality A v4/examples/graphes/capital.txt`
