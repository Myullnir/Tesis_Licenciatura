// Acá viene el TP de Tesis. La idea es empezar a armar la red que voy a evaluar

#include<stdio.h>
#include<stdlib.h>
#include<math.h>
#include<time.h>
#include"general.h"
#include"inicializar.h"



int main(int argc, char *argv[]){
	// Empecemos con la base. Defino variables de tiempo para medir cuanto tardo y cosas básicas
	time_t tt_prin,tt_fin;
	time(&tt_prin);
	srand(time(NULL));
	float f_tardanza; // Este es el float que le paso al printf para saber cuanto tardé
	
	// Acá Defino los parámetros, asigno memoria a mis vectores y los inicializo.
		struct Parametros datos;
		struct Red red;
		
		// Parámetros de mi modelo. Esto va desde número de agentes hasta el paso temporal de integración.
		datos.i_N = 5; // Cantidad de agentes en el modelo
		datos.i_T = 4;  //strtol(argv[1],NULL,10); Antes de hacer esto, arranquemos con número fijo   // Cantidad de temas sobre los que opinar
		datos.f_Beta = 0.5; // Exponente que regula homofilia. Arranquemos con homofilia intermedia.
		datos.f_Pint = 0.5; // Probabilidad de que se forme un enlace entre dos agentes aleatorios.
		datos.f_K = 1; // Influencia social. Arranquemos con un valor intermedio.
		datos.f_dt = 0.001; // Paso temporal de iteración del sistema
		datos.f_alfa = 0.5; // Controversialidad de los tópicos. Arranquemos con controversialidad intermedia.
		datos.i_Mopi = 3; // Este es el valor de máxima opinión inicial del sistema
		
		// Matrices de mi sistema. Estas son la de Adyacencia, la de Superposición de Tópicos y la de vectores de opinión de los agentes
		red.d_Ang = (double*) malloc((2+datos.i_T*datos.i_T)*sizeof(double)); // Matriz simétrica de superposición entre tópicos.
		red.i_Ady = (int*) malloc((2+datos.i_N*datos.i_N)*sizeof(int)); // Matriz de adyacencia de la red. Determina quienes están conectados con quienes
		red.d_Opi = (double*) malloc((2+datos.i_T*datos.i_N)*sizeof(double)); // Lista de vectores de opinión de la red, Tengo T elementos para cada agente.
		
		// Inicializo mis tres vectores.
		// Matriz de Adyacencia. Es de tamaño N*N
		for(int i_i=0; i_i<datos.i_N*datos.i_N+2; i_i++) red.i_Ady[i_i] = 0;
		red.i_Ady[0] = datos.i_N; // Pongo el número de filas en la primer coordenada
		red.i_Ady[1] = datos.i_N; // Pongo el número de columnas en la segunda coordenada
		
		// Matriz de vectores de opinión. Es de tamaño N*T
		for(int i_i=0; i_i<datos.i_N*datos.i_T+2; i_i++) red.d_Opi[i_i] = 0;
		red.d_Opi[0] = datos.i_N; // Pongo el número de filas en la primer coordenada
		red.d_Opi[1] = datos.i_T; // Pongo el número de columnas en la segunda coordenada
		
		//Matriz de Superposición de Tópicos. Es de tamaño T*T
		for(int i_i=0; i_i<datos.i_T*datos.i_T+2; i_i++) red.d_Ang[i_i] = 0;
		red.d_Ang[0] = datos.i_T; // Pongo el número de filas en la primer coordenada
		red.d_Ang[1] = datos.i_T; // Pongo el número de Columnas en la segunda coordenada
		
	
	// Genero las redes de mi sistema
	GenerarOpi(red,datos); // Esto me inicializa mis vectores de opinión, asignándole a cada agente una opinión en cada tópico
	GenerarAdy(red,datos); // Esto me inicializa mi matriz de adyacencia, creando las conexiones de mi red
	GenerarAng(red); // Esto me inicializa mi matriz de superposición, definiendo el solapamiento entre tópicos.
	
	// Visualizo las redes para comprobar que todo funcione correctamente
	Visualizar(red,0); // Con esto observo los vectores de opinión
	Visualizar(red,1); // Con esto observo la matriz de Superposición
	Visualizar(red,2); // Con esto observo la matriz de Adyacencia
	
	// double prueba=0;
	// prueba = Din2(red,datos,1,0);
	// printf("Lo que obtuve para el agente 0 en el topico 1 es %lf \n",prueba);
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
	// free(red.Ang);
	// free(red.Ady);
	// free(red.Opi);
	time(&tt_fin);
	f_tardanza = tt_fin-tt_prin;
	printf("Tarde %.3f segundos \n",f_tardanza);
	return 0;
 }

