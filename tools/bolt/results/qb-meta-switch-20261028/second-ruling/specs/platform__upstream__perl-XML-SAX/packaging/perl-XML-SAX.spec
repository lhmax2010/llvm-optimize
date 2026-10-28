#
# spec file for package perl-XML-SAX (Version 0.96)
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

Name:           perl-XML-SAX
Version:        1.02
Release:        6
Group:          Development/Libraries/Perl
License:        Artistic License ..
Url:            http://www.cpan.org/modules/by-module/XML/
Summary:        XML::SAX Perl Module
Source:         XML-SAX-%{version}.tar.bz2
Source1001:     %{name}.manifest

BuildRequires:  libxml2-devel
BuildRequires:  perl-XML-NamespaceSupport
BuildRequires:  perl-macros

Requires:       perl-XML-NamespaceSupport

%description
XML::SAX consists of several framework classes for using and building
Perl SAX2 XML parsers, filters, and drivers. It is designed around the
need to be able to "plug in" different SAX parsers to an application
without requiring programmer intervention. Those of you familiar with
the DBI will be right at home. Some of the designs come from the Java
JAXP specification (SAX part), only without the javaness.

%prep
%setup -q -n XML-SAX-%{version}
cp %{SOURCE1001} .

%build
perl Makefile.PL
make %{?_smp_mflags}

%check
# make test

%install
make DESTDIR=$RPM_BUILD_ROOT install_vendor
cat << EOF > $RPM_BUILD_ROOT/%{perl_vendorlib}/XML/SAX/ParserDetails.ini
[XML::SAX::PurePerl]
http://xml.org/sax/features/namespaces = 1
EOF
%perl_process_packlist

%remove_docs

%clean
rm -rf $RPM_BUILD_ROOT

%files
%manifest %{name}.manifest
%defattr(-,root,root)
%license LICENSE
%{perl_vendorlib}/XML
%config(noreplace) %{perl_vendorlib}/XML/SAX/ParserDetails.ini
%{perl_vendorarch}/auto/XML

%changelog
