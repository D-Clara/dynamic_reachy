# Réparation  & MAJ de Reachy


## Bras droit
Après une erreur de manipulation pdt laquelle Reachy a essayé un déplacer son bras en etant bloqué, le bras n’était plus détecté. 
Nous avons essayé de trouver l’erreur en se basant sur les symptômes :
- Le SDK ne se lance pas
- La leds liée au bras gauche de s’allume pas
- Il n’y a plus de tension dans le bras droit
- le bras gauche et la tête ne sont pas impacté

Après avoir comparé ces information du Reachy avec les schémas electrique du robot nous en avons conclu que le problème venait la diode qui fait le lien entre la tension d’alimentation du robot et le la tension d’entrée dans le bras gauche.
Cette diode n’étant pas simplement accessible nous avons ajouté une nouvelle diode a des points accessible de la carte qui correspondent aux même extrémités de la diode.
Cette solution venait bypass le switch on/off des moteurs, utile lors de la manipulation du robot. Nous avons donc décidé d’ajouter un nouvel interrupteur avant la diode pour pouvoir tout de même couper les moteurs du bras droit.


## Bras gauche
Nous avons trouvé plusieurs problèmes sur le bras gauche du Reachy.
Tout d’abord il y avait une erreur de 45° sur une articulation de l’épaule. Une pièce avait été changé a cet endroit l’année précédente nous avons donc conclu que le moteur avait du être mal repositionné. Nous avons donc simplement démonté le bras du robot, replacé le moteur ce qui a réglé ce premier problème.
Après quelques manipulation sur le bras gauche, nous avons remarqué quelques mouvement parasite imprévisible et assez violents. Ce problème venait d’un problème software qui a été réglé en effectuant la mise a jour du code.




## Mains
La partie supposée fixe de main avait un peu de jeu ce qui pouvait influencer sur la répétabilité des lancés. Nous avons donc, en démontant un moteur de la main, resserré les vis au niveau du capteur de force. 



## Mise à jour logiciel
Nous avons mis à jour le code du robot présent sur notre Reachy pour corriger le problème du bras gauche. Pour cela nous avons mis à jour chaque répertoire utile du Reachy :

Dans Reachy/Reachy_ws :
- reachy_description
- reachy_kinematics  
- reachy_sdk_server
- reachy_controllers      
- reachy_focus        
- reachy_msgs

Dans Reachy/dev :
- mobile-base-sdk       
- reachy_pyluos_hal  
- reachy-sdk-api         
- zoom_kurokesu
- reachy-sdk




Dans chacun de ces répertoire nous avons :
- créer une nouvelle branche pour sauvegarder l’état actuel en cas de dysfonctionnement de la mise à jour
- revenir dans la branche initial
- récupérer les modification depuis le git (git pull)
- build les nouvelles sources à partir des nouvelles données dans ROS (uniquement pour les repertoires dans reachy_ws)(colb)
- sourcer les modifications (sb)