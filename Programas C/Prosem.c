//Este es el archivo para testeos

#include<stdio.h>
#include<stdlib.h>
#include<math.h>
#include<time.h>

// Acá vienen los structs.
// El struct Red tiene los datos que definen mi red, y la info de la red
struct Red{
	double *pd_Ang; // Matriz de superposición entre tópicos. Tiene tamaño T*T
	int *pi_Ady; // Matriz de adyacencia que define mis conexiones. Tiene tamaño N*N
	double *pd_Opi; // Vector de opinión de cada individuo
};

struct Parametros{
	float f_Beta; // Exponente que regula el grado de homofilia
	float f_Pint; // Probabilidad de que se forme el enlace de manera aleatoria
	float f_K; // Influencia social
	float f_alfa; // Controversialidad de los temas
	int i_N; // Número de agentes en la red
	int i_T; // Cantidad de tópicos
	int i_Mopi; // Máximo inicial de opiniones
	float f_dt; // Paso temporal de iteración del sistema
};

// Acá voy a declarar las funciones.------------------------------------

double Random();
int Visualizar(struct Red var, int i_Crit);
int GenerarOpi(struct Red var, struct Parametros par);
int GenerarAng(struct Red var);
int GenerarAdy(struct Red var, struct Parametros par);
double Din1(struct Red var, struct Parametros par, int i_i, int i_j, int i_v);



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
	struct Red red;
	struct Parametros datos;
	datos.f_Beta = 0.5;
	datos.f_Pint = 1;
	datos.f_K = 1;
	datos.f_alfa = 1;
	datos.i_N = 2;
	datos.i_T = 3;
	datos.i_Mopi = 3;
	datos.f_dt = 0.5;
	
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
	
	// Visualizo las redes para ver que todo funca bien
	Visualizar(red,0);
	Visualizar(red,1);
	Visualizar(red,2);
	
	// Evolución dinámica del sistema
	double d_prueba;
	d_prueba = Din1(red,datos,0,1,0);
	printf("El termino dentro de la sumatoria me dio %.5lf\n",d_prueba);
	
	
	// Ejecuto los comandos finales para medir el tiempo.
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


// Esta función es para observar los vectores de opinión, la matriz de superposición y la matriz de adyacencia
int Visualizar(struct Red var, int i_Crit){
	if(i_Crit==0){ //En este caso observo los vectores de opinión
		
		// Obtengo las dimensiones de la "matriz" de vectores de opinión
		int i_Filas,i_Columnas;
		i_Filas = (int) var.pd_Opi[0];
		i_Columnas = (int) var.pd_Opi[1];
		
		// Imprimo la "matriz" en la consola
		printf("Visualizo el conjunto de vectores de opinion \n");
		for(int i_i=0; i_i<i_Filas; i_i++){
			for(int i_j=0; i_j<i_Columnas; i_j++) printf("%lf\t",var.pd_Opi[i_i*i_Columnas+i_j+2]);
			printf("\n");
		}
	}
	else if(i_Crit==1){ // En este caso observo la matriz de Superposición
	
		// Obtengo las dimensiones de la matriz de Superposición
		int i_Filas,i_Columnas;
		i_Filas = (int) var.pd_Ang[0];
		i_Columnas = (int) var.pd_Ang[1];
		
		// Imprimo la matriz en la consola
		printf("Visualizo la matriz de Superposicion entre Topicos \n");
		for(int i_i=0; i_i<i_Filas; i_i++){
			for(int i_j=0; i_j<i_Columnas; i_j++) printf("%lf\t",var.pd_Ang[i_i*i_Columnas+i_j+2]);
			printf("\n");
		}
	}
	else if(i_Crit==2){ // En este caso observo la matriz de adyacencia
	
		// Obtengo las dimensiones de la matriz de Adyacencia
		int i_Filas,i_Columnas;
		i_Filas = var.pi_Ady[0];
		i_Columnas = var.pi_Ady[1];
		
		// Imprimo la matriz en la consola
		printf("Visualizo la matriz de Adyacencia del sistema \n");
		for(int i_i=0; i_i<i_Filas; i_i++){
			for(int i_j=0; i_j<i_Columnas; i_j++) printf("%d\t",var.pi_Ady[i_i*i_Columnas+i_j+2]);
			printf("\n");
			printf("\n");
		}
	}
	return 0;
}


// Esta función me genera los vectores opinión iniciales del sistema. Esto es una matriz de tamaño N*T
int GenerarOpi(struct Red var, struct Parametros par){
	// Obtengo las dimensiones de la "matriz" de opiniones de mis agentes.
	int i_Filas,i_Columnas;
	i_Filas = (int) var.pd_Opi[0];
	i_Columnas = (int) var.pd_Opi[1];
	
	// Inicializo la "matriz" de opiniones de mis agentes.
	for(int i_i=0;i_i<i_Filas*i_Columnas;i_i++) var.pd_Opi[i_i+2] = par.i_Mopi*(Random()-0.5)*2;
	return 0;
}

// Esta función me genera la matriz de Superposicion del sistema. Esto es una matriz de T*T
int GenerarAng(struct Red var){
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
int GenerarAdy(struct Red var, struct Parametros par){
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
double Din1(struct Red var, struct Parametros par, int i_i, int i_j, int i_v){
	
	// Defino las variables locales de mi función. d_resultados es el return. 
	// d_opiniones_superpuestas es el producto de la matriz de superposición de tópicos con el vector opinión de un agente.
	double d_resultado,d_opiniones_superpuestas = 0;
	
	// Obtengo el tamaño de columnas de mis tres matrices
	int i_Co,i_Cs,i_Ca;
	i_Co = var.pd_Opi[1];
	i_Cs = var.pd_Ang[1];
	i_Ca = var.pi_Ady[1];
	
	for(register int i_p=0; i_p<i_Cs; i_p++) d_opiniones_superpuestas += var.pd_Ang[i_v*i_Cs+i_p+2]*var.pd_Opi[i_j*i_Co+i_p+2]; // Calculo previamente este producto de la matriz con el vector.
	d_resultado = var.pi_Ady[i_i*i_Ca+i_j+2]*tanh(par.f_alfa*d_opiniones_superpuestas); // Esto es lo que está dentro de la sumatoria en la ecuación dinámica.
	return d_resultado; // La función devuelve el número que buscás, no te lo asigna en una variable.
}



//#######################################################################################
