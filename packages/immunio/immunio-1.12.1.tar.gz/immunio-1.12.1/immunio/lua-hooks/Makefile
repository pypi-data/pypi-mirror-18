MODULES := lib ext

# Source of extensions compiled w/ Lua's source.
# Only include .c files that can't be directly included in ext/all.c.

# All these source variables are filled in by the module.mk files
SRC :=

CXX_SRC :=

SPECIAL_SRC :=

LUA_SRC :=

CLI_SRC := \
	ext/luajit/src/luajit.c

# Include module definitions
include $(patsubst %,%/module.mk,$(MODULES))

OBJ := \
	$(patsubst %.c,%.o,$(filter %.c,$(SRC))) \

SPECIAL_OBJ := \
	$(patsubst %.c,%.o,$(filter %.c,$(SPECIAL_SRC))) \

CXX_OBJ := \
	$(patsubst %.cc,%.o,$(filter %.cc,$(CXX_SRC)))

CLI_OBJ := \
	$(patsubst %.c,%.o,$(filter %.c,$(CLI_SRC)))


# CLI for running tests
CLI = ./lua

# Library archive. Used for compiling along agent bindings.
SO_OUT = libimmunio.so
A_OUT = libimmunio.a

include options.mk

INIT_HOOK = hooks/__init__.lua
HOOK_SRCS := $(wildcard hooks/*.lua) hooks/__init__.lua
MIN_SRCS = $(HOOK_SRCS:hooks/%.lua=build/%.lua)
HOOKS_TARBALL = hooks.tgz
HOOKS_SRCS_TARBALL = hooks_srcs.tgz

LUAJIT_OUT = libluajit.a
LUAJIT_OBJ = ext/luajit/src/${LUAJIT_OUT}

# Build lua, run tests, and create hooks archive
all: ${CLI} ${INIT_HOOK} ${HOOKS_TARBALL} ${HOOKS_SRCS_TARBALL}

${SO_OUT}: ${OBJ} ${SPECIAL_OBJ} ${LUAJIT_OBJ}
	${CC} -shared ${CFLAGS} ${LIBS} -o $@ -lc $^

${A_OUT}: ${OBJ} ${SPECIAL_OBJ}
	${AR} -rcus $@ $^

${LUAJIT_OUT}: ${LUAJIT_OBJ}
	cp $^ $@

${LUAJIT_OBJ}:
	cd ext/luajit/src && MACOSX_DEPLOYMENT_TARGET="10.8" make CROSS="${CROSS}" CC=cc HOST_CC=cc XCFLAGS="${LUAJIT_XCFLAGS}" ${LUAJIT_OUT}

# Build lua executable for testing and compilation
# Seperate compilation as we need the LUA_UNSAFE_MODE flag set...
${CLI}: CFLAGS += ${UNSAFE_FLAG}
${CLI}: CXXFLAGS += ${UNSAFE_FLAG}
${CLI}: ${CLI_SRC} ${SRC} ${SPECIAL_OBJ} ${CXX_OBJ} ${LUAJIT_OBJ}
	${CC} ${CFLAGS} ${LDFLAGS} -o $@ $^ ${LIBS}

# Concatenate init hooks into one __init__.lua hook with two newlines in between
${INIT_HOOK}: ${LUA_SRC} ${CLI}
	rm -f hooks/__init__.lua
	${CLI} ./luald.lua ${LUA_SRC} > hooks/__init__.lua

build/%.lua: hooks/%.lua ${CLI}
	@mkdir -p build
	@echo Minifying $<
	@cd LuaMinify; ../lua CommandLineMinify.lua ../$< ../$@ >/dev/null

# Create tarball of hooks to publish
${HOOKS_TARBALL}: ${MIN_SRCS}
	tar -czf $@ -C build .

${HOOKS_SRCS_TARBALL}: ${HOOK_SRCS}
	tar -czf $@ -C hooks . --exclude="init"

${SPECIAL_OBJ}: CFLAGS += ${OPTIMIZE_NONE}

${CLI_OBJ} ${OBJ} ${CXX_OBJ} ${LUAJIT_OBJ}: CFLAGS += ${OPTIMIZE_FULL}

%.o: %.c
	${CC} ${CFLAGS} -c ${INCS} -o $@ $<

%.o: %.cc
	${CXX} ${CXXFLAGS} -c ${INCS} -o $@ $<

cleanhooks:
	rm -f ${INIT_HOOK}
	rm -f build/*.lua

clean: cleanhooks
	rm -f ${CLI} ${CLI_OBJ} ${OBJ} ${CXX_OBJ} ${SPECIAL_OBJ} ${SO_OUT} ${A_OUT} ${LUAJIT_OUT}
	cd ext/luajit && make clean
	rm -f test_failed
	rm -rf build
	find . -name \*.o -delete

test: ${CLI} ${INIT_HOOK} lint ${MIN_SRCS}
	@rm -f test_failed
	@for file in test/*_test.lua; do \
		printf "\nRunning $$file\n"; \
		TEST_BUILT_HOOKS=1 ${CLI} -e 'package.path="./LuaMinify/?.lua;" .. package.path' -l 'Strict' $$file || touch test_failed; \
	done
	@test ! -f test_failed

enable-console: cleanhooks
	git update-index --assume-unchanged lib/term.lua
	cp lib/term.lua.dev lib/term.lua
	make

lint: ${INIT_HOOK}
	@# Scan all lua files for lines with trailing spaces
	@# The leading `!` negates the logic, so this target fails if trailing
	@# spaces are found in any Lua file.
	@! find . -path ./LuaMinify -prune -o -name "*.lua" -exec grep -E -n "[[:space:]]+$$" {} +

.PHONY: all test clean lint
