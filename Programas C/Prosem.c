//Este es el archivo para testeos

#include<stdio.h>
#include<stdlib.h>
#include<math.h>
#include<time.h>

int Operacion(double* d_parametro);
int Corte(double* d_parametro);
double Random();


int main(int argc, char *argv[]){
	// Defino mis variables temporales para medir el tiempo que tarda el programa. También genero una nueva semilla
	time_t tt_prin,tt_fin;
	time(&tt_prin);
	srand(time(NULL));
	int i_tardanza;

	// Defino mi contador de iteraciones, el parámetro de corte y una variable para la cantidad total de iteraciones
	double d_parametro = rand();
	int i_resultado, i_iteracionesT;
	
	// Como el valor inicial de parámetro es random, lo printeo para verlo
	printf("El numero inicial es %lf\n",d_parametro);
	
	// Printeo también la cantidad de pasos mínimos que voy a necesitar para que el sistema finalice su proceso
	i_resultado = (int) ceil(log(1000*d_parametro)/log(5))+50;
	printf("Voy a tener que iterar mínimo %d pasos\n", i_resultado);
	
	// Realizo las operaciones aplicando la función de Corte y muestro cuántas veces iteré.
	i_iteracionesT = Corte(&d_parametro);
	printf("En total itere %d veces\n", i_iteracionesT);
	
	// Ejecuto los comandos finales para medir el tiempo y liberar memoria
	time(&tt_fin);
	i_tardanza = tt_fin-tt_prin;
	printf("Tarde %d segundos en terminar\n",i_tardanza);
	return 0;
}

// Esta función me genera un número random entre 0 y 1
double Random(){
	return ((double) rand()/(double) RAND_MAX);
}

// Esta función realiza un proceso que modifica mi parámetro
int Operacion(double* pd_parametro){
	
	// Defino un mecanismo para que con una baja probabilidad el parámetro a veces suba en vez de bajar
	if(Random() < 0.7) *pd_parametro = *pd_parametro/5;
	else *pd_parametro = *pd_parametro*10;
	return 0;
}

// Esta función gestiona la iteración del sistema y se encarga de cortarlo cuando considera que el sistema llegó a un estado estable.
int Corte(double* pd_parametro){
	
	// Defino mi cantidad de pasos totales realizados
	int i_iteraciones=0, i_contador=0;
	
	while(i_contador<50){
		if(i_iteraciones > 0) printf("Se rompio la condicion de corte al hacer %d iteraciones extra\n",i_contador);
		// Inicializo el contador
		i_contador = 0;
		
		// Evoluciono el sistema hasta que se cumpla el criterio de corte
		do{
			Operacion(pd_parametro);
			i_iteraciones +=1;
		}
		while(*pd_parametro > 0.001);
		
		// Ahora evoluciono el sistema una cantidad arbitaria de veces, 500 en este caso. Le pongo como condición que si el sistema
		// deja de cumplir la condición de corte, deje de evolucionar
		while(i_contador < 50 && *pd_parametro <= 0.001 ){
			Operacion(pd_parametro);
			i_contador +=1;
			i_iteraciones +=1;
		}
		// Si el sistema evolucionó menos veces que la cantidad arbitraria, es porque rompió la condiciones de corte.
		// Por tanto lo vuelvo a hacer trabajar hasta que se vuelva a cumplir la condición de corte.
		// Si logra evolucionar la cantidad arbitraria de veces sin problemas, termino la evolución.
	}
	
	return i_iteraciones;
}