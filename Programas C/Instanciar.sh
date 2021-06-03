#!/bin/bash
# Este programa lo voy a usar para poder correr los programas de C
# y que sean programas separados, de manera de que me tire el tiempo que tardó
# en cada uno. Porque sino tengo que andar mirando los tiempos en los archivos.

make clean
make all

echo Apreta enter para correr, sino primero apreta alguna letra y despues enter
read decision

Redes='RandomR'

if [ -z $decision ]
then
	for N in 1000
	do
		for Red in $Redes
		do
			for Alfa in {0..20}
			do
				for Cdelta in {0..10}
				do
					for Gm in {4..16..4}
					do
						echo Alfa = $Alfa, Cdelta = $Cdelta, Red = $Red, Gm = $Gm
						for iteracion in {0..10}
						do 
							./$1.e $N $Red $Alfa $Cdelta $Gm $iteracion
						done
					done
				done
			done
		done
	done
	
	# ./Mover.sh

fi


