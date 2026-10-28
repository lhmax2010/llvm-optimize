Name:            libconfig
Summary:         C/C++ configuration file library
Version:         1.6
Release:         0
License:         LGPL-2.1+
Group:           Base/Configuration

Source0:         %{name}-%{version}.tar.gz
Source1001:      %{name}.manifest
BuildRequires:   bison
BuildRequires:   flex
BuildRequires:   makeinfo

%description
Libconfig is a library for reading and writing configuration files.
Format of configuration files is more readable than XML and library
does all the job related to types convesions.

%package devel
Summary:         Development package for libconfig
Group:           Development/Libraries
Requires:        %{name} = %{version}
Requires:        pkgconfig

%description devel
Development libraries for libconfig.

%prep
%setup -q
cp %{SOURCE1001} .

%build
%reconfigure
make

%install
%make_install

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%manifest %{name}.manifest
%license LICENSE.LGPL-2.1+
%defattr(-,root,root)
%{_libdir}/libconfig*.so.*

%files devel
%manifest %{name}.manifest
%defattr(-,root,root)
%{_includedir}/libconfig*
%{_libdir}/libconfig*.so
%{_libdir}/cmake/libconfig++/libconfig++Config.cmake
%{_libdir}/cmake/libconfig/libconfigConfig.cmake
%{_libdir}/pkgconfig/libconfig*.pc
%{_infodir}/libconfig.info*
