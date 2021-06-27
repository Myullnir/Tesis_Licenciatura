//Este es el archivo para testeos

#include<stdio.h>
#include<stdlib.h>
#include<math.h>
#include<time.h>
#include<string.h>


// Acá vienen los structs.
// El struct Red tiene los datos que definen mi red, y la info de la red
typedef struct Red{
	double *pd_Act; // Este vector contiene los valores de actividad de cada uno de los agentes.
	double *pd_Opi; // Este es el vector de opiniones del sistema
	int *pi_Ady; // Matriz de adyacencia que define mis conexiones. Tiene tamaño N*N
	int i_agente; // Entero que representa el agente que estoy mirando. Es un valor que va entre 0 y N-1
	int i_agente2; // Este es el segundo agente con el cual se pone en contacto el primero.
}s_Red;

typedef s_Red *ps_Red;

// El struct de Parametros tiene todos los datos sobre los parámetros del modelo, valga la redundancia
typedef struct Parametros{
	int i_N; // Número de agentes en la red
	int i_T; // Número de tópicos del sistema
	int i_m; // Esto sería el número de conexiones que haría para cada agente que se activa.
	int i_Mopi; // Este es el máximo valor de las opiniones iniciales
	double d_beta; // Este parámetro regula la homofilia del sistema.
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
int Conectar_agentes(ps_Red ps_red, ps_Param ps_datos);
int GenerarOpi(ps_Red ps_var, ps_Param ps_par);
double Norma_d(double *pd_x);


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
	ps_datos->i_T = 2;
	ps_datos->i_m = 3;
	ps_datos->d_epsilon = 0.01;
	ps_datos->d_gamma = 2.1;
	ps_datos->d_beta = 3;
	ps_datos->i_Mopi = 20;
	
	// Inicializo mis punteros
	ps_red->pi_Ady =(int*) malloc((2+ps_datos->i_N*ps_datos->i_N)*sizeof(int));
	for(register int i_i=0; i_i<ps_datos->i_N*ps_datos->i_N+2; i_i++) ps_red->pi_Ady[i_i] = 0;
	ps_red->pi_Ady[0] = ps_datos->i_N; // Pongo el número de filas en la primer coordenada
	ps_red->pi_Ady[1] = ps_datos->i_N; // Pongo el número de columnas en la segunda coordenada
	
	ps_red->pd_Act = (double*) malloc((2+ps_datos->i_N)*sizeof(double));
	for(register int i_i=0; i_i<2+ps_datos->i_N; i_i++) ps_red->pd_Act[i_i] = 0;
	ps_red->pd_Act[0] = 1;
	ps_red->pd_Act[1] = ps_datos->i_N;
	
	ps_red->pd_Opi = (double*) malloc((ps_datos->i_T*ps_datos->i_N+2)*sizeof(double));
	for(register int i_i=0; i_i<2+ps_datos->i_N*ps_datos->i_T; i_i++) ps_red->pd_Opi[i_i] = 0;
	ps_red->pd_Opi[0] = ps_datos->i_N;
	ps_red->pd_Opi[1] = ps_datos->i_T;
	
	// Asigno las actividades a mis agentes
	Actividad(ps_red->pd_Act, ps_datos->d_epsilon, -ps_datos->d_gamma);
	
	// Inicializo mi matriz de opiniones
	GenerarOpi(ps_red, ps_datos);
	
	// Fuerzo a dos agentes a tener la misma opinión
	ps_red->pd_Opi[5*ps_datos->i_T+0+2] = 1;
	ps_red->pd_Opi[5*ps_datos->i_T+1+2] = 1;
	ps_red->pd_Opi[3*ps_datos->i_T+0+2] = 1;
	ps_red->pd_Opi[3*ps_datos->i_T+1+2] = 1;
	
	// Veamos cómo era la matriz de Opiniones cosa de ver que tal eran las chances de conexiones
	printf("La matriz de Opiniones era:\n");
	Visualizar_d(ps_red->pd_Opi);
	
	// // Inicializo mi matriz de Adyacencia
	Adyacencia_Actividad(ps_red, ps_datos);
	
	// Visualicemos cómo quedó la matriz de Adyacencia
	printf("La matriz de Adyacencia era:\n");
	Visualizar_i(ps_red->pi_Ady);
	
	
	
	
	// Ejecuto los comandos finales para medir el tiempo y liberar memoria
	time(&tt_fin);
	free(ps_red->pi_Ady);
	free(ps_red->pd_Opi);
	free(ps_red->pd_Act);
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
	// for(ps_red->i_agente=0; ps_red->i_agente<i_F; ps_red->i_agente++) if(Random()<ps_red->pd_Act[ps_red->i_agente+2]) Conectar_agentes(ps_red, ps_datos);
	
	// Voy a probar conectar algunos agentes a la fuerza
	ps_red->i_agente = 5;
	Conectar_agentes(ps_red,ps_datos);
	
	return 0;
}


// Esta función recibe la matriz de Adyacencia y el agente, y lo conecta con m agentes.
int Conectar_agentes(ps_Red ps_red, ps_Param ps_datos){
	// Defino las variables del tamaño de la matriz y otras que voy a usar
	int i_F,i_C, i_indice, i_libres;
	i_indice = 0;
	i_libres = 0;
	i_F = ps_red->pi_Ady[0];
	i_C = ps_red->pi_Ady[1];
	double d_distancia = 0; // Este es el valor escalar de distancia entre dos opiniones
	double d_probacumulada = 0; // Esta es la probabilidad acumulada de los agentes
	double d_proba = 0; // Esta es la probabilidad que lanzo una sola vez
	
	
	// Armo un vector que voy a usar para samplear elementos y lo inicializo
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
			*(pi_agentes_libres+i_libres+2) = i_i;
			i_libres++;
		}
	}
	
	for(register int i_i=ps_red->i_agente+1; i_i<i_C; i_i++){
		if(ps_red->pi_Ady[ps_red->i_agente*i_F+i_i+2]==0){
			*(pi_agentes_libres+i_libres+2) = i_i;
			i_libres++;
		}
	}
	
	printf("La lista de agentes libres es: \n");
	Visualizar_i(pi_agentes_libres);
	
	// Armo un vector para ver la diferencia entre opiniones. Este vector lo voy a usar primero para calcular la
	// distancia entre agentes y con eso hallar el factor de normalización y sus probabilidades de conexión
	double* pd_DifOpi;
	pd_DifOpi = (double*) malloc((ps_datos->i_T+2)*sizeof(double));
	*pd_DifOpi = 1;
	*(pd_DifOpi+1) = ps_datos->i_T;
	for(register int i_i=0; i_i<ps_datos->i_T; i_i++) *(pd_DifOpi+i_i+2) = 0;
	
	
	// Voy a armar dos vectores más acá el primero es el de Distbeta, el cual me guarda
	// la distancia de cada agente con el agente ps_red->i_agente elevada a la menos beta.
	// El segundo ya toma el valor de normalización y a cada una de estas distancias las normaliza
	// para obtener la probabilidad de interacción por homofilia.
	double* pd_distbeta;
	pd_distbeta = (double*) malloc((ps_datos->i_N+2)*sizeof(double));
	*pd_distbeta = 1;
	*(pd_distbeta+1) = ps_datos->i_N;
	for(register int i_i=0; i_i<ps_datos->i_N; i_i++) *(pd_distbeta+i_i+2) = 0;
	
	double* pd_probabilidades;
	pd_probabilidades = (double*) malloc((ps_datos->i_N+2)*sizeof(double));
	*pd_probabilidades = 1;
	*(pd_probabilidades+1) = ps_datos->i_N;
	for(register int i_i=0; i_i<ps_datos->i_N; i_i++) *(pd_probabilidades+i_i+2) = 0;
	
	
	// Calculo todas las distancias y el factor de normalizacion
	double d_normalizacionP = 0;
	for(register int i_i=0; i_i<i_libres; i_i++){
		i_indice = *(pi_agentes_libres+i_i+2);
		for(register int i_j=0; i_j<ps_datos->i_T; i_j++) *(pd_DifOpi+i_j+2) = ps_red->pd_Opi[ps_red->i_agente*ps_datos->i_T+i_j+2]-ps_red->pd_Opi[i_indice*ps_datos->i_T+i_j+2];
		d_distancia = Norma_d(pd_DifOpi);
		if(d_distancia>0) *(pd_distbeta+i_indice+2) = pow(d_distancia,-ps_datos->d_beta);
		else *(pd_distbeta+i_indice+2) = 0;
	}
	for(register int i_i=0; i_i<ps_datos->i_N; i_i++) d_normalizacionP += *(pd_distbeta+i_i+2); // Esta línea me calcula el factor de normalización
	
	// // Ahora calculo las probabilidades
	for(register int i_i=0; i_i<i_libres; i_i++){
		i_indice = *(pi_agentes_libres+i_i+2);
		for(register int i_j=0; i_j<ps_datos->i_T; i_j++) *(pd_DifOpi+i_j+2) = ps_red->pd_Opi[ps_red->i_agente*ps_datos->i_T+i_j+2]-ps_red->pd_Opi[i_indice*ps_datos->i_T+i_j+2];
		d_distancia = Norma_d(pd_DifOpi);
		if(d_distancia>0) *(pd_probabilidades+i_indice+2) = *(pd_distbeta+i_indice+2)/d_normalizacionP;
		else *(pd_probabilidades+i_indice+2) = 1;
	}
	
	
	// Ahora sampleo m agentes de esta lista
	if(i_libres>ps_datos->i_m){
		int i_contador = 0;
		while(i_contador<ps_datos->i_m){
			printf("El factor de normalizacion es %lf \n", d_normalizacionP);
			i_indice = 0;
			d_proba = Random();
			d_probacumulada = *(pd_probabilidades+2);
			printf("Las probabilidades son: \n");
			Visualizar_d(pd_probabilidades);
			// Defino cuál es el agente que se conecta
			while(d_proba>d_probacumulada){
				i_indice++;
				d_probacumulada += *(pd_probabilidades+i_indice+2);
			}
			// Hago la conexión
			ps_red->pi_Ady[ps_red->i_agente*i_F+i_indice+2] = 1;
			ps_red->pi_Ady[i_indice*i_F+ps_red->i_agente+2] = 1; // Esto se encarga de marcar al sujeto simétrico
			// Saco al agente del grupo de agentes posibles para conectarse al
			// poner su distancia como cero y su probabilidad como cero.
			printf("Conecte al agente %d con el agente %d \n",ps_red->i_agente,i_indice);
			printf("La probabilidad de conectarlos era %lf \n",*(pd_probabilidades+i_indice+2));
			printf("El numero random es %lf y la proba acumulada es %lf \n",d_proba,d_probacumulada);
			*(pd_distbeta+i_indice+2) = 0;
			*(pd_probabilidades+i_indice+2) = 0;
			// Calculo el nuevo factor de normalización y las nuevas probabilidades,
			// ignorando aquellos sujetos cuya distancia es cero. Esto ignora tanto a los
			// ya conectados como a los que tienen distancia cero.
			d_normalizacionP = 0;
			for(register int i_i=0; i_i<ps_datos->i_N; i_i++) d_normalizacionP += *(pd_distbeta+i_i+2);
			for(register int i_i=0; i_i<ps_datos->i_N; i_i++) if(*(pd_distbeta+i_i+2)!=0) *(pd_probabilidades+i_i+2) = *(pd_distbeta+i_i+2)/d_normalizacionP;
			// Avanzo el contador para marcar que hice una conexión
			i_contador++;
		}
	}
	else for(register int i_i=0; i_i<i_libres; i_i++){
		ps_red->pi_Ady[ps_red->i_agente*i_F+*(pi_agentes_libres+i_i+2)+2] = 1;
		ps_red->pi_Ady[*(pi_agentes_libres+i_i+2)*i_F+ps_red->i_agente+2] = 1; // Esto se encarga de marcar al sujeto simétrico
	}
	
	
	free(pi_agentes_libres);
	free(pd_DifOpi);
	free(pd_distbeta);
	free(pd_probabilidades);
	return 0;
}

// Esta función me calcula la norma de un vector
double Norma_d(double *pd_x){
	// Defino mis variables iniciales que son el resultado final, la suma de los cuadrados y el tamao de mi vector
	double d_norm,d_sum = 0;
	int i_C,i_F;
	i_F = *pd_x;
	i_C = *(pd_x+1);
	
	// Calculo la norma como la raíz cuadrada de la sumatoria de los cuadrados de cada coordenada.
	for(register int i_i=0; i_i<i_C*i_F; ++i_i) d_sum += *(pd_x+i_i+2)*(*(pd_x+i_i+2));
	d_norm = sqrt(d_sum);
	return d_norm;
}

// Esta función me genera los vectores opinión iniciales del sistema. Esto es una matriz de tamaño N*T
int GenerarOpi(ps_Red ps_var, ps_Param ps_par){
	// Obtengo las dimensiones de la "matriz" de opiniones de mis agentes.
	int i_F,i_C;
	i_F = (int) ps_var->pd_Opi[0];
	i_C = (int) ps_var->pd_Opi[1];
	
	// Inicializo la "matriz" de opiniones de mis agentes.
	for(register int i_i=0;i_i<i_F*i_C;i_i++) ps_var->pd_Opi[i_i+2] = floor(ps_par->i_Mopi*(Random()-0.5)*2);
	return 0;
}


