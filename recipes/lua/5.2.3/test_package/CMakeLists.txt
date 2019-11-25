cmake_minimum_required(VERSION 3.5)
project(test_package)

set(CMAKE_CXX_STANDARD 11)

enable_testing()

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup(TARGETS)

# find_package(Lua)

add_executable(lua_test lua_test.cpp)
target_link_libraries(lua_test CONAN_PKG::Lua)
add_test(lua_test lua_test)
