# Place for all the compile/linker flags so we get a consistent build

##############################################################################
# Host system detection.
##############################################################################

ifeq (Windows,$(findstring Windows,$(OS))$(MSYSTEM)$(TERM))
  HOST_SYS= Windows
  HOST_RM= del
else
  HOST_SYS:= $(shell uname -s)
  ifneq (,$(findstring MINGW,$(HOST_SYS)))
    HOST_SYS= Windows
    HOST_MSYS= mingw
  endif
  ifneq (,$(findstring CYGWIN,$(HOST_SYS)))
    HOST_SYS= Windows
    HOST_MSYS= cygwin
  endif
  # Use Clang for OSX host.
  ifeq (Darwin,$(HOST_SYS))
    DEFAULT_CC= clang
  endif
endif

CROSS =
CC = $(CROSS)cc
AR = $(CROSS)ar

UNSAFE_FLAG = -DLUA_UNSAFE_MODE

# There is a huge performance advantage compiling sha1.c with just -O
# -O2 or -O3 *reduce* the speed of the algorithm 30%
OPTIMIZE_NONE = -O
OPTIMIZE_FULL = -O3

INCS = -Iext -Iext/luajit/src
LIBS = -lm
ifneq (mingw, $(HOST_MSYS))
	LIBS += -ldl
endif

ifneq ($(strip $(CXX_SRC)),)
	LIBS += -lstdc++
endif



XCFLAGS =
CFLAGS = -DLUA_USE_APICHECK -DLUAJIT -Dlua_assert=assert -Wall -fPIC ${INCS} ${XCFLAGS}
CXXFLAGS = -std=c++11 ${CFLAGS}
LDFLAGS = 


LUAJIT_XCFLAGS = -fPIC
ifeq (${HOST_SYS}, Darwin)
	# Disable the JIT on OS X
	LUAJIT_XCFLAGS += -DLUAJIT_ENABLE_GC64
endif
