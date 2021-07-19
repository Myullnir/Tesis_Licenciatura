#!/bin/bash
# Este programa lo voy a usar para poder correr los programas de C
# y que sean programas separados, de manera de que me tire el tiempo que tardó
# en cada uno. Porque sino tengo que andar mirando los tiempos en los archivos.

make clean
make all

echo Apreta enter para correr, sino primero apreta alguna letra y despues enter
read decision

if [ -z $decision ]
then
	for N in 1000
	do
		for Alfa in 2
		do
			for Cdelta in {0..10}
			do
				echo Alfa = $Alfa, Cdelta = $Cdelta
				for iteracion in {20..60}
				do
					./$1.e $N $Alfa $Cdelta $iteracion
				done
			done
		done
	done
	
	# ./Mover.sh

fi


