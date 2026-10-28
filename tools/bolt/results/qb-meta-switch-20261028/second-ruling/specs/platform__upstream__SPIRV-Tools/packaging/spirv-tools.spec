Name:       spirv-tools
Version:    2024.4.1
Release:    0
Summary:    Khronos SPIRV Tools
Group:      Graphics & UI Framework/GL
License:    Apache2.0
Source:     %{name}-%{version}.tar.gz
Source1001: %{name}.manifest

BuildRequires:  cmake
BuildRequires:  pkg-config
BuildRequires:  libtool
BuildRequires:  python3
BuildRequires:  python-xml
BuildRequires:  spirv-headers-devel

%define BUILD_TYPE Debug

%description
Khronos SPIRV Tools

%package devel
Summary:    Khronos SPIRV Tools
Group:      System/Libraries

%description devel
Khronos SPIRV Tools

%prep
%setup -q

%build
cp %{SOURCE1001} .

%{?asan:
export CXXFLAGS="$CXXFLAGS -Wno-maybe-uninitialized"
}

# build SPIRV tools
cmake -DCMAKE_BUILD_TYPE=%{BUILD_TYPE} \
      -DCMAKE_INSTALL_LIBDIR=%{_libdir} -DCMAKE_INSTALL_INCLUDEDIR=%{_includedir} \
      -DCMAKE_INSTALL_DATADIR=%{_datadir} -DCMAKE_INSTALL_BINDIR=%{_bindir} .
make -j 16

%install
rm -rf %{buildroot}
%{__make} DESTDIR=%{?buildroot:%{buildroot}} \
          INSTALL_ROOT=%{?buildroot:%{buildroot}} install

%files
%manifest %{name}.manifest
%license LICENSE
%defattr(-,root,root,-)
%{_libdir}/libSPIRV*
%{_libdir}/cmake/*
%{_bindir}/*

%files devel
%defattr(-,root,root,-)
%{_includedir}/spirv-tools/*
%{_libdir}/pkgconfig/SPIRV*.pc


