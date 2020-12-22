//Este es el archivo para testeos

#include<stdio.h>
#include<stdlib.h>
#include<math.h>
#include<time.h>

// Acá vienen los structs.
// El struct Red tiene los datos que definen mi red, y la info de la red
typedef struct Red{
	double *pd_Ang; // Matriz de superposición entre tópicos. Tiene tamaño T*T
	int *pi_Ady; // Matriz de adyacencia que define mis conexiones. Tiene tamaño N*N
	double *pd_Opi; // Vector de opinión de cada individuo
	int i_agente; // Entero que representa el agente que estoy mirando. Es un valor que va entre 0 y N-1
	int i_topico; // Entero que representa el tópico que estoy mirando. Es un valor que va entre 0 y T-1
} s_Red;

typedef struct Parametros{
	float f_Beta; // Exponente que regula el grado de homofilia
	float f_Pint; // Probabilidad de que se forme el enlace de manera aleatoria
	float f_K; // Influencia social
	float f_alfa; // Controversialidad de los temas
	int i_N; // Número de agentes en la red
	int i_T; // Cantidad de tópicos
	int i_Mopi; // Máximo inicial de opiniones
	float f_dt; // Paso temporal de iteración del sistema
} s_Param;

// Acá voy a declarar las funciones.------------------------------------

double Random();
int Visualizar_d(double *pd_vec);
int Visualizar_f(float *pf_vec);
int Visualizar_i(int *pi_vec);
int GenerarOpi(s_Red var, s_Param par);
int GenerarAng(s_Red var);
int GenerarAdy(s_Red var,s_Param par);
double Din1(s_Red var, s_Param par, int i_j);
double Din2(s_Red var, s_Param par);
double Duplicar(s_Red var, s_Param par);
int RK4(double *pd_vec ,s_Red var, s_Param par, double (*fp_funcion)(s_Red var, s_Param par));



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
	// Defino mis variables temporales para medir el tiempo que tarda el programa. También genero una nueva semilla
	time_t tt_prin,tt_fin;
	time(&tt_prin);
	srand(time(NULL));
	int i_tardanza;
	
	
	// Defino los nombres de mis structs en este programa y los valores de los parámetros
	s_Red red;
	s_Param datos;
	
	datos.f_Beta = 0.5;
	datos.f_Pint = 0.5;
	datos.f_K = 0.5;
	datos.f_alfa = 2;
	datos.i_N = 3;
	datos.i_T = 3;
	datos.i_Mopi = 3;
	datos.f_dt = 0.2;
	
	// Defino el puntero a mi función y lo inicializo
	double (*pf_Dup)(s_Red Red, s_Param Parametros) = &Duplicar;	
	
	// Asigno memoria a mis matrices y las inicializo
	
	// Matriz de Vectores de opinión. Tiene tamaño N*T
	red.pd_Opi = (double*) malloc((datos.i_N*datos.i_T+2)*sizeof(double)); // Asigno espacio de memoria al vector
	for(register int i_i=0; i_i<datos.i_N*datos.i_T+2; i_i++) red.pd_Opi[i_i] = 0; // Inicializo la matriz para que no haya "basura" en alguna posición
	red.pd_Opi[0] = datos.i_N; // Guardo el número de filas en la primer coordenada del vector
	red.pd_Opi[1] = datos.i_T; // Guardo el número de Columnas en la segunda coordenada del vector
	GenerarOpi(red,datos); // Genero la red de Vectores de opinión propiamente dicha.

	// Matriz de Superposición. Tiene tamaño T*T
	red.pd_Ang = (double*) malloc((datos.i_T*datos.i_T+2)*sizeof(double)); // Asigno espacio de memoria al vector
	for(register int i_i=0; i_i<datos.i_T*datos.i_T+2; i_i++) red.pd_Ang[i_i] = 0; // Inicializo la matriz para que no haya "basura" en alguna posición
	red.pd_Ang[0] = datos.i_T; // Guardo el número de filas en la primer coordenada del vector
	red.pd_Ang[1] = datos.i_T; // Guardo el número de Columnas en la segunda coordenada del vector
	GenerarAng(red); // Genero la red de Vectores de opinión propiamente dicha.
	
	// Matriz de Adyacencia. Tiene tamaño N*N
	red.pi_Ady = (int*) malloc((datos.i_N*datos.i_N+2)*sizeof(int)); // Asigno espacio de memoria al vector
	for(register int i_i=0; i_i<datos.i_N*datos.i_N+2; i_i++) red.pi_Ady[i_i] = 0; // Inicializo la matriz para que no haya "basura" en alguna posición
	red.pi_Ady[0] = datos.i_N; // Guardo el número de filas en la primer coordenada del vector
	red.pi_Ady[1] = datos.i_N; // Guardo el número de columnas en la segunda coordenada del vector
	GenerarAdy(red,datos); // Genero la red de Adyacencia propiamente dicha.
	
	// Aplico el RK4
	RK4(red.pd_Opi, red, datos, pf_Dup);
	
	
	// Ejecuto los comandos finales para medir el tiempo y liberar memoria
	free(red.pi_Ady);
	free(red.pd_Ang);
	free(red.pd_Opi);
	time(&tt_fin);
	i_tardanza = tt_fin-tt_prin;
	printf("Tarde %d segundos en terminar\n",i_tardanza);
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


// Estas son las funciones de Inicialización.
// #########################################################################################################


// Esta función es para observar los vectores double
int Visualizar_d(double *pd_vec){
	// Defino las variables que voy a necesitar.
	int i_F,i_C;
	i_F = *pd_vec;
	i_C = *(pd_vec+1);
	
	// Printeo mi vector
	for(register int i_i=0; i_i<i_F; i_i++){
		for(register int i_j=0; i_j<i_C; i_j++) printf("%lf\t",*(pd_vec+i_i*i_C+i_j+2));
		printf("\n");
	}
	printf("\n");
	
	return 0;
}

// Esta función es para observar los vectores float
int Visualizar_f(float *pf_vec){
	// Defino las variables que voy a necesitar.
	int i_F,i_C;
	i_F = *pf_vec;
	i_C = *(pf_vec+1);
	
	// Printeo mi vector
	for(register int i_i=0; i_i<i_F; i_i++){
		for(register int i_j=0; i_j<i_C; i_j++) printf("%lf\t",*(pf_vec+i_i*i_C+i_j+2));
		printf("\n");
	}
	printf("\n");
	
	return 0;
}

// Esta función es para observar los vectores int
int Visualizar_i(int *pi_vec){
	// Defino las variables que voy a necesitar.
	int i_F,i_C;
	i_F = *pi_vec;
	i_C = *(pi_vec+1);
	
	// Printeo mi vector
	for(register int i_i=0; i_i<i_F; i_i++){
		for(register int i_j=0; i_j<i_C; i_j++) printf("%d\t",*(pi_vec+i_i*i_C+i_j+2));
		printf("\n");
	}
	printf("\n");
	
	return 0;
}




// Esta función me genera los vectores opinión iniciales del sistema. Esto es una matriz de tamaño N*T
int GenerarOpi(s_Red var, s_Param par){
	// Obtengo las dimensiones de la "matriz" de opiniones de mis agentes.
	int i_Filas,i_Columnas;
	i_Filas = (int) var.pd_Opi[0];
	i_Columnas = (int) var.pd_Opi[1];
	
	// Inicializo la "matriz" de opiniones de mis agentes.
	for(int i_i=0;i_i<i_Filas*i_Columnas;i_i++) var.pd_Opi[i_i+2] = par.i_Mopi*(Random()-0.5)*2;
	return 0;
}

// Esta función me genera la matriz de Superposicion del sistema. Esto es una matriz de T*T
int GenerarAng(s_Red var){
	// Obtengo las dimensiones de la matriz de Superposicion.
	int i_Filas,i_Columnas;
	i_Filas = (int) var.pd_Ang[0];
	i_Columnas = (int) var.pd_Ang[1];
	
	// Inicializo la matriz de Superposicion de mi sistema.
	for(int i_i=0; i_i<i_Filas; i_i++) for(int i_j=0; i_j<i_i; i_j++) var.pd_Ang[i_i*i_Columnas+i_j+2] = 0.5; // Decidí poner 0.5 entre todos los tópicos de mi modelo
	for(int i_i=0; i_i<i_Filas; i_i++) var.pd_Ang[i_i*i_Columnas+i_i+2] = 1; // Esto me pone 1 en toda la diagonal
	for(int i_i=0; i_i<i_Filas; i_i++) for(int i_j=i_i+1; i_j<i_Columnas; i_j++) var.pd_Ang[i_i*i_Columnas+i_j+2] = var.pd_Ang[i_j*i_Columnas+i_i+2]; // Esta sola línea simetriza la matriz
	return 0;
}


// Esta función me inicializa la matriz de Adyacencia. Esto es una matriz de N*N
int GenerarAdy(s_Red var, s_Param par){
	// Obtengo las dimensiones de la matriz de Adyacencia.
	int i_Filas,i_Columnas;
	i_Filas = (int) var.pi_Ady[0];
	i_Columnas = (int) var.pi_Ady[1];
	
	// Inicializo la matriz de Adyacencia de mi sistema
	for(int i_i=0; i_i<i_Filas; i_i++) {
		for(int i_j=0; i_j<i_i; i_j++) {
			// Saco un número random y veo si asigno un 1 o un 0 a esa posición-
			if(Random()<par.f_Pint) var.pi_Ady[i_i*i_Columnas+i_j+2] = 1;
			else var.pi_Ady[i_i*i_Columnas+i_j+2] = 0;
		}
	}
	for(int i_i=0; i_i<i_Filas; i_i++) for(int i_j=i_i+1; i_j<i_Columnas; i_j++) var.pi_Ady[i_i*i_Columnas+i_j+2] = var.pi_Ady[i_j*i_Columnas+i_i+2]; // Esta sola línea simetriza la matriz
	// for(int i=0; i<par.N; i++) var.Ady[i*par.N+i] = 1; // Esto me pone 1 en toda la diagonal
	return 0;
}

// #####################################################################################

// Estas son las funciones del avance
//#######################################################################################

// Esta función resuelve un término de los de la sumatoria.
double Din1(s_Red var, s_Param par,int i_j){
	
	// Defino las variables locales de mi función. d_resultados es el return. 
	// d_opiniones_superpuestas es el producto de la matriz de superposición de tópicos con el vector opinión de un agente.
	double d_resultado,d_opiniones_superpuestas = 0;
	
	// Obtengo el tamaño de columnas de mis tres matrices
	int i_Co,i_Cs,i_Ca;
	i_Co = (int) var.pd_Opi[1];
	i_Cs = (int) var.pd_Ang[1];
	i_Ca = var.pi_Ady[1];
	
	for(register int i_p=0; i_p<i_Cs; i_p++) d_opiniones_superpuestas += var.pd_Ang[var.i_topico*i_Cs+i_p+2]*var.pd_Opi[i_j*i_Co+i_p+2]; // Calculo previamente este producto de la matriz con el vector.
	d_resultado = var.pi_Ady[var.i_agente*i_Ca+i_j+2]*tanh(par.f_alfa*d_opiniones_superpuestas); // Esto es lo que está dentro de la sumatoria en la ecuación dinámica.
	return d_resultado; // La función devuelve el número que buscás, no te lo asigna en una variable.
}

// Esta es la segunda parte de la ecuación dinámica, con esto puedo realizar una iteración del sistema.
double Din2(s_Red var, s_Param par){
	
	// Defino las variables locales de mi función. d_resultado es lo que voy a returnear.
	// d_sumatoria es el total de la sumatoria del segundo término de la ecuación diferencial.
	double d_resultado,d_sumatoria=0;
	
	// Calculo la sumatoria de la ecuación diferencial. Para esto es que existe la función Din1.
	for(register int i_j=0; i_j<var.i_agente; i_j++) d_sumatoria += Din1(var,par,i_j);
	for(register int i_j=var.i_agente+1; i_j<par.i_N; i_j++) d_sumatoria += Din1(var,par,i_j);
	
	// Obtengo el tamaño de Columnas de mi matriz de Vectores de opinión y calculo el valor del campo que define mi ecuación diferencial
	int i_Columnas = (int) var.pd_Opi[1];
	d_resultado = -var.pd_Opi[var.i_agente*i_Columnas+var.i_topico+2]+par.f_K*d_sumatoria;
	return d_resultado;
}

//#######################################################################################


// Esta función me realiza una iteración del sistema a partir de un RK4.
// Incluso creo que no es necesario el uso del puntero de funciones, pero quiero aprender a usarlo
int RK4(double *pd_vec ,s_Red var, s_Param par, double (*fp_funcion)(s_Red var, s_Param par)){
	// Defino las variables y vectores que voy a necesitar
	int i_filas = (int) *pd_vec; // Este es el número de filas del vector principal
	int i_columnas = (int) *(pd_vec+1); // Este es el número de columnas del vector principal
	double *pd_pendientes[5]; // Este array de punteros guarda los punteros kN
	float DT[4]; // Esto me ayuda a meter el paso temporal que se usa para calcular cada pendiente.
	
	
	// Voy a armar vectores con las pendientes que calcule, para luego calcular el avance de todas las variables al final
	double *k0;
	k0 = (double*) malloc((i_filas*i_columnas+2)*sizeof(double));
	
	double *k1;
	k1 = (double*) malloc((i_filas*i_columnas+2)*sizeof(double));
	
	double *k2;
	k2 = (double*) malloc((i_filas*i_columnas+2)*sizeof(double));
	
	double *k3;
	k3 = (double*) malloc((i_filas*i_columnas+2)*sizeof(double));
	
	double *k4;
	k4 = (double*) malloc((i_filas*i_columnas+2)*sizeof(double));
	
	double *pd_inicial; // Este me guarda las condiciones iniciales del vector, que las voy a necesitar al calcular cada paso del RK4
	pd_inicial = (double*) malloc((i_filas*i_columnas+2)*sizeof(double));
	
	// Inicializo mis punteros
	pd_pendientes[0] = k0;
	pd_pendientes[1] = k1;
	pd_pendientes[2] = k2;
	pd_pendientes[3] = k3;
	pd_pendientes[4] = k4;
	for(register int i_i=0; i_i<i_filas*i_columnas+2; i_i++){
		*(pd_inicial+i_i) = *(pd_vec+i_i);
		for(register int i_j=0; i_j<5;i_j++) *(pd_pendientes[i_j]+i_i) = 0; // De esta manera inicializo los 5 punteros, todos en una sola línea.
	}
	
	// Guardo registro del tamaño de mis vectores k
	for(register int i_j=0; i_j<5;i_j++) *(pd_pendientes[i_j]) = i_filas;
	for(register int i_j=0; i_j<5;i_j++) *(pd_pendientes[i_j]+1) = i_columnas;
	
	// Armo mi vector DT. Este hay que armarlo uno por uno, si o si.
	DT[0] = 0;
	DT[1] = par.f_dt*0.5;
	DT[2] = par.f_dt*0.5;
	DT[3] = par.f_dt;
		
	// Acá hago las iteraciones del RK4 para hallar las pendientes k
	for(register int i_j=0; i_j<4; i_j++){ // Esto itera para mis 4 k
		for(var.i_agente=0; var.i_agente<*pd_vec; var.i_agente++){ // Itero para todos los agentes
			for(var.i_topico=0; var.i_topico<*(pd_vec+1); var.i_topico++){ // Itero para todos los tópicos
				// Calculo el elemento de la pendiente k(i_j+1)
				for(register int i_i=0; i_i<i_filas*i_columnas; i_i++) *(pd_vec+i_i+2) = *(pd_inicial+i_i+2)+*(pd_pendientes[i_j]+i_i+2)*DT[i_j];
				*(pd_pendientes[i_j+1]+var.i_agente*i_columnas+var.i_topico+2) = (*fp_funcion)(var,par);
			}
		}
	}
	
	// Con TODAS las pendientes calculadas, ahora sí avanzo temporalmente mi sistema
	
	for(register int i_i=0; i_i<i_filas*i_columnas; i_i++){
	*(pd_vec+i_i+2) = *(pd_inicial+i_i+2)+(par.f_dt/6)*(*(pd_pendientes[1]+i_i+2)+*(pd_pendientes[2]+i_i+2)*2+*(pd_pendientes[3]+i_i+2)*2+*(pd_pendientes[4]+i_i+2));
	}
	
	// Ahora hagamos algún mecanismo de visualización, para ver que todo esté correctamente calculado. Dios que esto va a ser un bardo.
	// Primero visualicemos las pendientes. Para eso voy a armar unos strings que poner en el printeo
	
	char c_npendientes[] = "k1234"; //
	
	for(register int i_i=0; i_i<4; i_i++){
		printf("\n Estas son las pendientes %c%c \n",c_npendientes[0],c_npendientes[i_i+1]);
		Visualizar_d(pd_pendientes[i_i+1]);
	}
	
	// También tengo que visualizar mi vector trabajado.
	
	printf("Este es mi vector antes de evolucionarlo \n");
	Visualizar_d(pd_inicial);
	
	printf("Este es mi vector luego de evolucionarlo \n");
	Visualizar_d(pd_vec);
	

	// Libero el espacio de memoria asignado a los punteros de las pendientes y al pd_inicial
	free(pd_inicial);
	for(int register i_i=0; i_i<5; i_i++) free(pd_pendientes[i_i]);
	
	return 0;
}

// Esta es una función 
double Duplicar(s_Red var, s_Param par){
	// Defino mi variable a usar
	double doble;
	int i_Columnas = var.pd_Opi[1];
	
	// Esta ecuación diferencial me define las pendientes como el doble del valor actual.
	doble = 5*var.pd_Opi[var.i_agente*i_Columnas+var.i_topico+2];
		
	return doble;
}

