all: data base proc

data:
	bash collect.sh
	bash unzip.sh

base:
	bash construct.sh
	bash newyears.sh
	bash proc.sh

proc:
	python combine.py > ov.txt
	python wool.py

overview:
	python overview.py
