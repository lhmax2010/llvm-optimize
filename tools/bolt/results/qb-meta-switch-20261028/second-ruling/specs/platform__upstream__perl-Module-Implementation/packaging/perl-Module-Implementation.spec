Name:           perl-Module-Implementation
Version:        0.09
Release:        1
License:        Artistic-2.0
Summary:        Execute code after a scope finished compilation
Url:            https://metacpan.org/pod/Module::Implementation
Group:          Development/Libraries
Source0:        %{name}-%{version}.tar.gz
Source1001: 	perl-Module-Implementation.manifest
BuildRequires:  perl
BuildRequires:  perl(MIME::Base64)

%description
This module allows you to execute code when perl finished compiling the surrounding scope.

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
