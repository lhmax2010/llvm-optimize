#
# spec file for package nsjail
#

Name:           nsjail
Version:        3.0.20210707 
Release:	0
Summary:        A light-weight process isolation tool
License:        Apache-2.0
Group:          System/Other
URL:            https://nsjail.com
#X-Vcs-Url:     https://github.com/google/nsjail.git
Source0:        nsjail-%{version}.tar.gz
#Source1:        kafel.tar.gz
Source1001:	%{name}.manifest
Source1002:	%{name}.service
Source1003:	%{name}.sh
Source2001:	0001-Add-special-rules-for-generated-headers.patch
BuildRequires:  autoconf
BuildRequires:  bison
BuildRequires:  flex
BuildRequires:  gcc-c++
#BuildRequires:  git-core
BuildRequires:  glibc-devel
BuildRequires:  libnl3-devel
BuildRequires:  make
BuildRequires:  pkgconfig
BuildRequires:  protobuf-devel

%description
A light-weight process isolation tool, making use of Linux namespaces and
seccomp-bpf syscall filters (with help of the kafel bpf language)

%package test
Summary:  Tizen nsjail test programs
Group:    System/Other
Requires: %{name} = %{version}-%{release}

%description test
Tizen simple test programs to check nsjail execution validation in Tizen platform

%prep
%setup -q
cp %{SOURCE1001} .
cp %{SOURCE1002} .
cp %{SOURCE1003} .

%build
export CFLAGS="$CFLAGS -DTIZEN"
export CXXFLAGS="$CXXFLAGS -DTIZEN"
%ifarch %{arm}
export LDFLAGS="$LDFLAGS -mthumb"
%endif
tar -xf kafel.tar.gz
pushd kafel
for p in %{SOURCE2001}; do
	patch -p1 < $p
done
popd
make %{?_smp_mflags}

pushd test
make %{?_smp_mflags}
popd test

%install
mkdir -p %{buildroot}/%{_bindir}/
mkdir -p %{buildroot}/%{_bindir}/nsjail_test/
mkdir -p %{buildroot}/usr/share/
mkdir -p %{buildroot}/usr/share/lua-libs/
mkdir -p %{buildroot}/usr/share/lua-scripts/

mkdir -p %{buildroot}/%{_unitdir}

install -m 0755 nsjail %{buildroot}/%{_bindir}/
install -m 0755 cgroup_remount %{buildroot}/%{_bindir}/
install -m 0755 nsjail.sh %{buildroot}/%{_bindir}/
install -m 0644 nsjail.service %{buildroot}/%{_unitdir}/
%install_service multi-user.target.wants nsjail.service

cp -a test/*_test %{buildroot}/%{_bindir}/nsjail_test/
cp -a test/*.cfg %{buildroot}/usr/share/

%files
%manifest %{name}.manifest
%license LICENSE
%{_bindir}/nsjail
%{_bindir}/nsjail.sh
%{_bindir}/cgroup_remount*
%{_unitdir}/nsjail.service
%{_unitdir}/multi-user.target.wants/nsjail.service
/usr/share/lua-libs
/usr/share/lua-scripts

%files test
%manifest %{name}.manifest
%{_bindir}/nsjail_test/*
/usr/share/*

%changelog
* Mon Jul 7 2021 Baik 
 - Initial import of version latest version of nsjail - 2021-07-07 version 
