# -*- coding: utf-8 -*-
"""
Created on Sun Jul  4 12:21:50 2021

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

# Primero levanto datos de la carpeta de la red REDES

SuperDiccionario = dict()

Carpetas = ["Actividad Reversion","Regact","HomofiliaCero","TiempoExtra","RCC"]

for SelCarpeta in [3]:
    
    # CÓDIGO PARA LEVANTAR ARCHIVOS DE UNA CARPETA CON TODOS LOS ARCHIVOS MEZCLADOS
    
    CarpCheck=[[root,files] for root,dirs,files in os.walk("./DilAct/{}".format(Carpetas[SelCarpeta]))]
    
    # El elemento en la posición x[0] es el nombre de la carpeta
    
    for x in CarpCheck:
        Archivos_Datos = [nombre for nombre in x[1]]
        Archivos_Datos.insert(0,x[0])
        
    

    #-------------------------------------------------------------------------------------------------------
    
    # Es importante partir del hecho de que mis archivos llevan por nombre: "Datos_Opiniones_alfa=$_Cdelta=$_N=$_Iter=$"
    # También tengo otros archivos llamados "Datos_Actividades_alfa=$_Cdelta=$_N=$_Iter=$"
    
    Conjunto_Direcciones = [Archivos_Datos[0]]
    
    SuperDiccionario[Carpetas[SelCarpeta]] = dict()
    
    for nombre in Archivos_Datos[1:len(Archivos_Datos)]:
        tipo = nombre.split("_")[1]
        alfa = float(nombre.split("_")[2].split("=")[1])
        Cdelta = float(nombre.split("_")[3].split("=")[1])
        N = int(nombre.split("_")[4].split("=")[1])
        if tipo not in SuperDiccionario[Carpetas[SelCarpeta]].keys():
            SuperDiccionario[Carpetas[SelCarpeta]][tipo] = dict()
            SuperDiccionario[Carpetas[SelCarpeta]][tipo][N] = dict()
            SuperDiccionario[Carpetas[SelCarpeta]][tipo][N][Cdelta] = dict()
            SuperDiccionario[Carpetas[SelCarpeta]][tipo][N][Cdelta][alfa] = [nombre]
        if N not in SuperDiccionario[Carpetas[SelCarpeta]][tipo].keys():
            SuperDiccionario[Carpetas[SelCarpeta]][tipo][N] = dict()
            SuperDiccionario[Carpetas[SelCarpeta]][tipo][N][Cdelta] = dict()
            SuperDiccionario[Carpetas[SelCarpeta]][tipo][N][Cdelta][alfa] = [nombre]
        elif Cdelta not in SuperDiccionario[Carpetas[SelCarpeta]][tipo][N].keys():
            SuperDiccionario[Carpetas[SelCarpeta]][tipo][N][Cdelta] = dict()
            SuperDiccionario[Carpetas[SelCarpeta]][tipo][N][Cdelta][alfa] = [nombre]
        elif alfa not in SuperDiccionario[Carpetas[SelCarpeta]][tipo][N][Cdelta].keys():
            SuperDiccionario[Carpetas[SelCarpeta]][tipo][N][Cdelta][alfa] = [nombre]
        else:
            SuperDiccionario[Carpetas[SelCarpeta]][tipo][N][Cdelta][alfa].append(nombre)

    
    # Le hice una modificación a esta parte del código, ahora esto trabaja
    # armando el SuperDiccionario también, no sólo los Conjuntos de Alfa, Cdelta
    # y demás. Lo bueno de esto es que ahora el armado del SuperDiccionario
    # es mucho más rápido.

    #--------------------------------------------------------------------------------------------
        
    # Tengo que saber cuántas veces itero los programas para poder saber el tamaño de mis datos de los
    # agentes testigos. Para eso voy a tomar un archivo que tenga agentes testigos y medir el tamaño
    # de mi conjunto de datos y guardarme ese dato. También me armo una lista con los números de
    # los agentes testigos
        
    Datos = ldata("./DilAct/{}/Datos_Opiniones_alfa=0.000_Cdelta=0.00_N=1000_Iter=0".format(Carpetas[SelCarpeta]))
    Iteraciones = len(Datos[9][1::])
    AgentesTestigos = [1,10,50,100,300]
    T=2 # Defino acá el número de tópicos porque es algo que no cambia por ahora,
    # pero no tenía dónde más definirlo
    
    
    #--------------------------------------------------------------------------------------------
        
    # Empiezo iterando el N desde acá porque lo que voy a hacer es que al iniciar
    # la iteración en N, defino mis Conjunto_Alfa y Conjunto_Cdelta en función de
    # las keys de mi SuperDiccionario.
    
    
    for AGENTES in [1000]:
        
        tipo = "Opiniones"
    
        Conjunto_Cdelta = list(SuperDiccionario[Carpetas[SelCarpeta]][tipo][AGENTES].keys())
        Conjunto_Cdelta.sort()
        
        
        Conjunto_Alfa = list(SuperDiccionario[Carpetas[SelCarpeta]][tipo][AGENTES][0].keys())
        Conjunto_Alfa.sort()

        """
        # Me armo los arrays que voy a necesitar para graficar la varianza. Xvar es los valores
        # de alfa para los cuales calculo la varianza. Yvar1 es la varianza del tópico 1,
        # Yvar2 es la varianza del tópico 2, Varvar1 es el valor de Desviación media de la varianza
        # 1 para cada valor de Alfa correspondiente y lo mismo Varvar2 para el tópico 2.
        
        Xvar = np.array(Conjunto_Alfa)
        Yvar1 = np.zeros(len(Conjunto_Alfa))
        Yvar2 = np.zeros(len(Conjunto_Alfa))
        Varvar1 = np.zeros(len(Conjunto_Alfa))
        Varvar2 = np.zeros(len(Conjunto_Alfa))
        """
        
        
        #--------------------------------------------------------------------------------------------
        
#        for CDELTA,icdelta in zip(Conjunto_Cdelta,np.arange(len(Conjunto_Cdelta))):
        for CDELTA in [0]:
            
            for ALFA,ialfa in zip(Conjunto_Alfa,np.arange(len(Conjunto_Alfa))):
#            for ALFA in [0.3]:
            
                #-----------------------------------------------------------------------------------
                
                # Abro mis gráficos, creo listas que voy a llenar con todas las simulaciones y armo algunas cosas varias
                # que voy a necesitar para después
                
                OpinionesFinales = np.array([])
                OpinionesIniciales = np.array([])
                Resultados = list()
                Testigos = dict()
                for i in range(5):
                    Testigos[i] = np.array([])
                
                #-------------------------------------------------------------------------------------
                
                for nombre in SuperDiccionario[Carpetas[SelCarpeta]][tipo][AGENTES][CDELTA][ALFA]:
            
                    #--------------------------------------------------------------------------------------------
                
                    # Levanto los datos del archivo original y separo los datos en tres listas.
                    # Una para la matriz de Adyacencia, una para la matriz de superposición y una para los vectores de opiniones
                
                    Datos = ldata("{}/{}".format(Archivos_Datos[0],nombre))
                
                    # Lista con elementos de los vectores de opinión. Al final sí había una forma compacta de hacer esto.
                    # Si la matriz de Adyacencia evoluciona en el tiempo, va a haber que ver de hacer cambios acá.
                    Opi0 = np.array([float(x) for x in Datos[1][1::]])
                    
                    Var = np.array([float(x) for x in Datos[3][1::]])
                    
                    Opi = np.array([float(x) for x in Datos[5][1::]])
                
                    #----------------------------------------------------------------------------------------------
                    
                    # Voy a mirar en cada una de las iteraciones el estado final y guardarme eso en una lista.
                    
#                    Resultados.append(EstadoFinal(Opi))
                    
                    #------------------------------------------------------------------------------------------------
                    
                    # Armemos los arrays de las Opiniones para los agentes que estoy usando de testigos en el sistema.
                    for i in range(5):
                        Testigos[i] = np.concatenate((Testigos[i],np.array([float(x) for x in Datos[i*2+9][1::]])), axis=None)
                    
                    #------------------------------------------------------------------------------------------------
                    
                    # Además de las opiniones Finales, me voy a guardar un vector con las opiniones inciales
                    # para poder graficar eso también en los Gráficos Opiniones
                    
                    OpinionesIniciales = np.concatenate((OpinionesIniciales,Opi0), axis=None)
                    
                    #-------------------------------------------------------------------------------------------------
                    
                    # Ahora lo que voy a hacer es tomar el estado final del sistema y guardarlo en un array
                    # para después sobre esos datos determinar el estado final del sistema
                    
                    OpinionesFinales = np.concatenate((OpinionesFinales,Opi), axis=None)
                    
                    # Con esto me armo el array de estados finales de mi sistema
                    
                    #-------------------------------------------------------------------------------------------------

    #            Graficar = np.random.choice(int(len(Testigos[0])/Iteraciones),2,False)
                
                """
                # Hago un gráfico de los tópicos de los agentes testigos en función del tiempo. Hago un gráfico
                # para todas las iteraciones de un agente y de un tópico
                
                for repeticion in [1,2]:
                    plt.rcParams.update({'font.size': 24})
                    plt.figure("Topico",figsize=(20,15))
                    X = np.arange(len(Testigos[0][0:Iteraciones:4]))*0.01
                    for sujeto in [1,0,2]:
                        inicio = repeticion*Iteraciones+0
                        final = int(inicio + Iteraciones/2)
#                        if sujeto == 1:
#                            plt.plot(X[::100],Testigos[sujeto][inicio:final:200],linestyle = "", marker = "o", color = "red", markersize = 12, alpha = 0.7)
                        plt.plot(X,Testigos[sujeto][inicio:final:2],linewidth = 4)
    #                    plt.plot(X,Testigos[sujeto][repeticion*Iteraciones+1:(repeticion+1)*Iteraciones+1:2], label="T=1,agente={}".format(AgentesTestigos[sujeto]), linewidth = 4)
                    plt.xlabel("Tiempo")
                    plt.ylabel(r"$x^1$")
#                    plt.ylim(-30,30)
                    plt.xticks(np.arange(0,51,5))
                    plt.grid()
    #                plt.annotate(r"$\alpha$={},cos($\delta$)={},N={}".format(ALFA,CDELTA,AGENTES), xy=(0.5,0.75),xycoords='axes fraction',fontsize=20,bbox=dict(facecolor='White', alpha=0.7))
                    plt.savefig("../Imagenes/RedAct/{}/Topicos_alfa={:.3f}_Cdelta={:.2f}_N={}_iter={}.png".format(Carpetas[SelCarpeta],ALFA,CDELTA,AGENTES,repeticion),bbox_inches = "tight")
                    plt.close("Topico")
                        
        #                plt.rcParams.update({'font.size': 18})
        #                plt.figure("Topico2",figsize=(20,15))
        #                X = np.arange(len(Testigos[0][1:Iteraciones+1:2]))*0.01
        #                for sujeto in range(len(AgentesTestigos)):
        #                    plt.plot(X,Testigos[sujeto][repeticion*Iteraciones+1:(repeticion+1)*Iteraciones+1:2],linewidth = 4)
        #                plt.xlabel("Tiempo")
        #                plt.ylabel("Tópico 2")
        #                plt.grid()
        #                plt.annotate("Agente {}".format(AgentesTestigos[sujeto]), xy=(0.75,0.85),xycoords='axes fraction',fontsize=20,bbox=dict(facecolor='White', alpha=0.7))
        #                plt.annotate(r"$\alpha$={},cos($\delta$)={},N={}".format(ALFA,CDELTA,AGENTES), xy=(0.75,0.75),xycoords='axes fraction',fontsize=20,bbox=dict(facecolor='White', alpha=0.7))
        #                plt.savefig("../Imagenes/RedAct/Topico2_alfa={:.2f}_Cdelta={:.2f}_N={}_iter={}.png".format(ALFA,CDELTA,AGENTES,repeticion),bbox_inches = "tight")
        #                plt.close("Topico2")
                
            
                #---------------------------------------------------------------------------------------------------
                """
                # Voy a acá armar el gráfico de la Variación Promedio del sistema en cada una de las simulaciones.
                # La idea es mostrar que esta oscila en un valor muy por encima del crietrio de corte, y
                # después hacer un zoom mostrando que en los intervalos de tiempo discreto, cuando la red se
                # rearma, la Variación Promedio se dispara y vuelve a lentamente empezar a caer.
                
                plt.rcParams.update({'font.size': 24})
                plt.figure("VarProm",figsize=(20,15))
                X = np.arange(len(Testigos[0][0:Iteraciones:2]))*0.01
                plt.plot(X[0:2000],Var[0:2000], linewidth = 4)
                plt.hlines(y = 0.005, xmin = 0, xmax = 20, color = "red",linewidth = 3)
                plt.xlabel("Tiempo")
                plt.ylabel("Variación Promedio")
                plt.xticks(np.arange(0,21))
                plt.grid()
                plt.savefig("../Imagenes/RedAct/{}/VarProm_alfa={:.3f}_Cdelta={:.2f}_N={}.png".format(Carpetas[SelCarpeta],ALFA,CDELTA,AGENTES),bbox_inches = "tight")
                plt.close("VarProm")
                
            
            
            
            
            #---------------------------------------------------------------------------------------------------
            
            """
            # Voy a guardarme para cada Alfa la fracción de estados finales que llegan
            # al consenso. Al mismo tiempo voy a ir armando el vector de Alfas
            
            
#            Ycons.append(Resultados.count("Consenso")/len(Resultados))
#            Xcons.append(ALFA)
            
            # Hablando con Sebas, decidimos que lo que guarde en Ycons es para cada simulación
            # la fracción de agentes que está debajo del umbral de consenso. Por eso tengo que
            # armar mis vectores de valores más arriba.
            
            
            #-----------------------------------------------------------------------------------------------------------
            
            # Estos son los parámetros que definen el tamaño del gráfico, tamaño de la letra y nombres de
            # los ejes. Luego de eso guardo la figura y la cierro. Esto es para la figura de
            # TdO.
            
            # Este gráfico me coloca los puntos finales de las opiniones con colores y me 
            # pone un cartelito marcando cuál es el estado final del sistema. Voy a agregar
            # que se dibuje un círculo marcando la región donde se encuentran la mayoría de
            # las opiniones incialmente, puntos negros para las opiniones iniciales y agregar
            # el hecho de que los límites de los gráficos tienen que ser entre -30 y 30
            
            # Armo los valores X e Y que me dibujan el círculo
#            Tita = np.linspace(0,2*math.pi,1000)
#            Xcirc = 2*math.sqrt(2.5)*np.cos(Tita)
#            Ycirc = 2*math.sqrt(2.5)*np.sin(Tita)
#            
#            
#            for repeticion in Graficar:
#                plt.rcParams.update({'font.size': 18})
#                plt.figure("Grafico Opiniones",figsize=(20,15))
#                
#                # Grafico los puntos iniciales de las opiniones
#                for x1,x2 in zip (OpinionesIniciales[repeticion*len(Opi)+0:(repeticion+1)*len(Opi)+0:2],OpinionesIniciales[repeticion*len(Opi)+1:(repeticion+1)*len(Opi)+1:2]):
#                    plt.plot(x1,x2, "o" ,c = "black", markersize=5, alpha = 0.5)
#                
#                # Grafico los puntos finales de las opiniones
#                for x1,x2 in zip (OpinionesFinales[repeticion*len(Opi)+0:(repeticion+1)*len(Opi)+0:2],OpinionesFinales[repeticion*len(Opi)+1:(repeticion+1)*len(Opi)+1:2]):
#                    indice = Indice_Color(np.array([x1,x2]),Divisiones)
#                    plt.plot(x1,x2, "o" ,c = color[indice], markersize=10)
#                
#                # Grafico el círculo en distancia 2 sigma del cero
#                plt.plot(Xcirc,Ycirc,"--",linewidth=5,alpha=0.6)
#                
#                #            plt.tick_params(left=False,
#                #                bottom=False,
#                #                labelleft=False,
#                #                labelbottom=False)
#                plt.xlabel("Tópico 1")
#                plt.ylabel("Tópico 2")
#                plt.xlim(-30,30)
#                plt.ylim(-30,30)
#    #                    #            plt.title(r"Trayectoria de las opiniones en el espacio de tópicos para $\alpha$={},cos($\delta$)={} y N={}".format(ALFA,CDELTA,AGENTES))
#    ##                    plt.xlim((xmin,xmax))
#    ##                    plt.ylim((ymin,ymax))
#                plt.annotate("{}".format(EstadoFinal(OpinionesFinales[repeticion*len(Opi):(repeticion+1)*len(Opi)])), xy=(0.45,0.9),xycoords='axes fraction',fontsize=20,bbox=dict(facecolor='White', alpha=0.7))
#                plt.annotate(r"$\alpha$={},cos($\delta$)={},N={},iter={}".format(ALFA,CDELTA,AGENTES,repeticion), xy=(0.7,0.85),xycoords='axes fraction',fontsize=20,bbox=dict(facecolor='White', alpha=0.7))
#                plt.savefig("../Imagenes/RedAct/{}/Grafico_opiniones_alfa={:.3f}_Cdelta={:.2f}_N={}_iter={}.png".format(Carpetas[SelCarpeta],ALFA,CDELTA,AGENTES,repeticion),bbox_inches = "tight")
#                plt.close("Grafico Opiniones")

            #------------------------------------------------------------------------------------------------
                
            # Acá me voy a armar los gráficos de las trayectorias de Opiniones de los agentes Testigos.
    #        
    #        if len(Testigos[0]>0):
    #            for sujeto in range(len(AgentesTestigos)):
    #                plt.rcParams.update({'font.size': 18})
    #                plt.figure("TdO",figsize=(20,15))
    #                for repeticion in range(int(len(Testigos[sujeto])/Iteraciones)):
    #                    plt.plot(Testigos[sujeto][repeticion*Iteraciones+0:(repeticion+1)*Iteraciones+0:2],Testigos[sujeto][repeticion*Iteraciones+1:(repeticion+1)*Iteraciones+1:2], color="gray",linewidth = 1, alpha=0.5)
    #                    indice = Indice_Color(np.array([Testigos[sujeto][(repeticion+1)*Iteraciones-2],Testigos[sujeto][(repeticion+1)*Iteraciones-1]]),Divisiones)
    #                    plt.plot(Testigos[sujeto][(repeticion+1)*Iteraciones-2],Testigos[sujeto][(repeticion+1)*Iteraciones-1], "o" ,c = color[indice], markersize=10)
    #                plt.xlabel("Tópico 1")
    #                plt.ylabel("Tópico 2")
    #                plt.annotate("Agente {}".format(AgentesTestigos[sujeto]), xy=(0.75,0.85),xycoords='axes fraction',fontsize=20,bbox=dict(facecolor='White', alpha=0.7))
    #                plt.annotate(r"$\alpha$={},cos($\delta$)={},N={}".format(ALFA,CDELTA,AGENTES), xy=(0.75,0.75),xycoords='axes fraction',fontsize=20,bbox=dict(facecolor='White', alpha=0.7))
    #                plt.savefig("../Imagenes/RedAct/{}/TdO_alfa={:.2f}_Cdelta={:.2f}_N={}_testigo={}.png".format(Carpetas[SelCarpeta],ALFA,CDELTA,AGENTES,AgentesTestigos[sujeto]),bbox_inches = "tight")
    #                plt.close("TdO")
            
            #----------------------------------------------------------------------------------------------------------
            # Para graficar los valores de la Varianza en función de Alfa necesito primero aprovechar el for del Alfa
            # y armar mis datos al respecto.
            
            # Armo los arrays que me guardan los valores de varianza de todas las simulaciones
            # y con eso me voy a guardar los valores promedios
            Var1 = np.zeros(int(len(SuperDiccionario[AGENTES][ALFA][CDELTA])/2))
            Var2 = np.zeros(int(len(SuperDiccionario[AGENTES][ALFA][CDELTA])/2))
            
            for repeticion in np.arange(int(len(SuperDiccionario[AGENTES][ALFA][CDELTA])/2)):
                Var1[repeticion] = np.var(OpinionesFinales[repeticion*len(Opi)+0:(repeticion+1)*len(Opi)+0:2])
                Var2[repeticion] = np.var(OpinionesFinales[repeticion*len(Opi)+1:(repeticion+1)*len(Opi)+1:2])
            
            Yvar1[ialfa] = np.mean(Var1)
            Varvar1[ialfa] = math.sqrt(np.var(Var1))
            Yvar2[ialfa] = np.mean(Var2)
            Varvar2[ialfa] = math.sqrt(np.var(Var2))
            
            # Con esto me armé los datos que voy a graficar de la varianza. Ahora sólo tengo que hacer el gráfico.
            
            #----------------------------------------------------------------------------------------------------------
            
        #---------------------------------------------------------------------------------------------------
        
        # Acá armo los gráficos de Varianza en función de Alfa.
        
        plt.rcParams.update({'font.size': 18})
        plt.figure("Varianza Opiniones",figsize=(20,15))
        
        # Ahora grafico las curvas de Varianza de ambos tópicos
        plt.errorbar(Xvar,Yvar1,yerr=Varvar1,fmt="-o",label="Topico 1",linewidth = 4,markersize=10,elinewidth=3,ecolor="black",capsize=5)
        plt.errorbar(Xvar,Yvar2,yerr=Varvar2,fmt="-o",label="Topico 2",linewidth = 4,markersize=10,elinewidth=3,ecolor="black",capsize=5)
        plt.xlabel("Alfa")
        plt.ylabel("Varianza")
        plt.title("Datos {}, Varianza vs Alfa".format(Carpetas[SelCarpeta]))
        plt.legend()
        plt.grid()
        plt.savefig("../Imagenes/RedAct/{}/Varianza_opiniones_Cdelta={:.2f}_N={}.png".format(Carpetas[SelCarpeta],CDELTA,AGENTES),bbox_inches = "tight")
        plt.close("Varianza Opiniones")


#---------------------------------------------------------------------------------------------------------
# Voy a separar el armado del gráfico de Consenso Vs Alfa de forma de
# poder armar varios gráficos variando el umbral de detección del consenso entre
# 2 sigmas y 0.5 sigmas supongo

Carpetas = ["Actividad Reversion","Regact","HomofiliaCero","TiempoExtra","RCC"]
#SelCarpeta = 1
for SelCarpeta in [3]:  #range(1,len(Carpetas)):
    
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
    # a un cierto N, Alfa, Cdelta y Gm. Me armo primero el superdiccionario, que es el diccionario,
    # que contiene diccionarios, que llevan a diccionarios que lleva a diccionarios
    # que lleva a diccionarios que llevan a las listas de los nombres
    # de los archivos, donde los ingresos a los diccionarios son el número de Agentes, el Alfa,
    # el Cdelta, el tipo de red y el Gm respectivos. 
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
    
    #--------------------------------------------------------------------------------------------
    plt.rcParams.update({'font.size': 24})
    plt.figure("Consenso vs alfa",figsize=(20,12))

    for umbral in range(1,5):
        for AGENTES in [1000]:
        
            Conjunto_Alfa = list(SuperDiccionario[AGENTES].keys())
        
            Conjunto_Cdelta = list(SuperDiccionario[AGENTES][Conjunto_Alfa[0]].keys())[0]
    
            Ycons = []
            Xcons = []
            
            for ALFA,ialfa in zip(Conjunto_Alfa,np.arange(len(Conjunto_Alfa))):
                
                CDELTA = 0
                icdelta = 0
                
        #        for CDELTA,icdelta in zip(Conjunto_Cdelta,np.arange(len(Conjunto_Cdelta))):
    
                #-------------------------------------------------------------------------------------
                for nombre in SuperDiccionario[AGENTES][ALFA][CDELTA]:
                    if nombre.split("_")[1] == "Opiniones":
            
                        #--------------------------------------------------------------------------------------------
                    
                        # Levanto los datos del archivo original y separo los datos en tres listas.
                        # Una para la matriz de Adyacencia, una para la matriz de superposición y una para los vectores de opiniones
                    
                        Datos = ldata("{}/{}".format(Archivos_Datos[0],nombre))
                        
                        # Array con los valores de opiniones finales del sistema
                        Opi = np.array([float(x) for x in Datos[5][1::]])
                        
                        # Voy a armar acá los vectores a graficar para ver el Consenso versus Alfa.
                        
                        Xcons.append(ALFA)
                        ArrayAbs = np.absolute(Opi)
                        Comprobacion = np.sqrt(ArrayAbs[0::2]*ArrayAbs[0::2] + ArrayAbs[1::2]*ArrayAbs[1::2])
                        Ycons.append(np.count_nonzero(Comprobacion < (umbral/2)*math.sqrt(2.5))/len(Comprobacion))
            
            # -------------------------------------------------------------------------------------------------
            
            # Como estoy barriendo en un único coseno Delta, el Gráfico de estados finales en el espacio de parámetros
            # no estaría pudiendo hacerse corréctamente. Así que ahora mejor veo de graficar la cantidad de estados
            # finales de consenso en función del Alfa.
            
            plt.plot(Xcons,Ycons,"o",markersize = 16-3*umbral) # , label=r"umbral = {}$\sigma$".format((umbral/2)))
    
    plt.vlines(AlfaC(0,0.817),0,1,colors="red",linewidth = 3, label="Alfa Critico")
    plt.xlabel(r"$\alpha$")
    plt.ylabel("Fraccion de agentes")
#    plt.title("Fraccion de agentes en consenso en funcion de Alfa, Datos {}".format(Carpetas[SelCarpeta]))
    plt.grid()
    plt.savefig("../Imagenes/RedAct/{}/CvA.png".format(Carpetas[SelCarpeta]), bbox_inches = "tight")
    plt.close("Consenso vs alfa")
    
    
    # Voy a colocar acá el gráfico de la distribución de las opiniones porque no me gusta mucho eso de tener un gráfico abierto
    # durante el proceso de TOOODAS las otras cosas.
    
    for AGENTES in [1000]:
    
        Conjunto_Alfa = list(SuperDiccionario[AGENTES].keys())
    
        Conjunto_Cdelta = list(SuperDiccionario[AGENTES][Conjunto_Alfa[0]].keys())[0]
        
        # Abro acá el archivo de Distribucion de opiniones. La idea es armar un gráfico sólo
        # con las distribuciones de 10 alfas.
        
        for TOPICO in range(0,2):
        
            plt.rcParams.update({'font.size': 18})
            
            plt.figure("Distribucion Opiniones",figsize=(20,15))
            
            # Defino los alfas que voy a usar en el gráfico de Distribución de Opiniones
            
            Alfas_Dist = [Conjunto_Alfa[int(indice*math.floor(len(Conjunto_Alfa)/10))] for indice in range(0,10)]
    
            
            for ALFA,ialfa in zip(Alfas_Dist,np.arange(len(Alfas_Dist))):
                
                CDELTA = 0
                icdelta = 0
                
                OpinionesFinales = np.array([])
                
        #        for CDELTA,icdelta in zip(Conjunto_Cdelta,np.arange(len(Conjunto_Cdelta))):
    
                #-------------------------------------------------------------------------------------
                for nombre in SuperDiccionario[AGENTES][ALFA][CDELTA]:
                    if nombre.split("_")[1] == "Opiniones":
            
                        #--------------------------------------------------------------------------------------------
                    
                        # Levanto los datos del archivo original y separo los datos en tres listas.
                        # Una para la matriz de Adyacencia, una para la matriz de superposición y una para los vectores de opiniones
                    
                        Datos = ldata("{}/{}".format(Archivos_Datos[0],nombre))
                        
                        # Array con los valores de opiniones finales del sistema
                        Opi = np.array([float(x) for x in Datos[5][1::]])
                        
                        #-------------------------------------------------------------------------------------------------
                        
                        # Ahora lo que voy a hacer es tomar el estado final del sistema y guardarlo en un array
                        # para después sobre esos datos determinar el estado final del sistema
                        
                        OpinionesFinales = np.concatenate((OpinionesFinales,Opi), axis=None)
                        
                        # Con esto me armo el array de estados finales de mi sistema
                        
            
            # -------------------------------------------------------------------------------------------------
                
                # Acá voy a armar los gráficos de las proyecciones de las opiniones de los agentes. Para eso simplemente
                # voy a tomar los valores de opiniones de los agentes de una simulación, calcularle el histograma
                # con np.histogram y luego graficar eso como líneas.
                
                
                # Armo los histogramas correspondientes
                Histo,Bins = np.histogram(OpinionesFinales[TOPICO::2],bins=100)
                
                # Ahora grafico las curvas de distribución de ambas opiniones
                plt.plot((Bins[0:len(Bins)-1]+Bins[1::])/2,Histo,"-o",linewidth = 4,markersize = 8, label="Alfa = {}".format(ALFA))
            
            
            plt.xlabel("Opinion")
            plt.ylabel("Cuentas")
            plt.xlim(-5,5)
            plt.title(r"Datos {}, Distribucion Topico {}, Cos($\delta$)=0".format(Carpetas[SelCarpeta],TOPICO))
            plt.legend()
            plt.grid()
            
            plt.savefig("../Imagenes/RedAct/{}/Distribucion_opiniones_T={}_Cdelta={:.2f}_N={}.png".format(Carpetas[SelCarpeta],TOPICO,CDELTA,AGENTES),bbox_inches = "tight")
            plt.close("Distribucion Opiniones")
                
            #--------------------------------------------------------------------------------------------------------
            """






Tiempo()

