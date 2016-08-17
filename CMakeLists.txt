CMAKE_MINIMUM_REQUIRED(VERSION 2.6)

## Set compiler
#IF(APPLE)
#    SET(CMAKE_C_COMPILER "clang")
#    SET(CMAKE_CXX_COMPILER "clang++")
#ELSEIF(UNIX)
#    SET(CMAKE_C_COMPILER "gcc")
#    SET(CMAKE_CXX_COMPILER "g++")
#ELSEIF(WIN32)
#    # TODO: not how the code would work on Windows.
#ENDIF()

PROJECT(PyMesh_Depends)

#INCLUDE(Settings.cmake)

# Process code in each subdirectories
ADD_SUBDIRECTORY(clipper)
ADD_SUBDIRECTORY(cork)
ADD_SUBDIRECTORY(qhull-master)
ADD_SUBDIRECTORY(tetgen)
ADD_SUBDIRECTORY(triangle)
