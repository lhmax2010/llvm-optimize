Name: liblbs-location
Summary: Location Based Service Library
Version: 1.4.9
Release: 1
Group: Location/Libraries
License: Apache-2.0
Source0:  %{name}-%{version}.tar.gz
Source1001: %{name}.manifest
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig
BuildRequires:  cmake
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(gmodule-2.0)
BuildRequires:  pkgconfig(dlog)
BuildRequires:  pkgconfig(vconf)
BuildRequires:  pkgconfig(capi-appfw-app-manager)
BuildRequires:  pkgconfig(cynara-client)
BuildRequires:  pkgconfig(cynara-session)
BuildRequires:  pkgconfig(json-glib-1.0)
BuildRequires:  pkgconfig(bundle)
BuildRequires:  pkgconfig(capi-system-sensor)
BuildRequires:  pkgconfig(cynara-creds-self)

%description
Location Based Service Library


%package devel
Summary:    Location Based Service Library (Development files)
Group:      Location/Development
Requires:   %{name} = %{version}-%{release}

%description devel
Location Based Service Library (Development files)
The package includes header files and pkgconfig file.


%prep
%setup -q -n %{name}-%{version}
cp %{SOURCE1001} .


%build
%ifarch %arm aarch64
export CFLAGS="$CFLAGS -DTIZEN_DEVICE"
export CXXFLAGS="$CXXFLAGS -DTIZEN_DEVICE"
export FFLAGS="$FFLAGS -DTIZEN_DEVICE"
%endif

# Call make instruction with smp support
MAJORVER=`echo %{version} | awk 'BEGIN {FS="."}{print $1}'`
cmake . -DCMAKE_INSTALL_PREFIX=%{_prefix} -DLIBDIR=%{_libdir} -DINCLUDEDIR=%{_includedir} \
-DFULLVER=%{version} -DMAJORVER=${MAJORVER} \

make %{?jobs:-j%jobs}


%install
rm -rf %{buildroot}
%make_install


%clean
rm -rf %{buildroot}


%post
/sbin/ldconfig


%postun -p /sbin/ldconfig


%files
%manifest %{name}.manifest
%license LICENSE
%{_libdir}/*.so.*

%files devel
%{_includedir}/location/*.h
%{_libdir}/pkgconfig/*.pc
%{_libdir}/*.so
