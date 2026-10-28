Name:           perl-namespace-autoclean
Version:        0.31
Release:        1
License:        perl_5
Summary:        Keep imports out of your namespace
Url:            https://metacpan.org/pod/namespace::autoclean
Group:          Development/Libraries
Source0:        perl-namespace-autoclean-%{version}.tar.gz
Source1001: 	perl-namespace-autoclean.manifest
BuildRequires:  perl
BuildRequires:  perl(MIME::Base64)

%description
When you import a function into a Perl package, it will naturally also be available as a method.
The namespace::autoclean pragma will remove all imported symbols at the end of the current package's 
compile cycle. Functions called in the package itself will still be bound by their name, 
but they won't show up as methods on your class or instances.
This module is very similar to namespace::clean, except it will clean all imported functions,
no matter if you imported them before or after you used the pragma. 
It will also not touch anything that looks like a method.
If you're writing an exporter and you want to clean up after yourself (and your peers), 
you can use the -cleanee switch to specify what package to clean:

package My::MooseX::namespace::autoclean;
use strict;
 
use namespace::autoclean (); # no cleanup, just load
 
sub import {
    namespace::autoclean->import(
      -cleanee => scalar(caller),
    );
}

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
