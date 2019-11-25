cmake_minimum_required(VERSION 3.5)
project(test_package)

set(CMAKE_CXX_STANDARD 11)

include(${CMAKE_BINARY_DIR}/conan_paths.cmake)

find_package(Lua 5.2.3 CONFIG REQUIRED)

add_executable(lua_test ${CMAKE_CURRENT_SOURCE_DIR}/../test_package/lua_test.cpp)
target_link_libraries(lua_test PUBLIC lua::lua_lib)
add_test(lua_test lua_test)
