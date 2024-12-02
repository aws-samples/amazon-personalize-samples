# Rotation des filtres Amazon Personalize

Ce projet contient le code source et les fichiers de prise en charge pour le déploiement d'une application sans serveur qui fournit des capacités de rotation automatique des [filtres](https://docs.aws.amazon.com/personalize/latest/dg/filter.html) pour [Amazon Personalize](https://aws.amazon.com/personalize/), un service d'IA proposé par AWS qui vous permet de créer des outils de recommandation ML personnalisés en fonction de vos données. Les points forts du projet incluent :

- Création de filtres basés sur un modèle de dénomination de filtre dynamique que vous fournissez
- Création d'expressions de filtre basées sur un modèle d'expression de filtre dynamique que vous fournissez
- Suppression des filtres basée sur une expression de correspondance dynamique que vous fournissez (facultatif)
- Publication d'événements sur [Amazon EventBridge](https://aws.amazon.com/eventbridge/) lorsque des filtres sont créés ou supprimés (facultatif)

## <a name='Whatarefilters'></a>Qu'est ce que les filtres ?
Les filtres Amazon Personalize sont un excellent moyen d’appliquer des règles commerciales aux recommandations avant qu'elles ne soient renvoyées à votre application. Ils peuvent être utilisés pour inclure ou exclure la recommandation d'articles à un utilisateur en fonction d'une syntaxe de type SQL qui prend en compte l'historique des interactions de l'utilisateur, les métadonnées de l'article et les métadonnées de l'utilisateur. Par exemple, pour remplir un widget « Regarder à nouveau », recommandez uniquement les films que l'utilisateur a déjà regardé ou ajouté à ses favoris.

```
INCLUDE ItemID WHERE Interactions.event_type IN ('watched','favorited')
```

Ou faites en sorte que les produits actuellement en rupture de stock ne soient pas recommandés.

```
EXCLUDE ItemID WHERE Items.out_of_stock IN ('yes')
```

Vous pouvez même utiliser des filtres dynamiques où les valeurs d'expression de filtre sont spécifiées au moment de l'exécution. Par exemple, recommandez uniquement des films d'un genre spécifique.

```
INCLUDE ItemID WHERE Items.genre IN ($GENRES)
```

Pour utiliser le filtre ci-dessus, vous devez transmettre la ou les valeurs appropriées pour la variable `$GENRE` lors de la récupération des recommandations à l'aide de l'[API GetRecommendations](https://docs.aws.amazon.com/personalize/latest/dg/API_RS_GetRecommendations.html).

Vous pouvez en savoir plus sur les filtres sur le blog AWS Personalize en cliquant [ici](https://aws.amazon.com/blogs/machine-learning/introducing-recommendation-filters-in-amazon-personalize/) et [ici](https://aws.amazon.com/blogs/machine-learning/amazon-personalize-now-supports-dynamic-filters-for-applying-business-rules-to-your-recommendations-on-the-fly/).

## <a name='Whyisfilterrotationnecessary'></a>Pourquoi la rotation des filtres est-elle nécessaire ?
Les filtres constituent d'excellents outils. Toutefois, ils ont des limites. L'une de ces limites est la possibilité de spécifier une valeur dynamique pour une requête de plage (c'est-à-dire, `<`, `<=`, `>`, `>=`). Par exemple, le filtre suivant visant à limiter les recommandations aux nouveaux articles qui ont été créés à partir d'un point de roulement dans le passé n'est **pas** pris en charge.

**CE QUI SUIT NE FONCTIONNERA PAS !**
```
INCLUDE ItemID WHERE Items.creation_timestamp > $NEW_ITEM_THRESHOLD
```

La solution à cette limite consiste à utiliser une expression de filtre avec une valeur codée en dur pour les requêtes de plage.

**CE QUI SUIT FONCTIONNE !**
```
INCLUDE ItemID WHERE Items.creation_timestamp > 1633240824
```

Toutefois, cette solution n'est pas très flexible ni facile à maintenir, car le temps passe, mais votre expression de filtre statique ne bouge pas. La solution de contournement consiste à mettre à jour votre expression de filtre régulièrement afin conserver une fenêtre temporelle dynamique. Malheureusement, les filtres ne peuvent pas être mis à jour. C'est pourquoi un nouveau filtre doit être créé, votre application doit effectuer une transition pour utiliser ce nouveau filtre, et ce n'est qu'à ce moment-là que l'ancien filtre peut être supprimé en toute sécurité.

Le but de cette application sans serveur est de faciliter la maintenance de ce processus en automatisant la création et la suppression de filtres et en vous permettant de fournir une expression dynamique qui est résolue en valeur codée en dur appropriée lorsque le nouveau filtre est créé.

## <a name='Hereshowitworks'></a>Voici comment cela fonctionne

Cette application déploie une [fonction](./src/filter_rotator_function/filter_rotator.py) AWS Lambda, appelée de manière récurrente. Vous contrôlez le programme, qui peut être une [expression cron ou rate](https://docs.aws.amazon.com/lambda/latest/dg/services-cloudwatchevents-expressions.html). La fonction crée un nouveau filtre uniquement s'il n'existe pas déjà de filtre correspondant au modèle de nom du filtre actuel et supprime uniquement les filtres existants correspondant au modèle de suppression. Par conséquent, il est bon d'exécuter la fonction plus souvent que nécessaire (c'est-à-dire si vous ne disposez pas de fenêtres temporelles prévisibles et cohérentes au moment de la rotation des filtres).

La clé de la fonction de rotation des filtres réside dans les modèles utilisés pour vérifier que le modèle actuel existe et si les modèles existants peuvent être supprimés. Étant donné que les modèles sont résolus à chaque exécution de la fonction, la valeur résolue peut changer au fil du temps. Regardons quelques exemples. Vous fournissez ces valeurs de modèle en tant que paramètres CloudFormation au moment de déployer cette application.

### <a name="Currentfilternametemplate"></a>Modèle de nom du filtre actuel

Imaginons que vous souhaitez utiliser un filtre qui recommande uniquement les articles créés récemment. La colonne `CREATION_TIMESTAMP` dans le jeu de données des articles est un champ pratique à utiliser à cet effet. Ce nom de colonne est réservé et est utilisé pour prendre en charge la fonction d'exploration d'articles froids de la recette `aws-user-personalization`. Les valeurs de cette colonne doivent être exprimées au format d'heure Unix sous la forme `long`'s (c'est-à-dire le nombre de secondes écoulées depuis Epoch). L'expression de filtre suivante limite les articles qui ont été créés au cours du mois dernier (`1633240824` est l'heure Unix d'il y a 1 mois au moment de la rédaction de cet article).

```
INCLUDE ItemID WHERE Items.creation_timestamp > 1633240824
```

Vous pouvez également utiliser une colonne de métadonnées personnalisée pour le filtre qui utilise un format plus grossier et/ou lisible par l'homme, mais qui reste comparable pour les requêtes de plage, comme `YYYYMMDD`.

```
INCLUDE ItemID WHERE Items.published_date > 20211001
```

Comme indiqué précédemment, il est impossible de mettre les filtres à jour. Par conséquent, vous ne pouvez pas juste modifier l'expression de filtre du filtre. Vous devez plutôt créer un nouveau filtre avec une nouvelle expression, faire basculer votre application pour utiliser le nouveau filtre, puis supprimer l'ancien filtre. Cela nécessite l'utilisation d'une norme de dénomination prévisible pour les filtres afin que les applications puissent automatiquement basculer vers l'utilisation du nouveau filtre sans apporter aucune modification au codage. En continuant avec le thème de l'heure de création, le nom du filtre pourrait ressembler à ce qui suit.

```
filter-include-recent-items-20211101
```

En supposant que nous voulons effectuer la rotation de ce filtre tous les jours, le nom du filtre du lendemain serait `filter-include-recent-items-20211004`, le suivant serait `filter-include-recent-items-20211005`, et ainsi de suite au fil du temps. Étant donné qu'il existe des limites quant au nombre de filtres actifs que vous pouvez avoir à tout moment, il vous est impossible de précréer un grand nombre de filtres. Au lieu de cela, cette application crée de nouveaux filtres de manière dynamique en fonctions de vos besoins et supprime les anciens, au besoin. Cela fonctionne grâce aux modèles que vous définissez pour le nom et l'expression du filtre et grâce au fait qu'ils sont résolus au moment de l'exécution. Voici un exemple de modèle de nom de filtre qui correspond au schéma décrit ci-dessus.

```
filter-include-recent-items-{{datetime_format(now,'%Y%m%d')}}
```

Le modèle de nom de filtre ci-dessus résout et remplace l'expression comprise entre les caractères `{{` et `}}` (Handlebars ou Mustache) au moment de l'exécution. Dans ce cas, nous prenons l'heure actuelle exprimée en tant que `now` pour la formater à l'aide de l'expression de format de date `%Y%m%d`. Le résultat (à ce jour) est `20211102`. Si la fonction de rotation trouve un filtre existant portant ce nom, il n'est pas nécessaire de créer un nouveau filtre. Sinon, un nouveau filtre est créé et est appelé `filter-include-recent-items-20211102`.

Le paramètre du modèle CloudFormation `PersonalizeCurrentFilterNameTemplate` vous permet de spécifier votre propre modèle de nom de filtre personnalisé.

Les fonctions et les opérateurs disponibles pour utiliser dans la syntaxe du modèle sont décrits ci-dessous.

### <a name="Currentfilterexpressiontemplate"></a>Modèle d'expression de filtre actuel

Au moment de la rotation et de la création du nouveau filtre, il se peut que nous devions également résoudre l'expression de filtre réelle de façon dynamique. Le paramètre CloudFormation `PersonalizeCurrentFilterExpressionTemplate` peut être utilisé à cet effet. Voici quelques exemples.

```
INCLUDE ItemID WHERE Items.CREATION_TIMESTAMP > {{int(unixtime(now - timedelta_days(30)))}}
```

```
INCLUDE ItemID WHERE Items.published_date > {{datetime_format(now - timedelta_days(30),'%Y%m%d')}}
```

Les modèles ci-dessus se résolvent en une expression de filtre codée en dur basée sur l'heure actuelle au moment de leur résolution. Le premier modèle produit une heure Unix (exprimée en secondes tel que requis par Personalize pour `CREATION_TIMESTAMP`) qui date d'il y a 30 jours. Le deuxième modèle produit un entier représentant la date au format `YYYYMMDD` d'il y a 30 jours.

### <a name="Deletefiltermatchtemplate"></a>Supprimer le modèle de correspondance de filtre

Pour finir, nous devons nettoyer les anciens filtres après avoir effectué la transition vers une version plus récente du filtre. Sinon, nous finirons par atteindre une limite. Un modèle de correspondance de nom de filtre peut être utilisé à cet effet et peut être écrit de manière à retarder la suppression pendant un certain temps après la création du nouveau filtre. Cela donne à votre application le temps nécessaire pour effectuer la transition entre l'ancien et le nouveau filtre avant que l'ancien filtre ne soit supprimé. Le paramètre de modèle CloudFormation `PersonalizeDeleteFilterMatchTemplate` est l'endroit où vous spécifiez le modèle de suppression de correspondance de filtre.

Le modèle de suppression de correspondance de filtre suivant correspond aux filtres dont le nom de filtre commence par `filter-include-recent-items-` et dispose d'un suffixe antérieur de plus d'un jour par rapport à aujourd'hui. En d'autres termes, nous avons 1 jour pour faire passer les applications clientes vers le nouveau filtre avant que l'ancien filtre ne soit supprimé. Vous pouvez personnaliser ce délai en fonction de votre application.

```
starts_with(filter.name,'filter-include-recent-items-') and int(end(filter.name,8)) < int(datetime_format(now - timedelta_days(1),'%Y%m%d'))
```

Tous les filtres qui déclenchent ce modèle pour résoudre `true` seront supprimés. Tous les autres resteront intacts. Notez que tous les champs disponibles dans le [FilterSummary](https://docs.aws.amazon.com/personalize/latest/dg/API_FilterSummary.html) de la réponse de [l'API ListFilters](https://docs.aws.amazon.com/personalize/latest/dg/API_ListFilters.html) sont disponibles pour ce modèle. Par exemple, le modèle ci-dessus correspond à `filter.name`. D'autres champs de résumé du filtre tels que `filter.status`, `filter.creationDateTime` et `filter.lastUpdatedDateTime` peuvent également être inspectés dans la logique du modèle.

## <a name='Filterevents'></a>Filtrer les événements

Si vous souhaitez synchroniser la configuration de votre application ou être averti lorsqu'un filtre est créé ou supprimé, vous pouvez éventuellement configurer la fonction de rotation pour publier des événements sur [Amazon EventBridge](https://aws.amazon.com/eventbridge/). Lorsque les événements sont activés, il existe trois types de détails d'événements publiés par la fonction de rotation : `PersonalizeFilterCreated`, `PersonalizeFilterCreateFailed` et `PersonalizeFilterDeleted`. Chacun dispose d'un événement `Source` de `personalize.filter.rotator` et inclut des détails relatifs au filtre créé ou supprimé. Cela vous permet de configurer des règles EventBridge pour traiter les événements à votre guise. Par exemple, lorsqu'un nouveau filtre est créé, vous pouvez traiter l'événement `PersonalizeFilterCreated` dans une fonction Lambda pour mettre à jour la configuration de votre application afin de passer à l'utilisation du nouveau filtre dans les appels d'inférence.
## <a name='Filtertemplatesyntax'></a>Syntaxe du modèle de filtre

La bibliothèque [Simple Eval](https://github.com/danthedeckie/simpleeval) est utilisée comme base pour la syntaxe du modèle. Elle fournit une alternative plus sûre et plus cloisonnée (sandboxed) que l'utilisation de la fonction [eval](https://docs.python.org/3/library/functions.html#eval) de Python. Reportez-vous à la documentation de la bibliothèque Simple Eval pour plus de détails sur les fonctions disponibles et des exemples.

Les fonctions supplémentaires suivantes ont été ajoutées dans le cadre de cette application pour faciliter l'écriture de modèles pour la rotation des filtres.

- `unixtime(value)` : renvoie la valeur de l'heure Unix en fonction d'une chaîne, d'une valeur datetime, d'une date ou d'une heure. Si une chaîne est fournie, elle est d'abord analysée au format datetime.
- `datetime_format(date, pattern)` : formate une datetime, une date ou une heure à l'aide du modèle spécifié.
- `timedelta_days(int)` : renvoie une valeur timedelta pour un nombre de jours. Peut être utilisé pour calculer des dates.
- `timedelta_hours(int)` : renvoie une valeur timedelta pour un nombre d'heures. Peut être utilisé pour calculer des dates.
- `timedelta_minutes(int)` : renvoie une valeur timedelta pour un nombre de minutes. Peut être utilisé pour calculer des dates.
- `timedelta_seconds(int)` : renvoie une valeur timedelta pour un nombre de secondes. Peut être utilisé pour calculer des dates.
- `starts_with(str, prefix)` : renvoie la valeur True si la valeur de chaîne commence par un préfixe.
- `ends_with(str, suffix)` : renvoie la valeur True si la valeur de chaîne se termine par un suffixe.
- `start(str, num)` : renvoie les premiers caractères numériques de la valeur de chaîne
- `end(str, num)` : renvoie les derniers caractères numériques de la valeur de chaîne
- `now` : valeur datetime actuelle

## <a name='Installingtheapplication'></a>Installer l'application

***REMARQUE IMPORTANTE :** le déploiement de cette application dans votre compte AWS crée et consomme des ressources AWS, ce qui coûte de l'argent. La fonction Lambda est appelée en fonction de la planification que vous fournissez, mais elle ne doit généralement pas être appelée plus souvent qu'une fois par heure. Personalize ne facture pas les filtres, mais votre compte limite le nombre de filtres actifs à tout moment. Il existe également des limites sur le nombre de filtres pouvant être en attente ou en cours à tout moment. Par conséquent, si après avoir installé cette application, vous choisissez de ne pas l'utiliser dans le cadre de votre solution, assurez-vous de suivre les instructions de désinstallation de la section suivante pour éviter des frais permanents et pour nettoyer toutes les données.*

Cette application utilise le [modèle d'application sans serveur](https://aws.amazon.com/serverless/sam/) AWS (SAM) pour créer et déployer des ressources dans votre compte AWS.

Pour utiliser l'interface de la ligne de commande SAM, vous avez besoin des outils suivants installés localement.

* SAM CLI – [Installer la SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html)
* [Python 3 installé](https://www.python.org/downloads/)
* Docker – [Installer la version communautaire de Docker](https://hub.docker.com/search/?type=edition&offering=community)

Pour créer et déployer l'application pour la première fois, exécutez la commande suivante dans votre shell :

```bash
sam build --use-container --cached
sam deploy --guided
```

Si la première commande vous renvoie une erreur indiquant que vous ne pouvez pas télécharger l'image Docker à partir de `public.ecr.aws`, vous devrez peut-être vous connecter. Exécutez la commande suivante, puis réessayez les deux commandes ci-dessus.

```bash
aws ecr-public get-login-password --region us-east-1 | docker login --username AWS --password-stdin public.ecr.aws
```

La première commande crée la source de l'application. La deuxième commande empaquette et déploie l'application sur votre compte AWS, avec une série d'invites :

| Invite/Paramètre | Description | Valeur par défaut |
| --- | --- | --- |
| Nom de la pile | Le nom de la pile à déployer sur CloudFormation. Ce paramètre doit être unique à votre compte et à votre région. | `personalize-filter-rotator` |
| Région AWS | La région AWS dans laquelle vous souhaitez déployer cette application. | Votre région actuelle |
| Paramètre PersonalizeDatasetGroupArn | ARN du groupe du jeu de données dans lequel la rotation doit être effectuée. | |
| Paramètre PersonalizeCurrentFilterNameTemplate | Modèle à utiliser lors de la vérification et de la création du filtre actuel. | |
| Paramètre PersonalizeCurrentFilterExpressionTemplate | Modèle à utiliser au moment de la création de l'expression de filtre lors de la création du filtre actuel. | |
| Paramètre PersonalizeDeleteFilterMatchTemplate (facultatif) | Modèle à utiliser pour faire correspondre les filtres existants qui doivent être supprimés. | |
| Paramètre RotationSchedule | Expression cron ou rate pour contrôler la fréquence d'appel de la fonction de rotation. | `rate(1 day)` |
| Paramètre Timezone | Définissez le fuseau horaire de l'environnement Lambda de la fonction de rotation pour qu'il corresponde au vôtre. | `UTC` |
| Paramètre PublishFilterEvents | Indique s'il faut publier des événements sur le bus EventBridge par défaut lorsque des filtres sont créés et supprimés. | `Yes` |
| Confirmer les modifications avant le déploiement | Si ce paramètre est défini sur oui, tous les ensembles de modification CloudFormation vous sont présentés avant l'exécution pour une vérification manuelle. Si ce paramètre est défini sur non, l'interface de la ligne de commande AWS SAM déploie automatiquement les modifications apportées à l'application. | |
| Autoriser la création de rôles SAM CLI IAM | Étant donné que cette application crée des rôles IAM pour permettre aux fonctions Lambda d'accéder aux services AWS, ce paramètre doit être défini sur `Yes`. | |
| Sauvegarder les arguments dans samconfig.toml | Si ce paramètre est défini sur oui, vos choix seront sauvegardés dans un fichier de configuration à l'intérieur de l'application, de sorte qu'à l'avenir, il vous suffira de relancer l'exécution de `sam deploy` sans les paramètres pour déployer les modifications dans votre application. | |

**CONSEIL** : l'outil de la ligne de commande SAM vous offre la possibilité de sauvegarder vos valeurs paramétriques dans un fichier local (`samconfig.toml`) afin qu'elles soient disponibles par défaut lors du prochain déploiement de l'application. Cependant, SAM place vos valeurs paramétriques entre guillemets. Par conséquent, si les valeurs paramétriques de votre modèle contiennent des valeurs de chaîne incorporées (comme les expressions de format de date présentées dans les exemples ci-dessus), assurez-vous d'utiliser des guillemets simples pour ces valeurs incorporées. Sinon, vos valeurs paramétriques ne seront pas correctement sauvegardées.

## <a name='Uninstallingtheapplication'></a>Désinstaller l'application

Pour supprimer les ressources que cette application a créé dans votre compte AWS, utilisez l'AWS CLI. En supposant que vous avez utilisé le nom de l'application par défaut pour le nom de la pile (`personalize-filter-rotator`), vous pouvez exécuter la commande suivante :

```bash
aws cloudformation delete-stack --stack-name personalize-filter-rotator
```

Sinon, vous pouvez supprimer la pile dans CloudFormation dans la console AWS.

## <a name='FAQs'></a>Questions fréquentes

***Q : Comment puis-je modifier la fréquence d'exécution du script de rotation une fois que cette solution est déployée ?***

***R :*** Il existe deux options. Vous pouvez redéployer cette solution avec une fréquence différente. Un ensemble de modification sera créé pour mettre à jour uniquement la règle EventBridge avec la nouvelle fréquence. Autrement, vous pouvez modifier la règle EventBridge créée par cette solution directement dans votre compte AWS.

***Q : Comment puis-je utiliser cette solution pour effectuer la rotation de plusieurs filtres avec différents modèles et différentes fréquences de mise à jour ?***

***R :*** Une fois que vous avez déployé cette solution, vous pouvez créer des règles EventBridge supplémentaires qui appellent la fonction de rotation avec des valeurs d'entrée différentes. Pour la cible de la règle, sélectionnez la fonction de rotation et spécifiez une valeur d'entrée constante JSON au format suivant :

```javascript
{
    "datasetGroupArn": "[INSERT_PERSONALIZE_DATASET_GROUP_ARN]",
    "currentFilterNameTemplate": "[INSERT_CURRENT_FILTER_NAME_TEMPLATE]",
    "currentFilterExpressionTemplate": "[INSERT_CURRENT_FILTER_EXPRESSION_TEMPLATE]",
    "deleteFilterMatchTemplate": "[INSERT_DELETE_FILTER_MATCH_TEMPLATE]"
}
```

## <a name='Licensesummary'></a>Récapitulatif de licences

Cet exemple de code est distribué sous une licence MIT modifiée. Reportez-vous au fichier LICENSE.
