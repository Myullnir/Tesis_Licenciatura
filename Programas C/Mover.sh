#!/bin/bash
# Este programa lo voy a usar para mover los archivos de datos a la carpeta de Python.
# Y también para convertirlos en txt

for nombre in Datos_*
do
	mv $nombre ../"Programas Python"/"Modelo Erdos-Renyi"/$nombre
done
