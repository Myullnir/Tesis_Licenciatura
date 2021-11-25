# -*- coding: utf-8 -*-
"""
Created on Mon Jun 21 20:38:02 2021

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
    
    if Pcero > 1.1*Pmenos and Pcero > 1.1*Pmas:
        return "Consenso"
    
    ###########################################################################
    
    # Ahora veamos el caso de región de transición. Este estado
    # Lo caracterizo porque el sistema tiene un pico central y picos por fuera
    # que son comparables.
    
    Pmaximo = max(Pcero,Pmas,Pmenos)
    
    if Pmaximo*0.9 < Pcero < Pmaximo*1.1 and Pmaximo*0.9 < Pmas < Pmaximo*1.1 and Pmaximo*0.9 < Pmenos < Pmaximo*1.1 :
        return "RegionTrans"
    
    ###########################################################################
    
#    indicemenos = np.where(DistNegativa == Pmenos)[0][0]
#    indicemas = np.where(DistPositiva == Pmas)[0][0]
    
    if Pcero == min(Pcero,Pmas,Pmenos) and Pcero < Pmaximo*0.9:
        
        # Ahora veamos los otros dos casos. Primero voy a armar
        # un array que tenga las opiniones del tópico 1, y otro
        # con las opiniones del tópico 2.
        
        ArrayCuad = ClasificacionCuadrantes(Array)
        
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
    
    return "NoDefinido"



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
SuperDiccionario = dict()

T=2 # Defino acá el número de tópicos porque es algo que no cambia por ahora,
# pero no tenía dónde más definirlo

for REDES in ["Erdos-Renyi"]:


    # Este parámetro llamado Subdividido es algo que defino yo a mano para definir si estoy leyendo una 
    # carpeta donde los archivos de datos están divididos en 4 carpetas, o si están todos mezclados en
    # la carpeta. Empecé a hacer esto de dividirlos porque Pablo me dijo que era necesario.
    Subdividido = True
    
    # Primero levanto datos de los nombres de los archivos de mis redes. Para eso es importante notar
    # que mis archivos ahora van a empezar a tener cuatro carpetas donde los valores de GM estén
    # diferenciados. Para eso necesita que el programa distinga cuántas carpetas hay en la carpeta
    # principal y que me arme la lista de archivos dentro de cada carpeta. Voy a armar un segundo código
    # pensado en levantar los archivos de las carpetas que tienen los archivos separados en 4 carpetas
    # según GM. Luego activo el código en función de la carpeta de la cual voy a levantar datos.
    
    # CÓDIGO PARA LEVANTAR DATOS DE UNA CARPETA SUBDIVIDIDA EN 4 CARPETAS SEGÚN EL GM DE LOS ARCHIVOS.
    
    if Subdividido == True:
    
        CarpCheck=[[root,dirs,files] for root,dirs,files in os.walk("../NCC/{}".format(REDES))]
        
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
        
        CarpCheck=[[root,files] for root,dirs,files in os.walk("../NCC/{}".format(REDES))]
        
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
            
            Conjunto_Alfa = list(SuperDiccionario[REDES][AGENTES][GM].keys())
            Conjunto_Cdelta = list(SuperDiccionario[REDES][AGENTES][GM][Conjunto_Alfa[0]].keys())
            
            Conjunto_Cdelta.sort()
            
            # Primero me armo los grid para el gráfico de las fases. Para eso
            # primero tengo que armarme un array y con el np.meshgrid armarme 
            # los grids del pcolormesh.
            
            Conjunto_Alfa.reverse() # Lo invierto para que me quede el uno arriba y no abajo
            
            x = np.array(Conjunto_Cdelta)
            y = np.array(Conjunto_Alfa)
            
            Conjunto_Alfa.reverse() # Lo vuelvo a invertir para que de nuevo esté como siempre.
            
            XX,YY = np.meshgrid(x,y)
            
            ZZV = np.zeros(XX.shape) # Esta es la matriz de valores para la varianza
            ZZP = np.zeros(XX.shape) # Esta es la matriz de valores para los valores de opiniones máximas
            ZZE = np.zeros(XX.shape) # Esta es la matriz con valores de entropía para las distribuciones por cuadrantes
            # Con esto ya tengo armados los grids de XX,YY y de paso me armo el grid
            # del ZZ para ir rellenándolo a medida que corro todo el programa, o usando
            # los datos que ya guardé de antes. Para eso es el módulo siguiente
            
            #---------------------------------------------------------------------------------------------

            # Voy a iterar esto para todos los archivos de datos que tengo
            
            for ALFA,ialfa in zip(Conjunto_Alfa,np.arange(len(Conjunto_Alfa))):
                
#                fig = plt.figure("Distribucion por cuadrantes", figsize=(20,12))
#                Xhisto = np.arange(5)
#                Fondo = np.zeros(5)
#                plt.rcParams.update({'font.size': 18})
#                plt.figure("Distribucion de Valores", figsize=(20,12))
                
                for CDELTA,icdelta in zip(Conjunto_Cdelta,np.arange(len(Conjunto_Cdelta))):
                
                    #-----------------------------------------------------------------------------------
                    
                    # Abro mis gráficos, creo listas que voy a llenar con todas las simulaciones y armo algunas cosas varias
                    # que voy a necesitar para después
                    
                    # Creo el array TideSi, la cual voy a usar para guardar un nuevo valor en la matriz ZZV
                    # para cada combinación de Alfas y Cdelta
                    # Creo el array Maximos 
                    
                    
                    TideSi = np.zeros(len(SuperDiccionario[REDES][AGENTES][GM][ALFA][CDELTA]))
                    Promedios = np.zeros(len(SuperDiccionario[REDES][AGENTES][GM][ALFA][CDELTA]))
#                    plt.rcParams.update({'font.size': 18})
#                    plt.figure("Variaciones Promedio",figsize=(20,12))
                    OpinionesFinales = np.array([])
                    Colores2 = cm.rainbow(np.linspace(0,1,len(SuperDiccionario[REDES][AGENTES][GM][ALFA][CDELTA])))
                    
                    #-------------------------------------------------------------------------------------
                    
                    for nombre,numero in zip (SuperDiccionario[REDES][AGENTES][GM][ALFA][CDELTA],np.arange(len(SuperDiccionario[REDES][AGENTES][GM][ALFA][CDELTA]))):
    
                        #--------------------------------------------------------------------------------------------
                    
                        # Tengo que hacer una diferenciación entre levantar datos de las carpetas subdividida en 4 y de la carpeta con todo mezclado.
                        
                        if Subdividido == True:
                            #PARA LEVANTAR DATOS DE LA CARPETA SUBDIVIDIDA EN 4
                            Datos = ldata("{}/{}".format(Conjunto_Direcciones[igm],nombre))
                            
                        else:
                            # PARA LEVANTAR DATOS DE LA CARPETA TODA MEZCLADA
                            Datos = ldata("../{}/{}".format(Conjunto_Direcciones[0],nombre))
                        
                        # Lista con elementos de los vectores de opinión. Al final sí había una forma compacta de hacer esto.
                        # Si la matriz de Adyacencia evoluciona en el tiempo, va a haber que ver de hacer cambios acá.
                        
                        Opi0 = np.array([float(x) for x in Datos[1][1::]])
                        
                        Var = np.array([float(x) for x in Datos[3][1::]])
                        
                        Opi = np.array([float(x) for x in Datos[5][1::]])
                        
                        #-----------------------------------------------------------------------------------------------
                        """
                        # Para algunos valores de dt me ocurre que el sistema llega a valores de variación cero muy rápido.
                        # Eso en el gráfico de logaritmo lo único que hace es incluir muchos valores del eje x en los
                        # cuales no hay nada graficado. Comprimiendo de manera artificial mi gráfico a la izquierda, y 
                        # dificultando por tanto su lectura. Por ello es que al Var le voy a cortar todo valor que tenga
                        # a partir de que uno de sus valores se haga cero
        
                        X = np.arange(0,len(Var))*0.1 # El dt usado en todos los archivos es 0.1
                        
                        plt.semilogy(X,Var, "--", linewidth = 3,c = Colores2[numero])
        
                        # El programa sigue funcionando bárbaro, lo cual es buenísimo. Corta en el momento
                        # adecuado y el comportamiento es razonbale. El guardado y el cerrado de la figura
                        # lo dejo para el final del for de nombres. El tema de eso es que entonces
                        # tengo que iniciar el siguiente gráfico antes de cerrar este. Eso no es un problema
                        # para el código o de hacer, es sólo un tema de que dificulta un poquito más la modularidad
                        # del código porque ahora las cosas se mezclan y el cierre de este módulo está al final
                        """
                        #----------------------------------------------------------------------------------------------

                        # Voy a ir armando mi array con los valores de Tiempo de Simulación.
                        # Lo voy a llamar TideSi
                        
                        TideSi[numero] = Var.shape[0]*0.01 # 0,1 es el paso temporal dt
                        
                        # Esto debería funcionar derechito.
                        
                        #------------------------------------------------------------------------------------------------
                
                        # Quiero hacer un estudio de cómo varía el máximo al cual llega el sistema en función del
                        # cos(delta) y alfa. La idea es mirar las opiniones finales, promediar los máximos en
                        # las simulaciones realizadas y desde ahí asignar ese valor a cada punto del colormap.
                        
                        Promedios[numero] = np.mean((np.abs(Opi)))
                        
                        # Esto me guarda en cada posición del array el máximo de las opiniones finales alcanzadas
                        # en cada simulación
                        
                        #----------------------------------------------------------------------------------------------
                        
                        # Ahora lo que voy a hacer es tomar el estado final del sistema y guardarlo en un array
                        # para después sobre esos datos determinar el estado final del sistema
                        
                        OpinionesFinales = np.concatenate((OpinionesFinales,Opi), axis=None)
                        
                        # Con esto me armo el array de estados finales de mi sistema
                        
                    #------------------------------------------------------------------------------------------------
                    # Acá lo que voy a hacer es rellenar el grid de ZZV con los valores de los resultados de
                    # opiniones finales. Vamos a modificar esto porque la Varianza resulta muy sensible ante
                    # outliers. Vamos a tomar la mediana de los tiempos de simulación y con eso ver si obtenemos
                    # un gráfico más claro de cómo surgen las regiones de transición entre consenso y polarización
                    # a partir de la variación en los Tiempos de Simulación.
                    
                    Cuantiles = np.quantile(TideSi,[0.05,0.95])
                   
                    ZZV[len(Conjunto_Alfa)-1-ialfa, icdelta] = np.log10(Cuantiles[1]-Cuantiles[0]+1)
                    
                    # Esto ya debería correctamente armarme el ZZV ubicando para cada par de valores
                    # alfa y cos(delta) la diferencia entre el valor que define el cuantil de 0,05 y el de 0,95.
                    # Lo siguiente es tomar eso al final y graficarlo.
                        
                    #-------------------------------------------------------------------------------------------------
                    
                    # Acá lo que voy a hacer es rellenar el grid de ZZP con los valores de los maximos promedios
                    # de las opiniones finales
                
                    ZZP[len(Conjunto_Alfa)-1-ialfa, icdelta] = np.mean(Promedios)
                    
                    # Esto ya debería correctamente armarme el ZZM ubicando para cada par de valores
                    # alfa y cos(delta) su respectivo valor máximo. Lo siguiente es tomar eso al final y graficarlo.
                        
                    #-------------------------------------------------------------------------------------------------

                    # Ok, esto me confundió mucho en un principio. La idea es que uso ClasificaciónCuadrantes para
                    # armar el array que tenga los números de los cuadrantes en los que se encuentran las opiniones.
                    # Defino los bins a mano, total sé que distribuyo mis opiniones en los cuadrantes del 1 al 4, y
                    # el 0 es para aquellos en los que están muy cerca del cero.
                    
#                    plt.figure("Distribucion por cuadrantes")
    
                    Cuadrantes = ClasificacionCuadrantes(OpinionesFinales)
                    Bins = [-0.5,0.5,1.5,2.5,3.5,4.5]
                    
                    # Calculo la distribución. Del np.histogram obtengo dos arrays, el primero es el histograma
                    # y el segundo es los bins. Para evitar problemas, mando eso a la nada misma y listo.
                    
                    [Yhisto,nada] = np.histogram(Cuadrantes, bins = Bins)
                    
                    # Esto lo saqué del manual de uso. Simplemente grafica en el sistema de ejes del subplot
                    # el gráfico de barras y se encarga de tomar siempre como piso el anterior gráfico de barras
                    # de manera de ir stackeando las barras. Eso me va a permitir mostrar variso gráficos 
                    # juntos y con eso recorrer varios alfas.
                    
#                    plt.bar(Xhisto, Yhisto, 0.5, bottom = Fondo, label = r"cos($\delta$) = {}".format(CDELTA))
#                    Fondo = Fondo+Yhisto
                    
                    #---------------------------------------------------------------------------------------------------
                    
#                    Voy a aprovechar la cuenta hecha para distribucion por Cuadrantes para ir calculando la Entropía.
#                    A fin de cuentas, la entropía va a estar vista en función de la distribución de las opiniones en
#                    los cuadrantes. De paso, Seba me dijo que ignore el tema de las opiniones que se van a cero.
#                    Son muy pocas en general, así que no importan mucho, ¿Pero debería simplemente ignorarlas?
#                    Definitivamente son despreciables, dale para adelante.
                    
                    Probabilidades = Yhisto[Yhisto != 0]/np.sum(Yhisto)
                    ZZE[len(Conjunto_Alfa)-1-ialfa, icdelta] = np.matmul(Probabilidades, np.log2(Probabilidades))*(-1)
                
                #---------------------------------------------------------------------------------------------------
                
                # Esto me guarda el gráfico de variaciones Promedio
        #            plt.tick_params(left=False,
        #                bottom=False,
        #                labelleft=False,
        #                labelbottom=False)
#                    plt.figure("Variaciones Promedio")
#                    plt.xlabel("Tiempo Simulado")
#                    plt.ylabel("Variación promedio de las opiniones")
#                    plt.axis("tight")
#                    plt.title(r"Variación Promedio del sistema para $\alpha$={}_cos($\delta$)={}_N={}".format(ALFA,CDELTA,AGENTES))
#                    plt.annotate(r"$\alpha$={},cos($\delta$)={},N={}".format(ALFA,CDELTA,AGENTES), xy=(0.75,0.85),xycoords='axes fraction',fontsize=20,bbox=dict(facecolor='White', alpha=0.7))
#                    plt.annotate("Red={}, Gm={}".format(REDES,GM), xy=(0.75,0.75),xycoords='axes fraction',fontsize=20,bbox=dict(facecolor='White', alpha=0.7))
#                    plt.grid()
#                    plt.savefig("../../../Imagenes/Redes Estáticas/{}/GM={}/Variaciones Promedio_Gm={}_alfa={:.2f}_Cdelta={}_N={}.png".format(REDES,GM,GM,AGENTES,ALFA,CDELTA,AGENTES),bbox_inches = "tight")
#                    plt.close("Variaciones Promedio")
                    
                    #-------------------------------------------------------------------------------------------------
                    """
                    # Puedo armar acá el gráfico de distribución de valores. Además, para esto puedo usar una lista que
                    # ya armé antes que es la de Opiniones Finales. A partir de esta voy a hacer las distribuciones del
                    # Tópico 1 y del 2 y eso voy a graficar. Las distribuciones las voy a calcular con el np.histogram.
                    # Como tengo 100 agentes y 40 simulaciones, entonces tengo 4000 opiniones para cada tópico. Me parece
                    # razonable separar esto en 40 bins.
                    
                    Histo,Bordes_Bin = np.histogram(OpinionesFinales,bins=80)
                    
                    EjeX = (Bordes_Bin[1::]-Bordes_Bin[0:len(Bordes_Bin)-1])/2
                    
                    plt.figure("Distribucion de Valores")
                    plt.plot(EjeX,Histo,"--",linewidth = 3, label = r"$cos(\delta)$ = {}".format(CDELTA))
            
            
                plt.xlabel("Valores de Opiniones")
                plt.ylabel("Ocurrencias")
                plt.title(r"Distribucion de las opiniones para  N={}, Gm={} $\alpha$={:.2f}".format(AGENTES,GM,ALFA))
                plt.legend()
                plt.grid()
                plt.savefig("../../../Imagenes/Redes Estáticas/{}/GM={}/Distribución opiniones_N={}_alfa={:.2f}_GM={}.png".format(REDES,GM,AGENTES,ALFA,GM),bbox_inches = "tight")
                plt.close("Distribucion de Valores")
                """
                #-----------------------------------------------------------------------------------------------------------
                

#                plt.figure("Distribucion por cuadrantes")
#                plt.grid()
#                plt.rcParams.update({'font.size': 18})
#                plt.ylabel("Ocurrencias")
#                plt.xlabel("Cuadrantes")
#                plt.title(r"Distribución de opiniones en cuadrantes, $\alpha$ = {}".format(ALFA))
#                plt.annotate("Red={}, Gm={}".format(REDES,GM), xy=(0.5,0.85),xycoords='axes fraction',fontsize=20,bbox=dict(facecolor='White', alpha=0.7))
#                plt.legend()
#                plt.savefig("../../../Imagenes/Redes Estáticas/{}/GM={}/Distribucion Cuadrantes Alfa={}.png".format(REDES,GM,ALFA), bbox_inches = "tight")
#                plt.close("Distribucion por cuadrantes")
            #         plt.show()
            
            #------------------------------------------------------------------------------------------------------------
    
            
            # Acá termino mi gráfico de Fases, una vez que recorrí todos los Alfa y Cdelta.
        
            # Defino los parámetros usuales de mi gráfico
        
            plt.rcParams.update({'font.size': 18})
            plt.figure("Cuantil TideSi",figsize=(20,12))
            plt.xlabel(r"cos($\delta$)")
            plt.ylabel(r"$\alpha$")
            plt.title("Amplitud del Tiempo de Simulación en el espacio de parámetros")
        
            # Grafico la línea del Alfa Crítico teórico
        
            Xa = np.arange(min(Conjunto_Cdelta),max(Conjunto_Cdelta),0.002)
            Ya = np.array([AlfaC(x,GM) for x in Xa])
            plt.plot(Xa,Ya,"--",color = "red",linewidth = 5, label = r"$\alpha_c$ teórico")
        
            # Hago el ploteo del mapa de colores con el colormesh y usando el mapa de colroes creado por mi.
        
            plt.legend()
            plt.pcolormesh(XX,YY,ZZV,shading="nearest", cmap = "plasma")
            plt.colorbar()
            plt.annotate("Red={}, Gm={}".format(REDES,GM), xy=(0.6,0.85),xycoords='axes fraction',fontsize=20,bbox=dict(facecolor='White', alpha=0.7))
            plt.savefig("../../../Imagenes/Redes Estáticas/NCC/{}/GM={}/Cuantil EP.png".format(REDES,GM), bbox_inches = "tight")
            plt.close("Cuantil TideSi")
        #     plt.show()
        
            #---------------------------------------------------------------------------------------------------
            
            # Acá termino mi gráfico de Fases, una vez que recorrí todos los Alfa y Cdelta.
        
            # Defino los parámetros usuales de mi gráfico
        
            plt.rcParams.update({'font.size': 18})
            plt.figure("Promedios EP",figsize=(20,12))
            plt.xlabel(r"cos($\delta$)")
            plt.ylabel(r"$\alpha$")
            plt.title("Promedios de Opiniones en el Espacio de Parámetros")
        #
        #    # Grafico la línea del Alfa Crítico teórico
        #
            Xa = np.arange(min(Conjunto_Cdelta)+0.1,max(Conjunto_Cdelta)-0.1,0.002)
            Ya = np.array([AlfaC(x,GM) for x in Xa])
            plt.plot(Xa,Ya,"--",color = "red",linewidth = 5, label = r"$\alpha_c$ teórico")
        #
        #    # Hago el ploteo del mapa de colores con el colormesh y usando el mapa de colores creado por mi.
        #
            plt.legend()
            plt.pcolormesh(XX,YY,ZZP,shading="nearest", cmap = "viridis")
            plt.colorbar()
            plt.annotate("Red={}, Gm={}".format(REDES,GM), xy=(0.6,0.85),xycoords='axes fraction',fontsize=20,bbox=dict(facecolor='White', alpha=0.7))
            plt.savefig("../../../Imagenes/Redes Estáticas/NCC/{}/GM={}/Promedios EP.png".format(REDES,GM), bbox_inches = "tight")
            plt.close("Promedios EP")
        #     plt.show()
        
            #---------------------------------------------------------------------------------------------------
            
            # Acá termino mi gráfico de Fases, una vez que recorrí todos los Alfa y Cdelta.
        
            # Defino los parámetros usuales de mi gráfico
        
            plt.rcParams.update({'font.size': 18})
            plt.figure("Entropia EP",figsize=(20,12))
            plt.xlabel(r"cos($\delta$)")
            plt.ylabel(r"$\alpha$")
            plt.title("Entropía de las Distribuciones en el Espacio de Parámetros")
        #
        #    # Grafico la línea del Alfa Crítico teórico
        
            Xa = np.arange(min(Conjunto_Cdelta)+0.1,max(Conjunto_Cdelta)-0.1,0.002)
            Ya = np.array([AlfaC(x,GM) for x in Xa])
            plt.plot(Xa,Ya,"--",color = "red",linewidth = 4, label = r"$\alpha_c$ teórico")
        #
        #    # Hago el ploteo del mapa de colores con el colormesh y usando el mapa de colores creado por mi.
        #
            plt.legend()
            plt.pcolormesh(XX,YY,ZZE,shading="nearest", cmap = "viridis")
            plt.colorbar()
            plt.annotate("Red={}, Gm={}".format(REDES,GM), xy=(0.6,0.85),xycoords='axes fraction',fontsize=20,bbox=dict(facecolor='White', alpha=0.7))
            plt.savefig("../../../Imagenes/Redes Estáticas/NCC/{}/GM={}/Entropía EP.png".format(REDES,GM), bbox_inches = "tight")
            plt.close("Entropia EP")
        #     plt.show()
        
            #---------------------------------------------------------------------------------------------------

                    


    
    
Tiempo()