Name:           perl-Switch
Version:        2.17
Release:        1
License:        GPL-1.0+ or Artistic-1.0
%define cpan_name Switch
Summary:        A switch statement for Perl
Group:          Development/Libraries
Url:            http://search.cpan.org/dist/Switch/
Source:         %{cpan_name}-%{version}.tar.gz
Source1001: 	perl-Switch.manifest
Source1002: 	LICENSE

BuildRequires:  perl
BuildRequires:  perl-macros
BuildArch:      noarch

%description
The Switch.pm module implements a generalized case mechanism that covers
most (but not all) of the numerous possible combinations of switch and case
values described above.

The module augments the standard Perl syntax with two new control
statements: 'switch' and 'case'. The 'switch' statement takes a single
scalar argument of any type, specified in parentheses. 'switch' stores this
value as the current switch value in a (localized) control variable. The
value is followed by a block which may contain one or more Perl statements
(including the 'case' statement described below). The block is
unconditionally executed once the switch value has been cached.

%prep
%setup -q -n %{cpan_name}-%{version}
cp %{SOURCE1001} .
cp %{SOURCE1002} .

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%check
make test

%install
%perl_make_install
%perl_process_packlist
%perl_gen_filelist

%files -f %{name}.files
%manifest %{name}.manifest
%license LICENSE

%changelog
