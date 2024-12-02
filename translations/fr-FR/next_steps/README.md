# Prochaines étapes d'Amazon Personalize

Blocs-notes et exemples sur la façon d'intégrer et d'utiliser diverses fonctionnalités d'Amazon Personalize

## Exemples de cas d'utilisation d'Amazon Personalize

Le dossier [​core_use_cases/​​](core_use_cases/) contient des exemples détaillés des cas d'utilisation les plus courants.

## Exemples d'opérations évolutives pour vos déploiements Amazon Personalize

Le dossier ​​[operations/](operations/)​​ contient des exemples sur les sujets suivants :

* [Maintenir des expériences personnalisées avec le machine learning](https://aws.amazon.com/solutions/implementations/maintaining-personalized-experiences-with-ml/)
    - Cette solution AWS vous permet d'automatiser le processus de bout en bout d'importation de jeux de données, de création de solutions et de versions de solutions, de création et de mise à jour de campagnes, de création de filtres et d'exécution de travaux d'inférence par lots. Ces processus peuvent être exécutés à la demande ou déclenchés en fonction d'un calendrier que vous définissez.

* MLOps (hérité)
    - Il s'agit d'un projet visant à montrer comment déployer rapidement une campagne de personnalisation de façon entièrement automatisée à l'aide d'AWS Step Functions. Pour commencer, accédez au dossier ​​[ml_ops](operations/ml_ops/)​​ et suivez les instructions contenues dans README. Cet exemple a été remplacé par la solution ​[Maintenir des expériences personnalisées avec le machine learning](https://aws.amazon.com/solutions/implementations/maintaining-personalized-experiences-with-ml/).

* Kit SDK pour la science des données MLOps
    - Il s'agit d'un projet visant à montrer comment déployer rapidement une campagne de personnalisation de manière entièrement automatisée à l'aide du kit SDK d'AWS Data Science. Pour commencer, accédez au dossier [​​ml_ops_ds_sdk](operations/ml_ops_ds_sdk/)​​ et suivez les instructions contenues dans README.

* [API de personnalisation](https://github.com/aws-samples/personalization-apis)
    - Cadre d'API à faible latence en temps réel qui se situe entre vos applications et les systèmes de recommandation tels qu'Amazon Personalize. Fournit les bonnes pratiques de mise en œuvre du cache des réponses, des configurations de passerelles d'API, des tests A/B avec [Amazon CloudWatch Evidently](https://docs.aws.amazon.com/cloudwatchevidently/latest/APIReference/Welcome.html), des métadonnées d'articles en temps d'inférence, des recommandations contextuelles automatiques, etc.

* Événements de streaming
    - Il s'agit d'un projet visant à montrer comment déployer rapidement une couche API en amont de votre campagne Amazon Personalize et de votre point de terminaison Event Tracker. Pour commencer, accédez au dossier [​streaming_events](operations/streaming_events/)​​ et suivez les instructions contenues dans README.

* Exemples de Lambda
    - Ce dossier commence par un exemple simple de l'intégration de `put_events` dans vos campagnes de personnalisation en utilisant les fonctions Lambda qui traitent les nouvelles données de S3. Pour commencer, accédez au dossier ​​[lambda_examples](operations/lambda_examples/)​​ et suivez les instructions contenues dans README.

* Rotation des filtres
    - Cette ​​[application sans serveur](operations/filter_rotator/)​​ inclut une fonction AWS Lambda qui est exécutée selon un programme donné. Ce processus permet de faire tourner les filtres Personalize qui utilisent des expressions avec des valeurs fixes devant être modifiées au fil du temps. Par exemple, utiliser un opérateur d'intervalle en fonction d'une valeur de date ou d'heure qui vise à inclure/exclure des articles basés sur une fenêtre temporelle dynamique.

* [Moniteur Personalize](https://github.com/aws-samples/amazon-personalize-monitor)
    - Ce projet ajoute des outils de surveillance, d'alerte, de tableau de bord et d'optimisation pour exécuter Amazon Personalize dans vos environnements AWS.

## Architectures de référence

Les architectures de référence suivantes fournissent des exemples d'application d'Amazon Personalize dans tous les secteurs :

* Vente au détail – le ​[Magasin de démonstration de vente au détail](https://github.com/aws-samples/retail-demo-store)​​ est une application web Full-Stack qui implémente la personnalisation à l'aide de Personalize dans une application web, la messagerie et les interfaces de conversation d'IA. Des ateliers pratiques sont disponibles
* Médias et divertissements
* Voyage et accueil

## Ateliers

Le dossier ​[workshops/​​](workshops/) contient une liste de nos ateliers les plus récents :

* POC prêt à l'emploi
* Re:invent 2019

## Outils de science des données

Le dossier [​data_science/](data_science/)​​ contient un exemple sur la façon d'aborder la visualisation des propriétés clés de vos jeux de données d'entrée.

Les composants clés que nous recherchons comprennent :
- Données manquantes, événements en double et consommations d'articles répétées
- Distribution des champs catégoriels selon la loi de puissance
- Analyse de la dérive temporelle pour l'applicabilité au démarrage à froid
- Analyse de la distribution des sessions utilisateur

## Résumé de la licence

Cet exemple de code est distribué sous une licence MIT modifiée. Reportez-vous au fichier LICENSE.
