# Projet-PRS
Serveur TCP-over-UDP avec Python 2.7

Implémentations : 

- calcul du RTT lors de l'aller-retour du premier message.
- fenêtre de transmission glissante avec une taille fixe.
- slow start
- fast retransmit ( 3 duplicate ACK = retransmission)

Mécanismes à implémenter : 
- calcul du RTT dynamique (gérer l'évolution de la congestion)
- tracer l'évolution de la fenêtre de congestion

Performance : 
Cient1 => 1,8 Mo/s
Client2 => 1,0 Mo/s
Multiple client1 => 1.4 Mo/s

