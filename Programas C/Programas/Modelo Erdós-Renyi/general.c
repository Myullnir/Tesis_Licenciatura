// En este archivo defino todas las funciones generales, pero no las declaro.
// El <stdio.h>, o <math.h>, o <stdlib.h>, ¿Son necesarios?

#include<stdio.h>
#include<stdlib.h>
#include<math.h>
#include "general.h"


// Esta función me genera un número random entre 0 y 1
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

// Esta función me calcula la norma de un vector
double Norma_d(double *pd_x){
	// Defino mis variables iniciales que son el resultado final, la suma de los cuadrados y el tamaño de mi vector
	double d_norm,d_sum = 0;
	int i_C,i_F;
	i_F = *pd_x;
	i_C = *(pd_x+1);
	
	// Calculo la norma como la raíz cuadrada de la sumatoria de los cuadrados de cada coordenada.
	for(register int i_i=0; i_i<i_C*i_F; ++i_i) d_sum += *(pd_x+i_i+2)*(*(pd_x+i_i+2));
	d_norm = sqrt(d_sum);
	return d_norm;
}

// Esta función me calcula la diferencia entre dos vectores
int Delta_Vec_d(double *pd_x1, double *pd_x2, double *pd_Dx){
	// Compruebo primero que mis dos vectores sean iguales en tamaño
	if(*pd_x1!=*pd_x2 || *(pd_x1+1)!=*(pd_x2+1) || *pd_x1!=*pd_Dx || *(pd_x1+1)!=*(pd_Dx+1)){
		printf("Los vectores son de tamaños distintos, no puedo restarlos\n");
		return 0;
	}
	
	// Defino las variables de tamaño de mis vectores
	int i_C,i_F;
	i_F = *pd_x1;
	i_C = *(pd_x1+1);
	
	// Calculo la diferencia entre dos vectores
	for(register int i_i=0; i_i<i_C*i_F; ++i_i) *(pd_Dx+i_i+2) = *(pd_x1+i_i+2)-*(pd_x2+i_i+2);
	
	// Me anoto la diferencia en un vector que está en el main del programa, y luego libero el espacio usado.
	return 0;
}

//Funciones de Visualización
//----------------------------------------------------------------------------------------
// Esta función es para observar los vectores double
int Visualizar_d(double *pd_vec){
	// Defino las variables que voy a necesitar.
	int i_F,i_C;
	i_F = *pd_vec;
	i_C = *(pd_vec+1);
	
	// Printeo mi vector
	for(register int i_i=0; i_i<i_F; i_i++){
		for(register int i_j=0; i_j<i_C; i_j++) printf("%lf\t",*(pd_vec+i_i*i_C+i_j+2));
		printf("\n");
	}
	printf("\n");
	
	return 0;
}

// Esta función es para observar los vectores float
int Visualizar_f(float *pf_vec){
	// Defino las variables que voy a necesitar.
	int i_F,i_C;
	i_F = *pf_vec;
	i_C = *(pf_vec+1);
	
	// Printeo mi vector
	for(register int i_i=0; i_i<i_F; i_i++){
		for(register int i_j=0; i_j<i_C; i_j++) printf("%lf\t",*(pf_vec+i_i*i_C+i_j+2));
		printf("\n");
	}
	printf("\n");
	
	return 0;
}

// Esta función es para observar los vectores int
int Visualizar_i(int *pi_vec){
	// Defino las variables que voy a necesitar.
	int i_F,i_C;
	i_F = *pi_vec;
	i_C = *(pi_vec+1);
	
	// Printeo mi vector
	for(register int i_i=0; i_i<i_F; i_i++){
		for(register int i_j=0; i_j<i_C; i_j++) printf("%d\t",*(pi_vec+i_i*i_C+i_j+2));
		printf("\n");
	}
	printf("\n");
	
	return 0;
}
//--------------------------------------------------------------------------------------------

// La función RK4 evoluciona un sólo elemento de todo un sistema. La idea de esto es que la función sea completamente
// modular, y que en caso de querer evolucionar todo el sistema, desde fuera la llame múltiples veces y listo.
// Además, ahora lo que hace es devolver el cálculo de la evolución del número en vez de asignarlo al vector provisto.
// Esto ofrece mayor libertad a la hroa de implementarlo. Justamente la idea de esto es que me permite pasarle una
// foto del sistema en un cierto paso temporal, y guardar los datos evolucionados en un segundo vector, de manera
// que la foto no varía al ser evolucionada. Eso me permite que con sólo dos vectores, uno del paso temporal actual
// y uno del paso temporal siguiente me alcance para poder hacer una evolución sincrónica del sistema.
// Fijate que la foto se ve intacta, porque en la línea antes de calcular el resultado final, vuelvo a reescribir
// mi foto con el valor inicial que tenía, de manera de que esta foto entra y sale igual.
double RK4(double *pd_sistema ,ps_Red ps_var, ps_Param ps_par, double (*pf_funcion)(ps_Red ps_var, ps_Param ps_par)){
	// Defino las variables y vectores que voy a necesitar
	int i_F = (int) *pd_sistema; // Este es el número de filas del vector principal
	int i_C = (int) *(pd_sistema+1); // Este es el número de columnas del vector principal
	float DT[4]; // Esto me ayuda a meter el paso temporal que se usa para calcular cada pendiente.
	double d_resultado = 0; // Este número es el que voy a returnear a la salida de la función
	
	double *pd_inicial; // Este me guarda las condiciones iniciales del vector, que las voy a necesitar al calcular cada paso del RK4
	pd_inicial = (double*) malloc((i_F*i_C+2)*sizeof(double));
	
	double *pd_pendientes; // Este puntero de doubles me guarda todos los valores de las pendientes k
	pd_pendientes = (double*) malloc((5+2)*sizeof(double));
	
	// Inicializo mis punteros
	for(register int i_i=0; i_i<i_F*i_C+2; i_i++) *(pd_inicial+i_i) = *(pd_sistema+i_i);
	
	*pd_pendientes = 1;
	*(pd_pendientes+1) = 5;
	for(register int i_i=0; i_i<5;++i_i) *(pd_pendientes+i_i+2)=0;
	
	// Armo mi vector DT. Este hay que armarlo uno por uno, si o si.
	DT[0] = 0;
	DT[1] = ps_par->f_dt*0.5;
	DT[2] = ps_par->f_dt*0.5;
	DT[3] = ps_par->f_dt;
		
	// Acá hago las iteraciones del RK4 para hallar las pendientes k
	for(register int i_j=0; i_j<4; i_j++){ // Esto itera para mis 4 k
		// Calculo el elemento de la pendiente k(i_j+1)
		for(register int i_i=0; i_i<i_F*i_C; i_i++) *(pd_sistema+i_i+2) = *(pd_inicial+i_i+2)+*(pd_pendientes+i_j+2)*DT[i_j];
		*(pd_pendientes+i_j+1+2) = (*pf_funcion)(ps_var,ps_par);
	}
	
	// Copio al sistema igual que el inicial para deshacer los cambios que hice en el vector principal al calcular los k
	for(register int i_i=0; i_i<i_F*i_C; i_i++) *(pd_sistema+i_i+2) = *(pd_inicial+i_i+2);
	
	// Ahora que tengo los 4 k calculados, avanzo al sujeto que quiero avanzar.
	d_resultado = *(pd_inicial+ps_var->i_agente*i_C+ps_var->i_topico+2)+(ps_par->f_dt/6)*(*(pd_pendientes+3)+*(pd_pendientes+4)*2+*(pd_pendientes+5)*2+*(pd_pendientes+6));
	
	
	// Ahora hagamos algún mecanismo de visualización, para ver que todo esté correctamente calculado. Dios que esto va a ser un bardo.
	// Primero visualicemos las pendientes. Para eso voy a armar unos strings que poner en el printeo
	
	// printf("\n Estas son las pendientes\n");
	// Visualizar_d(pd_pendientes);
	
	// También tengo que visualizar mi vector trabajado.
	
	// printf("Este es mi vector antes de evolucionarlo \n");
	// Visualizar_d(pd_inicial);
	
	// printf("Este es mi vector luego de evolucionarlo \n");
	// Visualizar_d(pd_sistema);
	

	// Libero el espacio de memoria asignado a los punteros de las pendientes y al pd_inicial
	free(pd_inicial);
	free(pd_pendientes);
	
	return d_resultado;
}

//--------------------------------------------------------------------------------------------
// Las siguientes funciones son complementos para escribir datos en un archivo

// Esta función va a recibir un vector double y va a escribir ese vector en mi archivo.
int Escribir_d(double *pd_vec, FILE *pa_archivo){
	// Defino las variables del tamaño de mi vector
	int i_C,i_F;
	i_F = *pd_vec;
	i_C = *(pd_vec+1);
	
	// Ahora printeo todo el vector en mi archivo
	for(register int i_i=0; i_i<i_C*i_F; i_i++) fprintf(pa_archivo,"\t%.12lf",*(pd_vec+i_i+2));
	fprintf(pa_archivo,"\n");
	
	return 0;
}

// Esta función va a recibir un vector int y va a escribir ese vector en mi archivo.
int Escribir_i(int *pi_vec, FILE *pa_archivo){
	// Defino las variables del tamaño de mi vector
	int i_C,i_F;
	i_F = *pi_vec;
	i_C = *(pi_vec+1);
	
	// Ahora printeo todo el vector en mi archivo
	for(register int i_i=0; i_i<i_C*i_F; i_i++) fprintf(pa_archivo,"\t%d",*(pi_vec+i_i+2));
	fprintf(pa_archivo,"\n");
	
	return 0;
}

