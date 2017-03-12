PROJECT(conanjpeg)
cmake_minimum_required(VERSION 2.8)
include(${CMAKE_BINARY_DIR}/../conanbuildinfo.cmake)
CONAN_BASIC_SETUP()

if(MSVC)
    add_definitions(-D_CRT_SECURE_NO_DEPRECATE)
    add_definitions(-D_CRT_NONSTDC_NO_DEPRECATE)
endif()

set(LIB_VERSION_MAJOR 9)
set(LIB_VERSION_MINOR 2)
set(LIB_VERSION ${LIB_VERSION_MAJOR}.${LIB_VERSION_MINOR})

set(LIB_SOURCES jaricom.c jcapimin.c jcapistd.c jcarith.c jccoefct.c jccolor.c
        jcdctmgr.c jchuff.c jcinit.c jcmainct.c jcmarker.c jcmaster.c
        jcomapi.c jcparam.c jcprepct.c jcsample.c jctrans.c jdapimin.c
        jdapistd.c jdarith.c jdatadst.c jdatasrc.c jdcoefct.c jdcolor.c
        jddctmgr.c jdhuff.c jdinput.c jdmainct.c jdmarker.c jdmaster.c
        jdmerge.c jdpostct.c jdsample.c jdtrans.c jerror.c jfdctflt.c
        jfdctfst.c jfdctint.c jidctflt.c jidctfst.c jidctint.c jquant1.c
        jquant2.c jutils.c jmemmgr.c)

# Add system-dependent memory manager file (recommend jmemnobs for NT)
set(LIB_SOURCES ${LIB_SOURCES} jmemnobs.c)

configure_file(jconfig.vc include/jconfig.h COPYONLY)
include_directories(${PROJECT_BINARY_DIR}/include)

set(LIB_PUBLIC_HEADERS jerror.h jmorecfg.h jpeglib.h
    ${PROJECT_BINARY_DIR}/include/jconfig.h)

install(FILES ${LIB_PUBLIC_HEADERS} DESTINATION include)

add_library(jpeg ${LIB_SOURCES})

set_target_properties(jpeg PROPERTIES SOVERSION ${LIB_VERSION_MAJOR})
if(NOT CYGWIN)
    # This property causes shared libraries on Linux to have the full version
    # encoded into their final filename.  We disable this on Cygwin because
    # it causes cygz-${ZLIB_FULL_VERSION}.dll to be created when cygz.dll
    # seems to be the default.
    set_target_properties(jpeg PROPERTIES VERSION ${LIB_VERSION})
endif()

install(TARGETS jpeg
        RUNTIME DESTINATION bin
        ARCHIVE DESTINATION lib
        LIBRARY DESTINATION lib)

