#!/bin/bash
# Este programa lo voy a usar para poder correr los programas de C
# y que sean programas separados, de manera de que me tire el tiempo que tardó
# en cada uno. Porque sino tengo que andar mirando los tiempos en los archivos.

# make clean
# make all

# echo Apreta enter para correr, sino primero apreta alguna letra y despues enter
# read decision

echo "El ID del script es $$"

if [ -z $decision ]
then
	for N in 1000
	do
		for iteracion in {0..30}
		do
			Alfa=$2
			while [ $Alfa -le $3 ]
			do
				for Cdelta in {-5..5}
				do
					echo Alfa = $Alfa, Cdelta = $Cdelta
					./$1.e $N $Alfa $Cdelta $iteracion
				done
			((Alfa++))
			done
			echo Complete $iteracion simulaciones totales
		done
	done

fi


