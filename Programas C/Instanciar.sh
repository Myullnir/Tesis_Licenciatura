#!/bin/bash
# Este programa lo voy a usar para poder correr los programas de C
# y que sean programas separados, de manera de que me tire el tiempo que tardó
# en cada uno. Porque sino tengo que andar mirando los tiempos en los archivos.

make all

echo Apreta enter para correr, sino primero apreta alguna letra y despues enter
read decision

if [ -z $decision ]
then
	for N in {2..15}
	do
		for K in {0..5}
		do
			./$1.e $N $K
		done
	done

	./Mover.sh
fi
