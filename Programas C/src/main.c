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
	time_t tt_prin,tt_fin;
	time(&tt_prin);
	srand(time(NULL));
	float f_tardanza; // Este es el float que le paso al printf para saber cuanto tardé
	
	// Acá Defino los parámetros, asigno memoria a mis vectores y los inicializo.
		s_Param datos;
		s_Red red;
		
		// Parámetros de mi modelo. Esto va desde número de agentes hasta el paso temporal de integración.
		datos.i_N = 30; // Cantidad de agentes en el modelo
		datos.i_T = 5;  //strtol(argv[1],NULL,10); Antes de hacer esto, arranquemos con número fijo   // Cantidad de temas sobre los que opinar
		datos.f_Beta = 0.5; // Exponente que regula homofilia. Arranquemos con homofilia intermedia.
		datos.f_Pint = 0.6; // Probabilidad de que se forme un enlace entre dos agentes aleatorios.
		datos.f_K = 3; // Influencia social. Arranquemos con un valor intermedio.
		datos.f_dt = 0.001; // Paso temporal de iteración del sistema
		datos.f_alfa = 0.5; // Controversialidad de los tópicos. Arranquemos con controversialidad intermedia.
		datos.i_Mopi = 3; // Este es el valor de máxima opinión inicial del sistema
		datos.f_Tint = 20; // Este es el valor de tiempo total en el que voy a integrar mi sistema
		int i_Pasos = (int) datos.f_Tint/ datos.f_dt; // Esta es la cantidad de pasos en la que voy a iterar mi sistema.
		
		// Matrices de mi sistema. Estas son la de Adyacencia, la de Superposición de Tópicos y la de vectores de opinión de los agentes
		red.pd_Ang = (double*) malloc((2+datos.i_T*datos.i_T)*sizeof(double)); // Matriz simétrica de superposición entre tópicos.
		red.pi_Ady = (int*) malloc((2+datos.i_N*datos.i_N)*sizeof(int)); // Matriz de adyacencia de la red. Determina quienes están conectados con quienes
		red.pd_Opi = (double*) malloc((2+datos.i_T*datos.i_N)*sizeof(double)); // Lista de vectores de opinión de la red, Tengo T elementos para cada agente.
		
		// Inicializo mis tres "matrices".
		// Matriz de Adyacencia. Es de tamaño N*N
		for(register int i_i=0; i_i<datos.i_N*datos.i_N+2; i_i++) red.pi_Ady[i_i] = 0;
		red.pi_Ady[0] = datos.i_N; // Pongo el número de filas en la primer coordenada
		red.pi_Ady[1] = datos.i_N; // Pongo el número de columnas en la segunda coordenada
		
		// Matriz de vectores de opinión. Es de tamaño N*T
		for(register int i_i=0; i_i<datos.i_N*datos.i_T+2; i_i++) red.pd_Opi[i_i] = 0;
		red.pd_Opi[0] = datos.i_N; // Pongo el número de filas en la primer coordenada
		red.pd_Opi[1] = datos.i_T; // Pongo el número de columnas en la segunda coordenada
		
		// Matriz de Superposición de Tópicos. Es de tamaño T*T
		for(register int i_i=0; i_i<datos.i_T*datos.i_T+2; i_i++) red.pd_Ang[i_i] = 0;
		red.pd_Ang[0] = datos.i_T; // Pongo el número de filas en la primer coordenada
		red.pd_Ang[1] = datos.i_T; // Pongo el número de Columnas en la segunda coordenada
		
		// Inicializo el Agente y Tópico a mirar. Esto no significa mucho porque después lo voy a cambiar.
		red.i_agente = 0;
		red.i_topico = 0;
		
		// Puntero a la función que define mi ecuación diferencial
		double (*pf_EcDin)(s_Red var, s_Param par) = &Din2;
		
	
	// Genero las redes de mi sistema
	GenerarOpi(red,datos); // Esto me inicializa mis vectores de opinión, asignándole a cada agente una opinión en cada tópico
	GenerarAdy(red,datos); // Esto me inicializa mi matriz de adyacencia, creando las conexiones de mi red
	GenerarAng(red); // Esto me inicializa mi matriz de superposición, definiendo el solapamiento entre tópicos.
	
	printf("Visualizo la matriz de superposicion de mi sistema \n");
	Visualizar_d(red.pd_Ang);
	
	
	printf("Visualizo el estado inicial de mi sistema \n");
	Visualizar_d(red.pd_Opi);
	
	// Evolucionemos el sistema y probemos que estoy cambiando al sistema	
	for(register int i_i=-1; i_i<i_Pasos; ++i_i){
		RK4(red.pd_Opi, red, datos, pf_EcDin);
	}

	printf("Visualizo el estado final de mi sistema \n");
	Visualizar_d(red.pd_Opi);
	
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
	
	// Libero los espacios dedicados a mis vectores
	free(red.pd_Ang);
	free(red.pi_Ady);
	free(red.pd_Opi);
	
	// Finalmente imprimo el tiempo que tarde en ejecutar todo el programa
	time(&tt_fin);
	f_tardanza = tt_fin-tt_prin;
	printf("Tarde %.3f segundos \n",f_tardanza);
	
	
	return 0;
 }

