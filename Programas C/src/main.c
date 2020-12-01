// Acá viene el TP de Tesis. La idea es empezar a armar la red que voy a evaluar

#include<stdio.h>
#include<stdlib.h>
#include<math.h>
#include<time.h>
#include"general.h"
#include"inicializar.h"
#include"avanzar.h"


int main(int argc, char *argv[]){
	// Empecemos con la base. Defino variables de tiempo para medir cuanto tardo y cosas básicas
	time_t prin,fin;
	time(&prin);
	srand(time(NULL));
	int tardanza; // N2 es el largo de mi red + 2. Mi red es de N2*N2. La idea es tener filas y columnas extra que cumplan CCP.
	struct Parametros datos;
	struct Red red;
	// Acá Defino los parámetros, asigno memoria a mis vectores y los inicializo.
		datos.N = 3; // Cantidad de agentes en el modelo
		datos.T = 3;  //strtol(argv[1],NULL,10); Antes de hacer esto, arranquemos con número fijo   // Cantidad de temas sobre los que opinar
		datos.Beta = 2; // Exponente que regula homofilia. Arranquemos con homofilia intermedia.
		datos.Pint = 0.5; // Probabilidad de que se forme un enlace entre dos agentes aleatorios.
		datos.K = 1; // Influencia social. Arranquemos con un valor intermedio.
		datos.Temporal = 0.1; // Paso temporal de iteración del sistema
		datos.alfa = 2; // Controversialidad de los tópicos. Arranquemos con controversialidad intermedia.
		datos.Mopi = 3; // Este es el valor de máxima opinión inicial del sistema
		red.Ang = (double*) malloc(datos.T*datos.T*sizeof(double)); // Matriz simétrica de superposición entre tópicos.
		red.Ady = (int*) malloc(datos.N*datos.N*sizeof(int)); // Matriz de adyacencia de la red. Determina quienes están conectados con quienes
		red.Opi = (double*) malloc(datos.T*datos.N*sizeof(double)); // Lista de vectores de opinión de la red, Tengo T elementos para cada agente.
		// Inicializo mis tres vectores.
		for(int i=0; i<datos.N*datos.N; i++) red.Ady[i] = 0;
		for(int i=0; i<datos.N*datos.T; i++) red.Opi[i] = 0;
		for(int i=0; i<datos.T*datos.T; i++) red.Ang[i] = 0;
	GenerarOpi(red,datos); // Esto me inicializa mis vectores de opinión, asignándole a cada agente una opinión en cada tópico
	GenerarAdy(red,datos); // Esto me inicializa mi matriz de adyacencia, creando las conexiones de mi red
	GenerarAng(red,datos); // Esto me inicializa mi matriz de superposición, definiendo el solapamiento entre tópicos.
	Visualizar(red,datos,0); // Con esto observo los vectores de opinión
	Visualizar(red,datos,1); // Con esto observo la matriz de Superposición
	Visualizar(red,datos,2); // Con esto observo la matriz de Adyacencia
	double prueba=0;
	prueba = Din2(red,datos,1,0);
	printf("Lo que obtuve para el agente 0 en el topico 1 es %lf \n",prueba);
	// char filename[255];
	// sprintf(filename,"Etiqueta_Total_Red_N=%d_F=%d_Q=%d.txt",datos.N2-2,datos.F,datos.Q);
	// FILE *fp=fopen(filename,"w");
	// for(int j=0; j<datos.N2-2; j++){
		// for(int l=0; l<datos.N2-2; l++){
			// posi = (j+1)*datos.N2*datos.F+datos.F+l*datos.F;
			// S = Etiquetar(datos,posi);
			// fprintf(fp,"\t%lf",S);
		// }
	// }
	// fprintf(fp,"\n");
	// for(int i = 0; i<datos.N2*datos.N2*20; i++){
		// for(int k = 0; k<datos.N2*datos.F; k++) Paso(datos,p1,p2);
		// for(int j=0; j<datos.N2-2; j++){
			// for(int l=0; l<datos.N2-2; l++){
				// posi = (j+1)*datos.N2*datos.F+datos.F+l*datos.F;
				// S = Etiquetar(datos,posi);
				// fprintf(fp,"\t%lf",S);
			// }
		// }
		// fprintf(fp,"\n");
	// }
	// fclose(fp);
	free(red.Ang);
	free(red.Ady);
	free(red.Opi);
	time(&fin);
	tardanza = fin-prin;
	printf("Tarde %d segundos \n",tardanza);
	return 0;
 }

