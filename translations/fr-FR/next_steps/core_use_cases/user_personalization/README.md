Amazon Personalize – Personnalisation de l'utilisateur
---

En combinant un algorithme de pertinence basé sur HRNN avec l'exploration automatique des recommandations d'articles nouveaux ou anciens, la recette aws-user-personalization offre la plus grande flexibilité lors de la création de cas d'utilisation de la personnalisation de l'utilisateur. Bien que le jeu de données d'interactions est le seul jeu de données requis, cette recette tirera profit de tous les trois types de jeux de données (Interactions, Éléments, Utilisateurs) s'ils sont fournis. En outre, elle peut également modéliser les données d'impression si elles sont fournies dans votre jeu de données d'interactions et lors de la diffusion d'événements en temps réel à l'aide du suivi des événements.

Bien que nous fournissions des exemples de blocs-notes pour les recettes HRNN-* pour la postérité, il est recommandé de commencer par la recette de personnalisation de l'utilisateur.
## Exemples

### Personnalisation de l'utilisateur 

L'exemple [user-personalization-with-exploration.ipynb](user-personalization-with-exploration.ipynb) explique comment utiliser un jeu de données d'interactions et d'articles pour créer une solution et une campagne qui équilibre la formulation de recommandations basées sur la pertinence (exploitation) et l'exploration de la recommandation d'articles nouveaux/anciens. Un jeu de données d'utilisateurs aurait également pu être utilisé, mais il n'est pas inclus dans cet exemple. Cet exemple montre également comment inclure les données d'impression dans le jeu de données d'interactions et dans les appels API PutEvents.

### Recommandations contextuelles + Suivi des événements

Dans cet exemple, nous allons voir comment tirer profit des métadonnées et du contexte pour proposer aux utilisateurs les meilleures recommandations de compagnies aériennes sur la base des évaluations historiques de ces compagnies dans plusieurs types de cabines, avec l'emplacement de l'utilisateur comme métadonnée.

L'exemple [user-personalization-with-contextual-recommendations.ipynb](user-personalization-with-contextual-recommendations.ipynb) explique comment ces informations utiles peuvent être chargées dans notre système pour faciliter la recommandation. Une mise en garde qui s'impose est que les améliorations des recettes de métadonnées dépendent de la quantité d'informations pouvant être extraites des métadonnées fournies.


*Notez que les capacités de démarrage à froid des articles de la recette de personnalisation de l'utilisateur sont préférées à celles de la recette HRNN-Coldstart. Il est donc recommandé de commencer par la recette de personnalisation de l'utilisateur pour les scénarios concernant les articles anciens.*

## Résumé de la licence

Cet exemple de code est distribué sous une licence MIT modifiée. Reportez-vous au fichier LICENSE.
