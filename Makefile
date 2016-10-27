all:
	./pbs.sh

pbs:
	rm -f ./ece.*
	qsub pbs.sh
