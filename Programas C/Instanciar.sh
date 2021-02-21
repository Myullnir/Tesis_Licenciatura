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
	for Alfa in {0..10}
	do
		for Delta in {0..90..3}
		do
			./$1.e $Alfa $Delta
		done
	done
	
	./Mover.sh

fi
