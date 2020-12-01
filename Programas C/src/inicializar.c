// En este archivo me defino las funciones que inicializan, pero no las declaro

#include<stdio.h>
#include<stdlib.h>
#include<math.h>
#include "general.h"
#include "inicializar.h"


// Esta función me genera los vectores opinión iniciales del sistema. Esto es una matriz de tamaño N*T
int GenerarOpi(struct Red var, struct Parametros par){
	for(int i=0;i<par.N*par.T;i++) var.Opi[i] = (double) par.Mopi*(Random()-0.5)*2; // Inicializo mi red
	return 0;
}

// Esta función me genera la matriz de Superposicion del sistema. Esto es una matriz de T*T
int GenerarAng(struct Red var, struct Parametros par){
	for(int i=0; i<par.T; i++) for(int j=0; j<i; j++) var.Ang[i*par.T+j] = 0.35; // Decidí poner 0.35 entre todos los tópicos de mi modelo
	for(int i=0; i<par.T; i++) var.Ang[i*par.T+i] = 1; // Esto me pone 1 en toda la diagonal
	for(int i = 0; i<par.T; i++) for(int j=i+1; j<par.T; j++) var.Ang[i*par.T+j] = var.Ang[j*par.T+i]; // Esta sola línea simetriza la matriz
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
	// for(int i=0; i<par.N; i++) var.Ady[i*par.N+i] = 1; // Esto me pone 1 en toda la diagonal
	for(int i = 0; i<par.N; i++) for(int j=i+1; j<par.N; j++) var.Ady[i*par.N+j] = var.Ady[j*par.N+i]; // Esta sola línea simetriza la matriz
	return 0;
}

// Esta función es para observar los vectores de opinión, la matriz de superposición y la matriz de adyacencia
int Visualizar(struct Red var, struct Parametros par, int Crit){
	if(Crit==0){ //En este caso observo los vectores de opinión
		printf("Visualizo el conjunto de vectores de opinion \n");
		for(int i=0;i<par.N;i++){
			for(int j=0;j<par.T;j++) printf("%.2lf\t",var.Opi[i*par.T+j]);
			printf("\n");
		}
	}
	else if(Crit==1){ // En este caso observo la matriz de Superposición
		printf("Visualizo la matriz de Superposicion entre Topicos \n");
		for(int i=0;i<par.T;i++){
			for(int j=0;j<par.T;j++) printf("%.2lf\t",var.Ang[i*par.T+j]);
			printf("\n");
		}
	}
	else if(Crit==2){ // En este caso observo la matriz de adyacencia
		printf("Visualizo la matriz de adyacencia del sistema \n");
		for(int i=0;i<par.N;i++){
			for(int j=0;j<par.N;j++) printf("%d\t",var.Ady[i*par.N+j]);
			printf("\n");
		}
	}
	return 0;
}

