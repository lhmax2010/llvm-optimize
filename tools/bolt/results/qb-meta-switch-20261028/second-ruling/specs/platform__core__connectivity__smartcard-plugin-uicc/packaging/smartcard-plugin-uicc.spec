Name:             smartcard-plugin-uicc
Summary:          Smartcard plugin uicc
Version:          0.0.12
Release:          0
Group:            libs
License:          Apache-2.0
Source0:          %{name}-%{version}.tar.gz
BuildRequires:    cmake
BuildRequires:    pkgconfig(glib-2.0)
BuildRequires:    pkgconfig(dlog)
BuildRequires:    pkgconfig(tapi)
BuildRequires:    pkgconfig(smartcard-service-common)
Requires(post):   /sbin/ldconfig
Requires(postun): /sbin/ldconfig


%description
Smartcard Service plugin uicc


%prep
%setup -q


%package    devel
Summary:    smartcard service uicc
Group:      Development/Libraries
Requires:   %{name} = %{version}-%{release}


%description devel
smartcard service.

%if 0%{?gcov:1}
%package gcov
Summary:    A smartcard-plugin-uicc gcov Tool
Group:      Network & Connectivity/Development

%description gcov
A smartcard-plugin-uicc gcov objects
%endif

%build
%if 0%{?gcov:1}
export CFLAGS="-fprofile-arcs -ftest-coverage"
export CXXFLAGS="-fprofile-arcs -ftest-coverage"
export LDFLAGS=" -lgcov"
%endif

%if 0%{?sec_build_binary_debug_enable}
export CFLAGS="$CFLAGS -DTIZEN_DEBUG_ENABLE"
export CXXFLAGS="$CXXFLAGS -DTIZEN_DEBUG_ENABLE"
export FFLAGS="$FFLAGS -DTIZEN_DEBUG_ENABLE"
%endif
mkdir obj-arm-limux-qnueabi
cd obj-arm-limux-qnueabi
cmake .. -DCMAKE_INSTALL_PREFIX=%{_prefix} \
%ifarch aarch64 x86_64 riscv64
	 -DTIZEN_ARCH_64=1 \
%endif
	 -DBUILD_GCOV=%{?gcov:1}%{!?gcov:0}

#make %{?jobs:-j%jobs}

%if 0%{?gcov:1}
mkdir -p gcov-obj
find . -name '*.gcno' -exec cp '{}' gcov-obj ';'
%endif

%install
cd obj-arm-limux-qnueabi
%make_install

%if 0%{?gcov:1}
mkdir -p %{buildroot}%{_datadir}/gcov/obj
install -m 0644 gcov-obj/* %{buildroot}%{_datadir}/gcov/obj
%endif


%post
/sbin/ldconfig


%postun
/sbin/ldconfig


%files
%manifest %{name}.manifest
%license LICENSE.APLv2
%defattr(-,root,root,-)
%{_libdir}/se/lib*.so

%if 0%{?gcov:1}
%files gcov
%{_datadir}/gcov/obj/*
%endif

