// En este archivo me defino las funciones que inicializan, pero no las declaro

#include<stdio.h>
#include<stdlib.h>
#include<math.h>
#include "general.h"
#include "inicializar.h"


// Esta función me genera los vectores opinión iniciales del sistema. Esto es una matriz de tamaño N*T
int GenerarOpi(struct Red var, struct Parametros par){
	// Obtengo las dimensiones de la "matriz" de opiniones de mis agentes.
	int i_Filas,i_Columnas;
	i_Filas = (int) var.d_Opi[0];
	i_Columnas = (int) var.d_Opi[1];
	
	// Inicializo la "matriz" de opiniones de mis agentes.
	for(int i_i=0;i_i<i_Filas*i_Columnas;i_i++) var.d_Opi[i_i+2] = par.i_Mopi*(Random()-0.5)*2;
	return 0;
}

// Esta función me genera la matriz de Superposicion del sistema. Esto es una matriz de T*T
int GenerarAng(struct Red var){
	// Obtengo las dimensiones de la matriz de Superposicion.
	int i_Filas,i_Columnas;
	i_Filas = (int) var.d_Ang[0];
	i_Columnas = (int) var.d_Ang[1];
	
	// Inicializo la matriz de Superposicion de mi sistema.
	for(int i_i=0; i_i<i_Filas; i_i++) for(int i_j=0; i_j<i_i; i_j++) var.d_Ang[i_i*i_Columnas+i_j+2] = 0.5; // Decidí poner 0.5 entre todos los tópicos de mi modelo
	for(int i_i=0; i_i<i_Filas; i_i++) var.d_Ang[i_i*i_Columnas+i_i+2] = 1; // Esto me pone 1 en toda la diagonal
	for(int i_i=0; i_i<i_Filas; i_i++) for(int i_j=i_i+1; i_j<i_Columnas; i_j++) var.d_Ang[i_i*i_Columnas+i_j+2] = var.d_Ang[i_j*i_Columnas+i_i+2]; // Esta sola línea simetriza la matriz
	return 0;
}


// Esta función me inicializa la matriz de Adyacencia. Esto es una matriz de N*N
int GenerarAdy(struct Red var, struct Parametros par){
	// Obtengo las dimensiones de la matriz de Adyacencia.
	int i_Filas,i_Columnas;
	i_Filas = (int) var.i_Ady[0];
	i_Columnas = (int) var.i_Ady[1];
	
	// Inicializo la matriz de Adyacencia de mi sistema
	for(int i_i=0; i_i<i_Filas; i_i++) {
		for(int i_j=0; i_j<i_i; i_j++) {
			// Saco un número random y veo si asigno un 1 o un 0 a esa posición-
			if(Random()<par.f_Pint) var.i_Ady[i_i*i_Columnas+i_j+2] = 1;
			else var.i_Ady[i_i*i_Columnas+i_j+2] = 0;
		}
	}
	for(int i_i=0; i_i<i_Filas; i_i++) for(int i_j=i_i+1; i_j<i_Columnas; i_j++) var.i_Ady[i_i*i_Columnas+i_j+2] = var.i_Ady[i_j*i_Columnas+i_i+2]; // Esta sola línea simetriza la matriz
	// for(int i=0; i<par.N; i++) var.Ady[i*par.N+i] = 1; // Esto me pone 1 en toda la diagonal
	return 0;
}

// Esta función es para observar los vectores de opinión, la matriz de superposición y la matriz de adyacencia
int Visualizar(struct Red var, int i_Crit){
	if(i_Crit==0){ //En este caso observo los vectores de opinión
		
		// Obtengo las dimensiones de la "matriz" de vectores de opinión
		int i_Filas,i_Columnas;
		i_Filas = (int) var.d_Opi[0];
		i_Columnas = (int) var.d_Opi[1];
		
		// Imprimo la "matriz" en la consola
		printf("Visualizo el conjunto de vectores de opinion \n");
		for(int i_i=0; i_i<i_Filas; i_i++){
			for(int i_j=0; i_j<i_Columnas; i_j++) printf("%.2lf\t",var.d_Opi[i_i*i_Columnas+i_j+2]);
			printf("\n");
		}
	}
	else if(i_Crit==1){ // En este caso observo la matriz de Superposición
		// Obtengo las dimensiones de la matriz de Superposición
		int i_Filas,i_Columnas;
		i_Filas = (int) var.d_Ang[0];
		i_Columnas = (int) var.d_Ang[1];
		
		// Imprimo la matriz en la consola
		printf("Visualizo la matriz de Superposicion entre Topicos \n");
		for(int i_i=0; i_i<i_Filas; i_i++){
			for(int i_j=0; i_j<i_Columnas; i_j++) printf("%.2lf\t",var.d_Ang[i_i*i_Columnas+i_j+2]);
			printf("\n");
		}
	}
	else if(i_Crit==2){ // En este caso observo la matriz de adyacencia
		// Obtengo las dimensiones de la matriz de Adyacencia
		int i_Filas,i_Columnas;
		i_Filas = var.i_Ady[0];
		i_Columnas = var.i_Ady[1];
		
		// Imprimo la matriz en la consola
		printf("Visualizo la matriz de Adyacencia del sistema \n");
		for(int i_i=0; i_i<i_Filas; i_i++){
			for(int i_j=0; i_j<i_Columnas; i_j++) printf("%d\t",var.i_Ady[i_i*i_Columnas+i_j+2]);
			printf("\n");
			printf("\n");
		}
	}
	return 0;
}

