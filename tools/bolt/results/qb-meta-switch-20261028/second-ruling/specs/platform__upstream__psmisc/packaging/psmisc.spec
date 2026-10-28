Name:           psmisc
Version:        23.7
Release:        1
Summary:        Utilities for managing processes on your system
License:        GPL-2.0
Group:          System/Utilities
Url:            http://sourceforge.net/projects/psmisc/
Source:         %{name}-%{version}.tar.gz
Source1001:     psmisc.manifest

BuildRequires:  automake
BuildRequires:  gcc-c++
BuildRequires:  glibc-devel
BuildRequires:  ncurses-devel
BuildRequires:  gettext-tools

Provides:       ps:/usr/bin/killall

%description
The psmisc package contains utilities for managing processes on your
system: pstree, killall and fuser.  The pstree command displays a tree
structure of all of the running processes on your system.  The killall
command sends a specified signal (SIGTERM if nothing is specified) to
processes identified by name.  The fuser command identifies the PIDs of
processes that are using specified files or filesystems.

%prep
%setup -q
cp %{SOURCE1001} .

%build
export CFLAGS="$CFLAGS -fPIC -D_GNU_SOURCE -pipe"
export CXXFLAGS="$CXXFLAGS -fPIC -D_GNU_SOURCE -pipe"
export LDFLAGS="$LDFLAGS -pie"

%autogen
%configure --disable-rpath \
			--with-gnu-ld \
			--disable-nls

%__make %{?_smp_mflags} CFLAGS="$CFLAGS"

%install
%make_install
%remove_docs

%files
%manifest %{name}.manifest
%license COPYING
%{_bindir}/fuser
%{_bindir}/killall
%{_bindir}/peekfd
%{_bindir}/prtstat
%{_bindir}/pstree
%{_bindir}/pslog
%{_bindir}/pstree.x11
