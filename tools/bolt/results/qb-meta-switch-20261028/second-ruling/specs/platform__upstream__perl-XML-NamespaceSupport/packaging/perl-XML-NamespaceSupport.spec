#
# spec file for package perl-XML-NamespaceSupport
#
# Copyright (c) 2017 SUSE LINUX GmbH, Nuernberg, Germany.
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

%define cpan_name XML-NamespaceSupport

Name:           perl-XML-NamespaceSupport
Version:        1.12
Release:        0
Summary:        Simple Generic Namespace Processor
License:        Artistic-1.0 or GPL-1.0+
Group:          Development/Libraries/Perl
Url:            http://search.cpan.org/dist/XML-NamespaceSupport/
Source0:        https://cpan.metacpan.org/authors/id/P/PE/PERIGRIN/%{cpan_name}-%{version}.tar.gz
Source1001:     %{name}.manifest

BuildRequires:  perl
BuildRequires:  perl-macros

%description
This module offers a simple to process namespaced XML names (unames) from
within any application that may need them. It also helps maintain a prefix
to namespace URI map, and provides a number of basic checks.

The model for this module is SAX2's NamespaceSupport class, readable at
http://www.saxproject.org/namespaces.html It adds a few perlisations where
we thought it appropriate.

%prep
%setup -q -n XML-NamespaceSupport-%{version}
cp %{SOURCE1001} .

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
%{__make} %{?_smp_mflags}

%check
%{__make} test

%install
%perl_make_install
%perl_process_packlist
%perl_gen_filelist

%files -f %{name}.files
%manifest %{name}.manifest
%defattr(-,root,root,755)
%doc Changes README
%license LICENSE

%changelog

