Name:           lsof
Version:        4.91
Release:        0
License:        Zlib
Summary:        A utility which lists open files on a Linux/UNIX system
URL:            http://people.freebsd.org/~abe/
Group:          Base/Tools
# lsof contains licensed code that we cannot ship.  Therefore we use
# upstream2downstream.sh script to remove the code before shipping it.
Source0:        %{name}_%{version}-linux-only.tar.xz
#Source1:        upstream2downstream.sh
Source1001: 	lsof.manifest

%description
Lsof stands for LiSt Open Files, and it does just that: it lists
information about files that are open by the processes running on a
UNIX system.

%prep
%setup -q -n %{name}_%{version}-linux-only
cp %{SOURCE1001} .

%build
LSOF_CC="${CC}" LSOF_VSTR=2.6.16 LINUX_BASE=/proc ./Configure -n linux

make DEBUG="%{optflags} -fPIC" CFGL="-pie " %{?_smp_mflags}

%install
install -Dm755 lsof %{buildroot}%{_sbindir}/lsof
install -Dm644 lsof.8 %{buildroot}%{_mandir}/man8/lsof.8


%docs_package

%files
%manifest %{name}.manifest
%{_sbindir}/lsof
