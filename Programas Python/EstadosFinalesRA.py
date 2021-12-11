# -*- coding: utf-8 -*-
"""
Created on Tue Dec  7 22:25:38 2021

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
import pandas as pd
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
        if max(Absolutos)<0.5 or x1==0 or x2==0:
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

for Carpeta in ["ActividadConexa"]:

   # CÓDIGO PARA LEVANTAR ARCHIVOS DE UNA CARPETA CON TODOS LOS ARCHIVOS MEZCLADOS
    
    CarpCheck=[[root,files] for root,dirs,files in os.walk("./DilAct/{}".format(Carpeta))]
    
    # El elemento en la posición x[0] es el nombre de la carpeta
    
    for x in CarpCheck:
        # dada = x[0].split("\\")
        Archivos_Datos = [nombre for nombre in x[1]]
        Archivos_Datos.insert(0,x[0])
        
    

    #-------------------------------------------------------------------------------------------------------
    
    # Es importante partir del hecho de que mis archivos llevan por nombre: "Datos_Opiniones_alfa=$_Cdelta=$_N=$_Iter=$"
    # También tengo otros archivos llamados "Datos_Testigos_alfa=$_Cdelta=$_N=$_Iter=$"
    
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
    
    for AGENTES in [1000]:
        
        #---------------------------------------------------------------------------------------------------------------
        
        TIPO = "Opiniones"
        
        
        # Defino el conjunto de valores de Cdelta a recorrer. Tengo que ordenarlos porque
        # el SuperDiccionario los ordena como los recibe, y el os.walk no necesariamente recorre
        # todo en orden.
        
        Conjunto_Cdelta = list(SuperDiccionario[Carpeta][TIPO][AGENTES].keys())
        Conjunto_Cdelta.sort()
        
        
        # Para cada Cdelta defino el conjunto de Alfas asociados a recorrer.
        # De nuevo, lo ordeno porque el SuperDiccionario no los tiene necesariamente ordenados.
        # El CDELTA que estoy usando 0. Igual
        # no importa, la idea es que definitivamente todos los Cdeltas tienen el mismo
        # conjunto de alfas. De no ser así, no podría armar correctamente estos gráficos.
        
        Conjunto_Alfa = list(SuperDiccionario[Carpeta][TIPO][AGENTES][0].keys())
        Conjunto_Alfa.sort()
        
        
        Conjunto_Alfa.reverse() # Lo invierto para que me quede el uno arriba y no abajo
            
        x = np.array(Conjunto_Cdelta)
        y = np.array(Conjunto_Alfa)
        
        Conjunto_Alfa.reverse() # Lo vuelvo a invertir para que de nuevo esté como siempre.
        
        XX,YY = np.meshgrid(x,y)


        #------------------------------------------------------------------------------------

        # Levanto los datos del csv usando el pandas y luego paso los datos al ZZ
        
        DF = pd.read_csv("Grafico Fases.csv",delimiter = ",",header = None)
        
        ZZ = np.zeros(DF.shape)
        
        for fila in range(ZZ.shape[0]):
            for columna in range(ZZ.shape[1]):
                ZZ[fila,columna] = DF.iloc[fila,columna]
        
        
        #----------------------------------------------------------------------------------------------------------
        
        # Volvamos a lo que tenía antes, un array super gigante de grados medios de todas
        # las redes, y de ahí veo cómo resolver eso.
        GradosTotales = np.array([])
        TiemposTotales = np.zeros((len(Conjunto_Cdelta),len(Conjunto_Alfa)*len(SuperDiccionario[Carpeta][TIPO][AGENTES][0][0])))
        ActividadesTotales = np.zeros((len(Conjunto_Cdelta),len(Conjunto_Alfa)*len(SuperDiccionario[Carpeta][TIPO][AGENTES][0][0])))
        
        
        for CDELTA,icdelta in zip(Conjunto_Cdelta,np.arange(len(Conjunto_Cdelta))):
            
            # Para cada Cdelta defino el conjunto de Alfas asociados a recorrer.
            # De nuevo, lo ordeno porque el SuperDiccionario no los tiene necesariamente ordenados.
            
            Conjunto_Alfa = list(SuperDiccionario[Carpeta][TIPO][AGENTES][CDELTA].keys())
            Conjunto_Alfa.sort()
            
            
            for ALFA,ialfa in zip(Conjunto_Alfa,np.arange(len(Conjunto_Alfa))):
                
                for nombre,numero in zip(SuperDiccionario[Carpeta][TIPO][AGENTES][CDELTA][ALFA],np.arange(len(SuperDiccionario[Carpeta][TIPO][AGENTES][CDELTA][ALFA]))):
                    
                    
                    # Acá levanto los datos de los archivos de opiniones. Estos archivos tienen los siguientes datos:
                    # Opinión Inicial del sistema
                    # Variación Promedio
                    # Opinión Final
                    # Grado de Agentes
                    # Actividad de Agentes
                    # Semilla

                    #--------------------------------------------------------------------------------------------
                
                    # Levanto los datos del archivo original y separo los datos en tres listas.
                    # Una para la matriz de Adyacencia, una para la matriz de superposición y una para los vectores de opiniones
                
                    # Tengo que hacer una diferenciación entre levantar datos de las carpetas subdividida en 4 y de la carpeta con todo mezclado.

                    # PARA LEVANTAR DATOS DE LA CARPETA TODA MEZCLADA
                    Datos = ldata("{}/{}".format(Conjunto_Direcciones[0],nombre))
                    
                    # Levanto los datos de Variación Promedio
                    Var = np.array([float(x) for x in Datos[3][1::]])
                    
                    # Levanto los datos de Grados de los agentes
                    Grados = np.array([int(x) for x in Datos[7][1::]])
                    
                    # Levanto los datos de Actividad de los agentes
                    Actividad = np.array([int(x) for x in Datos[9][1::]])
                    
                    # Me guardo los datos de los grados en un solo array y con eso después calculo el grado
                    # medio del sistema "TOTAL"
                    
                    GradosTotales = np.concatenate((GradosTotales,np.mean(Grados)),axis=None)

                    #----------------------------------------------------------------------------------------------
                    
                    # Voy a ir armando mi array con los valores de Tiempo de Simulación.
                    # Lo voy a llamar TideSi.
                    # Voy a guardar también los tiempos Totales acá.
                    
                    TiemposTotales[icdelta,ialfa*len(SuperDiccionario[Carpeta][TIPO][AGENTES][0][0])+numero] = Var.shape[0]
                    
                    # Esto debería funcionar derechito.
                    
                    #------------------------------------------------------------------------------------------------
                    
                    # Me guardo los datos de las actividades en un solo array y con eso después calculo la actividad
                    # media del sistema "TOTAL"
                    
                    ActividadesTotales[icdelta,ialfa*len(SuperDiccionario[Carpeta][TIPO][AGENTES][0][0])+numero] = np.mean(Actividad)

                    #----------------------------------------------------------------------------------------------
        
        # Con el Ycdelta ya armado, grafico el Grado medio del sistema en función de Cdelta y veo si
        # ahora esto da alguna relación o nada que ver.
        
        # Me armo mi array de grados medios para cada Cdelta
#        Ycdelta = np.zeros(len(Conjunto_Cdelta))
#        for i in range(len(Conjunto_Cdelta)):
#            Ycdelta[i] = np.mean(GradosTotales[i*len(Conjunto_Alfa)*len(SuperDiccionario[Carpeta][TIPO][AGENTES][0][0]):(i+1)*len(Conjunto_Alfa)*len(SuperDiccionario[Carpeta][TIPO][AGENTES][0][0])])
        
        #-------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        
        # Como una primer medida burda, voy a definir el Gradomedio de la red como
        # el grado medio promediado de todas las redes conexas que se llegaron a crear.
        # Estaría bueno armar un histograma de esos datos. Eso lo mandaré mañana quizás
        
        GM = np.mean(GradosTotales)
        
        # También voy a definir el grado medio calculado a partir de la actividad
        # media de los agentes. Ese es el grado medio teórico de las redes de actividad
        # obtenido utilizando la teoría del modelo de redes de Actividad.
        # El cálculo es <k> = 2*m*<a>*<reconstrucciones>. Las reconstrucciones es la cantidad
        # de veces que una red se rearma. m es la cantidad de enlaces que genera un nodo
        # al activarse y <a> es la actividad media. Esta actividad, al igual que las
        # reconstrucciones, están promediadas a lo largo de todas las simulaciones.
        
        gradomedio = 2*10*np.mean(ActividadesTotales)*(np.mean(TiemposTotales)/100)

        # Acá termino mi gráfico de Fases, una vez que recorrí todos los Alfa y Cdelta.
        
        # Armo mi colormap. Para eso armo una lista con los colores que voy a usar,
        # los cuales son una tuplas de tres elementos que combinan colores en proporción
        # donde el primer número es el color rojo, el segundo el verde y el tercero el azul.
        # Con eso luego uso la función de LinearSegmentedeColormap para que me traduzca
        # mi lista de colores a un colormap, y como sólo voy a graficar tres valores
        # en N pongo un 3 para separar el binneado de mi mapa de colores en sólo 3.
        # Luego le mando ese colormap al pcolormesh y listo.
        
        
        colors = [(0, 0.7, 0), (0, 0.3, 1), (1, 0.3, 0),(0.8, 0, 0.8)] #,(0,0,0)]  #  R -> G -> B -> Viol -> N
        cmap_name = 'Mi_lista'
        ColMap = LinearSegmentedColormap.from_list(cmap_name, colors, N=4)
        
        # Defino los parámetros usuales de mi gráfico
        
        plt.rcParams.update({'font.size': 24})
        plt.figure("Espacio parametros",figsize=(20,12))
        plt.xlabel(r"cos($\delta$)")
        plt.ylabel(r"$\alpha$")
        # plt.title("Estados finales en Espacio de Parametros")
        
        # Grafico la línea del alfa con GM variable
        
#        Xv = np.array(Conjunto_Cdelta)
#        Yv = np.array([])
#        Yv = [AlfaC(x,gm) for x,gm in zip(Conjunto_Cdelta,Ycdelta)]
#        plt.plot(Xv,Yv,color = "cyan",linewidth = 5, label = r"$\alpha_v$")
        
        # Grafico la línea del alfa con gradomedio teórico según redes de actividad
        
        Xt = np.arange(min(Conjunto_Cdelta),max(Conjunto_Cdelta),0.002)
        Yt = np.array([AlfaC(x,gradomedio) for x in Xt])
        plt.plot(Xt,Yt,color = "cyan",linewidth = 5, label = r"$\alpha_t$")
        
        
        # Grafico la línea del Alfa Crítico teórico
        
        Xa = np.arange(min(Conjunto_Cdelta),max(Conjunto_Cdelta),0.002)
        Ya = np.array([AlfaC(x,GM) for x in Xa])
        plt.plot(Xa,Ya,"--",color = "black",linewidth = 5, label = r"$\alpha_c$")
        
        
        # Hago el ploteo del mapa de colores con el colormesh y usando el mapa de colroes creado por mi.
        
        plt.legend()
        plt.pcolormesh(XX,YY,ZZ,shading="nearest", cmap = ColMap)
        
        # plt.ylim(min(Conjunto_Alfa)-0.005,max(Conjunto_Alfa)+0.005)
        plt.savefig("../Imagenes/RedAct/{}/Estados finales EP.png".format(Carpeta), bbox_inches = "tight")
        plt.close("Espacio parametros")


        #---------------------------------------------------------------------------------------------------


Tiempo()