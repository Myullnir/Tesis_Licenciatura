//Este es el archivo para testeos

#include<stdio.h>
#include<stdlib.h>
#include<math.h>
#include<time.h>
#include<string.h>

typedef struct Tabla{
	double* pd_valores; // Este es el vector donde guardo los valores de la tabla
	int i_largo; // Este es el largo de la tabla.
} s_Tabla;

typedef s_Tabla * ps_Tab;

double Interpolacion(double d_y1, double d_y2, double d_x1,double d_x);
int Indices_Tabla(int* i_indice1, int* i_indice2, double d_argumento);
int Largo_Tabla_TANH(FILE *pa_file);
double IntrpTANH(double d_Arg, ps_Tab ps_val, FILE* pa_file);
int Lectura_Tabla_TANH(double* pd_vec, FILE* pa_file);
double Max(double d_a, double d_b);
double Min(double d_a, double d_b);




int main(int argc, char *argv[]){
	// Defino mis variables temporales para medir el tiempo que tarda el programa. También genero una nueva semilla
	time_t tt_prin,tt_fin;
	time(&tt_prin);
	srand(time(NULL));
	int i_tardanza;
	
	// Defino el puntero a mi archivo y lo abro
	char s_archivo[255];
	sprintf(s_archivo,"Tabla_Valores_TANH");
	FILE *pa_archivo=fopen(s_archivo,"r"); // Con esto abro mi archivo y dirijo el puntero a él. Con el +x lo que hago es que no me reescriba el archivo ya creado
	
	// Armo mi puntero a struct
	ps_Tab ps_tabla;
	ps_tabla = malloc(sizeof(s_Tabla));
	
	// Defino el tamaño de mi vector de índices, lo malloqueo y lo inicializo
	ps_tabla->i_largo = Largo_Tabla_TANH(pa_archivo);
	ps_tabla->pd_valores = (double*) malloc((ps_tabla->i_largo+2)*sizeof(double));
	for(int i_i=0; i_i<ps_tabla->i_largo+2;i_i++) ps_tabla->pd_valores[i_i] = 0;
	ps_tabla->pd_valores[0] = 1; // Cantidad de filas
	ps_tabla->pd_valores[1] = ps_tabla->i_largo; // Cantidad de columnas
	
	// Levanto los valores de la Tabla_Valores_TANH y los pongo en mi vector
	Lectura_Tabla_TANH(ps_tabla->pd_valores,pa_archivo);
	
	// Comparemos algunos cálculos de tanh con cálculos de Interpolación
	double da_array[8] = {-5,-4.213485,-3.457286,-2.123457,1.244567,2.124518,3.555555,5};
	
	for(int i_i=0; i_i<8; i_i++){
		printf("El resultado de la interpolacion para %lf es %.5lf\n",da_array[i_i],IntrpTANH(da_array[i_i],ps_tabla,pa_archivo));
		printf("El resultado de la tanh para %lf es %.5lf\n",da_array[i_i],tanh(da_array[i_i]));
	}
	
	// Ahora con esto me armo los datos para la interpolación. Voy a guardar 12 decimales.
	// fprintf(pa_archivo,"%lf\t",-1.0);
	// for(register int i_i=0; i_i<1000001; i_i++) fprintf(pa_archivo,"%lf\t",tanh(-5+0.00001*i_i));
	// fprintf(pa_archivo,"%lf\t",1.0);
		
	// Ejecuto los comandos finales para medir el tiempo y liberar memoria
	free(ps_tabla->pd_valores);
	free(ps_tabla);
	fclose(pa_archivo);
	time(&tt_fin);
	i_tardanza = tt_fin-tt_prin;
	printf("Tarde %d segundos en terminar",i_tardanza);
		
	return 0;
}

//###########################################################

// Me defino funciones de máximo y mínimo
double Max(double d_a, double d_b){
	// Defino la variable a usar
	double d_max = 0;
	
	d_max = (d_a > d_b)? d_a : d_b; // Uso un operador ternario. La idea es que se evalúa la función antes del
	// signo de pregunta. Si es verdadera, se devuelve lo que está a la izquierda de los dos puntos.
	// Sino se devuelve lo que está a la derecha
	
	return d_max;
}

double Min(double d_a, double d_b){
	// Defino la variable a usar
	double d_min = 0;
	
	d_min = (d_a < d_b)? d_a : d_b; // Uso un operador ternario. La idea es que se evalúa la función antes del
	// signo de pregunta. Si es verdadera, se devuelve lo que está a la izquierda de los dos puntos.
	// Sino se devuelve lo que está a la derecha
	
	return d_min;
}


// Voy a armar las funciones que voy a necesitar para poder realizar las interpolaciones.
// Eso sería la función de Interpolación y la función que calcula la posición

double Interpolacion(double d_y1, double d_y2,double d_x1,double d_x){
	// Defino las variables que voy a necesitar
	double d_resultado = 0;
	double d_deltax = 0.00001;
	double d_deltay = d_y2-d_y1;
	
	d_resultado = (d_deltay/d_deltax)*d_x+d_y1+(-d_deltay/d_deltax)*d_x1; // Esta es la cuenta de la interpolación
	
	return d_resultado;
}


// La siguiente función es la que me dice la cantidad de números que hay guardados en el
// archivo. La idea es que use este número para armar un vector que es el que guarda
// la posición de cada uno de los números de la tabla

int Largo_Tabla_TANH(FILE *pa_file){
	// Defino la variable que voy a returnear
	int i_largo = 0;
	double d_salida = 0;
	
	fseek(pa_file,0,SEEK_SET);
	while(fscanf(pa_file,"%lf\t",&d_salida)!=EOF) i_largo++;
	fseek(pa_file,0,SEEK_SET);
	
	return i_largo;
}

// Con esta función ubico el índice que le corresponde a cada número que va entre -5 y 5
// en el vector de valores de la tabla.

int Indices_Tabla(int* i_indice1, int* i_indice2, double d_argumento){
	// Defino las variables que voy a necesitar.
	double d_indice = 0; // Este es el valor "exacto" del índice que le correspondería al argumento
	
	d_indice = (d_argumento+5)/0.00001; // Esto sale de despejar la fórmula para calcular los valores de la tabla.
	// El 0,00001 es el paso con el que armé los valores de la tabla
	
	d_indice = Max(d_indice,0);
	d_indice = Min(d_indice,1000003-1);
	
	*i_indice1 = floor(d_indice);
	*i_indice2 = ceil(d_indice);
	
	return 0;
}


// Esta función empaqueta el resto para que sólo reciba los elementos básicos, y
// ya poder pasarlo al main
double IntrpTANH(double d_Arg, ps_Tab ps_val, FILE* pa_file){
	// Defino las variables que necesito
	double d_Y1,d_Y2,d_X1,d_resultado;
	int i_i1, i_i2;
	i_i1 = 0;
	i_i2 = 0;
	
	Indices_Tabla(&i_i1, &i_i2,d_Arg);
	d_Y1 = ps_val->pd_valores[i_i1+2];
	d_Y2 = ps_val->pd_valores[i_i2+2];
	d_X1 = -5+0.00001*i_i1;
	
	d_resultado = Interpolacion(d_Y1,d_Y2,d_X1,d_Arg);
	
	
	return d_resultado;
}


// Esta función se encarga de leer la tabla de valores y colocarla en
// el vector de valores del struct
int Lectura_Tabla_TANH(double* pd_vec, FILE* pa_file){
	// Defino mi variable de salida y el entero que recorra los índices
	double d_salida = 0;
	int i_indice = 0;
	
	// Leo los datos de la tabla y los guardo en el vector.
	while(fscanf(pa_file,"%lf\t",&d_salida)!=EOF){
		*(pd_vec+i_indice+2)= d_salida;
		i_indice++;
	}
	
	return 0;
}


