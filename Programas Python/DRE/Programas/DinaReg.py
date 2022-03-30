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

for REDES in ["Erdos-Renyi"]: # ,"RandomRegulars","Barabasi"]:

   # CÓDIGO PARA LEVANTAR ARCHIVOS DE UNA CARPETA CON TODOS LOS ARCHIVOS MEZCLADOS
    
    CarpCheck=[[root,files] for root,dirs,files in os.walk("../DinaReg/{}".format(REDES))]
    
    # El elemento en la posición x[0] es el nombre de la carpeta
    
    for x in CarpCheck:
        # dada = x[0].split("\\")
        Archivos_Datos = [nombre for nombre in x[1]]
        Archivos_Datos.insert(0,x[0])
        
    

    #-------------------------------------------------------------------------------------------------------
    
    # Es importante partir del hecho de que mis archivos llevan por nombre: "Datos_Opiniones_alfa=$_Cdelta=$_N=$_Gm=$_ID=$_Iter=$"
    # También tengo otros archivos llamados "Evolucion_Sistema_alfa=$_Cdelta=$_N=$_Gm=$_ID=$_Iter=$"
    
    Conjunto_Direcciones = [Archivos_Datos[0]]
    
    SuperDiccionario[REDES] = dict()
    
    for nombre in Archivos_Datos[1:len(Archivos_Datos)]:
        alfa = float(nombre.split("_")[2].split("=")[1])
        Cdelta = float(nombre.split("_")[3].split("=")[1])
        N = int(nombre.split("_")[4].split("=")[1])
        Gm = int(nombre.split("_")[5].split("=")[1])
        if N not in SuperDiccionario[REDES].keys():
            SuperDiccionario[REDES][N] = dict()
            SuperDiccionario[REDES][N][Gm] = dict()
            SuperDiccionario[REDES][N][Gm][alfa] = dict()
            SuperDiccionario[REDES][N][Gm][alfa][Cdelta] = [nombre]
        elif Gm not in SuperDiccionario[REDES][N].keys():
            SuperDiccionario[REDES][N][Gm] = dict()
            SuperDiccionario[REDES][N][Gm][alfa] = dict()
            SuperDiccionario[REDES][N][Gm][alfa][Cdelta] = [nombre]
        elif alfa not in SuperDiccionario[REDES][N][Gm].keys():
            SuperDiccionario[REDES][N][Gm][alfa] = dict()
            SuperDiccionario[REDES][N][Gm][alfa][Cdelta] = [nombre]
        elif Cdelta not in SuperDiccionario[REDES][N][Gm][alfa].keys():
            SuperDiccionario[REDES][N][Gm][alfa][Cdelta] = [nombre]
        else:
            SuperDiccionario[REDES][N][Gm][alfa][Cdelta].append(nombre)

    
    # Le hice una modificación a esta parte del código, ahora esto trabaja
    # armando el SuperDiccionario también, no sólo los Conjuntos de Alfa, Cdelta
    # y demás. Lo bueno de esto es que ahora el armado del SuperDiccionario
    # es mucho más rápido.
    
    # En este caso SuperDiccionario está juntando tanto los nombres
    # de Evolución Sistemas con los de Datos Opiniones.
    #--------------------------------------------------------------------------------------------
    
    AlfaV = 0.5
    CdeltaV = 0
    
    Graficar =[0,2,9,8]
    

    for AGENTES in [1000]:
        for GM in [8]:
            Conjunto_Alfa = list(SuperDiccionario[REDES][AGENTES][GM].keys())
            Conjunto_Alfa.sort()
            
            OpiMaxima = 0
            
            for ALFA in Conjunto_Alfa:
                Conjunto_Cdelta = list(SuperDiccionario[REDES][AGENTES][GM][ALFA].keys())
                Conjunto_Cdelta.sort()
                for CDELTA in Conjunto_Cdelta:
                    if ALFA == AlfaV and CDELTA == CdeltaV:
                        for nombre in SuperDiccionario[REDES][AGENTES][GM][ALFA][CDELTA][15::]:
                            if nombre.split("_")[1] == "Sistema":
                                Datos = ldata("{}/{}".format(Conjunto_Direcciones[0],nombre))
                                
                                Opi = Datos[1::] # Lista con los datos de las opiniones
                                ArrayOpi = np.zeros((len(Datos)-1,len(Datos[1])-1))
                                
                                for fila,i in zip(Datos[1::],np.arange(len(Datos[1::]))):
                                    ArrayOpi[i] = fila[1::]
                                # De esta manera tengo mi array que me guarda los datos de los
                                # agentes a lo largo de la evolución del sistema.
                                
                                OpiMaxima = max(OpiMaxima,np.absolute(ArrayOpi).max())
                                
                                # Con esto me calculo la Opinión Máxima para hacerme el gráfico igual en todos los casos.
                                
                                #----------------------------------------------------------------
                                
            
            # Abro el gráfico de las TdO
            plt.rcParams.update({'font.size': 24})
            plt.figure("Topico",figsize=(20,15))
            plt.xlabel("Tiempo")
            plt.ylabel(r"$x^1$")
            plt.ylim(-OpiMaxima,OpiMaxima)
            plt.grid()
            
            
            
            # Abro el gráfico de los Tópicos vs Tiempo
            plt.rcParams.update({'font.size': 24})
            plt.figure("Trayectoria Opiniones",figsize=(20,15))
            plt.xlabel(r"$x^1$")
            plt.ylabel(r"$x^2$")
            plt.xlim(-OpiMaxima,OpiMaxima)
            plt.ylim(-OpiMaxima,OpiMaxima)
            
            """

            
            # Abro el gráfico de Histogramas 2D
            plt.rcParams.update({'font.size': 24})
            plt.figure("Histograma 2D",figsize=(20,15))
            plt.xlabel(r"$x^1$")
            plt.ylabel(r"$x^2$")
            plt.xlim(-OpiMaxima,OpiMaxima)
            plt.ylim(-OpiMaxima,OpiMaxima)
            """
            
            for ALFA in Conjunto_Alfa:
                Conjunto_Cdelta = list(SuperDiccionario[REDES][AGENTES][GM][ALFA].keys())
                Conjunto_Cdelta.sort()
                for CDELTA in Conjunto_Cdelta:
#                    OpinionesFinales = np.array([])
                    
                    if ALFA == AlfaV and CDELTA == CdeltaV:
                        
                        for nombre in SuperDiccionario[REDES][AGENTES][GM][ALFA][CDELTA]:
                            
                            if nombre.split("_")[1] == "Sistema":
                                
                                repeticion = int(nombre.split("_")[7].split("=")[1])
                                if repeticion in Graficar:
                                
                                    Datos = ldata("{}/{}".format(Conjunto_Direcciones[0],nombre))
                                    
                                    Opi = Datos[1::] # Lista con los datos de las opiniones
                                    ArrayOpi = np.zeros((len(Datos)-1,len(Datos[1])-1))
                                    
                                    for fila,i in zip(Datos[1::],np.arange(len(Datos[1::]))):
                                        ArrayOpi[i] = fila[1::]
                                        
                                    # De esta manera tengo mi array que me guarda los datos de los
                                    # agentes a lo largo de la evolución del sistema.
                                    
                                    # Levanto las opiniones finales para graficar los histogramas 2D
#                                    OpinionesFinales = np.concatenate((OpinionesFinales,np.array([float(x) for x in Opi[len(Opi)-1][1::]])), axis=None)
                                    
                                    #----------------------------------------------------------------
                                    
                                    # Ahora yo voy a querer armar dos gráficos. Uno el que dijo Pablo de la
                                    # TdO si no me equivoco. El otro el gráfico de la convergencia de Opiniones
                                    # que estuve viendo en los archivos de Actividades
                                    
                                    # Tengo que armar los promedios para graficarlos también
                                                                        
                                    plt.figure("Topico")
                                    
                                    X = np.arange(ArrayOpi.shape[0])*0.01
                                    for sujeto in range(200):
                                        plt.plot(X,ArrayOpi[:,sujeto*4], color="gray", linewidth = 1, alpha = 0.5)

                                    #-----------------------------------------------------------------------------
                                    
                                    # Acá debería hacer el otro gráfico, el que me propuso Pablo. Para esto tengo que hacer los viejos y clásicos
                                    # TdO si no me equivoco. Eso no debería tardar mucho.
                                    
                                    plt.figure("Trayectoria Opiniones")
                                    
                                    for sujeto in range(AGENTES):
                                        plt.plot(ArrayOpi[:,0+2*sujeto],ArrayOpi[:,1+2*sujeto], color="gray",linewidth = 0.5, alpha=0.3)
                                        
        #                            for x1,x2 in zip(ArrayOpi[ArrayOpi.shape[0]-1][0::2],ArrayOpi[ArrayOpi.shape[0]-1][1::2]):
        #                                indice = Indice_Color(np.array([x1,x2]),Divisiones)
        #                                plt.plot(x1,x2, "o" ,c = color[indice], markersize=10)
                                        
        #                            plt.legend()
                                    
                                    #-----------------------------------------------------------------------------------------------
                                    """
                                    # Acá armo los gráficos de histogramas 2D.
                                    
                                    plt.figure("Histograma 2D")
                                    
                                    OpiExtremos = np.array([OpiMaxima,OpiMaxima,-OpiMaxima,OpiMaxima,OpiMaxima,-OpiMaxima,-OpiMaxima,-OpiMaxima])
                                    Opiniones2D = np.concatenate((OpinionesFinales,OpiExtremos), axis=None)
                                    plt.hist2d(Opiniones2D[0::2],Opiniones2D[1::2], bins=(59,59), density=True, cmap=plt.cm.Reds)
                                    plt.colorbar()
                                    
#                                    plt.savefig("../../../Imagenes/Redes Estáticas/DinaReg/{}/H2D_alfa={:.3f}_Cdelta={:.2f}_C2.png".format(REDES,ALFA,CDELTA,repeticion),bbox_inches = "tight")
                                    plt.savefig("../../../Imagenes/Redes Estáticas/DinaReg/{}/H2DCon0.png".format(REDES),bbox_inches = "tight")
                                    plt.close("Histograma 2D")
                                    """
                                    
                                    #-------------------------------------------------------------------------------------------------
                                    
                                    
                        
                        for nombre in SuperDiccionario[REDES][AGENTES][GM][ALFA][CDELTA]:
                            
                            if nombre.split("_")[1] == "Sistema":
                                
                                repeticion = int(nombre.split("_")[7].split("=")[1])
                                if repeticion in Graficar:
                                
                                    Datos = ldata("{}/{}".format(Conjunto_Direcciones[0],nombre))
                                    
                                    Opi = Datos[1::] # Lista con los datos de las opiniones
                                    ArrayOpi = np.zeros((len(Datos)-1,len(Datos[1])-1))
                                    
                                    for fila,i in zip(Datos[1::],np.arange(len(Datos[1::]))):
                                        ArrayOpi[i] = fila[1::]
                                    # De esta manera tengo mi array que me guarda los datos de los
                                    # agentes a lo largo de la evolución del sistema.
                                    
                                    #-----------------------------------------------------------------------------
                
                                    # Para graficar los Promedios, voy a hacer gráficos de promedios por
                                    # rama. Ahora, los casos son distintos para Polarización en general y
                                    # Consenso. Así que voy a hacer una separación según el alfa
                                    
                                    plt.figure("Topico")
                                    
                                    
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
                                    
                                    #--------------------------------------------------------------------------------------------------------
                    
                                    # Acá armo los promedios para cada rama. Para eso, como ahora estoy en el espacio de tópicos,
                                    # necesito tomar promedios de ambos tópicos, no de uno solo
                                    
                                    plt.figure("Trayectoria Opiniones")
                                    
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
#                                        plt.ylim(-100,100)
#                                        plt.xlim(-100,100)
                                        
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
                        
                        # Cierro los gráficos.
            
                        plt.figure("Topico")
                        plt.savefig("../../../Imagenes/Redes Estáticas/DinaReg/{}/Topicos_alfa={:.3f}_Cdelta={:.2f}.png".format(REDES,ALFA,CDELTA,Graficar[0]),bbox_inches = "tight")
                        plt.close("Topico")
                            
            
            
                        plt.figure("Trayectoria Opiniones")
                        plt.savefig("../../../Imagenes/Redes Estáticas/DinaReg/{}/TdO_alfa={:.3f}_Cdelta={:.2f}.png".format(REDES,ALFA,CDELTA,Graficar[0]),bbox_inches = "tight")
                        plt.close("Trayectoria Opiniones")
                    
                        # Esto es el gráfico de las líneas grises. Con el nuevo formato de los datos que
                        # guardo, no tengo bien armado el cómo hacer esto por ahora, así que lo dejo desacoplado por
                        # el momento
                    
Tiempo()
                    
                    