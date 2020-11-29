// En este archivo me defino las funciones que inicializan, pero no las declaro

#include<stdio.h>
#include<stdlib.h>
#include<math.h>
#include "general.h"
#include "inicializar.h"


// Esta función me genera los vectores opinión iniciales del sistema. Esto es una matriz de tamaño N*T
int GenerarOpi(struct Red var, struct Parametros par){
	for(int i=0;i<par.N*par.T;i++) var.Opi[i] = 3; // Inicializo mi red
	return 0;
}

// Esta función me genera la matriz de Superposicion del sistema. Esto es una matriz de T*T
int GenerarAng(struct Red var, struct Parametros par){
	for(int i=0; i<par.T; i++) for(int j=0; j<i; j++) var.Ang[i*par.T+j] = (float) Random(); // Voy a poner Randoms para probar la función de Simetrizar, después voy a usar sólo 0.5
	for(int i=0; i<par.T; i++) var.Ang[i*par.T+i] = 1; // Esto me pone 1 en toda la diagonal
	return 0;
}


// Esta función me inicializa la matriz de Adyacencia. Esto es una matriz de N*N
int GenerarAdy(struct Red var, struct Parametros par){
	double Prob;
	for(int i=0; i<par.N; i++) {
		for(int j=0; j<i; j++) {
			Prob = Random();
			if(Prob<par.Pint) var.Ady[i*par.N+j] = 1;
			else var.Ady[i*par.N+j] = 0;
		}
	}
	for(int i=0; i<par.N; i++) var.Ady[i*par.N+i] = 1; // Esto me pone 1 en toda la diagonal
	return 0;
}

// Esta función es para observar los vectores de opinión, la matriz de superposición y la matriz de adyacencia
int Visualizar(struct Red var, struct Parametros par, int Crit){
	if(Crit==0){ //En este caso observo los vectores de opinión
		printf("Visualizo el conjunto de vectores de opinion \n");
		for(int i=0;i<par.N;i++){
			for(int j=0;j<par.T;j++) printf("%lf\t",var.Opi[i*par.N+j]);
			printf("\n");
		}
	}
	else if(Crit==1){ // En este caso observo la matriz de Superposición
		printf("Visualizo la matriz de Superposicion entre Topicos \n");
		for(int i=0;i<par.T;i++){
			for(int j=0;j<par.T;j++) printf("%f ",var.Ang[i*par.T+j]);
			printf("\n");
		}
	}
	else if(Crit==2){ // En este caso observo la matriz de adyacencia
		printf("Visualizo la matriz de adyacencia del sistema \n");
		for(int i=0;i<par.N;i++){
			for(int j=0;j<par.N;j++) printf("%d ",var.Ady[i*par.N+j]);
			printf("\n");
		}
	}
	return 0;
}

