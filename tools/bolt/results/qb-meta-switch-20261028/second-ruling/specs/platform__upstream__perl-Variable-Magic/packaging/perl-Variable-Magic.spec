Name:           perl-Variable-Magic
Version:        0.64
Release:        1
License:        Artistic-1.0 OR GPL-1.0-or-later
Summary:        Associate user-defined magic to variables from Perl.
Url:            https://metacpan.org/pod/Variable::Magic
Group:          Development/Libraries
Source0:        %{name}-%{version}.tar.gz
Source1001: 	perl-Variable-Magic.manifest
BuildRequires:  perl
BuildRequires:  perl(MIME::Base64)

%description
Magic is Perl's way of enhancing variables. This mechanism 
lets the user add extra data to any variable and hook 
syntactical operations (such as access, assignment or destruction) 
that can be applied to it. With this module, you can add 
your own magic to any variable without having to write a single line of XS.

You'll realize that these magic variables look a lot like tied variables. 
It is not surprising, as tied variables are implemented as a special 
kind of magic, just like any 'irregular' Perl variable : scalars like $!, 
$( or $^W, the %ENV and %SIG hashes, the @ISA array, vec() and substr() 
lvalues, threads::shared variables... They all share the same underlying 
C API, and this module gives you direct access to it.

%prep
%setup -q -n %{name}-%{version}
cp %{SOURCE1001} .

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
%perl_make_install
##perl_process_packlist
{
#!/bin/bash
if test -n "$RPM_BUILD_ROOT" -a -d $RPM_BUILD_ROOT%perl_vendorarch/auto; then
 find $RPM_BUILD_ROOT%perl_vendorarch/auto -name .packlist -print0 | xargs -0 -r rm
  if [ %{_target_cpu} == noarch ]; then
   find $RPM_BUILD_ROOT%perl_vendorarch/auto -depth -type d -print0 | xargs -0 -r rm -rf
  fi
fi
rm -f $RPM_BUILD_ROOT%{perl_archlib}/perllocal.pod
}

%perl_gen_filelist

%files -f %{name}.files
%license README
