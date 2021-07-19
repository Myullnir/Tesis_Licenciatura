//Este es el archivo para testeos

#include<stdio.h>
#include<stdlib.h>
#include<math.h>
#include<time.h>
#include<string.h>


int main(int argc, char *argv[]){
	// Defino mis variables temporales para medir el tiempo que tarda el programa. También genero una nueva semilla
	time_t tt_prin,tt_fin;
	time(&tt_prin);
	srand(time(NULL));
	int i_tardanza;
	
	// Armo un array a punteros y lo examino
	int* ap_Array[3];
	
	for(register int i_i=0; i_i<3; i_i++){
		ap_Array[i_i] = (int*) malloc((2+5)*sizeof(int));
		*ap_Array[i_i] = 1;
		*(ap_Array[i_i]+1) = 4;
		for(register int i_j=0; i_j<4; i_j++) *(ap_Array[i_i]+i_j+2) = i_i*4+i_j;
	}
	
	for(register int i_i=0; i_i<3; i_i++) for(register int i_j=0; i_j<4; i_j++) printf("El número de agente es %d\n",*(ap_Array[i_i]+i_j+2));
	
	// Ejecuto los comandos finales para medir el tiempo y liberar memoria
	for(register int i_i=0; i_i<3; i_i++) free(ap_Array[i_i]);
	time(&tt_fin);
	i_tardanza = tt_fin-tt_prin;
	printf("Tarde %d segundos en terminar",i_tardanza);
		
	return 0;
}

