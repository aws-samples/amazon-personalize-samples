Amazon Personalize – Principaux cas d'utilisation
---

Amazon Personalize est un service de machine learning qui permet aux développeurs de générer facilement des recommandations individualisées pour les clients qui utilisent leurs applications. Il témoigne de la grande expérience d'Amazon dans la création de systèmes de personnalisation. Amazon Personalize peut servir dans de nombreux scénarios : recommandations aux utilisateurs en fonction de leurs préférences et de leur comportement, reclassement personnalisé des résultats, personnalisation du contenu des e-mails et des notifications, etc.

En tant que développeur, vous devez seulement faire ce qui suit :

- Formatez les données d'entrée et chargez-le dans un compartiment Amazon S3, ou envoyez des données en temps réel sur les événements, utilisateurs et articles à l'aide du kit SDK Personalize.
- Sélectionnez une recette d'entraînement (algorithme) à utiliser sur les données.
- Entraînez une version de la solution en utilisant la recette.
- Déployez la version de la solution.

## Mappage des cas d'utilisation aux recettes

| Cas d'utilisation | Recette | Description
|-------- | -------- |:------------
| Personnalisation de l'utilisateur | aws-user-personalization | Cette recette est optimisée pour tous les scénarios de recommandation des utilisateurs. Elle prédit les articles avec lesquels un utilisateur interagira sur la base des jeux de données d'interactions, d'articles et d'utilisateurs. Il utilise un algorithme HRNN pour générer des recommandations basées sur la pertinence (exploitation) et l'exploration automatique des articles pour recommander les éléments nouveaux ou anciens. Vous contrôlez la balance entre l'exploitation et l'exploration.
| Articles connexes | aws-sims | Calcule les articles similaires à un article donné sur la base de leur présence dans l'historique du même utilisateur dans le jeu de données d'interactions.
| Classement personnalisé | aws-personalized-ranking | Reclasse une liste des articles pour un utilisateur. Formation sur les jeux de données d'interactions, d'articles et d'utilisateurs.

*Le tableau ci-dessus présente les mappages principaux et les plus recommandés des cas d'utilisation aux recettes. Personalize prend en charge d'autres recettes telles que aws-popularity-count ainsi que les anciennes recettes aws-hrnn, aws-hrnn-coldstart et aws-hrnn-metadata. Cependant, les algorithmes des recettes aws-hrnn-* ont été incorporés et étendus par la recette aws-user-personalization et ne sont donc plus recommandés pour les cas d'utilisation de la personnalisation de l'utilisateur.*

## Contenu

Dans ce répertoire, nous avons des exemples de différents cas d'utilisation

1. [Personnalisation de l'utilisateur](user_personalization/)
    - Prédit les articles avec lesquels un utilisateur va interagir. Un réseau neuronal récurrent hiérarchique capable de modéliser l'ordre temporel des interactions entre l'utilisateur et les articles, en combinaison avec l'exploration automatique des articles nouveaux ou anciens.
2. [Articles connexes](related_items/)
    - Calcule les articles similaires à un article donné sur la base de leur présence dans l'historique du même utilisateur dans le jeu de données d'interaction utilisateur-article.
3. [Classement personnalisé](personalized_ranking/)
    - Reclasse une liste des articles pour un utilisateur en fonction de la pertinence.
4. [Recommandations par lots](batch_recommendations/)
    - Créez des recommandations pour plusieurs utilisateurs ou articles en un seule tâche par lot.
5. [Métadonnées](metadata/)
    - Exemples de préparation et d'inclusion de métadonnées dans vos jeux de données.
5. [Optimisation des objectifs](objective_optimization/objective-optimization.ipynb)
    - Exemple de la façon d'équilibrer les objectifs de l'entreprise avec des recommandations pertinentes en utilisant l'optimisation des objectifs.
## Résumé de la licence

Cet exemple de code est distribué sous une licence MIT modifiée. Reportez-vous au fichier LICENSE.
