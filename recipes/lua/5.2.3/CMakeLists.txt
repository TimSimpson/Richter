project(Lua C CXX)

cmake_minimum_required(VERSION 3.2 FATAL_ERROR)
include(CMakePackageConfigHelpers)

add_library(lua_lib
    "${CMAKE_CURRENT_SOURCE_DIR}/src/lauxlib.h"
    "${CMAKE_CURRENT_SOURCE_DIR}/src/ldo.h"
    "${CMAKE_CURRENT_SOURCE_DIR}/src/lfunc.h"
    "${CMAKE_CURRENT_SOURCE_DIR}/src/llex.h"
    "${CMAKE_CURRENT_SOURCE_DIR}/src/lopcodes.h"
    "${CMAKE_CURRENT_SOURCE_DIR}/src/lparser.h"
    "${CMAKE_CURRENT_SOURCE_DIR}/src/lua.hpp"
    "${CMAKE_CURRENT_SOURCE_DIR}/src/lundump.h"
    "${CMAKE_CURRENT_SOURCE_DIR}/src/lapi.h"
    "${CMAKE_CURRENT_SOURCE_DIR}/src/lcode.h"
    "${CMAKE_CURRENT_SOURCE_DIR}/src/lctype.h"
    "${CMAKE_CURRENT_SOURCE_DIR}/src/ldebug.h"
    "${CMAKE_CURRENT_SOURCE_DIR}/src/llimits.h"
    "${CMAKE_CURRENT_SOURCE_DIR}/src/lmem.h"
    "${CMAKE_CURRENT_SOURCE_DIR}/src/lobject.h"
    "${CMAKE_CURRENT_SOURCE_DIR}/src/lstring.h"
    "${CMAKE_CURRENT_SOURCE_DIR}/src/ltable.h"
    "${CMAKE_CURRENT_SOURCE_DIR}/src/ltm.h"
    "${CMAKE_CURRENT_SOURCE_DIR}/src/luaconf.h"
    "${CMAKE_CURRENT_SOURCE_DIR}/src/lualib.h"
    "${CMAKE_CURRENT_SOURCE_DIR}/src/lzio.h"
    "${CMAKE_CURRENT_SOURCE_DIR}/src/lgc.h"
    "${CMAKE_CURRENT_SOURCE_DIR}/src/lstate.h"
    "${CMAKE_CURRENT_SOURCE_DIR}/src/lua.h"
    "${CMAKE_CURRENT_SOURCE_DIR}/src/lvm.h"

    "${CMAKE_CURRENT_SOURCE_DIR}/src/lapi.c"
    "${CMAKE_CURRENT_SOURCE_DIR}/src/lcode.c"
    "${CMAKE_CURRENT_SOURCE_DIR}/src/lctype.c"
    "${CMAKE_CURRENT_SOURCE_DIR}/src/ldebug.c"
    "${CMAKE_CURRENT_SOURCE_DIR}/src/linit.c"
    "${CMAKE_CURRENT_SOURCE_DIR}/src/lmem.c"
    "${CMAKE_CURRENT_SOURCE_DIR}/src/lobject.c"
    "${CMAKE_CURRENT_SOURCE_DIR}/src/lstring.c"
    "${CMAKE_CURRENT_SOURCE_DIR}/src/ltable.c"
    "${CMAKE_CURRENT_SOURCE_DIR}/src/ltm.c"
    "${CMAKE_CURRENT_SOURCE_DIR}/src/lzio.c"
    "${CMAKE_CURRENT_SOURCE_DIR}/src/lbaselib.c"
    "${CMAKE_CURRENT_SOURCE_DIR}/src/ldump.c"
    "${CMAKE_CURRENT_SOURCE_DIR}/src/lgc.c"
    "${CMAKE_CURRENT_SOURCE_DIR}/src/liolib.c"
    "${CMAKE_CURRENT_SOURCE_DIR}/src/loslib.c"
    "${CMAKE_CURRENT_SOURCE_DIR}/src/lstate.c"
    "${CMAKE_CURRENT_SOURCE_DIR}/src/lvm.c"

    "${CMAKE_CURRENT_SOURCE_DIR}/src/lauxlib.c"
    "${CMAKE_CURRENT_SOURCE_DIR}/src/lbitlib.c"
    "${CMAKE_CURRENT_SOURCE_DIR}/src/lcorolib.c"
    "${CMAKE_CURRENT_SOURCE_DIR}/src/ldblib.c"
    "${CMAKE_CURRENT_SOURCE_DIR}/src/ldo.c"
    "${CMAKE_CURRENT_SOURCE_DIR}/src/lfunc.c"
    "${CMAKE_CURRENT_SOURCE_DIR}/src/llex.c"
    "${CMAKE_CURRENT_SOURCE_DIR}/src/lmathlib.c"
    "${CMAKE_CURRENT_SOURCE_DIR}/src/loadlib.c"
    "${CMAKE_CURRENT_SOURCE_DIR}/src/lopcodes.c"
    "${CMAKE_CURRENT_SOURCE_DIR}/src/lparser.c"
    "${CMAKE_CURRENT_SOURCE_DIR}/src/lstrlib.c"
    "${CMAKE_CURRENT_SOURCE_DIR}/src/ltablib.c"
    "${CMAKE_CURRENT_SOURCE_DIR}/src/lundump.c"
)

# sets "-lm", but only where it's needed.

find_library(found_math_lib m)

if (found_math_lib)
    target_link_libraries(lua_lib PUBLIC m)
endif()

# These are the only headers to install according to the makefile:
# lua.h luaconf.h lualib.h lauxlib.h lua.hpp

set_target_properties(lua_lib PROPERTIES OUTPUT_NAME "lua_lib")

target_include_directories(lua_lib
    PUBLIC
        $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
        $<INSTALL_INTERFACE:include/lua>
    PRIVATE
        src)

install(FILES
    "${CMAKE_CURRENT_SOURCE_DIR}/src/luaconf.h"
    "${CMAKE_CURRENT_SOURCE_DIR}/src/lua.h"
    "${CMAKE_CURRENT_SOURCE_DIR}/src/lua.hpp"
    "${CMAKE_CURRENT_SOURCE_DIR}/src/lualib.h"
    "${CMAKE_CURRENT_SOURCE_DIR}/src/lauxlib.h"
    DESTINATION include/lua5.2.3)

install(TARGETS lua_lib EXPORT Lua-targets
    RUNTIME DESTINATION bin
    LIBRARY DESTINATION lib
    ARCHIVE DESTINATION lib
    INCLUDES DESTINATION include.lua5.2.3
)

add_library(lua::lua ALIAS lua_lib)
install(EXPORT Lua-targets
    FILE Lua-targets.cmake
    NAMESPACE lua::
    DESTINATION lib/cmake/Lua_5.2.3
)

file(WRITE "${PROJECT_BINARY_DIR}/Lua-config.cmake" "
include(\"\${CMAKE_CURRENT_LIST_DIR}/Lua-targets.cmake\")
")

write_basic_package_version_file("${PROJECT_BINARY_DIR}/Lua-config-version.cmake"
    VERSION 5.2.3
    COMPATIBILITY AnyNewerVersion
)

install(FILES
    "${PROJECT_BINARY_DIR}/Lua-config.cmake"
    "${PROJECT_BINARY_DIR}/Lua-config-version.cmake"
    DESTINATION lib/cmake/Lua
)

add_executable(lua "${CMAKE_CURRENT_SOURCE_DIR}/src/lua.c")
target_link_libraries(lua lua_lib)

add_executable(luac ${CMAKE_CURRENT_SOURCE_DIR}/src/luac.c)
target_link_libraries(luac lua_lib)

