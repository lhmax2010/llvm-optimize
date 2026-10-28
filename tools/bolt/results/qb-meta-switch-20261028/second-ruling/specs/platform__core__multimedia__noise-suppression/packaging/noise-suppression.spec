Name: noise-suppression
Summary: Acoustic noise suppression library
Version: 1.2
Release: 2
License: BSD-3-Clause
Source0: %{name}-%{version}.tar.gz

BuildRequires: cmake

%description
Acoustic noise suppression library

%package devel
Summary: Acoustic noise suppression library (Development)
Requires: %{name} = %{version}

%description devel
Acoustic noise suppression library (Development)

%package tool
Summary: Acoustic noise suppression library (Tool)
Requires: %{name} = %{version}

%description tool
Acoustic noise suppression library (Tool)

%prep
%setup -q

%build
cmake . -DVERSION=%{version} \
	-DCMAKE_INSTALL_PREFIX=%{_prefix} \
	-DLIB_INSTALL_DIR=%{_libdir}

make %{?jobs:-j%jobs}

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%manifest %{name}.manifest
%{_libdir}/lib%{name}.so.*
%license LICENSE

%files devel
%{_libdir}/lib%{name}.so
%{_libdir}/pkgconfig/%{name}.pc
%{_includedir}/*

%files tool
%manifest %{name}.manifest
%{_bindir}/noise_suppression_tool
