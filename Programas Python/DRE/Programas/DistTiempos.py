# -*- coding: utf-8 -*-
"""
Created on Wed Nov 24 20:21:14 2021

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
        if max(Absolutos)<0.5:
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

T=2 # Defino acá el número de tópicos porque es algo que no cambia por ahora,
# pero no tenía dónde más definirlo

SuperDiccionario = dict()

for REDES in ["Erdos-Renyi","RandomRegulars","Barabasi"]:

    # Este parámetro llamado Subdividido es algo que defino yo a mano para definir si estoy leyendo una 
    # carpeta donde los archivos de datos están divididos en 4 carpetas, o si están todos mezclados en
    # la carpeta. Empecé a hacer esto de dividirlos porque Pablo me dijo que era necesario.
    Subdividido = False
    
    # Primero levanto datos de los nombres de los archivos de mis redes. Para eso es importante notar
    # que mis archivos ahora van a empezar a tener cuatro carpetas donde los valores de GM estén
    # diferenciados. Para eso necesita que el programa distinga cuántas carpetas hay en la carpeta
    # principal y que me arme la lista de archivos dentro de cada carpeta. Voy a armar un segundo código
    # pensado en levantar los archivos de las carpetas que tienen los archivos separados en 4 carpetas
    # según GM. Luego activo el código en función de la carpeta de la cual voy a levantar datos.
    
    # CÓDIGO PARA LEVANTAR DATOS DE UNA CARPETA SUBDIVIDIDA EN 4 CARPETAS SEGÚN EL GM DE LOS ARCHIVOS.
    
    if Subdividido == True:
    
        CarpCheck=[[root,dirs,files] for root,dirs,files in os.walk("../{}".format(REDES))]
        
        # En este caso lo mejor sería armar un diccionario en el cual guardaré los nombres
        # de los archivos y usaré el GM como índice. Para eso primero tengo que tomar el
        # nombre de la carpeta en la que se encuentra y de ahí extraer el número del GM.
        # El nombre es del estilo "../$Carpeta$/$Red$\\GM=$$". Entonces si no me equivoco,
        # puedo simplemente hacerle un split("=") y con eso ya saco el GM.
        
        # El elemento en la posición x[0] es el nombre de la carpeta
        
        Diccionario_Datos = dict()
        for indice in range(len(CarpCheck[0][1])):
            Gm = int(CarpCheck[0][1][indice].split("=")[1])
            if len(CarpCheck[indice+1][2]) > 0:
                Diccionario_Datos[Gm] = [nombre for nombre in CarpCheck[indice+1][2]]
                Diccionario_Datos[Gm].insert(0,CarpCheck[indice+1][0])
                
        
        
        # Con esto tengo los nombres de todos los archivos en la carpeta de Datos de Barabasi
        # Archivos_Datos tiene en la primer coordenada el principio de la dirección
        # de la carpeta, y el resto de elementos son los archivos en la carpeta.
        
        #---------------------------------------------------------------------------------------------
        
        # Es importante partir del hecho de que mis archivos llevan por nombre: "Datos_Opiniones_alfa=$_Cdelta=$_N=$_Gm=$_ID=$_Iter=$"
        
        Conjunto_Direcciones = []
        
        SuperDiccionario[REDES] = dict()
        
        for gradom in Diccionario_Datos.keys():
            Archivos_Datos = Diccionario_Datos[gradom]
            Gm = gradom
            Conjunto_Direcciones.append(Archivos_Datos[0])
            for nombre in Archivos_Datos[1:len(Archivos_Datos)]:
                alfa = float(nombre.split("_")[2].split("=")[1])
                Cdelta = float(nombre.split("_")[3].split("=")[1])
                N = int(nombre.split("_")[4].split("=")[1])
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



        Conjunto_Direcciones.sort(key = lambda direccion: int(direccion.split("=")[1]))
        
        
        
        
        # Le hice una modificación a esta parte del código, ahora esto trabaja
        # armando el SuperDiccionario también, no sólo los Conjuntos de Alfa, Cdelta
        # y demás. Lo bueno de esto es que ahora el armado del SuperDiccionario
        # es mucho más rápido.
        
        # No organizo el Conjunto_Gm para que vaya en el mismo orden que el Conjunto_Direcciones
        
        #-------------------------------------------------------------------------------------------------------

    
    else:    
        # CÓDIGO PARA LEVANTAR ARCHIVOS DE UNA CARPETA CON TODOS LOS ARCHIVOS MEZCLADOS
        
        CarpCheck=[[root,files] for root,dirs,files in os.walk("../{}".format(REDES))]
        
        # El elemento en la posición x[0] es el nombre de la carpeta
        
        for x in CarpCheck:
            # dada = x[0].split("\\")
            Archivos_Datos = [nombre for nombre in x[1]]
            Archivos_Datos.insert(0,x[0])
            
        
    
        #-------------------------------------------------------------------------------------------------------
        
        # Es importante partir del hecho de que mis archivos llevan por nombre: "Datos_Opiniones_alfa=$_Cdelta=$_N=$_Gm=$_ID=$_Iter=$"
        
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
        
        #--------------------------------------------------------------------------------------------
        
        
    # Empiezo iterando el N desde acá porque lo que voy a hacer es que al iniciar
    # la iteración en N, defino mis Conjunto_Alfa y Conjunto_Cdelta en función de
    # las keys de mi SuperDiccionario.

    
    
    for AGENTES in [1000]:

        Conjunto_Gm = list(SuperDiccionario[REDES][AGENTES].keys())
        Conjunto_Gm.sort()

        for GM,igm in zip(Conjunto_Gm,np.arange(len(Conjunto_Gm))):
            
            #-------------------------------------------------------------------------------------
            
            ALFA = 1
            for CDELTA in [-0.4,-0.2,0,0.2,0.4]:
                
                # Me armo el array de Tiempos de Simulación.
                
                TideSi = np.zeros(len(SuperDiccionario[REDES][AGENTES][GM][ALFA][CDELTA]))
                
                for nombre,numero in zip (SuperDiccionario[REDES][AGENTES][GM][ALFA][CDELTA],np.arange(len(SuperDiccionario[REDES][AGENTES][GM][ALFA][CDELTA]))):
                    
                    #--------------------------------------------------------------------------------------------
                
                    # Levanto los datos del archivo original y separo los datos en tres listas.
                    # Una para la matriz de Adyacencia, una para la matriz de superposición y una para los vectores de opiniones
                
                    # Tengo que hacer una diferenciación entre levantar datos de las carpetas subdividida en 4 y de la carpeta con todo mezclado.
                    
                    if Subdividido == True:
                        #PARA LEVANTAR DATOS DE LA CARPETA SUBDIVIDIDA EN 4
                        Datos = ldata("{}/{}".format(Conjunto_Direcciones[igm],nombre))
                        
                    else:
                        # PARA LEVANTAR DATOS DE LA CARPETA TODA MEZCLADA
                        Datos = ldata("{}/{}".format(Conjunto_Direcciones[0],nombre))
                    
                    # Lista con elementos de los vectores de opinión. Al final sí había una forma compacta de hacer esto.
                    # Si la matriz de Adyacencia evoluciona en el tiempo, va a haber que ver de hacer cambios acá.
                    
#                            Opi0 = np.array([float(x) for x in Datos[1][1::]])
                    
                    Var = np.array([float(x) for x in Datos[1][1::]])
                    
                    Opi = np.array([float(x) for x in Datos[3][1::]])
                    
                    #-----------------------------------------------------------------------------------------------
                    
                    # Voy guardando el tiempo de simulación de cada uno de las simulaciones del putno de ensamble.
                    # Acordate que en total son 61.
                    
                    TideSi[numero] = Var.shape[0]
                    
                    #-----------------------------------------------------------------------------------------------
                    
                # Acá armo el gráfico de las distribuciones de tiempos de Simulacion
                
                plt.rcParams.update({'font.size': 24})
                fig = plt.figure("DistTiempo",figsize=(20,15))
                plt.hist(TideSi,bins=15)
                plt.grid()
                plt.savefig("../../../Imagenes/Redes Estáticas/{}/GM={}/Dist_Tiempos_Cdelta={:.2f}.png".format(REDES,GM,CDELTA),bbox_inches = "tight")
                plt.close("DistTiempo")
                Tiempo()

                        
Tiempo()