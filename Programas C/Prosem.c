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
} s_red;

typedef s_red *ps_red;

// Acá voy a declarar las funciones.------------------------------------

double Random();
int Visualizar_d(double *pd_vec);
int Visualizar_f(float *pf_vec);
int Visualizar_i(int *pi_vec);
double Duplicar(ps_red var);



/*####################################################################################
####################################################################################
####################################################################################
####################################################################################
*/


//---------------------------------------------------------------------------------------------------

// Voy a probar cómo se usan los punteros a struct, escribiendo en ellos, en un puntero de struct
// Y pasando el puntero a una función simple.

int main(){
	// Defino mis variables temporales para medir el tiempo que tarda el programa. También genero una nueva semilla
	time_t tt_prin,tt_fin;
	time(&tt_prin);
	srand(time(NULL));
	int i_tardanza;
	
	
	// Defino el puntero a mi struct y lo inicializo.
	ps_red ps_inicial;
	ps_inicial = malloc(sizeof(s_red));
	
	// Malloqueo los punteros dentro de mis structs y los inicializo.
	ps_inicial->pd_Ang = (double*) malloc((15+2)*sizeof(double));
	ps_inicial->pd_Opi = (double*) malloc((15+2)*sizeof(double));
	ps_inicial->pi_Ady = (int*) malloc((15+2)*sizeof(int));
	
	ps_inicial->pd_Ang[0] = 1;
	ps_inicial->pd_Opi[0] = 1;
	ps_inicial->pi_Ady[0] = 1;
	
	ps_inicial->pd_Ang[1] = 15;
	ps_inicial->pd_Opi[1] = 15;
	ps_inicial->pi_Ady[1] = 15;
	
	for(register int i_i=0; i_i<15; i_i++){
		ps_inicial->pd_Ang[i_i+2] = i_i;
		ps_inicial->pi_Ady[i_i+2] = i_i;
		ps_inicial->pd_Opi[i_i+2] = i_i;
	}
	
	ps_inicial->i_agente = 1;
	ps_inicial->i_topico = 1;
	
	// Veamos que los punteros están bien escritos
	printf("Puntero Uno \n");
	Visualizar_d(ps_inicial->pd_Ang);
	printf("Puntero Dos  \n");
	Visualizar_d(ps_inicial->pd_Opi);
	printf("Puntero Tres \n");
	Visualizar_i(ps_inicial->pi_Ady);
	
	// Veamos cómo funca una función que recibe un puntero a struct
	printf("Doble del puntero Dos\n");
	for(ps_inicial->i_agente = 1; ps_inicial->i_agente <10; ps_inicial->i_agente++) printf("%d ",(int) Duplicar(ps_inicial));
	printf("\n");

	
	// Ejecuto los comandos finales para medir el tiempo.
	free(ps_inicial->pd_Opi);
	free(ps_inicial->pd_Ang);
	free(ps_inicial->pi_Ady);
	free(ps_inicial);
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
	
	return 0;
}


// Esta es una función 
double Duplicar(ps_red var){
	// Defino mi variable a usar
	double doble;
	
	// Esta ecuación diferencial me define las pendientes como el doble del valor actual.
	doble = 2*var->pd_Opi[var->i_agente+var->i_topico+2];
		
	return doble;
}

