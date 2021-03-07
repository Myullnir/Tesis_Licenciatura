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
	
	// Creo mis punteros a structs y los malloqueo.
		ps_Param ps_datos; // No te vayas a confundir, que ps_Param es el tipo de dato definido por usuario como un puntero al struct Parametros. En cambio, ps_datos es un puntero
		ps_datos = malloc(sizeof(s_Param));
		
		ps_Red ps_red; // No te vayas a confundir, que ps_Red es el tipo de dato definido por usuario como un puntero al struct Red. En cambio, ps_red es un puntero
		ps_red = malloc(sizeof(s_Red)); 
		
		// double d_AngtRad = (double) (2*M_PI)/360; // La idea es que con el instanciar le paso el ángulo en grados al archivo y esta es la constante para pasarlo a radianes.
		
		// Parámetros de mi modelo. Esto va desde número de agentes hasta el paso temporal de integración.
		ps_datos->i_N = strtol(argv[1],NULL,10); // Cantidad de agentes en el modelo
		ps_datos->i_T = 2;  //strtol(argv[1],NULL,10); Antes de hacer esto, arranquemos con número fijo   // Cantidad de temas sobre los que opinar
		ps_datos->f_Gradomedio = 8; // Valor de grado medio de los agentes de la red
		ps_datos->f_Pint = ps_datos->f_Gradomedio/(ps_datos->i_N-1); // Probabilidad de que se forme un enlace entre dos agentes aleatorios.
		ps_datos->f_K = 1; // Influencia social
		ps_datos->f_dt = 0.001; // Paso temporal de iteración del sistema
		ps_datos->f_alfa = strtof(argv[2],NULL)/10; // Controversialidad de los tópicos. Arranquemos con controversialidad intermedia. Voy a estar dividiendo esto acá para poder pasar enteros desde el instanciar.
		ps_datos->i_Mopi = 3; // Este es el valor de máxima opinión inicial del sistema
		ps_datos->d_NormDif = sqrt(ps_datos->i_N*ps_datos->i_T); // Este es el valor de Normalización de la variación del sistema, que me da la variación promedio de las opiniones.
		ps_datos->d_CritCorte = pow(10,-6); // Este valor es el criterio de corte. Con este criterio, toda variación más allá de la quinta cifra decimal es despreciable.
		ps_datos->i_Itextra = 2000; // Este valor es la cantidad de iteraciones extra que el sistema tiene que hacer para cersiorarse que el estado alcanzado efectivamente es estable
		ps_datos->f_Cosangulo =  0.2; // Este es el coseno de Delta que define la relación entre tópicos.
		int i_contador = 0; // Esta variable se encarga de llevar la cuenta de las iteraciones extra que realiza mi sistema.
		int i_tamaño = 0; // Esta variable mide el tamaño de la componente gigante de mi red.
		float DT[5] = {0.001,0.005,0.01,0.05,0.1}; // Estos son los valores de DT en los cuales voy a iterar
		
		// Matrices de mi sistema. Estas son la de Adyacencia, la de Superposición de Tópicos y la de vectores de opinión de los agentes.
		// También hay una matriz de paso previo del sistema, un vector para guardar la diferencia entre el paso previo y el actual y uno para los
		// valores de opiniones iniciales del sistema, para que todos arranquen del mismo lugar.
		ps_red->pd_Ang = (double*) malloc((2+ps_datos->i_T*ps_datos->i_T)*sizeof(double)); // Matriz simétrica de superposición entre tópicos.
		ps_red->pi_Ady = (int*) malloc((2+ps_datos->i_N*ps_datos->i_N)*sizeof(int)); // Matriz de adyacencia de la red. Determina quienes están conectados con quienes
		ps_red->pd_Opi = (double*) malloc((2+ps_datos->i_T*ps_datos->i_N)*sizeof(double)); // Lista de vectores de opinión de la red, Tengo T elementos para cada agente.
		ps_red->pd_PreOpi = (double*) malloc((2+ps_datos->i_T*ps_datos->i_N)*sizeof(double)); // Paso previo del sistema antes de iterar.
		ps_red->pd_Diferencia = (double*) malloc((2+ps_datos->i_T*ps_datos->i_N)*sizeof(double)); // Paso previo del sistema antes de iterar.
		ps_red->pd_OpiInicial = (double*) malloc((2+ps_datos->i_T*ps_datos->i_N)*sizeof(double)); // Lista de vectores de opiniones iniciales de la red, Tengo T elementos para cada agente.
		
		
		// Inicializo mis cinco "matrices".
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
		
		// Matriz de vectores de opiniones iniciales. Es de tamaño N*T
		for(register int i_i=0; i_i<ps_datos->i_N*ps_datos->i_T+2; i_i++) ps_red->pd_OpiInicial[i_i] = 0;
		ps_red->pd_OpiInicial[0] = ps_datos->i_N; // Pongo el número de filas en la primer coordenada
		ps_red->pd_OpiInicial[1] = ps_datos->i_T; // Pongo el número de columnas en la segunda coordenada
				
		// Inicializo el Agente y Tópico a mirar. Esto no significa mucho porque después lo voy a cambiar.
		ps_red->i_agente = 0;
		ps_red->i_topico = 0;
		ps_red->i_agente2 = 0;
		
		// Puntero a la función que define mi ecuación diferencial
		double (*pf_EcDin)(ps_Red var, ps_Param par) = &Din2;
		
	
	// Genero las redes de mi sistema
	GenerarOpi(ps_red,ps_datos); // Esto me inicializa mis vectores de opinión, asignándole a cada agente una opinión en cada tópico
	GenerarAng(ps_red,ps_datos); // Esto me inicializa mi matriz de superposición, definiendo el solapamiento entre tópicos.
	
	// Me armo una red conexa, por eso voy a repetir el proceso de creación hasta que el tamaño de la componente gigante sea toda la red.
	do{
		GenerarAdy(ps_red,ps_datos); // Esto me inicializa mi matriz de adyacencia, creando las conexiones de mi red
		i_tamaño = Tamaño_Comunidad(ps_red->pi_Ady,0);
	}
	while(i_tamaño != ps_datos->i_N);
	
	for(register int i_i=0; i_i<ps_datos->i_N*ps_datos->i_T; i_i++) ps_red->pd_OpiInicial[i_i+2] = ps_red->pd_Opi[i_i+2]; // Me guardo mi versión original del sistema
	
	for(register int i_i=0; i_i<5; i_i++){
		
		ps_datos->f_dt = DT[i_i]; // Establezco el nuevo dt
		
		// Reinicio las opiniones
		for(register int i_j=0; i_j<ps_red->pd_Opi[0]*ps_red->pd_Opi[1]; i_j++) ps_red->pd_Opi[i_j+2] = ps_red->pd_OpiInicial[i_j+2];
		
		
		// Voy a abrir un archivo ahora para la evolución de opiniones
			char s_archivo1[255];
			sprintf(s_archivo1,"Datos_Opiniones_alfa=%.3f_dt=%.3f",ps_datos->f_alfa,ps_datos->f_dt);
			FILE *pa_archivo1=fopen(s_archivo1,"w"); // Con esto abro mi archivo y dirijo el puntero a él.
		
		// Anoto los valores de mis tres matrices en mi archivo de evolución de opiniones
		fprintf(pa_archivo1, "\tMatriz de Adyacencia\n");
		Escribir_i(ps_red->pi_Ady,pa_archivo1); // Matriz de Adyacencia
		fprintf(pa_archivo1, "\tMatriz de Superposicion\n");
		Escribir_d(ps_red->pd_Ang,pa_archivo1); // Matriz de Superposición
		fprintf(pa_archivo1, "\tMatriz de Opiniones\n");
		Escribir_d(ps_red->pd_Opi,pa_archivo1); // Matriz de Opinión
		
		// Evolucionemos el sistema utilizando un mecanismo de corte
		// Queda para el futuro ver si vale la pena meter esto en una sola función.
		while(i_contador<ps_datos->i_Itextra){
			// Inicializo el contador
			i_contador = 0;
			
			// Evoluciono el sistema hasta que se cumpla el criterio de corte
			do{
				for(register int i_j=0; i_j<ps_datos->i_N*ps_datos->i_T; i_j++) ps_red->pd_PreOpi[i_j+2] = ps_red->pd_Opi[i_j+2];
				Iteracion(ps_red,ps_datos,pf_EcDin);
				Escribir_d(ps_red->pd_Opi,pa_archivo1); // Matriz de Opinión
				Delta_Vec_d(ps_red->pd_Opi,ps_red->pd_PreOpi,ps_red->pd_Diferencia); // Veo la diferencia entre el paso previo y el actual en las opiniones
				ps_red->d_Varprom = Norma_d(ps_red->pd_Diferencia)/ps_datos->d_NormDif; // Calculo la suma de las diferencias al cuadrado y la normalizo.
			}
			while(ps_red->d_Varprom > ps_datos->d_CritCorte);
			
			// Ahora evoluciono el sistema una cantidad i_Itextra de veces. Le pongo como condición que si el sistema deja de cumplir la condición de corte, deje de evolucionar
			while(i_contador < ps_datos->i_Itextra && ps_red->d_Varprom <= ps_datos->d_CritCorte ){
				for(register int i_j=0; i_j < ps_datos->i_N*ps_datos->i_T; i_j++) ps_red->pd_PreOpi[i_j+2] = ps_red->pd_Opi[i_j+2];
				Iteracion(ps_red,ps_datos,pf_EcDin);
				Escribir_d(ps_red->pd_Opi,pa_archivo1); // Matriz de Opinión
				Delta_Vec_d(ps_red->pd_Opi,ps_red->pd_PreOpi,ps_red->pd_Diferencia); // Veo la diferencia entre el paso previo y el actual en las opiniones
				ps_red->d_Varprom = Norma_d(ps_red->pd_Diferencia)/ps_datos->d_NormDif; // Calculo la suma de las diferencias al cuadrado y la normalizo.
				i_contador +=1;
			}
			// Si el sistema evolucionó menos veces que la cantidad arbitraria, es porque rompió la condiciones de corte.
			// Por tanto lo vuelvo a hacer trabajar hasta que se vuelva a cumplir la condición de corte.
			// Si logra evolucionar la cantidad arbitraria de veces sin problemas, termino la evolución.
		}
		fclose(pa_archivo1);
		i_contador = 0;
	
	}
	// Libero los espacios dedicados a mis vectores y cierro mis archivos
	free(ps_red->pd_Ang);
	free(ps_red->pi_Ady);
	free(ps_red->pd_Opi);
	free(ps_red->pd_PreOpi);
	free(ps_red->pd_Diferencia);
	free(ps_red);
	free(ps_datos);
	
	// Finalmente imprimo el tiempo que tarde en ejecutar todo el programa
	time(&tt_fin);
	f_tardanza = tt_fin-tt_prin;
	printf("Tarde %.1f segundos \n",f_tardanza);
	
	return 0;
 }

