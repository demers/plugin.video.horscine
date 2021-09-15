# Plugin Video Kodi Matrix et Leia pour Horscine

Ce module vidéo permet de visionner les vidéos qui se trouvent sur le site
https://horscine.org/

Le module génère d'abord le menu en analysant la structure du site https://horscine.org/
Le menu peut prendre jusqu'à 1 minute avant de s'afficher.  Le menu est
sauvegardé dans le dossier du module.  La sauvegarde du menu est affiché par la
suite.  La sauvegarde du menu est actualisée à chaque semaine.

En général, les sections affichées sont "Films au hasard", "Le film de la semaine", "Les autres
nouveautés" et "Rechercher".  Les 3 premières sections contiennent des films
qu'on retrouve dans les sections équivalentes sur le site même.  La liste des
films dans chacune de ses sections est sauvegardée dans le dossier du module.  La
liste sauvegardée est affichée par la suite.  La sauvegarde de la liste des films est actualisée
à chaque 48 heures.

La section "Rechercher" permet de lancer une recherche par mot-clé sur le site et de
pouvoir ensuite, consulter les résultats de la recherche comme le permet la fonction de
recherche fournie sur le site même.


## Téléchargements Kodi

Voir la section Releases de Github pour télécharger les fichiers d'installation
ZIP pour Kodi Matrix et Kodi Leia.

## Programmation

Le module a été développé à l'aide des scripts et modules suivants:

  * script.module.routing
  * script.module.arrow
  * script.module.beautifulsoup4
  * plugin.video.vimeo
  * plugin.video.youtube

Certaines vidéos vont générer une erreur de lecture en fonction de
l'hébergement.  Comme par exemple, les vidéos sur Peertube ne fonctionne pas
pour l'instant.

Les vidéos sur Youtube vont fonctionner si le module Youtube a bien été
configuré sur votre installation Kodi.
Les vidéos Vimeo et Archive.org vont bien fonctionner.
