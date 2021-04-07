
# coding: utf-8

# In[1]:


import matplotlib.pyplot as plt
from matplotlib.pyplot import cm
# from scipy.optimize import minimize
#from mpl_toolkits.mplot3d import Axes3D
from matplotlib.colors import LinearSegmentedColormap
import numpy as np
#import random
import time
#import pandas as pd
import math
#import csv
import os

t0=time.time()
###########################################################
###########################################################

# Esta celda define funciones y carga librerías.
# También sirve para levantar el nombre de los archivos, por lo que cada vez que armes
# nuevos archivos tenés que volver a correrla para volver a registrar los nuevos nombres

############################################################
############################################################

def scan(cant,lista):
    i=0
    for x in lista:
        print(x)
        i+=1
        if i>cant:
            break
            
def Tiempo():
    t1=time.time()
    print("Esto tardó {} segundos".format(t1-t0))


def ldata(archive):
        f = open(archive)
        data = []
        for line in f:
            col = line.split("\t")
            col = [x.strip() for x in col]
            data.append(col)
        return data 
    

# En esta celda voy a hacer los análisis de caracterización de la región de transición
# del sistema. Estos análisis son el análisis de la varianza de los tiempos de convergencia,
# La medición de los máximos valores alcanzados por el sistema y la distribución de opiniones
# por cuadrantes. (¿Se podría hacer un plot polar?)

t0=time.time()

T=2 # Tengo que definir el número de tópicos en algún lado, lo hago ahora porque más adelante no tiene lugar


#--------------------------------------------------------------------------------------

# Defino primero mi función de AlfaC

def AlfaC(x):
    T = 2 # Número de tópicos
    GM = 8 # Grado medio
    K = 1 # Influencia social
    if(x>0):
        alfa = (T-1)/((GM*K)*(T-1+x))
    else:
        alfa = (T-1)/((GM*K)*(T-1-x))
    return alfa

# Ya probé la función y ahora sí calcula perfecto. Hubo un pequeño
# error al principio.

#------------------------------------------------------------------


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
    
#----------------------------------------------------------------------------------------------

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
    
    
    # Primero veo el caso de que hayan tendido a cero
    
    ArrayAbs = np.absolute(Array)
    if max(ArrayAbs)<0.01:
        return "Consenso"
    
    #----------------------------------------------------------
    # Ahora veamos los otros dos casos. Primero voy a armar
    # un array que tenga las opiniones del tópico 1, y otro
    # con las opiniones del tópico 2.
    
    ArrayT1 = Array[0::2]
    ArrayT2 = Array[1::2]    
    ArrayProd = np.sign(np.multiply(ArrayT1,ArrayT2))
    
    if -1 in ArrayProd:
        return "Polarizacion"
    else:
        return "Ideologico"

# Lo probé con algunos vectores de prueba y parece funcar bárbaro. Habrá que probar
# más en detalle. Se me ocurre usar esto para que los gráficos estén etiquetados y
# mirar si en alguno se equivoca.

#-----------------------------------------------------------------------------------------------

# Voy a definir una función que tome un array con opiniones del sistema y me 
# diga en qué cuadrante se encuentran cada una de estas coordenadas. Luego a
# la salida me devuelve un array con el cual me voy a armar un histograma

def ClasificacionCuadrantes(Array):
    
    # Primero tomo el array y con sign reviso si sus variables son positivas o negativas.
    # Luego, creo el array Resultado que es lo que voy a returnear.
    # Lo siguiente es crear el array SwitchDic, que va a funcionar como un Switch para los
    # casos que voy a considerar.
    
    Signos = np.sign(Array)
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
    
    for x1,x2,indice in zip(Signos[0::2],Signos[1::2],np.arange(len(Signos[0::2]))):
        Resultado[indice] = SwitchDic[(x1,x2)]
  
    return Resultado

# Funciona bien, ya probé y resolví los errores que pudieran saltar con este código

#-----------------------------------------------------------------------------------------------

# Acá lo que voy a hacer es preparar los colores que voy a usar para definir los puntos finales
# de las trayectorias de las opiniones

Divisiones = 144
color=cm.rainbow(np.linspace(0,1,Divisiones))


# Lo que hice acá es definir una ¿lista? que tiene en cada casillero los datos que definen un color.
# Tiene diferenciados 144 colores, es decir que tengo un color para cada región de 2.5 grados. Estas regiones
# las voy a distribuir centrándolas en en cada ángulo que cada color representa. Por lo tanto,
# Los vectores que tengan ángulo entre -1.25º y 1.25º tienen el primer color. Los que tengan entre
# 1.25º y 3.75º tienen el segundo color. Y así. Por tanto yo tengo que hallar una fórmula que para
# cada ángulo le asigne el casillero que le corresponde en el vector de color. Luego, cuando grafique
# el punto, para el color le agrego un input que sea: c = color[n]
    


#--------------------------------------------------------------------------------------

CarpCheck=[[root,files] for root,dirs,files in os.walk("./ER2")]

# El comentario anterior era considerando que no le daba la dirección correcta
# de la carpeta con mi información al os.walk. Esta vez le estoy pasando la 
# dirección exacta, así que no es necesario hacer tanto quilombo para separar
# los nombres de los archivos. El elemento en la posición x[0] es el nombre de la carpeta

for x in CarpCheck:
    # dada = x[0].split("\\")
    Archivos_Datos = [nombre for nombre in x[1]]
    Archivos_Datos.insert(0,x[0])

# Con esto tengo los nombres de todos los archivos en la carpeta de Cambios dt
# Archivos_Datos tiene en la primer coordenada el principio de la dirección
# de la carpeta, y el resto de elementos son los archivos en la carpeta.
# Entonces si quiero buscar el objeto voy a tener que usar:
# Archivos_Datos[0]/Archivos_Datos[1]


#-------------------------------------------------------------------------------------------
# En sí no planeo armar muchas listas de datos, pero la cosa es que los valores de Alfa
# y dt utilizados varían y me gustaría armar dos conjuntos que me guarden estos valores
# para después poder iterar en estos, ya que voy a estar haciendo varios gráficos a partir
# de mis archivos. Voy a necesitar entonces dos conjuntos, uno para Alfa y otro para dt.

# Es importante partir del hecho de que mis archivos llevan por nombre: "Datos_Opiniones_alfa=$_Cdelta=$_N=$_Iter=$"

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


# Bien, esto ya me arma el conjunto de Alfas, Cdelta y N correctamente y ordenados
# Ahora podemos pasar a lo importante de esta celda

#--------------------------------------------------------------------------------------------

# Voy a armar un diccionar que contenga las listas de los nombres de los archivos asociados
# a un cierto N, Alfa y Cdelta. Me armo primero el superdiccionario, que es el diccionario,
# que contiene diccionarios, que llevan a diccionario que llevan a las listas de los nombres
# de los archivos, donde los ingresos a los diccionarios son el número de Agentes, el Alfa
# y el Cdelta respectivos. Entonces la lista se accede sabiendo el Alfa, Cdelta y N
# correspondiente de antemano.

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
    
# Ya mejoré el armado del SuperDiccionario de manera de que me cada N tenga los Alfa y cada
# Alfa tenga los Cdelta correspondientes. Antes me pasaba que el Conjunto_Alfa era el conjunto
# de TODOS los Alfas que hubiera entre todos los archivos, entonces si algún N tenía
# Alfas que el otro no, eso podía generar problemas. Ahora, como cada diccionario
# armado para cada N tiene por keys sólo los Alfas de ese N, puedo usar eso para
# definir el Conjunto_Alfa de cada N y evitar los problemas que había visto que
# iban a aparecer al querer graficar el mapa de colores de los estados finales del N=1000
    
#--------------------------------------------------------------------------------------------

# Empiezo iterando el N desde acá porque lo que voy a hacer es que al iniciar
# la iteración en N, defino mis Conjunto_Alfa y Conjunto_Cdelta en función de
# las keys de mi SuperDiccionario.
    
for AGENTES in [1000]:
    
    Conjunto_Alfa = list(SuperDiccionario[AGENTES].keys())
    
    Conjunto_Cdelta = list(SuperDiccionario[AGENTES][Conjunto_Alfa[0]].keys())
    
    # Primero me armo los grid para el Colormap. Para eso primero tengo que armarme un array 
    # y con el np.meshgrid armarme los grids del pcolormesh. Esto lo voy a usar para
    # armar el gráfico Varianza Tiempo Simulación
    
    Conjunto_Alfa.reverse() # Lo invierto para que me quede el uno arriba y no abajo
    
    x = np.array(Conjunto_Cdelta)
    y = np.array(Conjunto_Alfa)
    
    Conjunto_Alfa.reverse() # Lo vuelvo a invertir para que de nuevo esté como siempre.
    
    XX,YY = np.meshgrid(x,y)
    
    ZZV = np.zeros(XX.shape) # Esta es la matriz de valores para la varianza
#    ZZP = np.zeros(XX.shape) # Esta es la matriz de valores para los valores de opiniones máximas
#    ZZE = np.zeros(XX.shape) # Esta es la matriz con valores de entropía para las distribuciones por cuadrantes
    
    # Con esto ya tengo armados los grids de XX,YY y de paso me armo el grid
    # del ZZ para ir rellenándolo a medida que corro todo el programa, o usando
    # los datos que ya guardé de antes. Para eso es el módulo siguiente
    
    #---------------------------------------------------------------------------------------------

    # Voy a iterar esto para todos los archivos de datos que tengo
    
    for ALFA,ialfa in zip(Conjunto_Alfa,np.arange(len(Conjunto_Alfa))):
        
        # Defino mi figura y le defino el tamaño con plt.figure. Le defino algunos parámetros
        # le pongo el grid y después defino los valores del eje X y el array que es el fondo
        # para cada nuevo stack de distribución de valores.
        
#        fig = plt.figure("Distribucion por cuadrantes", figsize=(20,12))
#        Xhisto = np.arange(5)
#        Fondo = np.zeros(5)
        
        #-----------------------------------------------------------------------------------
        
        for CDELTA,icdelta in zip(Conjunto_Cdelta,np.arange(len(Conjunto_Cdelta))):
            
            #-----------------------------------------------------------------------------------
            
            # Creo el array TideSi, la cual voy a usar para guardar un nuevo valor en la matriz ZZV
            # para cada combinación de Alfas y Cdelta
            # Creo el array Maximos 
            
            TideSi = np.zeros(len(SuperDiccionario[AGENTES][ALFA][CDELTA]))
#            Promedios = np.zeros(len(SuperDiccionario[AGENTES][ALFA][CDELTA]))
#            OpinionesFinales = np.array([])
            
            
            #-------------------------------------------------------------------------------------
            
            for nombre,numero in zip (SuperDiccionario[AGENTES][ALFA][CDELTA],np.arange(len(SuperDiccionario[AGENTES][ALFA][CDELTA]))):

                #--------------------------------------------------------------------------------------------

                # Levanto los datos del archivo original y separo los datos en tres listas.
                # Una para la matriz de Adyacencia, una para la matriz de superposición y una para los vectores de opiniones

                Datos = ldata("{}/{}".format(Archivos_Datos[0],nombre))

#                Ady = Datos[1][1:len(Datos[1])] # Lista con elementos de la matriz de Adyacencia
#                Ady = [int(x) for x in Ady]
#
#                Sup = Datos[3][1:len(Datos[3])] # Lista con elementos de la matriz de Superposición
#                Sup = [float(x) for x in Sup]

                # Lista con elementos de los vectores de opinión. Al final sí había una forma compacta de hacer esto.
                # Si la matriz de Adyacencia evoluciona en el tiempo, va a haber que ver de hacer cambios acá.
                Opi = np.zeros((len(Datos[5::]),len(Datos[5])-1))
                for fila,ifila in zip (Datos[5::],np.arange(len(Datos[5::]))):
                    Opi[ifila] = fila[1::]

                # Mis listas ya se arman correctamente, tengo separados sin dramas los valores de mis tres matrices.

                #----------------------------------------------------------------------------------------------

                # Voy a ir armando mi array con los valores de Tiempo de Simulación.
                # Lo voy a llamar TideSi
                
                TideSi[numero] = Opi.shape[0]*0.1 # 0,1 es el paso temporal dt
                
                # Esto debería funcionar derechito.
                
                #------------------------------------------------------------------------------------------------
                
                # Quiero hacer un estudio de cómo varía el máximo al cual llega el sistema en función del
                # cos(delta) y alfa. La idea es mirar las opiniones finales, promediar los máximos en
                # las simulaciones realizadas y desde ahí asignar ese valor a cada punto del colormap.
                
#                Promedios[numero] = np.mean((np.abs(Opi[len(Opi)-1])))
                
                # Esto me guarda en cada posición del array el máximo de las opiniones finales alcanzadas
                # en cada simulación
                
                #-----------------------------------------------------------------------------------------------
                
                # Voy a armar el vector OpinionesFinales colocando los valores de las opiniones
                # en la última iteración de cada simulación.
                
#                OpinionesFinales = np.concatenate((OpinionesFinales,Opi[len(Opi)-1]), axis = None)
                
                # Esto me arma un vector que tiene las opiniones de la última iteración de todas las
                # simulaciones de un sistema con un cierto conjunto de parámetros.
                
                #-----------------------------------------------------------------------------------------------
                
            # Acá lo que voy a hacer es rellenar el grid de ZZV con los valores de los resultados de
            # opiniones finales
           
            Sumatoria = np.sum((TideSi*TideSi)-(np.ones(len(TideSi))*np.mean(TideSi)*np.mean(TideSi)))
            Varianza = math.sqrt(Sumatoria/len(TideSi))
        
            ZZV[len(Conjunto_Alfa)-1-ialfa, icdelta] = np.log10(Varianza+1)
            
            # Esto ya debería correctamente armarme el ZZV ubicando para cada par de valores
            # alfa y cos(delta) su respectiva Varianza. Lo siguiente es tomar eso al final y graficarlo.
                
            #-------------------------------------------------------------------------------------------------
            
            # Acá lo que voy a hacer es rellenar el grid de ZZM con los valores de los maximos promedios
            # de las opiniones finales
        
#            ZZP[len(Conjunto_Alfa)-1-ialfa, icdelta] = np.mean(Promedios)
            
            # Esto ya debería correctamente armarme el ZZM ubicando para cada par de valores
            # alfa y cos(delta) su respectivo valor máximo. Lo siguiente es tomar eso al final y graficarlo.
                
            #-------------------------------------------------------------------------------------------------

            # Ok, esto me confundió mucho en un principio. La idea es que uso ClasificaciónCuadrantes para
            # armar el array que tenga los números de los cuadrantes en los que se encuentran las opiniones.
            # Defino los bins a mano, total sé que distribuyo mis opiniones en los cuadrantes del 1 al 4, y
            # el 0 es para aquellos en los que están muy cerca del cero.
            
#            plt.figure("Distribucion por cuadrantes")
#            
#            Cuadrantes = ClasificacionCuadrantes(OpinionesFinales)
#            Bins = [-0.5,0.5,1.5,2.5,3.5,4.5]
            
            # Calculo la distribución. Del np.histogram obtengo dos arrays, el primero es el histograma
            # y el segundo es los bins. Para evitar problemas, mando eso a la nada misma y listo.
            
#            [Yhisto,nada] = np.histogram(Cuadrantes, bins = Bins)
#            
#           # Esto lo saqué del manual de uso. Simplemente grafica en el sistema de ejes del subplot
#           # el gráfico de barras y se encarga de tomar siempre como piso el anterior gráfico de barras
#           # de manera de ir stackeando las barras. Eso me va a permitir mostrar variso gráficos 
#           # juntos y con eso recorrer varios alfas.
#            
#           plt.bar(Xhisto, Yhisto, 0.5, bottom = Fondo, label = r"cos($\delta$) = {}".format(CDELTA))
#           Fondo = Fondo+Yhisto
            
#           #---------------------------------------------------------------------------------------------------
#            
#           Voy a aprovechar la cuenta hecha para distribucion por Cuadrantes para ir calculando la Entropía.
#           A fin de cuentas, la entropía va a estar vista en función de la distribución de las opiniones en
#           los cuadrantes. De paso, Seba me dijo que ignore el tema de las opiniones que se van a cero.
#           Son muy pocas en general, así que no importan mucho, ¿Pero debería simplemente ignorarlas?
#           Definitivamente son despreciables, dale para adelante.
            
#            Probabilidades = Yhisto[1::][Yhisto[1::] != 0]/np.sum(Yhisto[1::])
#            ZZE[len(Conjunto_Alfa)-1-ialfa, icdelta] = np.matmul(Probabilidades, np.log2(Probabilidades))*(-1)
            
        #---------------------------------------------------------------------------------------------------

#        plt.figure("Distribucion por cuadrantes")
#        plt.grid()
#        plt.rcParams.update({'font.size': 18})
#        plt.ylabel("Ocurrencias")
#        plt.xlabel("Cuadrantes")
#        plt.title(r"Distribución de opiniones en cuadrantes, $\alpha$ = {}".format(ALFA))
#        plt.legend()
#        plt.savefig("../Imagenes/ER2/N={}/Distribucion Cuadrantes Alfa={}.png".format(AGENTES,ALFA), bbox_inches = "tight")
#        plt.close("Distribucion por cuadrantes")
#    #         plt.show()
#    
    
    
    
    #-------------------------------------------------------------------------------------------------
            
            
    # Acá termino mi gráfico de Fases, una vez que recorrí todos los Alfa y Cdelta.

    # Defino los parámetros usuales de mi gráfico

    plt.figure("Varianza TideSi",figsize=(20,12))
    plt.rcParams.update({'font.size': 18})
    plt.xlabel(r"cos($\delta$)")
    plt.ylabel(r"$\alpha$")
    plt.title("Varianza del Tiempo de Simulación en el espacio de parámetros")

    # Grafico la línea del Alfa Crítico teórico

    Xa = np.arange(-0.05,1.05,0.01)
    Ya = np.array([AlfaC(x) for x in Xa])
    plt.plot(Xa,Ya,"--",color = "black",linewidth = 4, label = r"$\alpha_c$ teórico")

    # Hago el ploteo del mapa de colores con el colormesh y usando el mapa de colroes creado por mi.

    plt.legend()
    plt.pcolormesh(XX,YY,ZZV,shading="nearest", cmap = "plasma")
    plt.colorbar()
    plt.savefig("../Imagenes/ER2/N={}/Varianza EP.png".format(AGENTES), bbox_inches = "tight")
    plt.close("Varianza TideSi")
#     plt.show()

    #---------------------------------------------------------------------------------------------------
    
    # Acá termino mi gráfico de Fases, una vez que recorrí todos los Alfa y Cdelta.

    # Defino los parámetros usuales de mi gráfico

#    plt.figure("Promedios EP",figsize=(20,12))
#    plt.rcParams.update({'font.size': 18})
#    plt.xlabel(r"cos($\delta$)")
#    plt.ylabel(r"$\alpha$")
#    plt.title("Promedios de Opiniones en el espacio de parámetros")
#
#    # Grafico la línea del Alfa Crítico teórico
#
#    Xa = np.arange(-0.05,1.05,0.01)
#    Ya = np.array([AlfaC(x) for x in Xa])
#    plt.plot(Xa,Ya,"--",color = "black",linewidth = 4, label = r"$\alpha_c$ teórico")
#
#    # Hago el ploteo del mapa de colores con el colormesh y usando el mapa de colores creado por mi.
#
#    plt.legend()
#    plt.pcolormesh(XX,YY,ZZP,shading="nearest", cmap = "viridis")
#    plt.colorbar()
#    plt.savefig("../Imagenes/ER2/N={}/Promedios EP.png".format(AGENTES), bbox_inches = "tight")
#    plt.close("Promedios EP")
#     plt.show()

    #---------------------------------------------------------------------------------------------------
    
    # Acá termino mi gráfico de Fases, una vez que recorrí todos los Alfa y Cdelta.

    # Defino los parámetros usuales de mi gráfico

#    plt.figure("Entropia EP",figsize=(20,12))
#    plt.rcParams.update({'font.size': 18})
#    plt.xlabel(r"cos($\delta$)")
#    plt.ylabel(r"$\alpha$")
#    plt.title("Entropía de distribuciones en el espacio de parámetros")
#
#    # Grafico la línea del Alfa Crítico teórico
#
#    Xa = np.arange(-0.05,1.05,0.01)
#    Ya = np.array([AlfaC(x) for x in Xa])
#    plt.plot(Xa,Ya,"--",color = "black",linewidth = 4, label = r"$\alpha_c$ teórico")
#
#    # Hago el ploteo del mapa de colores con el colormesh y usando el mapa de colores creado por mi.
#
#    plt.legend()
#    plt.pcolormesh(XX,YY,ZZE,shading="nearest", cmap = "viridis")
#    plt.colorbar()
#    plt.savefig("../Imagenes/ER2/N={}/Entropía EP.png".format(AGENTES), bbox_inches = "tight")
#    plt.close("Entropia EP")
#     plt.show()

    #---------------------------------------------------------------------------------------------------
                
                
                

Tiempo()

