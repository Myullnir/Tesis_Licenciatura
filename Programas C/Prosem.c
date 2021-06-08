//Este es el archivo para testeos

#include<stdio.h>
#include<stdlib.h>
#include<math.h>
#include<time.h>
#include<string.h>


// Acá vienen los structs.
// El struct Red tiene los datos que definen mi red, y la info de la red
typedef struct Red{
	double *pd_actividad; // Este vector contiene los valores de actividad de cada uno de los agentes.
	int *pi_Ady; // Matriz de adyacencia que define mis conexiones. Tiene tamaño N*N
	int i_agente; // Entero que representa el agente que estoy mirando. Es un valor que va entre 0 y N-1
	int i_agente2; // Este es el segundo agente con el cual se pone en contacto el primero.
}s_Red;

typedef s_Red *ps_Red;

// El struct de Parametros tiene todos los datos sobre los parámetros del modelo, valga la redundancia
typedef struct Parametros{
	int i_N; // Número de agentes en la red
	int i_m; // Esto sería el número de conexiones que haría para cada agente que se activa.
	double d_epsilon; // Actividad mínima de los agentes
	double d_gamma; // Potencia de la distribución de probabilidades de la actividad. Es el valor positivo.
}s_Param;

typedef s_Param *ps_Param;




double Random();
int Visualizar_i(int *pi_vec);
int Visualizar_d(double *pd_vec);
int Actividad(double* pd_vec, double d_epsilon, double d_potencia);
int Escribir_d(double *pd_vec, FILE *pa_archivo);
int Adyacencia_Actividad(ps_Red ps_red, ps_Param ps_datos);
int Conectar_agentes(ps_Red ps_red, int i_m);


int main(int argc, char *argv[]){
	// Defino mis variables temporales para medir el tiempo que tarda el programa. También genero una nueva semilla
	time_t tt_prin,tt_fin;
	time(&tt_prin);
	srand(time(NULL));
	int i_tardanza;
	
	// Defino mis punteros a structs
	ps_Red ps_red;
	ps_red = malloc(sizeof(s_Red));
	
	ps_Param ps_datos;
	ps_datos = malloc(sizeof(s_Param));
	
	// Inicializo mis datos
	ps_datos->i_N = 20;
	ps_datos->i_m = 5;
	ps_datos->d_epsilon = 0.01;
	ps_datos->d_gamma = 2.1;
	
	// Inicializo mis punteros
	ps_red->pi_Ady =(int*) malloc((2+ps_datos->i_N*ps_datos->i_N)*sizeof(int));
	for(register int i_i=0; i_i<ps_datos->i_N*ps_datos->i_N+2; i_i++) ps_red->pi_Ady[i_i] = 0;
	ps_red->pi_Ady[0] = ps_datos->i_N; // Pongo el número de filas en la primer coordenada
	ps_red->pi_Ady[1] = ps_datos->i_N; // Pongo el número de columnas en la segunda coordenada
	
	ps_red->pd_actividad = (double*) malloc((2+ps_datos->i_N)*sizeof(double));
	for(register int i_i=0; i_i<2+ps_datos->i_N; i_i++) ps_red->pd_actividad[i_i] = 0;
	ps_red->pd_actividad[0] = 1;
	ps_red->pd_actividad[1] = ps_datos->i_N;
	
	// Asigno las actividades a mis agentes
	Actividad(ps_red->pd_actividad, ps_datos->d_epsilon, -ps_datos->d_gamma);
	
	// Visualizo mi red antes de generarla
	// Visualizar_i(ps_red->pi_Ady);
	
	// Armo mi matriz de actividad y luego la visualizo
	Adyacencia_Actividad(ps_red,ps_datos);
	Visualizar_i(ps_red->pi_Ady);
	printf("\n");
	
	// Lo repito sólo para ver que efectivamente la red se desarma en cada nueva iteración
	// Adyacencia_Actividad(ps_red,ps_datos);
	// Visualizar_i(ps_red->pi_Ady);
	// printf("\n");
	
	// Finalmente escribo mis valores de actividad, como para ver si alguno tenía una actividad alta y eso tiene sentido con lo observado.
	Visualizar_d(ps_red->pd_actividad);
	
	
	// Ejecuto los comandos finales para medir el tiempo y liberar memoria
	time(&tt_fin);
	free(ps_red->pi_Ady);
	free(ps_red->pd_actividad);
	free(ps_red);
	free(ps_datos);
	i_tardanza = tt_fin-tt_prin;
	printf("Tarde %d segundos en terminar",i_tardanza);
		
	return 0;
}

//###########################################################

// Esta función me genera un número random entre 0 y 1
double Random(){
	return ((double) rand()/(double) RAND_MAX);
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


// Programemos la función que debería devolver un valor de actividad
int Actividad(double* pd_vec, double d_epsilon, double d_potencia){
	// Defino las variables que voy a necesitar que son la probabilidad, la probabilidad mínima, La F del Epsilon
	double d_Feps;
	
	// Defino acá la cantidad de filas y de columnas de mi vector de double donde voy a guardar las actividades
	int i_F,i_C;
	i_F = (int) *pd_vec;
	i_C = (int) *(pd_vec+1);
	
	// Hago unas cuentas para tener de antemano
	d_Feps = pow(d_epsilon,d_potencia+1); // Esto lo hago para no rehacer esta cuenta mil veces en el camino
	
	for(register int i_i=0; i_i<i_F*i_C;i_i++){
		*(pd_vec+i_i+2) = pow((1-d_Feps)*Random()+d_Feps,1/(d_potencia+1));
	}
	
	return 0;
}


// Esta función va a recibir un vector int y va a escribir ese vector en mi archivo.
int Escribir_i(int *pi_vec, FILE *pa_archivo){
	// Defino las variables del tamao de mi vector
	int i_C,i_F;
	i_F = *pi_vec;
	i_C = *(pi_vec+1);
	
	// Ahora printeo todo el vector en mi archivo
	for(register int i_i=0; i_i<i_C*i_F; i_i++) fprintf(pa_archivo,"\t%d",*(pi_vec+i_i+2));
	fprintf(pa_archivo,"\n");
	
	return 0;
}


// Esta función va a recibir un vector double y va a escribir ese vector en mi archivo.
int Escribir_d(double *pd_vec, FILE *pa_archivo){
	// Defino las variables del tamao de mi vector
	int i_C,i_F;
	i_F = *pd_vec;
	i_C = *(pd_vec+1);
	
	// Ahora printeo todo el vector en mi archivo
	for(register int i_i=0; i_i<i_C*i_F; i_i++) fprintf(pa_archivo,"\t%.6lf",*(pd_vec+i_i+2));
	fprintf(pa_archivo,"\n");
	
	return 0;
}


// Esta función va a recibir a la matriz de adyacencia y la va a armar según la actividad de los agentes
// Creo que voy a cambiar esto en la función haciendo que directamente reciba los punteros de struct de Red
// y de Parametros
int Adyacencia_Actividad(ps_Red ps_red, ps_Param ps_datos){
	// Primero armo las variables que voy a necesitar, como el tamaño de mis vectores
	int i_F,i_C;
	i_F = ps_red->pi_Ady[0];
	i_C = ps_red->pi_Ady[1];
	
	// Desarmo todos los enlaces de la red
	for(register int i_i=0; i_i<i_F*i_C; i_i++) ps_red->pi_Ady[i_i+2] = 0;
	
	// Ahora reviso todos los agentes, los intento activar y si se activa lo conecto con m agentes.
	for(ps_red->i_agente=0; ps_red->i_agente<i_F; ps_red->i_agente++) if(Random()<ps_red->pd_actividad[ps_red->i_agente+2]){
		printf("Se activo el agente %d\n",ps_red->i_agente);
		Conectar_agentes(ps_red, ps_datos->i_m);
	}
	
	return 0;
}


// Esta función recibe la matriz de Adyacencia y el agente, y lo conecta con m agentes.
int Conectar_agentes(ps_Red ps_red, int i_m){
	// Defino las variables del tamaño de la matriz y un vector que voy a usar para samplear elementos. Inicializo el vector
	int i_F,i_C, i_indice;
	i_indice = 0;
	i_F = ps_red->pi_Ady[0];
	i_C = ps_red->pi_Ady[1];
	int* pi_agentes_libres;
	pi_agentes_libres = (int*) malloc((i_C+2)*sizeof(int));
	*pi_agentes_libres = 1;
	*(pi_agentes_libres+1) = i_C;
	for(register int i_i=0; i_i<i_C; i_i++) *(pi_agentes_libres+i_i+2) = 0;
	
	// Reviso la fila de la matriz de adyacencia del agente i_agente, y me guardo los números de los agentes
	// que no tienen conexión con i_agente. Lo separo en dos fors, porque la idea es saltear el caso
	// de i_i = ps_red->i_agente
	for(register int i_i=0; i_i<ps_red->i_agente; i_i++){
		if(ps_red->pi_Ady[ps_red->i_agente*i_F+i_i+2]==0){
			*(pi_agentes_libres+i_indice+2) = i_i;
			i_indice++;
		}
	}
	
	for(register int i_i=ps_red->i_agente+1; i_i<i_C; i_i++){
		if(ps_red->pi_Ady[ps_red->i_agente*i_F+i_i+2]==0){
			*(pi_agentes_libres+i_indice+2) = i_i;
			i_indice++;
		}
	}
	
	// Ahora sampleo m agentes de esta lista. ¿Podría pasar que un agente no tenga 10 sujetos con los
	// cuales conectarse? Eso requeriría que tenga un grado de 990 para arrancar. Muy poco probable.
	// Igual después armo una solución para ese caso.
	if(i_indice>9){
		for(register int i_i=0; i_i<i_m; i_i++){
			printf("Los agentes disponibles son: ");
			Visualizar_i(pi_agentes_libres);
			ps_red->i_agente2 = rand()%i_indice;
			ps_red->pi_Ady[ps_red->i_agente*i_F+*(pi_agentes_libres+ps_red->i_agente2+2)+2] = 1;
			ps_red->pi_Ady[*(pi_agentes_libres+ps_red->i_agente2+2)*i_F+ps_red->i_agente+2] = 1; // Esto se encarga de marcar al sujeto simétrico
			printf("Lo conecte con el agente %d\n",*(pi_agentes_libres+ps_red->i_agente2+2));
			for(register int i_j=ps_red->i_agente2; i_j<*(pi_agentes_libres+1)-1; i_j++) *(pi_agentes_libres+i_j+2) =  *(pi_agentes_libres+i_j+1+2);
			i_indice--;
		}
	}
	else for(register int i_i=0; i_i<i_indice; i_i++){
		ps_red->pi_Ady[ps_red->i_agente*i_F+*(pi_agentes_libres+i_i+2)+2] = 1;
		ps_red->pi_Ady[*(pi_agentes_libres+i_i+2)*i_F+ps_red->i_agente+2] = 1; // Esto se encarga de marcar al sujeto simétrico
	}
		
	
	free(pi_agentes_libres);
	return 0;
}

