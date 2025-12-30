# Aide-mémoire d'Amazon Personalize

## Amazon Personalize est-il un bon choix ?

Amazon Personalize est une plateforme idéale pour l'exploitation d'un système de recommandation à grande échelle sur AWS. Toutefois, elle ne convient pas à tous les scénarios de personnalisation ou de recommandation. Le tableau ci-dessous constitue un guide approximatif des bons et mauvais ajustements.

|Bon choix	|Mauvais choix	|
|---	|---	|
|Recommandations d'articles à des utilisateurs connus. Films aux utilisateurs en fonction de leur historique de visionnage.	|Recommandations basées sur des indicateurs de métadonnées explicites. Lorsqu'un nouvel utilisateur définit ses préférences pour guider ses recommandations.	|
|Recommandation de nouveaux articles aux utilisateurs connus. Un site de vente au détail ajoutant de nouveaux articles à vendre à ses utilisateurs existants.	|Faibles volumes de données pour les utilisateurs, les articles et les interactions (voir le graphique ci-dessous).	|
|Recommandation d'articles à de nouveaux utilisateurs. Un utilisateur vient de s'inscrire et reçoit aussitôt des recommandations	|Principalement des utilisateurs non identifiés. Une application qui ne permet pas aux utilisateurs d'avoir un historique de leurs activités.	|
|Recommandation de nouveaux articles à de nouveaux utilisateurs. Un site de vente au détail recommandant de nouveaux articles à un nouvel utilisateur.	|**Applications de la meilleure action suivante –** Personalize recommande des articles probables. Ne comprend pas les flux et les séquences appropriés.	|

### Volume de données minimum suggéré

1. Plus de 50 utilisateurs.
2. Plus de 50 articles.
3. Plus de 1 500 interactions.

Si vos jeux de données ne sont pas adaptés, c'est qu'il est trop tôt pour Amazon Personalize.


## Cas d'utilisation par recette

Quels types de cas d'utilisation peuvent être résolus et comment ?

1. **Recommandations personnalisées**`User-Personalization` :
    1. Il s'agit d'un des principaux cas d'utilisation d'Amazon Personalize, qui utilise les données relatives à l'interaction entre l'utilisateur et l'article pour créer un modèle de recommandation ciblant directement chaque utilisateur, et qui permet d'ajouter de nouveaux utilisateurs à la volée avec PutEvents sans nouvel entraînement. PutEvents permet également aux utilisateurs de voir des recommandations basées sur leur comportement le plus récent, afin que vous ne perdiez pas ces informations supplémentaires. Pour améliorer les résultats, vous pouvez également introduire des articles spécifiques au contexte, comme le type d'appareil ou la localisation.
    2. Vous pouvez également ajouter des métadonnées sur les articles et les utilisateurs afin de mieux enrichir le modèle, ou de filtrer les recommandations par attribut.
    3. Pour les cas d'utilisation de la vidéo à la demande et de la vente au détail, les recommandations de domaine « Bons plans pour vous » et « Recommandés » vous permettent d'être opérationnel rapidement et avec moins de frais opérationnels.
2. **Recommandation d'articles aux nouveaux utilisateurs** `User-Personalization` :
    1. Il est possible d'ajouter de nouveaux utilisateurs (utilisateurs froids) à vos solutions existantes de personnalisation des utilisateurs en utilisant la fonction PutEvents. Chaque nouvel utilisateur commence par une représentation dans le service qui renvoie les articles populaires. Cette représentation est renvoyée à la suite de l'action de l'utilisateur. À mesure qu'il interagit avec le contenu de l'application et que les événements sont envoyés par l'application à Personalize, les recommandations sont mises à jour sans qu'il soit nécessaire d'entraîner à nouveau le modèle. Ainsi, la personnalisation est actualisée sans qu'il soit nécessaire de suivre un entraînement continu.
3. **Recommandation de nouveaux articles ** `User-Personalization`:
    1. Cette fonction est extrêmement utile lorsque votre client dispose de nouveaux articles (articles froids) qui doivent être présentés à leurs utilisateurs avec une certaine forme de personnalisation. Ainsi, les articles peuvent être recommandés sans historique sur la base de facteurs liés aux métadonnées.
    2. Vous pouvez également l'utiliser pour l'entraînement et la mise à jour incrémentiels de votre jeu de données afin de faciliter le démarrage à froid de nouveaux articles.
    3. Enfin, cette approche tire parti d'une capacité d'exploration de type bandit pour vous aider à déterminer rapidement les résultats qui ont un sens et ceux qui n'en ont pas pour les recommandations, une approche bien meilleure que celle qui consiste à pousser aveuglément du nouveau contenu.
4. **Reclassement par ordre de pertinence** `Personalized-Ranking` :
    1. Utilise le même algorithme HRNN que pour la personnalisation de l'utilisateur, mais prend en compte un utilisateur ET une collection d'articles. La collection d'articles est ensuite examinée et les articles classés par ordre de pertinence pour l'utilisateur. Ceci est idéal pour promouvoir une collection présélectionnée d'articles et savoir ce qu'il convient de promouvoir pour un utilisateur particulier.
5. **Articles connexes** `Similar-Items`/`SIMS` :
    1. `Similar-Items`Modèle de deep learning qui tient compte à la fois des données d'interaction et des métadonnées des articles pour équilibrer les recommandations d'articles connexes en fonction de l'historique des interactions et de la similarité des métadonnées des articles. Utile lorsque vous disposez de moins de données sur les interactions, mais de métadonnées de qualité sur les articles ou lorsque vous introduisez fréquemment des articles nouveaux ou non.
    2. `SIMS`Idée assez simple, mise en œuvre grâce au filtrage collaboratif article-article, mais qui consiste essentiellement à examiner comment les gens interagissent avec des articles particuliers, puis à déterminer la similarité des articles à un niveau global sur la base des données d'interaction. Ne prend pas en compte les métadonnées des articles ou des utilisateurs et n'est pas adapté à chaque utilisateur. Utile lorsque vous avez beaucoup de données d'interaction pertinentes, que vous n'avez pas beaucoup d'articles froids (catalogue changeant) et/ou que vous manquez de métadonnées sur les articles.
    3. Pour les cas d'utilisation de la vidéo à la demande et de la vente au détail, les recommandations de domaine « Parce que vous avez regardé X », « Davantage comme X », « Fréquemment acheté ensemble » et « Les clients qui ont regardé X ont également regardé » vous permettent d'être opérationnel rapidement et avec moins de frais.
6. **Fréquemment achetés ensemble** `Similar-Items`/`SIMS` :
    1. La clé est de préparer les bonnes données utilisées pour entraîner un modèle dans Personalize et de choisir la bonne recette. Par exemple, entraînez un modèle SIMS uniquement sur les données d'achat et, si possible, uniquement sur les données d'achat où les clients ont acheté plusieurs articles et/ou acheté des articles dans plusieurs catégories. Ainsi, le comportement souhaité sera intégré au modèle et les recommandations seront diversifiées (ce que vous souhaitez pour ce cas d'utilisation).
    2. SIMS peut également être combiné avec le Personalized-Ranking (classement personnalisé) pour reclasser les recommandations du SIMS avant de les présenter à l'utilisateur. Ainsi, les articles qui sont fréquemment achetés ensemble peuvent être commandés de manière personnalisée.
    3. La recommandation de domaine « Fréquemment acheté ensemble » vous permettra d'être opérationnel rapidement et avec moins de frais.
7. **Les plus populaires** `Popularity-Count` :
    1. Il ne s'agit pas de machine learning, mais simplement d'une base de référence à partir du comptage des articles avec lesquels on interagit le plus souvent. Cette recette est utile pour les recommandations d'articles populaires ou pour créer une base de référence de métriques hors ligne qui peut être utilisée pour la comparaison avec des versions de solutions créées à l'aide d'autres recettes de personnalisation utilisateur avec les mêmes jeux de données.
    2. Pour les cas d'utilisation de la vidéo à la demande et de la vente au détail, les recommandations de domaine « Les plus populaires », « Les plus consultés » et « Les succès de vente » vous permettent d'être opérationnel rapidement et avec moins de frais.
8. **Répartition des utilisateurs** `Item-Affinity`/`Item-Attribute-Affinity` :
    1. Créez des segments d'utilisateurs en fonction de leur affinité avec des articles spécifiques de votre catalogue ou de leur affinité avec des attributs d'articles. Une excellente adéquation avec les campagnes de marketing où vous cherchez à cibler les utilisateurs qui auront un intérêt pour des articles spécifiques que vous cherchez à promouvoir ou des articles similaires à des articles existants.

## Fonctions irrésistibles :

1. [Groupes de jeux de données du domaine](https://docs.aws.amazon.com/personalize/latest/dg/domain-dataset-groups.html) : systèmes de recommandation pour les cas d'utilisation de la vidéo à la demande et de la vente au détail
    1. Un *groupe de jeux de données de domaine* est un conteneur Amazon Personalize pour les ressources préconfigurées spécifiques à un domaine, notamment les jeux de données, les recommandeurs et les filtres. Utilisez un groupe de jeux de données de domaine si vous avez une application de streaming vidéo ou de commerce électronique et que vous voulez laisser Amazon Personalize trouver les meilleures configurations pour vos recommandeurs.
2. Recommandations contextuelles
    1. Permet d'étendre les recommandations à un état qui varie en fonction de l'interaction plutôt que d'être spécifique à l'utilisateur ou à l'article. Réfléchissez à l'emplacement actuel de l'utilisateur, au dispositif/canal utilisé, à l'heure de la journée, au jour de la semaine, etc.
    2. Reportez-vous à ce billet de blog pour avoir un exemple détaillé : https://aws.amazon.com/blogs/machine-learning/increasing-the-relevance-of-your-amazon-personalize-recommendations-by-leveraging-contextual-information/.
3. Interaction et filtrage des métadonnées
    1. Filtrez les recommandations en fonction de l'historique des interactions de l'utilisateur ou des attributs de métadonnées pour les articles ou l'utilisateur actuel. Très pratique dans presque toutes les charges de travail des médias ou de la vente au détail. Par exemple, excluez les articles récemment achetés ou en rupture de stock ou incluez/excluez les articles recommandés en fonction de la catégorie ou du genre.
    2. Pour en savoir plus, reportez-vous à ce billet de blog : https://aws.amazon.com/blogs/machine-learning/enhancing-recommendation-filters-by-filtering-on-item-metadata-with-amazon-personalize/
4. Inférence par lot
    1. Idéal pour exporter de grandes quantités de recommandations vers des fichiers pour les caches, pour les campagnes d'e-mailing ou simplement pour l'exploration générale.
5. Campagnes AutoScaling
    1. Le service s'adaptera automatiquement à vos demandes de trafic si une campagne particulière est souscrite excessivement. Il sera ensuite ramené à la capacité minimale demandée lorsque le volume de trafic diminuera.
6. Texte non structuré comme métadonnées d'articles
    1. Ajoutez vos descriptions de produits, le synopsis de votre intrigue vidéo ou le contenu de votre article en tant que champ de métadonnées d'article et laissez Personalize utiliser le traitement du langage naturel (NLP) pour extraire les caractéristiques cachées de votre texte afin d'améliorer la pertinence des recommandations.
7. Put Events
    1. Permet aux applications de mettre à jour Personalize en temps réel en fonction des changements d'intention découlant du comportement de l'utilisateur. En d'autres termes, chaque demande ultérieure peut s'adapter à cette intention SANS nouvel entraînement.
8. Put Items/Put Users
    1. Permet aux applications d'ajouter/mettre à jour des articles ou des utilisateurs individuels ou en mini lots sans avoir à télécharger les ensembles de données complets des articles et des utilisateurs.
    2. Pour en savoir plus, reportez-vous aux FAQ ci-dessous.
9. Intégration KMS
    1. Toutes les données peuvent être cryptées à l'aide d'une clé gérée par le client ; toutes les données sont cryptées quoi qu'il en soit.
10. Aucun partage d'informations
    1. Toutes les données des clients sont totalement isolées et ne sont pas exploitées pour améliorer les recommandations d'Amazon ou de toute autre partie.
    2. Les modèles sont réservés au compte AWS du client.

## Série de vidéos :

1. Présentation d'Amazon Personalize : https://www.youtube.com/c/amazonwebservices/videos
2. Comprendre vos données avec Amazon Personalize : https://www.youtube.com/watch?v=TEioktJD1GE
3. Résoudre des cas d'utilisation réels avec Amazon Personalize : https://www.youtube.com/watch?v=9N7s_dVVWBE
4. Présenter vos recommandations personnalisées Amazon à vos utilisateurs : https://www.youtube.com/watch?v=oeVYCOFNFMI
5. Mettez en production votre POC Amazon Personalize : https://www.youtube.com/watch?v=3YawVCO6H14

## FAQ :

1. À quelle fréquence dois-je refaire l'entraînement ?
    1. La fréquence de nouveaux entraînements dépend des besoins de l'entreprise. À quelle fréquence avez-vous besoin de connaître globalement vos utilisateurs et la façon dont ils utilisent les articles ? À quelle fréquence devez-vous inclure de nouveaux articles ? Les réponses déterminent la fréquence à laquelle vous devez refaire l'entraînement. En général, la plupart des clients refont l'entraînement chaque semaine. Vous trouverez ci-dessous des conseils plus détaillés.
    2. Si vous utilisez la recette « aws-user-personalization », le service mettra automatiquement à jour la version de la solution en arrière-plan toutes les 2 heures (sans coût supplémentaire). Ce processus de mise à jour automatique intégrera les nouveaux articles ajoutés depuis la dernière mise à jour, afin qu'ils puissent commencer à être recommandés aux utilisateurs (c'est-à-dire les articles de démarrage à froid). Il fonctionne en coordination avec le paramètre explorationWeight défini sur la campagne pour contrôler le poids placé sur la recommandation d'articles nouveaux/froids par rapport aux articles pertinents (explorer/exploiter).
    3. Si la fréquence de mise à jour automatique de 2 heures n'est pas suffisante pour introduire de nouveaux articles, vous pouvez créer manuellement une nouvelle version de la solution avec trainingMode=UPDATE et mettre à jour la campagne plus fréquemment (c'est-à-dire toutes les heures). Cette action est identique à celle de la mise à jour automatique, mais à une fréquence définie par le client. Cependant, il y a un coût pour les heures d'entraînement pour le faire manuellement.
    4. Que le mode de mise à jour soit automatique ou manuel, le modèle n'est pas entièrement entraîné à nouveau. Le client devra toujours créer occasionnellement une nouvelle version de la solution avec trainingMode=FULL pour refaire entièrement l'entraînement du modèle. Il est important de le faire de temps en temps pour recalculer les poids du modèle sur la base de toutes les données, mais le processus de mise à jour automatique rend le nouvel entraînement complet nécessaire moins fréquemment. C'est là qu'interviennent les conseils hebdomadaires. Laissez donc la mise à jour automatique fonctionner toute la semaine et faites un nouvel entraînement complet une fois par semaine.
    5. Pour être plus précis dans la fréquence de nouvel entraînement, une autre approche consiste à surveiller les métriques en ligne. Lorsqu'elles commencent à s'éloigner (dérive du modèle), il est temps de refaire l'entraînement.
2. Comment ajouter un nouvel utilisateur ?
    1. Si vous utilisez l'API PutEvents, le nouvel utilisateur existe dès que vous enregistrez sa première action. Si vous n'exploitez pas cette possibilité, l'utilisateur existera dans le système dès que vous aurez refait l'entraînement d'un modèle qui contient son comportement dans votre ensemble de données d'interactions.
    2. Si votre utilisateur n'est pas connu (un nouvel utilisateur anonyme non inscrit), vous pouvez toujours travailler pour le faire démarrer à froid. Si vous pouvez attribuer immédiatement un nouvel UUID pour leur utilisateur et leur sessionID, c'est que vous pouvez continuer le processus tel que défini ci-dessus pour démarrer à froid un utilisateur.
    3. Si ce chemin ne fonctionne pas, vous pouvez toujours générer un nouvel UUID pour le sessionID, appeler PutEvents sans userID, puis continuer à spécifier le même sessionID après qu'un userID valide a été généré pour eux. Lorsque vous refaites l'entraînement, Personalize combinera les données historiques avec les données PutEvents, et lorsqu'il verra des identifiants de séance correspondants, il combinera toutes les interactions anonymes antérieures avec les interactions non anonymes de l'utilisateur. Vous pourrez ainsi spécifier l'historique avant qu'il ne dispose d'un ID utilisateur interne valide.
    4. Vous pouvez ajouter/mettre à jour les utilisateurs individuellement ou par mini-lots avec l'API PutUsers. Cependant, seuls les utilisateurs ayant des interactions recevront des recommandations personnalisées, soit après un nouvel entraînement, soit lors d'un démarrage à froid avec l'API PutEvents.
3. Comment puis-je ajouter un nouvel article ?
    1. Il y a deux façons d'ajouter des articles au jeu de données des articles : 1/ Ajouter de nouveaux articles au jeu de données d'articles en téléchargeant le jeu de données complet à l'aide d'une tâche d'importation de jeu de données, ou 2/ Ajouter des articles séparément ou par mini-lots à l'aide de l'API PutItems.
    2. Les nouveaux articles seront incorporés dans les recommandations après le nouvel entraînement si des interactions existent également (toutes les recettes) ou le démarrage à froid des recommandations de nouveaux articles avec ou sans interactions après la mise à jour de la solution (trainingMode = FULL/UPDATE pour aws-user-personalization et HRNN-Coldstart uniquement).
    3. Par exemple, vous pouvez diffuser de manière organique de nouveaux articles dans votre jeu de données historiques en plaçant des bannières pour les nouvelles versions. Tout ce qui amène un utilisateur à interagir avec les nouveaux articles et à enregistrer cette action peut améliorer les recommandations après le prochain entraînement.
4. Comment puis-je filtrer les résultats pour certaines conditions ?
    1. Utilisation de la fonction de filtrage pour les interactions (https://aws.amazon.com/blogs/machine-learning/introducing-recommendation-filters-in-amazon-personalize/) ou les informations de métadonnées (https://aws.amazon.com/blogs/machine-learning/enhancing-recommendation-filters-by-filtering-on-item-metadata-with-amazon-personalize/).
    2. Le filtrage basé sur l'historique des interactions ne prend actuellement en compte que les 100 interactions les plus récentes en temps réel (API PutEvents) et les 200 interactions historiques les plus récentes dans le jeu de données au moment du nouvel entraînement. Tous les types d'événements sont inclus dans les limites 100/200.
5. J'ai besoin de filtrer des articles sur la base d'une valeur de date mobile, mais les filtres ne prennent pas en charge les valeurs dynamiques pour les opérateurs de plage. Quelles sont mes options ?
    1. Les opérateurs de plage ne peuvent actuellement pas être utilisés avec des valeurs dynamiques. Vous devez donc créer une expression de filtre avec une valeur fixe, puis alterner le filtre périodiquement pour mettre à jour la valeur fixe. La solution de [rotation de filtre](https://github.com/aws-samples/amazon-personalize-samples/tree/master/next_steps/operations/filter_rotator) peut être utilisée pour automatiser le processus d'alternance.
6. Pourquoi devrais-je utiliser Amazon Personalize plutôt qu'une solution personnalisée ?
    1. En supposant que vos données et vos cas d'utilisation concordent, il s'agit d'un excellent moyen de présenter plus rapidement aux utilisateurs finaux le meilleur modèle de sa catégorie. Comme Personalize gère la charge opérationnelle liée à l'exécution d'un système de recommandation à grande échelle, vous avez plus de temps à consacrer à l'amélioration de l'ingénierie des fonctionnalités, la collecte de données, les expériences des utilisateurs ou la résolution d'autres problèmes.
7. J'ai un cas d'utilisation où mes clients achètent des articles ou interagissent avec les articles de mon catalogue de manière peu fréquente (par exemple, l'achat d'une voiture). Personalize est-il toujours un bon choix ?
    1. Oui. Personalize peut encore être efficace pour ce type de cas d'utilisation. Par exemple, un modèle SIMS peut être entraîné sur la base de toute l'activité de l'utilisateur, comme l'historique de navigation ou d'achat (en ligne et/ou hors ligne), puis utilisé pour les recommandations d'articles similaires sur les pages de détails des articles. Vous pouvez ainsi tirer parti de l'activité récente de tous les utilisateurs actifs pour faire des recommandations pertinentes aux utilisateurs qui reviennent.
    2. Les recommandations en temps réel sont également efficaces dans ce cas, car Personalize est capable d'apprendre des intérêts actuels d'un utilisateur et d'adapter rapidement ses recommandations. Par exemple, vous pouvez commencer par recommander des articles populaires, puis personnaliser rapidement les recommandations après la diffusion de quelques interactions à l'aide de l'API PutEvents.
8. Dois-je utiliser AutoML ?
    1. Non. Les recettes résolvent des cas d'utilisation différents. Prenez le temps de sélectionner la recette la plus appropriée pour votre cas d'utilisation et ignorez cette fonction.
9. Dois-je utiliser HPO / À quelle fréquence ?
    1. Peu souvent. Prenez les résultats d'un travail HPO et utilisez-les explicitement dans la configuration de la solution pour plusieurs nouveaux entraînements. Ensuite, exécutez à nouveau HPO et recommencez. Les paramètres réglés de façon réaliste ne devraient pas changer beaucoup entre les tâches d'entraînement. Cette approche vous permettra de réduire les temps d'entraînement, et donc les coûts, par rapport à l'exécution de HPO pour toutes les tâches d'entraînement, sans altérer la précision du modèle.
10. Comment puis-je prévoir le prix de l'entraînement ?
    1. Malheureusement, il est pratiquement impossible de le savoir à l'avance, mais nous disposons de quelques tests effectués sur le jeu de données MovieLens. Par exemple, en utilisant `User-Personalization`, il faut environ six heures humaines pour l'entraînement sur 25 millions d'interactions, mais moins d'une heure humaine pour l'entraînement sur cent mille interactions. L'entraînement étant réparti sur plusieurs hôtes, les heures réelles sont de 53,9 heures pour 50 millions et 2,135 heures pour cent mille. La facturation se fait sur les heures réelles, pas sur les heures humaines.
11. Qu'est-ce qu'une heure TPS et quel est son rapport avec la tarification/l'utilisabilité ?
    1. Amazon Personalize lance des ressources de calcul dédiées qui resteront provisionnées afin de répondre à vos exigences de débit minimum (Transactions par seconde ou TPS). Elles sont facturées en termes d'heures pendant lesquelles ces ressources sont allouées, donc une heure TPS. Une heure TPS est la capacité de calcul nécessaire pour fournir une recommandation par seconde pendant une heure entière.
    2. L'utilisation est mesurée par incréments de 5 minutes où le maximum du nombre moyen de demandes et le débit minimum provisionné dans chaque incrément est utilisé comme valeur de l'heure TPS. Par conséquent, lorsque le service passe au-dessus du TPS minimum provisionné, le client n'est facturé que pour la capacité réellement consommée. Les heures TPS pour tous les incréments de 5 minutes sont additionnées pendant la période de facturation pour déterminer le total des heures TPS pour les calculs de facturation.
    3. Le service augmentera automatiquement sa capacité si votre trafic dépasse le TPS minimum prévu pour la campagne, une option qui s'est avérée précieuse pour nombre de nos clients. Un tampon de capacité est alloué au-dessus du TPS minimum provisionné pour permettre au service d'absorber les augmentations de la charge des requêtes pendant qu'il monte en charge.
    4. Si votre client sait qu'il va atteindre un niveau d'activité élevé, par exemple lors d'une vente flash ou d'un événement promotionnel, demandez-lui d'utiliser un processus automatisé pour mettre à jour la capacité provisionnée afin de répondre aux nouveaux besoins, puis de réduire la capacité ultérieurement s'il ne peut pas attendre 5 à 10 minutes pour que le service s'adapte automatiquement à ses besoins.
    5. Le projet Amazon Personalize Monitor fournit un tableau de bord CloudWatch, des métriques personnalisées, des alarmes d'utilisation et des fonctions d'optimisation des coûts pour les campagnes Personalize : https://github.com/aws-samples/amazon-personalize-monitor.
12. Comment puis-je savoir si un modèle Personalize fournit des recommandations de haute qualité ?
    1. Personalize fournit des métriques hors ligne pour chaque version de la solution, qui mesurent la précision des prédictions du modèle par rapport aux données retenues dans le jeu de données d'interactions. Utilisez ces métriques pour donner une idée de la qualité d'une version de la solution par rapport aux autres versions.
    2. Les tests en ligne (c'est-à-dire les tests A/B) seront toujours la meilleure mesure de l'impact d'un modèle sur les paramètres commerciaux.
    3. Lorsque vous comparez les modèles Personalize à un système de recommandation existant, toutes les données historiques sont initialement biaisées en faveur de l'approche existante. Souvent, les mesures hors ligne ne reflètent pas ce qu'un utilisateur aurait PU faire s'il avait été exposé à quelque chose d'autre (comment le pourrait-il, les données ne le reflètent pas). Il convient donc de noter cet effet, ainsi que l'exploration basée sur le bandit que Personalize peut faire pour apprendre organiquement à mieux connaître vos utilisateurs. Par conséquent, il est recommandé d'effectuer un test en ligne pendant quelques semaines **avant** de commencer réellement un test pour mesurer les résultats.
    4. Pour en savoir plus, reportez-vous à ce billet de blog : https://aws.amazon.com/blogs/machine-learning/using-a-b-testing-to-measure-the-efficacy-of-recommendations-generated-by-amazon-personalize/
13. Comment puis-je optimiser les coûts ?
    1. N'UTILISEZ PAS AUTOML !
    2. NE COMMENCEZ PAS AVEC LE HPO – créez d'abord quelque chose de fonctionnel, optimisez ensuite.
    3. Refaites l'entraînement en fonction des besoins de l'entreprise uniquement. Pour en savoir plus, reportez-vous à la FAQ.
    4. Faites confiance à la mise à l'échelle automatique en fixant le TPS minimum provisionné à un niveau bas, sauf si vos objectifs de débit et de latence en pâtissent.
    5. Pensez à utiliser les recommandations par lots lorsque le cas d'utilisation s'aligne sur un processus par lots en aval, tel que le marketing par e-mail. Les recommandations par lots s'exécutant par rapport à une version de la solution, elles ne nécessitent pas de campagne.
    6. Le projet Amazon Personalize Monitor offre certaines fonctions d'optimisation des coûts pour optimiser le provisionnement des campagnes ainsi que l'alerte et la suppression des campagnes inactives/abandonnées : https://github.com/aws-samples/amazon-personalize-monitor.
14. Quelles sont les meilleures façons d'utiliser la mise en cache avec Amazon Personalize ? Comment dois-je intégrer Personalize à mes applications existantes ?
    1. Découvrez la solution des [API de personnalisation](_https://github.com/aws-samples/personalization-apis_) : Cadre d'API à faible latence en temps réel qui se situe entre vos applications et les systèmes de recommandation tels qu'Amazon Personalize. Fournit les bonnes pratiques de mise en œuvre du cache des réponses, des configurations de passerelles d'API, des tests A/B avec [Amazon CloudWatch Evidently](_https://docs.aws.amazon.com/cloudwatchevidently/latest/APIReference/Welcome.html_), des métadonnées d'articles en temps d'inférence, des recommandations contextuelles automatiques, etc.
15. Quelle est la meilleure façon de comparer Personalize à une expérience utilisateur existante ou à un autre système de recommandation ?
    1. Le test A/B est la technique la plus courante pour évaluer l'efficacité de Personalize par rapport aux mesures en ligne.  [Amazon CloudWatch Evidently]([_https://docs.aws.amazon.com/cloudwatchevidently/latest/APIReference/Welcome.html_](https://docs.aws.amazon.com/cloudwatchevidently/latest/APIReference/Welcome.html)) est un outil de test A/B d'AWS qui peut être utilisé avec Personalize. Le projet d'[API de personnalisation]([_https://github.com/aws-samples/personalization-apis_](https://github.com/aws-samples/personalization-apis)) fournit une solution déployable et une architecture de référence.
16. Comment les enregistrements incrémentiels influencent-ils les recommandations pour l'utilisateur actuel ?
    1. Amazon Personalize vous permet d'importer des [interactions](https://docs.aws.amazon.com/personalize/latest/dg/importing-interactions.html), des [utilisateurs](https://docs.aws.amazon.com/personalize/latest/dg/importing-users.html) et des [articles](https://docs.aws.amazon.com/personalize/latest/dg/importing-items.html) de manière progressive. Ils peuvent affecter les recommandations pour l'utilisateur actuel de différentes manières selon qu'une nouvelle version de la solution a été entraînée ou non et selon le type de trainingMode utilisé :

|Incrément	|Recette	|Pas de recyclage	|Recyclage de trainingMode=UPDATE	|Recyclage de trainingMode=FULL	|Commentaires	|
|---	|---	|---	|---	|---	|---	|
|putEvent avec un nouvel utilisateur	|Personnalisation de l'utilisateur	|La personnalisation commence après un événement, mais sera plus visible après environ deux à cinq événements avec un délai d'une à deux secondes après l'appel PutEvents après l'enregistrement de chaque événement.	|Pas d'effet supplémentaire au-delà des effets décrits dans « Pas de nouvel entraînement ».	|Recommandations personnalisées	|Plus le nombre d'événements diffusés est important, plus les recommandations sont personnalisées. Les impressions seront réduites pour les articles de démarrage à froid lorsque les enregistrements des nouveaux utilisateurs comprennent des données d'impressions.	|
|putEvent avec un nouvel utilisateur	|Classement personnalisé	|La personnalisation commence après un événement, mais sera plus visible après environ deux à cinq événements avec un délai d'une à deux secondes après l'appel PutEvents après l'enregistrement de chaque événement.	|-	|Recommandations personnalisées	|En utilisant le classement personnalisé, il est le plus souvent difficile de voir l'impact direct des enregistrements putEvents, car une liste organisée fournie par le client est reclassée (par rapport à la personnalisation de l'utilisateur où les recommandations sont générées à partir du vocabulaire complet des articles du catalogue sur la base du comportement appris du modèle/des caractéristiques des métadonnées et de l'historique des interactions de l'utilisateur).	|
|putEvent avec un nouvel utilisateur	|SIMS	|-	|-	|Inclus dans le modèle pour générer les recommandations	|SIMS ne fait pas vraiment de personnalisation. Par conséquent, dans le contexte de l'ajout de nouveaux utilisateurs avec PutEvents, les événements d'un nouvel utilisateur ne sont pris en compte dans les recommandations d'articles similaires qu'après un nouvel entraînement.	|
|putUser	|Personnalisation de l'utilisateur	|-	|-	|Recommandations personnalisées	|Les utilisateurs ajoutés avec putUser seront des utilisateurs « tièdes » en fonction de la combinaison de leur historique d'interaction connu et de leur userID après le prochain nouvel entraînement complet.	|
|putUser	|Classement personnalisé	|-	|-	|Recommandations personnalisées	|Les utilisateurs ajoutés avec putUser seront des utilisateurs « tièdes » en fonction de la combinaison de leur historique d'interaction connu et de leur userID après le prochain nouvel entraînement complet.	|
|putUser	|SIMS	|-	|-	|Aucun effet	|SIMS ne fait pas vraiment de personnalisation donc, dans le contexte de nouveaux utilisateurs ajoutés avec PutUser, les événements d'un nouvel utilisateur sont pris en compte dans les recommandations d'articles similaires seulement après le nouvel entraînement.	|
|putItem	|Personnalisation de l'utilisateur	|-	|Apparaissent comme des articles de démarrage à froid éligibles en fonction de l'âge limite d'exploration lorsque l'exploration est activée.	|Recommandations personnalisées	|Pour les articles nouveaux/de démarrage à froid, les recommandations sont personnalisées en fonction de l'historique d'interaction de l'utilisateur et des métadonnées des articles nouveaux/de démarrage à froid. Les articles de démarrage à froid (éligibles en fonction de l'âge limite d'exploration lorsque l'exploration est activée) seront inclus lors de la prochaine mise à jour. Les articles de démarrage à froid seront mis à jour automatiquement sur la base de l'actualisation de l'impression à partir de l'interaction générée pendant l'exploration. Cette pondération n'est pas linéaire et est combinée à des caractéristiques basées sur les métadonnées, mais les articles de démarrage à froid qui sont moins populaires (fournis dans le champ des impressions avec putEvents recevront moins de pondération d'exploration au fil du temps).	|
|putItem	|Classement personnalisé	|-	|-	|Personnalisé seulement après quelques interactions	|-	|
|putItem	|SIMS	|-	|-	|Les nouvelles interactions sont incluses dans le modèle pour générer des recommandations d'articles similaires basées sur la co-occurrence.	|SIMS ne fait pas vraiment de personnalisation. Par conséquent, dans le contexte de l'ajout de nouveaux utilisateurs avec PutEvents, les événements d'un nouvel utilisateur ne sont pris en compte dans les recommandations d'articles similaires qu'après un nouvel entraînement.	|

## Liens vers la préparation technique :

1. Échantillons généraux : https://github.com/aws-samples/amazon-personalize-samples
2. Démarrage : https://github.com/aws-samples/amazon-personalize-samples/tree/master/getting_started
3. POC in a Box 2.0 : https://github.com/aws-samples/amazon-personalize-samples/tree/master/next_steps/workshops/POC_in_a_box
4. Bloc-notes basés sur les cas d'utilisation : https://github.com/aws-samples/amazon-personalize-samples/tree/master/next_steps/core_use_cases
5. Outils de science des données : https://github.com/aws-samples/amazon-personalize-samples/tree/master/next_steps/data_science
6. MLOps pour Personalize : https://github.com/aws-samples/amazon-personalize-samples/tree/master/next_steps/operations/ml_ops
7. Suivi/Alerte/Optimisation des coûts : https://github.com/aws-samples/amazon-personalize-monitor

## Démos/ateliers :

* Médias et divertissement
    * Unicorn Flix
        * Instance en cours d'exécution : [https://unicornflix.amplify-video.com](https://unicornflix.amplify-video.com/)
* Vente au détail
    * Le magasin de démo de vente au détail
        * Source : https://github.com/aws-samples/retail-demo-store
        * Ateliers : https://github.com/aws-samples/retail-demo-store#hands-on-workshops
        * Instance en cours d'exécution : [http://retaildemostore.jory.cloud/](http://retaildemostore.jory.cloud/#/)

## Partenaires technologiques :

Plusieurs partenaires technologiques fournissent des fonctionnalités complémentaires à Personalize qui peuvent accélérer la mise en production des clients avec Personalize ou améliorer le retour sur investissement de la mise en œuvre de la personnalisation avec Personalize.

### Plateformes de données clients – Collecte d'événements/activation des recommandations

**Segment** est une [plateforme de données clients](https://en.wikipedia.org/wiki/Customer_data_platform). Il s'agit d'un partenaire technologique avancé d'AWS qui dispose des compétences [Expérience client numérique](https://aws.amazon.com/advertising-marketing/partner-solutions/) (DCX) et [Vente au détail](https://aws.amazon.com/retail/partner-solutions/).

Les fonctionnalités que Segment offre aux clients de Personalize sont les suivantes :

* Collecte d'événements, une fonctionnalité essentielle de Segment. Les clients utilisent Segment pour collecter les parcours de clics dans leur application web, leurs applications mobiles et d'autres intégrations. Ces événements sont collectés, validés et diffusés vers des destinations en aval configurées par le client. L'une de ces destinations est Amazon Personalize.
* Résolution de l'identité du profil du client/de l'utilisateur – étant donné que Segment voit les événements sur tous les canaux pour les utilisateurs d'un client, il est en mesure de créer un profil client unifié. Ce profil/cette identité est essentiel pour pouvoir fournir une personnalisation omnicanal.
* Activation dans les autres outils de marketing de l'entreprise – Segment permettant aux clients de créer des connexions avec d'autres outils de marketing, l'association de recommandations personnalisées de Personalize à des profils dans Segment permet aux clients et aux partenaires en aval d'exploiter ces recommandations dans leurs outils.

**Ressources**

* Vidéo du directeur technique de Segment : https://www.youtube.com/watch?v=LQSGz8ryvXU 
* Billet de blog : https://segment.com/blog/introducing-amazon-personalize/
* Ateliers AWS/Segment
    * Événements de personnalisation en temps réel : https://github.com/aws-samples/retail-demo-store/blob/master/workshop/1-Personalization/Lab-5-Real-time-events-Segment.ipynb
    * Plateformes de données clients et Personalize : https://github.com/aws-samples/retail-demo-store/blob/master/workshop/6-CustomerDataPlatforms/6.1-Segment.ipynb
    * Segment/Personalize (atelier hérité) : https://github.com/james-jory/segment-personalize-workshop
* Documentation : https://segment.com/docs/connections/destinations/catalog/amazon-personalize/

**mParticle** est une plateforme de données clients. Il s'agit d'un partenaire technologique avancé d'AWS qui dispose des compétences [Expérience client numérique](https://aws.amazon.com/advertising-marketing/partner-solutions/) (DCX) et [Vente au détail](https://aws.amazon.com/retail/partner-solutions/).

Les fonctionnalités que mParticle offre aux clients de Personalize sont les suivantes :

* Collecte d'événements, une fonctionnalité essentielle de mParticle. Les clients utilisent mParticle pour collecter des événements de parcours de clics dans leur application web, leurs applications mobiles et d'autres intégrations. Ces événements sont collectés, validés et diffusés vers des destinations en aval configurées par le client.
* Résolution de l'identité du profil du client/de l'utilisateur – étant donné que mParticle voit les événements sur tous les canaux pour les utilisateurs d'un client, ils sont en mesure de créer un profil unifié du client. Ce profil/cette identité est essentiel pour pouvoir fournir une personnalisation omnicanal.
* Activation dans les autres outils de marketing de l'entreprise – étant donné que mParticle permet aux clients de créer des connexions avec d'autres outils de marketing, l'association de recommandations personnalisées de Personalize aux profils dans mParticle permet aux clients et aux partenaires en aval d'exploiter ces recommandations dans leurs outils.

**Ressources**

* Ateliers AWS/mParticle
    * Événements de personnalisation en temps réel : https://github.com/aws-samples/retail-demo-store/blob/master/workshop/1-Personalization/Lab-6-Real-time-events-mParticle.ipynb
    * Plateformes de données clients et Personalize : https://github.com/aws-samples/retail-demo-store/blob/master/workshop/6-CustomerDataPlatforms/6.2-mParticle.ipynb

### Analytique/Mesure/Expérimentation

**Amplitude** est un partenaire technologique avancé d'AWS et dispose de la compétence [Expérience client numérique](https://aws.amazon.com/advertising-marketing/partner-solutions/) (DCX).
Les fonctionnalités qu'Amplitude offre aux clients de Personalize sont les suivantes :

* Informations sur le produit – Amplitude offre une visibilité sur les types d'événements qui mènent à la conversion grâce à une analyse sophistiquée de l'entonnoir. Les clients disposent ainsi des informations dont ils ont besoin pour optimiser leur taxonomie d'événements et sélectionner les bons événements et champs de métadonnées pour entraîner des modèles dans Personalize.
* Évaluation des tests A/B – Amplitude fournit une mesure en ligne des tests A/B qui peuvent être représentés par des expériences client personnalisées optimisées par Personalize.

**Ressources**

* Atelier : https://github.com/aws-samples/retail-demo-store/blob/master/workshop/3-Experimentation/3.5-Amplitude-Performance-Metrics.ipynb
* Billet de blog : https://aws.amazon.com/blogs/apn/measuring-the-effectiveness-of-personalization-with-amplitude-and-amazon-personalize/

**Optimizely** est une plateforme de test A/B leader sur le marché. Il s'agit d'un partenaire technologique avancé d'AWS qui dispose de la compétence [Expérience client numérique](https://aws.amazon.com/advertising-marketing/partner-solutions/) (DCX).

Les fonctionnalités qu'Optimizely offre aux clients de Personalize sont les suivantes :

* Résultats des tests A/B – l'une des principales offres d'Optimizely est la mesure et le rapport des expériences telles que les techniques de personnalisation.
* Signalisation des fonctionnalités – activer/désactiver les expériences personnalisées

**Ressources**

* Atelier : https://github.com/aws-samples/retail-demo-store/blob/master/workshop/3-Experimentation/3.6-Optimizely-AB-Experiment.ipynb

### Messagerie

**Braze** est une plateforme de messagerie leader sur le marché (e-mail, push, SMS). Il s'agit d'un partenaire technologique avancé d'AWS qui dispose des compétences [Expérience client numérique](https://aws.amazon.com/advertising-marketing/partner-solutions/) (DCX) et [Vente au détail](https://aws.amazon.com/retail/partner-solutions/).

Les fonctionnalités que Braze offre aux clients de Personalize sont les suivantes :

* Envoyer des messages personnalisés aux clients sur les bons canaux de communication grâce à une intégration en temps réel ou par lots.

**Ressources**

* Documentation Braze : https://www.braze.com/docs/partners/data_augmentation/recommendation/amazon_personalize/
* Billet de blog sur AWS ML : https://aws.amazon.com/blogs/machine-learning/optimizing-your-engagement-marketing-with-personalized-recommendations-using-amazon-personalize-and-braze/
* Billet de blog sur AWS Media : https://aws.amazon.com/blogs/media/speed-relevance-insight-how-streaming-services-can-master-effective-content-discovery-and-engagement/
* Atelier : https://github.com/aws-samples/retail-demo-store/blob/master/workshop/4-Messaging/4.2-Braze.ipynb

### Intégrations directes

**Magento 2** : Une extension Magento 2 a été développée par un partenaire Magento et AWS appelé Customer Paradigm. L'extension n'a PAS été développée par Adobe Magento.

Elle peut être facilement installée dans n'importe quelle vitrine Magento 2, qu'elle fonctionne sur site, chez un autre fournisseur de services cloud ou sur AWS. Amazon Personalize est toujours accessible dans le compte AWS du client.

**Ressources**

* Site web du partenaire : https://www.customerparadigm.com/amazon-personalize-magento/
* Marché Magento : https://marketplace.magento.com/customerparadigm-amazon-personalize-extension.html


**Shopify :** [Obviyo](https://www.obviyo.com/) (anciennement HiConversion) a créé une intégration gérée avec Personalize pour les vitrines Shopify. En d'autres termes, Obviyo gère Personalize dans son environnement AWS et les commerçants de Shopify paient Obviyo pour les capacités de personnalisation fournies par Personalize.

**Ressources**

* Site web du partenaire : https://www.obviyo.com/

**WooCommerce (BETA):** [WP-Engine](https://wpengine.com/) a créé une intégration de Personalize dans le plug-in AWS pour WordPress qui vous permet d'ajouter des recommandations de produits de Personalize à un site WooCommerce en quelques clics seulement.

**Ressources**

* Page de ressources WP-Engine : https://wpengine.com/resources/webinar-amazon-com-personalization-for-your-woocommerce-store/
