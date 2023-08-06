// Lists the registration functions for all the modules

#include "lua.h"

LUALIB_API int luaopen_libinjection(lua_State *L);
LUALIB_API int luaopen_utf8(lua_State *L);
LUALIB_API int luaopen_lpeg (lua_State *L);
LUALIB_API int luaopen_cmsgpack(lua_State *L);
LUALIB_API int luaopen_snapshot(lua_State *L);
LUALIB_API int luaopen_sha1(lua_State *L);
LUALIB_API int luaopen_sha256(lua_State *L);
LUALIB_API int luaopen_cpuload(lua_State *L);
LUALIB_API int luaopen_loadavg(lua_State* L);
LUALIB_API int luaopen_meminfo(lua_State *L);
LUALIB_API int luaopen_luaos(lua_State *L);
LUALIB_API int luaopen_sysutils(lua_State *L);

