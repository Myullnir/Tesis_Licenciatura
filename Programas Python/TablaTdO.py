# -*- coding: utf-8 -*-
"""
Created on Mon Apr 19 17:46:45 2021

@author: Favio
"""

import matplotlib.pyplot as plt
from matplotlib.pyplot import cm
#from scipy.optimize import minimize
#from mpl_toolkits.mplot3d import Axes3D
from matplotlib.colors import LinearSegmentedColormap
import numpy as np
#import random
import time
import pandas as pd
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


# En esta celda lo que voy a hacer es armar los gráficos de Trayectorias de Opiniones (TdO)
# para las simulaciones hechas con N=100 y N=1000 agentes, con dt = 0,1. Esas simulaciones están
# hechas sobre redes estáticas Erdós Renyi con grado medio 8, con CritCorte = 10^(-8) o 10^(-6).
# Lo importante es que tengo 40 simulaciones hechas para cada valor de Alfa y Delta y mi intención
# es graficar los datos de esas 40 simulaciones en un sólo gráfico.

# Después de eso la idea es tomar todos estos datos y empezar a armar el gráfico del comportamiento
# del sistema en el espacio de fases en función de alfa y delta.

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
    
    Conjunto_Alfa = [0, 0.05, 0.1, 0.15, 0.2, 0.3, 0.4]
    
    Conjunto_Cdelta = [0, 0.2, 0.4, 0.6, 0.8, 1]
    
    #--------------------------------------------------------------------------------------

    # Voy a primero graficar mi tabla de gráficos de TdO. Primero armo mi figura con
    # plt.figure. Después le pongo ejes explícitimante con plt.axes() y cambio el tamaño
    # de la letra a 40. 
    
    fig = plt.figure(figsize=(64,36))
    plt.axes()
    plt.rcParams.update({'font.size': 40})
    
    # Ahora, trabajando sobre los ejes, les pongo nombres al eje X e Y. Defino el tamaño
    # de los gráficos que van a estar en mi tabla de gráficos. "a" es el ancho y "b" es
    # el alto. Como todos los gráficos utilizados son iguales, o quizás porque el gridspec
    # genera espacios iguales, el tamaño de todos los gráficos es el mismo. Además, como
    # en la figura general fig no estoy ploteando nada, puedo definir que los límites vayan
    # de 0 a 1, la verdad esos es realmente indistinto. Luego, como conozco el tamaño total de
    # lo graficado en mi eje X y conozco el tamaño de mis gráficos, simplemente distribuyo los
    # ticks en X y en Y sabiendo que los ticks van en el centro de las imágenes, y por tanto
    # en X van de [a/2;1-a/2] y en Y van de [b/2;1-b/2]. Por eso uso el linspace para ubicar
    # de manera uniforme los ticks
    
    plt.xlabel(r"cos($\delta$)")
    plt.ylabel(r"$\alpha$")
    a = 1/len(Conjunto_Cdelta)
    b = 1/len(Conjunto_Alfa)
    plt.xticks(np.linspace(a/2,1-a/2,len(Conjunto_Cdelta)),Conjunto_Cdelta)
    plt.yticks(np.linspace(b/2,1-b/2,len(Conjunto_Alfa)),Conjunto_Alfa)
    plt.xlim(0,1)
    plt.ylim(0,1)
    
    
    # Sobre mi figura general agrego un gridspace usando add.gridspec. Los primeros
    # dos argumentos son la cantidad de filas y columnas que tendra la grilla. Además,
    # hspace es la separación que tendrán en filas y wspace la separación en columnas.
    # Lo pongo en cero porque como voy a graficar muchas cosas juntas, mejor reducir
    # el espacio todo lo posible. Sería un tema de mayor preocupación si graficara
    # durante la creación de esta figura en vez de simplemente levantar imágenes.
    # Lo siguiente es llamar al comando subplots de Gridspace, que me devuelve
    # las direcciones de los ejes para graficar lo que necesito.
    
    gs = fig.add_gridspec(len(Conjunto_Alfa),len(Conjunto_Cdelta),hspace=0,wspace=0)
    axs = gs.subplots(sharex='col', sharey='row')
    
    # Finalmente recorro la lista de imágenes que armé previamente y las voy
    # ubicando en sus respectivos lugares, es decir sus ejes correspondientes.
    # Para esto primero leo la imagen con imread, la ploteo con imshow con
    # una interpolación de "spline16" para no perder calidad en la imagen y
    # le saco los ejes porque al final del día estas son imágenes de gráficos
    # que ya tienen sus propias magnitudes graficadas, ponerles ejes extras 
    # es redundante y además confunde y me achica las imágenes.
    # Los ejes los completo en filas con len(Lista_Alfa)-1-i porque quiero
    # que los gráficos de Alfa Cero vayan abajo de todo y que el Alfa crezca
    # con el eje Y.
    
    
    #---------------------------------------------------------------------------------------------

    # Voy a iterar esto para todos los archivos de datos que tengo
    
    for ALFA,ialfa in zip(Conjunto_Alfa,np.arange(len(Conjunto_Alfa))):
        
        for CDELTA,icdelta in zip(Conjunto_Cdelta,np.arange(len(Conjunto_Cdelta))):
            
            #-----------------------------------------------------------------------------------
            
            OpinionesFinales = np.array([])
            PuntosFinales = np.array([])
            axs[len(Conjunto_Alfa)-1-ialfa,icdelta].set_xlim((-15,15))
            axs[len(Conjunto_Alfa)-1-ialfa,icdelta].set_ylim((-15,15))
#            axs[len(Conjunto_Alfa)-1-ialfa,icdelta].axis("off")
            
            #-------------------------------------------------------------------------------------
            for nombre,numero in zip (SuperDiccionario[AGENTES][ALFA][CDELTA],np.arange(len(SuperDiccionario[AGENTES][ALFA][CDELTA]))):

                #--------------------------------------------------------------------------------------------

                # Levanto los datos del archivo original y separo los datos en tres listas.
                # Una para la matriz de Adyacencia, una para la matriz de superposición y una para los vectores de opiniones

                Datos = ldata("{}/{}".format(Archivos_Datos[0],nombre))
                

                # Lista con elementos de los vectores de opinión. Al final sí había una forma compacta de hacer esto.
                # Si la matriz de Adyacencia evoluciona en el tiempo, va a haber que ver de hacer cambios acá.
                Opi = np.zeros((len(Datos[5::]),len(Datos[5])-1))
                for fila,ifila in zip (Datos[5::],np.arange(len(Datos[5::]))):
                    Opi[ifila] = fila[1::]

                # Mis listas ya se arman correctamente, tengo separados sin dramas los valores de mis tres matrices.

                #-----------------------------------------------------------------------------------------------

                # Como todavía tengo dos tópicos, puedo graficar esto en un plano. Así que ahora voy a hacer
                # un código presuponiendo que la cantidad de tópicos es 2. Sino, esto no debería realizarse.
                # Atento a eso.
                # Como ahora las listas en el diccionario no se sobreescriben, puedo hacer esto con un for aparte
                # de lo anterior

                for agente in range(AGENTES):
                    axs[len(Conjunto_Alfa)-1-ialfa,icdelta].plot(Opi[::,0+T*agente],Opi[::,1+T*agente], color="gray",linewidth = 0.6, alpha=0.2)
                    
                #-------------------------------------------------------------------------------------------------
                
                # Cuando quiera graficar los puntos que indican el punto final de la trayectoria
                # de un agente en el espacio de fases, voy a necesitar que ese array contenga los puntos
                # correctamente normalizados. Para eso voy a construir el array PuntosFinales que involucre
                # normalización con el MaxNorm Correcto
                
                PuntosFinales = np.concatenate((PuntosFinales,Opi[len(Opi)-1]), axis=None)
                
                # Con esto me armo la lista de estados finales de mi sistema
                
            #-------------------------------------------------------------------------------------------------

            # Genial, así como está esto ya arma el gráfico de las trayectorias de las opiniones. Ahora, me gustaría
            # colocar puntos marcando el final de mis trayectorias.


            for x1,x2 in zip (PuntosFinales[0::2],PuntosFinales[1::2]):
                indice = Indice_Color(np.array([x1,x2]),Divisiones)
                axs[len(Conjunto_Alfa)-1-ialfa,icdelta].plot(x1,x2, "o" ,c = color[indice], markersize=10)
            

            #----------------------------------------------------------------------------------------------

Tiempo()

