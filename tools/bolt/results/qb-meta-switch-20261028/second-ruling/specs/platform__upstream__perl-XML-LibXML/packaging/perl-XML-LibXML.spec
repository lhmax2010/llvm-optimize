#
# spec file for package perl-XML-LibXML (Version 1.70)
#
# Copyright (c) 2010 SUSE LINUX Products GmbH, Nuernberg, Germany.
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

%define cpan_name XML-LibXML
Name:           perl-XML-LibXML
Summary:        Perl Binding for libxml2
Version:        2.0210
Release:        0
Group:          Development/Libraries/Perl
License:        Artistic License ..
Url:            http://search.cpan.org/dist/XML-LibXML/
Source:         %{cpan_name}-%{version}.tar.bz2
Source1001:     %{name}.manifest

BuildRequires:  libxml2-devel
BuildRequires:  perl
BuildRequires:  perl-Alien-Build
BuildRequires:  perl-Alien-Libxml2
BuildRequires:  perl-XML-SAX-Base
BuildRequires:  perl-XML-SAX

%description
This module implements a Perl interface to the Gnome libxml2 library which
provides interfaces for parsing and manipulating XML files. This module allows
Perl programmers to make use of the highly capable validating XML parser and
the high performance DOM implementation.

Authors:
	Matt Sergeant, Christian Glahn, Petr Pajas

%prep
%setup -q -n %{cpan_name}-%{version}
cp %{SOURCE1001} .

%build
%{__perl} Makefile.PL OPTIMIZE="$RPM_OPT_FLAGS -Wall -Wno-error=incompatible-pointer-types"
%{__make} %{?_smp_mflags}

%check
# %{__make} test

%install
%perl_make_install
%perl_process_packlist
%perl_gen_filelist

%files -f %{name}.files
%manifest %{name}.manifest
%defattr(-,root,root)
%doc Changes LICENSE README

%changelog
