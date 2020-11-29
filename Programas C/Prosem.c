//Este es el archivo para testeos

#include<stdio.h>
#include<stdlib.h>
#include<math.h>
#include<time.h>

// El struct Red tiene los datos que definen mi red, y la info de la red
struct Red{
	int N2; // Largo de la red +2. Ese 2 extra es para tener dos filas y dos columnas que cumplan CCP. 
	int F; // Cantidad de temas sobre los que opinar
	int Q; // Cantidad de opiniones
	int Tpers; // Cantidad total de personas en la red
	int *red; // Array unidimensional que simula la red, con F casilleros para cada individuo
};

// Acá voy a declarar las funciones.------------------------------------

double Random();



/*####################################################################################
####################################################################################
####################################################################################
####################################################################################
*/


//---------------------------------------------------------------------------------------------------

// Vamos a intentar ver como se leen archivos y data desde estos
// Creo que lo más útil va a ser usar el fscanf porque mis datos están separados por tabulaciones
// Acá está la forma de leer el archivo. Sólo necesitaría poder saber que tan largo es antes de
// subirlo, pero creo que eso sería mucho pedir.

int main(){
	time_t prin,fin;
	time(&prin);
	int tardanza;
	struct Red datos;
	datos.N2 = 50; // En el archivo no mencione el N2, pero es 50.
	datos.F = 4;
	datos.Q = 5;
	double *tira;
	tira = (double*) malloc(datos.N2*datos.N2*datos.F*400*sizeof(double));
	char buff[255];
	FILE *fp=fopen("Datos_Correlacion_F=4_Q=5.txt","r");
	for(int i = 0; i<datos.N2*datos.N2*datos.F*400; i++){
		fscanf(fp,"%s",buff);
		*(tira+i) = strtod(buff,NULL);
	}
	fclose(fp);
	for(int j = 400; j<1000000; j = j*4){
		Correlacion(tira,j);
	}
	free(tira);
	time(&fin);
	tardanza = (int) (fin-prin);
	printf("Tarde %d segundos en terminar\n",tardanza);
	return 0;
}

/*####################################################################################
####################################################################################
####################################################################################
####################################################################################
*/

// De acá en adelante van las funciones a declarar

// Esta función me genera un número random
double Random(){
	return ((double) rand()/(double) RAND_MAX);
}


