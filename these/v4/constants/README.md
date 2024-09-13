# constants.py

Nous avons trois types de génération.
- RUN_BS pour la fusion de croyances
- RUN_JA pour l'agréation de jugements
- RUN_TD pour la découverte de la vérité

La variable `FORMULA` doit toujours prendre une de ces trois valeurs.

`TD_TEST` est a `True` si nous voulons tester les méthodes qui essayent d'améliorer les performances des méthodes S&F.

`PLOT_ORDER` permet de changer les méthodes qui vont apparaitre sur le graphique générer. 

`PARA_PLOT` permet de changer la couleur, le label et la forme de la courbe.

Toutes les métriques sont consignés dans ce ficher et s'exécute selon la valeur assignée à `FORMULA`.