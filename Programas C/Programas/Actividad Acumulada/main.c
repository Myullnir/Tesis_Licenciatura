// Acá viene el TP de Tesis. La idea es empezar a armar la red que voy a evaluar

#include<stdio.h>
#include<stdlib.h>
#include<math.h>
#include<time.h>
#include<string.h>
#include"general.h"
#include"TTanh.h"
#include"inicializar.h"
#include"avanzar.h"



int main(int argc, char *argv[]){
	// Empecemos con la base. Defino variables de tiempo para medir cuanto tardo y cosas básicas
	time_t tt_prin,tt_fin,semilla;
	time(&tt_prin);
	semilla = time(NULL);
	srand(semilla); // Voy a definir la semilla a partir de time(NULL);
	float f_tardanza; // Este es el float que le paso al printf para saber cuanto tardé
	
	// Creo mis punteros a structs y los malloqueo.
		ps_Param ps_datos; // No te vayas a confundir, que ps_Param es el tipo de dato definido por usuario como un puntero al struct Parametros. En cambio, ps_datos es un puntero
		ps_datos = malloc(sizeof(s_Param));
		
		ps_Red ps_red; // No te vayas a confundir, que ps_Red es el tipo de dato definido por usuario como un puntero al struct Red. En cambio, ps_red es un puntero
		ps_red = malloc(sizeof(s_Red)); 
		
		// Parámetros de mi modelo. Esto va desde número de agentes hasta el paso temporal de integración.
		ps_datos->i_N = 1000; // Cantidad de agentes en el modelo
		ps_datos->i_T = 0;  //strtol(argv[1],NULL,10); Antes de hacer esto, arranquemos con número fijo   // Cantidad de temas sobre los que opinar
		ps_datos->i_m = 5; // Cantidad de conexiones que hace el agente al activarse
		ps_datos->f_K = 0; // Influencia social
		ps_datos->f_dt = 0.01; // Paso temporal de iteración del sistema
		ps_datos->f_alfa = 0; // Controversialidad de los tópicos. Arranquemos con controversialidad intermedia. Voy a estar dividiendo esto acá para poder pasar enteros desde el instanciar.
		ps_datos->d_NormDif = 0; // Este es el valor de Normalización de la variación del sistema, que me da la variación promedio de las opiniones.
		ps_datos->d_epsilon = 0.001; // Mínimo valor de actividad de los agentes
		ps_datos->d_gamma = 2.8; // Esta es la potencia que define la distribución de actividad
		ps_datos->d_beta = 0; // Esta es la potencia que determina el grado de homofilia.
		// ps_datos->d_CritCorte = 0.001; // Este valor es el criterio de corte. Con este criterio, toda variación más allá de la quinta cifra decimal es despreciable.
		// ps_datos->i_Itextra = 50; // Este valor es la cantidad de iteraciones extra que el sistema tiene que hacer para cersiorarse que el estado alcanzado efectivamente es estable
		ps_datos->f_Cosangulo = 0; // Este es el coseno de Delta que define la relación entre tópicos.
		
		// Estos son unas variables que si bien podrían ir en el puntero red, son un poco ambiguas y no vale la pena pasarlas a un struct.
		int i_rearmar = 500;
		
		// Matrices de mi sistema. Estas son la de Adyacencia, la de Superposición de Tópicos y la de vectores de opinión de los agentes.
		// También hay una matriz de paso previo del sistema y un vector para guardar la diferencia entre el paso previo y el actual.
		// Agregué una matriz que guarda los valores de actividades, otra que guarda los agentes que se activan y una que guarda el valor medio
		ps_red->pi_Ady = (int*) malloc((2+ps_datos->i_N*ps_datos->i_N)*sizeof(int)); // Matriz de adyacencia de la red. Determina quienes están conectados con quienes
		ps_red->pd_Act = (double*) malloc((2+ps_datos->i_N)*sizeof(double)); // Vector que guarda los valores de actividad de todos los agentes
		
		
		// Este archivo es el que guarda los datos de la matriz de Adyacencia.
		char s_archivo1[355];
		sprintf(s_archivo1,"../Programas Python/DilAct/ActividadAcumulada/Construccion_Red_N=%d",ps_datos->i_N);
		FILE *pa_archivo1=fopen(s_archivo1,"w"); // Con esto abro mi archivo y dirijo el puntero a él.
		
		// Inicializo mis ocho "matrices".
		// Matriz de Adyacencia. Es de tamaño N*N
		for(register int i_i=0; i_i<ps_datos->i_N*ps_datos->i_N+2; i_i++) ps_red->pi_Ady[i_i] = 0;
		ps_red->pi_Ady[0] = ps_datos->i_N; // Pongo el número de filas en la primer coordenada
		ps_red->pi_Ady[1] = ps_datos->i_N; // Pongo el número de columnas en la segunda coordenada
				
		// Matriz de Actividad de los agentes. Es de tamaño 1*N
		for(register int i_i=0; i_i<ps_datos->i_N+2; i_i++) ps_red->pd_Act[i_i] = 0;
		ps_red->pd_Act[0] = 1;
		ps_red->pd_Act[1] = ps_datos->i_N;
				

	// Acá tengo que poner la inicialización de los valores de Actividad
	// Aprovecho también para guardarme los valores de actividad de mis agentes en orden
	// por número de agente.

	Actividad(ps_red->pd_Act,ps_datos->d_epsilon,-ps_datos->d_gamma);
	fprintf(pa_archivo1, "\tActividades agentes\n");
	Escribir_d(ps_red->pd_Act,pa_archivo1);
	fprintf(pa_archivo1, "\tMatriz Adyacencia\n");

	// Voy a separar esto en dos for por una cuestión de facilidad de lectura. Quiero correr de manera de que la red de actividad se rearme en cada paso.
	for(register int i_ciclos=0; i_ciclos<i_rearmar; i_ciclos++){
		Adyacencia_Actividad(ps_red, ps_datos);
		Escribir_i(ps_red->pi_Ady,pa_archivo1);
	}
	
	
	// Guardo las opiniones finales, la semilla y las opiniones de los testigos en el primer archivo
	fprintf(pa_archivo1, "\tSemilla\n");
	fprintf(pa_archivo1,"\t%ld\n",semilla);
	
	
	// Libero los espacios dedicados a mis vectores y cierro mis archivos
	free(ps_red->pi_Ady);
	free(ps_red->pd_Act);
	free(ps_red);
	free(ps_datos);
	fclose(pa_archivo1);
	
	// Finalmente imprimo el tiempo que tarde en ejecutar todo el programa
	time(&tt_fin);
	f_tardanza = tt_fin-tt_prin;
	printf("Tarde %.1f segundos \n",f_tardanza);
	
	return 0;
 }

