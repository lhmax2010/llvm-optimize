Name:           perl-DateTime-TimeZone
Version:        2.63
Release:        1
License:        Artistic-1.0 OR GPL-1.0-or-later
Summary:        Time zone object base class and factory
Url:            https://metacpan.org/pod/DateTime::TimeZone
Group:          Development/Libraries
Source0:        %{name}-%{version}.tar.gz
Source1001: 	perl-DateTime-TimeZone.manifest
BuildRequires:  perl
BuildRequires:  perl(MIME::Base64)

%description
This class is the base class for all time zone objects. 
A time zone is represented internally as a set of observances,
each of which describes the offset from GMT for a given time period.

Note that without the DateTime module, this module does not do much.
It's primary interface is through a DateTime object,
and most users will not need to directly use DateTime::TimeZone methods.

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
