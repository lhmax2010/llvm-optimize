Name:           perl-Exception-Class
Version:        1.45
Release:        1
License:        Artistic-1.0 OR GPL-1.0-or-later
Summary:        A module that allows you to declare real exception classes in Perl
Url:            https://metacpan.org/pod/Exception::Class
Group:          Development/Libraries
Source0:        %{name}-%{version}.tar.gz
Source1001: 	perl-Exception-Class.manifest
BuildRequires:  perl
BuildRequires:  perl(MIME::Base64)

%description
RECOMMENDATION 1: If you are writing modern Perl 
code with Moose or Moo I highly recommend using Throwable 
instead of this module.
RECOMMENDATION 2: Whether or not you use Throwable, 
you should use Try::Tiny.
Exception::Class allows you to declare exception 
hierarchies in your modules in a "Java-esque" manner.
It features a simple interface allowing programmers to 'declare' 
1exception classes at compile time. It also has a base exception
class, Exception::Class::Base, that can be easily extended.
It is designed to make structured exception handling simpler
and better by encouraging people to use hierarchies of exceptions
in their applications, as opposed to a single catch-all exception class.
This module does not implement any try/catch syntax. Please see the
"OTHER EXCEPTION MODULES (try/catch syntax)" section for more 
information on how to get this syntax.
You will also want to look at the documentation for 
Exception::Class::Base, which is the default base class for 
all exception objects created by this module.

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
