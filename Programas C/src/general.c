// En este archivo defino todas las funciones generales, pero no las declaro.
// El <stdio.h>, o <math.h>, o <stdlib.h>, ¿Son necesarios?

#include<stdio.h>
#include<stdlib.h>
#include<math.h>
#include "general.h"


// Esta función me genera un número random
double Random(){
	return ((double) rand()/(double) RAND_MAX);
}

// Esta función me da un valor tomado de una distribución gaussiana con valor medio mu y desviación sigma
double Gaussiana(float mu, float sigma){
	int n=10,i;
	double z=0;
	for(i=0;i<n;i++) z += Random();
	z = sqrt(12*n) * (z/n-0.5);
	return z*sigma+mu;
}

// Esta función me calcula la norma de la distancia entre dos partículas
double Norma(double *x){
	double norm;
	norm = sqrt((*x)*(*x)+(*(x+1))*(*(x+1))+(*(x+2))*(*(x+2)));
	return norm;
}

// Esta función me calcula el vector desplazamiento entre dos partículas
int delta_x(double *x1, double *x2, double L, double *Dx){
	int i;
	double *diferencias;
	diferencias = (double*) malloc(3*sizeof(double));
	for(i=0;i<3;i++) *(diferencias+i) = *(x1+i)-*(x2+i);
	for(i=0;i<3;i++) if(*(diferencias+i)<-0.5*L) *(diferencias+i) = *(diferencias+i)+L;
	for(i=0;i<3;i++) if(*(diferencias+i)>0.5*L) *(diferencias+i) = *(diferencias+i)-L;
	for(i=0;i<3;i++) *(Dx+i) = *(diferencias+i);
	free(diferencias);
	return 0;
}


