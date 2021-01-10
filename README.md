# Projet-PRS
Serveur TCP-over-UDP avec Python 2.7

Implémentations : 

- calcul du RTT lors de l'aller-retour du premier message.
- fenêtre de transmission glissante avec une taille fixe.
- slow start

Mécanismes à implémenter : 
- gérer plusieurs clients en même temps
- calcul du RTT dynamique (gérer l'évolution de la congestion)
- évaluation de la performance avec un graphe

Performance : 
Cient1 => 1,2 Mo/s
Client2 => 0,8 Mo/s
