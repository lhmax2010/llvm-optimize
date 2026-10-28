Name:           perl-Eval-Closure
Version:        0.14
Release:        1
License:        Artistic-1.0 OR GPL-1.0-or-later
Summary:        safely and cleanly create closures via string eval
Url:            https://metacpan.org/pod/Eval::Closure
Group:          Development/Libraries
Source0:        %{name}-%{version}.tar.gz
Source1001: 	perl-Eval-Closure.manifest
BuildRequires:  perl
BuildRequires:  perl(MIME::Base64)

%description
String eval is often used for dynamic code generation. 
For instance, Moose uses it heavily, to generate inlined 
versions of accessors and constructors, which speeds code up 
at runtime by a significant amount. String eval is not without 
its issues however - it's difficult to control the scope it's 
used in (which determines which variables are in scope inside the eval), 
and it's easy to miss compilation errors, since eval catches 
them and sticks them in $@ instead.

This module attempts to solve these problems. It provides an 
eval_closure function, which evals a string in a clean environment, 
other than a fixed list of specified variables. Compilation errors 
are rethrown automatically.

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
