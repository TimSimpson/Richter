cmake_minimum_required(VERSION 3.5)
project(test_package)

set(CMAKE_CXX_STANDARD 11)

# include(${CMAKE_BINARY_DIR}/conan_paths.cmake)


# include(/home/tim/.conan/data/Lua/5.2.3/_/_/package/5ab84d6acfe1f23c4fae0ab88f26e3a396351ac9/lib/cmake/Lua/LuaConfig.cmake)
#/home/tim/.conan/data/Lua/5.2.3/_/_/package/5ab84d6acfe1f23c4fae0ab88f26e3a396351ac9

# set(CMAKE_PREFIX_PATH /home/tim/.conan/data/Lua/5.2.3/_/_/package/5ab84d6acfe1f23c4fae0ab88f26e3a396351ac9)
include(${CMAKE_BINARY_DIR}/conan_paths.cmake)

include(CMakePackageConfigHelpers)

# find_package(Lua REQUIRED)
find_package(Lua CONFIG REQUIRED)

if(NOT TARGET lua::lua_lib)
    MESSAGE(FATAL_ERROR "Well this won't worK!!!!!!!!!!!!!!!!!!!!!")
endif()

# include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
# conan_basic_setup(TARGETS)


# find_package(Lua)

add_executable(lua_test ${CMAKE_CURRENT_SOURCE_DIR}/../test_package/lua_test.cpp)
target_link_libraries(lua_test PUBLIC lua::lua_lib)
add_test(lua_test lua_test)
