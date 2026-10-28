%define __spec_check_pre exit 0

Name:           strace
BuildRequires:  libacl-devel
BuildRequires:  xz
Version:        6.6
Release:        0
License:        LGPL-2.1+ and GPL-2.0+
Summary:        A utility to trace the system calls of a program
Url:            http://sourceforge.net/projects/strace/
Group:          Development/Tools
Source:         http://dl.sourceforge.net/strace/strace-%{version}.tar.xz
Source2:        baselibs.conf
Source1001:     strace.manifest

%description
With strace, you can trace the activity of a program.  Information
about any system calls the program makes and the signals it receives
and processes can be seen.  Child processes can also be tracked.

%prep
%setup -q
cp %{SOURCE1001} .

%build
CFLAGS+=" %{optflags} -fPIE"
CXXFLAGS+=" %{optflags} -fPIE"
LDFLAGS+=" %{optflags} -pie"

%ifnarch aarch64
%configure
%else
%configure --enable-mpers=no
%endif

%__make %{?_smp_mflags}

# Have to exclude make check for qemu builds, which apparently don't support PTRACE.
%if !(0%{?qemu_user_space_build})
%check
%__make check
%endif

%install
%make_install
rm -f %{buildroot}%{_bindir}/strace-graph

%files
%manifest %{name}.manifest
%defattr(-,root,root)
%{_bindir}/strace
%{_bindir}/strace-log-merge
%doc %{_mandir}/man1/strace.1.gz
%doc %{_mandir}/man1/strace-log-merge.1.gz
