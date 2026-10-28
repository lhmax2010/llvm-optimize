%define on_off() %{expand:%%{?with_%{1}:ON}%%{!?with_%{1}:OFF}}

Name:       libsessiond
Summary:    library to manage subsessions
Version:    11.0.0
Release:    1
Group:      System/Libraries
License:    MIT
Source0:    %{name}-%{version}.tar.gz
Source1:    %{name}.manifest
BuildRequires: cmake
BuildRequires: pkgconfig(capi-base-common)
BuildRequires: pkgconfig(gio-2.0)
BuildRequires: gtest-devel
BuildRequires: pkgconfig(libsmack)
BuildRequires: pkgconfig(dlog)
BuildRequires: pkgconfig(libsyscommon-plugin-api-sessiond)
BuildRequires: pkgconfig(libtzplatform-config)

Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig

%description

%package    devel
Summary:    Subsession support library - development headers
Group:      Development/Libraries
Requires:   libsessiond = %{version}-%{release}
%description devel

%package    tests
Summary:    Subsession support library - integration tests
Group:      Development/Libraries
%description tests

%package -n subsession-client-example
Summary:    Example program using libsessiond API
Group:      Development/Libraries
%description -n subsession-client-example

%package -n subsession-plugin-example
Summary:    Example plugin for sessiond
Group:      Development/Libraries
%description -n subsession-plugin-example

%prep
%setup -q

%build
mkdir -p build
pushd build
%cmake .. \
	-DVERSION=%{version} \
	-DCMAKE_BUILD_TYPE=Release

make %{?jobs:-j%jobs}
popd
cp %{SOURCE1} .

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%install
rm -rf %{buildroot}
pushd build
%make_install
popd

%files
%manifest libsessiond.manifest
%license LICENSE.MIT
%{_libdir}/libsessiond.so.*

%files devel
%manifest libsessiond.manifest
%license LICENSE.MIT
%{_libdir}/libsessiond.so
%{_libdir}/pkgconfig/libsessiond.pc
%{_includedir}/sessiond.h
%{_includedir}/sessiond-plugin-internal.h
%{_includedir}/sessiond-platform.h

%files tests
%manifest libsessiond.manifest
%license LICENSE.MIT
%{_bindir}/test_*
%{_bindir}/sessiond-integration-tests.sh

%files -n subsession-client-example
%manifest libsessiond.manifest
%license LICENSE.MIT
%{_bindir}/subsession-client-example

%files -n subsession-plugin-example
%manifest libsessiond.manifest
%license LICENSE.MIT
%{_libdir}/system/plugin/libplugin-backend-sessiond.so
