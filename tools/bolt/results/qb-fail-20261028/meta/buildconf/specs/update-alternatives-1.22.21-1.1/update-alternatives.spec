#
# spec file for package update-alternatives
#
# Copyright (c) 2012 SUSE LINUX Products GmbH, Nuernberg, Germany.
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

%define admindir %{_localstatedir}/lib/rpm/

Name:           update-alternatives
VCS:            platform/upstream/update-alternatives#cb725fd97b792b5aab95b36bf6c7b808de48dd82
Version:        1.22.21
Release:        1.1
Summary:        Maintain symbolic links determining default commands
License:        GPL-2.0-or-later
URL:            https://git.dpkg.org/git/dpkg/dpkg.git
Source0:        %{name}-%{version}.tar.gz
Source1001:     %{name}.manifest

# BuildRequires for autotools build system
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  libtool
BuildRequires:  gettext-tools
BuildRequires:  ncurses-devel
BuildRequires:  libmd-devel

%description
update-alternatives creates, removes, maintains and displays
information about the symbolic links comprising the alternatives
system. It is possible for several programs fulfilling the same or
similar functions to be installed on a single system at the same time.
For example, many systems have several text editors installed at once.
This gives choice to the users of a system, allowing each to use a
different editor, if desired, but makes it difficult for a program to
make a good choice of editor to invoke if the user has not specified a
particular preference.

%prep
%setup -q -n dpkg-%{version}
cp %{SOURCE1001} .

%build
export CFLAGS="$CFLAGS -fPIC"
export CXXFLAGS="$CXXFLAGS -fPIC"
export LDFLAGS="$LDFLAGS -pie"

%{configure} \
    --with-admindir=%{admindir} \
    --disable-compiler-warnings # disable for sles10 -Wvla

make -C lib/compat %{?_smp_mflags}
make -C utils/ %{?_smp_mflags}

%install
install -d -m 0755 %{buildroot}/%{_sbindir}/
install -d -m 0755 %{buildroot}/%{_sysconfdir}/alternatives
install -d -m 0755 %{buildroot}/%{admindir}/alternatives
install -d -m 0755 %{buildroot}/%{_localstatedir}/log

install -m 0755 utils/%{name} %{buildroot}/%{_sbindir}

touch %{buildroot}/%{_localstatedir}/log/alternatives.log

%remove_docs

%files
%manifest %{name}.manifest
%defattr(-,root,root,-)
%license COPYING
%dir %{_sysconfdir}/alternatives
%dir %{_localstatedir}/lib/rpm/alternatives
%{_sbindir}/update-alternatives
%ghost %{_localstatedir}/log/alternatives.log

