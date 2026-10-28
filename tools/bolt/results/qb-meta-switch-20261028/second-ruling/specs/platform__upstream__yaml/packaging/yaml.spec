Name:           yaml
Version:        0.2.5
Release:        1
License:        MIT
Group:          Development/Libraries/C and C++
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
Url:            http://pyyaml.org/wiki/LibYAML
Source:         http://pyyaml.org/download/libyaml/yaml-%{version}.tar.gz
Source1001: 	yaml.manifest
Summary:        A YAML 1.1 parser and emitter written in C
%description
A YAML 1.1 parser and emitter written in C

%package -n libyaml
Group:          Development/Libraries/C and C++
Summary:        A YAML 1.1 parser and emitter written in C

%description -n libyaml
A YAML 1.1 parser and emitter written in C

%package -n libyaml-devel
License:        MIT
Group:          Development/Libraries/C and C++
Requires:       libyaml = %{version}
Summary:        Development files for libyaml

%description -n libyaml-devel
A YAML 1.1 parser and emitter written in C

This package holds the development files for libyaml.

%prep
%setup -n %{name}-%{version}
cp %{SOURCE1001} .

%build
./bootstrap
%configure --with-pic --disable-static
make %{?_smp_flags}

%check
make check

%install
%make_install

%post   -n libyaml -p /sbin/ldconfig

%postun -n libyaml -p /sbin/ldconfig

%files  -n libyaml
%manifest %{name}.manifest
%defattr(-,root,root,-)
%{_libdir}/libyaml-0.so.*

%files -n libyaml-devel
%manifest %{name}.manifest
%defattr(-,root,root,-)
%{_includedir}/yaml.h
%{_libdir}/libyaml.so
%{_libdir}/pkgconfig/yaml-0.1.pc

%changelog
