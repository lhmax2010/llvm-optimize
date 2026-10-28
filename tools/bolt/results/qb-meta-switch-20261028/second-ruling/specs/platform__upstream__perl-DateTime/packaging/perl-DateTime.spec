Name:           perl-DateTime
Version:        1.65
Release:        0
License:        Artistic License 2.0
Summary:        A date and time object for Perl
Url:            https://metacpan.org/pod/DateTime
Group:          Development/Libraries
Source0:        DateTime-%{version}.tar.gz
Source1001: 	perl-DateTime.manifest
BuildRequires:  perl
BuildRequires:  perl(MIME::Base64)

%description
DateTime is a class for the representation of date/time 
combinations, and is part of the Perl DateTime project.
It represents the Gregorian calendar, extended backwards 
in time before its creation (in 1582). This is sometimes 
known as the "proleptic Gregorian calendar". In this calendar, 
the first day of the calendar (the epoch), 
is the first day of year 1, which corresponds to the date which 
was (incorrectly) believed to be the birth of Jesus Christ.
The calendar represented does have a year 0, and in that way differs
from how dates are often written using "BCE/CE" or "BC/AD".
For infinite datetimes, please see the DateTime::Infinite module.

%prep
%setup -q
cp %{SOURCE1001} .

%build
perl Makefile.PL INSTALLDIRS=vendor OPTIMIZE="%{optflags}"
#make %#{?_smp_mflags}
%make_build

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
%license LICENSE
