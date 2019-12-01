cmake_minimum_required(VERSION 3.5)
project(test_package)

set(CMAKE_CXX_STANDARD 11)

include(${CMAKE_BINARY_DIR}/conan_paths.cmake)

find_package(bgfx CONFIG REQUIRED)
find_package(SDL2 CONFIG REQUIRED)

add_executable(bgfx_test ${CMAKE_CURRENT_SOURCE_DIR}/../test_package/bgfx_test.cpp)
target_link_libraries(bgfx_test PUBLIC SDL2::SDL2-static bgfx::bgfx)
