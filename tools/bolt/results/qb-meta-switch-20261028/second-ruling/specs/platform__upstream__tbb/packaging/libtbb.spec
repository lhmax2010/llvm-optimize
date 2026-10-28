Name:       libtbb
Summary:    Intel® Threading Building Blocks
Version:    2019U3
Release:    0
Group:      Development/Libraries
Packager:   Wook Song <wook16.song@samsung.com>
License:    Apache-2.0
Source0:    %{name}-%{version}.tar.gz
Source1:    %{name}.manifest
Source1001:    %{name}.pc.in

%description
Threading Building Blocks (TBB) lets you easily write parallel C++ programs
that take full advantage of multicore performance, that are portable,
composable and have future-proof scalability.

%package devel
License: Apache-2.0
Summary: Development package to use Intel® Threading Building Blocks
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description devel
This package provides headers and other miscellaneous files required to use Intel® TBB.

%prep
%setup -q
cp %{SOURCE1} .
cp %{SOURCE1001} .

%build
CXXFLAGS=`echo $CXXFLAGS -Wno-class-memaccess -Wno-deprecated-declarations -Wno-nonnull-compare -Wno-strict-aliasing -Wno-sign-compare -Wno-error=strict-aliasing -Wno-error=shadow -Wno-error=missing-field-initializers -Wno-error=missing-attributes -Wno-error=unused-variable`

# Add the following warnings only if the compiler supports them
extraWarnings="changes-meaning template-id-cdtor"
for warning in $extraWarnings
do
  gcc --help=warnings | grep $warning &> /dev/null && CXXFLAGS+=" -Wno-$warning "
done

%{__make} tbb_build_prefix=tizen_%{_arch}
sed -i 's|@PREFIX@|%{_prefix}|g' %{name}.pc.in
sed -i 's|@LIB_INSTALL_DIR@|%{_libdir}|g' %{name}.pc.in
sed -i 's|@INCLUDE_INSTALL_DIR@|%{_includedir}|g' %{name}.pc.in

%install
pushd build/tizen_%{_arch}_release
mkdir -p %{buildroot}%{_libdir}
install -m 644 *.so* %{buildroot}%{_libdir}
popd
mkdir -p %{buildroot}%{_includedir}
cp -rf include/tbb %{buildroot}%{_includedir}/
mkdir -p %{buildroot}%{_libdir}/pkgconfig
install -m 644 %{name}.pc.in %{buildroot}%{_libdir}/pkgconfig/%{name}.pc

%post
%{_sbindir}/ldconfig

%postun
%{_sbindir}/ldconfig

%files
%manifest %{name}.manifest
%license LICENSE
%{_libdir}/lib*.so.*


%files devel
%manifest %{name}.manifest
%license LICENSE
%{_libdir}/lib*.so
%{_libdir}/pkgconfig/*.pc
%{_includedir}/*
