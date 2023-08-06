MODULES := \
	ext/libinjection \
	ext/lpeg \
	ext/lua-cmsgpack \
	ext/lua-snapshot \
	ext/luautf8 \
	ext/perf \
	ext/sha1 \
	ext/sha2 \
	ext/sysutils

SRC += \
	ext/all.c
	
include $(patsubst %,%/module.mk,$(MODULES))
