Name:           xmlto
Version:        0.0.28
Release:        0
License:        GPL-2.0+
Summary:        Tool for Converting XML Files to Various Formats
Url:            https://fedorahosted.org/xmlto/
Group:          Productivity/Publishing/XML
Source0:        https://fedorahosted.org/releases/x/m/xmlto/%{name}-%{version}.tar.bz2
Source1001: 	xmlto.manifest
BuildRequires:  docbook-xsl-stylesheets
BuildRequires:  flex
BuildRequires:  libxslt
BuildRequires:  sgml-skel
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
BuildRequires:  fdupes

# We rely entirely on the DocBook XSL stylesheets!
Requires:       docbook-xsl-stylesheets >= 1.56.0
Requires:       docbook_4
Requires:       xsltproc

%description
This is a package for converting XML files to various formats using XSL
stylesheets.  As a processor it depends on xsltproc and as a formatter
for print output it makes use of passivetex.

%prep
%setup -q
cp %{SOURCE1001} .


rm -f xmlif/xmlif.c

%build
CFLAGS="%{optflags} -fPIC -pie -Wno-implicit-int" \
%configure
make %{?_smp_mflags}

%check
make check

%install
%make_install
! mkdir %{buildroot}%{_datadir}/xmlto/xsl
%{fdupes '%{buildroot}%{_datadir}/xmlto'}

%files
%manifest %{name}.manifest
%defattr(-,root,root)
%doc COPYING
%{_bindir}/*
%{_mandir}/*/*
%{_datadir}/xmlto

%changelog
