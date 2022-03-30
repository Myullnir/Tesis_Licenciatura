# -*- coding: utf-8 -*-
"""
Created on Sat Jan  1 15:39:16 2022

@author: Favio
"""


import networkx as nx
import community as community_louvain
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
    if(x>0):
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

def EstadoFinal(Array,Histo,Bins):
    
    Topicos = 2

    # Primero identifico los tres posibles picos
    
    Nbins = len(Bins) # Esto es la cantidad de bins totales en los que dividí mi distribución
    
    Pcero = Histo[int((Nbins-1)/2)] # Esto es cuánto mide el pico en cero
    
    DistNegativa = Histo[0:int((Nbins-1)/2)] # Este es la distribución de las opiniones negativas
    Pmenos = max(DistNegativa) # Esto es la altura del pico de Distribución negativa
    
    DistPositiva = Histo[int((Nbins-1)/2)+1::] # Este es la distribución de las opiniones positivas
    Pmas = max(DistPositiva) # Esto es la altura del pico de Distribución positiva
    
    
    ###########################################################################
    
    # Ahora que tengo los picos, puedo empezar a definir el tema de los estados
    #finales. Arranco por el Consenso
    
    if Pcero == max(Pcero,Pmas,Pmenos):   #Pcero*0.85 > Pmax:  (Esto es la versión con umbral)
        return "Consenso"
    
    ###########################################################################
    
    # Ahora veamos el caso de región de transición. Este estado
    # Lo caracterizo porque el sistema tiene un pico central y picos por fuera
    # que no son definitorios del estado
    
#    Pmediano = min(Pmas,Pmenos)
    
#    if Pmaximo*0.7 < Pcero < Pmaximo*1.3 and Pmaximo*0.7 < Pmas < Pmaximo*1.3 and Pmaximo*0.7 < Pmenos < Pmaximo*1.3 :
#        return "RegionTrans"
    
    ###########################################################################
    
#    indicemenos = np.where(DistNegativa == Pmenos)[0][0]
#    indicemas = np.where(DistPositiva == Pmas)[0][0]
    
    if Pcero == min(Pcero,Pmas,Pmenos):  #and Pcero < Pmediano*0.85: (Esto es de la versión umbral)
        
        # Filtro los agentes que se hayan desviado apenas, cosa
        # de que el criterio final se decida con los agentes que se polarizaron
        # correctamente y no los que terminaron en cualquier lugar cerca del
        # cero.
        ArrayT1 = Array[0::2]
        ArrayT2 = Array[1::2]
        Maximo = max(np.absolute(Array))
        
        OpinionesFiltradas = np.zeros(len(Array))
        
        for agente,x1,x2 in zip(np.arange(len(ArrayT1)),ArrayT1,ArrayT2):
            if abs(x1) > Maximo*0.3 and abs(x2) > Maximo*0.3:
                OpinionesFiltradas[0+agente*Topicos:2+agente*Topicos] = [x1,x2]
        
        # Ahora veamos los otros dos casos. Primero voy a armar
        # un array que tenga las opiniones del tópico 1, y otro
        # con las opiniones del tópico 2.
        
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
    
    return "RegionTrans"


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

    
    # Repaso los elementos en Signos para identificar los cuadrantes de mis objetos.
    
    for x1,x2,indice in zip(Array[0::2],Array[1::2],np.arange(len(Array[0::2]))):
        Absolutos = np.abs(np.array([x1,x2]))
        if np.linalg.norm(Absolutos)< 1 or x1==0 or x2==0:
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
"""
T=2 # Defino acá el número de tópicos porque es algo que no cambia por ahora,
# pero no tenía dónde más definirlo

SuperDiccionario = dict()

for Carpeta in ["TEFinal"]:

   # CÓDIGO PARA LEVANTAR ARCHIVOS DE UNA CARPETA CON TODOS LOS ARCHIVOS MEZCLADOS
    
    CarpCheck=[[root,files] for root,dirs,files in os.walk("./DilAct/{}".format(Carpeta))]
    
    # El elemento en la posición x[0] es el nombre de la carpeta
    
    for x in CarpCheck:
        # dada = x[0].split("\\")
        Archivos_Datos = [nombre for nombre in x[1]]
        Archivos_Datos.insert(0,x[0])
        
    

    #-------------------------------------------------------------------------------------------------------
    
    # Es importante partir del hecho de que mis archivos llevan por nombre: "Datos_Adyacencia_alfa=$_Cdelta=$_N=$_Iter=$"
    # También tengo otros archivos llamados "Datos_Variacion_alfa=$_Cdelta=$_N=$_Iter=$" y
    # "Evolucion_Sistema_alfa=$_Cdelta=$_N=$_Iter=$".
    
    Conjunto_Direcciones = [Archivos_Datos[0]]
    
    SuperDiccionario[Carpeta] = dict()
    
    for nombre in Archivos_Datos[1:len(Archivos_Datos)]:
        tipo = nombre.split("_")[1]
        alfa = float(nombre.split("_")[2].split("=")[1])
        Cdelta = float(nombre.split("_")[3].split("=")[1])
        N = int(nombre.split("_")[4].split("=")[1])
        if tipo not in SuperDiccionario[Carpeta].keys():
            SuperDiccionario[Carpeta][tipo] = dict()
            SuperDiccionario[Carpeta][tipo][N] = dict()
            SuperDiccionario[Carpeta][tipo][N][Cdelta] = dict()
            SuperDiccionario[Carpeta][tipo][N][Cdelta][alfa] = [nombre]
        elif N not in SuperDiccionario[Carpeta][tipo].keys():
            SuperDiccionario[Carpeta][tipo][N] = dict()
            SuperDiccionario[Carpeta][tipo][N][Cdelta] = dict()
            SuperDiccionario[Carpeta][tipo][N][Cdelta][alfa] = [nombre]
        elif Cdelta not in SuperDiccionario[Carpeta][tipo][N].keys():
            SuperDiccionario[Carpeta][tipo][N][Cdelta] = dict()
            SuperDiccionario[Carpeta][tipo][N][Cdelta][alfa] = [nombre]
        elif alfa not in SuperDiccionario[Carpeta][tipo][N][Cdelta].keys():
            SuperDiccionario[Carpeta][tipo][N][Cdelta][alfa] = [nombre]
        else:
            SuperDiccionario[Carpeta][tipo][N][Cdelta][alfa].append(nombre)

    
    # Le hice una modificación a esta parte del código, ahora esto trabaja
    # armando el SuperDiccionario también, no sólo los Conjuntos de Alfa, Cdelta
    # y demás. Lo bueno de esto es que ahora el armado del SuperDiccionario
    # es mucho más rápido.
    
    # En este caso SuperDiccionario está juntando tanto los nombres
    # de Datos Testisgos con los de Datos Opiniones.
    #--------------------------------------------------------------------------------------------
    
    # Arranquemos con el primer gráfico. Quiero graficar las opiniones respecto del tópico 1
    # de los 10 agentes más activos y de los 10 agentes menos activos. Para eso voy a tomar datos
    # de los archivos de Evolucion_Sistema. Esos tienen en la primer fila las actividades
    # de los agentes y después tienen las opiniones de los agentes en cada iteración.
    
    for AGENTES in [1000]:
        
        #---------------------------------------------------------------------------------------------------------------
        
        TIPO = "Sistema"
        
        # Acá me voy a inicializar los arrays para graficar los mapas de colores de la red.
        
        
        # Defino el conjunto de valores de Cdelta a recorrer. Tengo que ordenarlos porque
        # el SuperDiccionario los ordena como los recibe, y el os.walk no necesariamente recorre
        # todo en orden.
        
        Conjunto_Cdelta = list(SuperDiccionario[Carpeta][TIPO][AGENTES].keys())
        Conjunto_Cdelta.sort()
        
        #----------------------------------------------------------------------------------------------------------
        
        for CDELTA,icdelta in zip(Conjunto_Cdelta,np.arange(len(Conjunto_Cdelta))):
            
            # Para cada Cdelta defino el conjunto de Alfas asociados a recorrer.
            # De nuevo, lo ordeno porque el SuperDiccionario no los tiene necesariamente ordenados.
            
            Conjunto_Alfa = list(SuperDiccionario[Carpeta][TIPO][AGENTES][CDELTA].keys())
            Conjunto_Alfa.sort()
            
            
            for ALFA,ialfa in zip(Conjunto_Alfa,np.arange(len(Conjunto_Alfa))):
                
                for nombre,numero in zip(SuperDiccionario[Carpeta][TIPO][AGENTES][CDELTA][ALFA],np.arange(len(SuperDiccionario[Carpeta][TIPO][AGENTES][CDELTA][ALFA]))):
                    
                    # Acá levanto los datos de los archivos de Evolucion_Sistema. Estos archivos tienen los siguientes datos:
                    # Actividad de Agentes
                    # Opiniones en cada iteración de todos los agentes
                    # Semilla

                    #--------------------------------------------------------------------------------------------
                
                    # Levanto los datos del archivo original y separo los datos en tres listas.
                    # Una para la matriz de Adyacencia, una para la matriz de superposición y una para los vectores de opiniones
                
                    # Tengo que hacer una diferenciación entre levantar datos de las carpetas subdividida en 4 y de la carpeta con todo mezclado.

                    # PARA LEVANTAR DATOS DE LA CARPETA TODA MEZCLADA
                    Datos = ldata("{}/{}".format(Conjunto_Direcciones[0],nombre))
                    
                    # Levanto los datos de Actividad
                    Actividad = np.array([float(x) for x in Datos[1][1::]])
                    
                    # Levanto los datos de las Opiniones Finales
                    Opi = np.zeros((len(Datos)-5,len(Datos[3])-1))
                    for fila,i in zip(Datos[3:len(Datos)-2],np.arange(len(Datos[3:len(Datos)-2]))):
                        Opi[i] = fila[1::]
                        
                    # Levanto el número de la iteración de la simulación.
                    repeticion = int(nombre.split("_")[5].split("=")[1])

                    
                    #------------------------------------------------------------------------------------------------
                    
                    # Arranquemos con el armado del gráfico, creo que puedo definir fácil cuáles son los
                    # 10 agentes con mayor actividad y cuáles son los 10 con menor actividad
                    
                    amenor = np.sort(Actividad)[4] # Esto me da el valor de actividad que es el más grande de los 5 más chicos.
                    amayor = np.sort(Actividad)[len(Actividad)-5] # Esto me da el valor de actividad que es el menor de los 5 más grandes
                    
                    
                    plt.rcParams.update({'font.size': 24})
                    plt.figure("Topico",figsize=(20,15))
                    X = np.arange(len(Opi))*0.01
                    for sujeto in np.arange(AGENTES):
                        plt.plot(X,Opi[::,sujeto],color = "gray", alpha = 0.5 ,linewidth = 0.5) 
                    # Primero plotea los 10 sujetos de mayor actividad
#                    for sujeto in np.arange(AGENTES)[Actividad <= amenor]:
#                        plt.plot(X,Opi[::,sujeto],color = "green", alpha = 0.7 ,linewidth = 3) 
#                    for sujeto in np.arange(AGENTES)[Actividad >= amayor]:
#                        plt.plot(X,Opi[::,sujeto],color = "red", alpha = 0.7 ,linewidth = 3)
#                    if sujeto == 1:
#                        plt.plot(X[::100],Testigos[sujeto][inicio:final:200],linestyle = "", marker = "o", color = "red", markersize = 12, alpha = 0.7)
    #                    plt.plot(X,Testigos[sujeto][repeticion*Iteraciones+1:(repeticion+1)*Iteraciones+1:2], label="T=1,agente={}".format(AgentesTestigos[sujeto]), linewidth = 4)
                    plt.xlabel("Tiempo")
                    plt.ylabel(r"$x^1$")
                    plt.xticks(np.arange(0,31,2))
                    if ALFA == 0:
                        plt.ylim(-5,5)
                    if ALFA == 0.5:
                        plt.ylim(-30,30)
                    plt.grid()
    #                plt.annotate(r"$\alpha$={},cos($\delta$)={},N={}".format(ALFA,CDELTA,AGENTES), xy=(0.5,0.75),xycoords='axes fraction',fontsize=20,bbox=dict(facecolor='White', alpha=0.7))
                    plt.savefig("../Imagenes/RedAct/{}/Topicos_alfa={:.3f}_Cdelta={:.2f}_N={}_iter={}.png".format(Carpeta,ALFA,CDELTA,AGENTES,repeticion),bbox_inches = "tight")
                    plt.close("Topico")

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Acá me preparo el código para el segundo gráfico, lo hago todo desde cero para evitar dudas,
# Después simplemente comento lo de arriba cualquier cosa. Armo dos relevamientos de nombres,
# uno para redes de actividad y otro para redes estáticas
            
T=2 # Defino acá el número de tópicos porque es algo que no cambia por ahora,
# pero no tenía dónde más definirlo

SuperDiccionario = dict()

for Carpeta in ["TEFinal"]:

   # CÓDIGO PARA LEVANTAR ARCHIVOS DE UNA CARPETA CON TODOS LOS ARCHIVOS MEZCLADOS
    
    CarpCheck=[[root,files] for root,dirs,files in os.walk("./DilAct/{}".format(Carpeta))]
    
    # El elemento en la posición x[0] es el nombre de la carpeta
    
    for x in CarpCheck:
        # dada = x[0].split("\\")
        Archivos_Datos = [nombre for nombre in x[1]]
        Archivos_Datos.insert(0,x[0])
        
    

    #-------------------------------------------------------------------------------------------------------
    
    # Es importante partir del hecho de que mis archivos llevan por nombre: "Datos_Adyacencia_alfa=$_Cdelta=$_N=$_Iter=$"
    # También tengo otros archivos llamados "Datos_Variacion_alfa=$_Cdelta=$_N=$_Iter=$" y
    # "Evolucion_Sistema_alfa=$_Cdelta=$_N=$_Iter=$". Estos son los archivos de TEFinal.
    
    Conjunto_Direcciones = [Archivos_Datos[0]]
    
    SuperDiccionario[Carpeta] = dict()
    
    for nombre in Archivos_Datos[1:len(Archivos_Datos)]:
        tipo = nombre.split("_")[1]
        alfa = float(nombre.split("_")[2].split("=")[1])
        Cdelta = float(nombre.split("_")[3].split("=")[1])
        N = int(nombre.split("_")[4].split("=")[1])
        if tipo not in SuperDiccionario[Carpeta].keys():
            SuperDiccionario[Carpeta][tipo] = dict()
            SuperDiccionario[Carpeta][tipo][N] = dict()
            SuperDiccionario[Carpeta][tipo][N][Cdelta] = dict()
            SuperDiccionario[Carpeta][tipo][N][Cdelta][alfa] = [nombre]
        elif N not in SuperDiccionario[Carpeta][tipo].keys():
            SuperDiccionario[Carpeta][tipo][N] = dict()
            SuperDiccionario[Carpeta][tipo][N][Cdelta] = dict()
            SuperDiccionario[Carpeta][tipo][N][Cdelta][alfa] = [nombre]
        elif Cdelta not in SuperDiccionario[Carpeta][tipo][N].keys():
            SuperDiccionario[Carpeta][tipo][N][Cdelta] = dict()
            SuperDiccionario[Carpeta][tipo][N][Cdelta][alfa] = [nombre]
        elif alfa not in SuperDiccionario[Carpeta][tipo][N][Cdelta].keys():
            SuperDiccionario[Carpeta][tipo][N][Cdelta][alfa] = [nombre]
        else:
            SuperDiccionario[Carpeta][tipo][N][Cdelta][alfa].append(nombre)

    
    # Le hice una modificación a esta parte del código, ahora esto trabaja
    # armando el SuperDiccionario también, no sólo los Conjuntos de Alfa, Cdelta
    # y demás. Lo bueno de esto es que ahora el armado del SuperDiccionario
    # es mucho más rápido.
    
    # En este caso SuperDiccionario está juntando tanto los nombres
    # de Datos Testisgos con los de Datos Opiniones.
    #--------------------------------------------------------------------------------------------
    
    # Arranquemos con el primer gráfico. Quiero graficar las opiniones respecto del tópico 1
    # de los 10 agentes más activos y de los 10 agentes menos activos. Para eso voy a tomar datos
    # de los archivos de Evolucion_Sistema. Esos tienen en la primer fila las actividades
    # de los agentes y después tienen las opiniones de los agentes en cada iteración.
    
for Carpeta in ["Erdos-Renyi"]:

   # CÓDIGO PARA LEVANTAR ARCHIVOS DE UNA CARPETA CON TODOS LOS ARCHIVOS MEZCLADOS
    
    CarpCheck=[[root,files] for root,dirs,files in os.walk("./DRE/{}".format(Carpeta))]
    
    # El elemento en la posición x[0] es el nombre de la carpeta
    
    for x in CarpCheck:
        # dada = x[0].split("\\")
        Archivos_Datos = [nombre for nombre in x[1]]
        Archivos_Datos.insert(0,x[0])
        
    

    #-------------------------------------------------------------------------------------------------------
    
    # Los archivos de Erdos-Renyi son del estilo "Datos_Opiniones_alfa=$_Cdelta=$_N=$_Gm=$_ID=$_Iter=$"
    
    Conjunto_Direcciones = [Archivos_Datos[0]]
    
    SuperDiccionario[Carpeta] = dict()
    
    for nombre in Archivos_Datos[1:len(Archivos_Datos)]:
        tipo = nombre.split("_")[1]
        alfa = float(nombre.split("_")[2].split("=")[1])
        Cdelta = float(nombre.split("_")[3].split("=")[1])
        N = int(nombre.split("_")[4].split("=")[1])
        Gm = int(nombre.split("_")[5].split("=")[1])
        if tipo not in SuperDiccionario[Carpeta].keys():
            SuperDiccionario[Carpeta][tipo] = dict()
            SuperDiccionario[Carpeta][tipo][N] = dict()
            SuperDiccionario[Carpeta][tipo][N][Gm] = dict()
            SuperDiccionario[Carpeta][tipo][N][Gm][Cdelta] = dict()
            SuperDiccionario[Carpeta][tipo][N][Gm][Cdelta][alfa] = [nombre]
        elif N not in SuperDiccionario[Carpeta][tipo].keys():
            SuperDiccionario[Carpeta][tipo][N] = dict()
            SuperDiccionario[Carpeta][tipo][N][Gm] = dict()
            SuperDiccionario[Carpeta][tipo][N][Gm][Cdelta] = dict()
            SuperDiccionario[Carpeta][tipo][N][Gm][Cdelta][alfa] = [nombre]
        elif Gm not in SuperDiccionario[Carpeta][tipo][N].keys():
            SuperDiccionario[Carpeta][tipo][N][Gm] = dict()
            SuperDiccionario[Carpeta][tipo][N][Gm][Cdelta] = dict()
            SuperDiccionario[Carpeta][tipo][N][Gm][Cdelta][alfa] = [nombre]
        elif Cdelta not in SuperDiccionario[Carpeta][tipo][N][Gm].keys():
            SuperDiccionario[Carpeta][tipo][N][Gm][Cdelta] = dict()
            SuperDiccionario[Carpeta][tipo][N][Gm][Cdelta][alfa] = [nombre]
        elif alfa not in SuperDiccionario[Carpeta][tipo][N][Gm][Cdelta].keys():
            SuperDiccionario[Carpeta][tipo][N][Gm][Cdelta][alfa] = [nombre]
        else:
            SuperDiccionario[Carpeta][tipo][N][Gm][Cdelta][alfa].append(nombre)

    
    # Le hice una modificación a esta parte del código, ahora esto trabaja
    # armando el SuperDiccionario también, no sólo los Conjuntos de Alfa, Cdelta
    # y demás. Lo bueno de esto es que ahora el armado del SuperDiccionario
    # es mucho más rápido.
    
    # En este caso SuperDiccionario está juntando tanto los nombres
    # de Datos Testisgos con los de Datos Opiniones.
    #--------------------------------------------------------------------------------------------
    
    # Para el segundo gráfico lo que quiero es comparar las Variaciones Promedio de las redes
    # de actividad con la Variación Promedio de redes estáticas. En este caso tengo redes
    # de Erdos-Renyi, y tomemos además las de grado medio 12.
    
for AGENTES in [1000]:
    
    #---------------------------------------------------------------------------------------------------------------
    
    Carpeta = "TEFinal"
    TIPO = "Variacion"
    
    # Voy a moverme en los valores de Cdelta y Alfa de las redes de actividad, esos
    # son los que me importa revisar.
    
    Conjunto_Cdelta = list(SuperDiccionario[Carpeta][TIPO][AGENTES].keys())
    Conjunto_Cdelta.sort()
    
    for CDELTA,icdelta in zip(Conjunto_Cdelta,np.arange(len(Conjunto_Cdelta))):
        
        # Para cada Cdelta defino el conjunto de Alfas asociados a recorrer.
        # De nuevo, lo ordeno porque el SuperDiccionario no los tiene necesariamente ordenados.
        
        Conjunto_Alfa = list(SuperDiccionario[Carpeta][TIPO][AGENTES][CDELTA].keys())
        Conjunto_Alfa.sort()
        
        
        for ALFA,ialfa in zip(Conjunto_Alfa,np.arange(len(Conjunto_Alfa))):
            
            # Ahora que sé que estoy en los alfas y Cdeltas de la red de actividad, abro
            # mi gráfico y luego reviso primero la Variación Promedio de la red de actividad.
            # Después reviso la de la red estática.
            
            
            
            for nombre_act,nombre_est in zip(SuperDiccionario["TEFinal"]["Variacion"][AGENTES][CDELTA][ALFA],SuperDiccionario["Erdos-Renyi"]["Opiniones"][N][12][CDELTA][ALFA][0:11]):
                
                plt.rcParams.update({'font.size': 24})
                plt.figure("VarProm",figsize=(20,15))
                
                # Levanto los datos de la red de actividad
                
                repeticion = int(nombre_act.split("_")[5].split("=")[1])
                
                # PARA LEVANTAR DATOS DE LA CARPETA TODA MEZCLADA
                Datos = ldata("./DilAct/TEFinal/{}".format(nombre_act))
                
                # Levanto los datos de Variacion Promedio
                Var = np.array([float(x) for x in Datos[1][1::]])
                
                # Defino los valores de X de mi gráfico.
                X = np.arange(len(Var))*0.01
                
                # Grafico la Variación Promedio de la red de Actividad
                plt.plot(X,Var, linewidth = 3)
                
                # Levanto los datos de la red estática
                
                # PARA LEVANTAR DATOS DE LA CARPETA TODA MEZCLADA
                Datos = ldata("./DRE/Erdos-Renyi/{}".format(nombre_est))
                
                # Levanto los datos de Variacion Promedio
                Var = np.array([float(x) for x in Datos[1][1::]])
                
                # Grafico la Variación Promedio de la red de Actividad
                plt.plot(X[0:len(Var)],Var,"--",linewidth = 4)
                
                #---------------------------------------------------------------
                
                # Agrego los toques finales
                
                plt.hlines(y = 0.0005, xmin = 0, xmax = 30, color = "red",linewidth = 2)
                plt.xlabel("Tiempo")
                plt.ylabel("Variación Promedio")
                plt.xticks(np.arange(0,31,2))
                plt.grid()
                plt.savefig("../Imagenes/RedAct/{}/VarProm_alfa={:.3f}_Cdelta={:.2f}_N={}_iter={}.png".format(Carpeta,ALFA,CDELTA,AGENTES,repeticion),bbox_inches = "tight")
                plt.close("VarProm")
                
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Acá me preparo el código para el tercer gráfico, lo hago todo desde cero para evitar dudas,
# Después simplemente comento lo de arriba cualquier cosa.
        
        
T=2 # Defino acá el número de tópicos porque es algo que no cambia por ahora,
# pero no tenía dónde más definirlo

SuperDiccionario = dict()

for Carpeta in ["TEFinal"]:

   # CÓDIGO PARA LEVANTAR ARCHIVOS DE UNA CARPETA CON TODOS LOS ARCHIVOS MEZCLADOS
    
    CarpCheck=[[root,files] for root,dirs,files in os.walk("./DilAct/{}".format(Carpeta))]
    
    # El elemento en la posición x[0] es el nombre de la carpeta
    
    for x in CarpCheck:
        Archivos_Datos = [nombre for nombre in x[1]]
        Archivos_Datos.insert(0,x[0])
        
    

    #-------------------------------------------------------------------------------------------------------
    
    # Es importante partir del hecho de que mis archivos llevan por nombre: "Datos_Adyacencia_alfa=$_Cdelta=$_N=$_Iter=$"
    # También tengo otros archivos llamados "Datos_Variacion_alfa=$_Cdelta=$_N=$_Iter=$" y
    # "Evolucion_Sistema_alfa=$_Cdelta=$_N=$_Iter=$".
    
    Conjunto_Direcciones = [Archivos_Datos[0]]
    
    SuperDiccionario[Carpeta] = dict()
    
    for nombre in Archivos_Datos[1:len(Archivos_Datos)]:
        tipo = nombre.split("_")[1]
        alfa = float(nombre.split("_")[2].split("=")[1])
        Cdelta = float(nombre.split("_")[3].split("=")[1])
        N = int(nombre.split("_")[4].split("=")[1])
        if tipo not in SuperDiccionario[Carpeta].keys():
            SuperDiccionario[Carpeta][tipo] = dict()
            SuperDiccionario[Carpeta][tipo][N] = dict()
            SuperDiccionario[Carpeta][tipo][N][Cdelta] = dict()
            SuperDiccionario[Carpeta][tipo][N][Cdelta][alfa] = [nombre]
        elif N not in SuperDiccionario[Carpeta][tipo].keys():
            SuperDiccionario[Carpeta][tipo][N] = dict()
            SuperDiccionario[Carpeta][tipo][N][Cdelta] = dict()
            SuperDiccionario[Carpeta][tipo][N][Cdelta][alfa] = [nombre]
        elif Cdelta not in SuperDiccionario[Carpeta][tipo][N].keys():
            SuperDiccionario[Carpeta][tipo][N][Cdelta] = dict()
            SuperDiccionario[Carpeta][tipo][N][Cdelta][alfa] = [nombre]
        elif alfa not in SuperDiccionario[Carpeta][tipo][N][Cdelta].keys():
            SuperDiccionario[Carpeta][tipo][N][Cdelta][alfa] = [nombre]
        else:
            SuperDiccionario[Carpeta][tipo][N][Cdelta][alfa].append(nombre)
    
    # Le hice una modificación a esta parte del código, ahora esto trabaja
    # armando el SuperDiccionario también, no sólo los Conjuntos de Alfa, Cdelta
    # y demás. Lo bueno de esto es que ahora el armado del SuperDiccionario
    # es mucho más rápido.
    
    # En este caso SuperDiccionario está juntando tanto los nombres
    # de Datos Testisgos con los de Datos Opiniones.
    #--------------------------------------------------------------------------------------------
    
    # Arranquemos con el primer gráfico. Quiero graficar las opiniones respecto del tópico 1
    # de los 10 agentes más activos y de los 10 agentes menos activos. Para eso voy a tomar datos
    # de los archivos de Evolucion_Sistema. Esos tienen en la primer fila las actividades
    # de los agentes y después tienen las opiniones de los agentes en cada iteración.
    
    for AGENTES in [1000]:
        
        #---------------------------------------------------------------------------------------------------------------
        
        TIPO = "Adyacencia"
        
        # Acá me voy a inicializar los arrays para graficar los mapas de colores de la red.
        
        
        # Defino el conjunto de valores de Cdelta a recorrer. Tengo que ordenarlos porque
        # el SuperDiccionario los ordena como los recibe, y el os.walk no necesariamente recorre
        # todo en orden.
        
        Conjunto_Cdelta = list(SuperDiccionario[Carpeta][TIPO][AGENTES].keys())
        Conjunto_Cdelta.sort()
        
        #----------------------------------------------------------------------------------------------------------
        
        for CDELTA,icdelta in zip(Conjunto_Cdelta,np.arange(len(Conjunto_Cdelta))):
            
            # Para cada Cdelta defino el conjunto de Alfas asociados a recorrer.
            # De nuevo, lo ordeno porque el SuperDiccionario no los tiene necesariamente ordenados.
            
            Conjunto_Alfa = list(SuperDiccionario[Carpeta][TIPO][AGENTES][CDELTA].keys())
            Conjunto_Alfa.sort()
            
            
            for ALFA,ialfa in zip(Conjunto_Alfa,np.arange(len(Conjunto_Alfa))):
                
                for nombre_ady,nombre_sist in zip(SuperDiccionario[Carpeta]["Adyacencia"][AGENTES][CDELTA][ALFA][0:2],SuperDiccionario[Carpeta]["Sistema"][AGENTES][CDELTA][ALFA][0:2]):
                    
                    # Acá levanto los datos de los archivos de Datos_Adyacencia. Estos archivos tienen los siguientes datos:
                    # Matrices de Adyacencia en cada iteracion

                    #--------------------------------------------------------------------------------------------
                
                    # Levanto los datos del archivo original y separo los datos en tres listas.
                    # Una para la matriz de Adyacencia, una para la matriz de superposición y una para los vectores de opiniones
                
                    repeticion = int(nombre_ady.split("_")[5].split("=")[1])
                    
                    
                    # Tengo que hacer una diferenciación entre levantar datos de las carpetas subdividida en 4 y de la carpeta con todo mezclado.

                    # PARA LEVANTAR DATOS DE LA CARPETA TODA MEZCLADA
                    Datos = ldata("{}/{}".format(Conjunto_Direcciones[0],nombre_ady))
                    
                    # Levanto los datos de las Opiniones Finales
                    Ady = np.zeros((len(Datos)-2,len(Datos[1])-1))
                    for fila,i in zip(Datos[1:len(Datos)],np.arange(len(Datos)-2)):
                        Ady[i] = fila[1::]
                        
                    #--------------------------------------------------------------------------------------------
                    
                    # Hagamos acá la parte de levantar los datos de Opiniones. Con esos datos mi idea es colorear los nodos.
                    # Para colorearlos hagamos algo simple. La idea es, pintemos de verde los que tienen módulo de opinión
                    # menor a 1. Hagamos eso ahora, después cualquier cosa se retoca un poco.
                    
                    # PARA LEVANTAR DATOS DE LA CARPETA TODA MEZCLADA
                    Datos = ldata("{}/{}".format(Conjunto_Direcciones[0],nombre_sist))
                    
                    
                    # Levanto los datos de las Opiniones Finales
                    Opi = np.zeros((len(Datos)-5,len(Datos[3])-1))
                    for fila,i in zip(Datos[3:len(Datos)-2],np.arange(len(Datos[3:len(Datos)-2]))):
                        Opi[i] = fila[1::]
                    
                        
                    #--------------------------------------------------------------------------------------------
                    
                    # Primero me preocupo por armar los gráficos de las redes, después veré
                    # de agregar el tema de considerar las opiniones y su distancia al cero
                    # como un parámetro para colorear a los nodos. O quizás para definir su tamaño, ya veré
                    
                    # La cosa es que yo tengo la forma de la red en cada rearmado. Y tengo 30 rearmados, por
                    # cada simulación. Siendo que tengo 10 simulaciones para alfa 0 y 10 para alfa 0,5,
                    # entonces tengo un total de 600 gráficos para armar. Lo cual es una bestialidad.
                    # Yo diría de graficar cinco gráficos para dos iteraciones nomás de cada alfa.
                    # Eso me daría unos 20 gráficos, que ya bastante son. Los gráficos son de las
                    # redes construidas en tiempo 5,10,15,20 y 25.
                    
                    Filas = [5,10,15,20,25]
                    
                    for tiempo in Filas:
                        Matriz = Ady[tiempo].reshape((AGENTES,AGENTES))
                        # La siguiente línea toma la matriz de Adyacencia y me arma una lista con todas las tuplas
                        # de los enlaces de la red sin ningún repetido. La verdad, bastante orgulloso. Además,
                        # esto es mejor que esa locura de revisar uno por uno los valores de la matriz con dos
                        # for, eso sería super engorroso, confuso y además tomaría mucho más.
                        enlaces = [(i,j) for i in range(AGENTES) for j in np.arange(i,AGENTES)[Matriz[i][i::] > 0]]
                        
                        # Tengo que armar la lista de nodos
                        nodos = []
                        for n in range(AGENTES):
                            if np.linalg.norm(Opi[(tiempo+1)*100][n*2:(n+1)*2]) < 1:
                                nodos.append((n,{"color":"green"}))
                            else:
                                nodos.append((n,{"color":"blue"}))
                        
                        # Ahora armo el grafo.
                        
                        plt.rcParams.update({'font.size': 24})
                        plt.figure("GrafoTE",figsize=(20,15))
                        
                        G = nx.Graph()
                        G.add_nodes_from(nodos)
                        G.add_edges_from(enlaces)
                        nx.draw_spring(G,node_color = [color[1] for color in G.nodes.data("color")],linewidths=0.2,with_labels=False)
                        plt.savefig("../Imagenes/RedAct/{}/GrafoTE_alfa={:.3f}_Cdelta={:.2f}_iter={}_sim={}.png".format(Carpeta,ALFA,CDELTA,repeticion,tiempo),bbox_inches = "tight")
                        plt.close("GrafoTE")
                    
                    
#------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------                       
"""                 
# Acá me preparo el código para el cuarto gráfico, lo hago todo desde cero para evitar dudas,
# Después simplemente comento lo de arriba cualquier cosa.
        
        
T=2 # Defino acá el número de tópicos porque es algo que no cambia por ahora,
# pero no tenía dónde más definirlo

SuperDiccionario = dict()

for Carpeta in ["ConexaFinal"]:

   # CÓDIGO PARA LEVANTAR ARCHIVOS DE UNA CARPETA CON TODOS LOS ARCHIVOS MEZCLADOS
    
    CarpCheck=[[root,files] for root,dirs,files in os.walk("./DilAct/{}".format(Carpeta))]
    
    # El elemento en la posición x[0] es el nombre de la carpeta
    
    for x in CarpCheck:
        Archivos_Datos = [nombre for nombre in x[1]]
        Archivos_Datos.insert(0,x[0])
        
    

    #-------------------------------------------------------------------------------------------------------
    
    # Es importante partir del hecho de que mis archivos llevan por nombre: "Datos_Opiniones_alfa=$_Cdelta=$_N=$_Iter=$"
    
    Conjunto_Direcciones = [Archivos_Datos[0]]
    
    SuperDiccionario[Carpeta] = dict()
    
    for nombre in Archivos_Datos[1:len(Archivos_Datos)]:
        tipo = nombre.split("_")[1]
        alfa = float(nombre.split("_")[2].split("=")[1])
        Cdelta = float(nombre.split("_")[3].split("=")[1])
        N = int(nombre.split("_")[4].split("=")[1])
        if tipo not in SuperDiccionario[Carpeta].keys():
            SuperDiccionario[Carpeta][tipo] = dict()
            SuperDiccionario[Carpeta][tipo][N] = dict()
            SuperDiccionario[Carpeta][tipo][N][Cdelta] = dict()
            SuperDiccionario[Carpeta][tipo][N][Cdelta][alfa] = [nombre]
        elif N not in SuperDiccionario[Carpeta][tipo].keys():
            SuperDiccionario[Carpeta][tipo][N] = dict()
            SuperDiccionario[Carpeta][tipo][N][Cdelta] = dict()
            SuperDiccionario[Carpeta][tipo][N][Cdelta][alfa] = [nombre]
        elif Cdelta not in SuperDiccionario[Carpeta][tipo][N].keys():
            SuperDiccionario[Carpeta][tipo][N][Cdelta] = dict()
            SuperDiccionario[Carpeta][tipo][N][Cdelta][alfa] = [nombre]
        elif alfa not in SuperDiccionario[Carpeta][tipo][N][Cdelta].keys():
            SuperDiccionario[Carpeta][tipo][N][Cdelta][alfa] = [nombre]
        else:
            SuperDiccionario[Carpeta][tipo][N][Cdelta][alfa].append(nombre)
    
    # Le hice una modificación a esta parte del código, ahora esto trabaja
    # armando el SuperDiccionario también, no sólo los Conjuntos de Alfa, Cdelta
    # y demás. Lo bueno de esto es que ahora el armado del SuperDiccionario
    # es mucho más rápido.
    
    # En este caso SuperDiccionario está juntando tanto los nombres
    # de Datos Testisgos con los de Datos Opiniones.
    #--------------------------------------------------------------------------------------------
    
    # Arranquemos con el primer gráfico. Quiero graficar las opiniones respecto del tópico 1
    # de los 10 agentes más activos y de los 10 agentes menos activos. Para eso voy a tomar datos
    # de los archivos de Evolucion_Sistema. Esos tienen en la primer fila las actividades
    # de los agentes y después tienen las opiniones de los agentes en cada iteración.
    
    for AGENTES in [1000]:
        
        #---------------------------------------------------------------------------------------------------------------
        
        TIPO = "Opiniones"
        
        # Acá me voy a inicializar los arrays para graficar los mapas de colores de la red.
        
        
        # Defino el conjunto de valores de Cdelta a recorrer. Tengo que ordenarlos porque
        # el SuperDiccionario los ordena como los recibe, y el os.walk no necesariamente recorre
        # todo en orden.
        
        Conjunto_Cdelta = list(SuperDiccionario[Carpeta][TIPO][AGENTES].keys())
        Conjunto_Cdelta.sort()
        
        #----------------------------------------------------------------------------------------------------------
        
        for CDELTA,icdelta in zip(Conjunto_Cdelta,np.arange(len(Conjunto_Cdelta))):
            
            # Para cada Cdelta defino el conjunto de Alfas asociados a recorrer.
            # De nuevo, lo ordeno porque el SuperDiccionario no los tiene necesariamente ordenados.
            
            Conjunto_Alfa = list(SuperDiccionario[Carpeta][TIPO][AGENTES][CDELTA].keys())
            Conjunto_Alfa.sort()
            
            
            for ALFA,ialfa in zip(Conjunto_Alfa,np.arange(len(Conjunto_Alfa))):
                
                for nombre in SuperDiccionario[Carpeta][TIPO][AGENTES][CDELTA][ALFA]:
                    
                    # Acá levanto los datos de los archivos de Datos_Adyacencia. Estos archivos tienen los siguientes datos:
                    # Opiniones
                    # Adyacencia

                    #--------------------------------------------------------------------------------------------
                
                    # Levanto los datos del archivo original y separo los datos en tres listas.
                    # Una para la matriz de Adyacencia, una para la matriz de superposición y una para los vectores de opiniones
                
                    repeticion = int(nombre.split("_")[5].split("=")[1])
                    
                    
                    # Tengo que hacer una diferenciación entre levantar datos de las carpetas subdividida en 4 y de la carpeta con todo mezclado.

                    # PARA LEVANTAR DATOS DE LA CARPETA TODA MEZCLADA
                    Datos = ldata("{}/{}".format(Conjunto_Direcciones[0],nombre))
                    
                    # Levanto los datos de las Opiniones Finales
                    Opi = np.array([float(x) for x in Datos[1][1::]])
                    
                    # Levanto los datos de la matriz de Adyacencia
                    Ady = np.array([float(x) for x in Datos[3][1::]])
                    Matriz = Ady.reshape((AGENTES,AGENTES))
                    
                    #--------------------------------------------------------------------------------------------
                    
                    
                    # La siguiente línea toma la matriz de Adyacencia y me arma una lista con todas las tuplas
                    # de los enlaces de la red sin ningún repetido. La verdad, bastante orgulloso. Además,
                    # esto es mejor que esa locura de revisar uno por uno los valores de la matriz con dos
                    # for, eso sería super engorroso, confuso y además tomaría mucho más.
                    enlaces = [(i,j) for i in range(AGENTES) for j in np.arange(i,AGENTES)[Matriz[i][i::] > 0]]
                    
                    # Clasifico a los nodos en cuadrantes
                    clasificacion = ClasificacionCuadrantes(Opi)
                    
                    # Armo la lista de nodos y les asigno colores
                    nodos = [(n,{"color":col}) for i,col in zip([0,1,2,3,4],["green","blue","red","magenta","orange"]) for n in np.arange(AGENTES)[clasificacion == i]]

                    # Ahora armo el grafo.
                    
                    plt.rcParams.update({'font.size': 24})
                    plt.figure("GrafoConexo",figsize=(20,15))
                    
                    G = nx.Graph()
                    G.add_nodes_from(nodos)
                    G.add_edges_from(enlaces)
                    nx.draw_spring(G, node_color = [color[1] for color in G.nodes.data("color")],linewidths=0.2,with_labels=False)
                    plt.savefig("../Imagenes/RedAct/{}/GrafoTE_alfa={:.3f}_Cdelta={:.2f}_iter={}.png".format(Carpeta,ALFA,CDELTA,repeticion),bbox_inches = "tight")
                    plt.close("GrafoConexo")
                    
                    #----------------------------------------------------------------------------------------------
                    
                    # Ahora hagamos el gráfico siguiendo partición de Louvain. Veamos qué da tanto en el caso
                    # de alfa = 0 y en el de alfa = 0,5.
                    
                    # La siguiente línea toma la matriz de Adyacencia y me arma una lista con todas las tuplas
                    # de los enlaces de la red sin ningún repetido. La verdad, bastante orgulloso. Además,
                    # esto es mejor que esa locura de revisar uno por uno los valores de la matriz con dos
                    # for, eso sería super engorroso, confuso y además tomaría mucho más.
                    enlaces = [(i,j) for i in range(AGENTES) for j in np.arange(i,AGENTES)[Matriz[i][i::] > 0]]
                    
                    # Preparo la lista de nodos
                    nodos = np.arange(AGENTES)
                    
                    # Ahora armo el grafo.
                    
                    G = nx.Graph()
                    G.add_nodes_from(nodos)
                    G.add_edges_from(enlaces)
                    
                    # Aplico el método de Louvain para detectar comunidades.
                    particion = community_louvain.best_partition(G)
                    
                    # A partir de acá copio la forma de armar el gráfico de algo que vi en internet, para poder
                    # pintar correctamente las comunidades.
                    # Esto de pos es para que queden graficados usando el algoritmo de spring. Aunque eso se puede resolver
                    # simplemente usando nx.draw_spring
#                    pos = nx.spring_layout(G)
                    
                    # Armo mi colormap a seguir para poder colocar todos mis nodos
                    cmap = cm.get_cmap('viridis', max(particion.values()) + 1)
                    
                    # Abro el gráfico
                    plt.rcParams.update({'font.size': 24})
                    plt.figure("GrafoConexo",figsize=(20,15))
                    
                    # Coloco mis nodos y mis enlaces
#                    nx.draw_networkx_nodes(G, pos, particion.keys(), node_size=120,cmap=cmap, node_color=list(particion.values()))
#                    nx.draw_networkx_edges(G, pos, linewidths = 0.2)
                    nx.draw_spring(G,cmap = cmap,node_color = list(particion.values()) ,linewidths=0.2,with_labels=False)
                    plt.savefig("../Imagenes/RedAct/{}/GrafoTELouvain_alfa={:.3f}_Cdelta={:.2f}_iter={}.png".format(Carpeta,ALFA,CDELTA,repeticion),bbox_inches = "tight")
                    plt.close("GrafoConexo")
                    
                    
"""
#------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------                       
                    
# Acá me preparo el código para el quinto gráfico, lo hago todo desde cero para evitar dudas,
# Después simplemente comento lo de arriba cualquier cosa.
        
        
T=2 # Defino acá el número de tópicos porque es algo que no cambia por ahora,
# pero no tenía dónde más definirlo

SuperDiccionario = dict()

for Carpeta in ["DinaReg"]:

   # CÓDIGO PARA LEVANTAR ARCHIVOS DE UNA CARPETA CON TODOS LOS ARCHIVOS MEZCLADOS
    
    CarpCheck=[[root,files] for root,dirs,files in os.walk("./DilAct/{}".format(Carpeta))]
    
    # El elemento en la posición x[0] es el nombre de la carpeta
    
    for x in CarpCheck:
        Archivos_Datos = [nombre for nombre in x[1]]
        Archivos_Datos.insert(0,x[0])
        
    

    #-------------------------------------------------------------------------------------------------------
    
    # Es importante partir del hecho de que mis archivos llevan por nombre: "Evolucion_Sistema_alfa=$_Cdelta=$_N=$_Iter=$"
    
    Conjunto_Direcciones = [Archivos_Datos[0]]
    
    SuperDiccionario[Carpeta] = dict()
    
    for nombre in Archivos_Datos[1:len(Archivos_Datos)]:
        tipo = nombre.split("_")[1]
        alfa = float(nombre.split("_")[2].split("=")[1])
        Cdelta = float(nombre.split("_")[3].split("=")[1])
        N = int(nombre.split("_")[4].split("=")[1])
        if tipo not in SuperDiccionario[Carpeta].keys():
            SuperDiccionario[Carpeta][tipo] = dict()
            SuperDiccionario[Carpeta][tipo][N] = dict()
            SuperDiccionario[Carpeta][tipo][N][Cdelta] = dict()
            SuperDiccionario[Carpeta][tipo][N][Cdelta][alfa] = [nombre]
        elif N not in SuperDiccionario[Carpeta][tipo].keys():
            SuperDiccionario[Carpeta][tipo][N] = dict()
            SuperDiccionario[Carpeta][tipo][N][Cdelta] = dict()
            SuperDiccionario[Carpeta][tipo][N][Cdelta][alfa] = [nombre]
        elif Cdelta not in SuperDiccionario[Carpeta][tipo][N].keys():
            SuperDiccionario[Carpeta][tipo][N][Cdelta] = dict()
            SuperDiccionario[Carpeta][tipo][N][Cdelta][alfa] = [nombre]
        elif alfa not in SuperDiccionario[Carpeta][tipo][N][Cdelta].keys():
            SuperDiccionario[Carpeta][tipo][N][Cdelta][alfa] = [nombre]
        else:
            SuperDiccionario[Carpeta][tipo][N][Cdelta][alfa].append(nombre)
    
    # Le hice una modificación a esta parte del código, ahora esto trabaja
    # armando el SuperDiccionario también, no sólo los Conjuntos de Alfa, Cdelta
    # y demás. Lo bueno de esto es que ahora el armado del SuperDiccionario
    # es mucho más rápido.
    
    # En este caso SuperDiccionario está juntando tanto los nombres
    # de Datos Testisgos con los de Datos Opiniones.
    #--------------------------------------------------------------------------------------------
    
    # Arranquemos con el primer gráfico. Quiero graficar las opiniones respecto del tópico 1
    # de los 10 agentes más activos y de los 10 agentes menos activos. Para eso voy a tomar datos
    # de los archivos de Evolucion_Sistema. Esos tienen en la primer fila las actividades
    # de los agentes y después tienen las opiniones de los agentes en cada iteración.
    
    for AGENTES in [1000]:
        
        #---------------------------------------------------------------------------------------------------------------
        
        TIPO = "Sistema"
        
        # Acá me voy a inicializar los arrays para graficar los mapas de colores de la red.
        
        
        # Defino el conjunto de valores de Cdelta a recorrer. Tengo que ordenarlos porque
        # el SuperDiccionario los ordena como los recibe, y el os.walk no necesariamente recorre
        # todo en orden.
        
        Conjunto_Cdelta = list(SuperDiccionario[Carpeta][TIPO][AGENTES].keys())
        Conjunto_Cdelta.sort()
        
        #----------------------------------------------------------------------------------------------------------
        
        for CDELTA,icdelta in zip(Conjunto_Cdelta,np.arange(len(Conjunto_Cdelta))):
            
            # Para cada Cdelta defino el conjunto de Alfas asociados a recorrer.
            # De nuevo, lo ordeno porque el SuperDiccionario no los tiene necesariamente ordenados.
            
            Conjunto_Alfa = list(SuperDiccionario[Carpeta][TIPO][AGENTES][CDELTA].keys())
            Conjunto_Alfa.sort()
            
            
            for ALFA,ialfa in zip(Conjunto_Alfa,np.arange(len(Conjunto_Alfa))):
                
                for nombre in SuperDiccionario[Carpeta][TIPO][AGENTES][CDELTA][ALFA]:
                    
                    # Acá levanto los datos de los archivos de Datos_Adyacencia. Estos archivos tienen los siguientes datos:
                    # Opiniones

                    #--------------------------------------------------------------------------------------------
                
                    # Levanto los datos del archivo original y separo los datos en tres listas.
                    # Una para la matriz de Adyacencia, una para la matriz de superposición y una para los vectores de opiniones
                
                    repeticion = int(nombre.split("_")[5].split("=")[1])
                    
                    
                    # Tengo que hacer una diferenciación entre levantar datos de las carpetas subdividida en 4 y de la carpeta con todo mezclado.

                    # PARA LEVANTAR DATOS DE LA CARPETA TODA MEZCLADA
                    Datos = ldata("{}/{}".format(Conjunto_Direcciones[0],nombre))
                    
                    # Levanto los datos de las Opiniones
                    ArrayOpi = np.zeros((len(Datos)-3,len(Datos[1])-1))
                    for fila,i in zip(Datos[1:len(Datos)-2],np.arange(len(Datos[1:len(Datos)-2]))):
                        ArrayOpi[i] = fila[1::]
                        
                    #----------------------------------------------------------------------------------------------
                    
                    # Abro los gráficos que quiero armar
                    
                    # Abro el gráfico de los Tópicos vs Tiempo 
                    
                    plt.rcParams.update({'font.size': 24})
                    plt.figure("Topico",figsize=(20,15))
                    plt.xlabel("Tiempo")
                    plt.ylabel(r"$x^1$")
#                    plt.ylim(-OpiMaxima,OpiMaxima)
                    plt.grid()

                    # Creo que no necesito las OpiMaxima
                    
                    #----------------------------------------------------------------
                    
                    # Ahora yo voy a querer armar dos gráficos. Uno el que dijo Pablo de la
                    # TdO si no me equivoco. El otro el gráfico de la convergencia de Opiniones
                    # que estuve viendo en los archivos de Actividades
                    
                    # Como ahora tengo los datos del sistema, voy a graficar muchos agentes.
                    # Voy a hacerlo con lineas bien finas y transparentadas
                                                        
                    plt.figure("Topico")
                    
                    X = np.arange(ArrayOpi.shape[0])*0.01
                    for sujeto in range(200):
                        plt.plot(X,ArrayOpi[:,sujeto*4], color="gray", linewidth = 1, alpha = 0.5)

                    #-----------------------------------------------------------------------------
                
                    # Para graficar los Promedios, voy a hacer gráficos de promedios por
                    # rama. Ahora, los casos son distintos para Polarización en general y
                    # Consenso. Así que voy a hacer una separación según el alfa
                    
                    if ALFA == 0:
                        # En este caso puedo tomar un único Promedio y listo
                        
                        Promedios = np.zeros(ArrayOpi.shape[0])
                        for indice in range(ArrayOpi.shape[0]):
                            Promedios[indice] = np.mean(ArrayOpi[indice][0::2]) # La cosa es promediar sólo la opinión del tópico 0
                            
                        X = np.arange(ArrayOpi.shape[0])*0.01
                        plt.plot(X,Promedios, color="green", linewidth = 5)
                        
                    else:
                        # Ahora tengo que armar el caso de Polarizacion
                        
                        # Establezco unos datos iniciales
                        colores = ["green","blue","red","magenta","orange"]
                        X = np.arange(ArrayOpi.shape[0])*0.01
                        
                        # Clasifico los agentes en cuadrantes según sus opiniones finales y después me armo una
                        # lista de los cuadrantes observados. Esto es importante porque en descorrelacionada veo
                        # 4 cuadrantes, mientras que en ideológico veo sólo 2. Quiero evitar los errores de intentar
                        # graficar un array de promedios vacío
                        clasificacion = ClasificacionCuadrantes(ArrayOpi[ArrayOpi.shape[0]-1])
                        cuadrantes = [int(n) for n in set(clasificacion)]
                        
                        # Voy a armar promedios para cada rama ignorando los que van al consenso
                        for n in cuadrantes:
                            if n != 0:
                                Promedios = np.zeros(ArrayOpi.shape[0])
                                for indice in range(ArrayOpi.shape[0]):
                                    Promedios[indice] = np.mean(ArrayOpi[indice][0::2][clasificacion == n]) # La cosa es promediar sólo la opinión del tópico 0 de los sujetos de cada rama
                                plt.plot(X,Promedios, color=colores[n], linewidth = 6)
                    
                    # Acá debería hacer el otro gráfico, el que me propuso Pablo. Para esto tengo que hacer los viejos y clásicos
                    # TdO si no me equivoco. Eso no debería tardar mucho.
                    
                    #------------------------------------------------------------------------------------------------------------------------
                        
                    # Cierro el gráfico
        
                    plt.savefig("../Imagenes/RedAct/ConexaFinal/Topicos_alfa={:.3f}_Cdelta={:.2f}_iter={}.png".format(ALFA,CDELTA,repeticion),bbox_inches = "tight")
                    plt.close("Topico")
                    
                    
                    #------------------------------------------------------------------------------------------------------------------------
                    
                    # Abro el gráfico de las TdO
                    
                    plt.rcParams.update({'font.size': 24})
                    plt.figure("Trayectoria Opiniones",figsize=(20,15))
                    plt.xlabel(r"$x^1$")
                    plt.ylabel(r"$x^2$")
                    
                    #-------------------------------------------------------------------------------------------------------
                    
                    # Grafico las trayectorias de los sujetos. Grafico todos los sujetos con lineas
                    # bien finas y transparentadas.
                    
                    
                    for sujeto in range(AGENTES):
                        plt.plot(ArrayOpi[:,0+2*sujeto],ArrayOpi[:,1+2*sujeto], color="gray",linewidth = 1.5, alpha=0.5)
    
    
                    #--------------------------------------------------------------------------------------------------------
                    
                    # Acá armo los promedios para cada rama. Para eso, como ahora estoy en el espacio de tópicos,
                    # necesito tomar promedios de ambos tópicos, no de uno solo
                    
                    if ALFA == 0:
                        # En este caso simplemente tomo promedio de todo y fue
                        
                        Promedios0 = np.zeros(ArrayOpi.shape[0])
                        Promedios1 = np.zeros(ArrayOpi.shape[0])
                        
                        for indice in range(ArrayOpi.shape[0]):
                            Promedios0[indice] = np.mean(ArrayOpi[indice][0::2]) # Acá tomo el promedio de las opiniones en el tópico 0
                            Promedios1[indice] = np.mean(ArrayOpi[indice][1::2]) # Acá tomo el promedio de las opiniones en el tópico 1
                            
                        X = np.arange(ArrayOpi.shape[0])*0.01
                        plt.plot(Promedios0,Promedios1, color="green",linewidth = 5)
                        
                    else:
                        # Ahora tengo que armar el caso de Polarizacion, tomando promedios de cada una de las ramas.
                        
                        # Establezco unos datos iniciales
                        colores = ["green","blue","red","magenta","orange"]
                        X = np.arange(ArrayOpi.shape[0])*0.01
                        
                        # Establezo el tamaño del gráfico y lo centro
                        plt.ylim(-100,100)
                        plt.xlim(-100,100)
                        
                        # Clasifico los agentes en cuadrantes según sus opiniones finales y después me armo una
                        # lista de los cuadrantes observados. Esto es importante porque en descorrelacionada veo
                        # 4 cuadrantes, mientras que en ideológico veo sólo 2. Quiero evitar los errores de intentar
                        # graficar un array de promedios vacío
                        clasificacion = ClasificacionCuadrantes(ArrayOpi[ArrayOpi.shape[0]-1])
                        cuadrantes = [int(n) for n in set(clasificacion)]
                        
                        # Voy a armar promedios para cada rama ignorando los que van al consenso
                        for n in cuadrantes:
                            if n != 0:
                                Promedios0 = np.zeros(ArrayOpi.shape[0])
                                Promedios1 = np.zeros(ArrayOpi.shape[0])
                                
                                for indice in range(ArrayOpi.shape[0]):
                                    Promedios0[indice] = np.mean(ArrayOpi[indice][0::2][clasificacion == n]) # La cosa es promediar sólo la opinión del tópico 0 de los sujetos de cada rama
                                    Promedios1[indice] = np.mean(ArrayOpi[indice][1::2][clasificacion == n]) # La cosa es promediar sólo la opinión del tópico 1 de los sujetos de cada rama
                                plt.plot(Promedios0,Promedios1, color=colores[n],linewidth = 6)
                                
                    #-------------------------------------------------------------------------------------------------------------------------------------------------------------------
                    
                    # Cierro el gráfico
                    
                    
                    plt.savefig("../Imagenes/RedAct/ConexaFinal/TdO_alfa={:.3f}_Cdelta={:.2f}_iter={}.png".format(ALFA,CDELTA,repeticion),bbox_inches = "tight")
                    plt.close("Trayectoria Opiniones")

                   
#------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------                       
                    
# Acá me preparo el código para el sexto gráfico, lo hago todo desde cero para evitar dudas,
# Después simplemente comento lo de arriba cualquier cosa.
        
        
T=2 # Defino acá el número de tópicos porque es algo que no cambia por ahora,
# pero no tenía dónde más definirlo

SuperDiccionario = dict()

for Carpeta in ["TiempoExtra"]:

   # CÓDIGO PARA LEVANTAR ARCHIVOS DE UNA CARPETA CON TODOS LOS ARCHIVOS MEZCLADOS
    
    CarpCheck=[[root,files] for root,dirs,files in os.walk("./DilAct/{}".format(Carpeta))]
    
    # El elemento en la posición x[0] es el nombre de la carpeta
    
    for x in CarpCheck:
        Archivos_Datos = [nombre for nombre in x[1]]
        Archivos_Datos.insert(0,x[0])
        
    

    #-------------------------------------------------------------------------------------------------------
    
    # Es importante partir del hecho de que mis archivos llevan por nombre: "Evolucion_Sistema_alfa=$_Cdelta=$_N=$_Iter=$"
    
    Conjunto_Direcciones = [Archivos_Datos[0]]
    
    SuperDiccionario[Carpeta] = dict()
    
    for nombre in Archivos_Datos[1:len(Archivos_Datos)]:
        tipo = nombre.split("_")[1]
        alfa = float(nombre.split("_")[2].split("=")[1])
        Cdelta = float(nombre.split("_")[3].split("=")[1])
        N = int(nombre.split("_")[4].split("=")[1])
        if tipo not in SuperDiccionario[Carpeta].keys():
            SuperDiccionario[Carpeta][tipo] = dict()
            SuperDiccionario[Carpeta][tipo][N] = dict()
            SuperDiccionario[Carpeta][tipo][N][Cdelta] = dict()
            SuperDiccionario[Carpeta][tipo][N][Cdelta][alfa] = [nombre]
        elif N not in SuperDiccionario[Carpeta][tipo].keys():
            SuperDiccionario[Carpeta][tipo][N] = dict()
            SuperDiccionario[Carpeta][tipo][N][Cdelta] = dict()
            SuperDiccionario[Carpeta][tipo][N][Cdelta][alfa] = [nombre]
        elif Cdelta not in SuperDiccionario[Carpeta][tipo][N].keys():
            SuperDiccionario[Carpeta][tipo][N][Cdelta] = dict()
            SuperDiccionario[Carpeta][tipo][N][Cdelta][alfa] = [nombre]
        elif alfa not in SuperDiccionario[Carpeta][tipo][N][Cdelta].keys():
            SuperDiccionario[Carpeta][tipo][N][Cdelta][alfa] = [nombre]
        else:
            SuperDiccionario[Carpeta][tipo][N][Cdelta][alfa].append(nombre)
    
    # Le hice una modificación a esta parte del código, ahora esto trabaja
    # armando el SuperDiccionario también, no sólo los Conjuntos de Alfa, Cdelta
    # y demás. Lo bueno de esto es que ahora el armado del SuperDiccionario
    # es mucho más rápido.
    
    # En este caso SuperDiccionario está juntando tanto los nombres
    # de Datos Testisgos con los de Datos Opiniones.
    #--------------------------------------------------------------------------------------------
    
    # Arranquemos con el primer gráfico. Quiero graficar las opiniones respecto del tópico 1
    # de los 10 agentes más activos y de los 10 agentes menos activos. Para eso voy a tomar datos
    # de los archivos de Evolucion_Sistema. Esos tienen en la primer fila las actividades
    # de los agentes y después tienen las opiniones de los agentes en cada iteración.
    
    for AGENTES in [1000]:
        
        #---------------------------------------------------------------------------------------------------------------
        
        TIPO = "Opiniones"
        
        # Acá me voy a inicializar los arrays para graficar los mapas de colores de la red.
        
        
        # Defino el conjunto de valores de Cdelta a recorrer. Tengo que ordenarlos porque
        # el SuperDiccionario los ordena como los recibe, y el os.walk no necesariamente recorre
        # todo en orden.
        
        Conjunto_Cdelta = list(SuperDiccionario[Carpeta][TIPO][AGENTES].keys())
        Conjunto_Cdelta.sort()
        
        #----------------------------------------------------------------------------------------------------------
        
        for CDELTA,icdelta in zip(Conjunto_Cdelta,np.arange(len(Conjunto_Cdelta))):
        
    
            # Defino los alfas que voy a usar en el gráfico de Distribución de Opiniones
            
            plt.rcParams.update({'font.size': 24})
            
            fig = plt.figure("Distribucion Opiniones",figsize=(64,36))
            
            gs = fig.add_gridspec(4,4, hspace = 0, wspace = 0)
            axs = gs.subplots(sharex=True,sharey=True)
            
            # Alfas_Dist = [Conjunto_Alfa[int(indice*math.floor(len(Conjunto_Alfa)/16))] for indice in range(0,16)]
            
            Columnas = [0,1,2,3]*4
            Filas = [i for i in range(0,4) for j in range(0,4)]
    
            Conjunto_Alfa = list(SuperDiccionario[Carpeta][TIPO][AGENTES][CDELTA].keys())
            Conjunto_Alfa.sort()

            # Reinicio la OpiMaxima a 0
            OpiMaxima = 0
            
            for ALFA in Conjunto_Alfa[0:30]:
                
                for nombre,numero in zip(SuperDiccionario[Carpeta][TIPO][AGENTES][CDELTA][ALFA],np.arange(len(SuperDiccionario[Carpeta][TIPO][AGENTES][CDELTA][ALFA]))):
                
                    #----------------------------------------------------------------------------------------------------------------------------------
                    # Acá levanto los datos de los archivos de opiniones. Estos archivos tienen los siguientes datos:
                    # Opinión Inicial del sistema
                    # Variación Promedio
                    # Opinión Final
                    # Grado de Agentes
                    # Actividad de Agentes
                    # Semilla
                        
                    Datos = ldata("{}/{}".format(Conjunto_Direcciones[0],nombre))
                    
                    # Levanto los datos de la Variación Promedio
                    Opi = np.array([float(x) for x in Datos[5][1::]])
                
                    #-----------------------------------------------------------------------------------------------
                        
                    # Acá voy armando el cálculo de la OpiMáxima
                    
                    OpiMaxima = max(max(Opi),OpiMaxima)
                    
                    #-----------------------------------------------------------------------------------------------
"""
"""
            
            for ALFA,fila,columna in zip(Conjunto_Alfa[0:16],Filas,Columnas):
                
                OpinionesFinales = np.array([])
    
                #-------------------------------------------------------------------------------------
                for nombre in SuperDiccionario[Carpeta][TIPO][AGENTES][CDELTA][ALFA]:
                    
                    #----------------------------------------------------------------------------------------------------------------------------------
                    # Acá levanto los datos de los archivos de opiniones. Estos archivos tienen los siguientes datos:
                    # Opinión Inicial del sistema
                    # Variación Promedio
                    # Opinión Final
                    # Semilla
                    # Testigos
                    
                    Datos = ldata("{}/{}".format(Conjunto_Direcciones[0],nombre))
                    
                    # Levanto los datos de la Variación Promedio
                    Opi = np.array([float(x) for x in Datos[5][1::]])
                    
                    # Me voy armando un array con las opiniones finales de los agentes a lo largo
                    # de todas las simulaciones
                    
                    OpinionesFinales = np.concatenate((OpinionesFinales,Opi),axis=None)
                    
                    
                        
            # -------------------------------------------------------------------------------------------------
                
                # Acá voy a armar los gráficos de las proyecciones de las opiniones de los agentes. Para eso simplemente
                # voy a tomar los valores de opiniones de los agentes de una simulación, calcularle el histograma
                # con np.histogram y luego graficar eso como líneas.
                
                OpiMaxima = max(np.absolute(OpinionesFinales))
#                Bordes = np.round(np.linspace(-OpiMaxima,OpiMaxima,22),5)
                Bordes = np.round(np.linspace(-20,20,40),3)
                Bins = (Bordes[1::]+Bordes[0:len(Bordes)-1])/2
                
                Histo,nada = np.histogram(OpinionesFinales,bins=Bordes)
                
                ResultadoEF = EstadoFinal(OpinionesFinales,Histo,Bins)
                # if ALFA == 0:
                #     print("Los valores del histograma de alfa=0 son:")
                #     print(Histo)
                
                # Armo los histogramas correspondientes
                Histo,nada = np.histogram(OpinionesFinales,bins=Bordes,density=True)
                
                # Defino el tema de los colores
                if ResultadoEF == "Consenso":
                    color = "green"
                elif ResultadoEF == "Polarizacion":
                    color = "blue"
                elif ResultadoEF == "Ideologico":
                    color = "red"
                elif ResultadoEF == "RegionTrans":
                    color = "purple"
                
                
                # Ahora grafico las curvas de distribución de ambas opiniones
                axs[fila,columna].plot(Bins,Histo,"-o",color = color,linewidth = 4,markersize = 8, label="Alfa = {}".format(ALFA))
                axs[fila,columna].legend()
                axs[fila,columna].grid()
            
            plt.savefig("../Imagenes/RedAct/TEFinal/Distribucion_opiniones_Cdelta={:.2f}.png".format(CDELTA),bbox_inches = "tight")
    #                plt.show()
            plt.close("Distribucion Opiniones")
"""
      
Tiempo()
