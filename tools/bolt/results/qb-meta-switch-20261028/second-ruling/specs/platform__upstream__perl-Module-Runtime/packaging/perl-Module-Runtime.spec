Name:           perl-Module-Runtime
Version:        0.016
Release:        1
License:        Artistic-1.0 OR GPL-1.0-or-later
Summary:        runtime module handling
Url:            https://metacpan.org/pod/Module::Runtime
Group:          Development/Libraries
Source0:        %{name}-%{version}.tar.gz
Source1001: 	perl-Module-Runtime.manifest
BuildRequires:  perl
BuildRequires:  perl(MIME::Base64)

%description
The functions exported by this module deal with runtime handling of Perl modules,
which are normally handled at compile time. This module avoids using any other modules,
so that it can be used in low-level infrastructureb.

The parts of this module that work with module names apply the same syntax
that is used for barewords in Perl source. In principle this syntax can 
vary between versions of Perl, and this module applies the syntax of 
the Perl on which it is running. In practice the usable syntax hasn't changed yet. 
There's some intent for Unicode module names to be supported in the future, 
but this hasn't yet amounted to any consistent facility.

The functions of this module whose purpose is to load modules include workarounds 
for three old Perl core bugs regarding require. These workarounds are applied on any Perl version 
where the bugs exist, except for a case where one of the bugs cannot be adequately worked around in pure Perl.

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
%license README
