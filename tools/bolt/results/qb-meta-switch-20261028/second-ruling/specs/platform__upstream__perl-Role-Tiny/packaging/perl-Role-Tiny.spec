Name:           perl-Role-Tiny
Version:        2.002004
Release:        1
License:        Artistic-1.0 OR GPL-1.0-or-later
Summary:        Roles: a nouvelle cuisine portion size slice of Moose
Url:            https://metacpan.org/pod/Role::Tiny
Group:          Development/Libraries
Source0:        %{name}-%{version}.tar.gz
Source1001: 	perl-Role-Tiny.manifest
BuildRequires:  perl
BuildRequires:  perl(MIME::Base64)

%description
Role::Tiny is a minimalist role composition tool.

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
