//Este es el archivo para testeos

#include<stdio.h>
#include<stdlib.h>
#include<math.h>
#include<time.h>

// Acá vienen los structs.
// El struct Red tiene los datos que definen mi red, y la info de la red
typedef struct Red{
	double *pd_Ang; // Matriz de superposición entre tópicos. Tiene tamaño T*T
	int *pi_Ady; // Matriz de adyacencia que define mis conexiones. Tiene tamaño N*N
	double *pd_Opi; // Vector de opinión de cada individuo
	int i_agente; // Entero que representa el agente que estoy mirando. Es un valor que va entre 0 y N-1
	int i_topico; // Entero que representa el tópico que estoy mirando. Es un valor que va entre 0 y T-1
	int i_agente2; // Este es el segundo agente con el cual se pone en contacto el primero.
} s_Red;

typedef struct Parametros{
	float f_Beta; // Exponente que regula el grado de homofilia
	float f_Pint; // Probabilidad de que se forme el enlace de manera aleatoria
	float f_K; // Influencia social
	float f_alfa; // Controversialidad de los temas
	int i_N; // Número de agentes en la red
	int i_T; // Cantidad de tópicos
	int i_Mopi; // Máximo inicial de opiniones
	float f_dt; // Paso temporal de iteración del sistema
} s_Param;

// Acá voy a declarar las funciones.------------------------------------

double Random();
int Visualizar_d(double *pd_vec);
int Visualizar_f(float *pf_vec);
int Visualizar_i(int *pi_vec);
int GenerarOpi(s_Red var, s_Param par);
int GenerarAng(s_Red var);
int GenerarAdy(s_Red var,s_Param par);
double Din1(s_Red var, s_Param par);
double Din2(s_Red var, s_Param par);
int Escribir_d(double *pd_vec, FILE *pa_archivo);
int Escribir_i(int *pi_vec, FILE *pa_archivo);
int RK4(double *pd_vec ,s_Red var, s_Param par, double (*fp_funcion)(s_Red var, s_Param par));
double Multiplo(s_Red var, s_Param par);
int Iteracion(s_Red var, s_Param par, double (*pf_Dinamica)(s_Red var, s_Param par));



/*####################################################################################
####################################################################################
####################################################################################
####################################################################################
*/


//---------------------------------------------------------------------------------------------------

// Vamos a intentar ver como se leen archivos y data desde estos
// Creo que lo más útil va a ser usar el fscanf porque mis datos están separados por tabulaciones
// Acá está la forma de leer el archivo. Sólo necesitaría poder saber que tan largo es antes de
// subirlo, pero creo que eso sería mucho pedir.

int main(){
	// Defino mis variables temporales para medir el tiempo que tarda el programa. También genero una nueva semilla
	time_t tt_prin,tt_fin;
	time(&tt_prin);
	srand(time(NULL));
	int i_tardanza;
		
	// Defino los nombres de mis structs en este programa y los valores de los parámetros
	s_Red red;
	s_Param datos;
	
	datos.f_Beta = 0.5;
	datos.f_Pint = 0.5; // Ahora mismo este valor no está haciendo nada
	datos.f_K = 5;
	datos.f_alfa = 2;
	datos.i_N = 20;
	datos.i_T = 4;
	datos.i_Mopi = 2;
	datos.f_dt = 0.2;
	
	// Defino el puntero a mi función y lo inicializo
	double (*pf_Dinamica)(s_Red Red, s_Param Parametros) = &Din2;	
	
	// Asigno memoria a mis matrices y las inicializo
	
	// Matriz de Vectores de opinión. Tiene tamaño N*T
	red.pd_Opi = (double*) malloc((datos.i_N*datos.i_T+2)*sizeof(double)); // Asigno espacio de memoria al vector
	for(register int i_i=0; i_i<datos.i_N*datos.i_T+2; i_i++) red.pd_Opi[i_i] = 0; // Inicializo la matriz para que no haya "basura" en alguna posición
	red.pd_Opi[0] = datos.i_N; // Guardo el número de filas en la primer coordenada del vector
	red.pd_Opi[1] = datos.i_T; // Guardo el número de Columnas en la segunda coordenada del vector
	GenerarOpi(red,datos); // Genero la red de Vectores de opinión propiamente dicha.

	// Matriz de Superposición. Tiene tamaño T*T
	red.pd_Ang = (double*) malloc((datos.i_T*datos.i_T+2)*sizeof(double)); // Asigno espacio de memoria al vector
	for(register int i_i=0; i_i<datos.i_T*datos.i_T+2; i_i++) red.pd_Ang[i_i] = 0; // Inicializo la matriz para que no haya "basura" en alguna posición
	red.pd_Ang[0] = datos.i_T; // Guardo el número de filas en la primer coordenada del vector
	red.pd_Ang[1] = datos.i_T; // Guardo el número de Columnas en la segunda coordenada del vector
	GenerarAng(red); // Genero la red de Vectores de opinión propiamente dicha.
	
	// Matriz de Adyacencia. Tiene tamaño N*N
	red.pi_Ady = (int*) malloc((datos.i_N*datos.i_N+2)*sizeof(int)); // Asigno espacio de memoria al vector
	for(register int i_i=0; i_i<datos.i_N*datos.i_N+2; i_i++) red.pi_Ady[i_i] = 0; // Inicializo la matriz para que no haya "basura" en alguna posición
	red.pi_Ady[0] = datos.i_N; // Guardo el número de filas en la primer coordenada del vector
	red.pi_Ady[1] = datos.i_N; // Guardo el número de columnas en la segunda coordenada del vector
	GenerarAdy(red,datos); // Genero la red de Adyacencia propiamente dicha.
	
	// // Defino las variables para mi archivo.txt que guarda los datos del sistema
	// char filename[255]; // Siempre lo hago lo más grande posible. Si sobra no es problema.
	// sprintf(filename,"Datos_Evolucion_Opinion_N=%d_T=%d",datos.i_N,datos.i_T); // Uso esto para asignarle el nombre a mi archivo.
	// FILE *pa_txt=fopen(filename,"w"); //Esto me crea un archivo con nombre filename y permiso de escritura. Es a partir del puntero pa_txt que accedo al archivo.
	
	// // Copio en el archivo mi matriz de Adyacencia
	// Escribir_i(red.pi_Ady, pa_txt);
	
	// // Copio en el archivo mi matriz de Superposicion
	// Escribir_d(red.pd_Ang, pa_txt);
	
	// // Copio en el archivo mis vectores de opinion
	// Escribir_d(red.pd_Opi, pa_txt);
	
	printf("Este es mi sistema antes de evolucionarlo\n");
	Visualizar_d(red.pd_Opi);
	
	// Evoluciono mi sistema y luego voy guardando los datos.
	for(register int i_i=0; i_i<5000; ++i_i) Iteracion(red,datos,pf_Dinamica);

	
	printf("Este es mi sistema final\n");
	Visualizar_d(red.pd_Opi);
	
	
	// Ejecuto los comandos finales para medir el tiempo y liberar memoria
	// fclose(pa_txt); // Con esto cierro mi archivo
	free(red.pi_Ady);
	free(red.pd_Ang);
	free(red.pd_Opi);
	time(&tt_fin);
	i_tardanza = tt_fin-tt_prin;
	printf("Tarde %d segundos en terminar\n",i_tardanza);
	return 0;
}

/*####################################################################################
####################################################################################
####################################################################################
####################################################################################
*/

// De acá en adelante van las funciones a declarar

// Esta función me genera un número random
double Random(){
	return ((double) rand()/(double) RAND_MAX);
}


// Estas son las funciones de Inicialización.
// #########################################################################################################


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




// Esta función me genera los vectores opinión iniciales del sistema. Esto es una matriz de tamaño N*T
int GenerarOpi(s_Red var, s_Param par){
	// Obtengo las dimensiones de la "matriz" de opiniones de mis agentes.
	int i_Filas,i_Columnas;
	i_Filas = (int) var.pd_Opi[0];
	i_Columnas = (int) var.pd_Opi[1];
	
	// Inicializo la "matriz" de opiniones de mis agentes.
	for(int i_i=0;i_i<i_Filas*i_Columnas;i_i++) var.pd_Opi[i_i+2] = par.i_Mopi*(Random()-0.5)*2;
	return 0;
}

// Esta función me genera la matriz de Superposicion del sistema. Esto es una matriz de T*T
int GenerarAng(s_Red var){
	// Obtengo las dimensiones de la matriz de Superposicion.
	int i_Filas,i_Columnas;
	i_Filas = (int) var.pd_Ang[0];
	i_Columnas = (int) var.pd_Ang[1];
	
	// Inicializo la matriz de Superposicion de mi sistema.
	for(int i_i=0; i_i<i_Filas; i_i++) for(int i_j=0; i_j<i_i; i_j++) var.pd_Ang[i_i*i_Columnas+i_j+2] = 0.5*(((-i_i-i_j)%2)*2+1); // Decidí poner 0.5 entre todos los tópicos de mi modelo
	for(int i_i=0; i_i<i_Filas; i_i++) var.pd_Ang[i_i*i_Columnas+i_i+2] = 1; // Esto me pone 1 en toda la diagonal
	for(int i_i=0; i_i<i_Filas; i_i++) for(int i_j=i_i+1; i_j<i_Columnas; i_j++) var.pd_Ang[i_i*i_Columnas+i_j+2] = var.pd_Ang[i_j*i_Columnas+i_i+2]; // Esta sola línea simetriza la matriz
	return 0;
}


// Esta función me inicializa la matriz de Adyacencia. Esto es una matriz de N*N
int GenerarAdy(s_Red var, s_Param par){
	// Obtengo las dimensiones de la matriz de Adyacencia.
	int i_Filas,i_Columnas;
	i_Filas = (int) var.pi_Ady[0];
	i_Columnas = (int) var.pi_Ady[1];
	
	// Inicializo la matriz de Adyacencia de mi sistema
	for(int i_i=0; i_i<i_Filas; i_i++) {
		for(int i_j=0; i_j<i_i; i_j++) {
			// Saco un número random y veo si asigno un 1 o un 0 a esa posición-
			if(Random()<par.f_Pint) var.pi_Ady[i_i*i_Columnas+i_j+2] = 1;
			else var.pi_Ady[i_i*i_Columnas+i_j+2] = 0;
		}
	}
	for(int i_i=0; i_i<i_Filas; i_i++) for(int i_j=i_i+1; i_j<i_Columnas; i_j++) var.pi_Ady[i_i*i_Columnas+i_j+2] = var.pi_Ady[i_j*i_Columnas+i_i+2]; // Esta sola línea simetriza la matriz
	// for(int i=0; i<par.N; i++) var.Ady[i*par.N+i] = 1; // Esto me pone 1 en toda la diagonal
	return 0;
}

// #####################################################################################

// Estas son las funciones del avance
//#######################################################################################

// Esta función resuelve un término de los de la sumatoria.
double Din1(s_Red var, s_Param par){
	// Defino las variables locales de mi función. d_resultados es el return. 
	// d_opiniones_superpuestas es el producto de la matriz de superposición de tópicos con el vector opinión de un agente.
	double d_resultado,d_opiniones_superpuestas = 0;
	
	// Obtengo el tamaño de columnas de mis tres matrices
	int i_Co,i_Cs;
	i_Co = (int) var.pd_Opi[1];
	i_Cs = (int) var.pd_Ang[1];
	
	for(register int i_p=0; i_p<i_Cs; i_p++) d_opiniones_superpuestas += var.pd_Ang[var.i_topico*i_Cs+i_p+2]*var.pd_Opi[var.i_agente2*i_Co+i_p+2]; // Calculo previamente este producto de la matriz con el vector.
	d_resultado = tanh(par.f_alfa*d_opiniones_superpuestas); // Esto es lo que está dentro de la sumatoria en la ecuación dinámica.
	return d_resultado; // La función devuelve el número que buscás, no te lo asigna en una variable.
}

// Esta es la segunda parte de la ecuación dinámica, con esto puedo realizar una iteración del sistema.
double Din2(s_Red var, s_Param par){
	// Defino las variables locales de mi función. d_resultado es lo que voy a returnear.
	// d_sumatoria es el total de la sumatoria del segundo término de la ecuación diferencial.
	double d_resultado,d_sumatoria=0;
	
	// Calculo la sumatoria de la ecuación diferencial. Para esto es que existe la función Din1.
	// La sumatoria es sobre un sólo agente ahora. La idea es ver que pasa cuando las interacciones se hacen de a pares de manera aleatoria
	// El sujeto lo voy a definir por afuera de esta función, cosa de que cada iteración del RK4 no me lo cambie.
	d_sumatoria += Din1(var,par);
	
	// Obtengo el tamaño de Columnas de mi matriz de Vectores de opinión y calculo el valor del campo que define mi ecuación diferencial
	int i_Columnas = (int) var.pd_Opi[1];
	d_resultado = -var.pd_Opi[var.i_agente*i_Columnas+var.i_topico+2]+par.f_K*d_sumatoria;
	return d_resultado;
}

//#######################################################################################


// Esta función me realiza una iteración del sistema a partir de un RK4.
// Incluso creo que no es necesario el uso del puntero de funciones, pero quiero aprender a usarlo
int RK4(double *pd_sistema ,s_Red var, s_Param par, double (*fp_funcion)(s_Red var, s_Param par)){
	// Defino las variables y vectores que voy a necesitar
	int i_F = (int) *pd_sistema; // Este es el número de filas del vector principal
	int i_C = (int) *(pd_sistema+1); // Este es el número de columnas del vector principal
	float DT[4]; // Esto me ayuda a meter el paso temporal que se usa para calcular cada pendiente.
	
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
	DT[1] = par.f_dt*0.5;
	DT[2] = par.f_dt*0.5;
	DT[3] = par.f_dt;
		
	// Acá hago las iteraciones del RK4 para hallar las pendientes k
	for(register int i_j=0; i_j<4; i_j++){ // Esto itera para mis 4 k
		// Calculo el elemento de la pendiente k(i_j+1)
		for(register int i_i=0; i_i<i_F*i_C; i_i++) *(pd_sistema+i_i+2) = *(pd_inicial+i_i+2)+*(pd_pendientes+i_j+2)*DT[i_j];
		*(pd_pendientes+i_j+1+2) = (*fp_funcion)(var,par);
	}
	
	// Copio al sistema igual que el inicial para deshacer los cambios que hice en el vector principal al calcular los k
	for(register int i_i=0; i_i<i_F*i_C; i_i++) *(pd_sistema+i_i+2) = *(pd_inicial+i_i+2);
	// Ahora que tengo los 4 k calculados, avanzo al sujeto que quiero avanzar.
	*(pd_sistema+var.i_agente*i_C+var.i_topico+2) = *(pd_inicial+var.i_agente*i_C+var.i_topico+2)+(par.f_dt/6)*(*(pd_pendientes+2)+*(pd_pendientes+3)*2+*(pd_pendientes+4)*2+*(pd_pendientes+5));
	
	
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
	
	return 0;
}

// Esta función va a recibir un vector double y va a escribir ese vector en mi archivo.
int Escribir_d(double *pd_vec, FILE *pa_archivo){
	// Defino las variables del tamaño de mi vector
	int i_C,i_F;
	i_F = *pd_vec;
	i_C = *(pd_vec+1);
	
	// Ahora printeo todo el vector en mi archivo
	for(register int i_i=0; i_i<i_C*i_F; i_i++) fprintf(pa_archivo,"\t%lf",*(pd_vec+i_i+2));
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


// Esta es una función define la ecuación deiferencial como un múltiplo del valor actual
double Multiplo(s_Red var, s_Param par){
	// Defino mis variables a usar
	int i_C;
	i_C = var.pd_Opi[1];
	double multiplo;
	
	// Esta ecuación diferencial me define las pendientes como el doble del valor actual.
	multiplo = 2*var.pd_Opi[var.i_agente*i_C+var.i_topico+2];
	
	return multiplo;
}


// Esta función me itera todo el sistema. Está buena para simplemente reemplazarla en el main.
int Iteracion(s_Red var, s_Param par, double (*pf_Dinamica)(s_Red var, s_Param par)){
	// Simplemente copio lo que estaba usando antes
	// Primero itero en los agentes, luego defino el segundo agente y evoluciono al primero interactuando con el segundo.
	for(var.i_agente=0; var.i_agente<par.i_N; ++var.i_agente){
			do{
				var.i_agente2 = rand()%par.i_N;
			}
			while(var.i_agente==var.i_agente2);
			for(var.i_topico=0; var.i_topico<par.i_T; ++var.i_topico) RK4(var.pd_Opi, var, par, pf_Dinamica);
		}
		
	return 0;
}


// Esta función toma un número y me da un número aleatorio DISTINTO al número recibido en un cierto rango.
// Esta es la versión con ints. Para que este programa funcione correctamente tiene que pasar que i_min <= i_input <= i_max
// Además, el min y el max pertenecen al rango.
// Seré sincero, toda esta función es para no meter un if justo en el corazón de la iteración de mi programa.
// Esta función no está terminada, otro día la retomo.
// int Aleatorio_distinto_i(int i_input, int i_min, int i_max){
	// // Defino mis variables a usar
	// unsigned int i_rango = i_max - i_min; // Fijate que el i_rango tiene que ser siempre positivo.
	// // 
	// // Espero que esto no me genere problemas a futuro. Problemas del tipo: "Segmentation Fault" que nunca más descubro dónde ocurren.
	// unsigned int i_aleatorio = (Random()%i_rango);
	
	// // Armo la tira de datos que va a tener todos los números posibles dentro del rango, MENOS el número i_input
	// int *pi_Tira;
	// pi_Tira = (int*) malloc((i_rango-1+2)*sizeof(int));
	// *pi_Tira = 1; // Este es el número de filas de mi vector
	// *(pi_Tira+1) = i_rango-1; // Este es el número de columnas de mi vector
	// for(register int i_i=0; i_i<i_input; ++i_i) *(pi_Tira+i_i+2) = i_i+i_min;
	// for(register int i_i=i_input+1; i_i<i_rango; ++i_i) *(pi_Tira+i_i-1+2) = i_i+i_min;
	
	
	
	
	
	
	// return ;
// }


