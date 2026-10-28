Name:           united-service
Summary:        United Service
Version:        1.3.3
Release:        0
Group:          App Framework/Application Core
License:        Apache-2.0
Source0:        %{name}-%{version}.tar.gz
SOURCE1:        %{name}.conf
Source1001:     %{name}.manifest
BuildRequires:  cmake
BuildRequires:  hash-signer
BuildRequires:  pkgconfig(dlog)
BuildRequires:  pkgconfig(bundle)
BuildRequires:  pkgconfig(tizen-core)
BuildRequires:  pkgconfig(tizen-libopener)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(iniparser)
BuildRequires:  pkgconfig(aul)
BuildRequires:  pkgconfig(libsystemd)
BuildRequires:  pkgconfig(gmock)

Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig

%description
United service is to integrate multiple currently independent daemons into one process
to improve management efficiency, optimize resource usage, and ensure consistency between services.

%package devel
Summary:        Development files for United Service
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}

%description devel
Development files for United Service.

%package unittests
Summary:    GTest for united-service API
Group:      Development/Libraries
Requires:   %{name}

%description unittests
GTest for united-service API

%prep
%setup -q
cp %{SOURCE1001} .

%build
MAJORVER=`echo %{version} | awk 'BEGIN {FS="."}{print $1}'`
%cmake \
	-DFULLVER=%{version} \
	-DMAJORVER=${MAJORVER} \
	.

%__make %{?jobs:-j%jobs}

%check
export LD_LIBRARY_PATH="../../src"
ctest --verbose %{?_smp_mflags}

%install
rm -rf %{buildroot}

%make_install

mkdir -p %{buildroot}%{_tmpfilesdir}
install -m 0644 %SOURCE1 %{buildroot}%{_tmpfilesdir}/%{name}.conf

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%manifest %{name}.manifest
%{_tmpfilesdir}/%{name}.conf
%license LICENSE.APLv2
%{_libdir}/libunited-service.so.*

%files devel
%manifest %{name}.manifest
%{_includedir}/tizen-base/*.h
%{_libdir}/libunited-service.so
%{_libdir}/pkgconfig/united-service.pc

%files unittests
%{_bindir}/united-service_unittests
