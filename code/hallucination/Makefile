all: libalign.so

libalign.so: align.c
	gcc -O3 -Wall -Wextra -shared -fPIC align.c -o libalign.so

clean:
	/bin/rm src/libalign.so
