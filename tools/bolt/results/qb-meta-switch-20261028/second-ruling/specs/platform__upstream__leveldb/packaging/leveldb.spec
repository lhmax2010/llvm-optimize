Name:   	leveldb
Summary:    A fast key-value storage library
Version: 	1.23
Release:    1
Group:      System/Libraries
License:    BSD-3-Clause
Source0:    %{name}-%{version}.tar.gz
Source1:    leveldb.pc 
Source1001: 	leveldb.manifest
Source1002:     disable_gtest_benchmarks.patch

BuildRequires: cmake

%description
LevelDB is a fast key-value storage library written at Google
that provides an ordered mapping from string keys to string values.


%package -n libleveldb
Summary:   A fast key-value storage library
Group:     System/Libraries

%description -n libleveldb
LevelDB is a fast key-value storage library written at Google
that provides an ordered mapping from string keys to string values.


%package devel
Summary:   A fast key-value storage library - Development
Group:     Development/Libraries
Requires:   libleveldb

%description devel
LevelDB is a fast key-value storage library written at Google
that provides an ordered mapping from string keys to string values.

Development Files.


%prep
%setup -q
cp %{SOURCE1001} .
%{__patch} -p1 < %{SOURCE1002}

%build
# LTO doesn't work with --as-needed
export CFLAGS=$(echo $CFLAGS | sed -e '/-flto/s/as-needed/no-as-needed/')
export CXXFLAGS=$(echo $CXXFLAGS | sed -e '/-flto/s/as-needed/no-as-needed/')

mkdir build
cd build
cmake -DCMAKE_BUILD_TYPE=Release \
      -DCMAKE_INSTALL_PREFIX=%{buildroot}%{_rootprefix} \
      -DBUILD_SHARED_LIBS=True .. 
cmake --build .
cd -

%install
cd build
%{__make} install
cd -
rm -rf %{buildroot}%{_libdir}/cmake
install -D -m 644 %{SOURCE1} %{buildroot}/%{_libdir}/pkgconfig/leveldb.pc

%post -p /sbin/ldconfig -n libleveldb

%postun -p /sbin/ldconfig -n libleveldb


%files -n libleveldb
%manifest %{name}.manifest
%license LICENSE
%defattr(-,root,root,-)
%{_libdir}/libleveldb.so.*


%files devel
%manifest %{name}.manifest
%license LICENSE

%{_libdir}/libleveldb.so
%{_includedir}/leveldb/*.h
%{_libdir}/pkgconfig/leveldb.pc
