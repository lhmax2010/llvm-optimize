Name:		libnet-client
Summary:	Network Client library (Shared library)
Version:	1.2.10
Release:	0
Group:		System/Network
License:	Flora-1.1
Source0:	%{name}-%{version}.tar.gz
BuildRequires:	pkgconfig(dlog)
BuildRequires:	pkgconfig(vconf)
BuildRequires:	pkgconfig(gio-2.0)
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	pkgconfig(gthread-2.0)

%if 0%{?gtests:1}
BuildRequires:  pkgconfig(gmock)
%endif

%description
Network Client library (Shared library)

%package devel
Summary:	Network Client library (Development)
Group:		Development/Library
Requires:	%{name} = %{version}-%{release}

%description devel
Network Client library (Development)

%prep
%setup -q


%build
%if 0%{?model_build_feature_network_dsds} == 1
export DUALSIM_CFLAGS+=" -DTIZEN_DUALSIM_ENABLE"
%endif

%if 0%{?gtests:1}
export GTEST_CFLAGS+=" -DGTEST_ENABLED"
%endif

./autogen.sh
./configure --prefix=/usr --libdir=%{_libdir} --enable-gcov=%{?gcov:yes}%{!?gcov:no}

make %{?_smp_mflags}


%if 0%{?gtests:1}
cd gtest
make
cd ..
%endif


%install
%make_install

%if 0%{?gtests:1}
cd gtest
mkdir -p %{buildroot}/%{_bindir}
install -m 0755 gtest-%{name} %{buildroot}/%{_bindir}/gtest-%{name}
cd ..
%endif

cd test
cp -rf %{buildroot}%{_libdir}/ ./
./build.sh
cd ..

%files
%manifest libnet-client.manifest
%{_libdir}/*.so.*
%license LICENSE
%if 0%{?gtests:1}
%{_bindir}/gtest-%{name}
%endif

%files devel
%defattr(-,root,root,-)
%{_includedir}/network/*.h
%{_libdir}/*.so
%{_libdir}/pkgconfig/network.pc
