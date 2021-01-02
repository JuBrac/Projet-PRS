//Attention : ./client_udp $@IP (127.0.0.1) $portConnexionUdp

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <sys/socket.h>
#include <netinet/in.h>

#define RCVSIZE 1024

int main(int argc, char *argv[]) {

    struct sockaddr_in adresse,adresse3;
    int port = atoi(argv[2]);
    char nomFichier[] = "testFragment.txt";
    int valid = 1;
    socklen_t alen = sizeof(adresse);
    socklen_t alen3 = sizeof(adresse3);
    char msg[RCVSIZE];
    char blanmsg[RCVSIZE];
    char SYN[] = "SYN";
    char SYNACK[] = "SYN-ACK";
    char ACK[] = "ACK";
    char delim[] = ":";

    char fichierRecu[100240];
    FILE *dataRecu;

    //create socket
    int server_desc = socket(AF_INET, SOCK_DGRAM, 0);

    // handle error
    if (server_desc < 0) {
        perror("cannot create socket\n");
        return -1;
    }

    setsockopt(server_desc, SOL_SOCKET, SO_REUSEADDR, &valid, sizeof(int));

    adresse.sin_family = AF_INET;
    adresse.sin_port = htons(port);
    adresse.sin_addr.s_addr = inet_addr(argv[1]);

    printf("Sending SYN...\n");

    int syn = sendto(server_desc,SYN,RCVSIZE,
                        0, (const struct sockaddr *) &adresse,
                        sizeof(adresse));
    printf("%d\n",syn);

    recvfrom(server_desc, blanmsg, RCVSIZE,
                    0, (struct sockaddr *) &adresse,
                    &alen);
    printf("%s\n", blanmsg);
    char *port3 = strtok(blanmsg,delim);
    //printf("ptr:%s",ptr);
    port3 = strtok(NULL,delim);
    //printf("port3:%d\n",atoi(port3));



    int server_desc3 = socket(AF_INET, SOCK_DGRAM, 0);//socket udp
    setsockopt(server_desc3, SOL_SOCKET, SO_REUSEADDR, &valid, sizeof(int));

    adresse3.sin_family = AF_INET;
    adresse3.sin_port = htons(atoi(port3));
    adresse3.sin_addr.s_addr = htonl(INADDR_ANY);

    if (strcmp(blanmsg,SYNACK) == 0){
                    int ack = sendto(server_desc,ACK,strlen(ACK),
                        0, (const struct sockaddr *) &adresse,
                        sizeof(adresse));
    }else
    {
        return -1;
    }

    printf("Entrez le nom du fichier : \n");

    //fgets(msg, RCVSIZE, stdin);
    //char nomFichier[sizeof(msg)];
    strcpy(msg,nomFichier);
    int sss = sendto(server_desc3,msg, strlen(msg),
                     0, (const struct sockaddr *) &adresse3,
                     sizeof(adresse3));;
    //printf("the value of sent is:%d\n", sss);
    recvfrom(server_desc3, blanmsg, RCVSIZE,
                 0, (struct sockaddr *) &adresse3,
                 &alen3);
    printf("Nombre de segments : %s\n",blanmsg );

    int cont = 1;
    int nbSegment = atoi(blanmsg);
    int nbSegmentRecu=0;

    while (cont==1) {
        // fgets(msg, RCVSIZE, stdin);
        // int sss = sendto(server_desc3,msg, strlen(msg),
        //                  0, (const struct sockaddr *) &adresse3,
        //                  sizeof(adresse3));;
        // printf("the value of sent is:%d\n", sss);
        recvfrom(server_desc3, blanmsg, RCVSIZE,
                     0, (struct sockaddr *) &adresse3,
                     &alen3);
       int ack2=sendto(server_desc3,ACK,strlen(ACK), 0, (const struct sockaddr *) &adresse3, sizeof(adresse3));
       printf("ack%d",ack2);
        //printf("Segment : %s\n",blanmsg );
        memcpy(fichierRecu+(nbSegmentRecu*1023),blanmsg,1023);
        nbSegmentRecu=nbSegmentRecu+1;

        //printf("Segment-----\n\n%s:",blanmsg);

        if(nbSegment==nbSegmentRecu){
          //printf("%s\n",fichierRecu);
          cont=2;
          char cheminFichier[]="/home/osboxes/Documents/PRS/TP3/Seance2/Downloads/";
          strcat(cheminFichier,nomFichier);
          printf("%s\n",cheminFichier);
          dataRecu = fopen(cheminFichier,"w");
          //fputs(fichierRecu,dataRecu);
          fwrite(fichierRecu,1024,nbSegment,dataRecu);
          fclose(dataRecu);
        }
        //printf("%s", blanmsg);
        memset(blanmsg, 0, RCVSIZE);
        if (strcmp(msg, "stop\n") == 0) {
            cont = 0;
        }
    }
    close(server_desc3);
    return 0;
}
