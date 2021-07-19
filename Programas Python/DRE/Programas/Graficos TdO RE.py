# -*- coding: utf-8 -*-
"""
Created on Sun May 16 19:15:15 2021

@author: Favio
"""

# La idea de este archivo es recopilar TODO el trabajo realizado en los archivos
# Graficador ER2, Caracterización Transición y TablaTdO. Admito que no estoy seguro
# de que sea una gran idea, porque al final del día es MUCHAS cuentas, y si están
# todas en un solo archivo no voy a poder frenar el archivo. Me encargaré de armar
# este código de forma de separar de forma muy clara las partes de cada archivo
# cosa que se pueda comentar fácilmente qué cosas hacer y qué cosas no.

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
    K = 1 # Influencia social
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

def EstadoFinal(Array):
    
    Topicos = 2    
    # Primero veo el caso de que hayan tendido a cero
    
    ArrayAbs = np.absolute(Array)
    CantP = np.count_nonzero(ArrayAbs > 0.5)
    if CantP/len(Array) < 0.5:
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

T=2 # Defino acá el número de tópicos porque es algo que no cambia por ahora,
# pero no tenía dónde más definirlo

SuperDiccionario = dict()

for REDES in ["Erdos-Renyi"]: # ["Barabasi"]: # ["Random Regulars"]:


    # Primero levanto datos de la carpeta de la red REDES
    
    CarpCheck=[[root,files] for root,dirs,files in os.walk("../{}".format(REDES))]
    
    # El elemento en la posición x[0] es el nombre de la carpeta
    
    for x in CarpCheck:
        # dada = x[0].split("\\")
        Archivos_Datos = [nombre for nombre in x[1]]
        Archivos_Datos.insert(0,x[0])
    
    # Con esto tengo los nombres de todos los archivos en la carpeta de Datos de Barabasi
    # Archivos_Datos tiene en la primer coordenada el principio de la dirección
    # de la carpeta, y el resto de elementos son los archivos en la carpeta.
    
    #---------------------------------------------------------------------------------------------
    
    # Es importante partir del hecho de que mis archivos llevan por nombre: "Datos_Opiniones_alfa=$_Cdelta=$_N=$_Gm=$_ID=$_Iter=$"
    
    Conjunto_Alfa = []
    Conjunto_Cdelta = []
    Conjunto_N = []
    Conjunto_Gm = []
    
    for nombre in Archivos_Datos[1:len(Archivos_Datos)]:
        alfa = float(nombre.split("_")[2].split("=")[1])
        Cdelta = float(nombre.split("_")[3].split("=")[1])
        N = int(nombre.split("_")[4].split("=")[1])
        Gm = int(nombre.split("_")[5].split("=")[1])
        if alfa not in Conjunto_Alfa:
            Conjunto_Alfa.append(alfa)
        if Cdelta not in Conjunto_Cdelta:
            Conjunto_Cdelta.append(Cdelta)
        if N not in Conjunto_N:
            Conjunto_N.append(N)
        if Gm not in Conjunto_Gm:
            Conjunto_Gm.append(Gm)
    
    Conjunto_Alfa.sort()
    Conjunto_Cdelta.sort()
    Conjunto_N.sort()
    Conjunto_Gm.sort()
    
    # Bien, esto ya me arma el conjunto de Alfas, Cdelta, N y Gm correctamente y ordenados
    # Ahora podemos pasar a lo importante de esta celda
    
    #--------------------------------------------------------------------------------------------
    
    # Voy a armar un diccionario que contenga las listas de los nombres de los archivos asociados
    # a un cierto N, Alfa, Cdelta y Gm. Me armo primero el superdiccionario, que es el diccionario,
    # que contiene diccionarios, que llevan a diccionarios que lleva a diccionarios
    # que lleva a diccionarios que llevan a las listas de los nombres
    # de los archivos, donde los ingresos a los diccionarios son el número de Agentes, el Alfa,
    # el Cdelta, el tipo de red y el Gm respectivos. 
    # Entonces la lista se accede sabiendo el Alfa, Cdelta y N correspondiente de antemano.
    
    SuperDiccionario[REDES] = dict()
    
    for AGENTES in Conjunto_N:
        SuperDiccionario[REDES][AGENTES] = dict()
        for ALFA in Conjunto_Alfa:
            for CDELTA in Conjunto_Cdelta:
                for GM in Conjunto_Gm:
                    for nombre in Archivos_Datos[1:len(Archivos_Datos)]:
                        alfa = float(nombre.split("_")[2].split("=")[1])
                        Cdelta = float(nombre.split("_")[3].split("=")[1])
                        N = int(nombre.split("_")[4].split("=")[1])
                        gm = int(nombre.split("_")[5].split("=")[1])
                        if N==AGENTES and alfa==ALFA and Cdelta==CDELTA and gm==GM:
                            if gm not in SuperDiccionario[REDES][AGENTES].keys():
                                SuperDiccionario[REDES][AGENTES][GM] = dict()
                            if alfa not in SuperDiccionario[REDES][AGENTES][GM].keys():
                                SuperDiccionario[REDES][AGENTES][GM][ALFA] = dict()
                            if Cdelta not in SuperDiccionario[REDES][AGENTES][GM][ALFA].keys():
                                SuperDiccionario[REDES][AGENTES][GM][ALFA][CDELTA] = []
                            else:
                                break
                    
                
    
    for nombre in Archivos_Datos[1:len(Archivos_Datos)]:
        alfa = float(nombre.split("_")[2].split("=")[1])
        Cdelta = float(nombre.split("_")[3].split("=")[1])
        N = int(nombre.split("_")[4].split("=")[1])
        gm = int(nombre.split("_")[5].split("=")[1])
        SuperDiccionario[REDES][N][gm][alfa][Cdelta].append(nombre)
        
    # Ya mejoré el armado del SuperDiccionario de manera de que cada N tenga los Alfa y cada
    # Alfa tenga los Cdelta y cada Cdelta tenga los GM correspondientes. Antes me pasaba que el Conjunto_Alfa era el conjunto
    # de TODOS los Alfas que hubiera entre todos los archivos, entonces si algún N tenía
    # Alfas que el otro no, eso podía generar problemas. Ahora, como cada diccionario
    # armado para cada N tiene por keys sólo los Alfas de ese N, puedo usar eso para
    # definir el Conjunto_Alfa de cada N y evitar los problemas que había visto que
    # iban a aparecer al querer graficar el mapa de colores de los estados finales del N=1000

#--------------------------------------------------------------------------------------------
    
# Empiezo iterando el N desde acá porque lo que voy a hacer es que al iniciar
# la iteración en N, defino mis Conjunto_Alfa y Conjunto_Cdelta en función de
# las keys de mi SuperDiccionario.

for REDES in ["Erdos-Renyi"]: # ["Barabasi"]: # ["Random Regulars"]:
    for AGENTES in [1000]:

        Conjunto_Gm = list(SuperDiccionario[REDES][AGENTES].keys())

        for GM in Conjunto_Gm:
            
            Conjunto_Alfa = list(SuperDiccionario[REDES][AGENTES][GM].keys())
        
            Conjunto_Cdelta = list(SuperDiccionario[REDES][AGENTES][GM][Conjunto_Alfa[0]].keys())
            
            # Primero me armo los grid para el gráfico de las fases. Para eso
            # primero tengo que armarme un array y con el np.meshgrid armarme 
            # los grids del pcolormesh.
            
            Conjunto_Alfa.reverse() # Lo invierto para que me quede el uno arriba y no abajo
            
            x = np.array(Conjunto_Cdelta)
            y = np.array(Conjunto_Alfa)
            
            Conjunto_Alfa.reverse() # Lo vuelvo a invertir para que de nuevo esté como siempre.
            
            XX,YY = np.meshgrid(x,y)
            
            ZZ = np.zeros(XX.shape)
            
            # Con esto ya tengo armados los grids de XX,YY y de paso me armo el grid
            # del ZZ para ir rellenándolo a medida que corro todo el programa, o usando
            # los datos que ya guardé de antes. Para eso es el módulo siguiente
            
            #---------------------------------------------------------------------------------------------

            # Voy a iterar esto para todos los archivos de datos que tengo
            
            for ALFA,ialfa in zip(Conjunto_Alfa,np.arange(len(Conjunto_Alfa))):
                
                for CDELTA,icdelta in zip(Conjunto_Cdelta,np.arange(len(Conjunto_Cdelta))):
                
                    #-----------------------------------------------------------------------------------
                    
                    # Abro mis gráficos, creo listas que voy a llenar con todas las simulaciones y armo algunas cosas varias
                    # que voy a necesitar para después
                    
                    OpinionesFinales = np.array([])
                    PuntosFinales = np.array([])
                    MaxNorm = 0
                    
                    #-------------------------------------------------------------------------------------
                    for nombre in SuperDiccionario[REDES][AGENTES][GM][ALFA][CDELTA]:

                        #--------------------------------------------------------------------------------------------
                    
                        # Levanto los datos del archivo original y separo los datos en tres listas.
                        # Una para la matriz de Adyacencia, una para la matriz de superposición y una para los vectores de opiniones
                    
                        Datos = ldata("../{}/{}".format(REDES,nombre))
                    
                        # Lista con elementos de los vectores de opinión. Al final sí había una forma compacta de hacer esto.
                        # Si la matriz de Adyacencia evoluciona en el tiempo, va a haber que ver de hacer cambios acá.
                        Var = np.array([float(x) for x in Datos[1][1::]])
                        
                        Opi = np.array([float(x) for x in Datos[3][1::]])
                    
                        #----------------------------------------------------------------------------------------------
                        
                        # Acá voy a calcular al sujeto que voy a usar para normalizar mis gráficos. Tiene que ser el máximo
                        # valor de opinión que haya alcanzado cualquier sujeto en cualquier momento.
                        
#                        MaxNorm = max(MaxNorm,max(np.absolute(Opi)))
                        
                        # Esto funciona perfecto. El único tema a considerar es que este valor MaxNorm se traspasa
                        # a otros módulos, entonces eso hace que esos módulos no sean tan independientes. En particular
                        # me refiero al módulo que construye el diccionario OdT y el que arma la lista de puntos
                        # finales PuntosFinales. Supongo que esto se podría solucionar directamente normalizando el 
                        # vector de opiniones. Entonces los otros trabajaría por su cuenta sin mezclar cosas
                        # de módulos que podrían no copiarse en futuros códigos.
                        
                        #-----------------------------------------------------------------------------------------------
                    
                        # Como todavía tengo dos tópicos, puedo graficar esto en un plano. Así que ahora voy a hacer
                        # un código presuponiendo que la cantidad de tópicos es 2. Sino, esto no debería realizarse.
                        # Atento a eso.
                        # Como ahora las listas en el diccionario no se sobreescriben, puedo hacer esto con un for aparte
                        # de lo anterior
                    
                    #                        plt.figure("Trayectoria Opiniones")
                    #                        for agente in range(AGENTES):
                    #                            plt.plot(Opi[::,0+T*agente],Opi[::,1+T*agente], color="gray",linewidth = 0.6, alpha=0.2)
                        
                        # Esto es el gráfico de las líneas grises. Con el nuevo formato de los datos que
                        # guardo, no tengo bien armado el cómo hacer esto por ahora, así que lo dejo desacoplado por
                        # el momento
                            
                        #-------------------------------------------------------------------------------------------------
                        
                        # Ahora lo que voy a hacer es tomar el estado final del sistema y guardarlo en un array
                        # para después sobre esos datos determinar el estado final del sistema
                        
                        OpinionesFinales = np.concatenate((OpinionesFinales,Opi), axis=None)
                        
                        # Con esto me armo el array de estados finales de mi sistema
                        
                        #-------------------------------------------------------------------------------------------------
                        
                        # Cuando quiera graficar los puntos que indican el punto final de la trayectoria
                        # de un agente en el espacio de fases, voy a necesitar que ese array contenga los puntos
                        # correctamente normalizados. Para eso voy a construir el array PuntosFinales que involucre
                        # normalización con el MaxNorm Correcto
                        
                        PuntosFinales = np.concatenate((PuntosFinales,Opi), axis=None)
                        
                        # Con esto me armo la lista de estados finales de mi sistema
                        
                        #-------------------------------------------------------------------------------------------------

                    # Genial, así como está esto ya arma el gráfico de las trayectorias de las opiniones. Ahora, me gustaría
                    # colocar puntos marcando el final de mis trayectorias.
                    
#                    plt.rcParams.update({'font.size': 18})
#                    plt.figure("Trayectoria Opiniones",figsize=(20,15))
#                    for x1,x2 in zip (PuntosFinales[0::2],PuntosFinales[1::2]):
#                        indice = Indice_Color(np.array([x1,x2]),Divisiones)
#                        plt.plot(x1,x2, "o" ,c = color[indice], markersize=10)
#
#
#                    #----------------------------------------------------------------------------------------------
                    
                    # Acá lo que voy a hacer es rellenar el grid de ZZ con los valores de los resultados de
                    # opiniones finales
                    
                    # Voy a agregar un paso extra en esto porque el sistema está teniendo problemas en clasificar algunos casos límite
                    EC = [("Consenso",0),("Polarizacion",1),("Ideologico",2)] # EC es Estados y colores. Tiene tuplas con los colores asociados
                    
                    ResultadoEF = EstadoFinal(OpinionesFinales)
                            
                    # Esto es ya lo mismo que antes, dependiendo de ResultadoEF es el número que va en la matriz ZZ
                    
                    for estado in EC:
                        if ResultadoEF == estado[0]:
                            ZZ[len(Conjunto_Alfa)-1-ialfa, icdelta] = estado[1] 
                    
                    #-----------------------------------------------------------------------------------------------------------
                    
                    # Estos son los parámetros que definen el tamaño del gráfico, tamaño de la letra y nombres de
                    # los ejes. Luego de eso guardo la figura y la cierro. Esto es para la figura de
                    # TdO.
                    
                    #            plt.tick_params(left=False,
                    #                bottom=False,
                    #                labelleft=False,
                    #                labelbottom=False)
#                    plt.xlabel("Tópico 1")
#                    plt.ylabel("Tópico 2")
#                    #            plt.title(r"Trayectoria de las opiniones en el espacio de tópicos para $\alpha$={},cos($\delta$)={} y N={}".format(ALFA,CDELTA,AGENTES))
##                    plt.xlim((xmin,xmax))
##                    plt.ylim((ymin,ymax))
#                    plt.annotate("{}".format(ResultadoEF), xy=(0.45,0.9),xycoords='axes fraction',fontsize=20,bbox=dict(facecolor='White', alpha=0.7))
#                    plt.annotate(r"$\alpha$={},cos($\delta$)={},N={}".format(ALFA,CDELTA,AGENTES), xy=(0.75,0.85),xycoords='axes fraction',fontsize=20,bbox=dict(facecolor='White', alpha=0.7))
#                    plt.annotate("Red={}, Gm={}".format(REDES,GM), xy=(0.75,0.8),xycoords='axes fraction',fontsize=20,bbox=dict(facecolor='White', alpha=0.7))
#                    plt.savefig("../../../Imagenes/Redes Estáticas/{}/GM={}/Trayectoria de las opiniones_Gm={}_alfa={:.2f}_Cdelta={}_N={}.png".format(REDES,GM,GM,ALFA,CDELTA,AGENTES),bbox_inches = "tight")
#                    plt.close("Trayectoria Opiniones")
                    
                    #------------------------------------------------------------------------------------------------
                    

            # Acá termino mi gráfico de Fases, una vez que recorrí todos los Alfa y Cdelta.
            
            # Armo mi colormap. Para eso armo una lista con los colores que voy a usar,
            # los cuales son una tuplas de tres elementos que combinan colores en proporción
            # donde el primer número es el color rojo, el segundo el verde y el tercero el azul.
            # Con eso luego uso la función de LinearSegmentedeColormap para que me traduzca
            # mi lista de colores a un colormap, y como sólo voy a graficar tres valores
            # en N pongo un 3 para separar el binneado de mi mapa de colores en sólo 3.
            # Luego le mando ese colormap al pcolormesh y listo.
            
            
            colors = [(0, 0.7, 0), (0, 0.3, 1), (1, 0.3, 0)]  #  R -> G -> B 
            cmap_name = 'Mi_lista'
            ColMap = LinearSegmentedColormap.from_list(cmap_name, colors, N=3)
            
            # Defino los parámetros usuales de mi gráfico
            
            plt.rcParams.update({'font.size': 24})
            plt.figure("Espacio parametros",figsize=(20,12))
            plt.xlabel(r"cos($\delta$)")
            plt.ylabel(r"$\alpha$")
            plt.title("Estados finales en EP")
            
            # Grafico la línea del Alfa Crítico teórico
            
            Xa = np.arange(-0.05,1.05,0.01)
            Ya = np.array([AlfaC(x,GM) for x in Xa])
            plt.plot(Xa,Ya,"--",color = "black",linewidth = 4, label = r"$\alpha_c$ teórico")
            plt.annotate("N={}_Gm={}_Red={}".format(AGENTES,GM,REDES), xy=(0.35,0.95),xycoords='axes fraction',fontsize=20,bbox=dict(facecolor='White', alpha=0.7))
            
            # Armo el gráfico del Alfa Crítico experimental
            
            Xb = Conjunto_Cdelta
            Yb = []
            
            for columna in range(ZZ.shape[1]):
                for fila in range(ZZ.shape[0]-1):
                    if ZZ[fila,columna]!=0 and ZZ[fila+1,columna]==0:
                        Yb.append((YY[fila,columna]+YY[fila+1,columna])/2)
                        break
                        
            plt.plot(Xb,Yb,"--",color = "yellow",linewidth = 4, label = r"$\alpha_c$ experimental")
            
            # Hago el ploteo del mapa de colores con el colormesh y usando el mapa de colroes creado por mi.
            
            plt.legend()
            plt.pcolormesh(XX,YY,ZZ,shading="nearest", cmap = ColMap)
            plt.savefig("../../../Imagenes/Redes Estáticas/{}/GM={}/Estados finales EP.png".format(REDES,GM), bbox_inches = "tight")
            plt.close("Espacio parametros")
            
            #---------------------------------------------------------------------------------------------------
            
            # Me falta guardar los valores de ZZ en un archivo, por si necesito hacerle un retoque al archivo y no 
            # quiero volver a correr todo de una
            
            np.savetxt("Grafico Fases Red={}_N={}_GM=_{}.csv".format(REDES,AGENTES,GM), ZZ, delimiter = ",")
            
            
            # -------------------------------------------------------------------------------------------------








Tiempo()





