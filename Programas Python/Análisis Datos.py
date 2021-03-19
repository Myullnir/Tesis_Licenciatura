
# coding: utf-8

# In[1]:


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
    
# Vamos a leer los archivos con esta celda. Al darle la dirección de la carpeta Datos, lo que estoy sacando
# son los nombres de todos los archivos en esa carpeta.
#--------------------------------------------------------------------------

CarpCheck=[[root,files] for root,dirs,files in os.walk("./Datos Corte")]

# El comentario anterior era considerando que no le daba la dirección correcta
# de la carpeta con mi información al os.walk. Esta vez le estoy pasando la 
# dirección exacta, así que no es necesario hacer tanto quilombo para separar
# los nombres de los archivos. El elemento en la posición x[0] es el nombre de la carpeta

for x in CarpCheck:
    # dada = x[0].split("\\")
    Archivos_Datos = [nombre for nombre in x[1]]
    Archivos_Datos.insert(0,x[0])

# Con esto tengo los nombres de todos los archivos en la carpeta de Datos
# Archivos_Datos tiene en la primer coordenada el principio de la dirección
# de la carpeta, y el resto de elementos son los archivos en la carpeta.
# Entonces si quiero buscar el objeto voy a tener que usar:
# Archivos_Datos[0]/Archivos_Datos[1]

#----------------------------------------------------------------------------

Tiempo()


# In[3]:


t0=time.time()

# En esta celda voy a levantar los datos de opiniones y buscar encontrar el valor de error que
# me permita definir un criterio de corte para mi función principal
#-------------------------------------------------------------------------------------------

CarpCheck=[[root,files] for root,dirs,files in os.walk("./Datos Corte")]

# El comentario anterior era considerando que no le daba la dirección correcta
# de la carpeta con mi información al os.walk. Esta vez le estoy pasando la 
# dirección exacta, así que no es necesario hacer tanto quilombo para separar
# los nombres de los archivos. El elemento en la posición x[0] es el nombre de la carpeta

for x in CarpCheck:
    # dada = x[0].split("\\")
    Archivos_Datos = [nombre for nombre in x[1]]
    Archivos_Datos.insert(0,x[0])

# Con esto tengo los nombres de todos los archivos en la carpeta de Datos Corte
# Archivos_Datos tiene en la primer coordenada el principio de la dirección
# de la carpeta, y el resto de elementos son los archivos en la carpeta.
# Entonces si quiero buscar el objeto voy a tener que usar:
# Archivos_Datos[0]/Archivos_Datos[1]

#----------------------------------------------------------------------------

# Tengo dos tipos de archivos. Los de datos de opiniones tienen el siguiente formato:
# Datos_Evolucion_Opinion_N=$_T=$_K=$
# Los de datos de error cuadrático tienen el formato: Datos_Variacion_Promedio_N=$_T=$_K=$
# Armemos dos listas, una con los nombres de las opiniones y otra con los nombres de los errores.
# En ambas listas el primer elemento va a ser la carpeta en la que se encuentran los datos.
# En esta celda voy a construir la lista de Nombres de Opiniones


Nombres_Opiniones = [Archivos_Datos[0]]
for nombre in Archivos_Datos[1:len(Archivos_Datos)]:
    if nombre.split("_")[1] == "Evolucion":
        Nombres_Opiniones.append(nombre)



# Bien, las listas de nombres de archivos ya se arman correctamente

#-----------------------------------------------------------------------------
# Como el número de agentes de cada batch de datos no tiene porqué ser siempre el 
# mismo, me gustaría saber cuáles son todos los N para los cuales existe un archivo.
# Por eso lo que voy a hacer es armar una lista, guardar TODOS los N ahí y después
# convertir la lista en conjunto para deshacerme de los duplicados

Conjunto_Agentes = []

for nombre in Nombres_Opiniones[1:len(Nombres_Opiniones)]:
    Conjunto_Agentes.append(int(nombre.split("_")[3].split("=")[1]))

Conjunto_Agentes = set(Conjunto_Agentes)

# Bien, esto ya me arma el conjunto de agentes con todos los valores de N para los cuales
# hay un archivo de datos.

#-------------------------------------------------------------------------------------------

# Voy a iterar esto con todos los archivos de opiniones a ver que observo
for agentes in Conjunto_Agentes:
    plt.figure(figsize=(20,12))
    for nombre in Nombres_Opiniones[1:len(Nombres_Opiniones)]:
        # Levanto los valores de N y T del nombre de mi archivo. Es importante recordar que mis
        # archivos tienen nombres de la forma: Datos_Evolucion_Opinion_N=$_T=$_K=$

        N = int(nombre.split("_")[3].split("=")[1])
        T = int(nombre.split("_")[4].split("=")[1])
        K = float(nombre.split("_")[5].split("=")[1])

        # Los valores de N, T y K se levantan correctamente
        if agentes==N:
            #--------------------------------------------------------------------------------------------

            # Levanto los datos del archivo original y separo los datos en tres listas.
            # Una para la matriz de Adyacencia, una para la matriz de superposición y una para los vectores de opiniones

            Datos = ldata("{}/{}".format(Nombres_Opiniones[0],nombre))

            Ady = Datos[1][1:len(Datos[1])] # Lista con elementos de la matriz de Adyacencia
            Ady = [int(x) for x in Ady]

            Sup = Datos[3][1:len(Datos[3])] # Lista con elementos de la matriz de Superposición
            Sup = [float(x) for x in Sup]

            # Lista con elementos de los vectores de opinión. Al final sí había una forma compacta de hacer esto.
            # Si la matriz de Adyacencia evoluciona en el tiempo, va a haber que ver de hacer cambios acá.
            Opi = [[float(x) for x in fila[1:len(fila)]] for fila in Datos[5:len(Datos)]]

            # Mis listas ya se arman correctamente, tengo separados sin dramas los valores de mis tres matrices.

            #--------------------------------------------------------------------------------------------

            # Hagamos un gráfico de estos datos
            # La idea es hacer una sumatoria del valor cuadrado de las opiniones de cada uno.
            # En otra celda empezaré a ver de hacer un gráfico que registre la trayectoria de la opinión de los agentes.

            X = np.arange(0,len(Opi))
            POC = {} # POC significa Promedio Opiniones Cuadradas.
            for j in range(T):
                # Obtengo los valores cuadrados de todos mis tópicos
                POC[j] = []
                for i in range(len(Opi)):
                    # TS es Tópicos Separados. Esta lista va a ir tomando todas las opiniones de un cierto tópico en una iteración
                    TS = [t**2 for t in Opi[i][j:len(Opi[i]):T]]
                    # Ahora los sumo y los agrego a mis vectores Y
                    POC[j].append(np.sum(TS)/len(TS))


            # El vector X con el número de iteraciones, así como el diccionario que guarda las opiniones de cada tópico por
            # separado funcionan correctamente. Ahora puedo cambiar el número de tópicos de mi sistema sin dramas.

            #-------------------------------------------------------------------------------------------

            # Hay que ver la forma de graficar esto correctamente, sin que estalle en términos de cantidad de
            # cosas graficadas, y que permita entenderse


            YT = np.zeros(len(Opi))
            for j in range(T):
                YT += np.array(POC[j])

            plt.plot(X,YT, "--",label="N={},K={},T={}".format(N,K,T) ,linewidth = 3)

    plt.rcParams.update({'font.size': 18})
    plt.xlabel("Iteraciones")
    plt.ylabel("Promedio de Opiniones Cuadradas")
    plt.title("Evolución de las opiniones con N={} agentes".format(agentes))
    plt.legend()
    plt.grid()
    plt.savefig("../Imagenes/Corte/Opiniones_Corte_N={}_T={}.png".format(agentes,T),bbox_inches = "tight")
    plt.close()


# El graficado de la función va bien, pero todavía siento que no puede bancarse cualquier cambio. Tengo que
# considerar un poco más los posibles casos.

Tiempo()


# In[4]:


t0 = time.time()

# En esta celda lo que voy a hacer es graficar los "errores" de mis sistemas. Es decir que voy a 
# estar mirando la suma del cuadrado de la diferencia del sistema en dos pasos temporales sucesivos. 
# La idea es ver cuánto cambia y a cuanto llega a medida que avanza en las iteraciones
# para poder establecer un criterio de corte de las iteraciones del sistema.

#--------------------------------------------------------------------------------------------

CarpCheck=[[root,files] for root,dirs,files in os.walk("./Datos Corte")]

# El comentario anterior era considerando que no le daba la dirección correcta
# de la carpeta con mi información al os.walk. Esta vez le estoy pasando la 
# dirección exacta, así que no es necesario hacer tanto quilombo para separar
# los nombres de los archivos. El elemento en la posición x[0] es el nombre de la carpeta

for x in CarpCheck:
    # dada = x[0].split("\\")
    Archivos_Datos = [nombre for nombre in x[1]]
    Archivos_Datos.insert(0,x[0])

# Con esto tengo los nombres de todos los archivos en la carpeta de Datos Corte
# Archivos_Datos tiene en la primer coordenada el principio de la dirección
# de la carpeta, y el resto de elementos son los archivos en la carpeta.
# Entonces si quiero buscar el objeto voy a tener que usar:
# Archivos_Datos[0]/Archivos_Datos[1]

#----------------------------------------------------------------------------

# Tengo dos tipos de archivos. Los de datos de opiniones tienen el siguiente formato:
# Datos_Evolucion_Opinion_N=$_T=$_K=$
# Los de datos de error cuadrático tienen el formato: Datos_Variacion_Promedio_N=$_T=$_K=$
# Armemos dos listas, una con los nombres de las opiniones y otra con los nombres de los errores.
# En ambas listas el primer elemento va a ser la carpeta en la que se encuentran los datos.
# En esta celda voy a armar la lista de Nombres de Errores.
        
Nombres_Errores = [Archivos_Datos[0]]
for nombre in Archivos_Datos[1:len(Archivos_Datos)]:
    if nombre.split("_")[1] == "Variacion":
        Nombres_Errores.append(nombre)

# Bien, las listas de nombres de archivos ya se arman correctamente

#-------------------------------------------------------------------------------------------
# Como el número de agentes de cada batch de datos no tiene porqué ser siempre el 
# mismo, me gustaría saber cuáles son todos los N para los cuales existe un archivo.
# Por eso lo que voy a hacer es armar una lista, guardar TODOS los N ahí y después
# convertir la lista en conjunto para deshacerme de los duplicados

Conjunto_Agentes = []

for nombre in Nombres_Errores[1:len(Nombres_Errores)]:
    Conjunto_Agentes.append(int(nombre.split("_")[3].split("=")[1]))
    
Conjunto_Agentes = set(Conjunto_Agentes)

# Bien, esto ya me arma el conjunto de agentes con todos los valores de N para los cuales
# hay un archivo de datos.

#-------------------------------------------------------------------------------------------

# Voy a iterar esto con todos los archivos de Variación de opinones a ver que observo
for agentes in Conjunto_Agentes:
    plt.figure(figsize=(20,12))
    for nombre in Nombres_Errores[1:len(Nombres_Errores)]:
        
        # Levanto los valores de N y T del nombre de mi archivo. Es importante recordar que mis
        # archivos tienen nombres de la forma: Datos_Errcuad_DiferenciaOpi_N=$_T=$_K=$

        N = int(nombre.split("_")[3].split("=")[1])
        T = int(nombre.split("_")[4].split("=")[1])
        K = float(nombre.split("_")[5].split("=")[1])

        # Los valores de N, T y K se levantan correctamente

        #--------------------------------------------------------------------------------------------
        if agentes==N:

            # Levanto los datos del archivo original y separo los datos en tres listas.
            # Una para la matriz de Adyacencia, una para la matriz de superposición y una para los vectores de opiniones

            Datos = ldata("{}/{}".format(Nombres_Errores[0],nombre))

            # Lista con elementos de los vectores de opinión. Al final sí había una forma compacta de hacer esto.
            # Si la matriz de Adyacencia evoluciona en el tiempo, va a haber que ver de hacer cambios acá.
            Var = [float(x) for x in Datos[0][1:len(Datos[0])]]

            # Tengo correctamente levantados los datos de los errores

            #--------------------------------------------------------------------------------------------

            # Como lo único que tengo que graficar es el Error, ya tengo los datos armados. Sólo necesito
            # un vector X asociado.

            X = np.arange(0,len(Var))

            plt.semilogy(X,Var, "--",label="N={},K={},T={}".format(N,K,T) ,linewidth = 3)

    plt.rcParams.update({'font.size': 18})
    plt.xlabel("Iteraciones")
    plt.ylabel("Variación promedio de las opiniones")
    plt.title("Variación Promedio del sistema para N={} agentes".format(agentes))
    plt.grid()
    plt.legend()
    plt.savefig("../Imagenes/Corte/Variaciones_Corte_N={}_T={}.png".format(agentes,T),bbox_inches = "tight")
    plt.close()



Tiempo()


# In[6]:


t0 = time.time()

# En esta celda voy a graficar los datos obtenidos con el mecanismo de corte implementado.
# Voy a graficar las opiniones y las variaciones promedio, todo en esta celda.
# Las imágenes las voy a guardar en la carpeta "Interacción Pares" dentro de imágenes

#--------------------------------------------------------------------------------------

CarpCheck=[[root,files] for root,dirs,files in os.walk("./Interaccion Pares")]

# El comentario anterior era considerando que no le daba la dirección correcta
# de la carpeta con mi información al os.walk. Esta vez le estoy pasando la 
# dirección exacta, así que no es necesario hacer tanto quilombo para separar
# los nombres de los archivos. El elemento en la posición x[0] es el nombre de la carpeta

for x in CarpCheck:
    # dada = x[0].split("\\")
    Archivos_Datos = [nombre for nombre in x[1]]
    Archivos_Datos.insert(0,x[0])

# Con esto tengo los nombres de todos los archivos en la carpeta de Datos Corte
# Archivos_Datos tiene en la primer coordenada el principio de la dirección
# de la carpeta, y el resto de elementos son los archivos en la carpeta.
# Entonces si quiero buscar el objeto voy a tener que usar:
# Archivos_Datos[0]/Archivos_Datos[1]

#----------------------------------------------------------------------------

# Tengo dos tipos de archivos. Los de datos de opiniones tienen el siguiente formato:
# Datos_Evolucion_Opinion_N=$_T=$_K=$
# Los de datos de error cuadrático tienen el formato: Datos_Variacion_Promedio_N=$_T=$_K=$
# Armemos dos listas, una con los nombres de las opiniones y otra con los nombres de los errores.
# En ambas listas el primer elemento va a ser la carpeta en la que se encuentran los datos.
# En esta celda voy a construir la lista de Nombres de Opiniones


Nombres_Opiniones = [Archivos_Datos[0]]
for nombre in Archivos_Datos[1:len(Archivos_Datos)]:
    if nombre.split("_")[1] == "Evolucion":
        Nombres_Opiniones.append(nombre)



# Bien, las listas de nombres de archivos ya se arman correctamente

#-----------------------------------------------------------------------------

# Como el número de agentes de cada batch de datos no tiene porqué ser siempre el 
# mismo, me gustaría saber cuál es el máximo y mínimo número de agentes. Por razones.

Nmin = int(Nombres_Opiniones[1].split("_")[3].split("=")[1])
Nmax = int(Nombres_Opiniones[1].split("_")[3].split("=")[1])

# Defino un Nmin y Nmax inicial cualquiera, pero que esté dentro del conjunto total

for nombre in Nombres_Opiniones[1:len(Nombres_Opiniones)]:
    N = int(nombre.split("_")[3].split("=")[1])
    Nmin = min(N,Nmin)
    Nmax = max(N,Nmax)

# Bien, esto ya me obtiene los valores de Nmin y Nmax correctamente

#-------------------------------------------------------------------------------------------

# Tengo dos tipos de archivos. Los de datos de opiniones tienen el siguiente formato:
# Datos_Evolucion_Opinion_N=$_T=$_K=$
# Los de datos de error cuadrático tienen el formato: Datos_Variacion_Promedio_N=$_T=$_K=$
# Armemos dos listas, una con los nombres de las opiniones y otra con los nombres de los errores.
# En ambas listas el primer elemento va a ser la carpeta en la que se encuentran los datos.
# En esta celda voy a armar la lista de Nombres de Errores.
        
Nombres_Errores = [Archivos_Datos[0]]
for nombre in Archivos_Datos[1:len(Archivos_Datos)]:
    if nombre.split("_")[1] == "Variacion":
        Nombres_Errores.append(nombre)

# Bien, las listas de nombres de archivos ya se arman correctamente

#-------------------------------------------------------------------------------------------

# Voy a iterar esto con todos los archivos de opiniones a ver que observo
for agentes in range(Nmin,Nmax+1):
    plt.figure(figsize=(20,12))
    for nombre in Nombres_Opiniones[1:len(Nombres_Opiniones)]:
        # Levanto los valores de N y T del nombre de mi archivo. Es importante recordar que mis
        # archivos tienen nombres de la forma: Datos_Evolucion_Opinion_N=$_T=$_K=$

        N = int(nombre.split("_")[3].split("=")[1])
        T = int(nombre.split("_")[4].split("=")[1])
        K = float(nombre.split("_")[5].split("=")[1])

        # Los valores de N, T y K se levantan correctamente
        if agentes==N:
            #--------------------------------------------------------------------------------------------

            # Levanto los datos del archivo original y separo los datos en tres listas.
            # Una para la matriz de Adyacencia, una para la matriz de superposición y una para los vectores de opiniones

            Datos = ldata("{}/{}".format(Nombres_Opiniones[0],nombre))

            Ady = Datos[1][1:len(Datos[1])] # Lista con elementos de la matriz de Adyacencia
            Ady = [int(x) for x in Ady]

            Sup = Datos[3][1:len(Datos[3])] # Lista con elementos de la matriz de Superposición
            Sup = [float(x) for x in Sup]

            # Lista con elementos de los vectores de opinión. Al final sí había una forma compacta de hacer esto.
            # Si la matriz de Adyacencia evoluciona en el tiempo, va a haber que ver de hacer cambios acá.
            Opi = [[float(x) for x in fila[1:len(fila)]] for fila in Datos[5:len(Datos)]]

            # Mis listas ya se arman correctamente, tengo separados sin dramas los valores de mis tres matrices.

            #--------------------------------------------------------------------------------------------

            # Hagamos un gráfico de estos datos
            # La idea es hacer una sumatoria del valor cuadrado de las opiniones de cada uno.
            # En otra celda empezaré a ver de hacer un gráfico que registre la trayectoria de la opinión de los agentes.

            X = np.arange(0,len(Opi))
            POC = {} # POC significa Promedio Opiniones Cuadradas.
            for j in range(T):
                # Obtengo los valores cuadrados de todos mis tópicos
                POC[j] = []
                for i in range(len(Opi)):
                    # TS es Tópicos Separados. Esta lista va a ir tomando todas las opiniones de un cierto tópico en una iteración
                    TS = [t**2 for t in Opi[i][j:len(Opi[i]):T]]
                    # Ahora los sumo y los agrego a mis vectores Y
                    POC[j].append(np.sum(TS)/len(TS))


            # El vector X con el número de iteraciones, así como el diccionario que guarda las opiniones de cada tópico por
            # separado funcionan correctamente. Ahora puedo cambiar el número de tópicos de mi sistema sin dramas.

            #-------------------------------------------------------------------------------------------

            # Hay que ver la forma de graficar esto correctamente, sin que estalle en términos de cantidad de
            # cosas graficadas, y que permita entenderse


            YT = np.zeros(len(Opi))
            for j in range(T):
                YT += np.array(POC[j])

            plt.plot(X,YT, "--",label="N={},K={},T={}".format(N,K,T) ,linewidth = 3)

    plt.rcParams.update({'font.size': 18})
    plt.xlabel("Iteraciones")
    plt.ylabel("Promedio de Opiniones Cuadradas")
    plt.title("Evolución de las opiniones con N={} agentes".format(agentes))
    plt.legend()
    plt.grid()
    plt.savefig("../Imagenes/Interaccion Pares/Opiniones_Corte_N={}_T={}.png".format(agentes,T),bbox_inches = "tight")
    plt.close()
    
#----------------------------------------------------------------------------------------------------

# Voy a iterar esto con todos los archivos de Variación de opiniones a ver que observo
for agentes in range(Nmin,Nmax+1):
    plt.figure(figsize=(20,12))
    for nombre in Nombres_Errores[1:len(Nombres_Errores)]:
        
        # Levanto los valores de N y T del nombre de mi archivo. Es importante recordar que mis
        # archivos tienen nombres de la forma: Datos_Errcuad_DiferenciaOpi_N=$_T=$_K=$

        N = int(nombre.split("_")[3].split("=")[1])
        T = int(nombre.split("_")[4].split("=")[1])
        K = float(nombre.split("_")[5].split("=")[1])

        # Los valores de N, T y K se levantan correctamente

        #--------------------------------------------------------------------------------------------
        if agentes==N:

            # Levanto los datos del archivo original y separo los datos en tres listas.
            # Una para la matriz de Adyacencia, una para la matriz de superposición y una para los vectores de opiniones

            Datos = ldata("{}/{}".format(Nombres_Errores[0],nombre))

            # Lista con elementos de los vectores de opinión. Al final sí había una forma compacta de hacer esto.
            # Si la matriz de Adyacencia evoluciona en el tiempo, va a haber que ver de hacer cambios acá.
            Var = [float(x) for x in Datos[0][1:len(Datos[0])]]

            # Tengo correctamente levantados los datos de los errores

            #--------------------------------------------------------------------------------------------

            # Como lo único que tengo que graficar es el Error, ya tengo los datos armados. Sólo necesito
            # un vector X asociado.

            X = np.arange(0,len(Var))

            plt.semilogy(X,Var, "--",label="N={},K={},T={}".format(N,K,T) ,linewidth = 3)

    plt.rcParams.update({'font.size': 18})
    plt.xlabel("Iteraciones")
    plt.ylabel("Variación promedio de las opiniones")
    plt.title("Variación Promedio del sistema para N={} agentes".format(agentes))
    plt.grid()
    plt.legend()
    plt.savefig("../Imagenes/Interaccion Pares/Variaciones_Corte_N={}_T={}.png".format(agentes,T),bbox_inches = "tight")
    plt.close()

# Con todo lo agregado, esto debería armar correctamente las imágenes y guardarlas en la carpeta de
# Interaccion Pares dentro de la carpeta de Imagenes.

Tiempo()


# In[ ]:


t0 = time.time()

# En esta celda lo que voy a hacer es intentar replicar el gráfico de Opiniones de Baumann
# Para eso voy a tener que armar una nueva tanda de datos. Estos datos ahora van a tener que
# tener los valores de alfa y Delta variables, número de agentes igual a 1000, K=3, T=2
# El beta y demás valores por ahora no los defino porque no afectan al modelo armado

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
    
#----------------------------------------------------------------------------------------------

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

CarpCheck=[[root,files] for root,dirs,files in os.walk("./Grafico Baumann")]

# El comentario anterior era considerando que no le daba la dirección correcta
# de la carpeta con mi información al os.walk. Esta vez le estoy pasando la 
# dirección exacta, así que no es necesario hacer tanto quilombo para separar
# los nombres de los archivos. El elemento en la posición x[0] es el nombre de la carpeta

for x in CarpCheck:
    # dada = x[0].split("\\")
    Archivos_Datos = [nombre for nombre in x[1]]
    Archivos_Datos.insert(0,x[0])

# Con esto tengo los nombres de todos los archivos en la carpeta de Datos Corte
# Archivos_Datos tiene en la primer coordenada el principio de la dirección
# de la carpeta, y el resto de elementos son los archivos en la carpeta.
# Entonces si quiero buscar el objeto voy a tener que usar:
# Archivos_Datos[0]/Archivos_Datos[1]


#--------------------------------------------------------------------------------------------

# Voy a iterar esto para todos los archivos de datos que tengo

for nombre in Archivos_Datos[1:len(Archivos_Datos)]:

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
    
    #--------------------------------------------------------------------------------------------

    # Levanto los valores de alfa y Cdelta del nombre de mi archivo. Es importante recordar que mis
    # archivos tienen nombres de la forma: Datos_Opiniones_alfa=$_Cdelta=$.
    # El valor de T es siempre 2. El valor de N puedo deducirlo sabiendo T.

    alfa = float(nombre.split("_")[2].split("=")[1])
    Cdelta = float(nombre.split("_")[3].split("=")[1])
    T = 2
    N = int(len(Opi[0])/T)

    # Los valores de alfa, Cdelta, T y N se levantan correctamente
    
    #----------------------------------------------------------------------------------------------
    
    # Estos son los parámetros que definen el tamaño del gráfico, tamaño de la letra y nombres de
    # los ejes.
        
        
    plt.figure(figsize=(20,12))
    plt.rcParams.update({'font.size': 18})
    plt.xlabel("Tópico 1")
    plt.ylabel("Tópico 2")
    plt.title(r"Trayectoria de las opiniones en el espacio de tópicos para $\alpha$={} y Cdelta={}".format(alfa,Cdelta))
    
   #----------------------------------------------------------------------------------------------
    
    
    # Voy a intentar replicar el gráfico de Baumann. Para eso voy a querer graficar la trayectoria
    # de todos los agentes. Como van a ser muchos agentes, me conviene que esas trayectorias se grafiquen
    # con líneas finitas
    
    for agente in range(N):
        OdT = dict() # OdT es Opiniones del Tópico.
        for topico in range(T):
            OdT[topico] = []
            for iteracion in range(len(Opi)):
                OdT[topico].append(Opi[iteracion][agente*T+topico])
    
    # Esto levanta correctamente los valores de las opiniones de los agentes para cada uno de sus tópicos      
    
    #-----------------------------------------------------------------------------------------------
    
    # Como todavía tengo dos tópicos, puedo graficar esto en un plano. Así que ahora voy a hacer
    # un código presuponiendo que la cantidad de tópicos es 2. Sino, esto no debería realizarse.
    # Atento a eso.
    
        plt.plot(OdT[0],OdT[1], color="gray",linewidth = 0.6)
    
    #-------------------------------------------------------------------------------------------------
    
    # Genial, así como está esto ya arma el gráfico de las trayectorias de las opiniones. Ahora, me gustaría
    # colocar puntos marcando el final de mis trayectorias. Empecemos con todos puntos del mismo color.
    # Después le voy a agregar que los puntos tengan un color que se corresponda con el ángulo que
    # forman sus componentes con la horizontal.
    
    # IMPORTANTE: Este código está actuando sobre el mismo plot que antes. Por tanto hay que estar atento
    # a respetar la indentación marcada por el for de "agente". Además el código está variando dinámicamente porque
    # estoy cambiando de lugar el plt.show hasta el final cada vez que agrego algo. Atento a eso considerando
    # que estoy intentando armar estos pedazos de código de forma modular.
        
        indice = Indice_Color([OdT[0][len(OdT[0])-1],OdT[1][len(OdT[1])-1]],Divisiones)
        plt.plot(OdT[0][len(OdT[0])-1],OdT[1][len(OdT[1])-1], "o" ,c = color[indice], markersize=10)
    plt.savefig("../Imagenes/Grafico Baumann/Trayectoria de las opiniones_alfa={}_Cdelta={}.png".format(alfa,Cdelta),bbox_inches = "tight")
    plt.close()
    
    # Ya implementé la coloración de cada punto según el ángulo que el vector final forma con la horizontal.
    # Ahora eso no se nota porque 



Tiempo()


# In[23]:


t0 = time.time()

# En esta celda lo que voy a hacer es mirar los datos que obtuve del programa
# Donde alfa y Delta son las variables. Quiero ver que no haya tocado nada
# raro en el programa y que siga funcionando bien.

#--------------------------------------------------------------------------------------

CarpCheck=[[root,files] for root,dirs,files in os.walk("./Grafico Baumann")]

# El comentario anterior era considerando que no le daba la dirección correcta
# de la carpeta con mi información al os.walk. Esta vez le estoy pasando la 
# dirección exacta, así que no es necesario hacer tanto quilombo para separar
# los nombres de los archivos. El elemento en la posición x[0] es el nombre de la carpeta

for x in CarpCheck:
    # dada = x[0].split("\\")
    Archivos_Datos = [nombre for nombre in x[1]]
    Archivos_Datos.insert(0,x[0])

# Con esto tengo los nombres de todos los archivos en la carpeta de Datos Corte
# Archivos_Datos tiene en la primer coordenada el principio de la dirección
# de la carpeta, y el resto de elementos son los archivos en la carpeta.
# Entonces si quiero buscar el objeto voy a tener que usar:
# Archivos_Datos[0]/Archivos_Datos[1]

#--------------------------------------------------------------------------------------------

# Levanto los datos del archivo original y separo los datos en tres listas.
# Una para la matriz de Adyacencia, una para la matriz de superposición y una para los vectores de opiniones

Datos = ldata("{}/{}".format(Archivos_Datos[0],Archivos_Datos[1]))

Ady = Datos[1][1:len(Datos[1])] # Lista con elementos de la matriz de Adyacencia
Ady = [int(x) for x in Ady]

Sup = Datos[3][1:len(Datos[3])] # Lista con elementos de la matriz de Superposición
Sup = [float(x) for x in Sup]

# Lista con elementos de los vectores de opinión. Al final sí había una forma compacta de hacer esto.
# Si la matriz de Adyacencia evoluciona en el tiempo, va a haber que ver de hacer cambios acá.
Opi = [[float(x) for x in fila[1:len(fila)]] for fila in Datos[5:len(Datos)]]

# Mis listas ya se arman correctamente, tengo separados sin dramas los valores de mis tres matrices.

#--------------------------------------------------------------------------------------------

# Hagamos un gráfico de estos datos
# La idea es hacer una sumatoria del valor cuadrado de las opiniones de cada uno.
# En otra celda empezaré a ver de hacer un gráfico que registre la trayectoria de la opinión de los agentes.

X = np.arange(0,len(Opi))
T = 2 # Este es el número de tópicos
POC = {} # POC significa Promedio Opiniones Cuadradas.
for j in range(T):
    # Obtengo los valores cuadrados de todos mis tópicos
    POC[j] = []
    for i in range(len(Opi)):
        # TS es Tópicos Separados. Esta lista va a ir tomando todas las opiniones de un cierto tópico en una iteración
        TS = [t**2 for t in Opi[i][j:len(Opi[i]):T]]
        # Ahora los sumo y los agrego a mis vectores Y
        POC[j].append(np.sum(TS)/len(TS))


# El vector X con el número de iteraciones, así como el diccionario que guarda las opiniones de cada tópico por
# separado funcionan correctamente. Ahora puedo cambiar el número de tópicos de mi sistema sin dramas.

# -------------------------------------------------------------------------------------------

# Hay que ver la forma de graficar esto correctamente, sin que estalle en términos de cantidad de
# cosas graficadas, y que permita entenderse


YT = np.zeros(len(Opi))
for j in range(T):
    YT += np.array(POC[j])

plt.figure(figsize=(20,12))
plt.plot(X,YT, "--", linewidth = 3)
plt.rcParams.update({'font.size': 18})
plt.xlabel("Iteraciones")
plt.ylabel("Promedio de Opiniones Cuadradas")
plt.title("Evolución de las opiniones")
plt.grid()
plt.show()

#-------------------------------------------------------------------------------------------------

# Acabo de caer en la cuenta que aunque no guarde los datos de las variaciones,
# puedo calcularlas, total tengo todos los datos de opiniones del sistema. El renglón de
# Var define la lista por comprensión.

Var = [math.sqrt(np.sum(np.array([((x2-x1)**2)/len(Opi[i]) for x1,x2 in zip (Opi[i],Opi[i+1])]))) for i in range(len(Opi)-1)]
X = np.arange(0,len(Var))

plt.figure(figsize=(20,12))
plt.semilogy(X,Var, "--",label="N={},K={},T={}".format(N,K,T) ,linewidth = 3)
plt.rcParams.update({'font.size': 18})
plt.xlabel("Iteraciones")
plt.ylabel("Variación promedio de las opiniones")
plt.title("Variación Promedio del sistema")
plt.grid()
plt.show()

# El programa sigue funcionando bárbaro, lo cual es buenísimo. Corta en el momento
# adecuado y el comportamiento es razonbale.



Tiempo()


# In[12]:


# En esta celda voy a analizar los datos obtenidos con el modelo que crea
# la red a partir de un modelo de Erdos-Renyi. Es decir, tengo una red fija
# creada de manera aleatoria con una cierta probabilidad p.

t0=time.time()

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
    
#----------------------------------------------------------------------------------------------

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

CarpCheck=[[root,files] for root,dirs,files in os.walk("./Modelo Erdos-Renyi")]

# El comentario anterior era considerando que no le daba la dirección correcta
# de la carpeta con mi información al os.walk. Esta vez le estoy pasando la 
# dirección exacta, así que no es necesario hacer tanto quilombo para separar
# los nombres de los archivos. El elemento en la posición x[0] es el nombre de la carpeta

for x in CarpCheck:
    # dada = x[0].split("\\")
    Archivos_Datos = [nombre for nombre in x[1]]
    Archivos_Datos.insert(0,x[0])

# Con esto tengo los nombres de todos los archivos en la carpeta de Datos Corte
# Archivos_Datos tiene en la primer coordenada el principio de la dirección
# de la carpeta, y el resto de elementos son los archivos en la carpeta.
# Entonces si quiero buscar el objeto voy a tener que usar:
# Archivos_Datos[0]/Archivos_Datos[1]


#--------------------------------------------------------------------------------------------

# Voy a iterar esto para todos los archivos de datos que tengo

for nombre in Archivos_Datos[1:len(Archivos_Datos)]:

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
    
    #--------------------------------------------------------------------------------------------

    # Levanto los valores de alfa y Cdelta del nombre de mi archivo. Es importante recordar que mis
    # archivos tienen nombres de la forma: Datos_Opiniones_alfa=$_Cdelta=$_N=$.
    # El valor de T es siempre 2. El valor de N puedo deducirlo sabiendo T.

    alfa = float(nombre.split("_")[2].split("=")[1])
    Cdelta = float(nombre.split("_")[3].split("=")[1])
    T = 2
    N = int(nombre.split("_")[4].split("=")[1])

    # Los valores de alfa, Cdelta, T y N se levantan correctamente
    
    #----------------------------------------------------------------------------------------------
    
    # Estos son los parámetros que definen el tamaño del gráfico, tamaño de la letra y nombres de
    # los ejes.
        
        
    plt.figure(figsize=(20,12))
    plt.rcParams.update({'font.size': 18})
    plt.xlabel("Tópico 1")
    plt.ylabel("Tópico 2")
    plt.title(r"Trayectoria de las opiniones en el espacio de tópicos para $\alpha$={}, Cdelta={} y N={}".format(alfa,Cdelta,N))
    
   #----------------------------------------------------------------------------------------------
    
    
    # Voy a intentar replicar el gráfico de Baumann. Para eso voy a querer graficar la trayectoria
    # de todos los agentes. Como van a ser muchos agentes, me conviene que esas trayectorias se grafiquen
    # con líneas finitas
    
    for agente in range(N):
        OdT = dict() # OdT es Opiniones del Tópico.
        for topico in range(T):
            OdT[topico] = []
            for iteracion in range(len(Opi)):
                OdT[topico].append(Opi[iteracion][agente*T+topico])
    
    # Esto levanta correctamente los valores de las opiniones de los agentes para cada uno de sus tópicos      
    
    #-----------------------------------------------------------------------------------------------
    
    # Como todavía tengo dos tópicos, puedo graficar esto en un plano. Así que ahora voy a hacer
    # un código presuponiendo que la cantidad de tópicos es 2. Sino, esto no debería realizarse.
    # Atento a eso.
    
        plt.plot(OdT[0],OdT[1], color="gray",linewidth = 0.6)
    
    #-------------------------------------------------------------------------------------------------
    
    # Genial, así como está esto ya arma el gráfico de las trayectorias de las opiniones. Ahora, me gustaría
    # colocar puntos marcando el final de mis trayectorias. Empecemos con todos puntos del mismo color.
    # Después le voy a agregar que los puntos tengan un color que se corresponda con el ángulo que
    # forman sus componentes con la horizontal.
    
    # IMPORTANTE: Este código está actuando sobre el mismo plot que antes. Por tanto hay que estar atento
    # a respetar la indentación marcada por el for de "agente". Además el código está variando dinámicamente porque
    # estoy cambiando de lugar el plt.show hasta el final cada vez que agrego algo. Atento a eso considerando
    # que estoy intentando armar estos pedazos de código de forma modular.
        
        indice = Indice_Color([OdT[0][len(OdT[0])-1],OdT[1][len(OdT[1])-1]],Divisiones)
        plt.plot(OdT[0][len(OdT[0])-1],OdT[1][len(OdT[1])-1], "o" ,c = color[indice], markersize=10)
    plt.savefig("../Imagenes/Modelo Erdos-Renyi/Trayectoria de las opiniones_alfa={}_Cdelta={}_N={}.png".format(alfa,Cdelta,N),bbox_inches = "tight")
    plt.close()
    
    # Ya implementé la coloración de cada punto según el ángulo que el vector final forma con la horizontal.
    # Ahora eso no se nota porque 



Tiempo()


# In[5]:


# En esta celda voy a analizar cómo varía el cálculo del sistema a medida que varío
# el valor del dt. La idea es ver si puedo usar dt's más grande al calcular el sistema.
# Poder usar dt's más grande sería copado para poder reducir el tamaño de los archivos y
# más importante, el tiempo que tardo en crear los archivos. Lo que vamos a comparar
# es gráficos de trayectorias, gráficos de Variación promedio y armar un gráfico
# final de cantidad de iteraciones en función de cos(delta) para cada alfa.

t0=time.time()

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

CarpCheck=[[root,files] for root,dirs,files in os.walk("./Cambios dt")]

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

# Es important partir del hecho de que mis archivos llevan por nombre: "Datos_Opiniones_alfa=$_dt=$"

Conjunto_Alfa = []
Conjunto_dt = []

for nombre in Archivos_Datos[1:len(Archivos_Datos)]:
    alfa = float(nombre.split("_")[2].split("=")[1])
    dt = float(nombre.split("_")[3].split("=")[1])
    Conjunto_Alfa.append(alfa)
    Conjunto_dt.append(dt)
    
Conjunto_Alfa = list(set(Conjunto_Alfa))
Conjunto_dt = list(set(Conjunto_dt))

Conjunto_Alfa.sort()
Conjunto_dt.sort()

# Bien, esto ya me arma el conjunto de Alfas y dt con todos los valores de alfa y dt
# que hay en los archivos.

#--------------------------------------------------------------------------------------------

# Voy a iterar esto para todos los archivos de datos que tengo

plt.figure("Iteraciones vs dt",figsize=(20,12),clear=True)
for ALFA in Conjunto_Alfa:
    plt.figure("Variaciones Promedio",figsize=(20,12),clear=True)
    
    Iteraciones = []
    DT = []
    for nombre in Archivos_Datos[1:len(Archivos_Datos)]:

        #--------------------------------------------------------------------------------------------

        # Levanto los valores de alfa y Cdelta del nombre de mi archivo. Es importante recordar que mis
        # archivos tienen nombres de la forma: Datos_Opiniones_alfa=$_dt=$.
        # El valor de T es siempre 2. El valor de N puedo deducirlo sabiendo T.

        alfa = float(nombre.split("_")[2].split("=")[1])
        dt = float(nombre.split("_")[3].split("=")[1])
        Cdelta = 0.2
        T = 2
        N = 100

        # Los valores de alfa, dt, Cdelta, T y N se levantan correctamente

        #--------------------------------------------------------------------------------------------
        
        # Antes de levantar mi archivo de datos, decido si es el alfa correspondiente
        
        if alfa==ALFA:
        
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

            # Estos son los parámetros que definen el tamaño del gráfico, tamaño de la letra y nombres de
            # los ejes.


            plt.figure("Trayectoria Opiniones",figsize=(20,12))
            plt.rcParams.update({'font.size': 18})
            plt.xlabel("Tópico 1")
            plt.ylabel("Tópico 2")
            plt.title(r"Trayectoria de las opiniones en el espacio de tópicos para $\alpha$={},dt={}, cos($\delta$)={} y N={}".format(alfa,dt,Cdelta,N))

           #----------------------------------------------------------------------------------------------

            # Voy a intentar replicar el gráfico de Baumann. Para eso voy a querer graficar la trayectoria
            # de todos los agentes. Como van a ser muchos agentes, me conviene que esas trayectorias se grafiquen
            # con líneas finitas

            OdT = dict() # OdT es Opiniones del Tópico.
            for agente in range(N):
                for topico in range(T):
                    OdT[topico+T*agente] = []
                    for iteracion in range(len(Opi)):
                        OdT[topico+T*agente].append(Opi[iteracion][agente*T+topico])

            # Esto levanta correctamente los valores de las opiniones de los agentes para cada uno de sus tópicos.
            # De paso, le agregué ahora que las listas del diccionario no se sobreescriban. Eso me va a permitir
            # graficar los puntos finales sin necesidad de revisar una segunda vez la lista Opi

            #-----------------------------------------------------------------------------------------------

            # Como todavía tengo dos tópicos, puedo graficar esto en un plano. Así que ahora voy a hacer
            # un código presuponiendo que la cantidad de tópicos es 2. Sino, esto no debería realizarse.
            # Atento a eso.
            # Como ahora las listas en el diccionario no se sobreescriben, puedo hacer esto con un for aparte
            # de lo anterior

            for agente in range(N):
                plt.plot(OdT[0+T*agente],OdT[1+T*agente], color="gray",linewidth = 0.6)

            #-------------------------------------------------------------------------------------------------

            # Genial, así como está esto ya arma el gráfico de las trayectorias de las opiniones. Ahora, me gustaría
            # colocar puntos marcando el final de mis trayectorias. Luego de eso guardo la figura y la cierro

            for agente in range(N):
                indice = Indice_Color([OdT[0+T*agente][len(OdT[0])-1],OdT[1+T*agente][len(OdT[1])-1]],Divisiones)
                plt.plot(OdT[0+T*agente][len(OdT[0])-1],OdT[1+T*agente][len(OdT[1])-1], "o" ,c = color[indice], markersize=10)

            plt.savefig("../Imagenes/Cambios dt/Trayectoria de las opiniones_alfa={}_dt={}_Cdelta={}_N={}.png".format(alfa,dt,Cdelta,N),bbox_inches = "tight")
            plt.close("Trayectoria Opiniones")

            #-------------------------------------------------------------------------------------------------

            # Esta fue la sección del gráfico de trayectorias de Opiniones, ahora debería hacer el gráfico de
            # Variación Promedio de opiniones

            #-------------------------------------------------------------------------------------------------

            # Acabo de caer en la cuenta que aunque no guarde los datos de las variaciones,
            # puedo calcularlas, total tengo todos los datos de opiniones del sistema. El renglón de
            # Var define la lista por comprensión.

            Var = [math.sqrt(np.sum(np.array([((x2-x1)**2)/len(Opi[i]) for x1,x2 in zip (Opi[i],Opi[i+1])]))) for i in range(len(Opi)-1)]
            
            
            # Para algunos valores de dt me ocurre que el sistema llega a valores de variación cero muy rápido.
            # Eso en el gráfico de logaritmo lo único que ahce es incluir muchos valores del eje x en los
            # cuales no hay nada graficado. Comprimiendo de manera artificial mi gráfico a la izquierda, y 
            # dificultando por tanto su lectura. Por ello es que al Var le voy a cortar todo valor que tenga
            # a partir de que uno de sus valores se haga cero
            for i in range(len(Var)):
                if Var[i]==0:
                    break
            Var = Var[0:i]
            
            X = np.arange(0,len(Var))*dt

            plt.figure("Variaciones Promedio")
            plt.semilogy(X,Var, "--",label=r"dt={},N={},cos($\delta$)={}".format(dt,N,Cdelta) ,linewidth = 3)
            
            # El programa sigue funcionando bárbaro, lo cual es buenísimo. Corta en el momento
            # adecuado y el comportamiento es razonbale. El guardado y el cerrado de la figura
            # lo dejo para el final del for de nombres. El tema de eso es que entonces
            # tengo que iniciar el siguiente gráfico antes de cerrar este. Eso no es un problema
            # para el código o de hacer, es sólo un tema de que dificulta un poquito más la modularidad
            # del código porque ahora las cosas se mezclan y el cierre de este módulo está al final
            
            #--------------------------------------------------------------------------------------------------
            
            # Con esto ya tengo hecho el gráfico de las variaciones promedios. Sólo necesita iterarse en todos
            # los dt para que esté hecho y se guarde. Ahora me queda entonces armar un gráfico de iteraciones 
            # en función de cos(delta) para cada alfa
            
            #--------------------------------------------------------------------------------------------------
            
            # Para este gráfico lo que voy a tener que hacer es construir mis dos vectores de valores, el de iteraciones
            # y el de DT asociado. Así que, primero que nada, voy a necesitar tener las listas creadas. Eso
            # lo voy a tener que crear en el mismo for de ALFA. Lo segundo es que esa lista no se va a armar de manera
            # ordenada. Eso es una cagada si quiero hacer el gráfico con líneas. Así que voy a tener que organizar eso,
            # fuera del for de nombres, para que todo vaya en orden creciente.
            
            Iteraciones.append(len(Opi))
            DT.append(dt)
            
            # Esto ya me arma las listas que quiero. Era muy simple la cosa
            
            #-----------------------------------------------------------------------------------------------
            
    # Ahora ordeno las listas de Iteraciones y DT. Los nombres raros que uso acá se deben a que los nombres clásicos
    # para estas variables ya están siendo usados, entonces necesito ir dándole alguna variante al nombre que me
    # distinga para qué lo uso, y que no me sobreescriba algo ya existente
    
    Xdt = list(Conjunto_dt)
    Xdt.sort()
    Yit = []
    
    for xdt in Xdt:
        for dete,It in zip(DT,Iteraciones):
            if dete==xdt:
                Yit.append(It-2000)
    
    # Esto ya me arma correctamente mis valores a graficar, ahora sólo tengo que ponerlos todos en un sólo gráfico
    
    plt.figure("Iteraciones vs dt")
    plt.loglog(Xdt,Yit,"--",label=r"$\alpha$={}".format(ALFA),linewidth = 3)
    
    # Esto me arma el gráfico de Iteraciones vs paso temporal

    #------------------------------------------------------------------------------------------------------------------
            
    # Esto me guarda el gráfico de variaciones Promedio
    plt.figure("Variaciones Promedio")
    plt.rcParams.update({'font.size': 18})
    plt.xlabel("Tiempo Simulado")
    plt.ylabel("Variación promedio de las opiniones")
    plt.axis("tight")
    plt.title(r"Variación Promedio del sistema con $\alpha$={}".format(ALFA))
    plt.legend()
    plt.grid()
    plt.savefig("../Imagenes/Cambios dt/Variaciones Promedio_alfa={}.png".format(ALFA,Cdelta,N),bbox_inches = "tight")
    plt.close("Variaciones Promedio")
    
    #------------------------------------------------------------------------------------------------------------------

# Esto me guarda el gráfico de Iteraciones vs dt    

plt.figure("Iteraciones vs dt")
plt.legend()
plt.grid()
plt.xlabel("dt")
plt.ylabel("Iteraciones")
plt.rcParams.update({'font.size': 18})
plt.title("Cantidad de iteraciones vs paso temporal")
plt.savefig("../Imagenes/Cambios dt/Iteraciones vs dt.png",bbox_inches = "tight")
plt.close("Iteraciones vs dt")


Tiempo()


# In[ ]:


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
    for ALFA in [0.05,0.06,0.07]:
        for CDELTA in Conjunto_Cdelta:
            plt.figure("Trayectoria Opiniones",figsize=(20,12))
            PuntosFinales = []
            EstadosFinales = []
            if CDELTA==0.4:
                continue
            for nombre in SuperDiccionario[AGENTES][ALFA][CDELTA]:

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
                
                # Acá voy a calcular al sujeto que voy a usar para normalizar mis gráficos. Tiene que ser el máximo
                # valor de opinión que haya alcanzado cualquier sujeto en cualquier momento.
                
                MaxNorm = 0
                for Opiniones in Opi:
                    MaxNorm = max(MaxNorm,max(np.absolute(np.array(Opiniones))))
                MaxNorm = 1/MaxNorm
                
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

                OdT = dict() # OdT es Opiniones del Tópico.
                for agente in range(N):
                    for topico in range(T):
                        OdT[topico+T*agente] = []
                        for iteracion in range(len(Opi)):
                            OdT[topico+T*agente].append(Opi[iteracion][agente*T+topico]*MaxNorm)

                # Esto levanta correctamente los valores de las opiniones de los agentes para cada uno de sus tópicos.
                # De paso, le agregué ahora que las listas del diccionario no se sobreescriban. Eso me va a permitir
                # graficar los puntos finales sin necesidad de revisar una segunda vez la lista Opi

                #-----------------------------------------------------------------------------------------------

                # Como todavía tengo dos tópicos, puedo graficar esto en un plano. Así que ahora voy a hacer
                # un código presuponiendo que la cantidad de tópicos es 2. Sino, esto no debería realizarse.
                # Atento a eso.
                # Como ahora las listas en el diccionario no se sobreescriben, puedo hacer esto con un for aparte
                # de lo anterior

                for agente in range(N):
                    plt.plot(OdT[0+T*agente],OdT[1+T*agente], color="gray",linewidth = 0.6, alpha=0.2)
                    
                #-------------------------------------------------------------------------------------------------
                
                # Voy a guardar las posiciones finales de todos mis sujetos para poder marcar los puntos finales
                # por encima de las líneas grises.
                
                PuntosFinales.append([x*MaxNorm for x in Opi[len(Opi)-1]])
                
                #-------------------------------------------------------------------------------------------------
                
                # Ahora lo que voy a hacer es tomar el estado final del sistema y usar la función EstadoFinal
                # para determinar si el sistema llegó a un Consenso, Polarización o Estado Ideológico.
                
                EstadosFinales.append(EstadoFinal(Opi[len(Opi)-1]))
                
                # Con esto me armo la lista de estados finales de mi sistema
                
                #--------------------------------------------------------------------------------------------------
                
                # Últimamente estoy teniendo unos serios problemas de consumo de memoria. Voy a probar el reducir
                # este consumo explícitamente mandando las listas y cosas que no uso a None. Por lo que leí
                # eso es mejor que hacer delete.
                
                Datos = None
                Ady = None
                Sup = None
                Opi = None
                MaxNorm = None
                OdT = None
                
                # Hecho estoy, voy a borrar las cosas que van por fuera de esto. Así que voy a crear una segunda parte
                # para direccionar a None más cosas.
                
            #--------------------------------------------------------------------------------------------------
            
            # Ahora, quedaría preguntarse: ¿Puede pasar que un sistema esté en dos estados al mismo tiempo?
            # Considerá que estamos mirando 40 instancias de un sistema con los mismo parámetros.
            # Este problema tendría más sentido si ocurre que en un caso el sistema cae al consenso y
            # en otro se polariza de alguna forma. En ese caso, le diré al sistema que el estado
            # prevalente es el que haya aparecido más veces.
            
            ConjEF = set(EstadosFinales) # Es el conjunto de estados finales
            Maxestados = 0
            ResultadoEF = EstadosFinales[0]
            for estado in ConjEF:
                Maxestados = max(Maxestados,EstadosFinales.count(estado))
                if Maxestados==EstadosFinales.count(estado):
                    ResultadoEF = estado
                    
            Maxestados = None
                        
            # Tuve problemas en pensar los nombres de estas cosas, en el futuro seguramente se los cambie.
            # Porque de verdad no sé cómo llamarlo y se me agotaron los nombres.

            #-------------------------------------------------------------------------------------------------

            # Genial, así como está esto ya arma el gráfico de las trayectorias de las opiniones. Ahora, me gustaría
            # colocar puntos marcando el final de mis trayectorias.

            for iteracion in range(len(PuntosFinales)):
                for agente in range(N):
                    indice = Indice_Color([PuntosFinales[iteracion][0+T*agente],PuntosFinales[iteracion][1+T*agente]],Divisiones)
                    plt.plot(PuntosFinales[iteracion][0+T*agente],PuntosFinales[iteracion][1+T*agente], "o" ,c = color[indice], markersize=10)

            indice = None

            #----------------------------------------------------------------------------------------------

            # Estos son los parámetros que definen el tamaño del gráfico, tamaño de la letra y nombres de
            # los ejes. Luego de eso guardo la figura y la cierro

            plt.rcParams.update({'font.size': 18})
            plt.xlabel("Tópico 1")
            plt.ylabel("Tópico 2")
            plt.title(r"Trayectoria de las opiniones en el espacio de tópicos para $\alpha$={},cos($\delta$)={} y N={}".format(ALFA,CDELTA,AGENTES))
            xmin,xmax = plt.xlim()
            ymin,ymax = plt.ylim()
            plt.text((xmax+xmin)/2*0.9,ymax*0.9,ResultadoEF, bbox=dict(facecolor='White', alpha=0.7))
            plt.savefig("../Imagenes/ER2/Trayectoria de las opiniones_alfa={}_Cdelta={}_N={}.png".format(ALFA,CDELTA,AGENTES),bbox_inches = "tight")
            plt.close("Trayectoria Opiniones")
#             plt.show()

            #-------------------------------------------------------------------------------------------------
    
            # Voy a seguir borrando algunas cosas acá.
        
            PuntosFinales = None
            EstadosFinales = None
            ConjEF = None
            ResultadoEF = None
            
            #-------------------------------------------------------------------------------------------------
        
            
        Tiempo()


#-------------------------------------------------------------------------------------------------

# Borro lo último acá

Conjunto_Alfa = None
Conjunto_Cdelta = None
Conjunto_N = None
SuperDiccionario = None


#-------------------------------------------------------------------------------------------------
        
        
        
Tiempo()


# In[21]:


print(EstadosFinales)
print(EstadosFinales.count("Consenso"))

