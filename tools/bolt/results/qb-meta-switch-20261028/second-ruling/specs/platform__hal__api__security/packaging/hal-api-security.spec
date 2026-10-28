### main package #########
Name:       hal-api-security
Summary:    hal-api-security interface
Version:    1.1.0
Release:    0
Group:      Development/Libraries
License:    Apache-2.0
Source0:    %{name}-%{version}.tar.gz
Source1:    %{name}.manifest
Source2:    %{name}-manifest.xml

Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig
BuildRequires: cmake
BuildRequires: pkgconfig(hal-api-common)

%description
%{name} interface

### devel package #########
%package -n     %{name}-devel
Summary:        %{name} interface
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}

%description -n %{name}-devel
%{name} Interface for product vendor developer

### haltest package #########
%package -n     %{name}-haltests
Summary:        %{name} tests
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
BuildRequires: pkgconfig(capi-system-info)
BuildRequires: pkgconfig(libtzplatform-config)
BuildRequires: pkgconfig(gmock)

%description -n %{name}-haltests
%{name} tests

### build and install #########
%prep
%setup -q

%cmake . -DCMAKE_C_COMPILER=%__cc \
        -DCMAKE_CXX_COMPILER=%__cxx \
        -DCMAKE_INSTALL_PREFIX=%{_prefix} \
        -DCMAKE_LIBDIR_PREFIX=%{_libdir}/ \
        -DHALTEST=on

%build
cp %{SOURCE1} .
make %{?jobs:-j%jobs}

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_sysconfdir}/hal
cp %{SOURCE2} %{buildroot}%{_sysconfdir}/hal/
%make_install

%clean
rm -rf %{buildroot}

%post
/sbin/ldconfig
/usr/bin/hal-compatibility-checker --reset

%postun
/sbin/ldconfig
/usr/bin/hal-compatibility-checker --reset

### contain files to package #########
%files -n %{name}
%manifest %{name}.manifest
%license LICENSE.Apache-2.0
%defattr(-,root,root,-)
%{_libdir}/hal/lib%{name}.so*
%{_sysconfdir}/hal/%{name}-manifest.xml

%files -n %{name}-devel
%defattr(-,root,root,-)
%manifest %{name}.manifest
%license LICENSE.Apache-2.0
%{_includedir}/hal/hal-security-auth*.h
%{_includedir}/hal/hal-security-certs*.h
%{_includedir}/hal/hal-security-keys*.h
%{_libdir}/pkgconfig/hal-api-security.pc
%{_libdir}/hal/lib%{name}.so

%files -n %{name}-haltests
%defattr(-,root,root,-)
%manifest %{name}.manifest
%license LICENSE.Apache-2.0
%{_bindir}/hal/security-haltests
