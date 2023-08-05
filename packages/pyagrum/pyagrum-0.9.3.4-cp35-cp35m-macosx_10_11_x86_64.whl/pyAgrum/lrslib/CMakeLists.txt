project (lrslib)

set (LRSLIB_SOURCE_DIR ${CMAKE_CURRENT_SOURCE_DIR}/src)
set (LRSLIB_BINARY_DIR ${CMAKE_CURRENT_BINARY_DIR})

set (LRSLIB_FILES ${LRSLIB_SOURCE_DIR}/lrslib/lrslib.c ${LRSLIB_SOURCE_DIR}/lrslib/lrsmp.c)

add_library(lrs STATIC ${LRSLIB_FILES})

