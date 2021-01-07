//Este es el archivo para testeos

#include<stdio.h>
#include<stdlib.h>
#include<math.h>
#include<time.h>


int main(){
	// Defino mis variables temporales para medir el tiempo que tarda el programa. También genero una nueva semilla
	time_t tt_prin,tt_fin;
	time(&tt_prin);
	srand(time(NULL));
	int i_tardanza;
	
	// Voy a abrir un archivo y guardar algo en él
	char s_Nombre1[255];
	sprintf(s_Nombre1,"Primer Archivo");
	FILE *pf_archivo1=fopen(s_Nombre1,"w");
	fprintf(pf_archivo1,"Estoy escribiendo en el primer archivo\n");
	
	// Ahora abro un segundo archivo en el mismo código
	char s_Nombre2[255];
	sprintf(s_Nombre2,"Segundo Archivo");
	FILE *pf_archivo2=fopen(s_Nombre2,"w");
	fprintf(pf_archivo2,"Estoy escribiendo en el segundo archivo\n");
	
	for(register int i_i=0; i_i<10; i_i++){
		fprintf(pf_archivo1,"%d\n",i_i);
		fprintf(pf_archivo2,"%d\n",i_i);
	}
	
	
	// Ejecuto los comandos finales para medir el tiempo y liberar memoria
	fclose(pf_archivo1);
	fclose(pf_archivo2);
	time(&tt_fin);
	i_tardanza = tt_fin-tt_prin;
	printf("Tarde %d segundos en terminar\n",i_tardanza);
	return 0;
}

