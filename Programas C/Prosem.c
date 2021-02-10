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
	sprintf(s_archivo,"Prueba_Double");
	FILE *pa_archivo=fopen(s_archivo,"w"); // Con esto abro mi archivo y dirijo el puntero a él. Con el +x lo que hago es que no me reescriba el archivo ya creado
	
	double d_valor = 1;
	
	for(register int i=0; i<100; i++){
		d_valor = d_valor/2;
		fprintf(pa_archivo,"%.32lf\n",d_valor);
	}
	
	
	// Ejecuto los comandos finales para medir el tiempo y liberar memoria
	fclose(pa_archivo);
	time(&tt_fin);
	i_tardanza = tt_fin-tt_prin;
	printf("Tarde %d segundos en terminar",i_tardanza);
	
	
	return 0;
}

