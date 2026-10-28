Name:           perl-Capture-Tiny
Version:        0.48
Release:        0
License:        Apache-2.0
Summary:        Capture STDOUT and STDERR from Perl, XS or external programs
Url:            https://metacpan.org/pod/Capture::Tiny
Group:          Development/Libraries
Source0:        Capture-Tiny-%{version}.tar.gz
Source1001: 	perl-Capture-Tiny.manifest
BuildRequires:  perl
BuildRequires:  perl(MIME::Base64)

%description
Capture::Tiny provides a simple, portable way to capture almost anything
sent to STDOUT or STDERR, regardless of whether it comes from Perl, 
from XS code or from an external program. Optionally, output can be teed 
so that it is captured while being passed through to the original filehandles. 
 Yes, it even works on Windows (usually). Stop guessing which of a dozen 
capturing modules to use in any particular situation and just use this one.

%prep
%setup -q
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
