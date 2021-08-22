# -*- coding: utf-8 -*-
"""
Created on Sun Aug 15 18:55:32 2021

@author: Favio
"""


# Este archivo la idea es que sirva para graficar las TdO de las Redes de Actividad,
# recordando que estas redes no terminan de converger, por lo que hay que ir promediando
# sus valores para obtener el resultado final

import matplotlib.pyplot as plt
from matplotlib.pyplot import cm
from matplotlib.colors import LinearSegmentedColormap
import numpy as np
import time
import math
import os

# Importo todas las librerías que voy a usar en el programa. Estas son las que
# uso en los tres programas, por lo que no debería necesitar nada más.

#--------------------------------------------------------------------------------

# Voy a definir TODAS las funciones que voy a usar, total definirlas no roba
# tiempo o proceso al programa.


# Esto printea una cantidad de valores cant de un objeto iterable que paso
# en la parte de lista.
def scan(lista,cant=10):
    i=0
    for x in lista:
        print(x)
        i+=1
        if i>cant:
            break
            
        
# Esto va al final de un código, simplemente printea cuánto tiempo pasó desde la última
# vez que escribí el inicio del cronómetro t0=time.time()
def Tiempo():
    t1=time.time()
    print("Esto tardó {} segundos".format(t1-t0))


# Esta es la función que uso por excelencia para levantar datos de archivos. Lo
# bueno es que lee archivos de forma general, no necesita que sean csv o cosas así
def ldata(archive):
        f = open(archive)
        data = []
        for line in f:
            col = line.split("\t")
            col = [x.strip() for x in col]
            data.append(col)
        return data 

    
# Esta función calcula el valor del Alfa crítico que grafico en los mapas de colores
# A diferencia de lo que tenía antes, voy a tener que introducir al GM como una variable
def AlfaC(x,GM):
    T = 2 # Número de tópicos
    K = 3 # Influencia social
    
    if(x > 0):
        alfa = (T-1)/((GM*K)*(T-1+x))
    else:
        alfa = (T-1)/((GM*K)*(T-1-x))
    return alfa


# Voy a definir una función para usar en esta celda, que me permite asignar
# a cada ángulo un color. La idea es que esta función reciba como datos
# el vector a clasificar y la cantidad de pedacitos en la cual divido los
# 360 grados de la circunferencia. Luego me devuelve un número, que va a ser
# el índice en el cual se halla el color de ese vector. El índice lo uso
# para buscar el color en un vector que previamente voy a definir con
# ciertos valores de colores en cada índice. 
# IMPORTANTE: Esto vale sólo para vectores 2D

def Indice_Color(vector,Divisiones):
    # Primero calculo el ángulo
    Vhor = [1,0] # Este vector representa la horizontal
    if np.linalg.norm(vector) != 0 :
        vector_unitario = vector/np.linalg.norm(vector)
        Producto_escalar = np.dot(Vhor,vector_unitario)
        Angulo = np.arccos(Producto_escalar)

        # Le hago ajuste considerando el cuadrante del vector
        if vector[1] < 0:
            Angulo = 2*math.pi-Angulo


        # Ahora calculo el valor de división entera y el Resto
        Delta = (2*math.pi)/Divisiones
        Dividendo = Angulo/Delta
        D = math.floor(Dividendo)
        R = (Dividendo - D) * Delta

        # Compruebo en qué casillero cae el ángulo y returneo el índice
        if R <= Delta/2:
            return D # En este caso el ángulo se encuentra entre (D*Delta-Delta/2,D*Delta+Delta/2]
        elif R > Delta/2:
            return (D+1)%Divisiones # En este caso el ángulo se encuentra entre ((D+1)*Delta-Delta/2,(D+1)*Delta+Delta/2]
    else:
        return 0;


# Voy a definir una función que tome un estado del sistema y a partir de las opiniones
# de los agentes pueda determianr si el sistema se encuentra en un estado de Consenso,
# Polarización Descorrelacionada o Estado ideológico. La idea es que la función reciba
# el estado final del sistema y a partir de este devuelva un string que defina en cual
# de mis tres estados me encuentro. Básicamente la idea de esto es que si mis opiniones
# están muy cerca del cero, entonces estoy en consenso porque ese cae al cero fuerte.
# Entonces pedir que el máximo sea menor a 0,1 es en sí una cota bastante generosa.
# Por el otro lado, el estado ideológico me deja valores sobre una sola diagonal,
# entonces si el producto de la opinión del tópico 1 con la del tópico 2 para
# todos los agentes me da con un único signo, estoy en el caso de estado ideológico.
# Finalmente, si algunos de estos productos me dan positivos y otros negativos,
# entonces estoy en Polarización Descorrelacionada.

def EstadoFinal(Array):
    
    Topicos = 2    
    # Primero veo el caso de que hayan tendido a cero. En este caso lo importante
    # es ver que la mayoría haya ido al cero y que alguno que se haya escapado no
    # me joda el consenso. Pedir que el 90% esté debajo del umbral es lo mismo que
    # decir que como máximo 100 sujetos se hayan escapado, que es un número
    # me parece razonable.
    
    ArrayAbs = np.absolute(Array)
    Comprobacion = np.sqrt(ArrayAbs[0::2]*ArrayAbs[0::2] + ArrayAbs[1::2]*ArrayAbs[1::2])
    Cant0 = np.count_nonzero(Comprobacion < 2*math.sqrt(2.5))/len(Comprobacion)
    if Cant0 > 0.95:
        return "Consenso"
    
    #----------------------------------------------------------
    # Ahora veamos los otros dos casos. Primero voy a armar
    # un array que tenga las opiniones del tópico 1, y otro
    # con las opiniones del tópico 2.
    
    ArrayT1 = Array[0::2]
    ArrayT2 = Array[1::2]
    Maximo = max(ArrayAbs)
    
    OpinionesFiltradas = np.zeros(len(Array))
    
    for agente,x1,x2 in zip(np.arange(len(ArrayT1)),ArrayT1,ArrayT2):
        if abs(x1) > Maximo*0.3 and abs(x2) > Maximo*0.3:
            OpinionesFiltradas[0+agente*Topicos:2+agente*Topicos] = [x1,x2]
    
    ArrayCuad = ClasificacionCuadrantes(OpinionesFiltradas)
    
    Cant1 = np.count_nonzero(ArrayCuad == 1)
    Cant2 = np.count_nonzero(ArrayCuad == 2)
    Cant3 = np.count_nonzero(ArrayCuad == 3)
    Cant4 = np.count_nonzero(ArrayCuad == 4)
    
    if Cant2 > 0 and Cant4 > 0 and Cant1 == 0 and Cant3 == 0:
        return "Ideologico"
    elif Cant2 == 0 and Cant4 == 0 and Cant1 > 0 and Cant3 > 0:
        return "Ideologico"
    else:
        return "Polarizacion"


# Armo una función acá que tome el conjunto de opiniones obtenidas en todas las iteraciones
# y luego promedie las opiniones para darme el estado al cual converge el sistema

def PromediosOpiniones(Array):
    
    # Tomo el array, y luego voy armando mi resultado a partir de promediar
    # las opiniones finales de todas las iteraciones. Para eso primero necesito
    # definir T y N
    
    T = 2
    N = 1000
    
    
    Resultado = np.zeros(N*T)
    
    for opinion in range(N*T):
        Resultado[opinion] = np.mean(Array[opinion::N*T])
    
    return Resultado
    


# Voy a definir una función que tome un array con opiniones del sistema y me 
# diga en qué cuadrante se encuentran cada una de estas coordenadas. Luego a
# la salida me devuelve un array con el cual me voy a armar un histograma

def ClasificacionCuadrantes(Array):
    
    # Primero tomo el array y con sign reviso si sus variables son positivas o negativas.
    # Luego, creo el array Resultado que es lo que voy a returnear.
    # Lo siguiente es crear el array SwitchDic, que va a funcionar como un Switch para los
    # casos que voy a considerar.
    
    Resultado = np.zeros(int(len(Array)/2))
    SwitchDic = dict()
    
    # Defino todos los casos posibles
    
    SwitchDic[(1,1)] = 1
    SwitchDic[(-1,1)] = 2
    SwitchDic[(-1,-1)] = 3
    SwitchDic[(1,-1)] = 4
    SwitchDic[(1,0)] = 0
    SwitchDic[(0,1)] = 0
    SwitchDic[(0,-1)] = 0
    SwitchDic[(-1,0)] = 0
    SwitchDic[(0,0)] = 0
    
    # Repaso los elementos en Signos para identificar los cuadrantes de mis objetos.
    
    for x1,x2,indice in zip(Array[0::2],Array[1::2],np.arange(len(Array[0::2]))):
        Absolutos = np.abs(np.array([x1,x2]))
        if max(Absolutos)<0.01:
            Resultado[indice] = 0
        else:
            Signos = np.sign(np.array([x1,x2]))
            Resultado[indice] = SwitchDic[(Signos[0],Signos[1])]
  
    return Resultado


# Acá lo que voy a hacer es preparar los colores que voy a usar para definir los puntos finales
# de las trayectorias de las opiniones

Divisiones = 144
color=cm.rainbow(np.linspace(0,1,Divisiones))


# Lo que hice acá es definir una ¿lista? que tiene en cada casillero los datos que definen un color.
# Tiene diferenciados 144 colores, es decir que tengo un color para cada región de 2.5 grados. Estas regiones
# las voy a distribuir centrándolas en cada ángulo que cada color representa. Por lo tanto,
# Los vectores que tengan ángulo entre -1.25º y 1.25º tienen el primer color. Los que tengan entre
# 1.25º y 3.75º tienen el segundo color. Y así. Por tanto yo tengo que hallar una fórmula que para
# cada ángulo le asigne el casillero que le corresponde en el vector de color. Luego, cuando grafique
# el punto, para el color le agrego un input que sea: c = color[n]



# Estas son todas las funciones que voy a necesitar. Lo último no es una función,
# es la lista de colores que necesitaba para usar la función Indice_Color.
# Ahora voy a definir la parte que se encarga de levantar los nombre y el path
# de los archivos.

t0 = time.time()

#-------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------

Carpetas = ["Actividad Reversion","Regact","HomofiliaCero","TiempoExtra"]
#SelCarpeta = 1
for SelCarpeta in range(1,len(Carpetas)):
    
    epsilon = 0.01
    gamma = 2.1
    
    # Primero levanto datos de la carpeta de la red Regact en DilAct
    
    CarpCheck=[[root,files] for root,dirs,files in os.walk("./DilAct/{}".format(Carpetas[SelCarpeta]))]
    
    # El elemento en la posición x[0] es el nombre de la carpeta
    
    for x in CarpCheck:
        # dada = x[0].split("\\")
        Archivos_Datos = [nombre for nombre in x[1]]
        Archivos_Datos.insert(0,x[0])
    
    # Con esto tengo los nombres de todos los archivos en la carpeta de Datos de Barabasi
    # Archivos_Datos tiene en la primer coordenada el principio de la dirección
    # de la carpeta, y el resto de elementos son los archivos en la carpeta.
    
    #---------------------------------------------------------------------------------------------
    
    # Es importante partir del hecho de que mis archivos llevan por nombre: "Datos_Opiniones_alfa=$_Cdelta=$_N=$_Iter=$"
    # Y también llevan de nombre "Datos_Actividades_alfa=$_Cdelta=$_N=$_Iter=$"
    
    Conjunto_Alfa = []
    Conjunto_Cdelta = []
    Conjunto_N = []
    
    for nombre in Archivos_Datos[1:len(Archivos_Datos)]:
        alfa = float(nombre.split("_")[2].split("=")[1])
        Cdelta = float(nombre.split("_")[3].split("=")[1])
        N = int(nombre.split("_")[4].split("=")[1])
        if alfa not in Conjunto_Alfa:
            Conjunto_Alfa.append(alfa)
        if Cdelta not in Conjunto_Cdelta:
            Conjunto_Cdelta.append(Cdelta)
        if N not in Conjunto_N:
            Conjunto_N.append(N)
    
    Conjunto_Alfa.sort()
    Conjunto_Cdelta.sort()
    Conjunto_N.sort()
    
    # Bien, esto ya me arma el conjunto de Alfas, Cdelta, N y Gm correctamente y ordenados
    # Ahora podemos pasar a lo importante de esta celda
    
    #--------------------------------------------------------------------------------------------
    
    # Voy a armar un diccionario que contenga las listas de los nombres de los archivos asociados
    # a un cierto N, Alfa y Cdelta. Me armo primero el superdiccionario, que es el diccionario,
    # que contiene diccionarios, que llevan a diccionarios que llevan a las listas de los nombres
    # de los archivos, donde los ingresos a los diccionarios son el número de Agentes, el Alfa y el Cdelta 
    # Entonces la lista se accede sabiendo el Alfa, Cdelta y N correspondiente de antemano.
    
    SuperDiccionario = dict()
    
    for AGENTES in Conjunto_N:
        SuperDiccionario[AGENTES] = dict()
        for ALFA in Conjunto_Alfa:
            for CDELTA in Conjunto_Cdelta:
                for nombre in Archivos_Datos[1:len(Archivos_Datos)]:
                    alfa = float(nombre.split("_")[2].split("=")[1])
                    Cdelta = float(nombre.split("_")[3].split("=")[1])
                    N = int(nombre.split("_")[4].split("=")[1])
                    if N==AGENTES and alfa==ALFA and Cdelta==CDELTA:
                        if alfa not in SuperDiccionario[AGENTES].keys():
                            SuperDiccionario[AGENTES][ALFA] = dict()
                        if Cdelta not in SuperDiccionario[AGENTES][ALFA].keys():
                            SuperDiccionario[AGENTES][ALFA][CDELTA] = []
                        else:
                            break
                    
                
    
    for nombre in Archivos_Datos[1:len(Archivos_Datos)]:
        alfa = float(nombre.split("_")[2].split("=")[1])
        Cdelta = float(nombre.split("_")[3].split("=")[1])
        N = int(nombre.split("_")[4].split("=")[1])
        SuperDiccionario[N][alfa][Cdelta].append(nombre)
        
    # Ya mejoré el armado del SuperDiccionario de manera de que cada N tenga los Alfa y cada
    # Alfa tenga los Cdelta y cada Cdelta tenga los GM correspondientes. Antes me pasaba que el Conjunto_Alfa era el conjunto
    # de TODOS los Alfas que hubiera entre todos los archivos, entonces si algún N tenía
    # Alfas que el otro no, eso podía generar problemas. Ahora, como cada diccionario
    # armado para cada N tiene por keys sólo los Alfas de ese N, puedo usar eso para
    # definir el Conjunto_Alfa de cada N y evitar los problemas que había visto que
    # iban a aparecer al querer graficar el mapa de colores de los estados finales del N=1000
        
    # Voy a guardar los archivos de Opiniones y de Actividades en el mismo SuperDiccionario.
    # Luego voy a ir usando un split.("_") y voy a tomar lo que está en la posición 1
    # para distinguir los archivos. Si dice "Actividades", es el archivo con grados
    # medios y actividades, si dice "Opiniones" tiene guardadas las opiniones.
    
    #--------------------------------------------------------------------------------------------
        
        
    # Empiezo iterando el N desde acá porque lo que voy a hacer es que al iniciar
    # la iteración en N, defino mis Conjunto_Alfa y Conjunto_Cdelta en función de
    # las keys de mi SuperDiccionario.
        
    # Armo el array de Actividades Totales aca porque voy a guardar el registro
    # de TODAS las actividades sorteadas, total esas actividades se arman usando
    # los mismos parámetros, de manera independiente del alfa y Cdelta
    ActividadesTotales = np.array([]) 
    
    # Armo la lista de listas que va a guardar el registro de los agentes que se activan.
    Registro = [[] for i in range(99)]
    Xactivacion = np.linspace(epsilon,1,num=100)
    
    # Armo el array de grados medios que voy a usar para ver la distribución de grados
    # de las redes.
    KMTotal = np.array([])
    
    
    for AGENTES in [1000]:
    
        Conjunto_Alfa = list(SuperDiccionario[AGENTES].keys())
    
        Conjunto_Cdelta = list(SuperDiccionario[AGENTES][Conjunto_Alfa[0]].keys())[0]
        
        for ALFA,ialfa in zip(Conjunto_Alfa,np.arange(len(Conjunto_Alfa))):
            
            CDELTA = 0
            icdelta = 0
            
    #        for CDELTA,icdelta in zip(Conjunto_Cdelta,np.arange(len(Conjunto_Cdelta))):
            
            #-----------------------------------------------------------------------------------
            
            # Abro mis gráficos, creo listas que voy a llenar con todas las simulaciones y armo algunas cosas varias
            # que voy a necesitar para después
            
            #-------------------------------------------------------------------------------------
            for nombre in SuperDiccionario[AGENTES][ALFA][CDELTA]:
                if nombre.split("_")[1] == "Actividades":
    
                    #--------------------------------------------------------------------------------------------
                
                    # Levanto los datos del archivo original y separo los datos en tres listas.
                    # Una para la matriz de Adyacencia, una para la matriz de superposición y una para los vectores de opiniones
                
                    Datos = ldata("{}/{}".format(Archivos_Datos[0],nombre))
                    for fila,posicion in zip (Datos,np.arange(len(Datos))):
                        if fila[1] == "Agentes Activados":
                            inicio_registro = posicion+1
                        if fila[1] == "Grado medio":
                            fin_registro = posicion
                    
                
                    # Lista con elementos de los vectores de opinión. Al final sí había una forma compacta de hacer esto.
                    # Si la matriz de Adyacencia evoluciona en el tiempo, va a haber que ver de hacer cambios acá.
                    Actividades = np.array([float(x) for x in Datos[1][1::]])
                    
                    Activacion = np.zeros((fin_registro-inicio_registro,1000))                
                    for fila in range(inicio_registro,fin_registro):
                        Activacion[fila-inicio_registro] = [int(x) for x in Datos[fila][1::]]
                    
                    Km = np.array([float(x) for x in Datos[fin_registro+1][1::]])
                
                    #----------------------------------------------------------------------------------------------
                    
                    # Voy a armarme mi array de valores de Actividades con el cual luego me construiré mi histograma.
                    
                    ActividadesTotales = np.concatenate((ActividadesTotales,Actividades), axis=None)
                    
                    # Esto me va a dejar un vector gigante con TODAS las actividades que lancé en TODAS
                    # las simulaciones. Luego con esto me voy a armar al final del programa un histograma.
                    
                    #-----------------------------------------------------------------------------------------------
                    
                    # Voy a guardar los registros de los agentes que se activaron en una lista de listas.
                    # La idea es que voy a armar ciertos rangos de valores de actividad
                    # de manera de conseguir un poco de estadística ya que mis redes se arman sólo
                    # 30 veces, y 30 no me sirve para mucha estadística. Entonces la idea es que los registros
                    # de actividades de todos los agentes en un cierto rango se guarden en una lista de manera
                    # de luego ir promediando esos valores y poder además tomar los datos de TODAS las simulaciones
                    # realizadas.
                    
                    paso = Xactivacion[1]-Xactivacion[0]
                    for agente in range(AGENTES):
                        Registro[math.floor((Actividades[agente]-epsilon)/paso)].append(Activacion[::,agente])
                    
                    # Esto debería armarme mi listas de registro correctamente.
                    
                    #--------------------------------------------------------------------------------------------------
                    
                    # Voy a juntar los valores del grado medio de la red de actividad para después hacer una
                    # distribución con eso.
                    
                    KMTotal = np.concatenate((KMTotal,Km),axis=None)
                    
                    #--------------------------------------------------------------------------------------------------
                    
                    
                    
                    
        # Armemos los datos de las actividades que voy a graficar.
        Feps = epsilon**(-gamma+1) # Función de distribución aplicada al epsilon
        Xact = np.linspace(epsilon,1,num=200)
        Yact = ((1-gamma)/(1-Feps))*(Xact**(-gamma))
        
        
        # Armo el histograma de actividades, lo comparo con la función original y luego
        # marco también los valores medios de actividad teóricos y calculados.
        plt.rcParams.update({'font.size': 18})
        plt.figure("Histograma Actividades",figsize=(20,15))
        # Grafico la distribución de actividades
        [Histo,Bins,nada] = plt.hist(ActividadesTotales,bins=500,density=True,label="Actividades sorteadas")
        # Grafico la función distribución de actividades teórica
        plt.plot(Xact,Yact,"*",color="green",markersize=15,label="Funcion distribucion")
        
        # Marco las actividades medias
        plt.vlines(0.04085,0,max(Histo),color="red",label="Actividad media calculada = 0.04085")
        plt.vlines(np.mean(ActividadesTotales),0,max(Histo),colors="blue",label="Actividad media empírica = {:.5f}".format(np.mean(ActividadesTotales)))
        plt.xlabel("Actividades")
        plt.ylabel("Probabilidad")
        plt.title("Histograma de Actividades")
        plt.yscale("log",nonpositive="clip")
        plt.grid()
        plt.legend()
        plt.savefig("../Imagenes/RedAct/{}/Distribucion Actividades".format(Carpetas[SelCarpeta]),bbox_inches="tight")
        plt.close("Histograma Actividades")
        
        #-----------------------------------------------------------------------------------------------------------------
        
        # Voy a graficar la probabilidad de que un agente se active si posee un cierto valor de
        # actividad. Para eso primero tengo que armar el valor de Y que voy a graficar
        
        Xactivacion = np.linspace(epsilon,1,num=99)
        Yactivacion = np.zeros(len(Registro))
        for fila in range(len(Registro)):
            Yactivacion[fila] = np.mean(np.array(Registro[fila]))
            
        plt.rcParams.update({'font.size': 18})
        plt.figure("Probabilidad de Activacion",figsize=(20,15))
        plt.plot(Xactivacion,Yactivacion,"--",color="green",linewidth=8)
        plt.grid()
        plt.xlabel("Actividad")
        plt.ylabel("Probabilidad de activacion")
        plt.title("Activacion de agentes segun su actividad")
        plt.savefig("../Imagenes/RedAct/{}/Activacion agentes".format(Carpetas[SelCarpeta]),bbox_inches="tight")
        plt.close("Probabilidad de Activacion")
    
        #--------------------------------------------------------------------------------------------------
        
        # Acá voy a graficar el histograma de los grados medios
        plt.rcParams.update({'font.size': 18})
        plt.figure("Histograma Grados",figsize=(20,15))
        # Grafico la distribución de actividades
        [Histo,Bins,nada] = plt.hist(KMTotal,bins=80,density=True,label="Grado medio de las redes")
        plt.vlines(0.817,0,max(Histo),color="red",label="Grado medio calculado", linewidth=6)
        plt.xlabel("Grado medio")
        plt.ylabel("Cuentas")
        plt.title("Distribución de Grados Medios")
        plt.grid()
        plt.legend()
        plt.savefig("../Imagenes/RedAct/{}/Distribucion Grado Medio".format(Carpetas[SelCarpeta]),bbox_inches="tight")
        plt.close("Histograma Grados")
                
                
                
                
Tiempo()