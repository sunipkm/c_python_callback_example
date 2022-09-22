all: libsrc.c
	gcc -dynamiclib -fPIC -O2 `pkg-config libczmq --cflags` -o libsrc.dylib $< `pkg-config libczmq --libs`
	gcc -O2 `pkg-config libczmq --cflags` -o libsrc.out $< `pkg-config libczmq --libs`