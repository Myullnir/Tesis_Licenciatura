// Este archivo es para guardar programas de pruebas armados previamente.

Para acceder a los programas rápido salteando todo el código que no querés ver
lo que tenés que hacer es apretar Ctrl+F, eso te abre el buscador de palabras dentro del código.
Lo que tenés que buscar es la palabra "NUEVO_PROGRAMA", con las mayúsculas y guión, todo correcto.
Luego vas saltando de uno al siguiente, y eso rápidamente te mueve entre programas


//-----------------------------------------------------------------------------------
//-----------------------------------------------------------------------------------
//-----------------------------------------------------------------------------------

NUEVO_PROGRAMA


Este es el programa que armé el 14/12/2020. La idea era probar cómo funcionan los arrays de punteros.
Esto es sólo para ver cómo funcionan, no hace nada especial. La sección de la evolución dinámica del
sistema no es necesaria para este programa.




// #include<stdio.h>
// #include<stdlib.h>
// #include<math.h>
// #include<time.h>

// // Acá vienen los structs.
// // El struct Red tiene los datos que definen mi red, y la info de la red
// struct Red{
	// double *pd_Ang; // Matriz de superposición entre tópicos. Tiene tamaño T*T
	// int *pi_Ady; // Matriz de adyacencia que define mis conexiones. Tiene tamaño N*N
	// double *pd_Opi; // Vector de opinión de cada individuo
	// int i_agente; // Entero que representa el agente que estoy mirando. Es un valor que va entre 0 y N-1
	// int i_topico; // Entero que representa el tópico que estoy mirando. Es un valor que va entre 0 y T-1
// };

// struct Parametros{
	// float f_Beta; // Exponente que regula el grado de homofilia
	// float f_Pint; // Probabilidad de que se forme el enlace de manera aleatoria
	// float f_K; // Influencia social
	// float f_alfa; // Controversialidad de los temas
	// int i_N; // Número de agentes en la red
	// int i_T; // Cantidad de tópicos
	// int i_Mopi; // Máximo inicial de opiniones
	// float f_dt; // Paso temporal de iteración del sistema
// };

// // Acá voy a declarar las funciones.------------------------------------

// double Random();
// int Visualizar_d(double *pd_vec);
// int Visualizar_f(float *pf_vec);
// int Visualizar_i(int *pi_vec);
// int GenerarOpi(struct Red var, struct Parametros par);
// int GenerarAng(struct Red var);
// int GenerarAdy(struct Red var, struct Parametros par);
// double Din1(struct Red var, struct Parametros par, int i_j);
// double Din2(struct Red var, struct Parametros par);
// double Duplicar(struct Red var, struct Parametros par);



// /*####################################################################################
// ####################################################################################
// ####################################################################################
// ####################################################################################
// */


// //---------------------------------------------------------------------------------------------------

// // Vamos a intentar ver como se leen archivos y data desde estos
// // Creo que lo más útil va a ser usar el fscanf porque mis datos están separados por tabulaciones
// // Acá está la forma de leer el archivo. Sólo necesitaría poder saber que tan largo es antes de
// // subirlo, pero creo que eso sería mucho pedir.

// int main(){
	// // Defino mis variables temporales para medir el tiempo que tarda el programa. También genero una nueva semilla
	// time_t tt_prin,tt_fin;
	// time(&tt_prin);
	// srand(time(NULL));
	// int i_tardanza;
	
	
	// // Defino los nombres de mis structs en este programa y los valores de los parámetros
	// struct Red red;
	// struct Parametros datos;
	// datos.f_Beta = 0.5;
	// datos.f_Pint = 1;
	// datos.f_K = 0.5;
	// datos.f_alfa = 2;
	// datos.i_N = 5;
	// datos.i_T = 4;
	// datos.i_Mopi = 3;
	// datos.f_dt = 0.5;
	
	// // Asigno memoria a mis matrices y las inicializo
	
	// // Matriz de Vectores de opinión. Tiene tamaño N*T
	// red.pd_Opi = (double*) malloc((datos.i_N*datos.i_T+2)*sizeof(double)); // Asigno espacio de memoria al vector
	// for(register int i_i=0; i_i<datos.i_N*datos.i_T+2; i_i++) red.pd_Opi[i_i] = 0; // Inicializo la matriz para que no haya "basura" en alguna posición
	// red.pd_Opi[0] = datos.i_N; // Guardo el número de filas en la primer coordenada del vector
	// red.pd_Opi[1] = datos.i_T; // Guardo el número de Columnas en la segunda coordenada del vector
	// GenerarOpi(red,datos); // Genero la red de Vectores de opinión propiamente dicha.

	// // Matriz de Superposición. Tiene tamaño T*T
	// red.pd_Ang = (double*) malloc((datos.i_T*datos.i_T+2)*sizeof(double)); // Asigno espacio de memoria al vector
	// for(register int i_i=0; i_i<datos.i_T*datos.i_T+2; i_i++) red.pd_Ang[i_i] = 0; // Inicializo la matriz para que no haya "basura" en alguna posición
	// red.pd_Ang[0] = datos.i_T; // Guardo el número de filas en la primer coordenada del vector
	// red.pd_Ang[1] = datos.i_T; // Guardo el número de Columnas en la segunda coordenada del vector
	// GenerarAng(red); // Genero la red de Vectores de opinión propiamente dicha.
	
	// // Matriz de Adyacencia. Tiene tamaño N*N
	// red.pi_Ady = (int*) malloc((datos.i_N*datos.i_N+2)*sizeof(int)); // Asigno espacio de memoria al vector
	// for(register int i_i=0; i_i<datos.i_N*datos.i_N+2; i_i++) red.pi_Ady[i_i] = 0; // Inicializo la matriz para que no haya "basura" en alguna posición
	// red.pi_Ady[0] = datos.i_N; // Guardo el número de filas en la primer coordenada del vector
	// red.pi_Ady[1] = datos.i_N; // Guardo el número de columnas en la segunda coordenada del vector
	// GenerarAdy(red,datos); // Genero la red de Adyacencia propiamente dicha.
	
	// double *pa_proba[2];
	// pa_proba[0] = red.pd_Opi;
	// pa_proba[1] = red.pd_Ang;
	
	// // Visualizo las redes para ver que todo funca bien
	// /*Visualizar(red,0);
	// Visualizar(red,1);
	// Visualizar(red,2);*/
	
	// // Voy a probar visualizar a partir de mi array de punteros
	// for(register int i_i=0; i_i<2;i_i++){
		// int i_columnas = *(pa_proba[i_i]+1);
		// for(register int i_j=0; i_j<*pa_proba[i_i]; i_j++){
			// for(register int i_p=0; i_p<*(pa_proba[i_i]+1); i_p++) printf("%.03lf\t",*(pa_proba[i_i]+i_j*i_columnas+i_p+2));
			// printf("\n");
		// }
		// printf("\n");
	// }
	
	
	// // Evolución dinámica del sistema
	// /*
	// double d_prueba;
	// for(register int i_v=0; i_v<3; i_v++){
		// d_prueba = Din2(red,datos,0,i_v);
		// printf("La pendiente para el topico %d me dio %.5lf\n",i_v,d_prueba);
	// }*/
	
	// // Ejecuto los comandos finales para medir el tiempo.
	// free(red.pi_Ady);
	// free(red.pd_Ang);
	// free(red.pd_Opi);
	// time(&tt_fin);
	// i_tardanza = tt_fin-tt_prin;
	// printf("Tarde %d segundos en terminar\n",i_tardanza);
	// return 0;
// }

// /*####################################################################################
// ####################################################################################
// ####################################################################################
// ####################################################################################
// */

// // De acá en adelante van las funciones a declarar

// // Esta función me genera un número random
// double Random(){
	// return ((double) rand()/(double) RAND_MAX);
// }


// // Estas son las funciones de Inicialización.
// // #########################################################################################################


// // Esta función es para observar los vectores double
// int Visualizar_d(double *pd_vec){
	// // Defino las variables que voy a necesitar.
	// int i_F,i_C;
	// i_F = *pd_vec;
	// i_C = *(pd_vec+1);
	
	// // Printeo mi vector
	// for(register int i_i=0; i_i<i_F; i_i++){
		// for(register int i_j=0; i_j<i_C; i_j++) printf("%lf\t",*(pd_vec+i_i*i_C+i_j+2));
		// printf("\n");
	// }
	
	// return 0;
// }

// // Esta función es para observar los vectores float
// int Visualizar_f(float *pf_vec){
	// // Defino las variables que voy a necesitar.
	// int i_F,i_C;
	// i_F = *pf_vec;
	// i_C = *(pf_vec+1);
	
	// // Printeo mi vector
	// for(register int i_i=0; i_i<i_F; i_i++){
		// for(register int i_j=0; i_j<i_C; i_j++) printf("%lf\t",*(pf_vec+i_i*i_C+i_j+2));
		// printf("\n");
	// }
	
	// return 0;
// }

// // Esta función es para observar los vectores int
// int Visualizar_i(int *pi_vec){
	// // Defino las variables que voy a necesitar.
	// int i_F,i_C;
	// i_F = *pi_vec;
	// i_C = *(pi_vec+1);
	
	// // Printeo mi vector
	// for(register int i_i=0; i_i<i_F; i_i++){
		// for(register int i_j=0; i_j<i_C; i_j++) printf("%lf\t",*(pi_vec+i_i*i_C+i_j+2));
		// printf("\n");
	// }
	
	// return 0;
// }




// // Esta función me genera los vectores opinión iniciales del sistema. Esto es una matriz de tamaño N*T
// int GenerarOpi(struct Red var, struct Parametros par){
	// // Obtengo las dimensiones de la "matriz" de opiniones de mis agentes.
	// int i_Filas,i_Columnas;
	// i_Filas = (int) var.pd_Opi[0];
	// i_Columnas = (int) var.pd_Opi[1];
	
	// // Inicializo la "matriz" de opiniones de mis agentes.
	// for(int i_i=0;i_i<i_Filas*i_Columnas;i_i++) var.pd_Opi[i_i+2] = par.i_Mopi*(Random()-0.5)*2;
	// return 0;
// }

// // Esta función me genera la matriz de Superposicion del sistema. Esto es una matriz de T*T
// int GenerarAng(struct Red var){
	// // Obtengo las dimensiones de la matriz de Superposicion.
	// int i_Filas,i_Columnas;
	// i_Filas = (int) var.pd_Ang[0];
	// i_Columnas = (int) var.pd_Ang[1];
	
	// // Inicializo la matriz de Superposicion de mi sistema.
	// for(int i_i=0; i_i<i_Filas; i_i++) for(int i_j=0; i_j<i_i; i_j++) var.pd_Ang[i_i*i_Columnas+i_j+2] = 0.5; // Decidí poner 0.5 entre todos los tópicos de mi modelo
	// for(int i_i=0; i_i<i_Filas; i_i++) var.pd_Ang[i_i*i_Columnas+i_i+2] = 1; // Esto me pone 1 en toda la diagonal
	// for(int i_i=0; i_i<i_Filas; i_i++) for(int i_j=i_i+1; i_j<i_Columnas; i_j++) var.pd_Ang[i_i*i_Columnas+i_j+2] = var.pd_Ang[i_j*i_Columnas+i_i+2]; // Esta sola línea simetriza la matriz
	// return 0;
// }


// // Esta función me inicializa la matriz de Adyacencia. Esto es una matriz de N*N
// int GenerarAdy(struct Red var, struct Parametros par){
	// // Obtengo las dimensiones de la matriz de Adyacencia.
	// int i_Filas,i_Columnas;
	// i_Filas = (int) var.pi_Ady[0];
	// i_Columnas = (int) var.pi_Ady[1];
	
	// // Inicializo la matriz de Adyacencia de mi sistema
	// for(int i_i=0; i_i<i_Filas; i_i++) {
		// for(int i_j=0; i_j<i_i; i_j++) {
			// // Saco un número random y veo si asigno un 1 o un 0 a esa posición-
			// if(Random()<par.f_Pint) var.pi_Ady[i_i*i_Columnas+i_j+2] = 1;
			// else var.pi_Ady[i_i*i_Columnas+i_j+2] = 0;
		// }
	// }
	// for(int i_i=0; i_i<i_Filas; i_i++) for(int i_j=i_i+1; i_j<i_Columnas; i_j++) var.pi_Ady[i_i*i_Columnas+i_j+2] = var.pi_Ady[i_j*i_Columnas+i_i+2]; // Esta sola línea simetriza la matriz
	// // for(int i=0; i<par.N; i++) var.Ady[i*par.N+i] = 1; // Esto me pone 1 en toda la diagonal
	// return 0;
// }

// // #####################################################################################

// // Estas son las funciones del avance
// //#######################################################################################

// // Esta función resuelve un término de los de la sumatoria.
// double Din1(struct Red var, struct Parametros par,int i_j){
	
	// // Defino las variables locales de mi función. d_resultados es el return. 
	// // d_opiniones_superpuestas es el producto de la matriz de superposición de tópicos con el vector opinión de un agente.
	// double d_resultado,d_opiniones_superpuestas = 0;
	
	// // Obtengo el tamaño de columnas de mis tres matrices
	// int i_Co,i_Cs,i_Ca;
	// i_Co = (int) var.pd_Opi[1];
	// i_Cs = (int) var.pd_Ang[1];
	// i_Ca = var.pi_Ady[1];
	
	// for(register int i_p=0; i_p<i_Cs; i_p++) d_opiniones_superpuestas += var.pd_Ang[var.i_topico*i_Cs+i_p+2]*var.pd_Opi[i_j*i_Co+i_p+2]; // Calculo previamente este producto de la matriz con el vector.
	// d_resultado = var.pi_Ady[var.i_agente*i_Ca+i_j+2]*tanh(par.f_alfa*d_opiniones_superpuestas); // Esto es lo que está dentro de la sumatoria en la ecuación dinámica.
	// return d_resultado; // La función devuelve el número que buscás, no te lo asigna en una variable.
// }

// // Esta es la segunda parte de la ecuación dinámica, con esto puedo realizar una iteración del sistema.
// double Din2(struct Red var, struct Parametros par){
	
	// // Defino las variables locales de mi función. d_resultado es lo que voy a returnear.
	// // d_sumatoria es el total de la sumatoria del segundo término de la ecuación diferencial.
	// double d_resultado,d_sumatoria=0;
	
	// // Calculo la sumatoria de la ecuación diferencial. Para esto es que existe la función Din1.
	// for(register int i_j=0; i_j<var.i_agente; i_j++) d_sumatoria += Din1(var,par,i_j);
	// for(register int i_j=var.i_agente+1; i_j<par.i_N; i_j++) d_sumatoria += Din1(var,par,i_j);
	
	// // Obtengo el tamaño de Columnas de mi matriz de Vectores de opinión y calculo el valor del campo que define mi ecuación diferencial
	// int i_Columnas = (int) var.pd_Opi[1];
	// d_resultado = -var.pd_Opi[var.i_agente*i_Columnas+var.i_topico+2]+par.f_K*d_sumatoria;
	// return d_resultado;
// }

// //#######################################################################################


// // Esta función me realiza una iteración del sistema a partir de un RK4.
// // Creo que no hay forma de que esta función sea 100% general para cualquier caso.
// // Incluso creo que no es necesario el uso del puntero de funciones, pero quiero aprender a usarlo
// int RK4(double *pd_vec ,struct Red var, struct Parametros par, double (*fp_funcion)(struct Red var, struct Parametros par)){
	// // Defino las variables y vectores que voy a necesitar
	// int i_filas = (int) *pd_vec; // Este es el número de filas del vector principal
	// int i_columnas = (int) *(pd_vec+1); // Este es el número de columnas del vector principal
	// double *pd_pendientes[5]; // Este array de punteros guarda los punteros kN
	// float DT[4]; // Esto me ayuda a meter el paso temporal que se usa para calcular cada pendiente.
	
	
	// // Voy a armar vectores con las pendientes que calcule, para luego calcular el avance de todas las variables al final
	// double *k0;
	// k0 = (double*) malloc((i_filas*i_columnas+2)*sizeof(double));
	
	// double *k1;
	// k1 = (double*) malloc((i_filas*i_columnas+2)*sizeof(double));
	
	// double *k2;
	// k2 = (double*) malloc((i_filas*i_columnas+2)*sizeof(double));
	
	// double *k3;
	// k3 = (double*) malloc((i_filas*i_columnas+2)*sizeof(double));
	
	// double *k4;
	// k4 = (double*) malloc((i_filas*i_columnas+2)*sizeof(double));
	
	// double *pd_inicial; // Este me guarda las condiciones iniciales del vector, que las voy a necesitar al calcular cada paso del RK4
	// pd_inicial = (double*) malloc((i_filas*i_columnas+2)*sizeof(double));
	
	// // Inicializo mis punteros
	// pd_pendientes[0] = k0;
	// pd_pendientes[1] = k1;
	// pd_pendientes[2] = k2;
	// pd_pendientes[3] = k3;
	// pd_pendientes[4] = k4;
	// for(register int i_i=0; i_i<i_filas*i_columnas+2; i_i++){
		// *(pd_inicial+i_i) = *(pd_vec+i_i);
		// for(register int i_j=0; i_j<5;i_j++) *(pd_pendientes[i_j]+i_i) = 0; // De esta manera inicializo los 5 punteros, todos en una sola línea.
	// }
	
	// // Guardo registro del tamaño de mis vectores k
	// for(register int i_j=0; i_j<5;i_j++) *(pd_pendientes[i_j]) = i_filas;
	// for(register int i_j=0; i_j<5;i_j++) *(pd_pendientes[i_j]+1) = i_columnas;
	
	// // Armo mi vector DT. Este hay que armarlo uno por uno, si o si.
	// DT[0] = 0;
	// DT[1] = var.f_dt*0.5;
	// DT[2] = var.f_dt*0.5;
	// DT[3] = var.f_dt;
		
	// // Acá hago las iteraciones del RK4 para hallar las pendientes k
	// for(register int i_j=0; i_j<4; i_j++){ // Esto itera para mis 4 k
		// for(var.i_agente=0; var.i_agente<*pd_vec; var.i_agente++){ // Itero para todos los agentes
			// for(var.i_topico=0; var.i_topico<*(pd_vec+1); var.i_topico++){ // Itero para todos los tópicos
				// // Calculo el elemento de la pendiente k(i_j+1)
				// for(register int i_i=0; i_i<i_filas*i_columnas;i_i++) *(pd_vec+i_i+2) = *(pd_inicial+i_i+2)+*(pd_pendientes[i_j]+i_i+2)*DT[i_j];
				// *(pd_pendientes[i_j+1]+var.i_agente*i_columnas+var.i_topico+2) = (*fp_funcion)(var,par);
			// }
		// }
	// }
	
	// // Con TODAS las pendientes calculadas, ahora sí avanzo temporalmente mi sistema
	
	// for(register int i_i=0; i_i<i_filas*i_columnas; i_i++){
	// *(pd_vec+i_i+2) = *(pd_inicial+i_i+2)+(var.f_dt/6)*(*(pd_pendientes[1]+i_i+2)+*(pd_pendientes[2]+i_i+2)*2+*(pd_pendientes[3]+i_i+2)*2+*(pd_pendientes[4]+i_i+2));
	// }
	
	// // Ahora hagamos algún mecanismo de visualización, para ver que todo esté correctamente calculado. Dios que esto va a ser un bardo.
	// // Primero visualicemos las pendientes. Para eso voy a armar unos strings que poner en el printeo
	
	// char c_npendientes[200] = {'k','1','k','2','k','3','k','4'};
	
	// for(register int i_i=0; i_i<4; i_i++){
		// printf("\n Estas son las pendientes %c%c \n",c_npendientes[i_i*2],c_npendientes[i_i*2+1])
		// Visualizar_d(pd_pendientes[i_i]);
	// }
	
	// // También tengo que visualizar mi vector trabajado.
	
	// printf("Este es mi vector antes de evolucionarlo \n")
	// Visualizar_d(pd_inicial);
	
	// printf("Este es mi vector luego de evolucionarlo \n");
	// Visualizar_d(pd_vec);
	


	// // Libero el espacio de memoria asignado a los punteros de las pendientes y al pd_inicial
	// free(pd_inicial);
	// for(int register i_i=0; i_i<5; i_i++) free(pd_pendientes[i_i]);
	// free(pd_pendientes);
	
	// return 0;
// }

// // Esta es una función 
// double Duplicar(struct Red var, struct Parametros par){
	// // Defino mi variable a usar
	// double doble;
	
	// // Esta ecuación diferencial me define las pendientes como el doble del valor actual.
	// doble = 2*var.pd_Opi[var.i_agente*var.pd_Opi[1]+var.i_topico+2];
		
	// return doble,
// }


//-----------------------------------------------------------------------------------
//-----------------------------------------------------------------------------------
//-----------------------------------------------------------------------------------

NUEVO_PROGRAMA

Este programa lo usé el 21/12/2020 para probar mi función de RK4. La estoy probando
usando la función Duplicar. Esta función lo que hace es determinarme una ecuación
diferencial en la cual la derivada es igual a un múltiplo del valor actual de
la función. Si lo corrés lo que va a hacer esto es printearte los valores
calculados de los k y el valor inicial y final del vector a evolucionar.
Esta probado, funciona bárbaro la función RK4




// #include<stdio.h>
// #include<stdlib.h>
// #include<math.h>
// #include<time.h>

// // Acá vienen los structs.
// // El struct Red tiene los datos que definen mi red, y la info de la red
// typedef struct Red{
	// double *pd_Ang; // Matriz de superposición entre tópicos. Tiene tamaño T*T
	// int *pi_Ady; // Matriz de adyacencia que define mis conexiones. Tiene tamaño N*N
	// double *pd_Opi; // Vector de opinión de cada individuo
	// int i_agente; // Entero que representa el agente que estoy mirando. Es un valor que va entre 0 y N-1
	// int i_topico; // Entero que representa el tópico que estoy mirando. Es un valor que va entre 0 y T-1
// } s_Red;

// typedef struct Parametros{
	// float f_Beta; // Exponente que regula el grado de homofilia
	// float f_Pint; // Probabilidad de que se forme el enlace de manera aleatoria
	// float f_K; // Influencia social
	// float f_alfa; // Controversialidad de los temas
	// int i_N; // Número de agentes en la red
	// int i_T; // Cantidad de tópicos
	// int i_Mopi; // Máximo inicial de opiniones
	// float f_dt; // Paso temporal de iteración del sistema
// } s_Param;

// // Acá voy a declarar las funciones.------------------------------------

// double Random();
// int Visualizar_d(double *pd_vec);
// int Visualizar_f(float *pf_vec);
// int Visualizar_i(int *pi_vec);
// int GenerarOpi(s_Red var, s_Param par);
// int GenerarAng(s_Red var);
// int GenerarAdy(s_Red var,s_Param par);
// double Din1(s_Red var, s_Param par, int i_j);
// double Din2(s_Red var, s_Param par);
// double Duplicar(s_Red var, s_Param par);
// int RK4(double *pd_vec ,s_Red var, s_Param par, double (*fp_funcion)(s_Red var, s_Param par));



// /*####################################################################################
// ####################################################################################
// ####################################################################################
// ####################################################################################
// */


// // ---------------------------------------------------------------------------------------------------

// // Vamos a intentar ver como se leen archivos y data desde estos
// // Creo que lo más útil va a ser usar el fscanf porque mis datos están separados por tabulaciones
// // Acá está la forma de leer el archivo. Sólo necesitaría poder saber que tan largo es antes de
// // subirlo, pero creo que eso sería mucho pedir.

// int main(){
	// // Defino mis variables temporales para medir el tiempo que tarda el programa. También genero una nueva semilla
	// time_t tt_prin,tt_fin;
	// time(&tt_prin);
	// srand(time(NULL));
	// int i_tardanza;
	
	
	// // Defino los nombres de mis structs en este programa y los valores de los parámetros
	// s_Red red;
	// s_Param datos;
	
	// datos.f_Beta = 0.5;
	// datos.f_Pint = 0.5;
	// datos.f_K = 0.5;
	// datos.f_alfa = 2;
	// datos.i_N = 3;
	// datos.i_T = 3;
	// datos.i_Mopi = 3;
	// datos.f_dt = 0.2;
	
	// // Defino el puntero a mi función y lo inicializo
	// double (*pf_Dup)(s_Red Red, s_Param Parametros) = &Duplicar;	
	
	// // Asigno memoria a mis matrices y las inicializo
	
	// // Matriz de Vectores de opinión. Tiene tamaño N*T
	// red.pd_Opi = (double*) malloc((datos.i_N*datos.i_T+2)*sizeof(double)); // Asigno espacio de memoria al vector
	// for(register int i_i=0; i_i<datos.i_N*datos.i_T+2; i_i++) red.pd_Opi[i_i] = 0; // Inicializo la matriz para que no haya "basura" en alguna posición
	// red.pd_Opi[0] = datos.i_N; // Guardo el número de filas en la primer coordenada del vector
	// red.pd_Opi[1] = datos.i_T; // Guardo el número de Columnas en la segunda coordenada del vector
	// GenerarOpi(red,datos); // Genero la red de Vectores de opinión propiamente dicha.

	// // Matriz de Superposición. Tiene tamaño T*T
	// red.pd_Ang = (double*) malloc((datos.i_T*datos.i_T+2)*sizeof(double)); // Asigno espacio de memoria al vector
	// for(register int i_i=0; i_i<datos.i_T*datos.i_T+2; i_i++) red.pd_Ang[i_i] = 0; // Inicializo la matriz para que no haya "basura" en alguna posición
	// red.pd_Ang[0] = datos.i_T; // Guardo el número de filas en la primer coordenada del vector
	// red.pd_Ang[1] = datos.i_T; // Guardo el número de Columnas en la segunda coordenada del vector
	// GenerarAng(red); // Genero la red de Vectores de opinión propiamente dicha.
	
	// // Matriz de Adyacencia. Tiene tamaño N*N
	// red.pi_Ady = (int*) malloc((datos.i_N*datos.i_N+2)*sizeof(int)); // Asigno espacio de memoria al vector
	// for(register int i_i=0; i_i<datos.i_N*datos.i_N+2; i_i++) red.pi_Ady[i_i] = 0; // Inicializo la matriz para que no haya "basura" en alguna posición
	// red.pi_Ady[0] = datos.i_N; // Guardo el número de filas en la primer coordenada del vector
	// red.pi_Ady[1] = datos.i_N; // Guardo el número de columnas en la segunda coordenada del vector
	// GenerarAdy(red,datos); // Genero la red de Adyacencia propiamente dicha.
	
	// // Aplico el RK4
	// RK4(red.pd_Opi, red, datos, pf_Dup);
	
	
	// // Ejecuto los comandos finales para medir el tiempo y liberar memoria
	// free(red.pi_Ady);
	// free(red.pd_Ang);
	// free(red.pd_Opi);
	// time(&tt_fin);
	// i_tardanza = tt_fin-tt_prin;
	// printf("Tarde %d segundos en terminar\n",i_tardanza);
	// return 0;
// }

// /*####################################################################################
// ####################################################################################
// ####################################################################################
// ####################################################################################
// */

// // De acá en adelante van las funciones a declarar

// // Esta función me genera un número random
// double Random(){
	// return ((double) rand()/(double) RAND_MAX);
// }


// // Estas son las funciones de Inicialización.
// // #########################################################################################################


// // Esta función es para observar los vectores double
// int Visualizar_d(double *pd_vec){
	// // Defino las variables que voy a necesitar.
	// int i_F,i_C;
	// i_F = *pd_vec;
	// i_C = *(pd_vec+1);
	
	// // Printeo mi vector
	// for(register int i_i=0; i_i<i_F; i_i++){
		// for(register int i_j=0; i_j<i_C; i_j++) printf("%lf\t",*(pd_vec+i_i*i_C+i_j+2));
		// printf("\n");
	// }
	// printf("\n");
	
	// return 0;
// }

// // Esta función es para observar los vectores float
// int Visualizar_f(float *pf_vec){
	// // Defino las variables que voy a necesitar.
	// int i_F,i_C;
	// i_F = *pf_vec;
	// i_C = *(pf_vec+1);
	
	// // Printeo mi vector
	// for(register int i_i=0; i_i<i_F; i_i++){
		// for(register int i_j=0; i_j<i_C; i_j++) printf("%lf\t",*(pf_vec+i_i*i_C+i_j+2));
		// printf("\n");
	// }
	// printf("\n");
	
	// return 0;
// }

// // Esta función es para observar los vectores int
// int Visualizar_i(int *pi_vec){
	// // Defino las variables que voy a necesitar.
	// int i_F,i_C;
	// i_F = *pi_vec;
	// i_C = *(pi_vec+1);
	
	// // Printeo mi vector
	// for(register int i_i=0; i_i<i_F; i_i++){
		// for(register int i_j=0; i_j<i_C; i_j++) printf("%d\t",*(pi_vec+i_i*i_C+i_j+2));
		// printf("\n");
	// }
	// printf("\n");
	
	// return 0;
// }




// // Esta función me genera los vectores opinión iniciales del sistema. Esto es una matriz de tamaño N*T
// int GenerarOpi(s_Red var, s_Param par){
	// // Obtengo las dimensiones de la "matriz" de opiniones de mis agentes.
	// int i_Filas,i_Columnas;
	// i_Filas = (int) var.pd_Opi[0];
	// i_Columnas = (int) var.pd_Opi[1];
	
	// // Inicializo la "matriz" de opiniones de mis agentes.
	// for(int i_i=0;i_i<i_Filas*i_Columnas;i_i++) var.pd_Opi[i_i+2] = par.i_Mopi*(Random()-0.5)*2;
	// return 0;
// }

// // Esta función me genera la matriz de Superposicion del sistema. Esto es una matriz de T*T
// int GenerarAng(s_Red var){
	// // Obtengo las dimensiones de la matriz de Superposicion.
	// int i_Filas,i_Columnas;
	// i_Filas = (int) var.pd_Ang[0];
	// i_Columnas = (int) var.pd_Ang[1];
	
	// // Inicializo la matriz de Superposicion de mi sistema.
	// for(int i_i=0; i_i<i_Filas; i_i++) for(int i_j=0; i_j<i_i; i_j++) var.pd_Ang[i_i*i_Columnas+i_j+2] = 0.5; // Decidí poner 0.5 entre todos los tópicos de mi modelo
	// for(int i_i=0; i_i<i_Filas; i_i++) var.pd_Ang[i_i*i_Columnas+i_i+2] = 1; // Esto me pone 1 en toda la diagonal
	// for(int i_i=0; i_i<i_Filas; i_i++) for(int i_j=i_i+1; i_j<i_Columnas; i_j++) var.pd_Ang[i_i*i_Columnas+i_j+2] = var.pd_Ang[i_j*i_Columnas+i_i+2]; // Esta sola línea simetriza la matriz
	// return 0;
// }


// // Esta función me inicializa la matriz de Adyacencia. Esto es una matriz de N*N
// int GenerarAdy(s_Red var, s_Param par){
	// // Obtengo las dimensiones de la matriz de Adyacencia.
	// int i_Filas,i_Columnas;
	// i_Filas = (int) var.pi_Ady[0];
	// i_Columnas = (int) var.pi_Ady[1];
	
	// // Inicializo la matriz de Adyacencia de mi sistema
	// for(int i_i=0; i_i<i_Filas; i_i++) {
		// for(int i_j=0; i_j<i_i; i_j++) {
			// // Saco un número random y veo si asigno un 1 o un 0 a esa posición-
			// if(Random()<par.f_Pint) var.pi_Ady[i_i*i_Columnas+i_j+2] = 1;
			// else var.pi_Ady[i_i*i_Columnas+i_j+2] = 0;
		// }
	// }
	// for(int i_i=0; i_i<i_Filas; i_i++) for(int i_j=i_i+1; i_j<i_Columnas; i_j++) var.pi_Ady[i_i*i_Columnas+i_j+2] = var.pi_Ady[i_j*i_Columnas+i_i+2]; // Esta sola línea simetriza la matriz
	// // for(int i=0; i<par.N; i++) var.Ady[i*par.N+i] = 1; // Esto me pone 1 en toda la diagonal
	// return 0;
// }

// // #####################################################################################

// // Estas son las funciones del avance
// // #######################################################################################

// // Esta función resuelve un término de los de la sumatoria.
// double Din1(s_Red var, s_Param par,int i_j){
	
	// // Defino las variables locales de mi función. d_resultados es el return. 
	// // d_opiniones_superpuestas es el producto de la matriz de superposición de tópicos con el vector opinión de un agente.
	// double d_resultado,d_opiniones_superpuestas = 0;
	
	// // Obtengo el tamaño de columnas de mis tres matrices
	// int i_Co,i_Cs,i_Ca;
	// i_Co = (int) var.pd_Opi[1];
	// i_Cs = (int) var.pd_Ang[1];
	// i_Ca = var.pi_Ady[1];
	
	// for(register int i_p=0; i_p<i_Cs; i_p++) d_opiniones_superpuestas += var.pd_Ang[var.i_topico*i_Cs+i_p+2]*var.pd_Opi[i_j*i_Co+i_p+2]; // Calculo previamente este producto de la matriz con el vector.
	// d_resultado = var.pi_Ady[var.i_agente*i_Ca+i_j+2]*tanh(par.f_alfa*d_opiniones_superpuestas); // Esto es lo que está dentro de la sumatoria en la ecuación dinámica.
	// return d_resultado; // La función devuelve el número que buscás, no te lo asigna en una variable.
// }

// // Esta es la segunda parte de la ecuación dinámica, con esto puedo realizar una iteración del sistema.
// double Din2(s_Red var, s_Param par){
	
	// // Defino las variables locales de mi función. d_resultado es lo que voy a returnear.
	// // d_sumatoria es el total de la sumatoria del segundo término de la ecuación diferencial.
	// double d_resultado,d_sumatoria=0;
	
	// // Calculo la sumatoria de la ecuación diferencial. Para esto es que existe la función Din1.
	// for(register int i_j=0; i_j<var.i_agente; i_j++) d_sumatoria += Din1(var,par,i_j);
	// for(register int i_j=var.i_agente+1; i_j<par.i_N; i_j++) d_sumatoria += Din1(var,par,i_j);
	
	// // Obtengo el tamaño de Columnas de mi matriz de Vectores de opinión y calculo el valor del campo que define mi ecuación diferencial
	// int i_Columnas = (int) var.pd_Opi[1];
	// d_resultado = -var.pd_Opi[var.i_agente*i_Columnas+var.i_topico+2]+par.f_K*d_sumatoria;
	// return d_resultado;
// }

// // #######################################################################################


// // Esta función me realiza una iteración del sistema a partir de un RK4.
// // Creo que no hay forma de que esta función sea 100% general para cualquier caso.
// // Incluso creo que no es necesario el uso del puntero de funciones, pero quiero aprender a usarlo
// int RK4(double *pd_vec ,s_Red var, s_Param par, double (*fp_funcion)(s_Red var, s_Param par)){
	// // Defino las variables y vectores que voy a necesitar
	// int i_filas = (int) *pd_vec; // Este es el número de filas del vector principal
	// int i_columnas = (int) *(pd_vec+1); // Este es el número de columnas del vector principal
	// double *pd_pendientes[5]; // Este array de punteros guarda los punteros kN
	// float DT[4]; // Esto me ayuda a meter el paso temporal que se usa para calcular cada pendiente.
	
	
	// // Voy a armar vectores con las pendientes que calcule, para luego calcular el avance de todas las variables al final
	// double *k0;
	// k0 = (double*) malloc((i_filas*i_columnas+2)*sizeof(double));
	
	// double *k1;
	// k1 = (double*) malloc((i_filas*i_columnas+2)*sizeof(double));
	
	// double *k2;
	// k2 = (double*) malloc((i_filas*i_columnas+2)*sizeof(double));
	
	// double *k3;
	// k3 = (double*) malloc((i_filas*i_columnas+2)*sizeof(double));
	
	// double *k4;
	// k4 = (double*) malloc((i_filas*i_columnas+2)*sizeof(double));
	
	// double *pd_inicial; // Este me guarda las condiciones iniciales del vector, que las voy a necesitar al calcular cada paso del RK4
	// pd_inicial = (double*) malloc((i_filas*i_columnas+2)*sizeof(double));
	
	// // Inicializo mis punteros
	// pd_pendientes[0] = k0;
	// pd_pendientes[1] = k1;
	// pd_pendientes[2] = k2;
	// pd_pendientes[3] = k3;
	// pd_pendientes[4] = k4;
	// for(register int i_i=0; i_i<i_filas*i_columnas+2; i_i++){
		// *(pd_inicial+i_i) = *(pd_vec+i_i);
		// for(register int i_j=0; i_j<5;i_j++) *(pd_pendientes[i_j]+i_i) = 0; // De esta manera inicializo los 5 punteros, todos en una sola línea.
	// }
	
	// // Guardo registro del tamaño de mis vectores k
	// for(register int i_j=0; i_j<5;i_j++) *(pd_pendientes[i_j]) = i_filas;
	// for(register int i_j=0; i_j<5;i_j++) *(pd_pendientes[i_j]+1) = i_columnas;
	
	// // Armo mi vector DT. Este hay que armarlo uno por uno, si o si.
	// DT[0] = 0;
	// DT[1] = par.f_dt*0.5;
	// DT[2] = par.f_dt*0.5;
	// DT[3] = par.f_dt;
		
	// // Acá hago las iteraciones del RK4 para hallar las pendientes k
	// for(register int i_j=0; i_j<4; i_j++){ // Esto itera para mis 4 k
		// for(var.i_agente=0; var.i_agente<*pd_vec; var.i_agente++){ // Itero para todos los agentes
			// for(var.i_topico=0; var.i_topico<*(pd_vec+1); var.i_topico++){ // Itero para todos los tópicos
				// // Calculo el elemento de la pendiente k(i_j+1)
				// for(register int i_i=0; i_i<i_filas*i_columnas; i_i++) *(pd_vec+i_i+2) = *(pd_inicial+i_i+2)+*(pd_pendientes[i_j]+i_i+2)*DT[i_j];
				// *(pd_pendientes[i_j+1]+var.i_agente*i_columnas+var.i_topico+2) = (*fp_funcion)(var,par);
			// }
		// }
	// }
	
	// // Con TODAS las pendientes calculadas, ahora sí avanzo temporalmente mi sistema
	
	// for(register int i_i=0; i_i<i_filas*i_columnas; i_i++){
	// *(pd_vec+i_i+2) = *(pd_inicial+i_i+2)+(par.f_dt/6)*(*(pd_pendientes[1]+i_i+2)+*(pd_pendientes[2]+i_i+2)*2+*(pd_pendientes[3]+i_i+2)*2+*(pd_pendientes[4]+i_i+2));
	// }
	
	// // Ahora hagamos algún mecanismo de visualización, para ver que todo esté correctamente calculado. Dios que esto va a ser un bardo.
	// // Primero visualicemos las pendientes. Para eso voy a armar unos strings que poner en el printeo
	
	// char c_npendientes[] = "k1234"; //
	
	// for(register int i_i=0; i_i<4; i_i++){
		// printf("\n Estas son las pendientes %c%c \n",c_npendientes[0],c_npendientes[i_i+1]);
		// Visualizar_d(pd_pendientes[i_i+1]);
	// }
	
	// // También tengo que visualizar mi vector trabajado.
	
	// printf("Este es mi vector antes de evolucionarlo \n");
	// Visualizar_d(pd_inicial);
	
	// printf("Este es mi vector luego de evolucionarlo \n");
	// Visualizar_d(pd_vec);
	

	// // Libero el espacio de memoria asignado a los punteros de las pendientes y al pd_inicial
	// free(pd_inicial);
	// for(int register i_i=0; i_i<5; i_i++) free(pd_pendientes[i_i]);
	
	// return 0;
// }

// // Esta es una función 
// double Duplicar(s_Red var, s_Param par){
	// // Defino mi variable a usar
	// double doble;
	// int i_Columnas = var.pd_Opi[1];
	
	// // Esta ecuación diferencial me define las pendientes como el doble del valor actual.
	// doble = 5*var.pd_Opi[var.i_agente*i_Columnas+var.i_topico+2];
		
	// return doble;
// }

//-----------------------------------------------------------------------------------
//-----------------------------------------------------------------------------------
//-----------------------------------------------------------------------------------

NUEVO_PROGRAMA

30/12/2020

Este programa lo hice hace unos días, lo hice para poder probar cómo se hacía para
guardar los datos que el programa iba calculando en un archivo externo. Tuve que
usar el puntero a un FILE, fopen, scanf, fprintf y fclose. Lo interesante es
que por algún motivo que desconozco, el programa ahora tiene el problema de que
no me permite ponerle a los archivos la extensión txt. Por algún motivo que desconozco,
ya eso no lo acepta. Igual a Python no le afecta que sean txt o no, así que eso por
no es un problema. También aproveché para crear unas funciones que reciben
un vector int o un vector double y el puntero al archivo y con eso te escriben
el vector en tu archivo.





// #include<stdio.h>
// #include<stdlib.h>
// #include<math.h>
// #include<time.h>

// // Acá vienen los structs.
// // El struct Red tiene los datos que definen mi red, y la info de la red
// typedef struct Red{
	// double *pd_Ang; // Matriz de superposición entre tópicos. Tiene tamaño T*T
	// int *pi_Ady; // Matriz de adyacencia que define mis conexiones. Tiene tamaño N*N
	// double *pd_Opi; // Vector de opinión de cada individuo
	// int i_agente; // Entero que representa el agente que estoy mirando. Es un valor que va entre 0 y N-1
	// int i_topico; // Entero que representa el tópico que estoy mirando. Es un valor que va entre 0 y T-1
// } s_Red;

// typedef struct Parametros{
	// float f_Beta; // Exponente que regula el grado de homofilia
	// float f_Pint; // Probabilidad de que se forme el enlace de manera aleatoria
	// float f_K; // Influencia social
	// float f_alfa; // Controversialidad de los temas
	// int i_N; // Número de agentes en la red
	// int i_T; // Cantidad de tópicos
	// int i_Mopi; // Máximo inicial de opiniones
	// float f_dt; // Paso temporal de iteración del sistema
// } s_Param;

// // Acá voy a declarar las funciones.------------------------------------

// double Random();
// int Visualizar_d(double *pd_vec);
// int Visualizar_f(float *pf_vec);
// int Visualizar_i(int *pi_vec);
// int GenerarOpi(s_Red var, s_Param par);
// int GenerarAng(s_Red var);
// int GenerarAdy(s_Red var,s_Param par);
// double Din1(s_Red var, s_Param par, int i_j);
// double Din2(s_Red var, s_Param par);
// int Escribir_d(double *pd_vec, FILE *pa_archivo);
// int Escribir_i(int *pi_vec, FILE *pa_archivo);
// int RK4(double *pd_vec ,s_Red var, s_Param par, double (*fp_funcion)(s_Red var, s_Param par));



// /*####################################################################################
// ####################################################################################
// ####################################################################################
// ####################################################################################
// */


// // ---------------------------------------------------------------------------------------------------

// // Vamos a intentar ver como se leen archivos y data desde estos
// // Creo que lo más útil va a ser usar el fscanf porque mis datos están separados por tabulaciones
// // Acá está la forma de leer el archivo. Sólo necesitaría poder saber que tan largo es antes de
// // subirlo, pero creo que eso sería mucho pedir.

// int main(){
	// // Defino mis variables temporales para medir el tiempo que tarda el programa. También genero una nueva semilla
	// time_t tt_prin,tt_fin;
	// time(&tt_prin);
	// srand(time(NULL));
	// int i_tardanza;
		
	// // Defino los nombres de mis structs en este programa y los valores de los parámetros
	// s_Red red;
	// s_Param datos;
	
	// datos.f_Beta = 0.5;
	// datos.f_Pint = 0.5;
	// datos.f_K = 0.5;
	// datos.f_alfa = 2;
	// datos.i_N = 50;
	// datos.i_T = 2;
	// datos.i_Mopi = 3;
	// datos.f_dt = 0.2;
	
	// // Defino el puntero a mi función y lo inicializo
	// double (*pf_Dup)(s_Red Red, s_Param Parametros) = &Din2;	
	
	// // Asigno memoria a mis matrices y las inicializo
	
	// // Matriz de Vectores de opinión. Tiene tamaño N*T
	// red.pd_Opi = (double*) malloc((datos.i_N*datos.i_T+2)*sizeof(double)); // Asigno espacio de memoria al vector
	// for(register int i_i=0; i_i<datos.i_N*datos.i_T+2; i_i++) red.pd_Opi[i_i] = 0; // Inicializo la matriz para que no haya "basura" en alguna posición
	// red.pd_Opi[0] = datos.i_N; // Guardo el número de filas en la primer coordenada del vector
	// red.pd_Opi[1] = datos.i_T; // Guardo el número de Columnas en la segunda coordenada del vector
	// GenerarOpi(red,datos); // Genero la red de Vectores de opinión propiamente dicha.

	// // Matriz de Superposición. Tiene tamaño T*T
	// red.pd_Ang = (double*) malloc((datos.i_T*datos.i_T+2)*sizeof(double)); // Asigno espacio de memoria al vector
	// for(register int i_i=0; i_i<datos.i_T*datos.i_T+2; i_i++) red.pd_Ang[i_i] = 0; // Inicializo la matriz para que no haya "basura" en alguna posición
	// red.pd_Ang[0] = datos.i_T; // Guardo el número de filas en la primer coordenada del vector
	// red.pd_Ang[1] = datos.i_T; // Guardo el número de Columnas en la segunda coordenada del vector
	// GenerarAng(red); // Genero la red de Vectores de opinión propiamente dicha.
	
	// // Matriz de Adyacencia. Tiene tamaño N*N
	// red.pi_Ady = (int*) malloc((datos.i_N*datos.i_N+2)*sizeof(int)); // Asigno espacio de memoria al vector
	// for(register int i_i=0; i_i<datos.i_N*datos.i_N+2; i_i++) red.pi_Ady[i_i] = 0; // Inicializo la matriz para que no haya "basura" en alguna posición
	// red.pi_Ady[0] = datos.i_N; // Guardo el número de filas en la primer coordenada del vector
	// red.pi_Ady[1] = datos.i_N; // Guardo el número de columnas en la segunda coordenada del vector
	// GenerarAdy(red,datos); // Genero la red de Adyacencia propiamente dicha.
	
	// // Defino las variables para mi archivo.txt que guarda los datos del sistema
	// char filename[255]; // Siempre lo hago lo más grande posible. Si sobra no es problema.
	// sprintf(filename,"Datos_Evolucion_Opinion_N=%d_T=%d",datos.i_N,datos.i_T); // Uso esto para asignarle el nombre a mi archivo.
	// FILE *pa_txt=fopen(filename,"w"); //Esto me crea un archivo con nombre filename y permiso de escritura. Es a partir del puntero pa_txt que accedo al archivo.
	
	// // Copio en el archivo mi matriz de Adyacencia
	// Escribir_i(red.pi_Ady, pa_txt);
	
	// // Copio en el archivo mi matriz de Superposicion
	// Escribir_d(red.pd_Ang, pa_txt);
	
	// // Copio en el archivo mis vectores de opinion
	// Escribir_d(red.pd_Opi, pa_txt);	
	
	// // Evoluciono mi sistema y luego voy guardando los datos.
	// for(register int i_p=0; i_p<20; i_p++){
		// RK4(red.pd_Opi, red, datos, pf_Dup);
		// Escribir_d(red.pd_Opi, pa_txt);
	// }
		
	// // Ejecuto los comandos finales para medir el tiempo y liberar memoria
	// fclose(pa_txt); // Con esto cierro mi archivo
	// free(red.pi_Ady);
	// free(red.pd_Ang);
	// free(red.pd_Opi);
	// time(&tt_fin);
	// i_tardanza = tt_fin-tt_prin;
	// printf("Tarde %d segundos en terminar\n",i_tardanza);
	// return 0;
// }

// /*####################################################################################
// ####################################################################################
// ####################################################################################
// ####################################################################################
// */

// // De acá en adelante van las funciones a declarar

// // Esta función me genera un número random
// double Random(){
	// return ((double) rand()/(double) RAND_MAX);
// }


// // Estas son las funciones de Inicialización.
// // #########################################################################################################


// // Esta función es para observar los vectores double
// int Visualizar_d(double *pd_vec){
	// // Defino las variables que voy a necesitar.
	// int i_F,i_C;
	// i_F = *pd_vec;
	// i_C = *(pd_vec+1);
	
	// // Printeo mi vector
	// for(register int i_i=0; i_i<i_F; i_i++){
		// for(register int i_j=0; i_j<i_C; i_j++) printf("%lf\t",*(pd_vec+i_i*i_C+i_j+2));
		// printf("\n");
	// }
	// printf("\n");
	
	// return 0;
// }

// // Esta función es para observar los vectores float
// int Visualizar_f(float *pf_vec){
	// // Defino las variables que voy a necesitar.
	// int i_F,i_C;
	// i_F = *pf_vec;
	// i_C = *(pf_vec+1);
	
	// // Printeo mi vector
	// for(register int i_i=0; i_i<i_F; i_i++){
		// for(register int i_j=0; i_j<i_C; i_j++) printf("%lf\t",*(pf_vec+i_i*i_C+i_j+2));
		// printf("\n");
	// }
	// printf("\n");
	
	// return 0;
// }

// // Esta función es para observar los vectores int
// int Visualizar_i(int *pi_vec){
	// // Defino las variables que voy a necesitar.
	// int i_F,i_C;
	// i_F = *pi_vec;
	// i_C = *(pi_vec+1);
	
	// // Printeo mi vector
	// for(register int i_i=0; i_i<i_F; i_i++){
		// for(register int i_j=0; i_j<i_C; i_j++) printf("%d\t",*(pi_vec+i_i*i_C+i_j+2));
		// printf("\n");
	// }
	// printf("\n");
	
	// return 0;
// }




// // Esta función me genera los vectores opinión iniciales del sistema. Esto es una matriz de tamaño N*T
// int GenerarOpi(s_Red var, s_Param par){
	// // Obtengo las dimensiones de la "matriz" de opiniones de mis agentes.
	// int i_Filas,i_Columnas;
	// i_Filas = (int) var.pd_Opi[0];
	// i_Columnas = (int) var.pd_Opi[1];
	
	// // Inicializo la "matriz" de opiniones de mis agentes.
	// for(int i_i=0;i_i<i_Filas*i_Columnas;i_i++) var.pd_Opi[i_i+2] = par.i_Mopi*(Random()-0.5)*2;
	// return 0;
// }

// // Esta función me genera la matriz de Superposicion del sistema. Esto es una matriz de T*T
// int GenerarAng(s_Red var){
	// // Obtengo las dimensiones de la matriz de Superposicion.
	// int i_Filas,i_Columnas;
	// i_Filas = (int) var.pd_Ang[0];
	// i_Columnas = (int) var.pd_Ang[1];
	
	// // Inicializo la matriz de Superposicion de mi sistema.
	// for(int i_i=0; i_i<i_Filas; i_i++) for(int i_j=0; i_j<i_i; i_j++) var.pd_Ang[i_i*i_Columnas+i_j+2] = 0.5; // Decidí poner 0.5 entre todos los tópicos de mi modelo
	// for(int i_i=0; i_i<i_Filas; i_i++) var.pd_Ang[i_i*i_Columnas+i_i+2] = 1; // Esto me pone 1 en toda la diagonal
	// for(int i_i=0; i_i<i_Filas; i_i++) for(int i_j=i_i+1; i_j<i_Columnas; i_j++) var.pd_Ang[i_i*i_Columnas+i_j+2] = var.pd_Ang[i_j*i_Columnas+i_i+2]; // Esta sola línea simetriza la matriz
	// return 0;
// }


// // Esta función me inicializa la matriz de Adyacencia. Esto es una matriz de N*N
// int GenerarAdy(s_Red var, s_Param par){
	// // Obtengo las dimensiones de la matriz de Adyacencia.
	// int i_Filas,i_Columnas;
	// i_Filas = (int) var.pi_Ady[0];
	// i_Columnas = (int) var.pi_Ady[1];
	
	// // Inicializo la matriz de Adyacencia de mi sistema
	// for(int i_i=0; i_i<i_Filas; i_i++) {
		// for(int i_j=0; i_j<i_i; i_j++) {
			// // Saco un número random y veo si asigno un 1 o un 0 a esa posición-
			// if(Random()<par.f_Pint) var.pi_Ady[i_i*i_Columnas+i_j+2] = 1;
			// else var.pi_Ady[i_i*i_Columnas+i_j+2] = 0;
		// }
	// }
	// for(int i_i=0; i_i<i_Filas; i_i++) for(int i_j=i_i+1; i_j<i_Columnas; i_j++) var.pi_Ady[i_i*i_Columnas+i_j+2] = var.pi_Ady[i_j*i_Columnas+i_i+2]; // Esta sola línea simetriza la matriz
	// // for(int i=0; i<par.N; i++) var.Ady[i*par.N+i] = 1; // Esto me pone 1 en toda la diagonal
	// return 0;
// }

// // #####################################################################################

// // Estas son las funciones del avance
// // #######################################################################################

// // Esta función resuelve un término de los de la sumatoria.
// double Din1(s_Red var, s_Param par,int i_j){
	
	// // Defino las variables locales de mi función. d_resultados es el return. 
	// // d_opiniones_superpuestas es el producto de la matriz de superposición de tópicos con el vector opinión de un agente.
	// double d_resultado,d_opiniones_superpuestas = 0;
	
	// // Obtengo el tamaño de columnas de mis tres matrices
	// int i_Co,i_Cs,i_Ca;
	// i_Co = (int) var.pd_Opi[1];
	// i_Cs = (int) var.pd_Ang[1];
	// i_Ca = var.pi_Ady[1];
	
	// for(register int i_p=0; i_p<i_Cs; i_p++) d_opiniones_superpuestas += var.pd_Ang[var.i_topico*i_Cs+i_p+2]*var.pd_Opi[i_j*i_Co+i_p+2]; // Calculo previamente este producto de la matriz con el vector.
	// d_resultado = var.pi_Ady[var.i_agente*i_Ca+i_j+2]*tanh(par.f_alfa*d_opiniones_superpuestas); // Esto es lo que está dentro de la sumatoria en la ecuación dinámica.
	// return d_resultado; // La función devuelve el número que buscás, no te lo asigna en una variable.
// }

// // Esta es la segunda parte de la ecuación dinámica, con esto puedo realizar una iteración del sistema.
// double Din2(s_Red var, s_Param par){
	
	// // Defino las variables locales de mi función. d_resultado es lo que voy a returnear.
	// // d_sumatoria es el total de la sumatoria del segundo término de la ecuación diferencial.
	// double d_resultado,d_sumatoria=0;
	
	// // Calculo la sumatoria de la ecuación diferencial. Para esto es que existe la función Din1.
	// for(register int i_j=0; i_j<var.i_agente; i_j++) d_sumatoria += Din1(var,par,i_j);
	// for(register int i_j=var.i_agente+1; i_j<par.i_N; i_j++) d_sumatoria += Din1(var,par,i_j);
	
	// // Obtengo el tamaño de Columnas de mi matriz de Vectores de opinión y calculo el valor del campo que define mi ecuación diferencial
	// int i_Columnas = (int) var.pd_Opi[1];
	// d_resultado = -var.pd_Opi[var.i_agente*i_Columnas+var.i_topico+2]+par.f_K*d_sumatoria;
	// return d_resultado;
// }

// // #######################################################################################


// // Esta función me realiza una iteración del sistema a partir de un RK4.
// // Incluso creo que no es necesario el uso del puntero de funciones, pero quiero aprender a usarlo
// int RK4(double *pd_vec ,s_Red var, s_Param par, double (*fp_funcion)(s_Red var, s_Param par)){
	// // Defino las variables y vectores que voy a necesitar
	// int i_filas = (int) *pd_vec; // Este es el número de filas del vector principal
	// int i_columnas = (int) *(pd_vec+1); // Este es el número de columnas del vector principal
	// double *pd_pendientes[5]; // Este array de punteros guarda los punteros kN
	// float DT[4]; // Esto me ayuda a meter el paso temporal que se usa para calcular cada pendiente.
	
	
	// // Voy a armar vectores con las pendientes que calcule, para luego calcular el avance de todas las variables al final
	// double *k0;
	// k0 = (double*) malloc((i_filas*i_columnas+2)*sizeof(double));
	
	// double *k1;
	// k1 = (double*) malloc((i_filas*i_columnas+2)*sizeof(double));
	
	// double *k2;
	// k2 = (double*) malloc((i_filas*i_columnas+2)*sizeof(double));
	
	// double *k3;
	// k3 = (double*) malloc((i_filas*i_columnas+2)*sizeof(double));
	
	// double *k4;
	// k4 = (double*) malloc((i_filas*i_columnas+2)*sizeof(double));
	
	// double *pd_inicial; // Este me guarda las condiciones iniciales del vector, que las voy a necesitar al calcular cada paso del RK4
	// pd_inicial = (double*) malloc((i_filas*i_columnas+2)*sizeof(double));
	
	// // Inicializo mis punteros
	// pd_pendientes[0] = k0;
	// pd_pendientes[1] = k1;
	// pd_pendientes[2] = k2;
	// pd_pendientes[3] = k3;
	// pd_pendientes[4] = k4;
	// for(register int i_i=0; i_i<i_filas*i_columnas+2; i_i++){
		// *(pd_inicial+i_i) = *(pd_vec+i_i);
		// for(register int i_j=0; i_j<5;i_j++) *(pd_pendientes[i_j]+i_i) = 0; // De esta manera inicializo los 5 punteros, todos en una sola línea.
	// }
	
	// // Guardo registro del tamaño de mis vectores k
	// for(register int i_j=0; i_j<5;i_j++) *(pd_pendientes[i_j]) = i_filas;
	// for(register int i_j=0; i_j<5;i_j++) *(pd_pendientes[i_j]+1) = i_columnas;
	
	// // Armo mi vector DT. Este hay que armarlo uno por uno, si o si.
	// DT[0] = 0;
	// DT[1] = par.f_dt*0.5;
	// DT[2] = par.f_dt*0.5;
	// DT[3] = par.f_dt;
		
	// // Acá hago las iteraciones del RK4 para hallar las pendientes k
	// for(register int i_j=0; i_j<4; i_j++){ // Esto itera para mis 4 k
		// for(var.i_agente=0; var.i_agente<*pd_vec; var.i_agente++){ // Itero para todos los agentes
			// for(var.i_topico=0; var.i_topico<*(pd_vec+1); var.i_topico++){ // Itero para todos los tópicos
				// // Calculo el elemento de la pendiente k(i_j+1)
				// for(register int i_i=0; i_i<i_filas*i_columnas; i_i++) *(pd_vec+i_i+2) = *(pd_inicial+i_i+2)+*(pd_pendientes[i_j]+i_i+2)*DT[i_j];
				// *(pd_pendientes[i_j+1]+var.i_agente*i_columnas+var.i_topico+2) = (*fp_funcion)(var,par);
			// }
		// }
	// }
	
	// // Con TODAS las pendientes calculadas, ahora sí avanzo temporalmente mi sistema
	// for(register int i_i=0; i_i<i_filas*i_columnas; i_i++){
	// *(pd_vec+i_i+2) = *(pd_inicial+i_i+2)+(par.f_dt/6)*(*(pd_pendientes[1]+i_i+2)+*(pd_pendientes[2]+i_i+2)*2+*(pd_pendientes[3]+i_i+2)*2+*(pd_pendientes[4]+i_i+2));
	// }
	
	// // Ahora hagamos algún mecanismo de visualización, para ver que todo esté correctamente calculado. Dios que esto va a ser un bardo.
	// // Primero visualicemos las pendientes. Para eso voy a armar unos strings que poner en el printeo
	
	// // char c_npendientes[] = "k1234"; //
	
	// // for(register int i_i=0; i_i<4; i_i++){
		// // printf("\n Estas son las pendientes %c%c \n",c_npendientes[0],c_npendientes[i_i+1]);
		// // Visualizar_d(pd_pendientes[i_i+1]);
	// // }
	
	// // También tengo que visualizar mi vector trabajado.
	
	// // printf("Este es mi vector antes de evolucionarlo \n");
	// // Visualizar_d(pd_inicial);
	
	// // printf("Este es mi vector luego de evolucionarlo \n");
	// // Visualizar_d(pd_vec);
	

	// // Libero el espacio de memoria asignado a los punteros de las pendientes y al pd_inicial
	// free(pd_inicial);
	// for(int register i_i=0; i_i<5; i_i++) free(pd_pendientes[i_i]);
	
	// return 0;
// }

// // Esta función va a recibir un vector double y va a escribir ese vector en mi archivo.
// int Escribir_d(double *pd_vec, FILE *pa_archivo){
	// // Defino las variables del tamaño de mi vector
	// int i_C,i_F;
	// i_F = *pd_vec;
	// i_C = *(pd_vec+1);
	
	// // Ahora printeo todo el vector en mi archivo
	// for(register int i_i=0; i_i<i_C*i_F; i_i++) fprintf(pa_archivo,"\t%lf",*(pd_vec+i_i+2));
	// fprintf(pa_archivo,"\n");
	
	// return 0;
// }

// // Esta función va a recibir un vector int y va a escribir ese vector en mi archivo.
// int Escribir_i(int *pi_vec, FILE *pa_archivo){
	// // Defino las variables del tamaño de mi vector
	// int i_C,i_F;
	// i_F = *pi_vec;
	// i_C = *(pi_vec+1);
	
	// // Ahora printeo todo el vector en mi archivo
	// for(register int i_i=0; i_i<i_C*i_F; i_i++) fprintf(pa_archivo,"\t%d",*(pi_vec+i_i+2));
	// fprintf(pa_archivo,"\n");
	
	// return 0;
// }



//-----------------------------------------------------------------------------------
//-----------------------------------------------------------------------------------
//-----------------------------------------------------------------------------------

NUEVO_PROGRAMA

Este programa lo terminé el 01/01/2021. Acá lo que hice fue modificar el RK4, la función Din2 y Din1.
El motivo es para poder realizar interacciones de agentes de a pares, en vez de hacerlos con todos los agentes
con los que tiene conexión. Además armé una nueva función llamada Iteración que comprime todos los for
y el proceso de selección del segundo agente para la evolución de cada sujeto. También agregué una nueva
variable en el struct de Red.
Recordá que antes de esta revisión la función Din1 recibía como input el segundo agente de interacción.
Ahora lo modifiqué para que ese agente se encuentre dentro del s_Red, como mencioné antes.

El RK4 está modificado ahora para que NO evolucione todo el vector que le pasas, sino que evolucione
sólamente una variable del vector. La variable a evolucionar tiene que ser definida por fuera del
RK4 ahora, lo cual es mejor en definitiva.


De paso, el proceso de selección del segundo agente lo hago con comparaciones a través de un while.
Este proceso puede realizar repeticiones innecesarias, si bien es un proceso muy corto. En caso de
tener tiempo, hay una función sin terminar al fondo de este código cuyo objetivo es poder seleccionar
un agente nuevo sin utilizar comparaciones, únicamente fors y algunos vectores. De ser necesario, se
podría intentar usar eso para modificar el proceso de selección y ahorrar algo de tiempo. No sé cuanto
se podría ahorrar igualmente. Esta mejora y otras más, se encuentran anotadas en el archivo de Optimización.txt


// #include<stdio.h>
// #include<stdlib.h>
// #include<math.h>
// #include<time.h>

// // Acá vienen los structs.
// // El struct Red tiene los datos que definen mi red, y la info de la red
// typedef struct Red{
	// double *pd_Ang; // Matriz de superposición entre tópicos. Tiene tamaño T*T
	// int *pi_Ady; // Matriz de adyacencia que define mis conexiones. Tiene tamaño N*N
	// double *pd_Opi; // Vector de opinión de cada individuo
	// int i_agente; // Entero que representa el agente que estoy mirando. Es un valor que va entre 0 y N-1
	// int i_topico; // Entero que representa el tópico que estoy mirando. Es un valor que va entre 0 y T-1
	// int i_agente2; // Este es el segundo agente con el cual se pone en contacto el primero.
// } s_Red;

// typedef struct Parametros{
	// float f_Beta; // Exponente que regula el grado de homofilia
	// float f_Pint; // Probabilidad de que se forme el enlace de manera aleatoria
	// float f_K; // Influencia social
	// float f_alfa; // Controversialidad de los temas
	// int i_N; // Número de agentes en la red
	// int i_T; // Cantidad de tópicos
	// int i_Mopi; // Máximo inicial de opiniones
	// float f_dt; // Paso temporal de iteración del sistema
// } s_Param;

// // Acá voy a declarar las funciones.------------------------------------

// double Random();
// int Visualizar_d(double *pd_vec);
// int Visualizar_f(float *pf_vec);
// int Visualizar_i(int *pi_vec);
// int GenerarOpi(s_Red var, s_Param par);
// int GenerarAng(s_Red var);
// int GenerarAdy(s_Red var,s_Param par);
// double Din1(s_Red var, s_Param par);
// double Din2(s_Red var, s_Param par);
// int Escribir_d(double *pd_vec, FILE *pa_archivo);
// int Escribir_i(int *pi_vec, FILE *pa_archivo);
// int RK4(double *pd_vec ,s_Red var, s_Param par, double (*fp_funcion)(s_Red var, s_Param par));
// double Multiplo(s_Red var, s_Param par);
// int Iteracion(s_Red var, s_Param par, double (*pf_Dinamica)(s_Red var, s_Param par));



// /*####################################################################################
// ####################################################################################
// ####################################################################################
// ####################################################################################
// */


// //---------------------------------------------------------------------------------------------------

// // Vamos a intentar ver como se leen archivos y data desde estos
// // Creo que lo más útil va a ser usar el fscanf porque mis datos están separados por tabulaciones
// // Acá está la forma de leer el archivo. Sólo necesitaría poder saber que tan largo es antes de
// // subirlo, pero creo que eso sería mucho pedir.

// int main(){
	// // Defino mis variables temporales para medir el tiempo que tarda el programa. También genero una nueva semilla
	// time_t tt_prin,tt_fin;
	// time(&tt_prin);
	// srand(time(NULL));
	// int i_tardanza;
		
	// // Defino los nombres de mis structs en este programa y los valores de los parámetros
	// s_Red red;
	// s_Param datos;
	
	// datos.f_Beta = 0.5;
	// datos.f_Pint = 0.5; // Ahora mismo este valor no está haciendo nada
	// datos.f_K = 5;
	// datos.f_alfa = 2;
	// datos.i_N = 20;
	// datos.i_T = 4;
	// datos.i_Mopi = 2;
	// datos.f_dt = 0.2;
	
	// // Defino el puntero a mi función y lo inicializo
	// double (*pf_Dinamica)(s_Red Red, s_Param Parametros) = &Din2;	
	
	// // Asigno memoria a mis matrices y las inicializo
	
	// // Matriz de Vectores de opinión. Tiene tamaño N*T
	// red.pd_Opi = (double*) malloc((datos.i_N*datos.i_T+2)*sizeof(double)); // Asigno espacio de memoria al vector
	// for(register int i_i=0; i_i<datos.i_N*datos.i_T+2; i_i++) red.pd_Opi[i_i] = 0; // Inicializo la matriz para que no haya "basura" en alguna posición
	// red.pd_Opi[0] = datos.i_N; // Guardo el número de filas en la primer coordenada del vector
	// red.pd_Opi[1] = datos.i_T; // Guardo el número de Columnas en la segunda coordenada del vector
	// GenerarOpi(red,datos); // Genero la red de Vectores de opinión propiamente dicha.

	// // Matriz de Superposición. Tiene tamaño T*T
	// red.pd_Ang = (double*) malloc((datos.i_T*datos.i_T+2)*sizeof(double)); // Asigno espacio de memoria al vector
	// for(register int i_i=0; i_i<datos.i_T*datos.i_T+2; i_i++) red.pd_Ang[i_i] = 0; // Inicializo la matriz para que no haya "basura" en alguna posición
	// red.pd_Ang[0] = datos.i_T; // Guardo el número de filas en la primer coordenada del vector
	// red.pd_Ang[1] = datos.i_T; // Guardo el número de Columnas en la segunda coordenada del vector
	// GenerarAng(red); // Genero la red de Vectores de opinión propiamente dicha.
	
	// // Matriz de Adyacencia. Tiene tamaño N*N
	// red.pi_Ady = (int*) malloc((datos.i_N*datos.i_N+2)*sizeof(int)); // Asigno espacio de memoria al vector
	// for(register int i_i=0; i_i<datos.i_N*datos.i_N+2; i_i++) red.pi_Ady[i_i] = 0; // Inicializo la matriz para que no haya "basura" en alguna posición
	// red.pi_Ady[0] = datos.i_N; // Guardo el número de filas en la primer coordenada del vector
	// red.pi_Ady[1] = datos.i_N; // Guardo el número de columnas en la segunda coordenada del vector
	// GenerarAdy(red,datos); // Genero la red de Adyacencia propiamente dicha.
	
	// // // Defino las variables para mi archivo.txt que guarda los datos del sistema
	// // char filename[255]; // Siempre lo hago lo más grande posible. Si sobra no es problema.
	// // sprintf(filename,"Datos_Evolucion_Opinion_N=%d_T=%d",datos.i_N,datos.i_T); // Uso esto para asignarle el nombre a mi archivo.
	// // FILE *pa_txt=fopen(filename,"w"); //Esto me crea un archivo con nombre filename y permiso de escritura. Es a partir del puntero pa_txt que accedo al archivo.
	
	// // // Copio en el archivo mi matriz de Adyacencia
	// // Escribir_i(red.pi_Ady, pa_txt);
	
	// // // Copio en el archivo mi matriz de Superposicion
	// // Escribir_d(red.pd_Ang, pa_txt);
	
	// // // Copio en el archivo mis vectores de opinion
	// // Escribir_d(red.pd_Opi, pa_txt);
	
	// printf("Este es mi sistema antes de evolucionarlo\n");
	// Visualizar_d(red.pd_Opi);
	
	// // Evoluciono mi sistema y luego voy guardando los datos.
	// for(register int i_i=0; i_i<5000; ++i_i) Iteracion(red,datos,pf_Dinamica);

	
	// printf("Este es mi sistema final\n");
	// Visualizar_d(red.pd_Opi);
	
	
	// // Ejecuto los comandos finales para medir el tiempo y liberar memoria
	// // fclose(pa_txt); // Con esto cierro mi archivo
	// free(red.pi_Ady);
	// free(red.pd_Ang);
	// free(red.pd_Opi);
	// time(&tt_fin);
	// i_tardanza = tt_fin-tt_prin;
	// printf("Tarde %d segundos en terminar\n",i_tardanza);
	// return 0;
// }

// /*####################################################################################
// ####################################################################################
// ####################################################################################
// ####################################################################################
// */

// // De acá en adelante van las funciones a declarar

// // Esta función me genera un número random
// double Random(){
	// return ((double) rand()/(double) RAND_MAX);
// }


// // Estas son las funciones de Inicialización.
// // #########################################################################################################


// // Esta función es para observar los vectores double
// int Visualizar_d(double *pd_vec){
	// // Defino las variables que voy a necesitar.
	// int i_F,i_C;
	// i_F = *pd_vec;
	// i_C = *(pd_vec+1);
	
	// // Printeo mi vector
	// for(register int i_i=0; i_i<i_F; i_i++){
		// for(register int i_j=0; i_j<i_C; i_j++) printf("%lf\t",*(pd_vec+i_i*i_C+i_j+2));
		// printf("\n");
	// }
	// printf("\n");
	
	// return 0;
// }

// // Esta función es para observar los vectores float
// int Visualizar_f(float *pf_vec){
	// // Defino las variables que voy a necesitar.
	// int i_F,i_C;
	// i_F = *pf_vec;
	// i_C = *(pf_vec+1);
	
	// // Printeo mi vector
	// for(register int i_i=0; i_i<i_F; i_i++){
		// for(register int i_j=0; i_j<i_C; i_j++) printf("%lf\t",*(pf_vec+i_i*i_C+i_j+2));
		// printf("\n");
	// }
	// printf("\n");
	
	// return 0;
// }

// // Esta función es para observar los vectores int
// int Visualizar_i(int *pi_vec){
	// // Defino las variables que voy a necesitar.
	// int i_F,i_C;
	// i_F = *pi_vec;
	// i_C = *(pi_vec+1);
	
	// // Printeo mi vector
	// for(register int i_i=0; i_i<i_F; i_i++){
		// for(register int i_j=0; i_j<i_C; i_j++) printf("%d\t",*(pi_vec+i_i*i_C+i_j+2));
		// printf("\n");
	// }
	// printf("\n");
	
	// return 0;
// }




// // Esta función me genera los vectores opinión iniciales del sistema. Esto es una matriz de tamaño N*T
// int GenerarOpi(s_Red var, s_Param par){
	// // Obtengo las dimensiones de la "matriz" de opiniones de mis agentes.
	// int i_Filas,i_Columnas;
	// i_Filas = (int) var.pd_Opi[0];
	// i_Columnas = (int) var.pd_Opi[1];
	
	// // Inicializo la "matriz" de opiniones de mis agentes.
	// for(int i_i=0;i_i<i_Filas*i_Columnas;i_i++) var.pd_Opi[i_i+2] = par.i_Mopi*(Random()-0.5)*2;
	// return 0;
// }

// // Esta función me genera la matriz de Superposicion del sistema. Esto es una matriz de T*T
// int GenerarAng(s_Red var){
	// // Obtengo las dimensiones de la matriz de Superposicion.
	// int i_Filas,i_Columnas;
	// i_Filas = (int) var.pd_Ang[0];
	// i_Columnas = (int) var.pd_Ang[1];
	
	// // Inicializo la matriz de Superposicion de mi sistema.
	// for(int i_i=0; i_i<i_Filas; i_i++) for(int i_j=0; i_j<i_i; i_j++) var.pd_Ang[i_i*i_Columnas+i_j+2] = 0.5*(((-i_i-i_j)%2)*2+1); // Decidí poner 0.5 entre todos los tópicos de mi modelo
	// for(int i_i=0; i_i<i_Filas; i_i++) var.pd_Ang[i_i*i_Columnas+i_i+2] = 1; // Esto me pone 1 en toda la diagonal
	// for(int i_i=0; i_i<i_Filas; i_i++) for(int i_j=i_i+1; i_j<i_Columnas; i_j++) var.pd_Ang[i_i*i_Columnas+i_j+2] = var.pd_Ang[i_j*i_Columnas+i_i+2]; // Esta sola línea simetriza la matriz
	// return 0;
// }


// // Esta función me inicializa la matriz de Adyacencia. Esto es una matriz de N*N
// int GenerarAdy(s_Red var, s_Param par){
	// // Obtengo las dimensiones de la matriz de Adyacencia.
	// int i_Filas,i_Columnas;
	// i_Filas = (int) var.pi_Ady[0];
	// i_Columnas = (int) var.pi_Ady[1];
	
	// // Inicializo la matriz de Adyacencia de mi sistema
	// for(int i_i=0; i_i<i_Filas; i_i++) {
		// for(int i_j=0; i_j<i_i; i_j++) {
			// // Saco un número random y veo si asigno un 1 o un 0 a esa posición-
			// if(Random()<par.f_Pint) var.pi_Ady[i_i*i_Columnas+i_j+2] = 1;
			// else var.pi_Ady[i_i*i_Columnas+i_j+2] = 0;
		// }
	// }
	// for(int i_i=0; i_i<i_Filas; i_i++) for(int i_j=i_i+1; i_j<i_Columnas; i_j++) var.pi_Ady[i_i*i_Columnas+i_j+2] = var.pi_Ady[i_j*i_Columnas+i_i+2]; // Esta sola línea simetriza la matriz
	// // for(int i=0; i<par.N; i++) var.Ady[i*par.N+i] = 1; // Esto me pone 1 en toda la diagonal
	// return 0;
// }

// // #####################################################################################

// // Estas son las funciones del avance
// //#######################################################################################

// // Esta función resuelve un término de los de la sumatoria.
// double Din1(s_Red var, s_Param par){
	// // Defino las variables locales de mi función. d_resultados es el return. 
	// // d_opiniones_superpuestas es el producto de la matriz de superposición de tópicos con el vector opinión de un agente.
	// double d_resultado,d_opiniones_superpuestas = 0;
	
	// // Obtengo el tamaño de columnas de mis tres matrices
	// int i_Co,i_Cs;
	// i_Co = (int) var.pd_Opi[1];
	// i_Cs = (int) var.pd_Ang[1];
	
	// for(register int i_p=0; i_p<i_Cs; i_p++) d_opiniones_superpuestas += var.pd_Ang[var.i_topico*i_Cs+i_p+2]*var.pd_Opi[var.i_agente2*i_Co+i_p+2]; // Calculo previamente este producto de la matriz con el vector.
	// d_resultado = tanh(par.f_alfa*d_opiniones_superpuestas); // Esto es lo que está dentro de la sumatoria en la ecuación dinámica.
	// return d_resultado; // La función devuelve el número que buscás, no te lo asigna en una variable.
// }

// // Esta es la segunda parte de la ecuación dinámica, con esto puedo realizar una iteración del sistema.
// double Din2(s_Red var, s_Param par){
	// // Defino las variables locales de mi función. d_resultado es lo que voy a returnear.
	// // d_sumatoria es el total de la sumatoria del segundo término de la ecuación diferencial.
	// double d_resultado,d_sumatoria=0;
	
	// // Calculo la sumatoria de la ecuación diferencial. Para esto es que existe la función Din1.
	// // La sumatoria es sobre un sólo agente ahora. La idea es ver que pasa cuando las interacciones se hacen de a pares de manera aleatoria
	// // El sujeto lo voy a definir por afuera de esta función, cosa de que cada iteración del RK4 no me lo cambie.
	// d_sumatoria += Din1(var,par);
	
	// // Obtengo el tamaño de Columnas de mi matriz de Vectores de opinión y calculo el valor del campo que define mi ecuación diferencial
	// int i_Columnas = (int) var.pd_Opi[1];
	// d_resultado = -var.pd_Opi[var.i_agente*i_Columnas+var.i_topico+2]+par.f_K*d_sumatoria;
	// return d_resultado;
// }

// //#######################################################################################


// // Esta función me realiza una iteración del sistema a partir de un RK4.
// // Incluso creo que no es necesario el uso del puntero de funciones, pero quiero aprender a usarlo
// int RK4(double *pd_sistema ,s_Red var, s_Param par, double (*fp_funcion)(s_Red var, s_Param par)){
	// // Defino las variables y vectores que voy a necesitar
	// int i_F = (int) *pd_sistema; // Este es el número de filas del vector principal
	// int i_C = (int) *(pd_sistema+1); // Este es el número de columnas del vector principal
	// float DT[4]; // Esto me ayuda a meter el paso temporal que se usa para calcular cada pendiente.
	
	// double *pd_inicial; // Este me guarda las condiciones iniciales del vector, que las voy a necesitar al calcular cada paso del RK4
	// pd_inicial = (double*) malloc((i_F*i_C+2)*sizeof(double));
	
	// double *pd_pendientes; // Este puntero de doubles me guarda todos los valores de las pendientes k
	// pd_pendientes = (double*) malloc((5+2)*sizeof(double));
	
	// // Inicializo mis punteros
	// for(register int i_i=0; i_i<i_F*i_C+2; i_i++) *(pd_inicial+i_i) = *(pd_sistema+i_i);
	
	// *pd_pendientes = 1;
	// *(pd_pendientes+1) = 5;
	// for(register int i_i=0; i_i<5;++i_i) *(pd_pendientes+i_i+2)=0;
	
	// // Armo mi vector DT. Este hay que armarlo uno por uno, si o si.
	// DT[0] = 0;
	// DT[1] = par.f_dt*0.5;
	// DT[2] = par.f_dt*0.5;
	// DT[3] = par.f_dt;
		
	// // Acá hago las iteraciones del RK4 para hallar las pendientes k
	// for(register int i_j=0; i_j<4; i_j++){ // Esto itera para mis 4 k
		// // Calculo el elemento de la pendiente k(i_j+1)
		// for(register int i_i=0; i_i<i_F*i_C; i_i++) *(pd_sistema+i_i+2) = *(pd_inicial+i_i+2)+*(pd_pendientes+i_j+2)*DT[i_j];
		// *(pd_pendientes+i_j+1+2) = (*fp_funcion)(var,par);
	// }
	
	// // Copio al sistema igual que el inicial para deshacer los cambios que hice en el vector principal al calcular los k
	// for(register int i_i=0; i_i<i_F*i_C; i_i++) *(pd_sistema+i_i+2) = *(pd_inicial+i_i+2);
	// // Ahora que tengo los 4 k calculados, avanzo al sujeto que quiero avanzar.
	// *(pd_sistema+var.i_agente*i_C+var.i_topico+2) = *(pd_inicial+var.i_agente*i_C+var.i_topico+2)+(par.f_dt/6)*(*(pd_pendientes+2)+*(pd_pendientes+3)*2+*(pd_pendientes+4)*2+*(pd_pendientes+5));
	
	
	// // Ahora hagamos algún mecanismo de visualización, para ver que todo esté correctamente calculado. Dios que esto va a ser un bardo.
	// // Primero visualicemos las pendientes. Para eso voy a armar unos strings que poner en el printeo
	
	// // printf("\n Estas son las pendientes\n");
	// // Visualizar_d(pd_pendientes);
	
	// // También tengo que visualizar mi vector trabajado.
	
	// // printf("Este es mi vector antes de evolucionarlo \n");
	// // Visualizar_d(pd_inicial);
	
	// // printf("Este es mi vector luego de evolucionarlo \n");
	// // Visualizar_d(pd_sistema);
	

	// // Libero el espacio de memoria asignado a los punteros de las pendientes y al pd_inicial
	// free(pd_inicial);
	// free(pd_pendientes);
	
	// return 0;
// }

// // Esta función va a recibir un vector double y va a escribir ese vector en mi archivo.
// int Escribir_d(double *pd_vec, FILE *pa_archivo){
	// // Defino las variables del tamaño de mi vector
	// int i_C,i_F;
	// i_F = *pd_vec;
	// i_C = *(pd_vec+1);
	
	// // Ahora printeo todo el vector en mi archivo
	// for(register int i_i=0; i_i<i_C*i_F; i_i++) fprintf(pa_archivo,"\t%lf",*(pd_vec+i_i+2));
	// fprintf(pa_archivo,"\n");
	
	// return 0;
// }

// // Esta función va a recibir un vector int y va a escribir ese vector en mi archivo.
// int Escribir_i(int *pi_vec, FILE *pa_archivo){
	// // Defino las variables del tamaño de mi vector
	// int i_C,i_F;
	// i_F = *pi_vec;
	// i_C = *(pi_vec+1);
	
	// // Ahora printeo todo el vector en mi archivo
	// for(register int i_i=0; i_i<i_C*i_F; i_i++) fprintf(pa_archivo,"\t%d",*(pi_vec+i_i+2));
	// fprintf(pa_archivo,"\n");
	
	// return 0;
// }


// // Esta es una función define la ecuación deiferencial como un múltiplo del valor actual
// double Multiplo(s_Red var, s_Param par){
	// // Defino mis variables a usar
	// int i_C;
	// i_C = var.pd_Opi[1];
	// double multiplo;
	
	// // Esta ecuación diferencial me define las pendientes como el doble del valor actual.
	// multiplo = 2*var.pd_Opi[var.i_agente*i_C+var.i_topico+2];
	
	// return multiplo;
// }


// // Esta función me itera todo el sistema. Está buena para simplemente reemplazarla en el main.
// int Iteracion(s_Red var, s_Param par, double (*pf_Dinamica)(s_Red var, s_Param par)){
	// // Simplemente copio lo que estaba usando antes
	// // Primero itero en los agentes, luego defino el segundo agente y evoluciono al primero interactuando con el segundo.
	// for(var.i_agente=0; var.i_agente<par.i_N; ++var.i_agente){
			// do{
				// var.i_agente2 = rand()%par.i_N;
			// }
			// while(var.i_agente==var.i_agente2);
			// for(var.i_topico=0; var.i_topico<par.i_T; ++var.i_topico) RK4(var.pd_Opi, var, par, pf_Dinamica);
		// }
		
	// return 0;
// }


// Esta función toma un número y me da un número aleatorio DISTINTO al número recibido en un cierto rango.
// Esta es la versión con ints. Para que este programa funcione correctamente tiene que pasar que i_min <= i_input <= i_max
// Además, el min y el max pertenecen al rango.
// Seré sincero, toda esta función es para no meter un if justo en el corazón de la iteración de mi programa.
// Esta función no está terminada, otro día la retomo.
// int Aleatorio_distinto_i(int i_input, int i_min, int i_max){
	// // Defino mis variables a usar
	// unsigned int i_rango = i_max - i_min; // Fijate que el i_rango tiene que ser siempre positivo.
	// // 
	// // Espero que esto no me genere problemas a futuro. Problemas del tipo: "Segmentation Fault" que nunca más descubro dónde ocurren.
	// unsigned int i_aleatorio = (Random()%i_rango);
	
	// // Armo la tira de datos que va a tener todos los números posibles dentro del rango, MENOS el número i_input
	// int *pi_Tira;
	// pi_Tira = (int*) malloc((i_rango-1+2)*sizeof(int));
	// *pi_Tira = 1; // Este es el número de filas de mi vector
	// *(pi_Tira+1) = i_rango-1; // Este es el número de columnas de mi vector
	// for(register int i_i=0; i_i<i_input; ++i_i) *(pi_Tira+i_i+2) = i_i+i_min;
	// for(register int i_i=i_input+1; i_i<i_rango; ++i_i) *(pi_Tira+i_i-1+2) = i_i+i_min;
	
	
	
	
	
	
	// return ;
// }


//-----------------------------------------------------------------------------------
//-----------------------------------------------------------------------------------
//-----------------------------------------------------------------------------------

NUEVO_PROGRAMA

Este programa lo hice el 03/01/2021. La idea era modificar las funciones de Deltax y
la que calculaba la norma de los vectores de manera de poder usarla de forma más general.
Para esto hice que puedan tomar el tamaño de los vectores de las primeras coordenadas
de los vectores. Aproveché para cambiarles los nombres siguiendo un poco las nuevas
reglas de nomenclatura. Les agregué una d al final para señalar que son las versiones
que funcionan sobre vectores double.

Este trabajito lo hice porque como quería implementar un mecanismo de corte en mi
programa principal, quería que este mecanismo use como criterio la diferencia entre
el paso siguiente y el anterior, de manera de que si al iterar el sistema deja de 
evolucionar, el programa corte y avance a otra cosa. Por eso necesitaba calcular
diferencias entre vectores y sus normas.



// #include<stdio.h>
// #include<stdlib.h>
// #include<math.h>
// #include<time.h>

// // Acá voy a declarar las funciones.------------------------------------

// double Random();
// int Visualizar_d(double *pd_vec);
// int Visualizar_f(float *pf_vec);
// int Visualizar_i(int *pi_vec);
// int Escribir_d(double *pd_vec, FILE *pa_archivo);
// int Escribir_i(int *pi_vec, FILE *pa_archivo);
// int Delta_Vec_d(double *pd_x1, double *pd_x2, double *pd_Dx);
// double Norma_d(double *pd_x);



// /*####################################################################################
// ####################################################################################
// ####################################################################################
// ####################################################################################
// */


// //---------------------------------------------------------------------------------------------------

// // Vamos a intentar ver como se leen archivos y data desde estos
// // Creo que lo más útil va a ser usar el fscanf porque mis datos están separados por tabulaciones
// // Acá está la forma de leer el archivo. Sólo necesitaría poder saber que tan largo es antes de
// // subirlo, pero creo que eso sería mucho pedir.

// int main(){
	// // Defino mis variables temporales para medir el tiempo que tarda el programa. También genero una nueva semilla
	// time_t tt_prin,tt_fin;
	// time(&tt_prin);
	// srand(time(NULL));
	// int i_tardanza;
	
	// // Defino los vectores que voy a restar y el que voy a usar para guardar la diferencia. También el tamaño de los vectores y la variable de la norma final.
	// int i_F = 3,i_C = 3; // Esto está bueno para reducir filas, pero no siempre es bueno para la lectura del código
	// double d_norma = 0;
	// double *pd_x1, *pd_x2, *pd_diferencia; // Pensé que no me iba a tomar esto.
	// // Voy a poner los tres punteros en un solo array
	// double *apd_punteros[3];
	// apd_punteros[0] = pd_x1;
	// apd_punteros[1] = pd_x2;
	// apd_punteros[2] = pd_diferencia;
	
	// // Asigno memoria a mis vectores.
	// for(register int i_i=0; i_i<3; ++i_i) apd_punteros[i_i] = (double*) malloc((i_F*i_C+2)*sizeof(double));
	
	// // Inicializo mis vectores
	// for(register int i_i=0; i_i<3; ++i_i) *(apd_punteros[i_i])= i_F;
	// for(register int i_i=0; i_i<3; ++i_i) *(apd_punteros[i_i]+1)= i_C;
	// for(register int i_i=0; i_i<3; ++i_i) for(register int i_j=0; i_j<i_F*i_C; ++i_j) *(apd_punteros[i_i]+i_j+2) = 0;
	
	// // Ahora sí. Voy a poner todos 1 en el primer vector, números que crecen en progresión de a 1 en el segundo vector, y el tercero queda para ser la diferencia
	// for(register int i_i=0; i_i<i_C*i_F; ++i_i) *(apd_punteros[0]+i_i+2) = 1;
	// for(register int i_i=0; i_i<i_C*i_F; ++i_i) *(apd_punteros[1]+i_i+2) = i_i;
	
	// // Voy a visualizarlos para garantizar que están bien
	// printf("Este es el primer vector. Tiene todos 1\n");
	// Visualizar_d(apd_punteros[0]);
	
	// printf("Este es el segundo vector. Tiene numeros que van del 0 al %d\n",i_C*i_F-1);
	// Visualizar_d(apd_punteros[1]);
	
	// printf("Este es el vector de diferencias. Por ahora solo tiene ceros porque simplemente esta inicializado\n");
	// Visualizar_d(apd_punteros[2]);
	
	// // Ahora aplico mis funciones
	// Delta_Vec_d(apd_punteros[0],apd_punteros[1],apd_punteros[2]);
	// d_norma = Norma_d(apd_punteros[2]);
	
	// printf("La norma del vector de diferencias es: %lf\n", d_norma);
	
	// printf("El vector de diferencias ahora cambio a esto\n");
	// Visualizar_d(apd_punteros[2]);
	
	// // Ejecuto los comandos finales para medir el tiempo y liberar memoria
	// for(register int i_i=0; i_i<3; ++i_i) free(apd_punteros[i_i]);
	// time(&tt_fin);
	// i_tardanza = tt_fin-tt_prin;
	// printf("Tarde %d segundos en terminar\n",i_tardanza);
	// return 0;
// }

// /*####################################################################################
// ####################################################################################
// ####################################################################################
// ####################################################################################
// */

// // De acá en adelante van las funciones a declarar

// // Esta función me genera un número random
// double Random(){
	// return ((double) rand()/(double) RAND_MAX);
// }


// // Estas son las funciones de Inicialización.
// // #########################################################################################################


// // Esta función es para observar los vectores double
// int Visualizar_d(double *pd_vec){
	// // Defino las variables que voy a necesitar.
	// int i_F,i_C;
	// i_F = *pd_vec;
	// i_C = *(pd_vec+1);
	
	// // Printeo mi vector
	// for(register int i_i=0; i_i<i_F; i_i++){
		// for(register int i_j=0; i_j<i_C; i_j++) printf("%lf\t",*(pd_vec+i_i*i_C+i_j+2));
		// printf("\n");
	// }
	// printf("\n");
	
	// return 0;
// }

// // Esta función es para observar los vectores float
// int Visualizar_f(float *pf_vec){
	// // Defino las variables que voy a necesitar.
	// int i_F,i_C;
	// i_F = *pf_vec;
	// i_C = *(pf_vec+1);
	
	// // Printeo mi vector
	// for(register int i_i=0; i_i<i_F; i_i++){
		// for(register int i_j=0; i_j<i_C; i_j++) printf("%lf\t",*(pf_vec+i_i*i_C+i_j+2));
		// printf("\n");
	// }
	// printf("\n");
	
	// return 0;
// }

// // Esta función es para observar los vectores int
// int Visualizar_i(int *pi_vec){
	// // Defino las variables que voy a necesitar.
	// int i_F,i_C;
	// i_F = *pi_vec;
	// i_C = *(pi_vec+1);
	
	// // Printeo mi vector
	// for(register int i_i=0; i_i<i_F; i_i++){
		// for(register int i_j=0; i_j<i_C; i_j++) printf("%d\t",*(pi_vec+i_i*i_C+i_j+2));
		// printf("\n");
	// }
	// printf("\n");
	
	// return 0;
// }

// // Esta función va a recibir un vector double y va a escribir ese vector en mi archivo.
// int Escribir_d(double *pd_vec, FILE *pa_archivo){
	// // Defino las variables del tamaño de mi vector
	// int i_C,i_F;
	// i_F = *pd_vec;
	// i_C = *(pd_vec+1);
	
	// // Ahora printeo todo el vector en mi archivo
	// for(register int i_i=0; i_i<i_C*i_F; i_i++) fprintf(pa_archivo,"\t%lf",*(pd_vec+i_i+2));
	// fprintf(pa_archivo,"\n");
	
	// return 0;
// }

// // Esta función va a recibir un vector int y va a escribir ese vector en mi archivo.
// int Escribir_i(int *pi_vec, FILE *pa_archivo){
	// // Defino las variables del tamaño de mi vector
	// int i_C,i_F;
	// i_F = *pi_vec;
	// i_C = *(pi_vec+1);
	
	// // Ahora printeo todo el vector en mi archivo
	// for(register int i_i=0; i_i<i_C*i_F; i_i++) fprintf(pa_archivo,"\t%d",*(pi_vec+i_i+2));
	// fprintf(pa_archivo,"\n");
	
	// return 0;
// }

// // Esta función me calcula la norma de un vector
// double Norma_d(double *pd_x){
	// // Defino mis variables iniciales que son el resultado final, la suma de los cuadrados y el tamaño de mi vector
	// double d_norm,d_sum = 0;
	// int i_C,i_F;
	// i_F = *pd_x;
	// i_C = *(pd_x+1);
	
	// // Calculo la norma como la raíz cuadrada de la sumatoria de los cuadrados de cada coordenada.
	// for(register int i_i=0; i_i<i_C*i_F; ++i_i) d_sum += *(pd_x+i_i+2)*(*(pd_x+i_i+2));
	// d_norm = sqrt(d_sum);
	// return d_norm;
// }

// // Esta función me calcula la diferencia entre dos vectores
// int Delta_Vec_d(double *pd_x1, double *pd_x2, double *pd_Dx){
	// // Compruebo primero que mis dos vectores sean iguales en tamaño
	// if(*pd_x1!=*pd_x2 || *(pd_x1+1)!=*(pd_x2+1) || *pd_x1!=*pd_Dx || *(pd_x1+1)!=*(pd_Dx+1)){
		// printf("Los vectores son de tamaños distintos, no puedo restarlos\n");
		// return 0;
	// }
	
	// // Defino las variables de tamaño de mis vectores
	// int i_C,i_F;
	// i_F = *pd_x1;
	// i_C = *(pd_x2);
	
	// // Defino mi vector intermedio de registro de datos y lo inicializo
	// double *pd_diferencias;
	// pd_diferencias = (double*) malloc((i_C*i_F+2)*sizeof(double));
	// *pd_diferencias = i_F;
	// *(pd_diferencias+1) = i_C;
	// for(register int i_i=0; i_i<i_C*i_F; ++i_i) *(pd_diferencias+i_i+2) = 0;
	
	// // Calculo la diferencia entre dos vectores
	// for(register int i_i=0; i_i<i_C*i_F; ++i_i) *(pd_diferencias+i_i+2) = *(pd_x1+i_i+2)-*(pd_x2+i_i+2);
	
	// // Me anoto la diferencia en un vector que está en el main del programa, y luego libero el espacio usado.
	// for(register int i_i=0; i_i<i_C*i_F; ++i_i) *(pd_Dx+i_i+2) = *(pd_diferencias+i_i+2);
	// free(pd_diferencias);
	// return 0;
// }


//-----------------------------------------------------------------------------------
//-----------------------------------------------------------------------------------
//-----------------------------------------------------------------------------------

NUEVO_PROGRAMA

Este programa lo hice el 07/01/2021. La idea era ver si se podía escribir en dos
archivos de manera simultánea. Efectivamente se puede, se necesitan abrir dos punteros
a FILE diferenciados y abrir los distintos programas por separado. Después de eso, todo
funca bárbaro. Es muy corto, saqué todo lo que no fuera necesario. Así que no tiene
ninguna de las otras funciones.


// #include<stdio.h>
// #include<stdlib.h>
// #include<math.h>
// #include<time.h>


// int main(){
	// // Defino mis variables temporales para medir el tiempo que tarda el programa. También genero una nueva semilla
	// time_t tt_prin,tt_fin;
	// time(&tt_prin);
	// srand(time(NULL));
	// int i_tardanza;
	
	// // Voy a abrir un archivo y guardar algo en él
	// char s_Nombre1[255];
	// sprintf(s_Nombre1,"Primer Archivo");
	// FILE *pf_archivo1=fopen(s_Nombre1,"w");
	// fprintf(pf_archivo1,"Estoy escribiendo en el primer archivo\n");
	
	// // Ahora abro un segundo archivo en el mismo código
	// char s_Nombre2[255];
	// sprintf(s_Nombre2,"Segundo Archivo");
	// FILE *pf_archivo2=fopen(s_Nombre2,"w");
	// fprintf(pf_archivo2,"Estoy escribiendo en el segundo archivo\n");
	
	// for(register int i_i=0; i_i<10; i_i++){
		// fprintf(pf_archivo1,"%d\n",i_i);
		// fprintf(pf_archivo2,"%d\n",i_i);
	// }
	
	
	// // Ejecuto los comandos finales para medir el tiempo y liberar memoria
	// fclose(pf_archivo1);
	// fclose(pf_archivo2);
	// time(&tt_fin);
	// i_tardanza = tt_fin-tt_prin;
	// printf("Tarde %d segundos en terminar\n",i_tardanza);
	// return 0;
// }


//-----------------------------------------------------------------------------------
//-----------------------------------------------------------------------------------
//-----------------------------------------------------------------------------------

NUEVO_PROGRAMA

Este programa lo armé el 09/01/2021. La idea era probar el funcionamiento del
argc y del argv para ver cómo se pasan datos a la función a través de línea
de comando. También acá probé el uso de la función strtol. Estas dos cosas
están muy bien explicadas al final de este programa.

// #include<stdio.h>
// #include<stdlib.h>
// #include<math.h>
// #include<time.h>


// int main(int argc, char *argv[]){
	// // Defino mis variables temporales para medir el tiempo que tarda el programa. También genero una nueva semilla
	// time_t tt_prin,tt_fin;
	// time(&tt_prin);
	// srand(time(NULL));
	// int i_tardanza;

	// // Defino dos variables a las que les voy a pasar input desde línea de comando, y las voy a sumar.
	// int i_var1,i_var2;
	// i_var1 = strtol(argv[1],NULL,10);
	// i_var2 = strtol(argv[2],NULL,10);
	
	// printf("La suma de los numeros que me pasaste es: %d \n",i_var1+i_var2);
	
	// // Ejecuto los comandos finales para medir el tiempo y liberar memoria
	// time(&tt_fin);
	// i_tardanza = tt_fin-tt_prin;
	// printf("Tarde %d segundos en terminar\n",i_tardanza);
	// return 0;
// }

// Voy a explicar acá cómo funca el strtol(const char *str, char **endptr, int base).
// La idea es que uno le pasa el string str. Este string puede tener una parte numérica seguida de una parte
// literal. O podría ser sólo numérica. La cosa es que uno le pasa el str a la primera coordenada. A la segunda
// coordenada le pasa la dirección de un puntero donde la función va a guardar la parte literal sobrante de str.
// Siempre se puede poner NULL ahí en caso de que uno no quiera guardar esa info. El tercer elemento es la
// base numérica a la cual quiere convertir el número. Claramente yo me muevo en base 10, así que eso
// siempre puede ser 10 tranquilamente.

// Expliquemos también argc y *argv. argc es el número de elementos pasados en por input de línea de
// comando al main. En particular el nombre del archivo SIEMPRE se pasa, así que argc siempre es 1 como mínimo.
// Por otro lado, en cada coordenada argv guarda cada uno de los argumentos pasados. argv[0] es el nombre del
// archivo. argv[1] es el primer argumento. argv[2] es el segundo argumento, y así.


//-----------------------------------------------------------------------------------
//-----------------------------------------------------------------------------------
//-----------------------------------------------------------------------------------

NUEVO_PROGRAMA

Este archivo es del 17/01/2021. La idea era simplemente probar cómo era el tema para que
el programa guarde en los archivos de datos mis valores con 12 decimales de precisión.
La cosa es que el sistema venía guardando sólo hasta 6 decimales, lo cual era una cagada
porque si ya tengo hecho el cálculo con datos más precisos, guardar menos decimales es
un desperdicio. Cuestión que ahora estoy guardando más datos, ya vi que simplemente tengo
que poner el punto con el número de decimales y listo.


// #include<stdio.h>
// #include<stdlib.h>
// #include<math.h>
// #include<time.h>


// int main(int argc, char *argv[]){
	// // Defino mis variables temporales para medir el tiempo que tarda el programa. También genero una nueva semilla
	// time_t tt_prin,tt_fin;
	// time(&tt_prin);
	// srand(time(NULL));
	// int i_tardanza;

	// // Defino unas variables int y doubles para hacer unas cuentas.
	
	// double d_resultado;
	// double d_num1 = 0.453;
	// int i_num1 = 250, i_num2 = 1000;
	
	// char s_archivo1[255];
	// sprintf(s_archivo1,"Prueba");
	// FILE *pa_archivo1=fopen(s_archivo1,"w"); // Con esto abro mi archivo y dirijo el puntero a él.
	
	// d_resultado = d_num1/(i_num1*i_num2);
	
	// fprintf(pa_archivo1,"%.12lf\t", d_resultado);
	
	// d_resultado = d_num1/ (double) (i_num1*i_num2);
	
	// fprintf(pa_archivo1,"%lf\t", d_resultado);
	
	// d_resultado = 0.000000001;
	
	// fprintf(pa_archivo1,"%lf\t",d_resultado);
	
	// // Ejecuto los comandos finales para medir el tiempo y liberar memoria
	// time(&tt_fin);
	// i_tardanza = tt_fin-tt_prin;
	// printf("Tarde %d segundos en terminar\n",i_tardanza);
	// return 0;
// }

// Estoy queriendo ver si descubro porqué mis datos de error me guardan sólo hasta
// seis decimales, cuando mis variables son doubles.

//-----------------------------------------------------------------------------------
//-----------------------------------------------------------------------------------
//-----------------------------------------------------------------------------------


NUEVO_PROGRAMA

Este programa es del 19/01/2021. Lo que hice acá fue probar el cómo armar una función
que implemente un método de corte automático, de manera que cuando la el sistema se
encuentre cerca de un estado estable, deje de iterar. Esto es para reducir el número
de iteraciones innecesarias. La idea es que tiene un parámetro, d_parámetro, que lo
compara con un valor de corte. Si el parámetro es menor que el valor de corte,
el sistema sigue operando una cantidad arbitaria de veces, como para asegurarse
de que no incumpla el valor de corte en el futuro. Algo así como decir que no
sea una estabilidad temporal y el sistema luego vuelva a dispararse. Si no se
vuelve a disparar durante esas iteraciones extra, el sistema deja de correr.



// #include<stdio.h>
// #include<stdlib.h>
// #include<math.h>
// #include<time.h>

// int Operacion(double* d_parametro);
// int Corte(double* d_parametro);
// double Random();


// int main(int argc, char *argv[]){
	// // Defino mis variables temporales para medir el tiempo que tarda el programa. También genero una nueva semilla
	// time_t tt_prin,tt_fin;
	// time(&tt_prin);
	// srand(time(NULL));
	// int i_tardanza;

	// // Defino mi contador de iteraciones, el parámetro de corte y una variable para la cantidad total de iteraciones
	// double d_parametro = rand();
	// int i_resultado, i_iteracionesT;
	
	// // Como el valor inicial de parámetro es random, lo printeo para verlo
	// printf("El numero inicial es %lf\n",d_parametro);
	
	// // Printeo también la cantidad de pasos mínimos que voy a necesitar para que el sistema finalice su proceso
	// i_resultado = (int) ceil(log(1000*d_parametro)/log(5))+50;
	// printf("Voy a tener que iterar mínimo %d pasos\n", i_resultado);
	
	// // Realizo las operaciones aplicando la función de Corte y muestro cuántas veces iteré.
	// i_iteracionesT = Corte(&d_parametro);
	// printf("En total itere %d veces\n", i_iteracionesT);
	
	// // Ejecuto los comandos finales para medir el tiempo y liberar memoria
	// time(&tt_fin);
	// i_tardanza = tt_fin-tt_prin;
	// printf("Tarde %d segundos en terminar\n",i_tardanza);
	// return 0;
// }

// // Esta función me genera un número random entre 0 y 1
// double Random(){
	// return ((double) rand()/(double) RAND_MAX);
// }

// // Esta función realiza un proceso que modifica mi parámetro
// int Operacion(double* pd_parametro){
	
	// // Defino un mecanismo para que con una baja probabilidad el parámetro a veces suba en vez de bajar
	// if(Random() < 0.7) *pd_parametro = *pd_parametro/5;
	// else *pd_parametro = *pd_parametro*10;
	// return 0;
// }

// // Esta función gestiona la iteración del sistema y se encarga de cortarlo cuando considera que el sistema llegó a un estado estable.
// int Corte(double* pd_parametro){
	
	// // Defino mi cantidad de pasos totales realizados
	// int i_iteraciones=0, i_contador=0;
	
	// while(i_contador<50){
		// if(i_iteraciones > 0) printf("Se rompio la condicion de corte al hacer %d iteraciones extra\n",i_contador);
		// // Inicializo el contador
		// i_contador = 0;
		
		// // Evoluciono el sistema hasta que se cumpla el criterio de corte
		// do{
			// Operacion(pd_parametro);
			// i_iteraciones +=1;
		// }
		// while(*pd_parametro > 0.001);
		
		// // Ahora evoluciono el sistema una cantidad arbitaria de veces, 500 en este caso. Le pongo como condición que si el sistema
		// // deja de cumplir la condición de corte, deje de evolucionar
		// while(i_contador < 50 && *pd_parametro <= 0.001 ){
			// Operacion(pd_parametro);
			// i_contador +=1;
			// i_iteraciones +=1;
		// }
		// // Si el sistema evolucionó menos veces que la cantidad arbitraria, es porque rompió la condiciones de corte.
		// // Por tanto lo vuelvo a hacer trabajar hasta que se vuelva a cumplir la condición de corte.
		// // Si logra evolucionar la cantidad arbitraria de veces sin problemas, termino la evolución.
	// }
	
	// return i_iteraciones;
// }