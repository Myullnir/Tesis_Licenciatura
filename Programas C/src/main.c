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
		
		ps_Tab ps_tab; // Al igual que en los otros, ps_Tab es el tipo de dato definidio por usuario como el puntero al struct Tabla, en cambio ps_tab es un puntero.
		ps_tab = malloc(sizeof(s_Tabla));
		
		// Parámetros de mi modelo. Esto va desde número de agentes hasta el paso temporal de integración.
		ps_datos->i_N = strtol(argv[1],NULL,10); // Cantidad de agentes en el modelo
		ps_datos->i_T = 2;  //strtol(argv[1],NULL,10); Antes de hacer esto, arranquemos con número fijo   // Cantidad de temas sobre los que opinar
		ps_datos->i_m = 10; // Cantidad de conexiones que hace el agente al activarse
		ps_datos->f_K = 3; // Influencia social
		ps_datos->f_dt = 0.01; // Paso temporal de iteración del sistema
		ps_datos->f_alfa = strtof(argv[2],NULL)/80; // Controversialidad de los tópicos. Arranquemos con controversialidad intermedia. Voy a estar dividiendo esto acá para poder pasar enteros desde el instanciar.
		ps_datos->d_NormDif = sqrt(ps_datos->i_N*ps_datos->i_T); // Este es el valor de Normalización de la variación del sistema, que me da la variación promedio de las opiniones.
		ps_datos->d_epsilon = 0.01; // Mínimo valor de actividad de los agentes
		ps_datos->d_gamma = 2.1; // Esta es la potencia que define la distribución de actividad
		ps_datos->d_beta = 3; // Esta es la potencia que determina el grado de homofilia.
		// ps_datos->d_CritCorte = 0.001; // Este valor es el criterio de corte. Con este criterio, toda variación más allá de la quinta cifra decimal es despreciable.
		// ps_datos->i_Itextra = 50; // Este valor es la cantidad de iteraciones extra que el sistema tiene que hacer para cersiorarse que el estado alcanzado efectivamente es estable
		ps_datos->f_Cosangulo = strtof(argv[3],NULL)/10; // Este es el coseno de Delta que define la relación entre tópicos.
		
		// Estos son unas variables que si bien podrían ir en el puntero red, son un poco ambiguas y no vale la pena pasarlas a un struct.
		int i_renovar_Adyacencia = (int) (1/ps_datos->f_dt); // Este número es la cantidad de veces que itero el sistema antes de renovar la matriz de Adyacencia
		int i_iteracion = strtol(argv[4],NULL,10); // Número de instancia de la simulación.
		int i_testigos = 5;
		int i_momento = 0;
		int i_gradosumado = 0;
		int a_Testigos[5] = {1,10,50,100,300};
		int i_rearmar = 30;
		
		// Matrices de mi sistema. Estas son la de Adyacencia, la de Superposición de Tópicos y la de vectores de opinión de los agentes.
		// También hay una matriz de paso previo del sistema y un vector para guardar la diferencia entre el paso previo y el actual.
		// Agregué una matriz que guarda los valores de actividades, otra que guarda los agentes que se activan y una que guarda el valor medio
		ps_red->pd_Ang = (double*) malloc((2+ps_datos->i_T*ps_datos->i_T)*sizeof(double)); // Matriz simétrica de superposición entre tópicos.
		ps_red->pi_Ady = (int*) malloc((2+ps_datos->i_N*ps_datos->i_N)*sizeof(int)); // Matriz de adyacencia de la red. Determina quienes están conectados con quienes
		ps_red->pd_Opi = (double*) malloc((2+ps_datos->i_T*ps_datos->i_N)*sizeof(double)); // Lista de vectores de opinión de la red, Tengo T elementos para cada agente.
		ps_red->pd_PreOpi = (double*) malloc((2+ps_datos->i_T*ps_datos->i_N)*sizeof(double)); // Paso previo del sistema antes de iterar.
		ps_red->pd_Diferencia = (double*) malloc((2+ps_datos->i_T*ps_datos->i_N)*sizeof(double)); // Paso previo del sistema antes de iterar.
		ps_red->pd_Act = (double*) malloc((2+ps_datos->i_N)*sizeof(double)); // Vector que guarda los valores de actividad de todos los agentes
		ps_red->pi_Activados = (int*) malloc((2+ps_datos->i_N)*sizeof(int)); // Vector que guarda un 1 para los agentes que se activan en la iteración y un cero para los que no.
		ps_red->pd_Km = (double*) malloc((2+i_rearmar)*sizeof(double)); // Vector que guarda los grados medios de las redes armadas.
		
		
		// Voy a abrir tres archivos. Uno para anotar la evolución de opiniones.
		// El segundo es para guardar los datos de las actividades.
		// El tercero es para levantar los datos de la Tabla_Valores_TANH
		// Este archivo es el que guarda las opiniones del sistema
		char s_archivo1[355];
		sprintf(s_archivo1,"../Programas Python/DilAct/Regact/Datos_Opiniones_alfa=%.3f_Cdelta=%.2f_N=%d_Iter=%d",ps_datos->f_alfa,ps_datos->f_Cosangulo,ps_datos->i_N,i_iteracion);
		FILE *pa_archivo1=fopen(s_archivo1,"w"); // Con esto abro mi archivo y dirijo el puntero a él.
		
		// Este archivo es el que guarda las actividades de los agentes, la cantidad de veces que se activan y la actividad promedio.
		char s_archivo2[355];
		sprintf(s_archivo2,"../Programas Python/DilAct/Regact/Datos_Actividades_alfa=%.3f_Cdelta=%.2f_N=%d_Iter=%d",ps_datos->f_alfa,ps_datos->f_Cosangulo,ps_datos->i_N,i_iteracion);
		FILE *pa_archivo2=fopen(s_archivo2,"w"); // Con esto abro mi archivo y dirijo el puntero a él.
		
		// Este archivo levanta los datos de la tabla de valores de tanh calculados previamente.
		char s_Tanh[100];
		sprintf(s_Tanh,"Tabla_Valores_TANH");
		FILE *pa_tabtanh=fopen(s_Tanh,"r");
		
		// Ahora que tengo el stream a la tabla de valores de tanh, malloqueo e inicializo mi vector donde guardo los valores.
		ps_tab->i_largo = Largo_Tabla_TANH(pa_tabtanh);
		
		// Inicializo mi vector donde guardo los valores
		ps_tab->pd_valores = (double*) malloc((ps_tab->i_largo+2)*sizeof(double));
		for(register int i_i=0; i_i<ps_tab->i_largo+2; i_i++) ps_tab->pd_valores[i_i] = 0;
		ps_tab->pd_valores[0] = 1;
		ps_tab->pd_valores[1] = ps_tab->i_largo;
		
		//Guardo los valores y cierro el archivo.
		Lectura_Tabla_TANH(ps_tab->pd_valores, pa_tabtanh);
		fclose(pa_tabtanh);
		
		
		
		// Inicializo mis ocho "matrices".
		// Matriz de Adyacencia. Es de tamaño N*N
		for(register int i_i=0; i_i<ps_datos->i_N*ps_datos->i_N+2; i_i++) ps_red->pi_Ady[i_i] = 0;
		ps_red->pi_Ady[0] = ps_datos->i_N; // Pongo el número de filas en la primer coordenada
		ps_red->pi_Ady[1] = ps_datos->i_N; // Pongo el número de columnas en la segunda coordenada
				
		// Matriz de Superposición de Tópicos. Es de tamaño T*T
		for(register int i_i=0; i_i<ps_datos->i_T*ps_datos->i_T+2; i_i++) ps_red->pd_Ang[i_i] = 0;
		ps_red->pd_Ang[0] = ps_datos->i_T; // Pongo el número de filas en la primer coordenada
		ps_red->pd_Ang[1] = ps_datos->i_T; // Pongo el número de Columnas en la segunda coordenada
				
		// Matriz de vectores de opinión. Es de tamaño N*T
		for(register int i_i=0; i_i<ps_datos->i_N*ps_datos->i_T+2; i_i++) ps_red->pd_Opi[i_i] = 0;
		ps_red->pd_Opi[0] = ps_datos->i_N; // Pongo el número de filas en la primer coordenada
		ps_red->pd_Opi[1] = ps_datos->i_T; // Pongo el número de columnas en la segunda coordenada
		
		// Matriz de vectores de opinión en el paso temporal Previo. Es de tamaño N*T
		for(register int i_i=0; i_i<ps_datos->i_N*ps_datos->i_T+2; i_i++) ps_red->pd_PreOpi[i_i] = 0;
		ps_red->pd_PreOpi[0] = ps_datos->i_N; // Pongo el número de filas en la primer coordenada
		ps_red->pd_PreOpi[1] = ps_datos->i_T; // Pongo el número de columnas en la segunda coordenada
		
		// Matriz de diferencia entre los vectores Opi y PreOpi. Es de tamaño N*T
		for(register int i_i=0; i_i<ps_datos->i_N*ps_datos->i_T+2; i_i++) ps_red->pd_Diferencia[i_i] = 0;
		ps_red->pd_Diferencia[0] = ps_datos->i_N; // Pongo el número de filas en la primer coordenada
		ps_red->pd_Diferencia[1] = ps_datos->i_T; // Pongo el número de columnas en la segunda coordenada
		
		// Matriz de Actividad de los agentes. Es de tamaño 1*N
		for(register int i_i=0; i_i<ps_datos->i_N+2; i_i++) ps_red->pd_Act[i_i] = 0;
		ps_red->pd_Act[0] = 1;
		ps_red->pd_Act[1] = ps_datos->i_N;
		
		// Matriz de agentes activados. Es de tamaño 1*N
		for(register int i_i=0; i_i<ps_datos->i_N+2; i_i++) ps_red->pi_Activados[i_i] = 0;
		ps_red->pi_Activados[0] = 1;
		ps_red->pi_Activados[1] = ps_datos->i_N;
		
		// Matriz de Grados medios de las redes armadas. Es de tamaño 1*i_rearmar
		for(register int i_i=0; i_i<i_rearmar+2; i_i++) ps_red->pd_Km[i_i] = 0;
		ps_red->pd_Km[0] = 1;
		ps_red->pd_Km[1] = i_rearmar;
		
				
		// Inicializo el Agente y Tópico a mirar. Esto no significa mucho porque después lo voy a cambiar.
		ps_red->i_agente = 0;
		ps_red->i_topico = 0;
		ps_red->i_agente2 = 0;
		
		// Puntero a la función que define mi ecuación diferencial
		double (*pf_EcDin)(ps_Red var, ps_Param par, ps_Tab tab) = &Din2;
		
		
		// Voy a armar un array de punteros que se encarguen de guardar los datos de los
		// agentes testigos.
		double* ap_Testigos[i_testigos];
		for(register int i_i=0; i_i<i_testigos; i_i++){
			ap_Testigos[i_i] = (double*) malloc((2+(30*i_renovar_Adyacencia+1)*2)*sizeof(double));
			*(ap_Testigos[i_i]) = 30*i_renovar_Adyacencia+1;
			*(ap_Testigos[i_i]+1) = 2;
			for(register int i_j=0; i_j<(30*i_renovar_Adyacencia+1)*2; i_j++) *(ap_Testigos[i_i]+i_j+2) = 0;
		}
		
	
	// Genero las redes de mi sistema
	GenerarOpi(ps_red,ps_datos); // Esto me inicializa mis vectores de opinión, asignándole a cada agente una opinión en cada tópico
	GenerarAng(ps_red,ps_datos); // Esto me inicializa mi matriz de superposición, definiendo el solapamiento entre tópicos.

	// Acá tengo que poner la inicialización de los valores de Actividad
	// Aprovecho también para guardarme los valores de actividad de mis agentes en orden
	// por número de agente.
	Actividad(ps_red->pd_Act,ps_datos->d_epsilon,-ps_datos->d_gamma);
	fprintf(pa_archivo2, "\tActividades agentes\n");
	Escribir_d(ps_red->pd_Act,pa_archivo2);
	fprintf(pa_archivo2, "\tAgentes Activados\n");

	// Evolucionemos el sistema utilizando un mecanismo de corte
	// Queda para el futuro ver si vale la pena meter esto en una sola función.
	fprintf(pa_archivo1,"\tEstado Inicial Matriz de Opiniones\n");
	Escribir_d(ps_red->pd_Opi,pa_archivo1);
	fprintf(pa_archivo1, "\tVariacion Promedio\n");
	
	// Voy a separar esto en dos for por una cuestión de facilidad de lectura. Quiero correr de manera
	// de que la red de actividad se genera en total 30 veces
	for(register int i_ciclos=0; i_ciclos<i_rearmar; i_ciclos++){
		Adyacencia_Actividad(ps_red, ps_datos);
		Escribir_i(ps_red->pi_Activados,pa_archivo2); // Esto me guarda el regsitro de los agentes que se activaron
		i_gradosumado = 0;
		for(int register i_i=0; i_i<ps_red->pi_Ady[0]*ps_red->pi_Ady[1]; i_i++) i_gradosumado += ps_red->pi_Ady[i_i+2];
		ps_red->pd_Km[i_ciclos+2] = (double) i_gradosumado/ps_datos->i_N;
		for(register int i_contador=0; i_contador<i_renovar_Adyacencia; i_contador++){
			for(register int i_sujeto=0; i_sujeto<i_testigos; i_sujeto++) for(register int i_opinion=0; i_opinion<2; i_opinion++){
				*(ap_Testigos[i_sujeto]+i_momento*2+i_opinion+2) = ps_red->pd_Opi[a_Testigos[i_sujeto]*ps_datos->i_T+i_opinion+2];
			}
			i_momento++;
			for(register int i_j=0; i_j<ps_datos->i_N*ps_datos->i_T; i_j++) ps_red->pd_PreOpi[i_j+2] = ps_red->pd_Opi[i_j+2];
			Iteracion(ps_red,ps_datos,ps_tab,pf_EcDin);
			// Escribir_d(ps_red->pd_Opi,pa_archivo1); // Matriz de Opinión
			Delta_Vec_d(ps_red->pd_Opi,ps_red->pd_PreOpi,ps_red->pd_Diferencia); // Veo la diferencia entre el paso previo y el actual en las opiniones
			ps_red->d_Varprom = Norma_d(ps_red->pd_Diferencia)/ps_datos->d_NormDif; // Calculo la suma de las diferencias al cuadrado y la normalizo.
			fprintf(pa_archivo1, "\t%lf",ps_red->d_Varprom);
		}
	}
	for(register int i_sujeto=0; i_sujeto<i_testigos; i_sujeto++) for(register int i_opinion=0; i_opinion<2; i_opinion++){
			*(ap_Testigos[i_sujeto]+i_momento*2+i_opinion+2) = ps_red->pd_Opi[a_Testigos[i_sujeto]*ps_datos->i_T+i_opinion+2];
		}
	
	// Guardo las opiniones finales, la semilla y las opiniones de los testigos en el primer archivo
	fprintf(pa_archivo1, "\n");
	fprintf(pa_archivo1, "\tEstado Final Matriz de Opiniones\n");
	Escribir_d(ps_red->pd_Opi,pa_archivo1); // Matriz de Opinión
	fprintf(pa_archivo1, "\tSemilla\n");
	fprintf(pa_archivo1,"\t%ld\n",semilla);
	for(register int i_sujeto=0; i_sujeto<i_testigos; i_sujeto++){
		fprintf(pa_archivo1,"\tAgente %d\n",a_Testigos[i_sujeto]);
		Escribir_d(ap_Testigos[i_sujeto],pa_archivo1);
	}
	
	// Guardo los valores de grados medios en el segundo archivo
	fprintf(pa_archivo2,"\tGrado medio\n");
	Escribir_d(ps_red->pd_Km,pa_archivo2);
	
	
	// Libero los espacios dedicados a mis vectores y cierro mis archivos
	for(register int i_i=0; i_i<i_testigos; i_i++) free(ap_Testigos[i_i]);
	free(ps_red->pd_Ang);
	free(ps_red->pi_Ady);
	free(ps_red->pd_Opi);
	free(ps_red->pd_PreOpi);
	free(ps_red->pd_Diferencia);
	free(ps_red->pd_Act);
	free(ps_red->pi_Activados);
	free(ps_red->pd_Km);
	free(ps_tab->pd_valores);
	free(ps_tab);
	free(ps_red);
	free(ps_datos);
	fclose(pa_archivo1);
	fclose(pa_archivo2);
	
	// Finalmente imprimo el tiempo que tarde en ejecutar todo el programa
	time(&tt_fin);
	f_tardanza = tt_fin-tt_prin;
	printf("Tarde %.1f segundos \n",f_tardanza);
	
	return 0;
 }

