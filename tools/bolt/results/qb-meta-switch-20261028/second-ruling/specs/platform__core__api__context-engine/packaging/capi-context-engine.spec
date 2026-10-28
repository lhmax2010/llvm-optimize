Name:           capi-context-engine
Summary:        ContextEngine C API Library for Tizen
Version:        0.0.3
Release:        1
Group:          Development/Libraries
License:        Apache-2.0
URL:            https://github.com/samsung/contextengine
Source0:        %{name}-%{version}.tar.gz

BuildRequires:  cmake
BuildRequires:  pkgconfig(dlog)
BuildRequires:  pkgconfig(bundle)
BuildRequires:  pkgconfig(capi-base-common)
BuildRequires:  pkgconfig(capi-appfw-app-common)
BuildRequires:  pkgconfig(capi-system-info)
BuildRequires:  pkgconfig(rpc-port)
BuildRequires:  tidl

%description
Context Engine C API (CAPI) is a Tizen platform library that provides
access to context data collected and managed by the ContextEngine service.

%package devel
Summary:    ContextEngine C API (development files)
Group:      Development/Libraries
Requires:   %{name} = %{version}-%{release}

%description devel
Header files and pkgconfig data for the ContextEngine C API.

%prep
%setup -q

%build
%if "%{tizen_profile_name}" == "tv"
%cmake . -DLIB_INSTALL_DIR=%{_libdir} -DTIZEN_TV_EXT=ON
%else
%cmake . -DLIB_INSTALL_DIR=%{_libdir}
%endif
make %{?jobs:-j%jobs}

%install
rm -rf %{buildroot}
%make_install

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%license LICENSE
%{_libdir}/libcapi-context-engine.so.*

%files devel
%{_libdir}/libcapi-context-engine.so
%{_libdir}/pkgconfig/*.pc
%{_datadir}/%{name}/tidl/ContextEngine.tidl
%{_includedir}/context/context_engine.h
%{_includedir}/context/context_engine_internal.h
