# Exemples de Lambda

Ce dossier commence par un exemple simple de l'intégration de `put_events` dans vos campagnes de personnalisation en utilisant les fonctions Lambda qui traitent les nouvelles données de S3.

Pour commencer, vous devez d'abord terminer la collection de bloc-notes `getting_started`, dont le deuxième manuel qui crée votre dispositif de suivi d'événement initial.


## Envoyer des événements vers S3

À l'intérieur de ce dossier, vous trouverez un manuel `Sending_Events_to_S3.ipynb` qui contient le code passe-partout pour transmettre toute une série de messages à votre compartiment S3.

Il s'agit de la clé pour utiliser votre fonction Lambda, qui à son tour envoie les messages à Amazon Personalize.

## Fonction Lambda

Maintenant que votre manuel peut écrire vos fichiers vers votre compartiment S3 de manière fiable, la prochaine étape consiste à créer une fonction Lambda à invoquer sur le déclenchement d'un événement S3. Le code pour la fonction Lambda est fourni dans le manuel `event_processor.py`


Commencez par accéder à la console Lambda, puis cliquez sur `Create Function`. Donnez-lui le nom que vous voulez et sélection Python 3.6 pour l'exécution.

Vous aurez besoin d'un nouveau rôle IAM pour cette fonction Lambda, commencez donc par lui attribuer un rôle IAM par défaut. Ce rôle sera mis à jour ultérieurement afin de fonctionner avec Amazon Personalize et Amazon S3. Étape suivante `Create function`


Cliquez maintenant sur `+ Add trigger`, recherchez S3, sélectionnez votre compartiment, sélectionnez `All object create events` à des fins de démonstration, puis ajoutez le suffixe `.json`. Pour finir, cliquez sur cette page `Add`

Cliquez ensuite sur l'icône de votre fonction Lambda, lorsque l'éditeur s'affiche en-dessous, copiez le contenu de `event_processor.py` dans l'éditeur et sauvegardez-le. Remplacez tout le contenu existant.

Faites défiler la page vers le bas, pour voir ce qui s'affiche sous l'éditeur. Puis, pour `Environment Variables`, saisissez `trackingId` en tant que clé, et fournissez le numéro de suivi de votre deuxième manuel en tant que valeur.

Vous avez presque terminé. La dernière partie de la configuration consiste à gérer IAM. Faites défiler la page vers le bas, jusqu'à ce que vous voyiez `Execution role`, au bas de la page vous verrez un lien `View the ....`, faites un clic droit dessus et ouvrez-le dans un nouvel onglet.

Cliquez sur `Attach policies`, ajoutez à la fois `AmazonS3FullAccess` et `AmazonPersonalizeFullAccess`, puis cliquez sur `Attach policy`. Ces configurations ne sont pas idéales pour la sécurité mais permettent d'illustrer ce propos. Pour une charge de travail de production, créez des politiques personnalisées explicitement adaptées aux ressources avec lesquelles vous travaillez.

Une fois l'association terminée, fermez l'onglet et revenez sur la page de la console Lambda que vous avez quittée. Cliquez sur `Save` dans le coin supérieur droit de l'écran.

Revenez en haut de la page, sélectionnez `Monitoring`, puis revenez sur votre manuel qui simule les événements et exécutez à nouveau cette cellule pour écrire de nouveaux fichiers et exécuter la fonction Lambda.

Au bout de quelques secondes, vous pouvez actualiser la page pour constater que les invocations sont réussies.
