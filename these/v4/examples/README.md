# read_file.py

Lecture d'un fichier et renvoye plusieurs listes (sous la forme d'une matrice d'adjacence) selon la méthode.

# Format du fichier pour la découverte de la vérité

Le format d'un fichier qui représente un graphe est simple :
- Si une ligne commence par un '#', elle est ignorée.
- La première ligne du graphique sans « # » est :
    - *nombre de sources* *nombre d'objets* *nombre de faits*

Nous représentons tous les faits par un nombre entier (de 1 à *nombre de faits*).

Ensuite, dans le dossier, nous avons les liens entre les sources et les faits :
- La première ligne correspondra aux faits affirmés par la source 1, la deuxième ligne à la source 2, etc.
- Le caractère « - » est le séparateur entre les sources et les objets.
- Nous avons maintenant les faits liés aux objets de la même manière que les sources. La première ligne pour l'objet 1, etc.

Exemple :

```
#nbsrc nbobj nbfct
5 2 4
#liens entre sources et faits
#source 1
2,4
#source 2
4
#source 3
1
-
#liens entre objets et faits
#object 1
1,2
3,4
```

# Format du fichier pour la fusions de croyances

Ici nous devons ajouter le nombre de littéraux à la première ligne puis les formules que nous allons utilisés pour prendre une décision. 

Sur l'exemple nous avons quatre formules séparé par `<` : 1,6,7 et 0,2,3 et 0,1,4,5,6 et 2,4,7.

La formule 1 a pour modèle les interprétations 1, 6 et 7. Sa négation a le complément : 0, 2, 3, 4 et 5. Pas besoin d'écrire la négation, le code se charge de générer la négation grâce au nombre de littéraux spécifié sur la première ligne (ici 3).

```
#nbsrc nbformulae nbfct nblit
2 4 8 3
#truth : 7
#Formulae:1,6,7<0,2,3<0,1,4,5,6<2,4,7
#links between sources and facts
#sources1
1,4,6,7
2,3,6,7
-
#liens entre les faits et les objets
#objet 1 :
1,2
3,4
5,6
7,8
```

# Format du fichier pour l'agrégation de jugements

Ici nous devons spécifier le fichier avec tous les ensembles de jugements possibles, toujours précédé de `#Formula:`. Ici le fichier est `v4/prop_files/ex2.txt` 

La source 2 ici affirme la première formule (représenté par l'id 1) puis la négation de la 2e formule (représenté par un indice impair, 4 ici).

```
#nbsrc nbobj nbfct
3 8 16
#ex2.txt example ana; b;nb
#Formula:v4/prop_files/ex2.txt
# négation = impair et vrai f = pair
#links between sources and facts
#source A1
2,4,6,8,10,12,14,16
1,4,6,7,9,11,14,16
2,3,5,7,9,12,13,15
-
#liens entre les faits et les objets
#objet 1 :
1,2
3,4
5,6
7,8
9,10
11,12
13,14
15,16
```