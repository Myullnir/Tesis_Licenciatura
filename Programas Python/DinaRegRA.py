# -*- coding: utf-8 -*-
"""
Created on Wed Nov  3 12:44:42 2021

@author: Favio
"""


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

for Carpeta in ["DinaReg"]:

   # CÓDIGO PARA LEVANTAR ARCHIVOS DE UNA CARPETA CON TODOS LOS ARCHIVOS MEZCLADOS
    
    CarpCheck=[[root,files] for root,dirs,files in os.walk("./DilAct/{}".format(Carpeta))]
    
    # El elemento en la posición x[0] es el nombre de la carpeta
    
    for x in CarpCheck:
        # dada = x[0].split("\\")
        Archivos_Datos = [nombre for nombre in x[1]]
        Archivos_Datos.insert(0,x[0])
        
    

    #-------------------------------------------------------------------------------------------------------
    
    # Es importante partir del hecho de que mis archivos llevan por nombre: "Datos_Opiniones_alfa=$_Cdelta=$_N=$_Iter=$"
    # También tengo otros archivos llamados "Evolucion_Sistema_alfa=$_Cdelta=$_N=$_Iter=$"
    
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
        if N not in SuperDiccionario[Carpeta][tipo].keys():
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
    
    AlfaV = 0.4
    CdeltaV = 0
    

    for AGENTES in [1000]:
        
        TIPO = "Sistema"
        
        # Acá me voy a inicializar los arrays para graficar los mapas de colores de la red.
        
        
        # Defino el conjunto de valores de Cdelta a recorrer. Tengo que ordenarlos porque
        # el SuperDiccionario los ordena como los recibe, y el os.walk no necesariamente recorre
        # todo en orden.
        
        Conjunto_Cdelta = list(SuperDiccionario[Carpeta][TIPO][AGENTES].keys())
        Conjunto_Cdelta.sort()
        
        # Inicializo mi OpiMaxima
        
#        OpiMaxima = 0
#        
#        for CDELTA,icdelta in zip(Conjunto_Cdelta,np.arange(len(Conjunto_Cdelta))):
#            
#            # Para cada Cdelta defino el conjunto de Alfas asociados a recorrer.
#            # De nuevo, lo ordeno porque el SuperDiccionario no los tiene necesariamente ordenados.
#            
#            Conjunto_Alfa = list(SuperDiccionario[Carpeta][TIPO][AGENTES][CDELTA].keys())
#            Conjunto_Alfa.sort()
#            
#            for ALFA,ialfa in zip(Conjunto_Alfa,np.arange(len(Conjunto_Alfa))):
#                
#                if ALFA == AlfaV and CDELTA == CdeltaV:
#                
#                    for nombre,numero in zip(SuperDiccionario[Carpeta][TIPO][AGENTES][CDELTA][ALFA],np.arange(len(SuperDiccionario[Carpeta][TIPO][AGENTES][CDELTA][ALFA]))):
#                        
#                        
#                        # Acá levanto los datos de los archivos de Testigos. Estos archivos tienen los siguientes datos:
#                        # Opiniones hasta el final del archivo de todos los agentes
#    
#                        #--------------------------------------------------------------------------------------------
#                    
#                        # Levanto los datos del archivo original y separo los datos en tres listas.
#                        # Una para la matriz de Adyacencia, una para la matriz de superposición y una para los vectores de opiniones
#                    
#                        # Tengo que hacer una diferenciación entre levantar datos de las carpetas subdividida en 4 y de la carpeta con todo mezclado.
#    
#                        # PARA LEVANTAR DATOS DE LA CARPETA TODA MEZCLADA
#                        Datos = ldata("{}/{}".format(Conjunto_Direcciones[0],nombre))
#                        
#                        ArrayOpi = np.zeros((len(Datos)-1,len(Datos[1])-1))
#                                
#                        for fila,i in zip(Datos[1::],np.arange(len(Datos[1::]))):
#                            ArrayOpi[i] = fila[1::]
#                        
#                        OpiMaxima = max(OpiMaxima,np.absolute(ArrayOpi).max())
#    
#                        
#                        #-----------------------------------------------------------------------------------------------
#                        
            
        print("Calculé OpiMaxima")
        Tiempo()                                
                            
#        # Abro el gráfico de los Tópicos vs Tiempo
#        plt.rcParams.update({'font.size': 24})
#        plt.figure("Topico",figsize=(20,15))
#        plt.xlabel("Tiempo")
#        plt.ylabel(r"$x^1$")
#        plt.ylim(-OpiMaxima,OpiMaxima)
#        plt.grid()
#        
#        print("Arme el primero")
#        
#        # Abro el gráfico de las TdO
#        plt.rcParams.update({'font.size': 24})
#        plt.figure("Trayectoria Opiniones",figsize=(20,15))
#        plt.xlabel(r"$x^1$")
#        plt.ylabel(r"$x^2$")
#        plt.xlim(-OpiMaxima,OpiMaxima)
#        plt.ylim(-OpiMaxima,OpiMaxima)
#        
#        print("Arme el segundo")

        OpiMaxima = 100 # La estoy definiendo a mano tomando en cuenta lo que observé al armar los gráficos
        # de Distribución de Opiniones
        
        for CDELTA,icdelta in zip(Conjunto_Cdelta,np.arange(len(Conjunto_Cdelta))):
        
            # Para cada Cdelta defino el conjunto de Alfas asociados a recorrer.
            # De nuevo, lo ordeno porque el SuperDiccionario no los tiene necesariamente ordenados.
            
            Conjunto_Alfa = list(SuperDiccionario[Carpeta][TIPO][AGENTES][CDELTA].keys())
            Conjunto_Alfa.sort()
            
            for ALFA,ialfa in zip(Conjunto_Alfa,np.arange(len(Conjunto_Alfa))):
                    
                if ALFA == AlfaV and CDELTA == CdeltaV:
                        
                    for nombre,numero in zip(SuperDiccionario[Carpeta][TIPO][AGENTES][CDELTA][ALFA],np.arange(len(SuperDiccionario[Carpeta][TIPO][AGENTES][CDELTA][ALFA]))):
                        
                        # Hago el armado de los gráficos por cada iteración para poder observar cuáles quiero unir.
                        
                        # Abro el gráfico de los Tópicos vs Tiempo 
                        plt.rcParams.update({'font.size': 24})
                        plt.figure("Topico",figsize=(20,15))
                        plt.xlabel("Tiempo")
                        plt.ylabel(r"$x^1$")
                        plt.ylim(-OpiMaxima,OpiMaxima)
                        plt.grid()
                        
                        print("Arme el primero")
                        
                        # Abro el gráfico de las TdO
                        plt.rcParams.update({'font.size': 24})
                        plt.figure("Trayectoria Opiniones",figsize=(20,15))
                        plt.xlabel(r"$x^1$")
                        plt.ylabel(r"$x^2$")
                        plt.xlim(-OpiMaxima,OpiMaxima)
                        plt.ylim(-OpiMaxima,OpiMaxima)
                            
                        
                        # Acordate que en estos archivos guardaste los datos de los tópicos de 5 agentes testigos.
                        # Así que esos 5 son los que vamos a graficar.
                        
                        repeticion = int(nombre.split("_")[5].split("=")[1])
#                        if repeticion in [5]:
                        
                        Datos = ldata("{}/{}".format(Conjunto_Direcciones[0],nombre))
                        
                        ArrayOpi = np.zeros((len(Datos)-1,len(Datos[1])-1))
                        
                        for fila,i in zip(Datos[1::],np.arange(len(Datos[1::]))):
                            ArrayOpi[i] = fila[1::]
                        # De esta manera tengo mi array que me guarda los datos de los
                        # agentes a lo largo de la evolución del sistema.
                        
                        #----------------------------------------------------------------
                    
                        # Ahora yo voy a querer armar dos gráficos. Uno el que dijo Pablo de la
                        # TdO si no me equivoco. El otro el gráfico de la convergencia de Opiniones
                        # que estuve viendo en los archivos de Actividades
                        
                        # Tengo que armar los promedios para graficarlos también
                                                            
                        plt.figure("Topico")
                        
                        X = np.arange((len(Datos)-1))*0.01
                        for sujeto in range(5):
                            plt.plot(X,ArrayOpi[:,sujeto*50], color="gray", linewidth = 3)
    
                        #-----------------------------------------------------------------------------
                    
                        # Ahora yo voy a querer armar dos gráficos. Uno el que dijo Pablo de la
                        # TdO si no me equivoco. El otro el gráfico de la convergencia de Opiniones
                        # que estuve viendo en los archivos de Actividades
                        
                        # Tengo que armar los promedios para graficarlos también
                        
                        Promedios = np.zeros(ArrayOpi.shape[0])
                        
                        for indice in range(ArrayOpi.shape[0]):
                            Promedios[indice] = np.mean(ArrayOpi[indice][0::2]) # La cosa es promediar sólo la opinión del tópico 0

                        
                        X = np.arange((len(Datos)-1))*0.01
                        plt.plot(X,Promedios, color="red", linewidth = 5)
#                            plt.legend()
#                            plt.annotate(r"$\alpha$={},cos($\delta$)={},N={}".format(ALFA,CDELTA,AGENTES), xy=(0.5,0.75),xycoords='axes fraction',fontsize=20,bbox=dict(facecolor='White', alpha=0.7))
                        
                        # Acá debería hacer el otro gráfico, el que me propuso Pablo. Para esto tengo que hacer los viejos y clásicos
                        # TdO si no me equivoco. Eso no debería tardar mucho.
                        
                        #------------------------------------------------------------------------------------------------------------------------
                        
                        plt.figure("Trayectoria Opiniones")
                        
                        for sujeto in range(800):
                            plt.plot(ArrayOpi[:,0+2*sujeto],ArrayOpi[:,1+2*sujeto], color="gray",linewidth = 2, alpha=0.2)
                            
    #                            for x1,x2 in zip(ArrayOpi[ArrayOpi.shape[0]-1][0::2],ArrayOpi[ArrayOpi.shape[0]-1][1::2]):
    #                                indice = Indice_Color(np.array([x1,x2]),Divisiones)
    #                                plt.plot(x1,x2, "o" ,c = color[indice], markersize=10)
                            
    #                            plt.legend()
    
    
                        #--------------------------------------------------------------------------------------------------------
                        
                        # Acá debería hacer el otro gráfico, el que me propuso Pablo. Para esto tengo que hacer los viejos y clásicos
                        # TdO si no me equivoco. Eso no debería tardar mucho.
                        
                        Promedios0 = np.zeros(ArrayOpi.shape[0])
                        Promedios1 = np.zeros(ArrayOpi.shape[0])
                        
                        for indice in range(ArrayOpi.shape[0]):
                            Promedios0[indice] = np.mean(ArrayOpi[indice][0::2]) # Acá tomo el promedio de las opiniones en el tópico 0
                            Promedios1[indice] = np.mean(ArrayOpi[indice][1::2]) # Acá tomo el promedio de las opiniones en el tópico 1
                            
                        plt.plot(Promedios0,Promedios1, color="red",linewidth = 5 )
   
                        
                        #-------------------------------------------------------------------------------------------------------
                        
                        # Cierro los gráficos.
            
                        plt.figure("Topico")
                        plt.savefig("../Imagenes/RedAct/ActividadConexa/Topicos_alfa={:.3f}_Cdelta={:.2f}_iter={}.png".format(ALFA,CDELTA,repeticion),bbox_inches = "tight")
                        plt.close("Topico")
                            
            
            
                        plt.figure("Trayectoria Opiniones")
                        plt.savefig("../Imagenes/RedAct/ActividadConexa/TdO_alfa={:.3f}_Cdelta={:.2f}_iter={}.png".format(ALFA,CDELTA,repeticion),bbox_inches = "tight")
                        plt.close("Trayectoria Opiniones")
                        
                        # Voy a armar un cierre prematuro de los gráficos para hacerme una idea de cuales iteraciones quiero unir.
                        # Para eso voy a poner acá el armado de las curvas de los promedios.
                        
                        #-------------------------------------------------------------------------------------------------------------------
                            
                            
        
            
#                            for nombre,numero in zip(SuperDiccionario[Carpeta][TIPO][AGENTES][CDELTA][ALFA],np.arange(len(SuperDiccionario[Carpeta][TIPO][AGENTES][CDELTA][ALFA]))):
#                                
#                                if nombre.split("_")[1] == "Sistema":
#                                    
#                                    repeticion = int(nombre.split("_")[5].split("=")[1])
#                                    if repeticion in [5]:
#                                    
#                                        Datos = ldata("{}/{}".format(Conjunto_Direcciones[0],nombre))
#                                        
#                                        Opi = Datos[1::] # Lista con los datos de las opiniones
#                                        ArrayOpi = np.zeros((len(Datos)-1,len(Datos[1])-1))
#                                        
#                                        for fila,i in zip(Datos[1::],np.arange(len(Datos[1::]))):
#                                            ArrayOpi[i] = fila[1::]
#                                        # De esta manera tengo mi array que me guarda los datos de los
#                                        # agentes a lo largo de la evolución del sistema.
#                                        
#                                        #----------------------------------------------------------------
#                                    
#                                        # Ahora yo voy a querer armar dos gráficos. Uno el que dijo Pablo de la
#                                        # TdO si no me equivoco. El otro el gráfico de la convergencia de Opiniones
#                                        # que estuve viendo en los archivos de Actividades
#                                        
#                                        # Tengo que armar los promedios para graficarlos también
#                                        
#                                        Promedios = np.zeros(ArrayOpi.shape[0])
#                                        
#                                        for indice in range(ArrayOpi.shape[0]):
#                                            Promedios[indice] = np.mean(ArrayOpi[indice][0::2]) # La cosa es promediar sólo la opinión del tópico 0
#                                        
#                                        plt.figure("Topico")
#                                        
#                                        X = np.arange((len(Datos)-1))*0.01
#                                        plt.plot(X,Promedios, color="red", linewidth = 5)
#            #                            plt.legend()
#            #                            plt.annotate(r"$\alpha$={},cos($\delta$)={},N={}".format(ALFA,CDELTA,AGENTES), xy=(0.5,0.75),xycoords='axes fraction',fontsize=20,bbox=dict(facecolor='White', alpha=0.7))
#            
#                                        #-----------------------------------------------------------------------------
#                                        
#                                        # Acá debería hacer el otro gráfico, el que me propuso Pablo. Para esto tengo que hacer los viejos y clásicos
#                                        # TdO si no me equivoco. Eso no debería tardar mucho.
#                                        
#                                        plt.figure("Trayectoria Opiniones")
#            
#            
#                                        Promedios0 = np.zeros(ArrayOpi.shape[0])
#                                        Promedios1 = np.zeros(ArrayOpi.shape[0])
#                                        
#                                        for indice in range(ArrayOpi.shape[0]):
#                                            Promedios0[indice] = np.mean(ArrayOpi[indice][0::2]) # Acá tomo el promedio de las opiniones en el tópico 0
#                                            Promedios1[indice] = np.mean(ArrayOpi[indice][1::2]) # Acá tomo el promedio de las opiniones en el tópico 1
#                                            
#                                        plt.plot(Promedios0,Promedios1, color="red",linewidth = 5 )
#                                        
#                                        
#            #                            for x1,x2 in zip(ArrayOpi[ArrayOpi.shape[0]-1][0::2],ArrayOpi[ArrayOpi.shape[0]-1][1::2]):
#            #                                indice = Indice_Color(np.array([x1,x2]),Divisiones)
#            #                                plt.plot(x1,x2, "o" ,c = color[indice], markersize=10)
#                                            
#            #                            plt.legend()
        
                                
                        #-------------------------------------------------------------------------------------------------------------------
#                        
#                        # Cierro los gráficos.
#            
#                        plt.figure("Topico")
#                        plt.savefig("../Imagenes/RedAct/ActividadConexa/Topicos_alfa={:.3f}_Cdelta={:.2f}.png".format(ALFA,CDELTA,repeticion),bbox_inches = "tight")
#                        plt.close("Topico")
#                            
#            
#            
#                        plt.figure("Trayectoria Opiniones")
#                        plt.savefig("../Imagenes/RedAct/ActividadConexa/TdO_alfa={:.3f}_Cdelta={:.2f}.png".format(ALFA,CDELTA,repeticion),bbox_inches = "tight")
#                        plt.close("Trayectoria Opiniones")
                    
                        # Esto es el gráfico de las líneas grises. Con el nuevo formato de los datos que
                        # guardo, no tengo bien armado el cómo hacer esto por ahora, así que lo dejo desacoplado por
                        # el momento
                                
                    
Tiempo()
                    
                    