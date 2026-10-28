Name:           perl-Package-Stash
Version:        0.40
Release:        1
License:        Artistic-1.0 OR GPL-1.0-or-later
Summary:        Routines for manipulating stashes
Url:            https://metacpan.org/pod/Package::Stash
Group:          Development/Libraries
Source0:        %{name}-%{version}.tar.gz
Source1001: 	perl-Package-Stash.manifest
BuildRequires:  perl
BuildRequires:  perl(MIME::Base64)

%description
Manipulating stashes (Perl's symbol tables) is occasionally
necessary, but incredibly messy, and easy to get wrong. 
This module hides all of that behind a simple API.

NOTE: Most methods in this class require a variable specification
that includes a sigil. If this sigil is absent, it is assumed 
to represent the IO slot.

Due to limitations in the typeglob API available to perl code, 
and to typeglob manipulation in perl being quite slow, this module
provides two implementations - one in pure perl, and one using XS.
The XS implementation is to be preferred for most usages; the pure
perl one is provided for cases where XS modules are not a possibility.
The current implementation in use can be set by setting 
$ENV{PACKAGE_STASH_IMPLEMENTATION} or $Package::Stash::IMPLEMENTATION 
before loading Package::Stash (with the environment variable 
taking precedence), otherwise, it will use the XS implementation 
if possible, falling back to the pure perl one.

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
