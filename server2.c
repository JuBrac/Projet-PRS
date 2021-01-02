// Attention : ./server $portConnexionTcp $portConnexionUdp

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/socket.h>
#include <sys/select.h>
#include <sys/time.h>
#include <netinet/in.h>

#define RCVSIZE 1024

int max(int desc1, int desc2);

int main(int argc, char *argv[]) {

    struct sockaddr_in adresse1, adresse2,adresse3, client;
    pid_t childpid;
    int port1 = atoi(argv[1]);
    int port2 = atoi(argv[2]);
    int valid = 1;
    socklen_t alen = sizeof(client);
    char buffer[RCVSIZE];
    char SYN[] = "SYN";
    char SYNACK[] = "SYN-ACK8787";
    char ACK[] = "ACK";
    char ACK2[] = "ACKtFragment.txt";
    char port_str[] = "8787";
    int count = 1;
    int port3 = 8787;

    FILE *dataFichier;
    char bufferFichier[100240];
    char bufferSegment[1024];



    //create socket
    int server_desc1 = socket(AF_INET, SOCK_STREAM, 0);//socket tcp
    int server_desc2 = socket(AF_INET, SOCK_DGRAM, 0);//socket udp

    //handle error
    if (server_desc1 < 0 || server_desc2 < 0) {
        perror("Cannot create socket\n");
        return -1;
    }

    setsockopt(server_desc1, SOL_SOCKET, SO_REUSEADDR, &valid, sizeof(int));
    setsockopt(server_desc2, SOL_SOCKET, SO_REUSEADDR, &valid, sizeof(int));

    adresse1.sin_family = AF_INET;
    adresse1.sin_port = htons(port1);
    adresse1.sin_addr.s_addr = htonl(INADDR_ANY);

    adresse2.sin_family = AF_INET;
    adresse2.sin_port = htons(port2);
    adresse2.sin_addr.s_addr = htonl(INADDR_ANY);

    //initialize socket
    if (bind(server_desc1, (struct sockaddr *) &adresse1, sizeof(adresse1)) == -1 ||
        bind(server_desc2, (struct sockaddr *) &adresse2, sizeof(adresse2)) == -1) {
        perror("Bind failed\n");
        close(server_desc1);
        return -1;
    }

    //listen to incoming clients
    if (listen(server_desc1, 0) < 0) {
        printf("Listen1 failed\n");
        return -1;
    }

    printf("Listen done\n");
// //Gestion de la fragmentation du du fichier
//     printf("Début fragmentation fichier:\n");
//     dataFichier = fopen ("testFragment.txt","r");
//     int tailleFichier = fread(bufferFichier,1024,100,dataFichier);
//     //printf(bufferFichier);
//     printf("Taille fichier : %d%",tailleFichier);
//
//     for (int index=0;index<=tailleFichier;index++){
//       memcpy(bufferSegment,bufferFichier+(index*1023),1023);
//       printf("%s\n",bufferSegment);
//       printf("------------------FIN SEGMENT------------\n");
//       int segment = sendto(server_desc3,bufferSegment,RCVSIZE,0, (struct sockaddr *) &client,alen);
//       // for(int j=0;j<1024;j++){
//       //   bufferSegment[j] = bufferFichier[j+(index*1024)];
//       //
//       // }
//     }





    printf("Value of socket TCP is:%d\n", server_desc1);
    printf("Value of socket UDP is:%d\n", server_desc2);

    recvfrom(server_desc2, buffer, sizeof(buffer), 0, (struct sockaddr *) &client, &alen);
    printf("%s\n", buffer);
    if (strcmp(buffer,SYN) != 0){
        return -1;
            }
    // int synack = sendto(server_desc2,SYNACK,RCVSIZE,
    //                      0, (struct sockaddr *) &client,alen);
    //
    // struct timeval rtt1;
    // gettimeofday(&rtt1,NULL);
    //gettimeofday()

    int server_desc3 = socket(AF_INET, SOCK_DGRAM, 0);//socket udp
    setsockopt(server_desc3, SOL_SOCKET, SO_REUSEADDR, &valid, sizeof(int));

    adresse3.sin_family = AF_INET;
    adresse3.sin_port = htons(port3);
    adresse3.sin_addr.s_addr = htonl(INADDR_ANY);

    if (bind(server_desc3, (struct sockaddr *) &adresse3, sizeof(adresse3)) == -1)  {
        perror("Bind failed\n");
        close(server_desc3);
        return -1;
    }
    //sendto(server_desc2,port_str,RCVSIZE,
                         //0, (struct sockaddr *) &client,alen);
     int synack = sendto(server_desc2,SYNACK,RCVSIZE,
                          0, (struct sockaddr *) &client,alen);

     struct timeval rtt1;
     gettimeofday(&rtt1,NULL);
     //gettimeofday()

    recvfrom(server_desc2, buffer, sizeof(buffer), 0, (struct sockaddr *) &client, &alen);

    //gettimeofday()
    struct timeval rtt2;
    gettimeofday(&rtt2,NULL);

    printf("seconds:%ld\n",rtt2.tv_sec-rtt1.tv_sec);
    printf("microseconds:%ld\n",rtt2.tv_usec-rtt1.tv_usec);

    if (strcmp(buffer,ACK) != 0){
        perror("ACK error");
        return -1;
            }


    fd_set readfds;
    FD_ZERO(&readfds);

    while (count) {
        FD_SET(server_desc1, &readfds);
        FD_SET(server_desc3, &readfds);
        int maxfd = max(server_desc1, server_desc3) + 1;
        int res = select(maxfd, &readfds, NULL, NULL, NULL);
        if (res < 0) {
            perror("select error");
        }
        if (FD_ISSET(server_desc1, &readfds)) {
            int client_desc1 = accept(server_desc1, (struct sockaddr *) &client, &alen);
            if ((childpid = fork()) == 0) {
                close(server_desc1);
                printf("Accepted by child process\n");
                int msgSize = read(client_desc1, buffer, RCVSIZE);
                while (msgSize > 0) {
                    write(client_desc1, buffer, msgSize);
                    printf("Message From TCP client: ");
                    printf("%s", buffer);
                    memset(buffer, 0, RCVSIZE);
                    msgSize = read(client_desc1, buffer, RCVSIZE);
                }
                close(client_desc1);
                exit(0);
            }
        } else if (FD_ISSET(server_desc3, &readfds)) {
            printf("UDP, fichier: ");
            recvfrom(server_desc3, buffer, sizeof(buffer), 0, (struct sockaddr *) &client, &alen);
            printf("%s", buffer);
            char *fichierATelecharge = strtok(buffer,"");
            //memset(buffer, 0, RCVSIZE);
            //strcpy(fichierATelecharge,buffer);

            //Gestion de la fragmentation du du fichier
            printf("Début fragmentation fichier:\n");
            printf("%s\n",fichierATelecharge);
            dataFichier = fopen("testFragment.txt","r");
            int tailleFichier = fread(bufferFichier,1024,100,dataFichier);
            //printf(bufferFichier);
            //printf("Taille fichier : %d%",tailleFichier);
            char nombre_segments[100];
            sprintf(nombre_segments,"%i",tailleFichier+1);
            printf("Nombre de segments:%s\n",nombre_segments );
            //strcat(nombre_segments,itoa(tailleFichier));


            sendto(server_desc3,nombre_segments,sizeof(nombre_segments),0, (struct sockaddr *) &client,alen);


                for (int index=0;index<=tailleFichier;index++){
                  memcpy(bufferSegment,bufferFichier+(index*1023),1023);
                  //printf("%s\n",bufferSegment);

                  printf("------------------FIN SEGMENT------------\n");
                  //Début du timer
                  struct timeval current_time1;
                  gettimeofday(&current_time1,NULL);

                  struct timeval current_time2;
                  gettimeofday(&current_time2,NULL);

                  // struct timeval timeout;
                  // timeout.tv_sec =rtt2.tv_sec-rtt1.tv_sec;
                  // timeout.tv_usec = rtt2.tv_usec-rtt1.tv_usec;
                  //timeout.tv_usec = 2;//simulation perte paquet

                  sendto(server_desc3,bufferSegment,sizeof(bufferSegment),0, (struct sockaddr *) &client,alen);


                  struct timeval timeout;
                  //timeout.tv_sec = 2*(rtt2.tv_sec-rtt1.tv_sec);
                  timeout.tv_sec = 2;

                  //timeout.tv_usec = 2*(rtt2.tv_usec-rtt1.tv_usec);
                  timeout.tv_usec =500;//simulation perte paquet

                  FD_ZERO(&readfds);
                  FD_SET(server_desc3, &readfds);
                  int maxfdp = server_desc3 + 1;
                  int try_time = 1;
                  int max_try_time = 100;
                  int ackRecu=0;

                  while(ackRecu==0){
                    switch (select(maxfdp, &readfds, NULL, NULL, &timeout)) {
                        case -1:
                            printf("transmission failed\n");
                            exit(-1);
                        case 0:
                            if (try_time <= max_try_time) {
                                printf("%d try failed\n", try_time);
                                try_time++;
                                break;
                            } else {
                                printf("transmission failed\n");
                                exit(-1);
                            }
                        default:
                            recvfrom(server_desc3, buffer, sizeof(buffer), 0, (struct sockaddr *) &client, &alen);
                            printf("buffer :%s\n",buffer);
                            ackRecu=1;
                    }
                  }

                  // int ackRecu=0;
                  //
                  // while(ackRecu==0){
                  //   sendto(server_desc3,bufferSegment,sizeof(bufferSegment),0, (struct sockaddr *) &client,alen);
                  //   //While(temps<timeout){
                  //   setsockopt(server_desc3, SOL_SOCKET,SO_RCVTIMEO,&timeout,sizeof(timeout));
                  //
                  //   recvfrom(server_desc3, buffer, sizeof(buffer), 0, (struct sockaddr *) &client, &alen);
                  //
                  //   setsockopt(server_desc3, SOL_SOCKET, SO_REUSEADDR, &valid, sizeof(int));
                  //
                  //   printf("%s\n", buffer);
                  //   if (strcmp((buffer),ACK2) == 0){
                  //     printf("Paquet bien arrivé");
                  //     ackRecu=1;
                  //           }
                  //   //memset(buffer, 0, RCVSIZE);
                  // }


                  // while(current_time1.tv_usec-current_time2.tv_usec<(rtt2.tv_usec-rtt1.tv_usec)*2{
                  //   printf("microseconds:%ld\n",current_time2.tv_usec-current_time1.tv_usec);
                  //   gettimeofday(&current_time2,NULL);
                  //
                  //   if()
                  // }

                  //Incrementer temps
                  //if(ACK est recue)
                  //sortir de la boucle
                  //Si (temps>timeout)
                  //sendto(message perdu)
                }

        }
    }
}

int max(int desc1, int desc2) {
    if (desc1 > desc2) return desc1;
    return desc2;
}
