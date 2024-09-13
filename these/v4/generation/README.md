# generation

Après les tests, nous écrivons tous les résultats dans un fichier .tex et nous lisons ce fichier pour générer les graphiques avec `matplotlib`.

# File in xp/

Chaque ligne représente un graphe généré et utilisé dans nos expériences. 

L'ID des faits commence à zéro.

Les lignes doivent être triées par fiabilité (ou par intervalle de fiabilité).

- NB_OBJ : Le nombre d'objets dans le graphe
- NB_SRC : Le nombre de sources dans le graphe
- NB_FL : Le nombre minimum de faits associés à un objet
- NB_FU : Le nombre maximum de faits associés à un objet
- NBF : Le nombre de faits dans le graphe
- TRUST : Probabilté moyenne de trouver la vérité du graphe
- SF : Les liens entre les sources et les faits. Les sources sont séparées par un tiret (-).
- A la première ligne, nous avons "5,12,27,29,33,38-..."  Cela signifie que la première source affirme le fait 5,12,etc.
- OF : Les liens entre les faits et les objets. Les objets sont séparés par un tiret (-).
- En première ligne, nous avons "0,1,2,3-..." cela signifie que les faits 0,1,2,3 sont liés au premier objet.
objet.
- TRUTH : ID des faits réels dans le graphique
- INTERVAL : l'intervalle utilisé pour regrouper les graphiques
- PRC/SRC/FCT : représentent ce que nous changeons dans nos graphiques et sont liés à l'INTERVALLE (PRC : fiabilité des sources ; SRC : nombre de sources ; FCT : nombre de faits par objet).
- PRP/SPR : `*/prop*` utilisé pour les méthodes d'agrégation de jugements où la première étoile correspond au dossier avec tous les agendas et `prop*` au nom du fichier contenant l'agenda pour ce graphe. SPR représente une génération où nous changeons le nombre de sources plutôt que la fiabilité moyenne du graphe.
- BIA : Pour la fusion de croyances. `0!=6,2,1,5,4-1=0,3,7` représente deux formules. La première `0` qui est une formule et `6,2,1,5,4` l'ensemble d'interprétations qui représente cette formule.

# att_metrics.py 

Regroupe toutes les informations pour obtenir les résultats des métriques.

# brutefrc_exp_para.py

- Génération des graphes pour la découverte de la vérité.
- Les paramètres sont a changer dans le main du fichier (nombre de source etc)
- Un prompt demande des informations à chaque itération. Pour une génération complétement aléatoire, utiliser le paramètre `r`. 
- SRC pour une génération avec un nombre différentes de sources
- FCT pour une génération avec un nombre différentes de faits
- PRC pour une génération avec une fiabilité différente. 

# gen_bel_spe_synt.py et gen_bel_spe2_synt.py 

Génération de graphe pour la fusion de croyances en changement le nombre de sources des graphes.

# gen_bel_synt.py

Génération de graphe pour la fusion de croyances en changement la fiabilité moyenne des graphes.

# generate_TD.py

Génération de graphe pour la méthode utilisant le log avec des hypothèses particulièrement : 
- graphe complet
- fiabilité des sources supérieur à 50%

# generate_w_prop.py

Génération de graphe pour l'agrégation de jugements.

# graph_methods.py

Génére un graphe et le copie pour toutes les méthodes, puis exécute l'algorithme et calcule le score des métriques.

# latex.py

Écrit les résultats dans un fichier Latex.

# main_generate.py

- Génére les graphiques (plot) en spécifiant le numéro du fichier avec les résultats des métriques.
- Doit être coupler avec la bonne valeur pour `FORMULA` dans le fichier `constants/constants.py`

# metrics.py

Calculer les résultats pour toutes les métriques avec les 1000 graphes

# plot.py, plot_bar.py et plot_max_min.py

Récupère les informations pour générer un graphique (plot).

# priors.py

Génére un fichier contenant les valeurs possibles de la probabilité a priori.

# random_graph.py

Génére un graphe en fonction des paramètres donnés.

# read_xp.py

Lecture d'un jeu de données. Paramètre à changer dans le main ou lors de la commande
- `python3 -m v4.generation.read_xp "" 1` pour le fichier 1 qui change la fiabilité des graphes (exécution spécial avec PRC)
- `python3 -m v4.generation.read_xp prp 470`
Doit être coupler avec la bonne valeur dans le fichier `constants/constants.py`

# spe_metrics.py

Classe spécifique pour écrire la fiabilité sources par sources dans le fichier .tex