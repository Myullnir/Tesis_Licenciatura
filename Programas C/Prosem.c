//Este es el archivo para testeos

#include<stdio.h>
#include<stdlib.h>
#include<math.h>
#include<time.h>

int main(int argc, char *argv[]){
	// Defino mis variables temporales para medir el tiempo que tarda el programa. También genero una nueva semilla
	time_t tt_prin,tt_fin;
	time(&tt_prin);
	srand(time(NULL));
	int i_tardanza;
	
	//##################################################################################
	// // Defino el puntero a mi archivo y lo abro
	char s_archivo[255];
	sprintf(s_archivo,"Histograma_Ciclos");
	FILE *pa_archivo=fopen(s_archivo,"w+x"); // Con esto abro mi archivo y dirijo el puntero a él. Con el +x lo que hago es que no me reescriba el archivo ya creado
	
	// // Primero voy a escribir un nuevo archivo que voy a usar para leer y ver cómo funcionan las funciones de lectura
	// for(int register i_i=0; i_i<1000; i_i++){
		// for(int register i_j=0; i_j<1000; i_j++) fprintf(pa_archivo,"%lf\t",tanh(i_j*0.001+i_i));
		// fprintf(pa_archivo,"\n");
	// }
	
	//##################################################################################
	
	// En un ratito continuo con el guardado de datos. Primero quiero probar unos temas de cómputo
	// Voy a hacer que el programa realice la misma tarea muchas veces, guardarme la cantidad de ciclos
	// que realiza en cada segundo y luego con eso armar un histograma. Por eso voy a separar la parte
	// del cálculo complejo del cálculo simple
	
	int i_contador = 0; // Este lo uso para ver la cantidad de ciclos que el programa realiza
	int i_a = 10;
	int i_b = -3;
	int i_c = 4;
	int i_resultado = 0;
	
	// Ahora realizo unas cuentas con tanh.
	// double d_resultado = 0; // Defino el double para guardar en algún lado la cuenta
	// for(int register i_i=0; i_i<10000000; i_i++) d_resultado = tanh(i_a*(i_b+i_i)+i_c); // Hago la cuenta 100000 veces para que me tome un tiempo medible
	for(int register i_j=0; i_j<2000; i_j++){
		i_contador = 0;
		time(&tt_prin);
		do{
			// Primero realizo unas simples cuentas con ints muchas veces
			
			for(int register i_i=0; i_i<10000000; i_i++) i_resultado = (i_a*(i_b+i_i)+i_c)/2;
			time(&tt_fin);
			i_tardanza = tt_fin-tt_prin;
			i_contador++;
		}
		while(i_tardanza<1);
		fprintf(pa_archivo,"\t%d",i_contador);
	}
	fprintf(pa_archivo,"\n"); // Separo los ciclos de mi primer cálculo de los ciclos del segundo
	//################################################################################
	
	// Defino mis variables para tomar registro y hacer las cuentas
	i_contador = 0; // Este lo uso para ver la cantidad de ciclos que el programa realiza
	i_a = 10;
	i_b = -3;
	i_c = 4;
	double d_resultado = 0; // Defino el double para guardar en algún lado la cuenta
	
	for(int register i_j=0; i_j<2000; i_j++){
		i_contador = 0;
		time(&tt_prin);
		do{
			// Primero realizo unas simples cuentas con ints muchas veces
			
			for(int register i_i=0; i_i<10000000; i_i++) d_resultado = tanh((i_a*(i_b+i_i)+i_c)/2);
			time(&tt_fin);
			i_tardanza = tt_fin-tt_prin;
			i_contador++;
		}
		while(i_tardanza<1);
		fprintf(pa_archivo, "\t%d",i_contador);
	}
	
	
	//#####################################################################################
	
	// Ejecuto los comandos finales para medir el tiempo y liberar memoria
	fclose(pa_archivo);
	time(&tt_fin);
	i_tardanza = tt_fin-tt_prin;
	printf("Tarde %d segundos en terminar de calcular las tanh\n",i_tardanza);
	
	
	return 0;
}

