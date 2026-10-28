Name:           perl-namespace-clean
Version:        0.27
Release:        1
License:        Artistic-1.0 OR GPL-1.0-or-later
Summary:        Keep imports and functions out of your namespace
Url:            https://metacpan.org/pod/namespace::clean
Group:          Development/Libraries
Source0:        %{name}-%{version}.tar.gz
Source1001: 	perl-namespace-clean.manifest
BuildRequires:  perl
BuildRequires:  perl(MIME::Base64)

%description
Keeping packages clean
When you define a function, or import one, into a Perl package, 
it will naturally also be available as a method. This does not 
per se cause problems, but it can complicate subclassing and, 
for example, plugin classes that are included via multiple 
inheritance by loading them as base classes.

The namespace::clean pragma will remove all previously declared
or imported symbols at the end of the current package's compile cycle.
Functions called in the package itself will still be bound by their name,
but they won't show up as methods on your class or instances.

By unimporting via no you can tell namespace::clean to start
collecting functions for the next use namespace::clean; specification.

You can use the -except flag to tell namespace::clean that you don't
want it to remove a certain function or method. A common use would be
a module exporting an import method along with some functions:

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
