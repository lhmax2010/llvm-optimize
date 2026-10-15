%define cross armv7l
%define armv7l 1

#
# spec file for package qemu-accel-ARCH, where ARCH = armv7l, armv7hl or aarch64
#
# Copyright (c) 2012 SUSE LINUX Products GmbH, Nuernberg, Germany.
# Copyright (c) 2015 Tizen
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via http://bugs.tizen.org/
#


# arm
%define target_cpu %{cross}
%define target_abi %{?armv7l:eabi}%{?armv7hl:eabihf}
%define target_arch %{target_cpu}-tizen-linux-gnu%{?target_abi}
%define libdir %{_prefix}/lib%{?aarch64:64}%{?riscv64:64}

#disable strip debug info due to patchelf + armv7hl bug
%{?armv7hl:
%define _rpm_strip_disable 1
}

# default path in qemu
%define emul_path /emul

Name:           qemu-accel
Version:        0.4
Release:        0
AutoReqProv:    off
BuildRequires:  gcc-%{cross}
BuildRequires:  binutils-%{cross}
BuildRequires:  gcc-fortran
#BuildRequires:  expect
BuildRequires:  fdupes
BuildRequires:  gettext-runtime
BuildRequires:  gettext-tools
BuildRequires:  m4
# required for xxd
BuildRequires:  vim
BuildRequires:  patchelf
BuildRequires:  elfutils
BuildRequires:  libxslt-tools
BuildRequires:  cmake
BuildRequires:  gawk
BuildRequires:  libstdc++
BuildRequires:  python libpython
BuildRequires:  python-xml
BuildRequires:  python-magic
BuildRequires:  python-rpm
BuildRequires:  python3-rpm
BuildRequires:  python-ply
BuildRequires:  file
BuildRequires:  libasan
%ifarch x86_64
BuildRequires:  liblsan
%endif
BuildRequires:  icecream
BuildRequires:  libunwind
BuildRequires:  libuuid
BuildRequires:  clang
BuildRequires:  pbzip2
BuildRequires:  python3
BuildRequires:  python3-base
BuildRequires:  glibc-accel-ldso
BuildRequires:  diffutils
BuildRequires:  libabigail
BuildRequires:  dash

# required for LLVM gold plugin
BuildRequires:  llvm-devel
# do not comapre with old rpms
#!BuildIgnore:  build-compare

Summary:        Native binaries for speeding up cross compile
License:        GPL-2.0
Group:          Development/Cross Compilation
ExclusiveArch:  x86_64

%description
This package is used in %{cross} architecture builds using qemu to speed up builds
with native binaries.
This should not be installed on systems, it is just intended for qemu environments.

%package -n python-accel
AutoReqProv: off
Requires: qemu-accel
Version: %{version}
Release: %{release}
Summary: Binaries for python acceleration
License:        GPL-2.0
Group:          Development/Cross Compilation

%description -n python-accel
This package is used in qemu-accel to accelerate python.

%post -n python-accel
ldconfig

%package -n clang-accel
AutoReqProv: off
Requires: qemu-accel
Version: %{version}
Release: %{release}
Summary: Binaries for clang acceleration
License:        GPL-2.0
Group:          Development/Cross Compilation
Requires: qemu-accel

%description -n clang-accel
This package is used in qemu-accel to accelerate clang compiler.

%post -n clang-accel

%prep

%build
%if 0%{?asan} || 0%{?ubsan} || 0%{?hwasan}
%gcc_unforce_options
%endif

%install
set +x
# gcc version major.minor.patch
gcc_version=`gcc --version | sed -ne '1s/[^0-9]*\(\([0-9]\.\?\)*\).*/\1/p'`
# Find cross-gcc install directory, like:
# - /usr/lib/gcc/armv7l-tizen-linux-gnueabi/6.2.1/ for armv7l,
# - /usr/lib64/gcc/aarch64-tizen-linux-gnu/6.2.1/ for aarch64
gcc_install_dir="$(%{target_arch}-gcc -print-file-name=)"

# just like it is determided in python.spec
host_python="python$(python2 --version 2>&1 | sed -ne '1s/.* //p' | head -c 3)"
host_python3="python$(python3 --version | sed -ne '1s/.* //p' | sed -e 's/^\(3\.[0-9]\+\).*/\1/')"

# Emul path inside buildroot for installation
buildroot_emul_path=%{buildroot}%{emul_path}

# Collect all shared objects from glibc and libgcc
# excluding RTLD since it's processed in another way later
for lib in $(rpm -ql glibc) \
 $(rpm -ql libgcc)
do
 if echo "$lib" | grep -E '\.so(\.[[:digit:]]+)?$' > /dev/null && ! echo "$lib" | grep -q '/ld-'; then
   binaries="$binaries $lib"
 fi
done

%ifarch %ix86
  LD="%{_libdir}/ld-linux.so.2"
%endif
%ifarch x86_64
  LD="%{_libdir}/ld-linux-x86-64.so.2"
%endif

# Disable bash acceleration for armv7hl due to corruption
%{?!armv7hl:
  BASH_EXECUTABLE=%{_bindir}/bash
  DASH_EXECUTABLE=%{_bindir}/dash
}

for executable in %{emul_path}$LD \
   $BASH_EXECUTABLE \
   $DASH_EXECUTABLE \
   %{_bindir}/rpm \
   %{_bindir}/rpm2cpio \
   %{_bindir}/rpmdb \
   %{_bindir}/rpmkeys \
   %{_bindir}/rpmqpack \
   %{_bindir}/rpmbuild \
   %{_bindir}/rpmsign \
   %{_bindir}/rpmspec \
   %{_bindir}/rpm2archive \
   %{_libdir}/rpm-plugins/ima.so \
   %{_libdir}/rpm-plugins/prioreset.so \
   %{_libdir}/rpm-plugins/syslog.so \
   %{_libdir}/libdb-4.8.so \
   %{_libdir}/libdb_cxx-4.8.so \
   %{_bindir}/tar \
   %{_bindir}/gzip \
   %{_bindir}/bzip2 \
   %{_bindir}/xz \
   %{_bindir}/xzdec \
   %{_bindir}/pbzip2 \
   %{_bindir}/grep \
   %{_bindir}/sed \
   %{_libdir}/libnssdbm3.so \
   %{_libdir}/libsoftokn3.so \
   %{_libdir}/libfreebl3.so \
   %{_libdir}/lib*san.so* \
   %{_libdir}/libssl.so* \
   %{_libdir}/libcrypto.so* \
   %{_bindir}/cat \
   %{_bindir}/expr \
   %{_bindir}/mkdir \
   %{_bindir}/mv \
   %{_bindir}/rm \
   %{_bindir}/rmdir \
   %{_bindir}/msgexec \
   %{_bindir}/msgfmt \
   %{_bindir}/msgcat \
   %{_bindir}/msgmerge \
   %{_bindir}/make \
   %{_bindir}/m4 \
   %{_bindir}/awk \
   %{_bindir}/gawk \
   %{_bindir}/patch \
   %{_bindir}/diff \
   %{_bindir}/echo \
   %{_bindir}/head \
   %{_bindir}/eu-addr2line \
   %{_bindir}/eu-ar \
   %{_bindir}/eu-elfclassify \
   %{_bindir}/eu-elfcmp \
   %{_bindir}/eu-elfcompress \
   %{_bindir}/eu-elflint \
   %{_bindir}/eu-findtextrel \
   %{_bindir}/eu-nm \
   %{_bindir}/eu-objdump \
   %{_bindir}/eu-ranlib \
   %{_bindir}/eu-readelf \
   %{_bindir}/eu-size \
   %{_bindir}/eu-stack \
   %{_bindir}/eu-strings \
   %{_bindir}/eu-strip \
   %{_bindir}/eu-unstrip \
   %{_bindir}/xsltproc \
   %{_bindir}/ccmake \
   %{_bindir}/cmake \
   %{_bindir}/cpack \
   %{_bindir}/ctest \
   %{_bindir}/%{target_arch}-addr2line \
   %{_bindir}/%{target_arch}-ar \
   %{_bindir}/%{target_arch}-as \
   %{_bindir}/%{target_arch}-c++filt \
   %{_bindir}/%{target_arch}-elfedit \
   %{_bindir}/%{target_arch}-gprof \
   %{_bindir}/%{target_arch}-ld \
   %{_bindir}/%{target_arch}-ld.bfd \
   %{_bindir}/%{target_arch}-nm \
   %{_bindir}/%{target_arch}-objcopy \
   %{_bindir}/%{target_arch}-objdump \
   %{_bindir}/%{target_arch}-ranlib \
   %{_bindir}/%{target_arch}-readelf \
   %{_bindir}/%{target_arch}-size \
   %{_bindir}/%{target_arch}-strings \
   %{_bindir}/%{target_arch}-strip \
   %{_bindir}/%{target_arch}-c++ \
   %{_bindir}/%{target_arch}-g++ \
   %{_bindir}/%{target_arch}-cpp \
   %{_bindir}/%{target_arch}-gcc \
   %{_bindir}/%{target_arch}-gcc-ar \
   %{_bindir}/%{target_arch}-gcc-nm \
   %{_bindir}/%{target_arch}-gcc-ranlib \
   %{_bindir}/%{target_arch}-gcov \
   %{_bindir}/%{target_arch}-gfortran \
   ${gcc_install_dir}cc1 \
   ${gcc_install_dir}cc1plus \
   ${gcc_install_dir}collect2 \
   ${gcc_install_dir}lto1 \
   ${gcc_install_dir}lto-wrapper \
   ${gcc_install_dir}liblto_plugin.so* \
   ${gcc_install_dir}f951 \
   %{_bindir}/file \
   %{_bindir}/icecc \
   %{_bindir}/icerun \
   %{_bindir}/find \
   %{_bindir}/xargs \
   %{_bindir}/readlink \
   %{_bindir}/ls \
   %{_bindir}/cpio \
   %{_rpmconfigdir}/debugedit \
   %{_rpmconfigdir}/*deps \
   %{_libdir}/libunwind*.so* \
   %{_libdir}/libuuid*.so* \
   %{_bindir}/localedef \
   %{_bindir}/abidw \
   %{_bindir}/abidiff \
   %{_bindir}/abicompat \
   %{_bindir}/abipkgdiff \
   %{_bindir}/kmidiff
do
  binaries="$binaries $executable"
done

# Add architecture-specific binaries (dwp and ld.gold are not available for riscv64)
%{?!riscv64:
for executable in %{_bindir}/%{target_arch}-dwp \
   %{_bindir}/%{target_arch}-ld.gold
do
  binaries="$binaries $executable"
done
}

prepare_package_list() {
  local bins=""
  local name=$1
  shift
  local executables="$@"
  echo "Setting up $name for $executables"
  ## Prepare the clang binaries separately
  for executable in $executables; do
    bins="$bins $executable `ldd $executable 2>/dev/null | sed -n 's,.*=> \(/[^ ]*\) .*,\1,p'`"
  done

  for b in $(echo "$bins" | tr ' ' '\n' | sort -u); do
    local orig_file=$(readlink -f $b)
    bins="$bins $orig_file"
    if ! echo "$b" | grep -q '/\.\./'; then
        # Ignore relative paths
        echo $b >> $name.list
    fi
    echo $orig_file >> $name.list
  done

  ## Store the resulting list for packaging, setting up the right prefix, removing duplication of %emul_path if one exists
  cat $name.list | \
      sed -e 's|^|%{emul_path}|;s| |\n%{emul_path}|g' | \
      grep -v "%{emul_path}%{emul_path}" | \
      sort -u > %{_sourcedir}/$name-accel.list
  binaries=$(echo "$binaries $bins" | tr ' ' '\n' | sort -u)
}

prepare_package_list all \
  $binaries

prepare_package_list clang \
  %{_bindir}/clang-* \
  %{_bindir}/clang++ \
  %{_bindir}/opt \
  %{_bindir}/lli \
  %{_bindir}/llc \
  %{_bindir}/llvm-* \
  %{_bindir}/lld \
  %{_bindir}/ld.lld \
  %{_libdir}/libLTO.so* \
  %{_libdir}/LLVMgold.so*

prepare_package_list python \
  %{_bindir}/${host_python} \
  %{_libdir}/${host_python}/lib-dynload/*.so \
  %{_libdir}/${host_python}/site-packages/*/*.so

prepare_package_list python3 \
  %{_bindir}/${host_python3} \
  %{_libdir}/${host_python3}/lib-dynload/*.so \
  %{_libdir}/${host_python3}/site-packages/*/*.so

## dump list of binaries and list of packages
echo "### Binaries accelerated ###"
echo $binaries | sed -e 's/[^ ]*\///g;s/[^ ]*.so[^ ]* \?//g'
echo "### Packages used ###"
rpm -qf $binaries | grep -v "not owned" | sed -e "s/-[0-9].*//g" | sort -u
echo ""

patch_binary() {
  local binary=$1
  local rtld=$2
  # We don't need to accelerate shell scripts
  local filetype=`file --brief $binary`
  if echo "$filetype" | grep -q '^POSIX shell script'; then
    return
  fi

  local outfile=${buildroot_emul_path}$binary
  if ! test -e "$binary"; then
    echo "WARNING: File not found, ignoring"
    return
  fi
  if test -f "$outfile"; then
    echo "WARNING: File exists, ignoring"
    return
  fi
  mkdir -p ${outfile%/*}
  cp -aL $binary $outfile
  [ "$binary" = "$rtld" ] && return
  [ "$binary" = "%{emul_path}$rtld" ] && return

  # not all binaries have an .interp section
  if patchelf --print-interpreter $outfile 1>/dev/null 2>/dev/null; then
    patchelf --set-interpreter %{emul_path}$rtld $outfile
  fi

  # Only patch RUNPATH if one exists and is absolute
  local rpath=$(readelf -d "$outfile" | sed -e '/RUNPATH/{s~.*\[\(.*\)\]~\1~;n};d')
  if [ -n "$rpath" ]; then
    first_char=$(echo "$rpath" | cut -c1)
    if [ "$first_char" = "/" ]; then
      patchelf --set-rpath "%{emul_path}%{_libdir}" $outfile
    fi
  fi
}

# Process all binaries directly (parallel jobs with simple file-based coordination)
for binary in $binaries; do
    patch_binary "$binary" "$LD" &
done
wait

set -x

%{?multilib:
# Detect name of current ld.so. E.g. ld-linux.so.2
cross_ld_symlink=$(basename `rpm -ql glibc-32bit | grep -E 'ld-linux\.so$'`)

# Patch all 32bit binaries to use the right ld.so though symlink
mkdir -p ${buildroot_emul_path}%{_prefix}/lib
mkdir -p ${buildroot_emul_path}/lib
for f in $(rpm -ql glibc-32bit) \
  $(rpm -ql libgcc-32bit)
do
 fdir=$(dirname $f)
 [ ! -d ${buildroot_emul_path}/$fdir ] && mkdir -p ${buildroot_emul_path}/$fdir
 cp -a $f ${buildroot_emul_path}/$f
 echo "%{emul_path}$f" >> %{_sourcedir}/multilib-accel.list
done

# Now we have to change the ld.so name to prevent name clashing in armv7l repos
i686_libdir="%{emul_path}/lib"

# 1. Rename the actual ld.so binary
cross_ld_so=$(find %{buildroot}${i686_libdir} -name 'ld-*.so.2' -printf '%f')
new_cross_ld_so=$(echo ${cross_ld_so} | sed -e 's,\.so,-i686.so,')
mv %{buildroot}${i686_libdir}/${cross_ld_so} %{buildroot}${i686_libdir}/${new_cross_ld_so}
sed -e "s|${cross_ld_so}|${new_cross_ld_so}|" -i %{_sourcedir}/multilib-accel.list

# 2. Force the symlink to point the right file.
ln -sf %{emul_path}/lib/${new_cross_ld_so} %{buildroot}${i686_libdir}/${cross_ld_symlink}
echo "${i686_libdir}/${cross_ld_symlink}" >> %{_sourcedir}/multilib-accel.list

# create symlinks for libgcc-32bit
# libgcc-32bit library is placed under ${gcc_install_dir}32/ not just /lib for 32bit
# Process lib*.so files only, we expect that licenses are already in the
# multilib-accel.list.
for f in $(rpm -ql libgcc-32bit | grep "\/lib[^\/]*\.so.*")
do
  filename=$(basename $f)
  ln -sf %{emul_path}/$f %{buildroot}${i686_libdir}/${filename}
  echo "${i686_libdir}/${filename}" >> %{_sourcedir}/multilib-accel.list
done
}

# create symlinks for bash
ln -s usr/bin "${buildroot_emul_path}/bin"
ln -sf bash "${buildroot_emul_path}%{_bindir}/sh"
echo '%{emul_path}%{_bindir}/sh' >> %{_sourcedir}/all-accel.list

mv ${buildroot_emul_path}/%{_lib}/* ${buildroot_emul_path}%{_libdir}/
rm -rf ${buildroot_emul_path}/%{_lib}
ln -sf usr/%{_lib} ${buildroot_emul_path}/%{_lib}
%{?multilib:
mv ${buildroot_emul_path}/lib/* ${buildroot_emul_path}%{_prefix}/lib/
rm -rf ${buildroot_emul_path}/lib
ln -sf usr/lib ${buildroot_emul_path}/lib
sed -e 's|%{emul_path}/lib|%{emul_path}/usr/lib|' -i %{_sourcedir}/multilib-accel.list
}

# rename binutils binaries
for binary in addr2line ar as c++filt%{!?riscv64: dwp} elfedit gprof ld ld.bfd%{!?riscv64: ld.gold} nm objcopy objdump ranlib readelf size strings strip
do
  mv ${buildroot_emul_path}%{_bindir}/%{target_arch}-$binary ${buildroot_emul_path}%{_bindir}/$binary
  sed -e "\|%{emul_path}%{_bindir}/%{target_arch}-$binary|d" -i %{_sourcedir}/all-accel.list
  echo "%{emul_path}%{_bindir}/$binary" >> %{_sourcedir}/all-accel.list
done

mkdir -p ${buildroot_emul_path}/%{_prefix}/%{target_arch}/bin
for binary in ar as ld ld.bfd%{!?riscv64: ld.gold} nm objcopy objdump ranlib strip; do
  ln -sf %{emul_path}%{_bindir}/$binary ${buildroot_emul_path}%{_prefix}/%{target_arch}/bin/$binary
  echo "%{emul_path}%{_bindir}/$binary" >> %{_sourcedir}/all-accel.list
  echo "%{emul_path}%{_prefix}/%{target_arch}/bin/$binary" >> %{_sourcedir}/all-accel.list
done

# create symlinks for python
mv ${buildroot_emul_path}%{_bindir}/${host_python} ${buildroot_emul_path}%{_bindir}/${host_python}-orig
cat > ${buildroot_emul_path}%{_bindir}/${host_python} << EOF
#!/bin/bash
if [ -z "\$PYTHONPATH" ]; then
  export PYTHONPATH="%{libdir}/${host_python}"
else
  export PYTHONPATH+=":%{libdir}/${host_python}"
fi
export PYTHONHOME="%{emul_path}%{_prefix}"
%{emul_path}%{_bindir}/${host_python}-orig "\$@"
EOF
chmod +x ${buildroot_emul_path}%{_bindir}/${host_python}

ln -s ${host_python} ${buildroot_emul_path}%{_bindir}/python
ln -s ${host_python} ${buildroot_emul_path}%{_libdir}/python

# create symlinks for python3
mv ${buildroot_emul_path}%{_bindir}/${host_python3} ${buildroot_emul_path}%{_bindir}/${host_python3}-orig
cat > ${buildroot_emul_path}%{_bindir}/${host_python3} << EOF
#!/bin/bash
if [ -z "\$PYTHONPATH" ]; then
  export PYTHONPATH="%{libdir}/${host_python3}"
else
  export PYTHONPATH+=":%{libdir}/${host_python3}"
fi
export PYTHONHOME="%{emul_path}%{_prefix}"
export LD_LIBRARY_PATH="%{emul_path}%{_libdir}:$LD_LIBRARY_PATH"
%{emul_path}%{_bindir}/${host_python3}-orig "\$@"
EOF
chmod +x ${buildroot_emul_path}%{_bindir}/${host_python3}

ln -s ${host_python3} ${buildroot_emul_path}%{_bindir}/python3
ln -s ${host_python3} ${buildroot_emul_path}%{_libdir}/python3

#create symlinks for Scons & ply
#scons>=4.4.0 version now is python3 code
mkdir -p ${buildroot_emul_path}%{libdir}/${host_python3}/site-packages
ln -sf %{libdir}/${host_python3}/site-packages/SCons ${buildroot_emul_path}%{libdir}/${host_python3}/site-packages/SCons
py3_version=$(python3 --version | sed -ne '1s/.* //p' | sed -e 's/^\(3\.[0-9]\+\).*/\1/')
ln -sf %{libdir}/${host_python3}/site-packages/SCons-4.4.0-py${py3_version}.egg-info  ${buildroot_emul_path}%{libdir}/${host_python3}/site-packages/SCons-4.4.0-py${py3_version}.egg-info
echo "%{libdir}/${host_python3}/site-packages/SCons" >> python.list
echo "%{libdir}/${host_python3}/site-packages/SCons-4.4.0-py${py3_version}.egg-info" >> python.list

mkdir -p ${buildroot_emul_path}%{libdir}/${host_python}/site-packages
ln -sf %{libdir}/${host_python}/site-packages/ply ${buildroot_emul_path}%{libdir}/${host_python}/site-packages/ply
echo "%{libdir}/${host_python}/site-packages/ply" >> python.list

mkdir -p ${buildroot_emul_path}%{_libdir}/${host_python}/site-packages/rpm/
mkdir -p ${buildroot_emul_path}%{_libdir}/${host_python3}/site-packages/rpm/
mkdir -p ${buildroot_emul_path}%{_libdir}/${host_python}/encodings/
cp %{_libdir}/${host_python}/site-packages/rpm/*.py ${buildroot_emul_path}%{_libdir}/${host_python}/site-packages/rpm/
cp %{_libdir}/${host_python3}/site-packages/rpm/*.py ${buildroot_emul_path}%{_libdir}/${host_python3}/site-packages/rpm/
cp %{_libdir}/${host_python}/*.py ${buildroot_emul_path}%{_libdir}/${host_python}/
cp %{_libdir}/${host_python}/encodings/*.py ${buildroot_emul_path}%{_libdir}/${host_python}/encodings/
cp -r %{_libdir}/${host_python3} ${buildroot_emul_path}%{_libdir}/
find ${buildroot_emul_path}%{_libdir}/${host_python3} -name *.pyc -exec rm {} \;
# Skip directories to not glob all inside them during #files processing
find %{buildroot} ! -type d -name 'python*' | sed -e "s|${buildroot_emul_path}||" | tee -a python.list

# rename gcc binaries
for bin in c++ g++ gcc gfortran cpp gcc-ar gcc-nm gcc-ranlib gcov
do
  mv ${buildroot_emul_path}%{_bindir}/%{target_arch}-$bin ${buildroot_emul_path}%{_bindir}/$bin
  ln -s $bin ${buildroot_emul_path}%{_bindir}/%{target_arch}-$bin
  echo "%{emul_path}%{_bindir}/$bin" >> %{_sourcedir}/all-accel.list
done
ln -s gcc ${buildroot_emul_path}/%{_bindir}/cc
echo '%{emul_path}%{_bindir}/cc' >> %{_sourcedir}/all-accel.list

# rpmbuild when generating 'requires' tag for gobject-introspection binaries
# selects (64-bit) suffix for libs based on ${HOSTTYPE} bash variable
# so we replace x86_64 to armv7l to avoid bogus dependencies
%ifarch x86_64
%{?armv7l:
sed -i -e "s/x86_64/armv7l/g" ${buildroot_emul_path}%{_bindir}/bash
}
%endif

# Default Tizen gcc build dir, must be synchronized with linaro-gcc spec
# definition. Expected to be 'home/abuild/rpmbuild/BUILD/gcc-${version}/obj/'
gcc_build_dir=%{_builddir}/gcc-${gcc_version}/obj

# create symlinks for gcc build (CC_FOR_TARGET)
mkdir -p ${buildroot_emul_path}${gcc_build_dir}/gcc
for binary in as cpp gcc-ar gcc-nm gcc-ranlib gcov nm
do
  ln -sf %{emul_path}%{_bindir}/${binary} ${buildroot_emul_path}${gcc_build_dir}/gcc/${binary}
  echo "%{emul_path}${gcc_build_dir}/gcc/${binary}" >> %{_sourcedir}/all-accel.list
done
for binary in cc1 cc1plus collect2 lto1 lto-wrapper f951
do
  ln -sf %{emul_path}${gcc_install_dir}${binary} ${buildroot_emul_path}${gcc_build_dir}/gcc/${binary}
  echo "%{emul_path}${gcc_build_dir}/gcc/${binary}" >> %{_sourcedir}/all-accel.list
done
ln -sf %{emul_path}%{_bindir}/gcc ${buildroot_emul_path}${gcc_build_dir}/gcc/xgcc
ln -sf %{emul_path}%{_bindir}/g++ ${buildroot_emul_path}${gcc_build_dir}/gcc/xg++
echo "%{emul_path}${gcc_build_dir}/gcc/xgcc" >> %{_sourcedir}/all-accel.list
echo "%{emul_path}${gcc_build_dir}/gcc/xg++" >> %{_sourcedir}/all-accel.list

# support /lib/cpp
ln -sf %{emul_path}%{_bindir}/cpp ${buildroot_emul_path}/usr/lib/cpp
echo '%{emul_path}/usr/lib/cpp' >> %{_sourcedir}/all-accel.list

# generate baselibs.conf for current architecture to prevent rpm overwriting in download repo
echo  %{cross}
cat > %{_sourcedir}/baselibs_prologue << EOF
arch i686 targets %{cross}:%{cross}
arch i686 targets %{cross}:x86-%{cross}
arch x86_64 targets %{cross}:%{cross}
arch x86_64 targets %{cross}:x86_64-%{cross}
EOF
cat %{_sourcedir}/baselibs_prologue %{_sourcedir}/baselibs_body > %{_sourcedir}/baselibs.conf

# By default this is ${gcc_install_dir}/liblto_plugin.so
target_liblto_plugin="$(%{target_arch}-gcc -print-file-name=liblto_plugin.so)"
# update baselibs.conf, overwrite LTO plugin
sed -e "s,#PLUGIN_POSTIN#,if [ -d $(dirname ${target_liblto_plugin}) ]; then\"\n  post \" mv ${target_liblto_plugin} ${target_liblto_plugin}_backup \&\& ln -sf %{emul_path}${target_liblto_plugin} ${target_liblto_plugin}\"\n  post \"fi," -i %{_sourcedir}/baselibs.conf
sed -e "s,#PLUGIN_POSTUN#,mv ${target_liblto_plugin}_backup ${target_liblto_plugin}," -i %{_sourcedir}/baselibs.conf

# Use /usr/lib for cross clang libdir on armv7l architecture
%{?armv7l:
awk '/post "/ && !x {print "  post \"echo export\\ CLANG_NO_LIBDIR_SUFFIX=1 >> /etc/profile\""; print $0; x=1;next} 1' %{_sourcedir}/baselibs.conf > baselibs_updated && mv baselibs_updated %{_sourcedir}/baselibs.conf
}

%{?multilib:
awk '/post "/ && !x {print "  post \"echo '%{emul_path}/lib' >> /etc/ld.so.conf\"\n"; print $0; x=1;next} 1' %{_sourcedir}/baselibs.conf > baselibs_updated && mv baselibs_updated %{_sourcedir}/baselibs.conf
}

# Remove the ld-$VERSION.so to prevent name clashing with native ld.so
find ${buildroot_emul_path}%{_libdir} -name 'ld-*.so' -delete
sed -e '\|%{emul_path}%{_libdir}/ld-[[:digit:]].*\.so|d' -i %{_sourcedir}/all-accel.list

# allow build of baselibs.conf
sed -e "/targettype %{cross} block!/d" -i %{_sourcedir}/baselibs.conf

# Various clang{,++}-* files in the original clang package are
# symlinks to clang-<major version>. prepare_package_list() above
# causes those files to be separate copies in ${builldroot_emul_path}.
# This recreates the original symlink structure in /emul
clang_major=`%{_bindir}/clang --version | sed -ne 's/^.*[cC]lang version\s\+\([[:digit:]]\+\).*$/\1/p'`
clang="clang-$clang_major"
emul_bin="${buildroot_emul_path}%{_bindir}"
for file in $emul_bin/clang-* $emul_bin/clang++; do
    if [ "$file" = "$emul_bin/$clang" ]; then
        continue
    fi
    if cmp "$file" "$emul_bin/$clang"; then
        rm "$file"
        ln -s $clang "$file"
    fi
done

# Plain clang binary is not copied by "prepare_package_list clang"
# call. We've just added it as symlink and now need to add it to the
# future rpm file list
ln -s $clang "$emul_bin/clang"
echo "%{_bindir}/clang" >> clang.list

# Create target-triple symlinks and add them to file list
for bin in clang clang++; do
    ln -s $bin "$emul_bin/%{target_arch}-$bin"
    echo "%{_bindir}/%{target_arch}-$bin" >> clang.list
done

## Prepare file lists for packages
# Change libdir to handle symlinks right
find . %{_sourcedir} -name '*.list' -exec sed -e 's|%{emul_path}/%{_lib}|%{emul_path}%{_libdir}|' -i {} \;
# Join native and multilib lists
cat %{_sourcedir}/all-accel.list %{?multilib:%{_sourcedir}/multilib-accel.list} | sort -u > %{_sourcedir}/qemu-accel.list

## python-accel
# Generate list of all python files
find %{buildroot} -name '*.py' | sed -e "s|${buildroot_emul_path}||" >> python.list
# Generate list of all python3 files
find ${buildroot_emul_path}%{_libdir}/${host_python3} -type f | sed -e "s|${buildroot_emul_path}||" >> python.list
# Add python3 dependant libraries
for library in ffi gdbm ncursesw panelw python3 tinfow; do
  find ${buildroot_emul_path}%{_libdir} -name "lib${library}.*" | sed -e "s|${buildroot_emul_path}||" >> python.list
done
sed -e 's|^|%{emul_path}|;s|%{emul_path}/%{_lib}|%{emul_path}%{_libdir}|' python.list | sort -u > python-full.list
# Remove common files from python-accel
comm -13 %{_sourcedir}/qemu-accel.list python-full.list | sort -u > %{_sourcedir}/python-accel.list

## clang-accel
# Prepare clang files list
sed -e 's|^|%{emul_path}|;s|%{emul_path}/%{_lib}|%{emul_path}%{_libdir}|' clang.list | sort -u > clang-full.list
# Remove common files from clang-accel
comm -13 %{_sourcedir}/qemu-accel.list clang-full.list > %{_sourcedir}/clang-accel.list

#Fix build error with rpm 4.14.1:#Not a directory
# Add symlinks to qemu-accel packaging
echo '%{emul_path}/bin' >> %{_sourcedir}/qemu-accel.list
echo '%{emul_path}/%{_lib}' >> %{_sourcedir}/qemu-accel.list
%{?multilib:echo '%{emul_path}/lib' >> %{_sourcedir}/qemu-accel.list}

mv ${buildroot_emul_path}%{emul_path}$LD ${buildroot_emul_path}$LD
rm -rf ${buildroot_emul_path}%{emul_path}

%fdupes %{buildroot}
%filter_provides_in %{emul_path}

%post
ldconfig

%postun
ldconfig

%postun -n python-accel
ldconfig

%files -f %{_sourcedir}/qemu-accel.list
%defattr(-,root,root)
%exclude %{emul_path}%{py_libdir}/*

%files -n python-accel -f %{_sourcedir}/python-accel.list
%defattr(-,root,root)

%files -n clang-accel -f %{_sourcedir}/clang-accel.list
%defattr(-,root,root)

%changelog
