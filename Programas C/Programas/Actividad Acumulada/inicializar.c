// En este archivo me defino las funciones que inicializan, pero no las declaro

#include<stdio.h>
#include<stdlib.h>
#include<math.h>
#include<string.h>
#include "general.h"
#include "TTanh.h"
#include "inicializar.h"


// Esta función me genera los vectores opinión iniciales del sistema. Esto es una matriz de tamaño N*T
int GenerarOpi(ps_Red ps_var, ps_Param ps_par){
	// Obtengo las dimensiones de la "matriz" de opiniones de mis agentes.
	int i_F,i_C;
	i_F = (int) ps_var->pd_Opi[0];
	i_C = (int) ps_var->pd_Opi[1];
	double d_varianza;
	d_varianza = sqrt(2.5);
	
	// Inicializo la "matriz" de opiniones de mis agentes.
	for(register int i_i=0;i_i<i_F*i_C;i_i++) ps_var->pd_Opi[i_i+2] = Gaussiana(0,d_varianza);
	return 0;
}

// Esta función me genera la matriz de Superposicion del sistema. Esto es una matriz de T*T
int GenerarAng(ps_Red ps_var, ps_Param ps_par){
	// Obtengo las dimensiones de la matriz de Superposicion.
	int i_F,i_C;
	i_F = (int) ps_var->pd_Ang[0];
	i_C = (int) ps_var->pd_Ang[1];
	
	// Inicializo la matriz de Superposicion de mi sistema.
	for(register int i_i=0; i_i<i_F; i_i++) for(register int i_j=0; i_j<i_i; i_j++) ps_var->pd_Ang[i_i*i_C+i_j+2] = ps_par->f_Cosangulo; //*(((-i_i-i_j)%2)*2+1); // Decidí poner 0.5 entre todos los tópicos de mi modelo
	for(register int i_i=0; i_i<i_F; i_i++) ps_var->pd_Ang[i_i*i_C+i_i+2] = 1; // Esto me pone 1 en toda la diagonal
	for(register int i_i=0; i_i<i_F; i_i++) for(register int i_j=i_i+1; i_j<i_C; i_j++) ps_var->pd_Ang[i_i*i_C+i_j+2] = ps_var->pd_Ang[i_j*i_C+i_i+2]; // Esta sola línea simetriza la matriz
	return 0;
}


// // Esta función me inicializa la matriz de Adyacencia. Esto es una matriz de N*N
// int GenerarAdy(ps_Red ps_var, ps_Param ps_par){
	// // Obtengo las dimensiones de la matriz de Adyacencia.
	// int i_F,i_C;
	// i_F = (int) ps_var->pi_Ady[0];
	// i_C = (int) ps_var->pi_Ady[1];
	
	// // Inicializo la matriz de Adyacencia de mi sistema
	// for(register int i_i=0; i_i<i_F; i_i++) {
		// for(register int i_j=0; i_j<i_i; i_j++) {
			// // Saco un número random y veo si asigno un 1 o un 0 a esa posición
			// if(Random()< ps_par->f_Pint) ps_var->pi_Ady[i_i*i_C+i_j+2] = 1;
			// else ps_var->pi_Ady[i_i*i_C+i_j+2] = 0;
		// }
	// }
	// for(register int i_i=0; i_i<i_F; i_i++) for(register int i_j=i_i+1; i_j<i_C; i_j++) ps_var->pi_Ady[i_i*i_C+i_j+2] = ps_var->pi_Ady[i_j*i_C+i_i+2]; // Esta sola línea simetriza la matriz
	// for(register int i_i=0; i_i<i_F; i_i++) ps_var->pi_Ady[i_i*i_C+i_i+2] = 0; // Esto me pone 0 en toda la diagonal
	// return 0;
// }


// // Esta función es la que lee un archivo y me arma la matriz de Adyacencia
int Lectura_Adyacencia(int *pi_vec, FILE *pa_archivo){
	// Deefino los enteros que voy a usar para leer el archivo y escribir sobre el vector.	
	int i_indice = 2;
	int i_salida = 0;
	
	// Leo la matriz de Adyacencia del archivo y la guardo en el vector de Adyacencia.
	while(fscanf(pa_archivo,"%d",&i_salida) != EOF && i_indice < *pi_vec * *(pi_vec+1)+2){
		*(pi_vec+i_indice) = i_salida;
		i_indice++;
	}
	
	// Aviso si hubo algún problema.
	if(fscanf(pa_archivo,"%d",&i_salida) != EOF){
		printf("La matriz del archivo es mas grande que tu vector\n");
		return 1;
	}
	if(fscanf(pa_archivo,"%d",&i_salida) == EOF && i_indice < *pi_vec * *(pi_vec+1)+2){
		printf("La matriz del archivo es mas chica que el vector\n");
		return 1;
	}
	
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
	for(ps_red->i_agente=0; ps_red->i_agente<i_F; ps_red->i_agente++) if(Random()<ps_red->pd_Act[ps_red->i_agente+2]) Conectar_agentes(ps_red,ps_datos);
	
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
	

	// Voy a usar las probabilidades y calcularlas de manera de que la proba sea homogenea.
	double* pd_probabilidades;
	pd_probabilidades = (double*) malloc((ps_datos->i_N+2)*sizeof(double));
	*pd_probabilidades = 1;
	*(pd_probabilidades+1) = ps_datos->i_N;
	for(register int i_i=0; i_i<ps_datos->i_N; i_i++) *(pd_probabilidades+i_i+2) = 0;
	
	// Ahora calculo las probabilidades de manera de que sean homogéneas.
	for(register int i_i=0; i_i<i_libres; i_i++) *(pd_probabilidades+*(pi_agentes_libres+i_i+2)+2) = (double) 1/i_libres;
	
	
	// Ahora sampleo m agentes de esta lista
	if(i_libres>ps_datos->i_m){
		int i_contador = 0;
		while(i_contador<ps_datos->i_m){
			i_indice = 0;
			d_proba = Random();
			d_probacumulada = *(pd_probabilidades+2);
			// Defino cuál es el agente que se conecta
			while(d_proba>d_probacumulada){
				i_indice++;
				d_probacumulada += *(pd_probabilidades+i_indice+2);
			}
			// Hago la conexión
			ps_red->pi_Ady[ps_red->i_agente*i_F+i_indice+2] = 1;
			ps_red->pi_Ady[i_indice*i_F+ps_red->i_agente+2] = 1; // Esto se encarga de marcar al sujeto simétrico
			// Avanzo el contador para marcar que hice una conexión
			i_contador++;
			// Saco al agente del grupo de agentes posibles para conectarse al
			// poner su probabilidad como cero.
			*(pd_probabilidades+i_indice+2) = 0;
			for(register int i_i=0; i_i<*(pd_probabilidades+1); i_i++) if(*(pd_probabilidades+i_i+2)>0) *(pd_probabilidades+i_i+2) = (double) 1/(i_libres-i_contador);
		}
	}
	else for(register int i_i=0; i_i<i_libres; i_i++){
		ps_red->pi_Ady[ps_red->i_agente*i_F+*(pi_agentes_libres+i_i+2)+2] = 1;
		ps_red->pi_Ady[*(pi_agentes_libres+i_i+2)*i_F+ps_red->i_agente+2] = 1; // Esto se encarga de marcar al sujeto simétrico
	}
	
	
	free(pi_agentes_libres);
	free(pd_probabilidades);
	return 0;
}


