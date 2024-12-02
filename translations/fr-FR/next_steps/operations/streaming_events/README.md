# Démarrage

Cet exemple présente un élément clé que vous pouvez utiliser afin de construire votre couche d'API pour consommer des recommandations Amazon Personalize et produire des événements en temps réel

Comme nous pouvons le voir ci-dessous, voici l'architecture que vous allez déployer à partir de ce projet.

![Architecture Diagram](images/architecture.png)

**Remarque :** Les campagnes Amazon Personalize et les traqueurs d'événements doivent être déployés indépendamment au préalable pour que vous puissiez terminer ce didacticiel. Vous pouvez déployer votre campagne Amazon Personalize en utilisant l'exemple d'automatisation suivant dans le dossier MLOps, ou en tirant parti du dossier de démarrage.

## Conditions préalables

### Installation d'AWS SAM

Le modèle d'application sans serveur AWS (SAM) est un cadre open-source pour la création d'applications sans serveur. Il fournit une syntaxe abrégée pour exprimer les fonctions, les API, les bases de données et les mappages de sources d'événements. Avec seulement quelques lignes par ressource, vous pouvez définir l'application que vous voulez et la modéliser à l'aide de YAML. Lors du déploiement, SAM transforme et étend la syntaxe SAM dans la syntaxe AWS CloudFormation, ce qui vous permet de créer des applications sans serveur plus rapidement.

**Installer** l'[AWS SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html).
Vous allez ainsi installer les outils nécessaires pour créer, déployer et tester localement votre projet. Dans cet exemple particulier, nous utiliserons AWS SAM pour créer et déployer uniquement. Pour plus d'informations, veuillez consulter notre ​​[documentation](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/what-is-sam.html)​​.

### Créer vos composants Personalize 

​**Créez**​ une campagne Amazon Personalize et joignez-y un traqueur d'événements, après avoir suivi nos [​instructions​​](https://github.com/aws-samples/amazon-personalize-samples/tree/master/getting_started) de démarrage.

Vous pouvez également automatiser cette portion du processus en tirant parti de cet ​[exemple​](https://github.com/aws-samples/amazon-personalize-samples/tree/master/next_steps/operations/ml_ops) de MLOps

## Créer et déployer

Pour déployer le projet, vous devrez exécuter les commandes suivantes :

1. Cloner le référentiel des exemples d'Amazon Personalize
    - `git clone https://github.com/aws-samples/amazon-personalize-samples.git`
2. Accéder au répertoire *​next_steps/operations/streaming_events*
    - `cd amazon-personalize-samples/next_steps/operations/streaming_events`
3. Créez votre projet SAM. [Instructions d'installation](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html)
    - `sam build`
4. Déployez votre projet. SAM offre une option de déploiement guidé. Notez que vous devrez fournir votre adresse e-mail comme paramètre nécessaire pour recevoir une notification.
    - `sam deploy --guided`
5. Saisissez le compartiment S3 où vous souhaitez stocker vos données d'événements, l'ARN de la campagne Personalize et l'ID de l'EventTracker.

## Test des points de terminaison

- Accédez à la [​​console​​](https://console.aws.amazon.com/cloudformation/home?region=us-east-1) Amazon CloudFormation
- Sélectionnez la pile déployée par SAM
- Accédez aux sections de sorties où vous trouverez 2 points de terminaison d'une clé API :
    1. Point de terminaison POST getRecommendations
    2. Point de terminaison d'événements POST
    3. Redirection vers la console API Gateway où vous pouvez cliquer sur la section Afficher la clé pour afficher la clé d'API

Si vous utilisez PostMan ou quelque chose de similaire, vous devrez fournir un en-tête avec :
`x-api-key: <YOUR API KEY VALUE>`

**Exemple de POST getRecommendations :**

*Paramètre de corps :*
```
{
    "userId":"12345"
    
}
```

*Point de terminaison:* `https://XXXXXX.execute-api.us-east-1.amazonaws.com/dev2/recommendations`


**Exemple d'événement POST**

Pour le point de terminaison POST, vous devez donc envoyer un événement similaire à ce qui suit dans le ​​*corps​​* de la demande :

*Point de terminaison:* `https://XXXXXX.execute-api.us-east-1.amazonaws.com/dev2/history`

*Corps :*
```
{
    "Event":{
        "itemId": "ITEMID",
        "eventValue": EVENT-VALUE,
        "CONTEXT": "VALUE" //optional
    },
    "SessionId": "SESSION-ID-IDENTIFIER",
    "EventType": "YOUR-EVENT-TYPE",
    "UserId": "USERID"
}
```

## Résumé

Maintenant que vous avez cette architecture dans votre compte, vous pouvez consommer des recommandations Amazon Personalize par le biais du point de terminaison des recommandations API Gateway POST et diffuser des données d'interactions en temps réel vers le point de terminaison d'événements POST.

Cette architecture comporte deux fonctionnalités supplémentaires :

- Un compartiment S3 contenant vos événements a persisté depuis votre flux Kinesis. Vous pouvez effectuer une analyse sur ce compartiment en utilisant d'autres services AWS tels que Glue et Athena. Par exemple, vous pouvez suivre ce ​[blog​​](https://aws.amazon.com/blogs/big-data/build-and-automate-a-serverless-data-lake-using-an-aws-glue-trigger-for-the-data-catalog-and-etl-jobs/) sur la façon d'automatiser un pipeline ETL.



## Prochaines étapes

Félicitations ! Vous avez bien déployé et testé la couche d'API autour de votre déploiement Amazon Personalize.

Pour plus d'informations sur Obtenir des recommandations, veuillez vous reporter à notre ​​[documentation​​](https://docs.aws.amazon.com/personalize/latest/dg/getting-recommendations.html)
