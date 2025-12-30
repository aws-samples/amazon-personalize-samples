## Automatisation de votre flux Amazon Personalize à l'aide du kit SDK AWS Step Functions Data Science

Alors que le machine learning (ML) devient de plus en plus important dans les activités des entreprises, l'accent est davantage mis sur la réduction du temps entre la création et le déploiement des modèles. En novembre 2019, AWS a publié le kit SDK AWS Step Functions Data Science pour Amazon SageMaker, un kit SDK open source qui permet aux développeurs de créer des flux de machine learning en Python et basés sur Step Functions. Vous pouvez désormais utiliser le kit SDK pour créer des flux de déploiement de modèles réutilisables avec les mêmes outils que vous utilisez pour développer vos modèles. Le manuel complet de cette solution est disponible dans le dossier « automate_personalize_workflow » de notre référentiel GitHub.

Ce référentiel démontre les capacités du kit SDK Data Science avec un cas d'utilisation courant : l'automatisation de Personalize. Dans cet article, vous créez un flux sans serveur pour entraîner un moteur de recommandation de films. Enfin, l'article vous explique comment déclencher un flux en se basant sur une planification périodique.

### Cet article utilise les services AWS suivants :
•	AWS Step Functions vous permet de coordonner plusieurs services AWS dans un flux sans serveur. Vous pouvez concevoir et exécuter des flux dans lesquels la sortie d'une étape agit comme l'entrée de l'étape suivante, et vous pouvez également intégrer la gestion des erreurs dans le flux.\
•	AWS Lambda est un service de calcul qui vous permet d'exécuter du code sans provisionner ni gérer de serveurs. Lambda exécute votre code uniquement lorsque la fonction est déclenchée et se met automatiquement à l'échelle, passant de quelques requêtes par jour à des milliers par seconde.\
•	Amazon Personalize est un service de machine learning qui vous permet de personnaliser votre site web, votre application, vos publicités, vos e-mails, etc., avec des modèles de machine learning personnalisés qui peuvent être créés dans Amazon Personalize, sans avoir aucune expérience préalable en machine learning.

## Présentation du kit SDK
Le kit SDK offre une nouvelle façon d'utiliser AWS Step Functions. La solution Step Functions est une machine d'état qui se compose d'une série d'étapes distinctes. Chaque étape peut effectuer une tâche, faire des choix, initier une exécution parallèle ou gérer des délais d'attente. Vous pouvez développer des étapes individuelles et utiliser Step Functions pour gérer le déclenchement, la coordination et l'état du flux global. Avant le kit SDK Data Science, vous deviez définir Step Functions à l'aide du langage Amazon States basé sur JSON. Avec le kit SDK, vous pouvez désormais facilement créer, exécuter et visualiser des Step Functions à l'aide du code Python.

Ce référentiel fournit un aperçu du kit SDK, y compris comment créer des étapes Step Function, travailler avec des paramètres, intégrer des fonctionnalités spécifiques au service et lier ces étapes pour créer et visualiser un flux. Vous trouverez plusieurs exemples de code tout au long de cet article. Toutefois, nous avons créé un manuel Amazon SageMaker détaillé pour l'ensemble du processus.

## Présentation d'Amazon Personalize
Amazon Personalize est un service de machine learning qui permet aux développeurs de créer facilement des recommandations personnalisées pour les clients qui utilisent leurs applications.

Le machine learning est de plus en plus utilisé pour améliorer l'engagement des clients en proposant des recommandations personnalisées de produits et de contenu, des résultats de recherche sur mesure et des promotions marketing ciblées. Toutefois, le développement des capacités de machine learning nécessaires pour produire ces systèmes de recommandation sophistiqués est aujourd'hui hors de portée de la plupart des organisations en raison de leur complexité. Amazon Personalize permet aux développeurs sans expérience préalable en machine learning de créer facilement des capacités de personnalisation sophistiquées dans leurs applications, en utilisant une technologie de machine learning perfectionnée après des années d'utilisation sur Amazon.com.

Avec Amazon Personalize, vous fournissez un flux d'activité à partir de votre application (nombre de clics, de pages consultées, d'inscriptions, d'achats, etc.) ainsi qu'un inventaire des articles que vous souhaitez recommander, tels que des articles, des produits, des vidéos ou de la musique. Vous pouvez également choisir de fournir à Amazon Personalize des informations démographiques supplémentaires sur vos utilisateurs, comme l'âge ou l'emplacement géographique. Amazon Personalize traite et examine les données, identifie les informations utiles, sélectionne les bons algorithmes, et forme et optimise un modèle de personnalisation conçu sur mesure pour vos données. Toutes les données analysées par Amazon Personalize restent privées et sécurisées, et ne sont utilisées que pour vos recommandations personnalisées. Vous pouvez commencer à proposer des recommandations personnalisées par le biais d'un simple appel d'API. Vous ne payez que pour ce que vous utilisez, et il n'y a pas de frais minimum ni d'engagement initial.

Avec Amazon Personalize, c'est comme si vous aviez votre propre équipe de personnalisation de machine learning Amazon.com à votre disposition, 24 heures sur 24.



## Instructions
Téléchargez le manuel et suivez les instructions

## Licence

Cette bibliothèque est sous licence MIT-0. Reportez-vous au fichier LICENSE.


