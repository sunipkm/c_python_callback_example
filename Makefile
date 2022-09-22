all: libsrc.c
	gcc -dynamiclib -fPIC -O2 -o libsrc.dylib $<