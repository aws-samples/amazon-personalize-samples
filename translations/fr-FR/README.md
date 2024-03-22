# Exemples Amazon Personalize

Blocs-notes et exemples sur la façon d'intégrer et d'utiliser diverses fonctionnalités d'Amazon Personalize

## Démarrer avec Amazon Personalize

Le dossier [getting_started/](getting_started/) contient un modèle CloudFormation qui déploiera toutes les ressources dont vous avez besoin pour créer votre première campagne avec Amazon Personalize.

Les bloc-notes fournis peuvent également servir de modèle pour créer vos propres modèles avec vos propres données. Ce référentiel est cloné dans l'environnement afin que vous puissiez explorer les bloc-notes plus avancés avec cette approche également.

## Prochaines étapes d'Amazon Personalize

Le dossier [next_steps/](next_steps/) contient des exemples détaillés des prochaines étapes typiques suivantes de votre parcours Amazon Personalize. Ce dossier contient le contenu détaillé suivant :

* Principaux cas d'utilisation
  - [Personnalisation de l'utilisateur](next_steps/core_use_cases/user_personalization)
  - [Personnaliser le classement](next_steps/core_use_cases/personalized_ranking)
  - [Articles connexes](next_steps/core_use_cases/related_items)
  - [Recommandations par lots](next_steps/core_use_cases/batch_recommendations)
  - [Répartition des utilisateurs](next_steps/core_use_cases/user_segmentation)

* Exemples d'opérations évolutives pour vos déploiements Amazon Personalize
    - [Maintenir des expériences personnalisées avec le machine learning](https://aws.amazon.com/solutions/implementations/maintaining-personalized-experiences-with-ml/)
        - Cette solution AWS vous permet d'automatiser le processus de bout en bout d'importation de jeux de données, de création de solutions et de versions de solutions, de création et de mise à jour de campagnes, de création de filtres et d'exécution de travaux d'inférence par lots. Ces processus peuvent être exécutés à la demande ou déclenchés en fonction d'un calendrier que vous définissez.
    - [MLOps Step Function](next_steps/operations/ml_ops) (héritée)
        - Il s'agit d'un projet visant à montrer comment déployer rapidement une campagne de personnalisation de façon entièrement automatisée à l'aide d'AWS Step Functions. Pour commencer, accédez au dossier ​​[ml_ops](next_steps/operations/ml_ops)​​ et suivez les instructions contenues dans README. Cet exemple a été remplacé par la solution ​[Maintenir des expériences personnalisées avec le machine learning](https://aws.amazon.com/solutions/implementations/maintaining-personalized-experiences-with-ml/).
    - [Kit SDK pour la science des données MLOps](next_steps/operations/ml_ops_ds_sdk)
        - Il s'agit d'un projet visant à montrer comment déployer rapidement une campagne de personnalisation de manière entièrement automatisée à l'aide du kit SDK d'AWS Data Science. Pour commencer, accédez au dossier [​​ml_ops_ds_sdk](next_steps/operations/ml_ops_ds_sdk)​​ et suivez les instructions contenues dans README.
    - [API de personnalisation](https://github.com/aws-samples/personalization-apis)
        - Cadre d'API à faible latence en temps réel qui se situe entre vos applications et les systèmes de recommandation tels qu'Amazon Personalize. Fournit les bonnes pratiques de mise en œuvre du cache des réponses, des configurations de passerelles d'API, des tests A/B avec [Amazon CloudWatch Evidently](https://docs.aws.amazon.com/cloudwatchevidently/latest/APIReference/Welcome.html), des métadonnées d'articles en temps d'inférence, des recommandations contextuelles automatiques, etc.
    - [Exemples de Lambda](next_steps/operations/lambda_examples)
        - Ce dossier commence par un exemple simple de l'intégration de `put_events` dans vos campagnes de personnalisation en utilisant les fonctions Lambda qui traitent les nouvelles données de S3. Pour commencer, accédez au dossier ​​[lambda_examples](next_steps/operations/lambda_examples)​​ et suivez les instructions contenues dans README.
    - [Moniteur Personalize](https://github.com/aws-samples/amazon-personalize-monitor)
        - Ce projet ajoute des outils de surveillance, d'alerte, de tableau de bord et d'optimisation pour exécuter Amazon Personalize dans vos environnements AWS.
    - [Événements de streaming](next_steps/operations/streaming_events)
        - Ce projet a pour but de montrer comment déployer rapidement une couche d'API devant votre campagne Amazon Personalize et votre point de terminaison EventTracker. Pour commencer, accédez au dossier [​streaming_events](operations/streaming_events/)​​ et suivez les instructions contenues dans README.
    - [Rotation des filtres](next_steps/operations/filter_rotator)
        - Cette ​​application sans serveur​​ inclut une fonction AWS Lambda qui est exécutée selon un programme donné. Ce processus permet de faire tourner les filtres Personalize qui utilisent des expressions avec des valeurs fixes devant être modifiées au fil du temps. Par exemple, utiliser un opérateur d'intervalle en fonction d'une valeur de date ou d'heure qui vise à inclure/exclure des articles basés sur une fenêtre temporelle dynamique.

* Ateliers
    - Le dossier [Workshops/](next_steps/workshops/) contient une liste de nos ateliers les plus récents :
        - [POC prêt à l'emploi](next_steps/workshops/POC_in_a_box)
        - [re:Invent 2019](next_steps/workshops/Reinvent_2019)
        - [Journée d'immersion](next_steps/workshops/Immersion_Day)
    - [Intégrations des partenaires](https://github.com/aws-samples/retail-demo-store#partner-integrations)
        - Reportez-vous aux ateliers qui montrent comment utiliser Personalize avec des partenaires tels qu'Amplitude, Braze, Optimizely et Segment.

* Outils de science des données
    - Le dossier [​data_science/](next_steps/data_science/)​​ contient un exemple sur la façon d'aborder la visualisation des propriétés clés de vos jeux de données d'entrée.
        - Données manquantes, événements en double et consommations d'articles répétées
        - Distribution des champs catégoriels selon la loi de puissance
        - Analyse de la dérive temporelle pour l'applicabilité au démarrage à froid
        - Analyse de la distribution des sessions utilisateur

* Démonstrations/Architectures de référence
    - [Magasin de démonstration pour la vente au détail](https://github.com/aws-samples/retail-demo-store)
        - Exemple d'application web de vente au détail et de plateforme d'atelier démontrant comment offrir des expériences client personnalisées omnicanal à l'aide d'Amazon Personalize.

## Résumé de la licence

Cet exemple de code est distribué sous une licence MIT modifiée. Reportez-vous au fichier LICENSE.
