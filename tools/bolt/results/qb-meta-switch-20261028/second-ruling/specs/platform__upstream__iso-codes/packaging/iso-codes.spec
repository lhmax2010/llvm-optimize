Name:           iso-codes
Version:        4.18.0
Release:        1
License:        LGPL-2.1+
Summary:        ISO code lists and translations
Url:            https://salsa.debian.org/iso-codes-team/iso-codes
Group:          System/Base
Source0:        iso-codes-%{version}.tar.gz
Source1001:     iso-codes.manifest
BuildRequires:  gettext-tools
BuildRequires:  pkgconfig(python3)
BuildArch:      noarch

%description
This package provides the ISO 639 Language code list, the ISO 4217
Currency code list, the ISO 3166 Territory code list, and ISO 3166-2
sub-territory lists, and all their translations in gettext format.

%package devel
Summary:        Files for development using %{name}
Group:          Development/Libraries
Requires:       %{name} = %{version}

%description devel
This package contains the pkg-config files for development
when building programs that use %{name}.

%prep
%setup -q
cp %{SOURCE1001} .

%build

%configure
%{__make} %{?_smp_mflags}

%install
%make_install

%find_lang iso-codes --all-name

%files -f iso-codes.lang
%license COPYING
%manifest %{name}.manifest
%dir %{_datadir}/xml/%{name}
%{_datadir}/xml/%{name}/*.xml
%{_datadir}/%{name}/json/*.json

%files devel
%license COPYING
%manifest %{name}.manifest
%{_datadir}/pkgconfig/iso-codes.pc

