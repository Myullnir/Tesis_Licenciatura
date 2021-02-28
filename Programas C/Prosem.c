//Este es el archivo para testeos

#include<stdio.h>
#include<stdlib.h>
#include<math.h>
#include<time.h>


// Acá vienen los structs.
// El struct Red tiene los datos que definen mi red, y la info de la red
typedef struct Red{
	int *pi_Ady; // Matriz de adyacencia que define mis conexiones. Tiene tamaño N*N
}s_Red;

typedef s_Red *ps_Red;

typedef struct Parametros{
	float f_Pint; // Probabilidad de que se forme el enlace de manera aleatoria
	float f_Gradomedio; // Este es el grado medio de los agentes de la red.
	int i_N; // Número de agentes en la red
}s_Param;

typedef s_Param *ps_Param;


int Visualizar_i(int *pi_vec);
double Random();
int Inicializar_Adyacencia(int *pi_adyacencia);
int GenerarAdy(ps_Red ps_var, ps_Param ps_par);
int Tamaño_Comunidad(int *pi_adyacencia,int i_inicial);


int main(){
	// Defino mis variables temporales para medir el tiempo que tarda el programa. También genero una nueva semilla
	time_t tt_prin,tt_fin;
	time(&tt_prin);
	srand(time(NULL));
	int i_tardanza;
	
	// Defino los punteros a Structs
	ps_Red ps_red1;
	ps_red1 = malloc(sizeof(s_Red));
	
	ps_Param ps_datos;
	ps_datos = malloc(sizeof(s_Param));
	
	// Defino los parámetros de la red
	ps_datos->f_Gradomedio = 8;
	ps_datos->i_N = 1000;
	ps_datos->f_Pint = ps_datos->f_Gradomedio/(ps_datos->i_N-1);
	int i_tamaño = 0; // Esto me mide el tamaño del grupo medido en la red.
	int i_contador = 0; // Esto me sirve para contar cuantas veces se cumple que la red es conexa.
	
	
	// Defino el puntero a mi matriz, lo malloqueo y lo inicializo
	ps_red1->pi_Ady = (int*) malloc((2+ps_datos->i_N*ps_datos->i_N)*sizeof(int));
	ps_red1->pi_Ady[0] = ps_datos->i_N;
	ps_red1->pi_Ady[1] = ps_datos->i_N;
	for(register int i_i=0; i_i<ps_datos->i_N*ps_datos->i_N; i_i++) ps_red1->pi_Ady[i_i+2] = 0;
	
	// Inicializo la matriz de manera aleatoria para ver si se genera una única componente gigante
	// Calculo el tamaño de un grupo en la red. Si el tamaño es menor que el total de agentes, arranco de nuevo.
	do{
		GenerarAdy(ps_red1,ps_datos);
		i_tamaño = Tamaño_Comunidad(ps_red1->pi_Ady, 0);
		if(i_tamaño == ps_datos->i_N){
			i_contador +=1;
			printf("El tamano de la red es: %d\n", i_tamaño);
			break;
		}
		printf("El número del contador es: %d\n",i_contador);
	}
	while(i_contador < 10);
	printf("El número del contador es: %d\n",i_contador);

	// Ejecuto los comandos finales para medir el tiempo y liberar memoria
	free(ps_red1->pi_Ady);
	free(ps_red1);
	free(ps_datos);
	time(&tt_fin);
	i_tardanza = tt_fin-tt_prin;
	printf("Tarde %d segundos en terminar",i_tardanza);

	return 0;
}




//###########################################################
//###########################################################
//###########################################################


// Funciones

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

// Esta función me genera un número random entre 0 y 1
double Random(){
	return ((double) rand()/(double) RAND_MAX);
}

// Esta función me inicializa una red de 20 agentes conectados en tres grupos, uno de 7 agentes, uno de 5 y uno de 8.
// Los primeros 7 agentes son un grupo, del 8 al 12 son otro grupo y el último son los agentes del 13 al 20
int Inicializar_Adyacencia(int *pi_adyacencia){
	// Defino el tamaño de mi vector y lo guardo en variables
	int i_C;
	i_C = *(pi_adyacencia+1);
	
	// Este es el primer grupo
	
		// Armo la primer fila
		*(pi_adyacencia+1+2) = 1; // Conecta con 2
		*(pi_adyacencia+4+2) = 1; // Conecta con 5
		*(pi_adyacencia+6+2) = 1; // Conecta con 7
		
		// Armo la segunda fila
		*(pi_adyacencia+i_C+2) = 1; // Conecta con 1
		*(pi_adyacencia+2+i_C+2) = 1; // Conecta con 3
		*(pi_adyacencia+3+i_C+2) = 1; // Conecta con 4
		*(pi_adyacencia+4+i_C+2) = 1; // Conecta con 5
		*(pi_adyacencia+5+i_C+2) = 1; // Conecta con 6
		*(pi_adyacencia+6+i_C+2) = 1; // Conecta con 7
		
		// Armo la tercera fila
		*(pi_adyacencia+1+2*i_C+2) = 1; // Conecta con 2
		*(pi_adyacencia+3+2*i_C+2) = 1; // Conecta con 4
		*(pi_adyacencia+4+2*i_C+2) = 1; // Conecta con 5
		
		// Armo la cuarta fila
		*(pi_adyacencia+1+3*i_C+2) = 1; // Conecta con 2
		*(pi_adyacencia+2+3*i_C+2) = 1; // Conecta con 3
		*(pi_adyacencia+4+3*i_C+2) = 1; // Conecta con 5
		
		// Armo la quinta fila
		*(pi_adyacencia+4*i_C+2) = 1; // Conecta con 1
		*(pi_adyacencia+1+4*i_C+2) = 1; // Conecta con 2
		*(pi_adyacencia+2+4*i_C+2) = 1; // Conecta con 3
		*(pi_adyacencia+3+4*i_C+2) = 1; // Conecta con 4
		*(pi_adyacencia+5+4*i_C+2) = 1; // Conecta con 6
		
		// Armo la sexta fila
		*(pi_adyacencia+1+5*i_C+2) = 1; // Conecta con 2
		*(pi_adyacencia+4+5*i_C+2) = 1; // Conecta con 5
		*(pi_adyacencia+5+5*i_C+2) = 1; // Conecta con 6
		
		// Armo la septima fila
		*(pi_adyacencia+6*i_C+2) = 1; // Conecta con 1
		*(pi_adyacencia+1+6*i_C+2) = 1; // Conecta con 2
		*(pi_adyacencia+5+6*i_C+2) = 1; // Conecta con 6
	
	// Este es el segundo grupo
	
		// Armo la octava fila
		*(pi_adyacencia+9+7*i_C+2) = 1; // Conecta con 10
		*(pi_adyacencia+10+7*i_C+2) = 1; // Conecta con 11
		
		// Armo la novena fila
		*(pi_adyacencia+10+8*i_C+2) = 1; // Conecta con 11
		*(pi_adyacencia+11+8*i_C+2) = 1; // Conecta con 12
		
		// Armo la decima fila
		*(pi_adyacencia+7+9*i_C+2) = 1; // Conecta con 8
		*(pi_adyacencia+10+9*i_C+2) = 1; // Conecta con 11
		
		// Armo la onceava fila
		*(pi_adyacencia+7+10*i_C+2) = 1; // Conecta con 8
		*(pi_adyacencia+8+10*i_C+2) = 1; // Conecta con 9
		*(pi_adyacencia+9+10*i_C+2) = 1; // Conecta con 10
		*(pi_adyacencia+11+10*i_C+2) = 1; // Conecta con 12
		
		// Armo la doceava fila
		*(pi_adyacencia+8+11*i_C+2) = 1; // Conecta con 9
		*(pi_adyacencia+10+11*i_C+2) = 1; // Conecta con 11
		
	// Este es el tercer grupo
	
		// Armo la treceava fila
		*(pi_adyacencia+13+12*i_C+2) = 1; // Conecta con 14
		*(pi_adyacencia+15+12*i_C+2) = 1; // Conecta con 16
		*(pi_adyacencia+16+12*i_C+2) = 1; // Conecta con 17
		
		// Armo la catorceava fila
		*(pi_adyacencia+12+13*i_C+2) = 1; // Conecta con 13
		
		// Armo la quinceava fila
		*(pi_adyacencia+15+14*i_C+2) = 1; // Conecta con 16
		
		// Armo la decimo sexta fila
		*(pi_adyacencia+12+15*i_C+2) = 1; // Conecta con 13
		*(pi_adyacencia+14+15*i_C+2) = 1; // Conecta con 15
		*(pi_adyacencia+16+15*i_C+2) = 1; // Conecta con 17
		
		// Armo la decimo séptima fila
		*(pi_adyacencia+12+16*i_C+2) = 1; // Conecta con 13
		*(pi_adyacencia+15+16*i_C+2) = 1; // Conecta con 16
		*(pi_adyacencia+17+16*i_C+2) = 1; // Conecta con 18
		*(pi_adyacencia+18+16*i_C+2) = 1; // Conecta con 19
		*(pi_adyacencia+19+16*i_C+2) = 1; // Conecta con 20
		
		// Armo la decimo octava fila
		*(pi_adyacencia+16+17*i_C+2) = 1; // Conecta con 17
		*(pi_adyacencia+18+17*i_C+2) = 1; // Conecta con 19
		*(pi_adyacencia+19+17*i_C+2) = 1; // Conecta con 20
		
		// Armo la decimo novena fila
		*(pi_adyacencia+16+18*i_C+2) = 1; // Conecta con 17
		*(pi_adyacencia+17+18*i_C+2) = 1; // Conecta con 18
		
		// Armo la vigésima fila
		*(pi_adyacencia+16+19*i_C+2) = 1; // Conecta con 17
		*(pi_adyacencia+17+19*i_C+2) = 1; // Conecta con 18
		
	// Con eso están armados los tres grupos
	
	return 0;
}

// Esta función me inicializa la matriz de Adyacencia. Esto es una matriz de N*N
int GenerarAdy(ps_Red ps_var, ps_Param ps_par){
	// Obtengo las dimensiones de la matriz de Adyacencia.
	int i_F,i_C;
	i_F = (int) ps_var->pi_Ady[0];
	i_C = (int) ps_var->pi_Ady[1];
	
	// Inicializo la matriz de Adyacencia de mi sistema
	for(register int i_i=0; i_i<i_F; i_i++) {
		for(register int i_j=0; i_j<i_i; i_j++) {
			// Saco un número random y veo si asigno un 1 o un 0 a esa posición
			if(Random()< ps_par->f_Pint) ps_var->pi_Ady[i_i*i_C+i_j+2] = 1;
			else ps_var->pi_Ady[i_i*i_C+i_j+2] = 0;
		}
	}
	for(register int i_i=0; i_i<i_F; i_i++) for(register int i_j=i_i+1; i_j<i_C; i_j++) ps_var->pi_Ady[i_i*i_C+i_j+2] = ps_var->pi_Ady[i_j*i_C+i_i+2]; // Esta sola línea simetriza la matriz
	for(register int i_i=0; i_i<i_F; i_i++) ps_var->pi_Ady[i_i*i_C+i_i+2] = 0; // Esto me pone 0 en toda la diagonal
	return 0;
}

// Esta función me mide el tamaño del grupo al cual pertenece el nodo inicial i_inicial
int Tamaño_Comunidad(int *pi_adyacencia, int i_inicial){
	// Defino la variable del tamaño del grupo, el número de filas de la matriz de Adyacencia, el número de agentes
	// restantes por visitar; y los inicializo
	int i_tamaño, i_F, i_restantes;
	i_tamaño = 0;
	i_F = *pi_adyacencia;
	i_restantes = 0;
	
	// Defino un puntero que registre cuáles agentes están conectados y lo inicializo
	int *pi_Grupo;
	pi_Grupo = (int*) malloc((2+i_F)*sizeof(int));
	
	*pi_Grupo = 1;
	*(pi_Grupo+1) = i_F;
	for(register int i_i=0; i_i<i_F; i_i++) *(pi_Grupo+i_i+2) = 0;
	
	// Defino un puntero que me marque los nuevos sujetos que visitar. Lo hago de tamaño i_F para poder asignar un 1 al visitar el agente en cada posición correcta.
	int *pi_Visitar;
	pi_Visitar = (int*) malloc((2+i_F)*sizeof(int));
	
	*pi_Visitar = 1;
	*(pi_Visitar+1) = i_F;
	for(register int i_i=0; i_i<i_F; i_i++) *(pi_Visitar+i_i+2) = 0;
	
	// Empiezo recorriendo la matriz desde un nodo inicial, que será el primero siempre.
	for(register int i_i=0; i_i<i_F; i_i++){
		*(pi_Grupo+i_i+2) = *(pi_adyacencia+i_i+i_inicial*i_F+2);
		*(pi_Visitar+i_i+2) = *(pi_adyacencia+i_i+i_inicial*i_F+2);
	}
	
	do{
		i_restantes = 0;
		// Primero reviso mi lista de gente por visitar
		for(register int i_i=0; i_i<i_F; i_i++){
			// Si encuentro un uno en la lista, reviso esa fila de la matriz de adyacencia. Es decir, la fila i_i
			if(*(pi_Visitar+i_i+2) == 1){
				// Si en esa fila encuentro un uno, tengo que agregar eso al grupo y a la lista de Visitar. Pero no siempre.
				// La idea es: Si el sujeto no estaba marcado en grupo, entonces lo visito y lo marco en el grupo.
				// Si ya estaba marcado, es porque lo visité o está en mi lista de visitar.
				// La idea de esto es no revisitar nodos ya visitados.
				for(register int i_j=0; i_j<i_F; i_j++){
					if(*(pi_adyacencia+i_j+i_i*i_F+2) == 1){
						if(*(pi_Grupo+i_j+2) == 0) *(pi_Visitar+i_j+2) = 1; // Esta línea me agrega el sujeto a visitar sólo si no estaba en el grupo
						*(pi_Grupo+i_j+2) = *(pi_adyacencia+i_j+i_i*i_F+2); // Esta línea me marca al sujeto en el grupo, porque al final si ya había un uno ahí, simplemente lo vuelve a escribir.
					}
				}
				*(pi_Visitar+i_i+2) = 0;
			}
		}
		for(int register i_i=0; i_i<i_F; i_i++) i_restantes += *(pi_Visitar+i_i+2);
	}
	while(i_restantes > 0);
	
	// Finalmente mido el tamaño de mi grupo
	for(register int i_i=0; i_i<i_F; i_i++) i_tamaño += *(pi_Grupo+i_i+2);
	
	// Libero las memorias malloqueadas
	free(pi_Grupo);
	free(pi_Visitar);
	
	return i_tamaño;
}

