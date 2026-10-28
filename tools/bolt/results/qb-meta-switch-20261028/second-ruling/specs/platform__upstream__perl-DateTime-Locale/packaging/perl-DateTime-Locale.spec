Name:           perl-DateTime-Locale
Version:        1.44
Release:        1
License:        Artistic-1.0 OR GPL-1.0-or-later
Summary:        Class for locale objects instantiated from pre-defined data
Url:            https://metacpan.org/pod/DateTime::Locale::FromData
Group:          Development/Libraries
Source0:        %{name}-%{version}.tar.gz
Source1001: 	perl-DateTime-Locale.manifest
BuildRequires:  perl
BuildRequires:  perl-File-ShareDir-Install
BuildRequires:  perl(MIME::Base64)

%description
This class is used to represent locales instantiated
from the data in the DateTime::Locale::Data module.

%prep
%setup -q -n %{name}-%{version}
cp %{SOURCE1001} .

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
%perl_make_install
%perl_process_packlist
%perl_gen_filelist

%files -f %{name}.files
%license LICENSE
