Name:           perl-TimeDate
VCS:            platform/upstream/perl-TimeDate#b8669a2b422dc95645ec742c0ca5a07a047bf614
Version:        2.33
Release:        2.1
Summary:        A Perl module for time and date manipulation

License:        GPL+ or Artistic
Url:            http://search.cpan.org/dist/TimeDate/
Group:          Development/Libraries
Source0:        http://www.cpan.org/authors/id/G/GB/GBARR/TimeDate-%{version}.tar.gz
Source1001: 	perl-TimeDate.manifest

BuildRequires:  perl(ExtUtils::MakeMaker)
Requires:       perl

%description
This module includes a number of smaller modules suited for
manipulation of time and date strings with Perl.  In particular, the
Date::Format and Date::Parse modules can display and read times and
dates in various formats, providing a more reliable interface to
textual representations of points in time.

%prep
%setup -q -n TimeDate-%{version}
cp %{SOURCE1001} .

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%check
#make test

%install
make pure_install PERL_INSTALL_ROOT=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
find %{buildroot} -depth -type d -exec rmdir {} 2>/dev/null ';'
%{_fixperms} %{buildroot}/*

%remove_docs

%files
%manifest %{name}.manifest
%{perl_vendorlib}/*

