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
	srand(semilla); // Voy a definir la semilla a partir de un número entero que es el número de iteración  srand(time(NULL));
	float f_tardanza; // Este es el float que le paso al printf para saber cuanto tardé
	
	// Creo mis punteros a structs y los malloqueo.
		ps_Param ps_datos; // No te vayas a confundir, que ps_Param es el tipo de dato definido por usuario como un puntero al struct Parametros. En cambio, ps_datos es un puntero
		ps_datos = malloc(sizeof(s_Param));
		
		ps_Red ps_red; // No te vayas a confundir, que ps_Red es el tipo de dato definido por usuario como un puntero al struct Red. En cambio, ps_red es un puntero
		ps_red = malloc(sizeof(s_Red)); 
		
		ps_Tab ps_tab; // Al igual que en los otros, ps_Tab es el tipo de dato definidio por usuario como el puntero al struct Tabla, en cambio ps_tab es un puntero.
		ps_tab = malloc(sizeof(s_Tabla));
		
		
		// ps_red->s_Tred = NULL;
		sprintf(ps_red->s_Tred,"%s",argv[2]);
		
		
		// Parámetros de mi modelo. Esto va desde número de agentes hasta el paso temporal de integración.
		ps_datos->i_N = strtol(argv[1],NULL,10); // Cantidad de agentes en el modelo
		ps_datos->i_T = 2;  //strtol(argv[1],NULL,10); Antes de hacer esto, arranquemos con número fijo   // Cantidad de temas sobre los que opinar
		ps_datos->i_Gradomedio = strtol(argv[5],NULL,10); // Valor de grado medio de los agentes de la red. Esto lo obtengo del input porque ahora armo redes de diferentes grados medios
		ps_datos->f_K = 1; // Influencia social
		ps_datos->f_dt = 0.01; // Paso temporal de iteración del sistema
		ps_datos->i_ID = strtol(argv[6],NULL,10)%20; // La ID simplemente diferencia a las 20 redes que armé que son del mismo tipo, con el mismo N y el mismo Gm.
		ps_datos->f_alfa = strtof(argv[3],NULL)/100; // Controversialidad de los tópicos. Arranquemos con controversialidad intermedia. Voy a estar dividiendo esto acá para poder pasar enteros desde el instanciar.
		ps_datos->i_Mopi = 3; // Este es el valor de máxima opinión inicial del sistema
		ps_datos->d_NormDif = sqrt(ps_datos->i_N*ps_datos->i_T); // Este es el valor de Normalización de la variación del sistema, que me da la variación promedio de las opiniones.
		ps_datos->d_CritCorte = 0.0005; // Este valor es el criterio de corte. Con este criterio, toda variación más allá de la quinta cifra decimal es despreciable.
		ps_datos->i_Itextra = 50; // Este valor es la cantidad de iteraciones extra que el sistema tiene que hacer para cersiorarse que el estado alcanzado efectivamente es estable
		ps_datos->f_Cosangulo = strtof(argv[4],NULL)/100; // Este es el coseno de Delta que define la relación entre tópicos.
		ps_datos->i_pasosprevios = 20; // Elegimos 20 de manera arbitraria con Pablo y Sebas. Sería la cantidad de pasos hacia atrás que miro para comparar cuanto varió el sistema
		
		// Estos son unas variables que si bien podrían ir en el puntero red, son un poco ambiguas y no vale la pena pasarlas a un struct.
		int i_contador = 0; // Esta variable se encarga de llevar la cuenta de las iteraciones extra que realiza mi sistema.
		int i_iteracion = strtol(argv[6],NULL,10); // Número de instancia de la simulación.
		
		// Voy a armar mi array de punteros, el cual voy a usar para guardar los datos de pasos previos del sistema
		double* ap_OpinionesPrevias[ps_datos->i_pasosprevios];
		
		for(register int i_i=0; i_i<ps_datos->i_pasosprevios; i_i++){
			ap_OpinionesPrevias[i_i] = (double*) malloc((2+ps_datos->i_T*ps_datos->i_N)*sizeof(double));
			*ap_OpinionesPrevias[i_i] = ps_datos->i_N;
			*(ap_OpinionesPrevias[i_i]+1) = ps_datos->i_T;
			for(register int i_j=0; i_j<ps_datos->i_T*ps_datos->i_N;i_j++) *(ap_OpinionesPrevias[i_i]+i_j+2) = 0;
		}
		
		
		// Matrices de mi sistema. Estas son la de Adyacencia, la de Superposición de Tópicos y la de vectores de opinión de los agentes.
		// También hay una matriz de paso previo del sistema y un vector para guardar la diferencia entre el paso previo y el actual.
		ps_red->pd_Ang = (double*) malloc((2+ps_datos->i_T*ps_datos->i_T)*sizeof(double)); // Matriz simétrica de superposición entre tópicos.
		ps_red->pi_Ady = (int*) malloc((2+ps_datos->i_N*ps_datos->i_N)*sizeof(int)); // Matriz de adyacencia de la red. Determina quienes están conectados con quienes
		ps_red->pd_Opi = (double*) malloc((2+ps_datos->i_T*ps_datos->i_N)*sizeof(double)); // Lista de vectores de opinión de la red, Tengo T elementos para cada agente.
		ps_red->pd_PreOpi = (double*) malloc((2+ps_datos->i_T*ps_datos->i_N)*sizeof(double)); // Paso previo del sistema antes de iterar.
		ps_red->pd_Diferencia = (double*) malloc((2+ps_datos->i_T*ps_datos->i_N)*sizeof(double)); // Paso previo del sistema antes de iterar.
		
		// Voy a abrir cuatrio archivos. Uno para anotar la evolución de opiniones.
		// El segundo es donde voy a guardar la evolución del sistema paso a paso para un cierto grupo de agentes.
		// El otro es del que voy a levantar mi matriz de Adyacencia
		// El tercero es para levantar los datos de la Tabla_Valores_TANH
		char s_archivo1[355];
		// Estas líneas son gigantescamente largas porque tienen anotado todo el path para el lugar donde se van a guardar los archivos,
		// y además lo archivos tienen que tener registro de bastantes datos importantes de la red. Ese registro por ahora lo vengo
		// llevando en el nombre de los archivos, pero supongo que podría pensar en el futuro para pasar eso a un archivo separado
		// que guarde junto a los archivos. Cuestión que esto hace que no sea necesario el usar el archivo de Bash Mover.sh
		// Hay tres if porque cada uno corresponde a cada tipo de red en particular.
		if(strcmp("Barabasi",argv[2])==0) sprintf(s_archivo1,"../Programas Python/DRE/DinaReg/Barabasi/Datos_Opiniones_alfa=%.3f_Cdelta=%.2f_N=%d_Gm=%d_ID=%d_Iter=%d",ps_datos->f_alfa,ps_datos->f_Cosangulo,ps_datos->i_N,ps_datos->i_Gradomedio,ps_datos->i_ID,i_iteracion);
		if(strcmp("ErdosRenyi",argv[2])==0) sprintf(s_archivo1,"../Programas Python/DRE/DinaReg/Erdos-Renyi/Datos_Opiniones_alfa=%.3f_Cdelta=%.2f_N=%d_Gm=%d_ID=%d_Iter=%d",ps_datos->f_alfa,ps_datos->f_Cosangulo,ps_datos->i_N,ps_datos->i_Gradomedio,ps_datos->i_ID,i_iteracion);
		if(strcmp("RandomR",argv[2])==0) sprintf(s_archivo1,"../Programas Python/DRE/DinaReg/RandomRegulars/Datos_Opiniones_alfa=%.3f_Cdelta=%.2f_N=%d_Gm=%d_ID=%d_Iter=%d",ps_datos->f_alfa,ps_datos->f_Cosangulo,ps_datos->i_N,ps_datos->i_Gradomedio,ps_datos->i_ID,i_iteracion);
		FILE *pa_archivo1=fopen(s_archivo1,"w"); // Con esto abro mi archivo y dirijo el puntero a él.
		
		
		char s_archivo2[355];
		// Estas líneas son gigantescamente largas porque tienen anotado todo el path para el lugar donde se van a guardar los archivos,
		// y además lo archivos tienen que tener registro de bastantes datos importantes de la red. Ese registro por ahora lo vengo
		// llevando en el nombre de los archivos, pero supongo que podría pensar en el futuro para pasar eso a un archivo separado
		// que guarde junto a los archivos. Cuestión que esto hace que no sea necesario el usar el archivo de Bash Mover.sh
		// Hay tres if porque cada uno corresponde a cada tipo de red en particular.
		if(strcmp("Barabasi",argv[2])==0) sprintf(s_archivo2,"../Programas Python/DRE/DinaReg/Barabasi/Evolucion_Sistema_alfa=%.3f_Cdelta=%.2f_N=%d_Gm=%d_ID=%d_Iter=%d",ps_datos->f_alfa,ps_datos->f_Cosangulo,ps_datos->i_N,ps_datos->i_Gradomedio,ps_datos->i_ID,i_iteracion);
		if(strcmp("ErdosRenyi",argv[2])==0) sprintf(s_archivo2,"../Programas Python/DRE/DinaReg/Erdos-Renyi/Evolucion_Sistema_alfa=%.3f_Cdelta=%.2f_N=%d_Gm=%d_ID=%d_Iter=%d",ps_datos->f_alfa,ps_datos->f_Cosangulo,ps_datos->i_N,ps_datos->i_Gradomedio,ps_datos->i_ID,i_iteracion);
		if(strcmp("RandomR",argv[2])==0) sprintf(s_archivo2,"../Programas Python/DRE/DinaReg/RandomRegulars/Evolucion_Sistema_alfa=%.3f_Cdelta=%.2f_N=%d_Gm=%d_ID=%d_Iter=%d",ps_datos->f_alfa,ps_datos->f_Cosangulo,ps_datos->i_N,ps_datos->i_Gradomedio,ps_datos->i_ID,i_iteracion);
		FILE *pa_archivo2=fopen(s_archivo2,"w"); // Con esto abro mi archivo y dirijo el puntero a él.
		
		// Esto me va a levantar mi matriz de Adyacencia. Armé tres ifs para los casos dependiendo del tipo de red que vaya a usar.
		char s_Mady[255];
		if(strcmp("Barabasi",argv[2])==0) sprintf(s_Mady,"../Programas Python/MARE/Barabasi/%s_N=%d_Gm=%d_ID=%d.txt",argv[2],ps_datos->i_N, ps_datos->i_Gradomedio,ps_datos->i_ID);
		if(strcmp("ErdosRenyi",argv[2])==0) sprintf(s_Mady,"../Programas Python/MARE/Erdos-Renyi/%s_N=%d_Gm=%d_ID=%d.txt",argv[2],ps_datos->i_N,ps_datos->i_Gradomedio,ps_datos->i_ID);
		if(strcmp("RandomR",argv[2])==0) sprintf(s_Mady,"../Programas Python/MARE/Random Regulars/%s_N=%d_Gm=%d_ID=%d.txt",argv[2],ps_datos->i_N,ps_datos->i_Gradomedio,ps_datos->i_ID);
		FILE *pa_Mady=fopen(s_Mady,"r"); // Con esto abro mi archivo y dirijo el puntero a él.
		
		
		
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
				
		// Inicializo el Agente y Tópico a mirar. Esto no significa mucho porque después lo voy a cambiar.
		ps_red->i_agente = 0;
		ps_red->i_topico = 0;
		ps_red->i_agente2 = 0;
		
		// Puntero a la función que define mi ecuación diferencial
		double (*pf_EcDin)(ps_Red var, ps_Param par, ps_Tab tab) = &Din2;
		
	
	// Genero las redes de mi sistema
	GenerarOpi(ps_red,ps_datos); // Esto me inicializa mis vectores de opinión, asignándole a cada agente una opinión en cada tópico
	GenerarAng(ps_red,ps_datos); // Esto me inicializa mi matriz de superposición, definiendo el solapamiento entre tópicos.

	// Levanto mi red conexa a partir de mi un archivo txt donde estaba armada previamente. Si hubo un error en 
	// el levantar la red, hago que corte todo ahora y además ya habrá mandado un mensaje. Luego cierro mi archivo.
	// Tengo un poco de duda sobre usar el goto, pero confío que todo está bien.
	if(Lectura_Adyacencia(ps_red->pi_Ady,pa_Mady) == 1){
		fclose(pa_Mady);
		goto Final;
	}
	fclose(pa_Mady);
	
	//############################################################################################################
	
	// Hablando con Seba y Pablo, charlamos sobre que no era necesario guardar TODOS los datos, porque eso ocupa mucho espacios
	// y tarda mucho tiempo. Por eso vamos a guardar sólo el estado final del sistema y la semilla. Por eso todo esto lo comento.
	
	// Anoto los valores de mis tres matrices en mi archivo de evolución de opiniones
	// fprintf(pa_archivo1, "\tMatriz de Adyacencia\n");
	// Escribir_i(ps_red->pi_Ady,pa_archivo1); // Matriz de Adyacencia
	// fprintf(pa_archivo1, "\tMatriz de Superposicion\n");
	// Escribir_d(ps_red->pd_Ang,pa_archivo1); // Matriz de Superposición
	// Escribir_d(ps_red->pd_Opi,pa_archivo1); // Matriz de Opinión
	fprintf(pa_archivo1,"\tEstado inicial Matriz de Opiniones\n");
	Escribir_d(ps_red->pd_Opi,pa_archivo1);
	fprintf(pa_archivo1, "\tVariacion Promedio\n");
	
	// Acá guardo los datos de las opiniones del sistema.
	// fprintf(pa_archivo2,"\tOpiniones de los agentes\n");
	// Escribir_d(ps_red->pd_Opi,pa_archivo2);
	
	//############################################################################################################
	
	// Esto es una "Termalización" del sistema. Dejo pasar i_IndiceOpiPasado iteraciones para guardarlas en mi lista de arrays y de
	// ahí ya usarlo en el resto del programa
	
	int i_IndiceOpiPasado = 0;
	
	for(register int i_i=0; i_i<ps_datos->i_pasosprevios; i_i++){
		for(register int i_j=0; i_j<ps_datos->i_N*ps_datos->i_T; i_j++) ps_red->pd_PreOpi[i_j+2] = ps_red->pd_Opi[i_j+2];
		Iteracion(ps_red,ps_datos,ps_tab,pf_EcDin);
		for(register int i_j=0; i_j<ps_datos->i_N*ps_datos->i_T; i_j++) *(ap_OpinionesPrevias[i_IndiceOpiPasado]+i_j+2) = ps_red->pd_Opi[i_j+2];
		// Escribir_d(ps_red->pd_Opi,pa_archivo2);
		i_IndiceOpiPasado++;
	}
	
	
	//############################################################################################################
	
	// Evolucionemos el sistema utilizando un mecanismo de corte
	// Queda para el futuro ver si vale la pena meter esto en una sola función.
	while(i_contador < ps_datos->i_Itextra){
		// Inicializo el contador
		i_contador = 0;
		
		// Evoluciono el sistema hasta que se cumpla el criterio de corte
		do{
			for(register int i_j=0; i_j<ps_datos->i_N*ps_datos->i_T; i_j++) ps_red->pd_PreOpi[i_j+2] = ps_red->pd_Opi[i_j+2];
			Iteracion(ps_red,ps_datos,ps_tab,pf_EcDin);
			// Escribir_d(ps_red->pd_Opi,pa_archivo2);
			i_IndiceOpiPasado++;
			// Escribir_d(ps_red->pd_Opi,pa_archivo1); // Matriz de Opinión
			Delta_Vec_d(ps_red->pd_Opi,ap_OpinionesPrevias[i_IndiceOpiPasado%ps_datos->i_pasosprevios],ps_red->pd_Diferencia); // Veo la diferencia entre 20 pasos anteriores y el actual en las opiniones
			ps_red->d_Varprom = Norma_d(ps_red->pd_Diferencia)/ps_datos->d_NormDif; // Calculo la suma de las diferencias al cuadrado y la normalizo.
			for(register int i_p=0; i_p<ps_datos->i_N*ps_datos->i_T; i_p++) *(ap_OpinionesPrevias[i_IndiceOpiPasado%ps_datos->i_pasosprevios]+i_p+2) = ps_red->pd_Opi[i_p+2];
			fprintf(pa_archivo1, "\t%lf",ps_red->d_Varprom);
		}
		while(ps_red->d_Varprom > ps_datos->d_CritCorte);
		
		// Ahora evoluciono el sistema una cantidad i_Itextra de veces. Le pongo como condición que si el sistema deja de cumplir la condición de corte, deje de evolucionar
		while(i_contador < ps_datos->i_Itextra && ps_red->d_Varprom <= ps_datos->d_CritCorte ){
			for(register int i_j=0; i_j < ps_datos->i_N*ps_datos->i_T; i_j++) ps_red->pd_PreOpi[i_j+2] = ps_red->pd_Opi[i_j+2];
			Iteracion(ps_red,ps_datos,ps_tab,pf_EcDin);
			// Escribir_d(ps_red->pd_Opi,pa_archivo2);
			i_IndiceOpiPasado++;
			// Escribir_d(ps_red->pd_Opi,pa_archivo1); // Matriz de Opinión
			Delta_Vec_d(ps_red->pd_Opi,ap_OpinionesPrevias[i_IndiceOpiPasado%ps_datos->i_pasosprevios],ps_red->pd_Diferencia); // Veo la diferencia entre el paso previo y el actual en las opiniones
			ps_red->d_Varprom = Norma_d(ps_red->pd_Diferencia)/ps_datos->d_NormDif; // Calculo la suma de las diferencias al cuadrado y la normalizo.
			for(register int i_p=0; i_p<ps_datos->i_N*ps_datos->i_T; i_p++) *(ap_OpinionesPrevias[i_IndiceOpiPasado%ps_datos->i_pasosprevios]+i_p+2) = ps_red->pd_Opi[i_p+2];
			fprintf(pa_archivo1, "\t%lf",ps_red->d_Varprom);
			i_contador +=1;
		}
		// Si el sistema evolucionó menos veces que la cantidad arbitraria, es porque rompió la condiciones de corte.
		// Por tanto lo vuelvo a hacer trabajar hasta que se vuelva a cumplir la condición de corte.
		// Si logra evolucionar la cantidad arbitraria de veces sin problemas, termino la evolución.
	}
	
	// Guardo los datos finales del sistema y la semilla
	
	fprintf(pa_archivo1, "\n");
	fprintf(pa_archivo1, "\tEstado Final Matriz de Opiniones\n");
	Escribir_d(ps_red->pd_Opi,pa_archivo1); // Matriz de Opinión
	fprintf(pa_archivo1, "\tSemilla\n");
	fprintf(pa_archivo1,"\t%ld\n",semilla);
	
	
	Final:
	
	// Libero los espacios dedicados a mis vectores y cierro mis archivos
	for(register int i_i=0; i_i<ps_datos->i_pasosprevios; i_i++) free(ap_OpinionesPrevias[i_i]);
	free(ps_red->pd_Ang);
	free(ps_red->pi_Ady);
	free(ps_red->pd_Opi);
	free(ps_red->pd_PreOpi);
	free(ps_red->pd_Diferencia);
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

