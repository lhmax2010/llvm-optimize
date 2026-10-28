Name:           perl-B-Hooks-EndOfScope
Version:        0.28
Release:        0
License:        perl_5
Summary:        Execute code after a scope finished compilation
Url:            https://metacpan.org/pod/B::Hooks::EndOfScope
Group:          Development/Libraries
Source0:        perl-B-Hooks-EndOfScope-%{version}.tar.gz
Source1001: 	perl-B-Hooks-EndOfScope.manifest
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
%license LICENCE
