Name:           perl-Class-Singleton
Version:        1.6
Release:        0
License:        Artistic-1.0 OR GPL-1.0-or-later
Summary:        Implementation of a "Singleton" class
Url:            https://metacpan.org/pod/Class::Singleton
Group:          Development/Libraries
Source0:        %{name}-%{version}.tar.gz
Source1001: 	perl-Class-Singleton.manifest
BuildRequires:  perl
BuildRequires:  perl(MIME::Base64)

%description
This is the Class::Singleton module. A Singleton describes
an object class that can have only one instance in any system.
An example of a Singleton might be a print spooler or 
system registry. This module implements a Singleton class 
from which other classes can be derived. By itself, 
the Class::Singleton module does very little other than manage
the instantiation of a single object. In deriving a class 
from Class::Singleton, your module will inherit the Singleton
instantiation method and can implement whatever specific 
functionality is required.

For a description and discussion of the Singleton class,
see "Design Patterns", Gamma et al, Addison-Wesley, 1995, ISBN 0-201-63361-2.

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
