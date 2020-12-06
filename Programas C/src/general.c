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
double Gaussiana(float f_mu, float f_sigma){
	// Defino mis variables iniciales
	int i_n=10;
	double d_z=0;
	
	// Genero el número que voy a obtener de mi Gaussiana.
	// Para ser sincero, esto es un código legado del cual no comprendo la matemática involucrada.
	for(int i_i=0;i_i<i_n;i_i++) d_z += Random();
	d_z = sqrt(12*i_n) * (d_z/i_n-0.5);
	return d_z*f_sigma+f_mu;
}

// Esta función me calcula la norma de la distancia entre dos partículas
double Norma(double *pd_x){
	// Defino mis variables iniciales
	double d_norm;
	
	// Calculo la norma como la raíz cuadrada de la sumatoria de los cuadrados de cada coordenada. (Hasta ahora considera vectores de tres coordenadas.)
	d_norm = sqrt((*pd_x)*(*pd_x)+(*(pd_x+1))*(*(pd_x+1))+(*(pd_x+2))*(*(pd_x+2)));
	return d_norm;
}

// Esta función me calcula el vector desplazamiento entre dos partículas
int delta_x(double *d_x1, double *d_x2, double d_L, double *d_Dx){
	// Defino mi vector intermedio de registro de datos
	double *d_diferencias;
	d_diferencias = (double*) malloc(3*sizeof(double));
	
	// Calculo la diferencia entre dos vectores de R^3
	for(int i_i=0;i_i<3;i_i++) *(d_diferencias+i_i) = *(d_x1+i_i)-*(d_x2+i_i);
	for(int i_i=0;i_i<3;i_i++) if(*(d_diferencias+i_i) < -0.5*d_L) *(d_diferencias+i_i) = *(d_diferencias+i_i)+d_L;
	for(int i_i=0;i_i<3;i_i++) if(*(d_diferencias+i_i) > 0.5*d_L) *(d_diferencias+i_i) = *(d_diferencias+i_i)-d_L;
	
	// Me anoto la diferencia en un vector que está en el main del programa, y luego libero el espacio usado.
	for(int i_i=0;i_i<3;i_i++) *(d_Dx+i_i) = *(d_diferencias+i_i);
	free(d_diferencias);
	return 0;
}

