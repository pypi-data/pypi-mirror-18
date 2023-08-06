#define LUA_LIB
#include <lua.h>
#include <lauxlib.h>

#ifdef _WIN32
#define WIN32_LEAN_AND_MEAN
#include <windows.h>
#else
#include <sys/utsname.h>
#endif /* _WIN32 */

static int lua_uname(lua_State *L)
{
#ifdef _WIN32
  const char *name;
  SYSTEM_INFO info;
  lua_pushliteral(L, "Windows");
  name = getenv("COMPUTERNAME");
  lua_pushstring(L, name ? name : "");
  memset(&info, 0, sizeof(info));
  GetSystemInfo(&info);
  if (info.wProcessorArchitecture == PROCESSOR_ARCHITECTURE_AMD64)
    lua_pushliteral(L, "AMD64");
  else if (info.wProcessorArchitecture == PROCESSOR_ARCHITECTURE_INTEL)
    lua_pushliteral(L, "X86");
  else if (info.wProcessorArchitecture == PROCESSOR_ARCHITECTURE_ARM)
    lua_pushliteral(L, "ARM");
  else if (info.wProcessorArchitecture == PROCESSOR_ARCHITECTURE_IA64)
    lua_pushliteral(L, "IA64");
  else if (info.wProcessorArchitecture == PROCESSOR_ARCHITECTURE_IA64)
    lua_pushstring(L, "");
  return 3;
#else
  struct utsname info;
  if (uname(&info) >= 0)
  {
    lua_pushstring(L, info.sysname);
    lua_pushstring(L, info.nodename);
    lua_pushstring(L, info.machine);
    return 3;
  }
  lua_pushstring(L, "Unknown");
  return 1;
#endif
}

static const luaL_Reg sys_utils[] = {
  {"uname", lua_uname},
  {NULL, NULL}
};

int luaopen_sysutils(lua_State *L) {
//  luaL_checkversion(L);
  luaL_register(L, "sysutils", sys_utils);
  return 1;
}
