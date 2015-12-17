cmake_minimum_required(VERSION 2.8)
project(Meido-san)

set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11")


file(GLOB M_SRC "*.h" "*.cpp")

add_executable(Meido-san main.cpp ${M_SRC})

set(EXECUTABLE_NAME "Test_Meido_san")
