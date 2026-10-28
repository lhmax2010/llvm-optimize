Name:           perl-Devel-StackTrace
Version:        2.05
Release:        1
License:        Artistic-2.0
Summary:        An object representing a stack trace
Url:            https://metacpan.org/pod/Devel::StackTrace
Group:          Development/Libraries
Source0:        %{name}-%{version}.tar.gz
Source1001: 	perl-Devel-StackTrace.manifest
BuildRequires:  perl
BuildRequires:  perl(MIME::Base64)

%description
The Devel::StackTrace module contains two classes, 
Devel::StackTrace and Devel::StackTrace::Frame. These 
objects encapsulate the information that can 
retrieved via Perl's caller function, as well as 
providing a simple interface to this data.

The Devel::StackTrace object contains a set of 
Devel::StackTrace::Frame objects, one for each 
level of the stack. The frames contain all the 
data available from caller.
This code was created to support my 
Exception::Class::Base class (part of 
Exception::Class) but may be useful in other contexts.

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
