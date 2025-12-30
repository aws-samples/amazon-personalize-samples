Évaluation des performances hors ligne
===

Vous disposez de données historiques et vous voulez savoir comment Personalize fonctionne sur vos données. Voici ce que nous vous proposons :

1. Répartissez temporairement vos données en un ensemble de formation « antérieur » et un ensemble de test « à venir ».
2. Chargez les données « passées » sur Amazon Personalize, configurez une solution et déployez une campagne.
3. Servez-vous de votre campagne pour obtenir des recommandations pour tous vos utilisateurs, et comparez-les avec l'ensemble de tests « à venir ».

Voici un exemple, [personalize_temporal_holdout.ipynb](personalize_temporal_holdout.ipynb/) pour réaliser les étapes ci-dessus. Nous incluons une recommandation simple basée sur la popularité, qui devrait être facile à dépasser. C'est pour des raisons de sécurité. L'étape suivante consiste souvent à conserver la même répartition de la formation et des tests, tout en formant des modèles différents pour des comparaisons hors ligne plus importantes.

## Résumé de la licence

Cet exemple de code est distribué sous une licence MIT modifiée. Reportez-vous au fichier LICENSE.
