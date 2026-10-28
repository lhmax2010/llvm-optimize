#
# spec file for package perl-Net-DBus
#
# Copyright (c) 2011 SUSE LINUX Products GmbH, Nuernberg, Germany.
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via http://bugs.opensuse.org/
#



Name:           perl-Net-DBus
Version:        1.2.0
Release:        1
License:        GPL-2.0+
Summary:        Perl extension for the DBus message system
Url:            http://search.cpan.org/dist/Net-DBus/
Group:          Development/Libraries
Source:         http://www.cpan.org/authors/id/D/DA/DANBERR/Net-DBus-%{version}.tar.gz
Source1001: 	perl-Net-DBus.manifest
BuildRequires:  perl
BuildRequires:  perl(Test::Pod)
BuildRequires:  perl(Test::Pod::Coverage)
BuildRequires:  perl(XML::Twig)
BuildRequires:  perl-macros
# MANUAL
BuildRequires:  pkgconfig(dbus-1)
BuildRequires:  pkgconfig(pkg-config)
Requires:       perl(XML::Twig)

%description
Net::DBus provides a Perl API for the DBus message system. The DBus Perl
interface is currently operating against the 0.32 development version of
DBus, but should work with later versions too, providing the API changes
have not been too drastic.

Users of this package are either typically, service providers in which case
the the Net::DBus::Service manpage and the Net::DBus::Object manpage
modules are of most relevance, or are client consumers, in which case the
Net::DBus::RemoteService manpage and the Net::DBus::RemoteObject manpage
are of most relevance.

%prep
%setup -q -n %{name}-%{version}
cp %{SOURCE1001} .
find . -type f -print0 | xargs -0 chmod 644

%build
perl Makefile.PL INSTALLDIRS=vendor OPTIMIZE="%{optflags}"
make %{?_smp_mflags}

%check
make test

%install
%perl_make_install
%perl_process_packlist
%perl_gen_filelist

%files -f %{name}.files
%manifest %{name}.manifest
%defattr(-,root,root,755)
%doc AUTHORS examples LICENSE README

%changelog
