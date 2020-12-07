// Este es el header para el módulo general

#ifndef General_H
#define General_H
#include <math.h>

double Random();
double Gaussiana(float f_mu, float f_sigma);
double Norma(double *d_x);
int delta_x(double *d_x1, double *d_x2, double d_L, double *d_Dx);

//################################################################################################

// Acá vienen los structs.
// El struct Red tiene los datos que definen mi red, y la info de la red
struct Red{
	double *pd_Ang; // Matriz de superposición entre tópicos. Tiene tamaño T*T
	int *pi_Ady; // Matriz de adyacencia que define mis conexiones. Tiene tamaño N*N
	double *pd_Opi; // Vector de opinión de cada individuo
};

struct Parametros{
	float f_Beta; // Exponente que regula el grado de homofilia
	float f_Pint; // Probabilidad de que se forme el enlace de manera aleatoria
	float f_K; // Influencia social
	float f_alfa; // Controversialidad de los temas
	int i_N; // Número de agentes en la red
	int i_T; // Cantidad de tópicos
	int i_Mopi; // Máximo inicial de opiniones
	float f_dt; // Paso temporal de iteración del sistema
};

#endif

