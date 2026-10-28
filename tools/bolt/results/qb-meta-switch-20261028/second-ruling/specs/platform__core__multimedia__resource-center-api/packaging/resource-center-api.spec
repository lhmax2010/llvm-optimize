Name: resource-center-api
Summary: resource center library
Version: 0.1
Release: 1
Group:   Multimedia/Libraries
License: Apache-2.0
Source0: %{name}-%{version}.tar.gz
BuildRequires:  cmake
BuildRequires:  pkgconfig(dlog)
BuildRequires:  pkgconfig(gio-2.0)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(libtzplatform-config)
BuildRequires:  pkgconfig(resource-manager)
BuildRequires:  pkgconfig(resource-information)

Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig

%description
Resource center library in Tizen

%package devel
Summary: resource center library (Development)
Group: TO_BE/FILLED_IN
Requires: %{name} = %{version}-%{release}

%description devel
Resource center library in Tizen (DEV)

%if ("%{_vd_cfg_licensing}" == "y")
%{?!TOMATO: %define TOMATO n}
%else
%{?!TOMATO: %define TOMATO y}
%endif

%prep
%setup -q

%build
%if (%{TOMATO} == "y")
export CXXFLAGS="$CXXFLAGS %{?__vd_cxxflags} -Wno-error"
%endif

MAJORVER=`echo %{version} | awk 'BEGIN {FS="."}{print $1}'`
cmake . \
      -DFULLVER=%{version} \
      -DMAJORVER=${MAJORVER} \
      -DLIB_DIR=%{_libdir} \
      -DCMAKE_INSTALL_PREFIX=%{_libdir}
make %{?jobs:-j%jobs}

%install
rm -rf %{buildroot}
%if (%{TOMATO} == "y")
mkdir -p %{buildroot}%{_tomatodir}
mkdir -p %{buildroot}%{_tomatodir}/tc
cp -rf ut/tc/* %{buildroot}%{_tomatodir}/tc
%endif

%make_install

%clean

%post
/sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%{_libdir}/libresource-center-api.so.*
%manifest resource-center-api.manifest
%license LICENSE.APLv2
#%{_bindir}/resource_center_test

%files devel
%{_includedir}/resource_center.h
%{_includedir}/resource_center_internal.h
%{_libdir}/pkgconfig/*.pc
%{_libdir}/*.so
