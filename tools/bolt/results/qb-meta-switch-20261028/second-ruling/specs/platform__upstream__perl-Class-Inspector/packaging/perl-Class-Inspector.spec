Name:           perl-Class-Inspector
Version:        1.36
Release:        0
License:        Artistic-1.0 OR GPL-1.0-or-later
Summary:        Get information about a class and its structure
Url:            https://metacpan.org/pod/Class::Inspector
Group:          Development/Libraries
Source0:        %{name}-%{version}.tar.gz
Source1001: 	perl-Class-Inspector.manifest
BuildRequires:  perl
BuildRequires:  perl(MIME::Base64)

%description
Class::Inspector allows you to get information about a loaded class. 
Most or all of this information can be found in other ways, 
but they aren't always very friendly, and usually involve a relatively 
high level of Perl wizardry, or strange and unusual looking code. 
Class::Inspector attempts to provide an easier, 
more friendly interface to this information.

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
