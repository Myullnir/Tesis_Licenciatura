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

	// Defino dos variables a las que les voy a pasar input desde línea de comando, y las voy a sumar.
	int i_var1,i_var2;
	i_var1 = strtol(argv[1],NULL,10);
	i_var2 = strtol(argv[2],NULL,10);
	
	printf("La suma de los numeros que me pasaste es: %d \n",i_var1+i_var2);
	
	// Ejecuto los comandos finales para medir el tiempo y liberar memoria
	time(&tt_fin);
	i_tardanza = tt_fin-tt_prin;
	printf("Tarde %d segundos en terminar\n",i_tardanza);
	return 0;
}

// Voy a explicar acá cómo funca el strtol(const char *str, char **endptr, int base).
// La idea es que uno le pasa el string str. Este string puede tener una parte numérica seguida de una parte
// literal. O podría ser sólo numérica. La cosa es que uno le pasa el str a la primera coordenada. A la segunda
// coordenada le pasa la dirección de un puntero donde la función va a guardar la parte literal sobrante de str.
// Siempre se puede poner NULL ahí en caso de que uno no quiera guardar esa info. El tercer elemento es la
// base numérica a la cual quiere convertir el número. Claramente yo me muevo en base 10, así que eso
// siempre puede ser 10 tranquilamente.

// Expliquemos también argc y *argv. argc es el número de elementos pasados en por input de línea de
// comando al main. En particular el nombre del archivo SIEMPRE se pasa, así que argc siempre es 1 como mínimo.
// Por otro lado, en cada coordenada argv guarda cada uno de los argumentos pasados. argv[0] es el nombre del
// archivo. argv[1] es el primer argumento. argv[2] es el segundo argumento, y así.