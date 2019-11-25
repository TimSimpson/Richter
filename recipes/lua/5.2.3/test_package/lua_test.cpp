#include <iostream>
#include <string>
#include <lua.hpp>

const std::string LUA_CODE = "require 'os'; print('This is Lua from within the test program.')";


int main() {
    lua_State * L = luaL_newstate();
    luaL_openlibs(L);
    int error = luaL_loadbuffer(L, LUA_CODE.c_str(), LUA_CODE.size(),
                                "hello-lua.cpp")
                || lua_pcall(L, 0, 0, 0);
    if (error)
    {
        std::cerr << "An error occured within Lua:"
            << lua_tostring(L, -1) << std::endl;
    }
    lua_close(L);
    return error;
}
