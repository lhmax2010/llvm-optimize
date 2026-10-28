%define SYSTEM_PLUGIN_LIBDIR %{_libdir}/system/plugin

Name:           system-plugin-backend-update-control-generic
Version:        1.0.6
Release:        0
License:        Apache-2.0
Summary:        Plugin for BART
Group:          Development/System
Source0:        %{name}-%{version}.tar.gz

Source1001:     %{name}.manifest
BuildRequires:  cmake
BuildRequires:  pkgconfig(dlog)
BuildRequires:  pkgconfig(libcurl)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(gio-2.0)
BuildRequires:  pkgconfig(gio-unix-2.0)
BuildRequires:  pkgconfig(hal-api-device)
BuildRequires:  pkgconfig(alarm-service)
BuildRequires:  pkgconfig(libsyscommon)
BuildRequires:  pkgconfig(libsyscommon-plugin-api-update-control)
BuildRequires:  pkgconfig(capi-system-info)

%description
Plugin for BART

%prep
%setup -q
cp %{SOURCE1001} .

%build
MAJORVER=`echo %{version} | awk 'BEGIN {FS="."}{print $1}'`

%if 0%{?asan:1}
export CFLAGS+=" -Wno-stringop-truncation"
%endif

%cmake . -DMAJORVER=${MAJORVER} \
	 -DFULLVER=%{version} \
	 -DDEBUG_MODE=on \
	 -DPLUGIN_LIB_DIR=%{SYSTEM_PLUGIN_LIBDIR}

%__make %{?jobs:-j%jobs}

%install
%make_install
mkdir -p %{buildroot}/%{_bindir}
install -m 0755 tools/scripts/make-update-control-config.sh %{buildroot}/%{_bindir}/make-update-control-config.sh

%post
/sbin/ldconfig
chsmack -a 'System::Tools' %{_bindir}/make-update-control-config.sh

%postun -p /sbin/ldconfig

%files
%manifest %{name}.manifest
%license LICENSE
%{SYSTEM_PLUGIN_LIBDIR}/libplugin-backend-update-control.so*
%{_bindir}/make-update-control-config.sh
