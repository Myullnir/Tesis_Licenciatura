

import matplotlib.pyplot as plt
from matplotlib.pyplot import cm
from scipy.optimize import minimize
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import random
import time
import pandas as pd
import math
import csv
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
        R = Dividendo - D

        # Compruebo en qué casillero cae el ángulo y returneo el índice
        if R <= Delta/2:
            return D # En este caso el ángulo se encuentra entre (D*Delta-Delta/2,D*Delta+Delta/2]
        elif R > Delta/2:
            return (D+1)%72 # En este caso el ángulo se encuentra entre ((D+1)*Delta-Delta/2,(D+1)*Delta+Delta/2]
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

def EstadoFinal(Lista):
    
    # Tomo la lista y la convierto en array para trabajarla mejor
    Array = np.array(Lista)
    
    #----------------------------------------------------------
    # Primero veo el caso de que hayan tendido a cero
    
    ArrayAbs = np.absolute(Array)
    if max(ArrayAbs)<0.1:
        return "Consenso"
    
    #----------------------------------------------------------
    # Ahora veamos los otros dos casos. Primero voy a armar
    # un array que tenga las opiniones del tópico 1, y otro
    # con las opiniones del tópico 2.
    
    ArrayT1 = Array[0:len(Array):2]
    ArrayT2 = Array[1:len(Array):2]
    
    ArrayProd = np.multiply(ArrayT1,ArrayT2)
    for producto in ArrayProd[1:len(ArrayProd)-1]:
        if producto*ArrayProd[0]<0:
            return "Polarizacion"
    
    return "Ideologico"

# Lo probé con algunos vectores de prueba y parece funcar bárbaro. Habrá que probar
# más en detalle. Se me ocurre usar esto para que los gráficos estén etiquetados y
# mirar si en alguno se equivoca.

#-----------------------------------------------------------------------------------------------

# Acá lo que voy a hacer es preparar los colores que voy a usar para definir los puntos finales
# de las trayectorias de las opiniones

Divisiones = 72
color=cm.rainbow(np.linspace(0,1,Divisiones))


# Lo que hice acá es definir una ¿lista? que tiene en cada casillero los datos que definen un color.
# Tiene diferenciados 720 colores, es decir que tengo un color para cada región de 0.5 grados. Estas regiones
# las voy a distribuir centrándolas en en cada ángulo que cada color representa. Por lo tanto,
# Los vectores que tengan ángulo entre -0.25º y 0.25º tienen el primer color. Los que tengan entre
# 0.25º y 0.75º tienen el segundo color. Y así. Por tanto yo tengo que hallar una fórmula que para
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
        SuperDiccionario[AGENTES][ALFA] = dict()
        for CDELTA in Conjunto_Cdelta:
            SuperDiccionario[AGENTES][ALFA][CDELTA] = []
            

for nombre in Archivos_Datos[1:len(Archivos_Datos)]:
    alfa = float(nombre.split("_")[2].split("=")[1])
    Cdelta = float(nombre.split("_")[3].split("=")[1])
    N = int(nombre.split("_")[4].split("=")[1])
    SuperDiccionario[N][alfa][Cdelta].append(nombre)


#---------------------------------------------------------------------------------------------

# Voy a iterar esto para todos los archivos de datos que tengo

for AGENTES in [100]:
    for ALFA in Conjunto_Alfa:
        
        # Abro el gráfico de Distribución de Opiniones Finales.
        
        plt.figure("Distribucion de Valores",figsize=(20,12))
        
        for CDELTA in Conjunto_Cdelta:
            
            #-----------------------------------------------------------------------------------
            
            # Abro mis gráficos, creo listas que voy a llenar con todas las simulaciones y armo algunas cosas varias
            # que voy a necesitar para después
            
#            plt.figure("Trayectoria Opiniones",figsize=(20,12))
#            plt.figure("Variaciones Promedio",figsize=(20,12))
#            PuntosFinales = []
            OpinionesFinales = []
#            Colores2 = cm.rainbow(np.linspace(0,1,len(SuperDiccionario[AGENTES][ALFA][CDELTA])))
            
            #-------------------------------------------------------------------------------------
            for nombre,numero in zip (SuperDiccionario[AGENTES][ALFA][CDELTA],np.arange(len(SuperDiccionario[AGENTES][ALFA][CDELTA]))):

                #--------------------------------------------------------------------------------------------

                # Levanto los datos del archivo original y separo los datos en tres listas.
                # Una para la matriz de Adyacencia, una para la matriz de superposición y una para los vectores de opiniones

                Datos = ldata("{}/{}".format(Archivos_Datos[0],nombre))

                Ady = Datos[1][1:len(Datos[1])] # Lista con elementos de la matriz de Adyacencia
                Ady = [int(x) for x in Ady]

                Sup = Datos[3][1:len(Datos[3])] # Lista con elementos de la matriz de Superposición
                Sup = [float(x) for x in Sup]

                # Lista con elementos de los vectores de opinión. Al final sí había una forma compacta de hacer esto.
                # Si la matriz de Adyacencia evoluciona en el tiempo, va a haber que ver de hacer cambios acá.
                Opi = [[float(x) for x in fila[1:len(fila)]] for fila in Datos[5:len(Datos)]]

                # Mis listas ya se arman correctamente, tengo separados sin dramas los valores de mis tres matrices.

                #----------------------------------------------------------------------------------------------

                # Acabo de caer en la cuenta que aunque no guarde los datos de las variaciones,
                # puedo calcularlas, total tengo todos los datos de opiniones del sistema. El renglón de
                # Var define la lista por comprensión.

#                Var = [math.sqrt(np.sum(np.array([((x2-x1)**2)/len(Opi[i]) for x1,x2 in zip (Opi[i],Opi[i+1])]))) for i in range(len(Opi)-1)]


                # Para algunos valores de dt me ocurre que el sistema llega a valores de variación cero muy rápido.
                # Eso en el gráfico de logaritmo lo único que ahce es incluir muchos valores del eje x en los
                # cuales no hay nada graficado. Comprimiendo de manera artificial mi gráfico a la izquierda, y 
                # dificultando por tanto su lectura. Por ello es que al Var le voy a cortar todo valor que tenga
                # a partir de que uno de sus valores se haga cero
#                 for i in range(len(Var)):
#                     if Var[i]==0:
#                         break
#                 Var = Var[0:i]

#                X = np.arange(0,len(Var))*0.1 # El dt usado en todos los archivos es 0.1
#
#                plt.figure("Variaciones Promedio")
#                plt.semilogy(X,Var, "--",c = Colores2[numero],linewidth = 2)

                # El programa sigue funcionando bárbaro, lo cual es buenísimo. Corta en el momento
                # adecuado y el comportamiento es razonbale. El guardado y el cerrado de la figura
                # lo dejo para el final del for de nombres. El tema de eso es que entonces
                # tengo que iniciar el siguiente gráfico antes de cerrar este. Eso no es un problema
                # para el código o de hacer, es sólo un tema de que dificulta un poquito más la modularidad
                # del código porque ahora las cosas se mezclan y el cierre de este módulo está al final

                #--------------------------------------------------------------------------------------------------
                
                
                # Acá voy a calcular al sujeto que voy a usar para normalizar mis gráficos. Tiene que ser el máximo
                # valor de opinión que haya alcanzado cualquier sujeto en cualquier momento.
                
#                MaxNorm = 0
#                for Opiniones in Opi:
#                    MaxNorm = max(MaxNorm,max(np.absolute(np.array(Opiniones))))
#                MaxNorm = 1/MaxNorm
                
                # Esto funciona perfecto. El único tema a considerar es que este valor MaxNorm se traspasa
                # a otros módulos, entonces eso hace que esos módulos no sean tan independientes. En particular
                # me refiero al módulo que construye el diccionario OdT y el que arma la lista de puntos
                # finales PuntosFinales. Supongo que esto se podría solucionar directamente normalizando el 
                # vector de opiniones. Entonces los otros trabajaría por su cuenta sin mezclar cosas
                # de módulos que podrían no copiarse en futuros códigos.
                
                #----------------------------------------------------------------------------------------------

                # Voy a intentar replicar el gráfico de Baumann. Para eso voy a querer graficar la trayectoria
                # de todos los agentes. Como van a ser muchos agentes, me conviene que esas trayectorias se grafiquen
                # con líneas finitas

#                OdT = dict() # OdT es Opiniones del Tópico.
#                for agente in range(N):
#                    for topico in range(T):
#                        OdT[topico+T*agente] = []
#                        for iteracion in range(len(Opi)):
#                            OdT[topico+T*agente].append(Opi[iteracion][agente*T+topico]*MaxNorm)

                # Esto levanta correctamente los valores de las opiniones de los agentes para cada uno de sus tópicos.
                # De paso, le agregué ahora que las listas del diccionario no se sobreescriban. Eso me va a permitir
                # graficar los puntos finales sin necesidad de revisar una segunda vez la lista Opi

                #-----------------------------------------------------------------------------------------------

                # Como todavía tengo dos tópicos, puedo graficar esto en un plano. Así que ahora voy a hacer
                # un código presuponiendo que la cantidad de tópicos es 2. Sino, esto no debería realizarse.
                # Atento a eso.
                # Como ahora las listas en el diccionario no se sobreescriben, puedo hacer esto con un for aparte
                # de lo anterior

#                plt.figure("Trayectoria Opiniones")
#                for agente in range(N):
#                    plt.plot(OdT[0+T*agente],OdT[1+T*agente], color="gray",linewidth = 0.6, alpha=0.2)
                    
                #-------------------------------------------------------------------------------------------------
                
                # Voy a guardar las posiciones finales de todos mis sujetos para poder marcar los puntos finales
                # por encima de las líneas grises.
                
#                PuntosFinales.append([x*MaxNorm for x in Opi[len(Opi)-1]])
                
                #-------------------------------------------------------------------------------------------------
                
                # Ahora lo que voy a hacer es tomar el estado final del sistema y usar la función EstadoFinal
                # para determinar si el sistema llegó a un Consenso, Polarización o Estado Ideológico.
                
                OpinionesFinales = OpinionesFinales+Opi[len(Opi)-1]
                
                # Con esto me armo la lista de estados finales de mi sistema
                
            #-------------------------------------------------------------------------------------------------

            # Genial, así como está esto ya arma el gráfico de las trayectorias de las opiniones. Ahora, me gustaría
            # colocar puntos marcando el final de mis trayectorias.

#            plt.figure("Trayectoria Opiniones")
#            for iteracion in range(len(PuntosFinales)):
#                for agente in range(N):
#                    indice = Indice_Color([PuntosFinales[iteracion][0+T*agente],PuntosFinales[iteracion][1+T*agente]],Divisiones)
#                    plt.plot(PuntosFinales[iteracion][0+T*agente],PuntosFinales[iteracion][1+T*agente], "o" ,c = color[indice], markersize=10)


            #----------------------------------------------------------------------------------------------

            # Estos son los parámetros que definen el tamaño del gráfico, tamaño de la letra y nombres de
            # los ejes. Luego de eso guardo la figura y la cierro. Esto es para la figura de
            # TdO.
            
#            plt.figure("Trayectoria Opiniones")
#            plt.rcParams.update({'font.size': 18})
#            plt.xlabel("Tópico 1")
#            plt.ylabel("Tópico 2")
#            plt.title(r"Trayectoria de las opiniones en el espacio de tópicos para $\alpha$={},cos($\delta$)={} y N={}".format(ALFA,CDELTA,AGENTES))
#            xmin,xmax = plt.xlim()
#            ymin,ymax = plt.ylim()
#            plt.text((xmax+xmin)/2*0.9,ymax*0.9,EstadoFinal(OpinionesFinales), bbox=dict(facecolor='White', alpha=0.7))
#            plt.savefig("../Imagenes/ER2/Trayectoria de las opiniones_alfa={:.2f}_Cdelta={}_N={}.png".format(ALFA,CDELTA,AGENTES),bbox_inches = "tight")
#            plt.close("Trayectoria Opiniones")

            #------------------------------------------------------------------------------------------------
            
            # Esto me guarda el gráfico de variaciones Promedio
#            plt.figure("Variaciones Promedio")
#            plt.rcParams.update({'font.size': 18})
#            plt.xlabel("Tiempo Simulado")
#            plt.ylabel("Variación promedio de las opiniones")
#            plt.axis("tight")
#            plt.title(r"Variación Promedio del sistema para $\alpha$={}_cos($\delta$)={}_N={}".format(ALFA,CDELTA,AGENTES))
#            plt.grid()
#            plt.savefig("../Imagenes/ER2/Variaciones Promedio_alfa={:.2f}_Cdelta={}_N={}.png".format(ALFA,CDELTA,AGENTES),bbox_inches = "tight")
#            plt.close("Variaciones Promedio")
            
            #------------------------------------------------------------------------------------------------------------------
        
            # Puedo armar acá el gráfico de distribución de valores. Además, para esto puedo usar una lista que
            # ya armé antes que es la de Opiniones Finales. A partir de esta voy a hacer las distribuciones del
            # Tópico 1 y del 2 y eso voy a graficar. Las distribuciones las voy a calcular con el np.histogram.
            # Como tengo 100 agentes y 40 simulaciones, entonces tengo 4000 opiniones para cada tópico. Me parece
            # razonable separar esto en 40 bins.
            
            ArrayOpifin = np.array(OpinionesFinales)
            
            Histo,Bordes_Bin = np.histogram(ArrayOpifin,bins=30)
            
            EjeX = [(Bordes_Bin[i+1]+Bordes_Bin[i])/2 for i in range(len(Bordes_Bin)-1)]
            
            plt.figure("Distribucion de Valores")
            plt.plot(EjeX,Histo,"--",linewidth = 3, label = r"$cos(\delta)$ = {}".format(CDELTA))
            
        plt.rcParams.update({'font.size': 18})
        plt.xlabel("Valores de Opiniones")
        plt.ylabel("Ocurrencias")
        plt.title(r"Distribucion de las opiniones para $\alpha$={:.2f} y N={}".format(ALFA, AGENTES))
        plt.grid()
        plt.savefig("../Imagenes/ER2/Distribución opiniones_N={}_alfa={:.2f}.png".format(AGENTES,ALFA),bbox_inches = "tight")
        plt.close("Distribucion de Valores")
            
        #-----------------------------------------------------------------------------------------------------------
        
        
        print("Ya terminé con el Alfa:{:.2f}".format(ALFA))
        Tiempo()


# -------------------------------------------------------------------------------------------------
       
        
Tiempo()