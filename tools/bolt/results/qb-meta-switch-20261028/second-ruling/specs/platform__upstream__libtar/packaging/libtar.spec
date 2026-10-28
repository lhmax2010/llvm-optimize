Name:       libtar 
Summary:    %{name}
Version:    1.2.20 
Release:    0

# ==========================================================
License:    NCSA
# ==========================================================

Group:      Development/ROS
Source0:    %{name}-%{version}.tar.gz
Source10:   Use-reentrant-versions-of-getpwnam-getgrnam.patch
Source1001: %{name}.manifest

# ==========================================================
# BuildRequires
# specifies build-time dependencies for the package
# ==========================================================
BuildRequires:  libtool
BuildRequires:  automake

%description
Library for manipulating tar files from within C programs

%package devel
Summary:    %{name}-devel
Requires:   %{name} = %{version}

%description devel
Library for manipulating tar files from within C programs(devel)

%define keepstatic 1

%prep
%setup -q
%{__patch} -p1 < %{SOURCE10}
cp %{SOURCE1001} .

# ==========================================================
# build section
# how to actually build the software we are packaging
# ==========================================================
%build
export CFLAGS="$CFLAGS -Wall -fPIE"
export CXXFLAGS="$CXXFLAGS -Wall -fPIE"
export LDFLAGS="$LDFLAGS -Wl,--as-needed -pie"

aclocal
autoreconf -fvi
%{configure}
%{make_build}


# ==========================================================
# install section
# how to actually build the software we are packaging
# ==========================================================
%install
%{make_install}
%{remove_docs}

%clean  

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

# ==========================================================
# files section
# The list of files that will be installed in the end 
# user’s system.
# ==========================================================
%files
%manifest %{name}.manifest
%license COPYRIGHT
%{_bindir}/%{name}
%{_libdir}/%{name}.so.*

%files devel
%manifest %{name}.manifest
%license COPYRIGHT
%{_libdir}/%{name}.so
%{_libdir}/%{name}.a
%{_includedir}/*.h
