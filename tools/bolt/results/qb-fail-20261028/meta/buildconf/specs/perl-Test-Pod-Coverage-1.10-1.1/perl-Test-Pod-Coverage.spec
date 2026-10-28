Name:           perl-Test-Pod-Coverage
VCS:            platform/upstream/perl-Test-Pod-Coverage#b0e183e415832c40a47d315475bbb6cdadbb1c45
Version:        1.10
Release:        1.1
License:        GPL-1.0+ or Artistic-1.0
Summary:        Test::Pod::Coverage Perl module
Group:          Development/Libraries/Perl
Url:            http://search.cpan.org/dist/Test-Pod-Coverage/
%define cpan_name Test-Pod-Coverage
Source:         %{cpan_name}-%{version}.tar.gz
Source1001: 	perl-Test-Pod-Coverage.manifest
Source1002: 	LICENSE

BuildRequires:  perl
BuildRequires:  perl(Pod::Coverage)
BuildRequires:  perl(Test::Pod)
BuildRequires:  perl-macros

Requires:       perl(Pod::Coverage)

%description
Test::Pod::Coverage Perl module

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
# do not perl_process_packlist (noarch)
# remove .packlist file
rm -rf %{buildroot}%perl_vendorarch
# remove perllocal.pod file
rm -rf %{buildroot}%perl_archlib
%perl_gen_filelist

%files -f %{name}.files
%manifest %{name}.manifest
%license LICENSE

%changelog
