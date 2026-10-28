%define libname tracker

Name:       lib%{libname}
Summary:    tracker library for system information
Version:    1.0.1
Release:    1
Group:      System/Libraries
License:    Apache-2.0
Source0:    %{name}-%{version}.tar.gz
Source1001: %{name}.manifest
BuildRequires:  cmake
BuildRequires:  pkgconfig(capi-base-common)
BuildRequires:  pkgconfig(dlog)
BuildRequires:  pkgconfig(glib-2.0)

Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig

%description
Tracker library for system information.

%package devel
Summary:    tracker library for system information (devel)
Group:      Development/Libraries
Requires:   %{name} = %{version}-%{release}

%description devel
Tracker library for system information (devel)

%prep
%setup -q
cp %{SOURCE1001} .


%build
MAJORVER=`echo %{version} | awk 'BEGIN {FS="."}{print $1}'`

%cmake . \
	-DCMAKE_INSTALL_PREFIX=%{_prefix} \
	-DLIBNAME=%{libname} \
	-DMAJORVER=${MAJORVER} \
	-DFULLVER=%{version}

make %{?jobs:-j%jobs}

%install
%make_install

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%license LICENSE
%manifest %{name}.manifest
%{_libdir}/%{name}.so.*

%files devel
%manifest %{name}.manifest
%{_includedir}/%{name}/%{libname}.h
%{_libdir}/%{name}.so
%{_libdir}/pkgconfig/%{libname}.pc
