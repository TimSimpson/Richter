cmake_minimum_required(VERSION 3.5)
project(test_package)

set(CMAKE_CXX_STANDARD 11)

enable_testing()

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup(TARGETS)

add_executable(lua_test ${CMAKE_CURRENT_SOURCE_DIR}/lua_test.cpp)
target_link_libraries(lua_test CONAN_PKG::Lua)
add_test(lua_test lua_test)
