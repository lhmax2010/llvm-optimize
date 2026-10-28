Name:       libcgroup
Summary:    Linux control group abstraction library
Version:    3.2.0
Release:    0

# ==========================================================
License:    LGPL-2.1
# ==========================================================

Url:        https://github.com/libcgroup/libcgroup
Group:      System/Management
Source0:    %{name}-%{version}.tar.gz
Source1001: %{name}.manifest

# ==========================================================
# BuildRequires
# specifies build-time dependencies for the package
# ==========================================================
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gtest-devel
BuildRequires:  bison
BuildRequires:  flex
BuildRequires:  pam-devel
BuildRequires:  systemd-devel

%description
libcgroup is a library that abstracts the control group file system \
in Linux. Control groups allow you to limit, account and isolate resource usage \
(CPU, memory, disk I/O, etc.) of groups of processes.

%package devel
Summary:        Linux control group abstraction library.(devel)
Group:          Development/Libraries/C and C++
Requires:       %name = %version

%description devel
libcgroup is a library that abstracts the control group file system \
in Linux. Control groups allow you to limit, account and isolate resource usage \
(CPU, memory, disk I/O, etc.) of groups of processes.(devel)

%package tools
Summary:        Linux control group abstraction library.(tools)
Group:          System/Management

%description tools
libcgroup is a library that abstracts the control group file system \
in Linux. Control groups allow you to limit, account and isolate resource usage \
(CPU, memory, disk I/O, etc.) of groups of processes.(tools)


%prep
%setup -q
cp %{SOURCE1001} .

# ==========================================================
# build section
# how to actually build the software we are packaging
# ==========================================================
%build
export CFLAGS="$CFLAGS -Wall -fPIE"
export CXXFLAGS="$CXXFLAGS -Wall -fPIE"
export LDFLAGS="$LDFLAGS -Wl,--as-needed -pie"
autoreconf -fi
%{configure}
%{__make} %{?_smp_mflags}


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
%license COPYING
%{_libdir}/libcgroup.so.*

%files tools
%manifest %{name}.manifest
%license COPYING
%{_bindir}/*
%{_sbindir}/*
%{_libdir}/security/pam_cgroup.so


%files devel
%manifest %{name}.manifest
%license COPYING
%{_includedir}/*.h
%{_includedir}/libcgroup/*.h
%{_libdir}/*.so
%{_libdir}/pkgconfig/libcgroup.pc
