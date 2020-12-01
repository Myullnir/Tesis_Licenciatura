// Este es el header para el módulo general

#ifndef General_H
#define General_H
#include <math.h>

double Random();
double Gaussiana(float mu, float sigma);
double Norma(double *x);
int delta_x(double *x1, double *x2, double L, double *Dx);

//################################################################################################

// Acá vienen los structs.
// El struct Red tiene los datos que definen mi red, y la info de la red
struct Red{
	double *Ang; // Matriz de superposición entre tópicos. Tiene tamaño T*T
	int *Ady; // Matriz de adyacencia que define mis conexiones. Tiene tamaño N*N
	double *Opi; // Vector de opinión de cada individuo
};

struct Parametros{
	float Beta; // Exponente que regula el grado de homofilia
	float Pint; // Probabilidad de que se forme el enlace de manera aleatoria
	float K; // Influencia social
	float alfa; // Controversialidad de los temas
	int N; // Número de agentes en la red
	int T; // Cantidad de tópicos
	int Mopi; // Máximo inicial de opiniones
	float Temporal; // Paso temporal de iteración del sistema
};

#endif

