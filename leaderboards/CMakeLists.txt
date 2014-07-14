cmake_minimum_required (VERSION 2.8)

project (leaderboards)

if (CMAKE_COMPILER_IS_GNUCC OR CMAKE_COMPILER_IS_GNUCXX)
	add_definitions(-Wall)
endif()

if (NOT WIN32)
	add_definitions("-std=c++0x")
endif()

if (NOT WIN32)
	include(FindProtobuf)
	find_package(Protobuf REQUIRED)
	include_directories(${PROTOBUF_INCLUDE_DIR})
endif ()

include_directories (
	${PROJECT_SOURCE_DIR}/../common
	${PROJECT_SOURCE_DIR}/../../ext-deps/protobuf-2.5.0/vsprojects/include
	${PROJECT_SOURCE_DIR}/../lmdb_win_include
	${PROJECT_SOURCE_DIR}/../../ext-deps/openldap-2.4.39/libraries/liblmdb
	${PROJECT_SOURCE_DIR}/../../ext-deps/EASTL/include
)

set (LEADERBOARDS_SOURCES
	leaderboards.cpp
	../database/database.pb.cc
	../database/lmdb_helper.cpp
	../../ext-deps/openldap-2.4.39/libraries/liblmdb/mdb.c
	../../ext-deps/openldap-2.4.39/libraries/liblmdb/midl.c
	../protobuf-cpp/data.pb.cc
	../protobuf-cpp/math.pb.cc
)

add_definitions(-D_SCL_SECURE_NO_WARNINGS)
add_definitions(-D_CRT_SECURE_NO_WARNINGS)
add_definitions(-DPROTOBUF_USE_EXCEPTIONS=0)
add_definitions(-DEA_CHAR16_NATIVE=1)

add_executable (leaderboards ${LEADERBOARDS_SOURCES})

if (NOT WIN32)
	target_link_libraries(leaderboards ${PROTOBUF_LIBRARY})
endif ()

if (WIN32)
	target_link_libraries(leaderboards debug ${PROJECT_SOURCE_DIR}/../../ext-deps/protobuf-2.5.0-vs2013/vsprojects/Debug/libprotobuf.lib)

	target_link_libraries(leaderboards optimized ${PROJECT_SOURCE_DIR}/../../ext-deps/protobuf-2.5.0-vs2013/vsprojects/Release/libprotobuf.lib)
endif (WIN32)
