cmake_minimum_required(VERSION 3.5)
project(loguru)

option(LOGURU_STATIC ON)
option(LOGURU_USE_FMTLIB OFF)

set(CMAKE_CXX_STANDARD 11)
set(src loguru.cpp loguru.hpp)

if (LOGURU_STATIC)
    message("-- loguru: building a static library")
    add_library(loguru STATIC ${src})
else ()
    message("-- loguru: building a shared library")
    add_library(loguru SHARED ${src})
endif ()

if (LOGURU_USE_FMTLIB)
    message("-- loguru: using fmtlib")
    target_compile_definitions(loguru PUBLIC -DLOGURU_USE_FMTLIB)
endif ()

install(TARGETS loguru)
