Name:      sgml-common
Version:   0.6.3
Release:   0
Group:     Applications/Text
Summary:   Common SGML catalog and DTD files
License:   GPL-2.0
# Actually - there is no homepage of this project, on that URL 
# page you could get complete ISO 8879 listing as was on the 
# old page - only part of it is included in sgml-common package.
URL:       http://www.w3.org/2003/entities/
Source0:   %{name}-%{version}.tar.bz2
# Following 4 from openjade/pubtext - same maintainer as in
# SGML-common, so up2date:
Source1:   xml.dcl
Source2:   xml.soc
Source3:   html.dcl
Source4:   html.soc
Patch0:    sgml-common-umask.patch
Patch1:    sgml-common-xmldir.patch
BuildArch: noarch
BuildRequires: libxml2 >= 2.4.8-2
BuildRequires: automake
BuildRequires: docbook_4

%description
The sgml-common package contains a collection of entities and DTDs
that are useful for processing SGML, but that don't need to be
included in multiple packages.  Sgml-common also includes an
up-to-date Open Catalog file.

%package -n xml-common
Group: Applications/Text
Summary: Common XML catalog and DTD files
License: GPL-2.0
URL: http://www.w3.org/2003/entities/

%description -n xml-common
The xml-common is a subpackage of sgml-common which contains 
a collection XML catalogs that are useful for processing XML, 
but that don't need to be included in main package.


%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
%reconfigure


%install
make install DESTDIR="%{buildroot}" htmldir='%{_datadir}/doc' INSTALL='install -p'
mkdir %{buildroot}%{_sysconfdir}/xml
mkdir -p %{buildroot}%{_datadir}/sgml/docbook
# Create an empty XML catalog.
XMLCATALOG=%{buildroot}%{_sysconfdir}/xml/catalog
%{_bindir}/xmlcatalog --noout --create $XMLCATALOG
# Now put the common DocBook entries in it
%{_bindir}/xmlcatalog --noout --add "delegatePublic" \
    "-//OASIS//ENTITIES DocBook XML" \
    "file://%{_datadir}/sgml/docbook/xmlcatalog" $XMLCATALOG
%{_bindir}/xmlcatalog --noout --add "delegatePublic" \
    "-//OASIS//DTD DocBook XML" \
    "file://%{_datadir}/sgml/docbook/xmlcatalog" $XMLCATALOG
%{_bindir}/xmlcatalog --noout --add "delegatePublic" \
    "ISO 8879:1986" \
    "file://%{_datadir}/sgml/docbook/xmlcatalog" $XMLCATALOG
%{_bindir}/xmlcatalog --noout --add "delegateSystem" \
    "http://www.oasis-open.org/docbook/" \
    "file://%{_datadir}/sgml/docbook/xmlcatalog" $XMLCATALOG
%{_bindir}/xmlcatalog --noout --add "delegateURI" \
    "http://www.oasis-open.org/docbook/" \
    "file://%{_datadir}/sgml/docbook/xmlcatalog" $XMLCATALOG
# Also create the common DocBook catalog
%{_bindir}/xmlcatalog --noout --create \
    %{buildroot}%{_datadir}/sgml/docbook/xmlcatalog

rm -f %{buildroot}%{_datadir}/sgml/xml.dcl

install -p -m0644 %{SOURCE1} %{SOURCE2} %{SOURCE3} %{SOURCE4} \
    %{buildroot}%{_datadir}/sgml

rm -rf %{buildroot}%{_datadir}/xml/*
rm -f %{buildroot}%{_datadir}/doc/*.html


%files
%dir %{_sysconfdir}/sgml
%config(noreplace) %{_sysconfdir}/sgml/sgml.conf
%dir %{_datadir}/sgml
%dir %{_datadir}/sgml/sgml-iso-entities-8879.1986
%{_datadir}/sgml/sgml-iso-entities-8879.1986/*
%{_datadir}/sgml/xml.dcl
%{_datadir}/sgml/xml.soc
%{_datadir}/sgml/html.dcl
%{_datadir}/sgml/html.soc
%{_bindir}/sgmlwhich
%{_bindir}/install-catalog
%doc %{_mandir}/man8/install-catalog.8*

%files -n xml-common
%dir %{_sysconfdir}/xml
%config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/xml/catalog
%dir %{_datadir}/sgml
%dir %{_datadir}/sgml/docbook
%verify(not md5 size mtime) %{_datadir}/sgml/docbook/xmlcatalog
%dir %{_datadir}/xml
