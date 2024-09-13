# all_methods.py

Exécute et montre les résultats sur un graphe spécifique pour nos méthodes (S&F avec `Plurality rule` et `Borda rule` ainsi que les deux normalisations).

`python3 -m v4.main.all_methods v4/examples/graphes/capital.txt`

# comparaison.py

Test sur toutes les méthodes, y compris les méthodes de la littérature.

`python3 -m v4.main.comparaison v4/examples/graphes/capital.txt`

# main_bm.py

Exécute et montre les résultats sur un graphe spécifique pour une méthode de fusion de croyances. 

Il faut un graphe venant du dossier `exmaples/bms` car il faut donner en plus les formules (sous forme d'ensemble d'interprétations) ainsi que le nombre de littéraux utilisés. Il faut aussi spécifié la méthode, ici avgA qui est la méthode utilisant la fiabilité et choisie le maxcons avec la fiabilité moyenne la plus haute.

`python3 -m v4.main.main_bm avgA v4/examples/bms/exKR2000.txt`

# main_formule.py

Exécute et montre les résultats sur un graphe spécifique pour une méthode d'agrégation de jugements. 

`python3 -m v4.main.main_formule sum v4/examples/formula/ex2.txt`

# main_borda.py

Exécute et montre les résultats sur un graphe spécifique avec la `Borda rule`.

La normalisation et le chemin du fichier doivent être spécifiés dans la ligne de commande :

`python3 -m v4.main.borda_method.py *normalisation* v4/examples/graphes/capital.txt`

si `*normalisation*` n'est pas spécifié, par défaut nous utilisons la normalisation A. Vous pouvez choisir 2 normalisations : A ou C.

# main_plurality.py

Exécute et montre les résultats sur un graphe spécifique avec la `Plurality rule`.

La normalisation et le chemin du fichier doivent être spécifiés dans la ligne de commande :

`python3 -m v4.main.plurality_method.py *normalisation* v4/examples/graphes/capital.txt`

si `*normalisation*` n'est pas spécifié, par défaut nous utilisons la normalisation A. Vous pouvez choisir 2 normalisations : A ou C. 

# Affichage lors de l'exécution

Reliability sources :
`1` : 0.0 - [1] ; `2` : 0.5 - [2] 

Reliability facts :
`1` : 0.5 - 0 - [1] ; `2` : 1.5 - 1 - [2]

- La source 1 a une fiabilité de 0.0 et la source 1 affirme un fait ([1])
- La source 2 a une fiabilité de 0.5 et la source 2 affirme deux faits ([2])
- Le fait `1` a une fiabilité de 0.5. Les sources qui l'affirme vont recevoir un score `V` de `0` et le fait est affirmé par une seule source ([1])
- Le fait `2` a une fiabilité de 1.5. Les sources qui l'affirme vont recevoir un score `V` de `1` et le fait est affirmé par deux sources ([2])

Plusieurs options pour l'affichage à chaque itération dans `v4/graph/obj` dans la fonction `str_trust_f()`