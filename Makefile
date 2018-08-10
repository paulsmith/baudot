all: baudot

charmap.c: code.py baudot.txt
	python3 code.py baudot.txt > $@

baudot: charmap.c baudot.c
	cc -Wall -o $@ baudot.c
