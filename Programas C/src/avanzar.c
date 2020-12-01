// En este archivo defino todas las funciones de que manipulan datos del sistema, pero no las declaro.
// El <stdio.h>, o <math.h>, o <stdlib.h>, ¿Son necesarios?

#include<stdio.h>
#include<stdlib.h>
#include<math.h>
#include "general.h"
#include "inicializar.h"
#include "avanzar.h"


// Voy a separar la ecuación dinámica en dos funciones. Una que tome el término con la tanh pero que se aplique a 
// un sólo agente externo. Luego esa función la voy a usar en la otra dentro de una sumatoria.
// La gran pregunta es: ¿Me conviene hacer un juego como el que hicimos en Física Computacional, donde armábamos
// una tabla con valores pre calculados y a los valores intermedios los interpolábamos? Por ahora, probemos sin
// eso. Si resulta que tarda mucho el programa, consideraré agregarlo.

double Din1(struct Red var, struct Parametros par, int v, int i, int j){
	// resultado es lo que obtengo de la cuenta de esta función. 
	// Opiniones superpuestas es el resultado del producto de la matriz Phi con x_j y mirando el tópico v
	double resultado,opiniones_superpuestas = 0;
	for(int p=0; p<par.T;p++) opiniones_superpuestas += var.Ang[v*par.T+p]*var.Opi[j*par.T+p]; // Calculo previamente este producto de la matriz con el vector.
	resultado = var.Ady[i*par.N+j]*tanh(par.alfa*opiniones_superpuestas); // Esto es lo que está dentro de la sumatoria en la ecuación dinámica.
	return resultado; // La función devuelve el número que buscás, no te lo asigna en una variable.
}


// Esta es la segunda parte de la ecuación dinámica, con esto puedo realizar una iteración del sistema.
double Din2(struct Red var, struct Parametros par, int v, int i){
	double resultado,Sumatoria=0;
	for(int j=0; j<i; j++) Sumatoria += Din1(var,par,v,i,j);
	for(int j=i+1; j<par.N; j++) Sumatoria += Din1(var,par,v,i,j);
	resultado = var.Opi[i*par.T+v]*(par.dt-1)+par.dt*par.K*Sumatoria;
	return resultado;
}

