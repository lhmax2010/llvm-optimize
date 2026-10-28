Name:           perl-Class-Data-Inheritable
Version:        0.10
Release:        0
License:        Artistic-1.0 OR GPL-1.0-or-later
Summary:        Inheritable, overridable class data
Url:            https://metacpan.org/pod/Class::Data::Inheritable
Group:          Development/Libraries
Source0:        %{name}-%{version}.tar.gz
Source1001: 	perl-Class-Data-Inheritable.manifest
BuildRequires:  perl
BuildRequires:  perl(MIME::Base64)

%description
Class::Data::Inheritable is for creating accessor/mutators to class data. 
That is, if you want to store something about your class as a whole 
(instead of about a single object). 
This data is then inherited by your subclasses and can be overridden.

For example:
  Pere::Ubu->mk_classdata('Suitcase');

will generate the method Suitcase() in the class Pere::Ubu.

This new method can be used to get and set a piece of class data.

 Pere::Ubu->Suitcase('Red');
 $suitcase = Pere::Ubu->Suitcase;

The interesting part happens when a class inherits from Pere::Ubu:

 package Raygun;
 use base qw(Pere::Ubu);

 # Raygun's suitcase is Red.
 $suitcase = Raygun->Suitcase;
 
Raygun inherits its Suitcase class data from Pere::Ubu.

Inheritance of class data works analogous to method inheritance. 
As long as Raygun does not "override" its inherited class data 
(by using Suitcase() to set a new value) it will continue 
to use whatever is set in Pere::Ubu and inherit further changes:

 # Both Raygun's and Pere::Ubu's suitcases are now Blue
 Pere::Ubu->Suitcase('Blue');

However, should Raygun decide to set its own Suitcase()
it has now "overridden" Pere::Ubu and is on its own, 
just like if it had overridden a method:

 # Raygun has an orange suitcase, Pere::Ubu's is still Blue.
 Raygun->Suitcase('Orange');

Now that Raygun has overridden Pere::Ubu further 
changes by Pere::Ubu no longer effect Raygun.

 # Raygun still has an orange suitcase, but Pere::Ubu is using Samsonite.
 Pere::Ubu->Suitcase('Samsonite');

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
