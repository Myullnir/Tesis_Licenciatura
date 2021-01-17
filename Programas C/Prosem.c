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

	// Defino unas variables int y doubles para hacer unas cuentas.
	
	double d_resultado;
	double d_num1 = 0.453;
	int i_num1 = 250, i_num2 = 1000;
	
	char s_archivo1[255];
	sprintf(s_archivo1,"Prueba");
	FILE *pa_archivo1=fopen(s_archivo1,"w"); // Con esto abro mi archivo y dirijo el puntero a él.
	
	d_resultado = d_num1/(i_num1*i_num2);
	
	fprintf(pa_archivo1,"%.12lf\t", d_resultado);
	
	d_resultado = d_num1/ (double) (i_num1*i_num2);
	
	fprintf(pa_archivo1,"%lf\t", d_resultado);
	
	d_resultado = 0.000000001;
	
	fprintf(pa_archivo1,"%lf\t",d_resultado);
	
	// Ejecuto los comandos finales para medir el tiempo y liberar memoria
	time(&tt_fin);
	i_tardanza = tt_fin-tt_prin;
	printf("Tarde %d segundos en terminar\n",i_tardanza);
	return 0;
}

// Estoy queriendo ver si descubro porqué mis datos de error me guardan sólo hasta
// seis decimales, cuando mis variables son doubles.