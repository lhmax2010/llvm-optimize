# Install script for directory: /home/abuild/rpmbuild/BUILD/llvm-22.1.8/clang/tools/driver

# Set the install prefix
if(NOT DEFINED CMAKE_INSTALL_PREFIX)
  set(CMAKE_INSTALL_PREFIX "/usr")
endif()
string(REGEX REPLACE "/$" "" CMAKE_INSTALL_PREFIX "${CMAKE_INSTALL_PREFIX}")

# Set the install configuration name.
if(NOT DEFINED CMAKE_INSTALL_CONFIG_NAME)
  if(BUILD_TYPE)
    string(REGEX REPLACE "^[^A-Za-z0-9_]+" ""
           CMAKE_INSTALL_CONFIG_NAME "${BUILD_TYPE}")
  else()
    set(CMAKE_INSTALL_CONFIG_NAME "Release")
  endif()
  message(STATUS "Install configuration: \"${CMAKE_INSTALL_CONFIG_NAME}\"")
endif()

# Set the component getting installed.
if(NOT CMAKE_INSTALL_COMPONENT)
  if(COMPONENT)
    message(STATUS "Install component: \"${COMPONENT}\"")
    set(CMAKE_INSTALL_COMPONENT "${COMPONENT}")
  else()
    set(CMAKE_INSTALL_COMPONENT)
  endif()
endif()

# Install shared libraries without execute permission?
if(NOT DEFINED CMAKE_INSTALL_SO_NO_EXE)
  set(CMAKE_INSTALL_SO_NO_EXE "0")
endif()

# Is this installation the result of a crosscompile?
if(NOT DEFINED CMAKE_CROSSCOMPILING)
  set(CMAKE_CROSSCOMPILING "FALSE")
endif()

# Set path to fallback-tool for dependency-resolution.
if(NOT DEFINED CMAKE_OBJDUMP)
  set(CMAKE_OBJDUMP "/bin/llvm-objdump")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "clang" OR NOT CMAKE_INSTALL_COMPONENT)
  foreach(file
      "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/bin/clang-22"
      "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/bin/clang"
      )
    if(EXISTS "${file}" AND
       NOT IS_SYMLINK "${file}")
      file(RPATH_CHECK
           FILE "${file}"
           RPATH "\$ORIGIN/../lib64")
    endif()
  endforeach()
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/bin" TYPE EXECUTABLE FILES
    "/home/abuild/bolt-work/bolt-v4-20261014-fallback/config-install-temp/bin/clang-22"
    "/home/abuild/bolt-work/bolt-v4-20261014-fallback/config-install-temp/bin/clang"
    )
  foreach(file
      "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/bin/clang-22"
      "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/bin/clang"
      )
    if(EXISTS "${file}" AND
       NOT IS_SYMLINK "${file}")
      file(RPATH_CHANGE
           FILE "${file}"
           OLD_RPATH "\$ORIGIN/../lib64:"
           NEW_RPATH "\$ORIGIN/../lib64")
      if(CMAKE_INSTALL_DO_STRIP)
        execute_process(COMMAND "/bin/llvm-strip" "${file}")
      endif()
    endif()
  endforeach()
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "clang" OR NOT CMAKE_INSTALL_COMPONENT)
  include("/home/abuild/rpmbuild/BUILD/llvm-22.1.8/llvm/cmake/modules/LLVMInstallSymlink.cmake")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "clang" OR NOT CMAKE_INSTALL_COMPONENT)
  install_symlink("clang++" "clang" "bin" "create_symlink")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "clang" OR NOT CMAKE_INSTALL_COMPONENT)
  include("/home/abuild/rpmbuild/BUILD/llvm-22.1.8/llvm/cmake/modules/LLVMInstallSymlink.cmake")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "clang" OR NOT CMAKE_INSTALL_COMPONENT)
  install_symlink("clang-cl" "clang" "bin" "create_symlink")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "clang" OR NOT CMAKE_INSTALL_COMPONENT)
  include("/home/abuild/rpmbuild/BUILD/llvm-22.1.8/llvm/cmake/modules/LLVMInstallSymlink.cmake")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "clang" OR NOT CMAKE_INSTALL_COMPONENT)
  install_symlink("clang-cpp" "clang" "bin" "create_symlink")
endif()

string(REPLACE ";" "\n" CMAKE_INSTALL_MANIFEST_CONTENT
       "${CMAKE_INSTALL_MANIFEST_FILES}")
if(CMAKE_INSTALL_LOCAL_ONLY)
  file(WRITE "/home/abuild/bolt-work/bolt-v4-20261014-fallback/config-install-temp/tools/clang/tools/driver/install_local_manifest.txt"
     "${CMAKE_INSTALL_MANIFEST_CONTENT}")
endif()
