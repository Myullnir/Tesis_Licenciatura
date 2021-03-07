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
	for Alfa in {0..5..1}
	do
		./$1.e 100 $Alfa 2
	done
	
	./Mover.sh

fi
