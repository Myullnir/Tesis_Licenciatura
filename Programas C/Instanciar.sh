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
		for Alfa in 90
		do
			for Cdelta in 6
			do
				echo Estoy trabajando el alfa $Alfa y el Cdelta $Cdelta
				for iteracion in {101..200}
				do
					./$1.e $N $Alfa $Cdelta $iteracion
				done
			done
		done
	done
	
	./Mover.sh

fi
