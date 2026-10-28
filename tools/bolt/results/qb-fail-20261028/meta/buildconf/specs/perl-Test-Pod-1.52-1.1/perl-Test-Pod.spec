Name:           perl-Test-Pod
VCS:            platform/upstream/perl-Test-Pod#d31d9e37dae244901d26b233624f9fd3e6105546
Version:        1.52
Release:        1.1
License:        GPL-1.0 or Artistic-2.0
Summary:        check for POD errors in files
Group:          Development/Libraries/Perl
Url:            http://search.cpan.org/dist/Test-Pod/
%define cpan_name Test-Pod
Source:         %{cpan_name}-%{version}.tar.gz
Source1001: 	perl-Test-Pod.manifest
Source1002: 	LICENSE

BuildRequires:  perl
BuildRequires:  perl(File::Spec)
BuildRequires:  perl-Module-Build
BuildRequires:  perl(Pod::Simple) >= 3.05
BuildRequires:  perl(Test::More) >= 0.62

Requires:       perl(File::Spec)
Requires:       perl(Pod::Simple) >= 3.05
Requires:       perl(Test::Builder::Tester) >= 1.02
Requires:       perl(Test::More) >= 0.62

%description
Check POD files for errors or warnings in a test file, using 'Pod::Simple'
to do the heavy lifting.

%prep
%setup -q -n %{cpan_name}-%{version}
cp %{SOURCE1001} .
cp %{SOURCE1002} .

%build
perl Makefile.PL
%{__make}

%check
%{__make} test

%install
%perl_make_install
%remove_docs
%perl_process_packlist
%perl_gen_filelist

%files -f %{name}.files
%manifest %{name}.manifest
%license LICENSE

%changelog
