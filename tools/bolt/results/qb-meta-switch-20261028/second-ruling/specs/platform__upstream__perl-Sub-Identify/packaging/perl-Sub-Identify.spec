Name:           perl-Sub-Identify
Version:        0.14
Release:        1
License:        Artistic-1.0 OR GPL-1.0-or-later
Summary:        Retrieve names of code references
Url:            https://metacpan.org/pod/Sub::Identify
Group:          Development/Libraries
Source0:        %{name}-%{version}.tar.gz
Source1001: 	perl-Sub-Identify.manifest
BuildRequires:  perl
BuildRequires:  perl(MIME::Base64)

%description
Sub::Identify allows you to retrieve the real name of code references.
It provides six functions, all of them taking a code reference.
sub_name returns the name of the code reference passed as an argument
(or __ANON__ if it's an anonymous code reference), stash_name 
returns its package, and sub_fullname returns the concatenation of the two.

get_code_info 
returns a list of two elements, the package and the subroutine name 
(in case of you want both and are worried by the speed.)

In case of subroutine aliasing, those functions always return the original name.
get_code_location returns a two-element list containing the file name 
and the line number where the subroutine has been defined.

is_sub_constant returns a boolean value indicating whether 
the subroutine is a constant or not.

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
%license README.mdown
