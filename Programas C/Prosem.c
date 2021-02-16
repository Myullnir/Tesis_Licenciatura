//Este es el archivo para testeos

#include<stdio.h>
#include<stdlib.h>
#include<math.h>
#include<time.h>

int main(int argc, char *argv[]){
	// Defino mis variables temporales para medir el tiempo que tarda el programa. También genero una nueva semilla
	time_t tt_prin,tt_fin;
	time(&tt_prin);
	srand(time(NULL));
	int i_tardanza;
	
	// Defino el puntero a mi archivo y lo abro
	char s_archivo[255];
	sprintf(s_archivo,"Tabla_Valores_TANH");
	FILE *pa_archivo=fopen(s_archivo,"w"); // Con esto abro mi archivo y dirijo el puntero a él. Con el +x lo que hago es que no me reescriba el archivo ya creado
	
	// Ahora con esto me armo los datos para la interpolación. Voy a guardar 12 decimales.
	fprintf(pa_archivo,"%lf\t",-1.0);
	for(register int i_i=0; i_i<1000001; i_i++) fprintf(pa_archivo,"%lf\t",tanh(-5+0.00001*i_i));
		
	// Ejecuto los comandos finales para medir el tiempo y liberar memoria
	fclose(pa_archivo);
	time(&tt_fin);
	i_tardanza = tt_fin-tt_prin;
	printf("Tarde %d segundos en terminar",i_tardanza);
		
	return 0;
}

