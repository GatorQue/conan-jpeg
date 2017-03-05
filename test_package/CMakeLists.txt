PROJECT(MyHello)
cmake_minimum_required(VERSION 2.8)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
CONAN_BASIC_SETUP()

find_package("JPEG")

IF(JPEG_FOUND)
    ADD_EXECUTABLE(testpkg testpkg.c)
    include_directories(${JPEG_INCLUDE_DIRS})
    TARGET_LINK_LIBRARIES(testpkg ${JPEG_LIBRARIES})
ELSE()
    MESSAGE(FATAL_ERROR "JPEG not found")
ENDIF()
